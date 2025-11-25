from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends, Response
from app.services.watermark_service import WatermarkService
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
from app.utils.logger import logger
from .models import WatermarkByUrlRequest
from typing import Optional

router = APIRouter()


@router.post("/api/v1/watermark")
async def add_watermark(
    image: UploadFile = File(...),
    watermark_text: str = Form(...),
    position: str = Form("center"),
    font_size: int = Form(36),
    font_color: str = Form("#000000"),
    font_family: str = Form("Arial"),
    opacity: float = Form(0.5),
    margin_x: int = Form(20),
    margin_y: int = Form(20),
    rotation: int = Form(0),
    stroke_width: int = Form(0),
    stroke_color: str = Form("#000000"),
    shadow_offset_x: int = Form(0),
    shadow_offset_y: int = Form(0),
    shadow_color: str = Form("#000000"),
    repeat_mode: str = Form("none"),
    quality: int = Form(90),
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """
    为图片添加文字水印并上传到AIGC网盘

    Args:
        image: 上传的图片文件
        watermark_text: 水印文字
        position: 水印位置 (center, top-left, top-right, bottom-left, bottom-right)
        font_size: 字体大小
        font_color: 字体颜色 (十六进制格式，如 #000000)
        opacity: 透明度 (0.0-1.0)
        quality: 输出图像质量 (1-100)
        current_user: 当前用户

    Returns:
        处理后的图片响应
    """

    call_id = None
    try:
        # 读取图片内容
        image_content = await image.read()
        original_size = len(image_content)

        # 计算预估费用
        billing_info = calculate_upload_only_billing(primary_file_size=original_size, result_size=original_size)
        estimated_tokens = billing_info["total_cost"]
        
        # 准备请求上下文
        context = {
            "watermark_text": watermark_text,
            "position": position,
            "font_size": font_size,
            "font_color": font_color,
            "font_family": font_family,
            "opacity": opacity,
            "repeat_mode": repeat_mode,
            "filename": image.filename
        }
        
        # 生成详细备注
        remark = generate_operation_remark(
            "/api/v1/watermark", f"文字水印({watermark_text[:10]}...)", billing_info,
            水印文字=watermark_text[:20] + "..." if len(watermark_text) > 20 else watermark_text,
            位置=position,
            文件名=image.filename
        )
        
        # 预扣费 - 先付费再服务
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/watermark",
            context=context,
            estimated_tokens=estimated_tokens,
            remark=remark
        )
        
        if not call_id:
            raise HTTPException(
                status_code=402,
                detail="余额不足或预扣费失败，请检查账户余额"
            )

        # 处理水印
        result_bytes = WatermarkService.add_watermark(
            image_content,
            watermark_text,
            position,
            opacity,
            font_color,
            font_size,
            rotation,
            quality,
            font_family=font_family,
            margin_x=margin_x,
            margin_y=margin_y,
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            shadow_offset_x=shadow_offset_x,
            shadow_offset_y=shadow_offset_y,
            shadow_color=shadow_color,
            repeat_mode=repeat_mode
        )

        # 准备上传参数
        parameters = {
            "watermark_text": watermark_text,
            "position": position,
            "font_size": font_size,
            "font_color": font_color,
            "font_family": font_family,
            "opacity": opacity,
            "margin_x": margin_x,
            "margin_y": margin_y,
            "rotation": rotation,
            "stroke_width": stroke_width,
            "stroke_color": stroke_color,
            "shadow_offset_x": shadow_offset_x,
            "shadow_offset_y": shadow_offset_y,
            "shadow_color": shadow_color,
            "repeat_mode": repeat_mode,
            "quality": quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="watermark",
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
            message="文字水印处理并上传成功",
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
            await billing_service.refund_all(call_id, f"文字水印处理失败: {str(e)}")
        logger.error(f"文字水印处理异常: {type(e).__name__}: {str(e)}")
        import traceback
        logger.error(f"异常堆栈: {traceback.format_exc()}")
        return ApiResponse.error(
            message=f"水印处理失败: {type(e).__name__}: {str(e) or '未知错误'}",
            code=500
        )


@router.post("/api/v1/watermark-by-url")
async def add_watermark_by_url(
    request: WatermarkByUrlRequest,
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """
    通过URL为图片添加文字水印
    
    Args:
        request: 水印请求参数
        current_user: 当前用户
        
    Returns:
        处理后的图片响应
    """
    call_id = None
    try:
        # 下载图片
        image_content, content_type = ImageUtils.download_image_from_url(request.image_url)
        
        # 验证图片大小 (临时禁用)
        # if not ImageUtils.is_valid_image_size(image_content):
        #     raise HTTPException(status_code=400, detail="图片尺寸超出限制")
        
        # 计算预估费用
        billing_info = calculate_url_download_billing(len(image_content))
        estimated_tokens = billing_info["total_cost"]
        
        # 准备请求上下文
        context = {
            "image_url": request.image_url,
            "watermark_text": request.watermark_text,
            "position": request.position,
            "font_size": request.font_size,
            "opacity": request.opacity
        }
        
        # 生成详细备注
        remark = generate_operation_remark(
            "/api/v1/watermark/text", f"文字水印({request.watermark_text})", billing_info,
            图片URL=request.image_url,
            水印文字=request.watermark_text,
            位置=request.position
        )
        
        # 预扣费 - 先付费再服务
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/watermark/text",
            context=context,
            estimated_tokens=estimated_tokens,
            remark=remark
        )
        
        if not call_id:
            raise HTTPException(
                status_code=402,
                detail="余额不足或预扣费失败，请检查账户余额"
            )
        
        # 处理水印
        result_bytes = WatermarkService.add_watermark(
            image_content,
            request.watermark_text,
            request.position,
            request.opacity,
            request.font_color,
            request.font_size,
            request.rotation,
            request.quality,
            font_family=request.font_family,
            margin_x=request.margin_x,
            margin_y=request.margin_y,
            stroke_width=request.stroke_width,
            stroke_color=request.stroke_color,
            shadow_offset_x=request.shadow_offset_x,
            shadow_offset_y=request.shadow_offset_y,
            shadow_color=request.shadow_color,
            repeat_mode=request.repeat_mode
        )
        
        # 上传处理后的图片
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="watermark",
            parameters={
                "watermark_text": request.watermark_text,
                "position": request.position,
                "font_size": request.font_size,
                "opacity": request.opacity
            },
            original_filename=f"watermark_{ImageUtils.get_filename_from_url(request.image_url)}",
            content_type="image/jpeg"
        )

        if not upload_response:
            raise HTTPException(
                status_code=500,
                detail="文件上传失败：AIGC网盘服务不可用(502错误)，OSS备用上传也失败。请稍后重试或联系管理员。"
            )
        
        # 构造响应
        from ...schemas.response_models import FileInfo
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="水印添加成功",
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
            await billing_service.refund_all(call_id, f"文字水印处理失败: {str(e)}")
        logger.error(f"水印处理异常: {type(e).__name__}: {str(e)}")
        return ApiResponse.error(
            message=f"水印处理失败: {type(e).__name__}: {str(e) or '未知错误'}",
            code=500
        )



