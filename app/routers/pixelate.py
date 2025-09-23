from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.pixelate_service import PixelateService
from ..services.file_upload_service import file_upload_service
from ..utils.image_utils import ImageUtils
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

    try:
        contents = await file.read()
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
                "processing_info": parameters
            }
        )
    except Exception as e:
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
    try:
        contents, content_type = await ImageUtils.download_image_from_url(request.image_url)
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
            "block_size": request.block_size,
            "region": request.region,
            "quality": request.quality,
            "source_url": request.image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="pixelate",
            parameters=parameters,
            original_filename=None,
            content_type=content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL图片像素化处理并上传成功",
            data={
                "file": file_info.dict(),
                "processing_info": parameters
        
            }
        )
    except Exception as e:
        return ApiResponse.error(
            message=str(e),
            code=500
        )