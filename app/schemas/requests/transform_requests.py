from pydantic import BaseModel, Field
from typing import Optional, List, Tuple
from .enums import TransformType


class RotateRequest(BaseModel):
    """旋转请求模型"""
    angle: float = Field(..., description="旋转角度（度）")
    expand: bool = Field(True, description="是否扩展画布以适应旋转后的图像")
    center: Optional[Tuple[int, int]] = Field(None, description="旋转中心点坐标")
    background_color: str = Field("#FFFFFF", description="背景颜色")
    resample_method: str = Field("BICUBIC", description="重采样方法")
    auto_crop: bool = Field(False, description="自动裁剪空白区域")
    preserve_transparency: bool = Field(True, description="保留透明度")


class FlipRequest(BaseModel):
    """翻转请求模型"""
    horizontal: bool = Field(False, description="水平翻转")
    vertical: bool = Field(False, description="垂直翻转")
    preserve_metadata: bool = Field(True, description="保留元数据")
