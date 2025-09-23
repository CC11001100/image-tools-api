from pydantic import BaseModel, Field
from typing import Optional, List
from .enums import WatermarkPosition, FilterType, ArtFilterType


class WatermarkRequest(BaseModel):
    """水印请求模型"""
    text: str = Field(..., description="水印文字")
    position: WatermarkPosition = Field(WatermarkPosition.CENTER, description="水印位置")
    font_size: int = Field(36, ge=8, le=200, description="字体大小")
    font_color: str = Field("#000000", description="字体颜色")
    opacity: float = Field(0.5, ge=0.0, le=1.0, description="透明度")
    rotation: float = Field(0.0, ge=-360.0, le=360.0, description="旋转角度")
    font_family: str = Field("Arial", description="字体族")
    stroke_width: int = Field(0, ge=0, le=10, description="描边宽度")
    stroke_color: str = Field("#FFFFFF", description="描边颜色")
    shadow_offset_x: int = Field(0, description="阴影X偏移")
    shadow_offset_y: int = Field(0, description="阴影Y偏移")
    shadow_color: str = Field("#808080", description="阴影颜色")
    shadow_opacity: float = Field(0.0, ge=0.0, le=1.0, description="阴影透明度")


class ResizeRequest(BaseModel):
    """调整大小请求模型"""
    width: Optional[int] = Field(None, ge=1, le=8000, description="目标宽度")
    height: Optional[int] = Field(None, ge=1, le=8000, description="目标高度")
    maintain_aspect_ratio: bool = Field(True, description="保持宽高比")
    resample_method: str = Field("LANCZOS", description="重采样方法")
    background_color: str = Field("#FFFFFF", description="背景颜色")
    fit_mode: str = Field("contain", description="适应模式")


class FilterRequest(BaseModel):
    """滤镜请求模型"""
    filter_type: FilterType = Field(..., description="滤镜类型")
    intensity: float = Field(1.0, ge=0.0, le=5.0, description="滤镜强度")
    radius: Optional[float] = Field(None, ge=0.1, le=50.0, description="滤镜半径")
    threshold: Optional[float] = Field(None, ge=0.0, le=255.0, description="阈值")


class ArtFilterRequest(BaseModel):
    """艺术滤镜请求模型"""
    filter_type: ArtFilterType = Field(..., description="艺术滤镜类型")
    intensity: float = Field(1.0, ge=0.0, le=2.0, description="滤镜强度")
    style_strength: float = Field(1.0, ge=0.0, le=2.0, description="风格强度")
    preserve_details: bool = Field(True, description="保留细节")
    color_preservation: float = Field(0.5, ge=0.0, le=1.0, description="颜色保留度")
