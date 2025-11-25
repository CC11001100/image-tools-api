from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ...services.enhance_service import EnhanceService
from ...services.file_upload_service import file_upload_service
from ...utils.image_utils import ImageUtils
from ...utils.logger import logger
from ...schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ...middleware.auth_middleware import get_current_api_token
from typing import Optional
from pydantic import BaseModel

class EnhanceByUrlRequest(BaseModel):
    """图片增强URL请求模型"""
    image_url: str
    enhance_type: str
    intensity: Optional[float] = 1.0
    quality: Optional[int] = 90

router = APIRouter(
    tags=["enhance"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/enhance")
async def enhance_image(
    file: UploadFile = File(...),
    enhance_type: str = Form(...),
    intensity: Optional[float] = Form(1.0),
    quality: Optional[int] = Form(90),
    api_token: str = Depends(get_current_api_token)
):
    """
    增强上传的图片并上传到AIGC网盘
    """

    try:
        contents = await file.read()
        result_bytes = EnhanceService.apply_enhance_effect(
            image_bytes=contents,
            effect_type=enhance_type,
            intensity=intensity,
            quality=quality,
        )

        # 准备上传参数
        parameters = {
            "enhance_type": enhance_type,
            "intensity": intensity,
            "quality": quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="enhance",
            parameters=parameters,
            original_filename=file.filename,
            content_type=file.content_type or "image/jpeg"
        )

        if not upload_response:
            logger.error("文件上传失败")
            raise HTTPException(status_code=500, detail="文件上传失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="图片增强处理并上传成功",
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

@router.post("/api/v1/enhance-by-url")
async def enhance_image_by_url(
    request: EnhanceByUrlRequest = Body(..., description="图片增强URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    增强URL图片并上传到AIGC网盘
    """
    try:
        contents, content_type = ImageUtils.download_image_from_url(request.image_url)
        result_bytes = EnhanceService.apply_enhance_effect(
            image_bytes=contents,
            effect_type=request.enhance_type,
            intensity=request.intensity,
            quality=request.quality,
        )

        # 准备上传参数
        parameters = {
            "enhance_type": request.enhance_type,
            "intensity": request.intensity,
            "quality": request.quality,
            "source_url": request.image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="enhance",
            parameters=parameters,
            original_filename=None,
            content_type=content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL图片增强处理并上传成功",
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

