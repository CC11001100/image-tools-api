# 请求模型统一导出 - 模块化版本
from .requests import *

# 为了保持向后兼容性，重新导出所有模型
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
