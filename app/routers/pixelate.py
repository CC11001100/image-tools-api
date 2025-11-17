from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.pixelate_service import PixelateService
from ..services.file_upload_service import file_upload_service
from ..services.billing_service import billing_service
from ..utils.image_utils import ImageUtils
from ..utils.billing_utils import calculate_upload_only_billing, generate_operation_remark
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..middleware.auth_middleware import get_current_api_token
from typing import Optional
from pydantic import BaseModel

class PixelateByUrlRequest(BaseModel):
    """像素化URL请求模型"""
    image_url: str
    block_size: Optional[int] = 10
    region: Optional[str] = None
    quality: Optional[int] = 90

router = APIRouter(
    tags=["pixelate"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/pixelate")
async def pixelate_image(
    file: UploadFile = File(...),
    block_size: Optional[int] = Form(10),
    region: Optional[str] = Form(None),
    quality: Optional[int] = Form(90),
    api_token: str = Depends(get_current_api_token)
):
    """
    对图片进行像素化处理并上传到AIGC网盘
    """
    call_id = None
    try:
        contents = await file.read()
        
        # 计算预估费用
        billing_info = calculate_upload_only_billing(len(contents))
        estimated_tokens = billing_info["total_cost"]
        
        # 准备请求上下文
        context = {
            "block_size": block_size,
            "region": region,
            "quality": quality,
            "filename": file.filename,
            "file_size": len(contents)
        }
        
        # 生成详细备注
        remark = generate_operation_remark(
            "/api/v1/pixelate", f"图片像素化(块大小:{block_size})", billing_info,
            文件名=file.filename,
            块大小=block_size,
            区域=region or "全图"
        )
        
        # 预扣费 - 先付费再服务
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/pixelate",
            context=context,
            estimated_tokens=estimated_tokens,
            remark=remark
        )
        
        if not call_id:
            raise HTTPException(
                status_code=402,
                detail="余额不足或预扣费失败，请检查账户余额"
            )

        # 根据region参数选择处理方法
        if region:
            # 如果指定了区域，使用区域像素化
            # 这里简化处理，实际应该解析region参数
            result_bytes = PixelateService.pixelate_full(
                image_bytes=contents,
                pixel_size=block_size,
                quality=quality,
            )
        else:
            # 全图像素化
            result_bytes = PixelateService.pixelate_full(
                image_bytes=contents,
                pixel_size=block_size,
                quality=quality,
            )

        # 准备上传参数
        parameters = {
            "block_size": block_size,
            "region": region,
            "quality": quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="pixelate",
            parameters=parameters,
            original_filename=file.filename,
            content_type=file.content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="像素化处理并上传成功",
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
            await billing_service.refund_all(call_id, f"像素化处理失败: {str(e)}")
        return ApiResponse.error(
            message=str(e),
            code=500
        )

@router.post("/api/v1/pixelate-by-url")
async def pixelate_image_by_url(
    request: PixelateByUrlRequest = Body(..., description="像素化URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    对URL图片进行像素化处理并上传到AIGC网盘
    """
    call_id = None
    try:
        contents, content_type = ImageUtils.download_image_from_url(request.image_url)
        
        # 计算预估费用
        from ..utils.billing_utils import calculate_url_download_billing
        billing_info = calculate_url_download_billing(len(contents))
        estimated_tokens = billing_info["total_cost"]
        
        # 准备请求上下文
        context = {
            "image_url": request.image_url,
            "block_size": request.block_size,
            "region": request.region,
            "quality": request.quality,
            "download_size": len(contents)
        }
        
        # 生成详细备注
        remark = generate_operation_remark(
            "/api/v1/pixelate-by-url", f"URL图片像素化(块大小:{request.block_size})", billing_info,
            图片URL=request.image_url[:50] + "..." if len(request.image_url) > 50 else request.image_url,
            块大小=request.block_size,
            区域=request.region or "全图"
        )
        
        # 预扣费 - 先付费再服务
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/pixelate-by-url",
            context=context,
            estimated_tokens=estimated_tokens,
            remark=remark
        )
        
        if not call_id:
            raise HTTPException(
                status_code=402,
                detail="余额不足或预扣费失败，请检查账户余额"
            )

        # 根据region参数选择处理方法
        if request.region:
            # 如果指定了区域，使用区域像素化
            result_bytes = PixelateService.pixelate_full(
                image_bytes=contents,
                pixel_size=request.block_size,
                quality=request.quality,
            )
        else:
            # 全图像素化
            result_bytes = PixelateService.pixelate_full(
                image_bytes=contents,
                pixel_size=request.block_size,
                quality=request.quality,
            )

        # 准备上传参数
        parameters = {
            "image_url": request.image_url,
            "block_size": request.block_size,
            "region": request.region,
            "quality": request.quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="pixelate",
            parameters=parameters,
            original_filename=None,
            content_type="image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL像素化处理并上传成功",
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
            await billing_service.refund_all(call_id, f"URL像素化处理失败: {str(e)}")
        return ApiResponse.error(
            message=str(e),
            code=500
        )