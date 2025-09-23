from typing import Optional, Tuple
from ..utils.logger import logger
from .advanced_enhance import (
    AdvancedSharpen,
    AdvancedBlur,
    NoiseReduction,
    StructureEnhance,
    HDRLighting,
    ArtisticEffects
)


class AdvancedEnhanceService:
    """高级图像增强服务 - 模块化版本"""
    
    # 高级锐化方法
    @staticmethod
    def apply_high_pass_sharpen(image_bytes: bytes, radius: float = 2.0, intensity: float = 1.0) -> bytes:
        """高通锐化"""
        return AdvancedSharpen.apply_high_pass_sharpen(image_bytes, radius, intensity)
    
    @staticmethod
    def apply_adaptive_sharpen(image_bytes: bytes, threshold: float = 0.5, intensity: float = 1.0) -> bytes:
        """自适应锐化"""
        return AdvancedSharpen.apply_adaptive_sharpen(image_bytes, threshold, intensity)
    
    # 高级模糊方法
    @staticmethod
    def apply_lens_blur(image_bytes: bytes, radius: float = 5.0, sides: int = 6) -> bytes:
        """镜头模糊（散景效果）"""
        return AdvancedBlur.apply_lens_blur(image_bytes, radius, sides)
    
    @staticmethod
    def apply_zoom_blur(image_bytes: bytes, center_x: Optional[int] = None, 
                       center_y: Optional[int] = None, strength: float = 5.0) -> bytes:
        """缩放模糊（放射状模糊）"""
        return AdvancedBlur.apply_zoom_blur(image_bytes, center_x, center_y, strength)
    
    # 降噪处理方法
    @staticmethod
    def apply_wiener_denoise(image_bytes: bytes, noise_variance: float = 0.1) -> bytes:
        """维纳滤波降噪"""
        return NoiseReduction.apply_wiener_denoise(image_bytes, noise_variance)
    
    @staticmethod
    def apply_morphological_denoise(image_bytes: bytes, kernel_size: int = 3) -> bytes:
        """形态学降噪"""
        return NoiseReduction.apply_morphological_denoise(image_bytes, kernel_size)
    
    # 结构增强方法
    @staticmethod
    def apply_structure_enhance(image_bytes: bytes, intensity: float = 1.0) -> bytes:
        """结构增强"""
        return StructureEnhance.apply_structure_enhance(image_bytes, intensity)
    
    @staticmethod
    def apply_micro_contrast(image_bytes: bytes, radius: int = 10, intensity: float = 1.0) -> bytes:
        """微对比度增强"""
        return StructureEnhance.apply_micro_contrast(image_bytes, radius, intensity)
    
    @staticmethod
    def apply_laplacian_enhance(image_bytes: bytes, intensity: float = 1.0) -> bytes:
        """拉普拉斯增强"""
        return StructureEnhance.apply_laplacian_enhance(image_bytes, intensity)
    
    @staticmethod
    def apply_sobel_enhance(image_bytes: bytes, intensity: float = 1.0) -> bytes:
        """Sobel边缘增强"""
        return StructureEnhance.apply_sobel_enhance(image_bytes, intensity)
    
    # HDR和光影方法
    @staticmethod
    def apply_hdr_enhance(image_bytes: bytes, gamma: float = 2.2, exposure: float = 1.0) -> bytes:
        """HDR增强"""
        return HDRLighting.apply_hdr_enhance(image_bytes, gamma, exposure)
    
    @staticmethod
    def apply_shadow_highlight(image_bytes: bytes, shadow_amount: float = 0.5, 
                              highlight_amount: float = 0.5, color_correction: float = 0.2) -> bytes:
        """阴影高光调整"""
        return HDRLighting.apply_shadow_highlight(image_bytes, shadow_amount, highlight_amount, color_correction)
    
    # 艺术效果方法
    @staticmethod
    def apply_glow_enhance(image_bytes: bytes, radius: int = 20, intensity: float = 1.0) -> bytes:
        """发光增强效果"""
        return ArtisticEffects.apply_glow_enhance(image_bytes, radius, intensity)
    
    @staticmethod
    def apply_dreamy_enhance(image_bytes: bytes, softness: float = 0.5, brightness: float = 0.2) -> bytes:
        """梦幻增强效果"""
        return ArtisticEffects.apply_dreamy_enhance(image_bytes, softness, brightness)
    
    @staticmethod
    def apply_portrait_enhance(image_bytes: bytes, skin_smooth: float = 0.3, 
                              eye_enhance: float = 0.5, teeth_whiten: float = 0.3) -> bytes:
        """人像增强"""
        return ArtisticEffects.apply_portrait_enhance(image_bytes, skin_smooth, eye_enhance, teeth_whiten)
    
    @staticmethod
    def apply_landscape_enhance(image_bytes: bytes, clarity: float = 0.8, 
                               vibrance: float = 0.6, sky_enhance: float = 0.4) -> bytes:
        """风景增强"""
        return ArtisticEffects.apply_landscape_enhance(image_bytes, clarity, vibrance, sky_enhance)
