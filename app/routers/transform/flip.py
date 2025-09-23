from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body
from typing import Optional
from ...services.image_service import ImageService
from ...utils.image_utils import ImageUtils
from ...schemas.response_models import ErrorResponse, ApiResponse
from fastapi.responses import Response
from pydantic import BaseModel

class FlipByUrlRequest(BaseModel):
    """翻转URL请求模型"""
    image_url: str
    quality: Optional[int] = 90

router = APIRouter(
    tags=["transform"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/transform/flip-horizontal")
async def flip_horizontal(
    file: UploadFile = File(...),
    quality: Optional[int] = Form(90),
):
    """水平翻转图片（镜像）"""
    try:
        contents = await file.read()
        result = ImageService.flip_horizontal(
            image_bytes=contents,
            quality=quality,
        )
        # 将图片转换为base64编码返回
        import base64
        result_base64 = base64.b64encode(result).decode('utf-8')
        
        return ApiResponse.success(
            message="处理成功",
            data={
                "image_data": result_base64,
                "content_type": file.content_type or "image/jpeg"
            }
        )
    except Exception as e:
        return ApiResponse.error(
            message=f"水平翻转失败: {str(e)}",
            code=500
        )

@router.post("/api/v1/transform/flip-horizontal-by-url")
async def flip_horizontal_by_url(
    request: FlipByUrlRequest = Body(..., description="水平翻转URL请求参数")
):
    """水平翻转URL图片"""
    try:
        contents, content_type = await ImageUtils.download_image_from_url(request.image_url)
        result = ImageService.flip_horizontal(
            image_bytes=contents,
            quality=request.quality,
        )
        # 将图片转换为base64编码返回
        import base64
        result_base64 = base64.b64encode(result).decode('utf-8')
        
        return ApiResponse.success(
            message="处理成功",
            data={
                "image_data": result_base64,
                "content_type": content_type or "image/jpeg"
            }
        )
    except Exception as e:
        return ApiResponse.error(
            message=f"URL水平翻转失败: {str(e)}",
            code=500
        )

@router.post("/api/v1/transform/flip-vertical")
async def flip_vertical(
    file: UploadFile = File(...),
    quality: Optional[int] = Form(90),
):
    """垂直翻转图片"""
    try:
        contents = await file.read()
        result = ImageService.flip_vertical(
            image_bytes=contents,
            quality=quality,
        )
        # 将图片转换为base64编码返回
        import base64
        result_base64 = base64.b64encode(result).decode('utf-8')
        
        return ApiResponse.success(
            message="处理成功",
            data={
                "image_data": result_base64,
                "content_type": file.content_type or "image/jpeg"
            }
        )
    except Exception as e:
        return ApiResponse.error(
            message=f"垂直翻转失败: {str(e)}",
            code=500
        )

@router.post("/api/v1/transform/flip-vertical-by-url")
async def flip_vertical_by_url(
    request: FlipByUrlRequest = Body(..., description="垂直翻转URL请求参数")
):
    """垂直翻转URL图片"""
    try:
        contents, content_type = await ImageUtils.download_image_from_url(request.image_url)
        result = ImageService.flip_vertical(
            image_bytes=contents,
            quality=request.quality,
        )
        # 将图片转换为base64编码返回
        import base64
        result_base64 = base64.b64encode(result).decode('utf-8')
        
        return ApiResponse.success(
            message="处理成功",
            data={
                "image_data": result_base64,
                "content_type": content_type or "image/jpeg"
            }
        )
    except Exception as e:
        return ApiResponse.error(
            message=f"垂直翻转失败: {str(e)}",
            code=500
        )