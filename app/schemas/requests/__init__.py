# 请求模型模块化导出

# 枚举类型
from .enums import (
    WatermarkPosition,
    FilterType,
    ArtFilterType,
    CropType,
    TransformType,
    ColorEffectType,
    EnhanceEffectType
)

# 基础请求模型
from .basic_requests import (
    WatermarkRequest,
    ResizeRequest,
    FilterRequest,
    ArtFilterRequest
)

# 裁剪请求模型
from .crop_requests import (
    CropRectangleRequest,
    CropCircleRequest,
    CropPolygonRequest,
    CropSmartCenterRequest
)

# 变换请求模型
from .transform_requests import (
    RotateRequest,
    FlipRequest
)

# 效果请求模型
from .effect_requests import (
    ColorEffectRequest,
    EnhanceEffectRequest
)

__all__ = [
    # 枚举类型
    'WatermarkPosition',
    'FilterType',
    'ArtFilterType',
    'CropType',
    'TransformType',
    'ColorEffectType',
    'EnhanceEffectType',
    
    # 基础请求模型
    'WatermarkRequest',
    'ResizeRequest',
    'FilterRequest',
    'ArtFilterRequest',
    
    # 裁剪请求模型
    'CropRectangleRequest',
    'CropCircleRequest',
    'CropPolygonRequest',
    'CropSmartCenterRequest',
    
    # 变换请求模型
    'RotateRequest',
    'FlipRequest',
    
    # 效果请求模型
    'ColorEffectRequest',
    'EnhanceEffectRequest'
]
