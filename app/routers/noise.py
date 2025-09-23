from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.noise_service import NoiseService
from ..services.file_upload_service import file_upload_service
from ..utils.image_utils import ImageUtils
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..middleware.auth_middleware import get_current_api_token
from typing import Optional
from pydantic import BaseModel

class NoiseByUrlRequest(BaseModel):
    """降噪URL请求模型"""
    image_url: str
    noise_type: str
    intensity: Optional[float] = 1.0
    quality: Optional[int] = 90

router = APIRouter(
    tags=["noise"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/noise")
async def reduce_noise(
    file: UploadFile = File(...),
    noise_type: str = Form(...),
    intensity: Optional[float] = Form(1.0),
    quality: Optional[int] = Form(90),
    api_token: str = Depends(get_current_api_token)
):
    """
    为上传的图片进行噪点处理并上传到AIGC网盘
    """

    try:
        contents = await file.read()
        result_bytes = NoiseService.add_noise(
            image_bytes=contents,
            noise_type=noise_type,
            intensity=intensity,
            quality=quality,
        )

        # 准备上传参数
        parameters = {
            "noise_type": noise_type,
            "intensity": intensity,
            "quality": quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="noise",
            parameters=parameters,
            original_filename=file.filename,
            content_type=file.content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="噪点处理并上传成功",
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

@router.post("/api/v1/noise-by-url")
async def reduce_noise_by_url(
    request: NoiseByUrlRequest = Body(..., description="降噪URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    为URL图片进行噪点处理并上传到AIGC网盘
    """
    try:
        contents, content_type = await ImageUtils.download_image_from_url(request.image_url)
        result_bytes = NoiseService.add_noise(
            image_bytes=contents,
            noise_type=request.noise_type,
            intensity=request.intensity,
            quality=request.quality,
        )

        # 准备上传参数
        parameters = {
            "noise_type": request.noise_type,
            "intensity": request.intensity,
            "quality": request.quality,
            "source_url": request.image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="noise",
            parameters=parameters,
            original_filename=None,
            content_type=content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL图片噪点处理并上传成功",
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


