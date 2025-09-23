from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body
from typing import Optional
from ...services.transform_service import TransformService
from ...utils.image_utils import ImageUtils
from ...schemas.response_models import ErrorResponse, ApiResponse
from fastapi.responses import Response
from pydantic import BaseModel

class RotateByUrlRequest(BaseModel):
    """图片旋转URL请求模型"""
    image_url: str
    angle: float
    expand: Optional[bool] = True
    quality: Optional[int] = 90

router = APIRouter(
    tags=["transform"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/transform/rotate")
async def rotate_image(
    file: UploadFile = File(...),
    angle: float = Form(...),
    expand: Optional[bool] = Form(True),
    quality: Optional[int] = Form(90),
):
    """旋转图片"""
    try:
        contents = await file.read()
        result = TransformService.rotate_image(
            image_bytes=contents,
            angle=angle,
            expand=expand,
            quality=quality
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
            message=f"图片旋转失败: {str(e)}",
            code=500
        )

@router.post("/api/v1/transform/rotate-by-url")
async def rotate_image_by_url(
    request: RotateByUrlRequest = Body(..., description="图片旋转URL请求参数")
):
    """旋转URL图片"""
    try:
        contents, content_type = await ImageUtils.download_image_from_url(request.image_url)
        result = TransformService.rotate_image(
            image_bytes=contents,
            angle=request.angle,
            expand=request.expand,
            quality=request.quality
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
            message=f"URL图片旋转失败: {str(e)}",
            code=500
        )