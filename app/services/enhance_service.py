from typing import Optional, Tuple
from ..utils.logger import logger
from .enhance import (
    BlurEffects,
    SharpenEffects,
    MainEnhance
)


class EnhanceService:
    """图像增强服务 - 模块化版本"""

    # 模糊效果方法
    @staticmethod
    def motion_blur(image_bytes: bytes, angle: float = 0.0, length: int = 15, quality: int = 90) -> bytes:
        """运动模糊效果"""
        return BlurEffects.motion_blur(image_bytes, angle, length, quality)

    @staticmethod
    def radial_blur(image_bytes: bytes, center_x: Optional[int] = None, center_y: Optional[int] = None,
                   strength: float = 5.0, quality: int = 90) -> bytes:
        """径向模糊效果"""
        return BlurEffects.radial_blur(image_bytes, center_x, center_y, strength, quality)

    @staticmethod
    def surface_blur(image_bytes: bytes, radius: int = 5, threshold: int = 15, quality: int = 90) -> bytes:
        """表面模糊效果（保边模糊）"""
        return BlurEffects.surface_blur(image_bytes, radius, threshold, quality)

    # 锐化效果方法
    @staticmethod
    def unsharp_mask(image_bytes: bytes, radius: float = 1.0, amount: float = 1.0,
                    threshold: int = 0, quality: int = 90) -> bytes:
        """USM锐化（反锐化掩模）"""
        return SharpenEffects.unsharp_mask(image_bytes, radius, amount, threshold, quality)

    @staticmethod
    def smart_sharpen(image_bytes: bytes, amount: float = 100.0, radius: float = 1.0,
                     noise_reduction: float = 0.0, quality: int = 90) -> bytes:
        """智能锐化"""
        return SharpenEffects.smart_sharpen(image_bytes, amount, radius, noise_reduction, quality)

    @staticmethod
    def edge_sharpen(image_bytes: bytes, strength: float = 1.0, quality: int = 90) -> bytes:
        """边缘锐化"""
        return SharpenEffects.edge_sharpen(image_bytes, strength, quality)

    # 主要方法
    @staticmethod
    def apply_enhance_effect(image_bytes: bytes, effect_type: str, **kwargs) -> bytes:
        """应用增强效果"""
        return MainEnhance.apply_enhance_effect(image_bytes, effect_type, **kwargs)

    @staticmethod
    def _apply_simple_enhance(image_bytes: bytes, effect_type: str, intensity: float, quality: int) -> bytes:
        """应用简单增强效果"""
        return MainEnhance._apply_simple_enhance(image_bytes, effect_type, intensity, quality)
