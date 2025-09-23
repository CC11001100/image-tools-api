# 枚举统一导出 - 模块化版本
from .enums import (
    WatermarkPosition,
    FilterType,
    ArtFilterType,
    CropType,
    TransformType,
    ColorEffectType,
    EnhanceEffectType
)

# 保持向后兼容的导出
__all__ = [
    'WatermarkPosition',
    'FilterType',
    'ArtFilterType',
    'CropType',
    'TransformType',
    'ColorEffectType',
    'EnhanceEffectType'
]
