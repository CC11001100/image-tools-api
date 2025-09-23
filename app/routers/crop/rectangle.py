from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body
from typing import Optional
from ...services.image_service import ImageService
from ...utils.image_utils import ImageUtils
from ...schemas.request_models import CropRectangleRequest
from ...schemas.response_models import ErrorResponse, ApiResponse
from fastapi.responses import Response
from pydantic import BaseModel

class RectangleCropByUrlRequest(BaseModel):
    """矩形裁剪URL请求模型"""
    image_url: str
    x: int
    y: int
    width: int
    height: int
    quality: Optional[int] = 90

router = APIRouter(
    tags=["crop"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/crop/rectangle")
async def crop_rectangle(
    file: UploadFile = File(...),
    x: int = Form(...),
    y: int = Form(...),
    width: int = Form(...),
    height: int = Form(...),
    quality: Optional[int] = Form(90),
):
    """矩形裁剪图片"""
    try:
        contents = await file.read()
        result = ImageService.crop_rectangle(
            image_bytes=contents,
            x=x,
            y=y,
            width=width,
            height=height,
            quality=quality
        )

        # 将图片转换为base64编码返回
        import base64
        result_base64 = base64.b64encode(result).decode('utf-8')

        return ApiResponse.success(
            message="矩形裁剪成功",
            data={
                "image_data": result_base64,
                "content_type": file.content_type or "image/jpeg",
                "processing_info": {
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                    "quality": quality
                }
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/crop/rectangle-by-url")
async def crop_rectangle_by_url(
    request: RectangleCropByUrlRequest = Body(..., description="矩形裁剪URL请求参数")
):
    """矩形裁剪URL图片"""
    try:
        contents, content_type = await ImageUtils.download_image_from_url(request.image_url)
        result = ImageService.crop_rectangle(
            image_bytes=contents,
            x=request.x,
            y=request.y,
            width=request.width,
            height=request.height,
            quality=request.quality
        )

        # 将图片转换为base64编码返回
        import base64
        result_base64 = base64.b64encode(result).decode('utf-8')

        return ApiResponse.success(
            message="URL图片矩形裁剪成功",
            data={
                "image_data": result_base64,
                "content_type": content_type or "image/jpeg",
                "processing_info": {
                    "x": request.x,
                    "y": request.y,
                    "width": request.width,
                    "height": request.height,
                    "quality": request.quality,
                    "source_url": request.image_url
                }
            }
        )
    except Exception as e:
        return ApiResponse.error(
            message=f"矩形裁剪失败: {str(e)}",
            code=500
        )