from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw
import random
from typing import Callable

class ColorFilters:
    """色彩效果滤镜"""

    @staticmethod
    @staticmethod
    def _apply_saturate(img: Image.Image, intensity: float) -> Image.Image:
        """饱和度调整"""
        enhancer = ImageEnhance.Color(img)
        return enhancer.enhance(intensity)
    
    @staticmethod
    @staticmethod
    def _apply_desaturate(img: Image.Image, intensity: float) -> Image.Image:
        """去饱和"""
        enhancer = ImageEnhance.Color(img)
        return enhancer.enhance(1.0 - intensity * 0.8)
    
    @staticmethod
    @staticmethod
    def _apply_warm(img: Image.Image, intensity: float) -> Image.Image:
        """暖色调"""
        r, g, b = img.split()
        r = r.point(lambda x: min(255, int(x * (1 + intensity * 0.1))))
        g = g.point(lambda x: min(255, int(x * (1 + intensity * 0.05))))
        b = b.point(lambda x: max(0, int(x * (1 - intensity * 0.1))))
        return Image.merge('RGB', (r, g, b))
    
    @staticmethod
    @staticmethod
    def _apply_cool(img: Image.Image, intensity: float) -> Image.Image:
        """冷色调"""
        r, g, b = img.split()
        r = r.point(lambda x: max(0, int(x * (1 - intensity * 0.1))))
        g = g.point(lambda x: min(255, int(x * (1 + intensity * 0.05))))
        b = b.point(lambda x: min(255, int(x * (1 + intensity * 0.1))))
        return Image.merge('RGB', (r, g, b))
    
    @staticmethod
    @staticmethod
    def _apply_vintage(img: Image.Image, intensity: float) -> Image.Image:
        """复古效果"""
        # 应用棕褐色效果
        from .basic_filters import BasicFilters
        sepia = BasicFilters._apply_sepia(img, intensity * 0.6)
        # 降低饱和度
        enhancer = ImageEnhance.Color(sepia)
        vintage = enhancer.enhance(0.8)
        # 降低对比度
        enhancer = ImageEnhance.Contrast(vintage)
        vintage = enhancer.enhance(0.9)
        # 添加暖色调
        return ColorFilters._apply_warm(vintage, intensity * 0.3)
    
    @staticmethod
    @staticmethod
    def _apply_hueshift(img: Image.Image, intensity: float) -> Image.Image:
        """色调偏移"""
        # 简单的色相偏移实现
        r, g, b = img.split()
        # 交换颜色通道来模拟色相偏移
        shift = int(intensity * 3) % 3
        if shift == 1:
            return Image.merge('RGB', (b, r, g))
        elif shift == 2:
            return Image.merge('RGB', (g, b, r))
        return img
    
    @staticmethod
    @staticmethod
    def _apply_gamma(img: Image.Image, intensity: float) -> Image.Image:
        """伽马校正"""
        gamma = 0.5 + intensity * 1.5  # 0.5 to 2.0
        return img.point(lambda x: int(255 * (x / 255) ** (1 / gamma)))
    
    @staticmethod
    @staticmethod
    def _apply_levels(img: Image.Image, intensity: float) -> Image.Image:
        """色阶调整"""
        # 自动色阶调整
        return ImageOps.autocontrast(img, cutoff=intensity * 10)
    
    # 艺术效果滤镜
