from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from .enums import ColorEffectType, EnhanceEffectType


class ColorEffectRequest(BaseModel):
    """色彩效果请求模型"""
    effect_type: ColorEffectType = Field(..., description="色彩效果类型")
    intensity: float = Field(1.0, ge=0.0, le=3.0, description="效果强度")
    preserve_luminance: bool = Field(True, description="保留亮度")
    blend_mode: str = Field("normal", description="混合模式")
    mask_areas: Optional[List[Dict[str, Any]]] = Field(None, description="遮罩区域")


class EnhanceEffectRequest(BaseModel):
    """增强效果请求模型"""
    effect_type: EnhanceEffectType = Field(..., description="增强效果类型")
    intensity: float = Field(1.0, ge=0.0, le=3.0, description="效果强度")
    radius: Optional[float] = Field(None, ge=0.1, le=100.0, description="效果半径")
    threshold: Optional[float] = Field(None, ge=0.0, le=255.0, description="阈值")
    preserve_edges: bool = Field(True, description="保留边缘")
    adaptive: bool = Field(False, description="自适应处理")
    local_contrast: bool = Field(False, description="局部对比度增强")
    noise_reduction: bool = Field(False, description="降噪处理")
