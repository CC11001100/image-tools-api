from pydantic import BaseModel, Field
from typing import List, Tuple, Optional
from .enums import CropType


class CropRectangleRequest(BaseModel):
    """矩形裁剪请求模型"""
    x: int = Field(..., ge=0, description="起始X坐标")
    y: int = Field(..., ge=0, description="起始Y坐标")
    width: int = Field(..., ge=1, description="裁剪宽度")
    height: int = Field(..., ge=1, description="裁剪高度")
    maintain_aspect_ratio: bool = Field(False, description="保持宽高比")
    background_color: str = Field("#FFFFFF", description="背景颜色")


class CropCircleRequest(BaseModel):
    """圆形裁剪请求模型"""
    center_x: int = Field(..., ge=0, description="圆心X坐标")
    center_y: int = Field(..., ge=0, description="圆心Y坐标")
    radius: int = Field(..., ge=1, description="圆半径")
    background_color: str = Field("#FFFFFF", description="背景颜色")
    anti_alias: bool = Field(True, description="抗锯齿")


class CropPolygonRequest(BaseModel):
    """多边形裁剪请求模型"""
    points: List[Tuple[int, int]] = Field(..., min_items=3, description="多边形顶点坐标列表")
    background_color: str = Field("#FFFFFF", description="背景颜色")
    anti_alias: bool = Field(True, description="抗锯齿")
    smooth_edges: bool = Field(False, description="平滑边缘")
    feather_radius: int = Field(0, ge=0, le=50, description="羽化半径")


class CropSmartCenterRequest(BaseModel):
    """智能居中裁剪请求模型"""
    target_width: int = Field(..., ge=1, le=8000, description="目标宽度")
    target_height: int = Field(..., ge=1, le=8000, description="目标高度")
    detection_method: str = Field("face", description="检测方法")
    fallback_position: str = Field("center", description="回退位置")
    padding: int = Field(0, ge=0, le=100, description="边距")
    min_face_size: int = Field(30, ge=10, le=200, description="最小人脸尺寸")
    confidence_threshold: float = Field(0.5, ge=0.1, le=1.0, description="置信度阈值")
