from typing import Optional, Tuple, Dict, Any
from ..utils.logger import logger
from .advanced_color_service import AdvancedColorService
from .color import (
    BasicColorAdjustments,
    ColorEffects,
    SpecialEffects,
    StyleEffects,
    MainAdjustments
)


class ColorService:
    """色彩调整服务 - 模块化版本"""

    # 基础色彩调整方法
    @staticmethod
    def adjust_hue_saturation(image_bytes: bytes, hue_shift: float = 0.0, saturation: float = 1.0, quality: int = 90) -> bytes:
        """调整色相和饱和度"""
        return BasicColorAdjustments.adjust_hue_saturation(image_bytes, hue_shift, saturation, quality)

    @staticmethod
    def adjust_color_balance(image_bytes: bytes, shadows: Tuple[float, float, float] = (0.0, 0.0, 0.0),
                           midtones: Tuple[float, float, float] = (0.0, 0.0, 0.0),
                           highlights: Tuple[float, float, float] = (0.0, 0.0, 0.0), quality: int = 90) -> bytes:
        """调整色彩平衡"""
        return BasicColorAdjustments.adjust_color_balance(image_bytes, shadows, midtones, highlights, quality)

    @staticmethod
    def adjust_levels(image_bytes: bytes, input_black: int = 0, input_white: int = 255, gamma: float = 1.0,
                     output_black: int = 0, output_white: int = 255, quality: int = 90) -> bytes:
        """调整色阶"""
        return BasicColorAdjustments.adjust_levels(image_bytes, input_black, input_white, gamma, output_black, output_white, quality)

    @staticmethod
    def auto_color_correct(image_bytes: bytes, quality: int = 90) -> bytes:
        """自动色彩校正"""
        return BasicColorAdjustments.auto_color_correct(image_bytes, quality)

    @staticmethod
    def adjust_temperature_tint(image_bytes: bytes, temperature: float = 0.0, tint: float = 0.0, quality: int = 90) -> bytes:
        """调整色温和色调"""
        return BasicColorAdjustments.adjust_temperature_tint(image_bytes, temperature, tint, quality)

    @staticmethod
    def create_duotone(image_bytes: bytes, shadow_color: Tuple[int, int, int] = (0, 0, 0),
                      highlight_color: Tuple[int, int, int] = (255, 255, 255), quality: int = 90) -> bytes:
        """创建双色调效果"""
        return BasicColorAdjustments.create_duotone(image_bytes, shadow_color, highlight_color, quality)

    # 主要调整方法
    @staticmethod
    def adjust_color(image_bytes: bytes, brightness: float = 0.0, contrast: float = 0.0, saturation: float = 0.0,
                    hue: float = 0.0, gamma: float = 1.0, shadows: float = 0.0, highlights: float = 0.0, quality: int = 90) -> bytes:
        """综合色彩调整"""
        return MainAdjustments.adjust_color(image_bytes, brightness, contrast, saturation, hue, gamma, shadows, highlights, quality)

    @staticmethod
    def apply_color_effect(image_bytes: bytes, effect_type: str, intensity: float = 1.0, quality: int = 90) -> bytes:
        """应用色彩效果"""
        return MainAdjustments.apply_color_effect(image_bytes, effect_type, intensity, quality)

    # 私有方法（保持向后兼容）
    @staticmethod
    def _apply_pop_art(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用波普艺术效果"""
        return ColorEffects.apply_pop_art(image_bytes, intensity, quality)

    @staticmethod
    def _apply_pastel_colors(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用粉彩色效果"""
        return ColorEffects.apply_pastel_colors(image_bytes, intensity, quality)

    @staticmethod
    def _apply_vibrant_colors(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用鲜艳色彩效果"""
        return ColorEffects.apply_vibrant_colors(image_bytes, intensity, quality)

    @staticmethod
    def _apply_muted_colors(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用柔和色彩效果"""
        return ColorEffects.apply_muted_colors(image_bytes, intensity, quality)

    @staticmethod
    def _apply_earth_tones(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用大地色调效果"""
        return ColorEffects.apply_earth_tones(image_bytes, intensity, quality)

    @staticmethod
    def _apply_cool_tones(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用冷色调效果"""
        return ColorEffects.apply_cool_tones(image_bytes, intensity, quality)

    @staticmethod
    def _apply_warm_tones(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用暖色调效果"""
        return ColorEffects.apply_warm_tones(image_bytes, intensity, quality)

    @staticmethod
    def _apply_monochrome(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用单色效果"""
        return ColorEffects.apply_monochrome(image_bytes, intensity, quality)

    @staticmethod
    def _apply_infrared(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用红外效果"""
        return ColorEffects.apply_infrared(image_bytes, intensity, quality)

    @staticmethod
    def _apply_night_vision(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用夜视效果"""
        return ColorEffects.apply_night_vision(image_bytes, intensity, quality)

    @staticmethod
    def _apply_thermal(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用热成像效果"""
        return SpecialEffects.apply_thermal(image_bytes, intensity, quality)

    @staticmethod
    def _apply_saturation_boost(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用饱和度增强效果"""
        return SpecialEffects.apply_saturation_boost(image_bytes, intensity, quality)

    @staticmethod
    def _apply_contrast_enhance(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用对比度增强效果"""
        return SpecialEffects.apply_contrast_enhance(image_bytes, intensity, quality)

    @staticmethod
    def _apply_brightness_adjust(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用亮度调整效果"""
        return SpecialEffects.apply_brightness_adjust(image_bytes, intensity, quality)

    @staticmethod
    def _apply_vibrance(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用自然饱和度效果"""
        return SpecialEffects.apply_vibrance(image_bytes, intensity, quality)

    @staticmethod
    def _apply_rainbow_effect(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用彩虹效果"""
        return SpecialEffects.apply_rainbow_effect(image_bytes, intensity, quality)

    @staticmethod
    def _apply_sunset_effect(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用日落效果"""
        return SpecialEffects.apply_sunset_effect(image_bytes, intensity, quality)

    @staticmethod
    def _apply_ocean_effect(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用海洋效果"""
        return SpecialEffects.apply_ocean_effect(image_bytes, intensity, quality)

    @staticmethod
    def _apply_sepia_tone(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用棕褐色调效果"""
        return StyleEffects.apply_sepia_tone(image_bytes, intensity, quality)

    @staticmethod
    def _apply_cyanotype(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用蓝晒效果"""
        return StyleEffects.apply_cyanotype(image_bytes, intensity, quality)

    @staticmethod
    def _apply_instagram_vintage(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用Instagram复古效果"""
        return StyleEffects.apply_instagram_vintage(image_bytes, intensity, quality)

    @staticmethod
    def _apply_vsco_film(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用VSCO胶片效果"""
        return StyleEffects.apply_vsco_film(image_bytes, intensity, quality)
