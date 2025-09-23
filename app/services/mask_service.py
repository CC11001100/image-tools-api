"""蒙版处理服务 - 模块化版本"""
from PIL import Image
from typing import Tuple, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import logger
from .mask import (
    BasicMasks,
    ClippingMasks,
    GradientMasks,
    ShapeMasks,
    MaskUtils
)


class MaskService:
    """蒙版处理服务类 - 模块化版本"""
    
    @staticmethod
    def apply_mask(
        image_bytes: bytes,
        mask_type: str,
        feather: int = 0,
        invert: bool = False,
        background_color: str = "#FFFFFF",
        opacity: float = 1.0,
        quality: int = 90,
        **kwargs
    ) -> bytes:
        """应用遮罩到图片"""
        return BasicMasks.apply_mask(
            image_bytes, mask_type, feather, invert, 
            background_color, opacity, quality, **kwargs
        )
    
    @staticmethod
    def apply_layer_mask(
        base_image_bytes: bytes,
        overlay_image_bytes: bytes,
        mask_bytes: bytes,
        blend_mode: str = "normal",
        opacity: float = 1.0,
        quality: int = 90
    ) -> bytes:
        """应用图层遮罩"""
        return BasicMasks.apply_layer_mask(
            base_image_bytes, overlay_image_bytes, mask_bytes,
            blend_mode, opacity, quality
        )
    
    @staticmethod
    def apply_clipping_mask(
        image: Image.Image,
        shape: str = "circle",
        padding: int = 0
    ) -> Image.Image:
        """应用剪贴蒙版"""
        return ClippingMasks.apply_clipping_mask(image, shape, padding)
    
    @staticmethod
    def apply_gradient_mask(
        image: Image.Image,
        gradient_type: str = "linear",
        direction: str = "horizontal",
        start_opacity: float = 1.0,
        end_opacity: float = 0.0
    ) -> Image.Image:
        """应用渐变蒙版"""
        return GradientMasks.apply_gradient_mask(
            image, gradient_type, direction, start_opacity, end_opacity
        )
    
    @staticmethod
    def create_shape_mask(
        size: Tuple[int, int],
        shape: str = "rectangle",
        params: dict = None
    ) -> Image.Image:
        """创建形状蒙版"""
        return ShapeMasks.create_shape_mask(size, shape, params)
    
    @staticmethod
    def apply_shape_mask(
        image: Image.Image,
        mask_type: str = "circle",
        feather: int = 0,
        invert: bool = False,
        background_color: str = "#FFFFFF",
        opacity: float = 1.0
    ) -> Image.Image:
        """应用形状遮罩"""
        return ShapeMasks.apply_shape_mask(
            image, mask_type, feather, invert, background_color, opacity
        )
    
    @staticmethod
    def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """将十六进制颜色转换为RGB"""
        return MaskUtils.hex_to_rgb(hex_color)
