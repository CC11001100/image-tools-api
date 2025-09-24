from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.blend_service import BlendService
from ..services.file_upload_service import file_upload_service
from ..utils.image_utils import ImageUtils
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..middleware.auth_middleware import get_current_api_token
from typing import Optional
from pydantic import BaseModel

class BlendByUrlRequest(BaseModel):
    """图片混合URL请求模型"""
    base_image_url: str
    blend_image_url: str
    blend_mode: str
    opacity: Optional[float] = 1.0
    quality: Optional[int] = 90

router = APIRouter(
    tags=["blend"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/blend")
async def blend_images(
    base_image: UploadFile = File(..., description="基础图片文件"),
    blend_image: UploadFile = File(..., description="混合图片文件"),
    blend_mode: str = Form(..., description="混合模式"),
    opacity: Optional[float] = Form(1.0, description="混合透明度"),
    quality: Optional[int] = Form(90, description="输出图像质量"),
    api_token: str = Depends(get_current_api_token)
):
    """
    混合两张上传的图片并上传到AIGC网盘
    """

    try:
        base_contents = await base_image.read()
        blend_contents = await blend_image.read()
        result_bytes = BlendService.blend_images(
            base_image_bytes=base_contents,
            blend_image_bytes=blend_contents,
            blend_mode=blend_mode,
            opacity=opacity,
            quality=quality,
        )

        # 准备上传参数
        parameters = {
            "blend_mode": blend_mode,
            "opacity": opacity,
            "quality": quality,
            "base_filename": base_image.filename,
            "blend_filename": blend_image.filename
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="blend",
            parameters=parameters,
            original_filename=f"{base_image.filename}_blend_{blend_image.filename}",
            content_type=base_image.content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="图片混合处理并上传成功",
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

@router.post("/api/v1/blend-by-url")
async def blend_images_by_url(
    request: BlendByUrlRequest = Body(..., description="图片混合URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    混合两张URL图片并上传到AIGC网盘
    """
    try:
        base_contents, base_content_type = await ImageUtils.download_image_from_url(request.base_image_url)
        blend_contents, _ = await ImageUtils.download_image_from_url(request.blend_image_url)
        result_bytes = BlendService.blend_images(
            base_image_bytes=base_contents,
            blend_image_bytes=blend_contents,
            blend_mode=request.blend_mode,
            opacity=request.opacity,
            quality=request.quality,
        )

        # 准备上传参数
        parameters = {
            "blend_mode": request.blend_mode,
            "opacity": request.opacity,
            "quality": request.quality,
            "base_image_url": request.base_image_url,
            "blend_image_url": request.blend_image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="blend",
            parameters=parameters,
            original_filename=None,
            content_type=base_content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL图片混合处理并上传成功",
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

