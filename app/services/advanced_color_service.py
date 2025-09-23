"""高级色彩调整服务 - 模块化版本"""
from typing import Tuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import logger
from .advanced_color import (
    ColorAdjustments,
    ToneProcessing,
    StyleEffects,
    SpecialEffects
)


class AdvancedColorService:
    """高级色彩调整服务类 - 模块化版本"""
    
    @staticmethod
    def apply_curves(image_bytes: bytes, curve_points: list = None, intensity: float = 1.0) -> bytes:
        """应用曲线调整"""
        return ColorAdjustments.apply_curves(image_bytes, curve_points, intensity)
    
    @staticmethod
    def apply_channel_mixer(image_bytes: bytes, red_weights: tuple = (1, 0, 0), 
                           green_weights: tuple = (0, 1, 0), blue_weights: tuple = (0, 0, 1)) -> bytes:
        """应用通道混合器"""
        return ColorAdjustments.apply_channel_mixer(
            image_bytes, red_weights, green_weights, blue_weights
        )
    
    @staticmethod
    def apply_split_toning(image_bytes: bytes, highlight_color: tuple = (255, 255, 200),
                          shadow_color: tuple = (100, 100, 150), intensity: float = 1.0) -> bytes:
        """分离色调"""
        return ToneProcessing.apply_split_toning(
            image_bytes, highlight_color, shadow_color, intensity
        )
    
    @staticmethod
    def apply_color_grading(image_bytes: bytes, shadows: tuple = (0, 0, 0),
                           midtones: tuple = (0, 0, 0), highlights: tuple = (0, 0, 0),
                           intensity: float = 1.0) -> bytes:
        """色彩分级"""
        return ToneProcessing.apply_color_grading(
            image_bytes, shadows, midtones, highlights, intensity
        )
    
    @staticmethod
    def apply_vintage_film(image_bytes: bytes, film_type: str = "kodachrome", intensity: float = 1.0) -> bytes:
        """胶片风格"""
        return StyleEffects.apply_vintage_film(image_bytes, film_type, intensity)
    
    @staticmethod
    def apply_cinematic_look(image_bytes: bytes, look_type: str = "orange_teal", intensity: float = 1.0) -> bytes:
        """电影级调色"""
        return StyleEffects.apply_cinematic_look(image_bytes, look_type, intensity)
    
    @staticmethod
    def apply_color_pop(image_bytes: bytes, target_color: tuple = (255, 0, 0),
                       tolerance: int = 50, intensity: float = 1.0) -> bytes:
        """色彩突出"""
        return SpecialEffects.apply_color_pop(
            image_bytes, target_color, tolerance, intensity
        )
    
    @staticmethod
    def apply_neon_colors(image_bytes: bytes, intensity: float = 1.0) -> bytes:
        """霓虹色彩效果"""
        return SpecialEffects.apply_neon_colors(image_bytes, intensity)
