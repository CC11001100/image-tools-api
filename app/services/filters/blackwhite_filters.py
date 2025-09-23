from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw
import random
from typing import Callable

class BlackwhiteFilters:
    """黑白效果滤镜"""

    @staticmethod
    @staticmethod
    def _apply_monochrome(img: Image.Image, intensity: float) -> Image.Image:
        """单色"""
        mono = img.convert('L').convert('RGB')
        if intensity < 1.0:
            mono = Image.blend(img, mono, intensity)
        return mono
    
    @staticmethod
    @staticmethod
    def _apply_dramatic_bw(img: Image.Image, intensity: float) -> Image.Image:
        """戏剧性黑白"""
        # 转换为黑白
        bw = img.convert('L')
        # 增强对比度
        enhancer = ImageEnhance.Contrast(bw)
        dramatic = enhancer.enhance(1.5 + intensity * 0.5)
        return dramatic.convert('RGB')
    
    @staticmethod
    @staticmethod
    def _apply_infrared(img: Image.Image, intensity: float) -> Image.Image:
        """红外效果"""
        r, g, b = img.split()
        # 红外效果：红色通道作为亮度，其他通道反转
        infrared = Image.merge('RGB', (r, g.point(lambda x: 255 - x), b.point(lambda x: 255 - x)))
        if intensity < 1.0:
            infrared = Image.blend(img, infrared, intensity)
        return infrared
    
    @staticmethod
    @staticmethod
    def _apply_high_contrast_bw(img: Image.Image, intensity: float) -> Image.Image:
        """高对比度黑白"""
        bw = img.convert('L')
        threshold = 128 + int(intensity * 50)
        high_contrast = bw.point(lambda x: 255 if x > threshold else 0)
        return high_contrast.convert('RGB')
    
    # 复古和胶片效果滤镜
