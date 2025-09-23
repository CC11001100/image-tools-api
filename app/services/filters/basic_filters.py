from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw
import random
from typing import Callable

class BasicFilters:
    """基础滤镜"""

    @staticmethod
    @staticmethod
    def _apply_grayscale(img: Image.Image, intensity: float) -> Image.Image:
        """应用灰度滤镜"""
        filtered_img = img.convert("L")
        if intensity != 1.0:
            if intensity > 1.0:
                intensity = 1.0
            filtered_img = Image.blend(
                img.convert("RGB"), 
                filtered_img.convert("RGB"), 
                intensity
            )
        return filtered_img
    
    @staticmethod
    @staticmethod
    def _apply_sepia(img: Image.Image, intensity: float) -> Image.Image:
        """应用棕褐色滤镜"""
        img_gray = img.convert("L")
        img_sepia = Image.new("RGB", img.size)
        
        for x in range(img.width):
            for y in range(img.height):
                gray_value = img_gray.getpixel((x, y))
                r = min(int(gray_value * 1.07 * intensity), 255)
                g = min(int(gray_value * 0.74 * intensity), 255)
                b = min(int(gray_value * 0.43 * intensity), 255)
                img_sepia.putpixel((x, y), (r, g, b))
        
        return img_sepia
    
    @staticmethod
    @staticmethod
    def _apply_blur(img: Image.Image, intensity: float) -> Image.Image:
        """应用模糊滤镜"""
        blur_radius = max(1, int(5 * intensity))
        return img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    
    @staticmethod
    @staticmethod
    def _apply_sharpen(img: Image.Image, intensity: float) -> Image.Image:
        """应用锐化滤镜"""
        sharpened = img.filter(ImageFilter.SHARPEN)
        
        if intensity != 1.0:
            if intensity > 1.0:
                # 多次应用锐化
                for _ in range(int(intensity) - 1):
                    sharpened = sharpened.filter(ImageFilter.SHARPEN)
                # 处理小数部分
                fraction = intensity - int(intensity)
                if fraction > 0:
                    last_sharpen = sharpened.filter(ImageFilter.SHARPEN)
                    sharpened = Image.blend(sharpened, last_sharpen, fraction)
            else:
                # 弱化锐化效果
                sharpened = Image.blend(img, sharpened, intensity)
        
        return sharpened
    
    @staticmethod
    @staticmethod
    def _apply_brightness(img: Image.Image, intensity: float) -> Image.Image:
        """调整亮度"""
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(intensity)
    
    @staticmethod
    @staticmethod
    def _apply_contrast(img: Image.Image, intensity: float) -> Image.Image:
        """调整对比度"""
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(intensity)

    # 色彩效果滤镜
