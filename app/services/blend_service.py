"""图层混合服务 - 模块化版本"""
from typing import Tuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import logger
from .blend import BlendController, BasicBlends, AdvancedBlends


class BlendService:
    """图层混合服务类 - 模块化版本"""
    
    @staticmethod
    def blend_images(
        base_image_bytes: bytes,
        blend_image_bytes: bytes,
        blend_mode: str = "normal",
        opacity: float = 1.0,
        quality: int = 90
    ) -> bytes:
        """统一的图片混合方法"""
        return BlendController.blend_images(
            base_image_bytes, blend_image_bytes, blend_mode, opacity, quality
        )
    
    @staticmethod
    def blend_normal(
        base_bytes: bytes,
        overlay_bytes: bytes,
        opacity: float = 1.0,
        position: Tuple[int, int] = (0, 0),
        quality: int = 90
    ) -> bytes:
        """正常混合模式"""
        return BasicBlends.blend_normal(base_bytes, overlay_bytes, opacity, position, quality)
    
    @staticmethod
    def blend_multiply(
        base_bytes: bytes,
        overlay_bytes: bytes,
        opacity: float = 1.0,
        quality: int = 90
    ) -> bytes:
        """正片叠底混合模式"""
        return BasicBlends.blend_multiply(base_bytes, overlay_bytes, opacity, quality)
    
    @staticmethod
    def blend_screen(
        base_bytes: bytes,
        overlay_bytes: bytes,
        opacity: float = 1.0,
        quality: int = 90
    ) -> bytes:
        """滤色混合模式"""
        return BasicBlends.blend_screen(base_bytes, overlay_bytes, opacity, quality)
    
    @staticmethod
    def blend_overlay(
        base_bytes: bytes,
        overlay_bytes: bytes,
        opacity: float = 1.0,
        quality: int = 90
    ) -> bytes:
        """叠加混合模式"""
        return AdvancedBlends.blend_overlay(base_bytes, overlay_bytes, opacity, quality)
    
    @staticmethod
    def blend_color_dodge(
        base_bytes: bytes,
        overlay_bytes: bytes,
        opacity: float = 1.0,
        quality: int = 90
    ) -> bytes:
        """颜色减淡混合模式"""
        return AdvancedBlends.blend_color_dodge(base_bytes, overlay_bytes, opacity, quality)
    
    @staticmethod
    def blend_color_burn(
        base_bytes: bytes,
        overlay_bytes: bytes,
        opacity: float = 1.0,
        quality: int = 90
    ) -> bytes:
        """颜色加深混合模式"""
        return AdvancedBlends.blend_color_burn(base_bytes, overlay_bytes, opacity, quality)
