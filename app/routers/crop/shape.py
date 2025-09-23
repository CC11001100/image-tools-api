from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from ...services.image_service import ImageService
from ...schemas.request_models import CropCircleRequest, CropPolygonRequest
from .base import CropImageHandler

from ...schemas.response_models import ApiResponse
router = APIRouter()


@router.post("/circle")
async def crop_circle(
    file: UploadFile = File(...),
    center_x: int = Form(...),
    center_y: int = Form(...),
    radius: int = Form(...),
    quality: Optional[int] = Form(90),
):
    """圆形裁剪图片"""
    # 验证并创建请求模型
    crop_request = CropCircleRequest(
        center_x=center_x, center_y=center_y, radius=radius, quality=quality
    )
    
    return await CropImageHandler.process_crop_upload(
        file=file,
        processor_func=ImageService.crop_circle,
        media_type_override="image/png",  # 圆形裁剪返回PNG格式（支持透明背景）
        center_x=crop_request.center_x,
        center_y=crop_request.center_y,
        radius=crop_request.radius,
        quality=crop_request.quality,
    )


@router.post("/circle-url")
async def crop_circle_url(
    image_url: str = Form(...),
    center_x: int = Form(...),
    center_y: int = Form(...),
    radius: int = Form(...),
    quality: Optional[int] = Form(90),
):
    """圆形裁剪图片 (通过URL)"""
    # 验证并创建请求模型
    crop_request = CropCircleRequest(
        center_x=center_x, center_y=center_y, radius=radius, quality=quality
    )
    
    return await CropImageHandler.process_crop_url(
        image_url=image_url,
        processor_func=ImageService.crop_circle,
        media_type_override="image/png",  # 圆形裁剪返回PNG格式（支持透明背景）
        center_x=crop_request.center_x,
        center_y=crop_request.center_y,
        radius=crop_request.radius,
        quality=crop_request.quality,
    )


@router.post("/polygon")
async def crop_polygon(
    file: UploadFile = File(...),
    points: str = Form(...),  # JSON字符串格式的坐标点
    quality: Optional[int] = Form(90),
):
    """
    多边形裁剪图片
    points格式: "[[x1,y1],[x2,y2],[x3,y3],...]"
    """
    # 解析坐标点
    points_tuples = CropImageHandler.parse_points(points)
    
    # 验证并创建请求模型
    crop_request = CropPolygonRequest(
        points=points_tuples, quality=quality
    )
    
    return await CropImageHandler.process_crop_upload(
        file=file,
        processor_func=ImageService.crop_polygon,
        media_type_override="image/png",  # 多边形裁剪返回PNG格式（支持透明背景）
        points=crop_request.points,
        quality=crop_request.quality,
    )


@router.post("/polygon-url")
async def crop_polygon_url(
    image_url: str = Form(...),
    points: str = Form(...),  # JSON字符串格式的坐标点
    quality: Optional[int] = Form(90),
):
    """
    多边形裁剪图片 (通过URL)
    points格式: "[[x1,y1],[x2,y2],[x3,y3],...]"
    """
    # 解析坐标点
    points_tuples = CropImageHandler.parse_points(points)
    
    # 验证并创建请求模型
    crop_request = CropPolygonRequest(
        points=points_tuples, quality=quality
    )
    
    return await CropImageHandler.process_crop_url(
        image_url=image_url,
        processor_func=ImageService.crop_polygon,
        media_type_override="image/png",  # 多边形裁剪返回PNG格式（支持透明背景）
        points=crop_request.points,
        quality=crop_request.quality,
    ) 