from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw
import random
import io
from typing import Callable

class ArtisticFilters:
    """艺术效果滤镜"""

    @staticmethod
    def apply_filter(
        image_bytes: bytes,
        filter_type: str,
        intensity: float = 1.0,
        quality: int = 90
    ) -> bytes:
        """
        应用艺术滤镜

        Args:
            image_bytes: 输入图片的字节数据
            filter_type: 滤镜类型
            intensity: 效果强度
            quality: 输出质量

        Returns:
            处理后图片的字节数据
        """
        # 导入滤镜函数
        from ...filters.oil_painting import apply_oil_painting
        from ...filters.pencil_sketch import apply_pencil_sketch
        from ...filters.watercolor import apply_watercolor
        from ...filters.special_effects import apply_neon_glow
        from ..filter_service import FilterService

        if filter_type == "oil_painting":
            return apply_oil_painting(
                image_bytes=image_bytes,
                radius=5,
                intensity=intensity * 10.0  # 转换intensity范围
            )
        elif filter_type == "pencil_sketch":
            return apply_pencil_sketch(
                image_bytes=image_bytes,
                sigma_s=60,
                sigma_r=0.07,
                shade_factor=0.1,
                intensity=intensity
            )
        elif filter_type == "watercolor":
            return apply_watercolor(
                image_bytes=image_bytes,
                sigma_s=60,
                sigma_r=0.6,
                texture_strength=0.1,
                intensity=intensity
            )
        elif filter_type == "cartoon":
            # 使用基础滤镜服务的卡通效果
            from ..filter_service import FilterService
            return FilterService.apply_filter(
                image_bytes=image_bytes,
                filter_type="cartoon",
                intensity=intensity
            )
        elif filter_type == "vintage":
            # 使用基础滤镜服务的复古效果
            from ..filter_service import FilterService
            return FilterService.apply_filter(
                image_bytes=image_bytes,
                filter_type="vintage",
                intensity=intensity
            )
        elif filter_type == "dreamy":
            # 使用基础滤镜服务的梦幻效果
            from ..filter_service import FilterService
            return FilterService.apply_filter(
                image_bytes=image_bytes,
                filter_type="dream",
                intensity=intensity
            )
        else:
            # 对于不支持的滤镜类型，返回原图
            return image_bytes



    @staticmethod
    @staticmethod
    def _apply_emboss(img: Image.Image, intensity: float) -> Image.Image:
        """浮雕效果"""
        embossed = img.filter(ImageFilter.EMBOSS)
        if intensity < 1.0:
            embossed = Image.blend(img, embossed, intensity)
        return embossed
    
    @staticmethod
    @staticmethod
    def _apply_posterize(img: Image.Image, intensity: float) -> Image.Image:
        """色调分离"""
        bits = max(1, int(8 - intensity * 6))  # 1-8 bits
        return ImageOps.posterize(img, bits)
    
    @staticmethod
    @staticmethod
    def _apply_solarize(img: Image.Image, intensity: float) -> Image.Image:
        """曝光过度"""
        threshold = int(255 * (1 - intensity))
        return ImageOps.solarize(img, threshold)
    
    @staticmethod
    @staticmethod
    def _apply_invert(img: Image.Image, intensity: float) -> Image.Image:
        """反转"""
        inverted = ImageOps.invert(img)
        if intensity < 1.0:
            inverted = Image.blend(img, inverted, intensity)
        return inverted
    
    @staticmethod
    @staticmethod
    def _apply_edge_enhance(img: Image.Image, intensity: float) -> Image.Image:
        """边缘增强"""
        enhanced = img.filter(ImageFilter.EDGE_ENHANCE)
        if intensity < 1.0:
            enhanced = Image.blend(img, enhanced, intensity)
        return enhanced
    
    @staticmethod
    @staticmethod
    def _apply_smooth(img: Image.Image, intensity: float) -> Image.Image:
        """平滑"""
        smooth = img.filter(ImageFilter.SMOOTH)
        if intensity < 1.0:
            smooth = Image.blend(img, smooth, intensity)
        return smooth
    
    @staticmethod
    @staticmethod
    def _apply_detail(img: Image.Image, intensity: float) -> Image.Image:
        """细节增强"""
        detailed = img.filter(ImageFilter.DETAIL)
        if intensity < 1.0:
            detailed = Image.blend(img, detailed, intensity)
        return detailed
    
    # 黑白效果滤镜
