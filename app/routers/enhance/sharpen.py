from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Body
from fastapi.responses import Response
from ...services.enhance_service import EnhanceService
from ...schemas.response_models import ErrorResponse, ApiResponse
from fastapi.responses import Response
from ...utils.image_utils import ImageUtils
from typing import Optional
from pydantic import BaseModel

class UnsharpMaskByUrlRequest(BaseModel):
    """USM锐化URL请求模型"""
    image_url: str
    radius: float = 2.0
    amount: float = 150.0
    threshold: int = 3
    quality: int = 90

class SmartSharpenByUrlRequest(BaseModel):
    """智能锐化URL请求模型"""
    image_url: str
    amount: float = 1.5
    radius: float = 1.0
    noise_reduction: float = 0.1
    quality: int = 90

class EdgeSharpenByUrlRequest(BaseModel):
    """边缘锐化URL请求模型"""
    image_url: str
    strength: float = 1.0
    edge_threshold: int = 10
    quality: int = 90

router = APIRouter(
    tags=["enhance"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/enhance/sharpen/usm")
async def unsharp_mask(
    file: UploadFile = File(...),
    radius: float = Form(2.0, ge=0.1, le=10, description="模糊半径"),
    amount: float = Form(150.0, ge=0, le=500, description="锐化强度（百分比）"),
    threshold: int = Form(3, ge=0, le=255, description="阈值"),
    quality: int = Form(90, ge=1, le=100, description="输出图像质量 (1-100)")
):
    """USM锐化（非锐化遮罩）"""
    try:
        contents = await file.read()
        result = EnhanceService.unsharp_mask(
            image_bytes=contents,
            radius=radius,
            amount=amount,
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

@router.post("/api/v1/enhance/sharpen/usm-by-url")
async def unsharp_mask_by_url(
    request: UnsharpMaskByUrlRequest = Body(..., description="USM锐化URL请求参数")
):
    """USM锐化（非锐化遮罩）"""
    try:
        contents, content_type = await ImageUtils.download_image_from_url(request.image_url)
        result = EnhanceService.unsharp_mask(
            image_bytes=contents,
            radius=request.radius,
            amount=request.amount,
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

@router.post("/api/v1/enhance/sharpen/smart")
async def smart_sharpen(
    file: UploadFile = File(...),
    amount: float = Form(1.5, ge=0, le=5, description="锐化强度"),
    radius: float = Form(1.0, ge=0.1, le=5, description="锐化半径"),
    noise_reduction: float = Form(0.1, ge=0, le=1, description="噪点抑制"),
    quality: int = Form(90, ge=1, le=100, description="输出图像质量 (1-100)")
):
    """智能锐化"""
    try:
        contents = await file.read()
        result = EnhanceService.smart_sharpen(
            image_bytes=contents,
            amount=amount,
            radius=radius,
            noise_reduction=noise_reduction,
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

@router.post("/api/v1/enhance/sharpen/smart-by-url")
async def smart_sharpen_by_url(
    request: SmartSharpenByUrlRequest = Body(..., description="智能锐化URL请求参数")
):
    """智能锐化"""
    try:
        contents, content_type = await ImageUtils.download_image_from_url(request.image_url)
        result = EnhanceService.smart_sharpen(
            image_bytes=contents,
            amount=request.amount,
            radius=request.radius,
            noise_reduction=request.noise_reduction,
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

@router.post("/api/v1/enhance/sharpen/edge")
async def edge_sharpen(
    file: UploadFile = File(...),
    strength: float = Form(1.0, ge=0, le=3, description="锐化强度"),
    edge_threshold: int = Form(10, ge=1, le=100, description="边缘检测阈值"),
    quality: int = Form(90, ge=1, le=100, description="输出图像质量 (1-100)")
):
    """边缘锐化"""
    try:
        contents = await file.read()
        result = EnhanceService.edge_sharpen(
            image_bytes=contents,
            strength=strength,
            edge_threshold=edge_threshold,
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

@router.post("/api/v1/enhance/sharpen/edge-by-url")
async def edge_sharpen_by_url(
    request: EdgeSharpenByUrlRequest = Body(..., description="边缘锐化URL请求参数")
):
    """边缘锐化"""
    try:
        contents, content_type = await ImageUtils.download_image_from_url(request.image_url)
        result = EnhanceService.edge_sharpen(
            image_bytes=contents,
            strength=request.strength,
            edge_threshold=request.edge_threshold,
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