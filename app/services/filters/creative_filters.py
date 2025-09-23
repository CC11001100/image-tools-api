from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw
import random
from typing import Callable

class CreativeFilters:
    """创意效果滤镜"""

    @staticmethod
    @staticmethod
    def _apply_pencil(img: Image.Image, intensity: float) -> Image.Image:
        """铅笔画效果"""
        # 转换为灰度
        gray = img.convert('L')
        # 反转
        inverted = ImageOps.invert(gray)
        # 模糊
        blurred = inverted.filter(ImageFilter.GaussianBlur(radius=5))
        # 反转回来
        pencil = ImageOps.invert(blurred)
        # 与原图混合
        result = Image.blend(gray.convert('RGB'), pencil.convert('RGB'), intensity)
        return result
    
    @staticmethod
    @staticmethod
    def _apply_sketch(img: Image.Image, intensity: float) -> Image.Image:
        """素描效果"""
        # 查找边缘
        edges = img.filter(ImageFilter.FIND_EDGES)
        # 转换为灰度
        sketch = edges.convert('L')
        # 反转
        sketch = ImageOps.invert(sketch)
        return sketch.convert('RGB')
    
    @staticmethod
    @staticmethod
    def _apply_cartoon(img: Image.Image, intensity: float) -> Image.Image:
        """卡通效果"""
        # 应用色调分离
        cartoon = FilterService._apply_posterize(img, intensity)
        # 增强边缘
        cartoon = FilterService._apply_edge_enhance(cartoon, intensity)
        # 增加饱和度
        enhancer = ImageEnhance.Color(cartoon)
        cartoon = enhancer.enhance(1.3)
        return cartoon
    
    @staticmethod
    @staticmethod
    def _apply_hdr(img: Image.Image, intensity: float) -> Image.Image:
        """HDR效果"""
        # 增强对比度
        enhancer = ImageEnhance.Contrast(img)
        hdr = enhancer.enhance(1.5)
        # 增加饱和度
        enhancer = ImageEnhance.Color(hdr)
        hdr = enhancer.enhance(1.3)
        # 调整亮度
        enhancer = ImageEnhance.Brightness(hdr)
        hdr = enhancer.enhance(1.1)
        return hdr
    
    @staticmethod
    @staticmethod
    def _apply_cyberpunk(img: Image.Image, intensity: float) -> Image.Image:
        """赛博朋克效果"""
        # 增强对比度
        enhancer = ImageEnhance.Contrast(img)
        cyber = enhancer.enhance(1.4)
        # 调整颜色通道
        r, g, b = cyber.split()
        r = r.point(lambda x: min(255, int(x * (1 + intensity * 0.3))))
        g = g.point(lambda x: min(255, int(x * (1 + intensity * 0.2))))
        b = b.point(lambda x: min(255, int(x * (1 + intensity * 0.5))))
        return Image.merge('RGB', (r, g, b))
    
    @staticmethod
    @staticmethod
    def _apply_noir(img: Image.Image, intensity: float) -> Image.Image:
        """黑色电影效果"""
        # 转换为黑白
        noir = img.convert('L')
        # 增强对比度
        enhancer = ImageEnhance.Contrast(noir)
        noir = enhancer.enhance(1.5)
        # 降低亮度
        enhancer = ImageEnhance.Brightness(noir)
        noir = enhancer.enhance(0.9)
        return noir.convert('RGB')
    
    @staticmethod
    @staticmethod
    def _apply_faded(img: Image.Image, intensity: float) -> Image.Image:
        """褪色效果"""
        # 降低饱和度
        enhancer = ImageEnhance.Color(img)
        faded = enhancer.enhance(0.5)
        # 增加亮度
        enhancer = ImageEnhance.Brightness(faded)
        faded = enhancer.enhance(1.2)
        # 降低对比度
        enhancer = ImageEnhance.Contrast(faded)
        faded = enhancer.enhance(0.8)
        return faded
    
    @staticmethod
    @staticmethod
    def _apply_pastel(img: Image.Image, intensity: float) -> Image.Image:
        """柔和色彩效果"""
        # 降低饱和度
        enhancer = ImageEnhance.Color(img)
        pastel = enhancer.enhance(0.7)
        # 增加亮度
        enhancer = ImageEnhance.Brightness(pastel)
        pastel = enhancer.enhance(1.1)
        # 降低对比度
        enhancer = ImageEnhance.Contrast(pastel)
        pastel = enhancer.enhance(0.9)
        return pastel
    
