from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw
import random
from typing import Callable

class SpecialFilters:
    """特殊效果滤镜"""

    @staticmethod
    @staticmethod
    def _apply_dream(img: Image.Image, intensity: float) -> Image.Image:
        """梦幻效果"""
        # 应用柔焦
        dreamy = FilterService._apply_soft_focus(img, intensity * 0.7)
        # 增加亮度
        enhancer = ImageEnhance.Brightness(dreamy)
        dreamy = enhancer.enhance(1.1)
        # 降低对比度
        enhancer = ImageEnhance.Contrast(dreamy)
        dreamy = enhancer.enhance(0.9)
        return dreamy
    
    @staticmethod
    @staticmethod
    def _apply_glow(img: Image.Image, intensity: float) -> Image.Image:
        """发光效果"""
        # 创建发光效果
        glow = img.filter(ImageFilter.GaussianBlur(radius=int(intensity * 10)))
        # 增加亮度
        enhancer = ImageEnhance.Brightness(glow)
        glow = enhancer.enhance(1.5)
        # 与原图混合
        return Image.blend(img, glow, intensity * 0.3)
    
    @staticmethod
    @staticmethod
    def _apply_soft_focus(img: Image.Image, intensity: float) -> Image.Image:
        """柔焦效果"""
        blur_radius = int(intensity * 5)
        soft = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        # 与原图混合
        return Image.blend(img, soft, 0.5)
    
    @staticmethod
    @staticmethod
    def _apply_noise(img: Image.Image, intensity: float) -> Image.Image:
        """噪点效果"""
        return FilterService._apply_film_grain(img, intensity)
    
    @staticmethod
    @staticmethod
    def _apply_vignette(img: Image.Image, intensity: float) -> Image.Image:
        """暗角效果"""
        width, height = img.size
        # 创建暗角遮罩
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        # 计算中心点和半径
        center_x, center_y = width // 2, height // 2
        max_radius = min(width, height) // 2
        
        # 绘制径向渐变
        for radius in range(max_radius, 0, -1):
            alpha = int(255 * (1 - (radius / max_radius) * intensity))
            draw.ellipse(
                [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
                fill=alpha
            )
        
        # 应用遮罩
        vignette = Image.new('RGB', img.size, (0, 0, 0))
        return Image.composite(img, vignette, mask)
    
    @staticmethod
    @staticmethod
    def _apply_mosaic(img: Image.Image, intensity: float) -> Image.Image:
        """马赛克效果"""
        # 缩小图像
        small_size = max(1, int(100 / (1 + intensity * 9)))
        small = img.resize((small_size, small_size), Image.NEAREST)
        # 放大回原尺寸
        return small.resize(img.size, Image.NEAREST)
    
    # 滤镜效果
