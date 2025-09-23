from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw
import random
from typing import Callable

class VintageFilters:
    """复古和胶片效果滤镜"""

    @staticmethod
    @staticmethod
    def _apply_film_grain(img: Image.Image, intensity: float) -> Image.Image:
        """胶片颗粒"""
        # 添加噪点模拟胶片颗粒
        pixels = list(img.getdata())
        noisy_pixels = []
        for pixel in pixels:
            r, g, b = pixel
            noise = random.randint(-int(intensity * 20), int(intensity * 20))
            r = max(0, min(255, r + noise))
            g = max(0, min(255, g + noise))
            b = max(0, min(255, b + noise))
            noisy_pixels.append((r, g, b))
        
        film_grain = Image.new('RGB', img.size)
        film_grain.putdata(noisy_pixels)
        return film_grain
    
    @staticmethod
    @staticmethod
    def _apply_retro(img: Image.Image, intensity: float) -> Image.Image:
        """复古风格"""
        # 降低饱和度
        enhancer = ImageEnhance.Color(img)
        retro = enhancer.enhance(0.7)
        # 增加对比度
        enhancer = ImageEnhance.Contrast(retro)
        retro = enhancer.enhance(1.2)
        # 添加暖色调
        retro = FilterService._apply_warm(retro, intensity * 0.5)
        return retro
    
    @staticmethod
    @staticmethod
    def _apply_polaroid(img: Image.Image, intensity: float) -> Image.Image:
        """宝丽来效果"""
        # 降低对比度
        enhancer = ImageEnhance.Contrast(img)
        polaroid = enhancer.enhance(0.8)
        # 增加亮度
        enhancer = ImageEnhance.Brightness(polaroid)
        polaroid = enhancer.enhance(1.1)
        # 添加淡淡的棕褐色
        polaroid = FilterService._apply_sepia(polaroid, intensity * 0.3)
        return polaroid
    
    @staticmethod
    @staticmethod
    def _apply_lomo(img: Image.Image, intensity: float) -> Image.Image:
        """LOMO风格"""
        # 增加饱和度
        enhancer = ImageEnhance.Color(img)
        lomo = enhancer.enhance(1.3)
        # 增加对比度
        enhancer = ImageEnhance.Contrast(lomo)
        lomo = enhancer.enhance(1.2)
        # 添加暗角效果
        lomo = FilterService._apply_vignette(lomo, intensity * 0.5)
        return lomo
    
    @staticmethod
    @staticmethod
    def _apply_analog(img: Image.Image, intensity: float) -> Image.Image:
        """模拟风格"""
        # 添加轻微的颗粒
        analog = FilterService._apply_film_grain(img, intensity * 0.3)
        # 调整色彩
        enhancer = ImageEnhance.Color(analog)
        analog = enhancer.enhance(1.1)
        return analog
    
    @staticmethod
    @staticmethod
    def _apply_crossprocess(img: Image.Image, intensity: float) -> Image.Image:
        """交叉处理"""
        # 模拟交叉处理的颜色偏移
        r, g, b = img.split()
        # 调整各个颜色通道
        r = r.point(lambda x: min(255, int(x * (1 + intensity * 0.2))))
        g = g.point(lambda x: min(255, int(x * (1 - intensity * 0.1))))
        b = b.point(lambda x: min(255, int(x * (1 + intensity * 0.3))))
        return Image.merge('RGB', (r, g, b))
    
    # 特殊效果滤镜
