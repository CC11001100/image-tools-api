from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body
from typing import Optional
from ...services.image_service import ImageService
from ...utils.image_utils import ImageUtils
from ...schemas.response_models import ErrorResponse, ApiResponse
from fastapi.responses import Response
from pydantic import BaseModel

class SmartCropByUrlRequest(BaseModel):
    """智能裁剪URL请求模型"""
    image_url: str
    target_width: int
    target_height: int
    quality: Optional[int] = 90

router = APIRouter(
    tags=["crop"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/crop/smart")
async def crop_smart(
    file: UploadFile = File(...),
    target_width: int = Form(...),
    target_height: int = Form(...),
    quality: Optional[int] = Form(90),
):
    """智能居中裁剪图片到指定尺寸"""
    try:
        contents = await file.read()
        result = ImageService.crop_smart_center(
            image_bytes=contents,
            target_width=target_width,
            target_height=target_height,
            quality=quality
        )
        return Response(content=result, media_type=file.content_type or "image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/crop/smart-by-url")
async def crop_smart_by_url(
    request: SmartCropByUrlRequest = Body(..., description="智能裁剪URL请求参数")
):
    """智能居中裁剪URL图片到指定尺寸"""
    try:
        contents, content_type = ImageUtils.download_image_from_url(request.image_url)
        result = ImageService.crop_smart_center(
            image_bytes=contents,
            target_width=request.target_width,
            target_height=request.target_height,
            quality=request.quality
        )
        return Response(content=result, media_type=content_type or "image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 