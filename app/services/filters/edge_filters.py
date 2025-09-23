from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw
import random
from typing import Callable

class EdgeFilters:
    """边缘处理滤镜"""

    @staticmethod
    @staticmethod
    def _apply_find_edges(img: Image.Image, intensity: float) -> Image.Image:
        """查找边缘"""
        edges = img.filter(ImageFilter.FIND_EDGES)
        if intensity < 1.0:
            edges = Image.blend(img, edges, intensity)
        return edges
    
    @staticmethod
    @staticmethod
    def _apply_contour(img: Image.Image, intensity: float) -> Image.Image:
        """轮廓"""
        contour = img.filter(ImageFilter.CONTOUR)
        if intensity < 1.0:
            contour = Image.blend(img, contour, intensity)
        return contour
    
    @staticmethod
    @staticmethod
    def _apply_edge_enhance_more(img: Image.Image, intensity: float) -> Image.Image:
        """强边缘增强"""
        enhanced = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        if intensity < 1.0:
            enhanced = Image.blend(img, enhanced, intensity)
        return enhanced
    
    @staticmethod
    @staticmethod
    def _apply_smooth_more(img: Image.Image, intensity: float) -> Image.Image:
        """强平滑"""
        smooth = img.filter(ImageFilter.SMOOTH_MORE)
        if intensity < 1.0:
            smooth = Image.blend(img, smooth, intensity)
        return smooth
    
    @staticmethod
    @staticmethod
    def _apply_unsharp_mask(img: Image.Image, intensity: float) -> Image.Image:
        """反锐化遮罩"""
        # 创建模糊版本
        blurred = img.filter(ImageFilter.GaussianBlur(radius=2))
        # 计算差异
        diff = Image.blend(img, blurred, -intensity)
        return diff
    
    # 创意效果滤镜
