from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from app.services.watermark_service import WatermarkService
from app.services.overlay.logo_watermark import LogoWatermarkService
from app.services.file_upload_service import file_upload_service
from app.services.billing_service import billing_service
from app.utils.image_utils import ImageUtils
from app.utils.billing_utils import (
    calculate_upload_only_billing, calculate_url_download_billing,
    calculate_dual_upload_billing, calculate_mixed_mode_billing,
    generate_operation_remark
)
from app.schemas.response_models import ErrorResponse, ImageProcessResponse, FileInfo, ApiResponse
from app.schemas.user_models import User
from app.middleware.auth_middleware import get_current_user, get_current_api_token
from .models import ImageWatermarkByUrlRequest
from typing import Optional
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/api/v1/watermark/image")
async def add_image_watermark(
    image: UploadFile = File(...),
    watermark_image: UploadFile = File(...),
    position: str = Form("center"),
    opacity: float = Form(0.5),
    scale: float = Form(1.0),
    quality: int = Form(90),
    api_token: str = Depends(get_current_api_token)
):
    """
    为图片添加图片水印

    Args:
        image: 主图片文件
        watermark_image: 水印图片文件
        position: 水印位置 (center, top-left, top-right, bottom-left, bottom-right)
        opacity: 透明度 (0.0-1.0)
        scale: 水印缩放比例
        quality: 输出图像质量 (1-100)

    Returns:
        处理后的图片响应
    """

    call_id = None
    try:
        # 读取图片内容
        image_content = await image.read()
        watermark_content = await watermark_image.read()

        # 计算预估费用
        total_input_size = len(image_content) + len(watermark_content)
        billing_info = calculate_dual_upload_billing(len(image_content), len(watermark_content))
        estimated_tokens = billing_info["total_cost"]
        
        # 准备请求上下文
        context = {
            "position": position,
            "opacity": opacity,
            "scale": scale,
            "quality": quality,
            "main_image_filename": image.filename,
            "watermark_image_filename": watermark_image.filename
        }
        
        # 生成详细备注
        remark = generate_operation_remark(
            "/api/v1/watermark/image", f"图片水印({position})", billing_info,
            主图片=image.filename,
            水印图片=watermark_image.filename,
            位置=position
        )
        
        # 预扣费 - 先付费再服务
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/watermark/image",
            context=context,
            estimated_tokens=estimated_tokens,
            remark=remark
        )
        
        if not call_id:
            raise HTTPException(
                status_code=402,
                detail="余额不足或预扣费失败，请检查账户余额"
            )
        
        # 处理图片水印
        # 打开图片
        base_image = Image.open(io.BytesIO(image_content))
        watermark_image = Image.open(io.BytesIO(watermark_content))

        # 调用LogoWatermarkService处理图片水印
        result_image = LogoWatermarkService.add_image_watermark(
            base_image,
            watermark_image,
            opacity=opacity,
            tile=False,
            spacing=50
        )

        # 转换为字节数据
        output = io.BytesIO()
        result_image.save(output, format="JPEG", quality=quality)
        result_bytes = output.getvalue()
        
        # 准备上传参数
        parameters = {
            "position": position,
            "opacity": opacity,
            "scale": scale,
            "quality": quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="image_watermark",
            parameters=parameters,
            original_filename=image.filename,
            content_type=image.content_type or "image/jpeg"
        )

        if not upload_response:
            logger.error("文件上传失败")
            raise HTTPException(status_code=500, detail="文件上传失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="图片水印处理并上传成功",
            data={
                "file_info": file_info.dict(),
                "processing_info": parameters,
                "billing_info": billing_info
            }
        )
        
    except HTTPException:
        if call_id:
            await billing_service.refund_all(call_id, "HTTP异常，退还费用")
        raise
    except Exception as e:
        if call_id:
            await billing_service.refund_all(call_id, f"图片水印处理失败: {str(e)}")
        logger.error(f"图片水印处理异常: {type(e).__name__}: {str(e)}")
        return ApiResponse.error(
            message=f"图片水印处理失败: {type(e).__name__}: {str(e) or '未知错误'}",
            code=500
        )


@router.post("/api/v1/watermark/image-by-url")
async def add_image_watermark_by_url(
    request: ImageWatermarkByUrlRequest,
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """
    通过URL为图片添加图片水印
    
    Args:
        request: 图片水印请求参数
        current_user: 当前用户
        
    Returns:
        处理后的图片响应
    """
    call_id = None
    try:
        # 下载主图片和水印图片
        image_content = ImageUtils.download_image_from_url(request.image_url)
        watermark_content = ImageUtils.download_image_from_url(request.watermark_image_url)
        
        # 验证图片大小
        if not ImageUtils.is_valid_image_size(image_content):
            raise HTTPException(status_code=400, detail="主图片尺寸超出限制")
        
        if not ImageUtils.is_valid_image_size(watermark_content):
            raise HTTPException(status_code=400, detail="水印图片尺寸超出限制")
        
        # 计算预估费用
        total_input_size = len(image_content) + len(watermark_content)
        billing_info = calculate_mixed_mode_billing(len(image_content), len(watermark_content))
        estimated_tokens = billing_info["total_cost"]
        
        # 准备请求上下文
        context = {
            "image_url": request.image_url,
            "watermark_image_url": request.watermark_image_url,
            "position": request.position,
            "opacity": request.opacity,
            "scale": request.scale
        }
        
        # 生成详细备注
        remark = generate_operation_remark(
            "/api/v1/watermark/image", f"图片水印({request.position})", billing_info,
            主图片URL=request.image_url,
            水印图片URL=request.watermark_image_url,
            位置=request.position
        )
        
        # 预扣费 - 先付费再服务
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/watermark/image",
            context=context,
            estimated_tokens=estimated_tokens,
            remark=remark
        )
        
        if not call_id:
            raise HTTPException(
                status_code=402,
                detail="余额不足或预扣费失败，请检查账户余额"
            )
        
        # 处理图片水印
        result_bytes = WatermarkService.add_image_watermark(
            image_content,
            watermark_content,
            request.position,
            request.opacity,
            request.scale,
            request.quality
        )
        
        # 上传处理后的图片
        file_info = await file_upload_service.upload_processed_image(
            result_bytes,
            f"watermark_{ImageUtils.get_filename_from_url(request.image_url)}",
            current_user.id
        )
        
        return ApiResponse.success(
            message="图片水印添加成功",
            data={
                "file": file_info.dict(),
                "billing_info": billing_info
            }
        )
        
    except HTTPException:
        if call_id:
            await billing_service.refund_all(call_id, "HTTP异常，退还费用")
        raise
    except Exception as e:
        if call_id:
            await billing_service.refund_all(call_id, f"图片水印处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图片水印处理失败: {str(e)}")
