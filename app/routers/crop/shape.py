from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body
from typing import Optional
from ...services.image_service import ImageService
from ...utils.image_utils import ImageUtils
from ...schemas.response_models import ErrorResponse, ApiResponse
from pydantic import BaseModel
import base64

class CircleCropByUrlRequest(BaseModel):
    """圆形裁剪URL请求模型"""
    image_url: str
    center_x: int
    center_y: int
    radius: int
    quality: Optional[int] = 90

router = APIRouter(
    tags=["crop"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)


@router.post("/api/v1/crop/circle")
async def crop_circle(
    file: UploadFile = File(...),
    center_x: int = Form(...),
    center_y: int = Form(...),
    radius: int = Form(...),
    quality: Optional[int] = Form(90),
):
    """圆形裁剪图片"""
    try:
        contents = await file.read()
        result = ImageService.crop_circle(
            image_bytes=contents,
            center_x=center_x,
            center_y=center_y,
            radius=radius,
            quality=quality
        )

        # 将图片转换为base64编码返回
        result_base64 = base64.b64encode(result).decode('utf-8')

        return ApiResponse.success(
            message="圆形裁剪成功",
            data={
                "image_data": result_base64,
                "content_type": "image/png",  # 圆形裁剪返回PNG格式（支持透明背景）
                "processing_info": {
                    "center_x": center_x,
                    "center_y": center_y,
                    "radius": radius,
                    "quality": quality
                }
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/v1/crop/circle-by-url")
async def crop_circle_by_url(
    request: CircleCropByUrlRequest = Body(..., description="圆形裁剪URL请求参数")
):
    """圆形裁剪URL图片"""
    try:
        contents, content_type = ImageUtils.download_image_from_url(request.image_url)
        result = ImageService.crop_circle(
            image_bytes=contents,
            center_x=request.center_x,
            center_y=request.center_y,
            radius=request.radius,
            quality=request.quality
        )

        # 将图片转换为base64编码返回
        result_base64 = base64.b64encode(result).decode('utf-8')

        return ApiResponse.success(
            message="URL图片圆形裁剪成功",
            data={
                "image_data": result_base64,
                "content_type": "image/png",  # 圆形裁剪返回PNG格式（支持透明背景）
                "processing_info": {
                    "center_x": request.center_x,
                    "center_y": request.center_y,
                    "radius": request.radius,
                    "quality": request.quality,
                    "source_url": request.image_url
                }
            }
        )
    except Exception as e:
        return ApiResponse.error(
            message=f"圆形裁剪失败: {str(e)}",
            code=500
        )

