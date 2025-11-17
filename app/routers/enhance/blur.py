from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Body
from ...services.enhance_service import EnhanceService
from ...schemas.response_models import ErrorResponse, ApiResponse
from fastapi.responses import Response
from ...utils.image_utils import ImageUtils
from typing import Optional
from pydantic import BaseModel

class MotionBlurByUrlRequest(BaseModel):
    """运动模糊URL请求模型"""
    image_url: str
    angle: float = 0.0
    length: int = 15
    quality: int = 90

class RadialBlurByUrlRequest(BaseModel):
    """径向模糊URL请求模型"""
    image_url: str
    center_x: Optional[int] = None
    center_y: Optional[int] = None
    strength: float = 0.1
    quality: int = 90

class SurfaceBlurByUrlRequest(BaseModel):
    """表面模糊URL请求模型"""
    image_url: str
    radius: int = 5
    threshold: int = 50
    quality: int = 90

router = APIRouter(
    tags=["enhance"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/enhance/blur/motion")
async def motion_blur(
    file: UploadFile = File(...),
    angle: float = Form(0.0, ge=-180, le=180, description="运动角度（度）"),
    length: int = Form(15, ge=1, le=100, description="模糊长度"),
    quality: int = Form(90, ge=1, le=100, description="输出图像质量 (1-100)")
):
    """运动模糊效果"""
    try:
        contents = await file.read()
        result = EnhanceService.motion_blur(
            image_bytes=contents,
            angle=angle,
            length=length,
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
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/enhance/blur/motion-by-url")
async def motion_blur_by_url(
    request: MotionBlurByUrlRequest = Body(..., description="运动模糊URL请求参数")
):
    """运动模糊效果（URL方式）"""
    try:
        contents, content_type = ImageUtils.download_image_from_url(request.image_url)
        result = EnhanceService.motion_blur(
            image_bytes=contents,
            angle=request.angle,
            length=request.length,
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
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/enhance/blur/radial")
async def radial_blur(
    file: UploadFile = File(...),
    center_x: Optional[int] = Form(None, description="模糊中心X坐标（默认图片中心）"),
    center_y: Optional[int] = Form(None, description="模糊中心Y坐标（默认图片中心）"),
    strength: float = Form(0.1, ge=0, le=1, description="模糊强度"),
    quality: int = Form(90, ge=1, le=100, description="输出图像质量 (1-100)")
):
    """径向模糊效果"""
    try:
        contents = await file.read()
        result = EnhanceService.radial_blur(
            image_bytes=contents,
            center_x=center_x,
            center_y=center_y,
            strength=strength,
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
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/enhance/blur/radial-by-url")
async def radial_blur_by_url(
    request: RadialBlurByUrlRequest = Body(..., description="径向模糊URL请求参数")
):
    """径向模糊效果（URL方式）"""
    try:
        contents, content_type = ImageUtils.download_image_from_url(request.image_url)
        result = EnhanceService.radial_blur(
            image_bytes=contents,
            center_x=request.center_x,
            center_y=request.center_y,
            strength=request.strength,
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
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/enhance/blur/surface")
async def surface_blur(
    file: UploadFile = File(...),
    radius: int = Form(5, ge=1, le=50, description="模糊半径"),
    threshold: int = Form(50, ge=1, le=255, description="阈值（颜色差异阈值）"),
    quality: int = Form(90, ge=1, le=100, description="输出图像质量 (1-100)")
):
    """表面模糊（保留边缘）"""
    try:
        contents = await file.read()
        result = EnhanceService.surface_blur(
            image_bytes=contents,
            radius=radius,
            threshold=threshold,
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
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/enhance/blur/surface-by-url")
async def surface_blur_by_url(
    request: SurfaceBlurByUrlRequest = Body(..., description="表面模糊URL请求参数")
):
    """表面模糊（保留边缘）（URL方式）"""
    try:
        contents, content_type = ImageUtils.download_image_from_url(request.image_url)
        result = EnhanceService.surface_blur(
            image_bytes=contents,
            radius=request.radius,
            threshold=request.threshold,
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
        raise HTTPException(status_code=500, detail=str(e)) 