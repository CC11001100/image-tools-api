from PIL import Image, ImageEnhance
import io
import numpy as np
from typing import Optional, Tuple, Dict, Any
from ...utils.logger import logger
from ..advanced_color_service import AdvancedColorService
from .color_effects import ColorEffects
from .special_effects import SpecialEffects
from .style_effects import StyleEffects


class MainAdjustments:
    """主要色彩调整方法"""
    
    @staticmethod
    def adjust_color(
        image_bytes: bytes,
        brightness: float = 0.0,
        contrast: float = 0.0,
        saturation: float = 0.0,
        hue: float = 0.0,
        gamma: float = 1.0,
        shadows: float = 0.0,
        highlights: float = 0.0,
        quality: int = 90
    ) -> bytes:
        """
        综合色彩调整
        
        Args:
            image_bytes: 输入图片的字节数据
            brightness: 亮度调整 (-100 到 100)
            contrast: 对比度调整 (-100 到 100)
            saturation: 饱和度调整 (-100 到 100)
            hue: 色相调整 (-180 到 180)
            gamma: 伽马值 (0.1 到 3.0)
            shadows: 阴影调整 (-100 到 100)
            highlights: 高光调整 (-100 到 100)
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"综合色彩调整: brightness={brightness}, contrast={contrast}, saturation={saturation}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img, dtype=np.float32)
            
            # 亮度调整
            if brightness != 0:
                img_array += brightness * 2.55  # 转换为0-255范围
            
            # 对比度调整
            if contrast != 0:
                factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
                img_array = factor * (img_array - 128) + 128
            
            # 饱和度调整
            if saturation != 0:
                # 转换为HSV进行饱和度调整
                hsv = MainAdjustments._rgb_to_hsv_simple(img_array)
                sat_factor = 1 + saturation / 100.0
                hsv[:, :, 1] *= sat_factor
                hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 1)
                img_array = MainAdjustments._hsv_to_rgb_simple(hsv)
            
            # 色相调整
            if hue != 0:
                hsv = MainAdjustments._rgb_to_hsv_simple(img_array)
                hsv[:, :, 0] = (hsv[:, :, 0] + hue / 360.0) % 1.0
                img_array = MainAdjustments._hsv_to_rgb_simple(hsv)
            
            # 伽马校正
            if gamma != 1.0:
                img_array = np.power(img_array / 255.0, 1.0 / gamma) * 255.0
            
            # 阴影和高光调整
            if shadows != 0 or highlights != 0:
                # 计算亮度掩码
                luminance = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2]
                
                # 阴影掩码（暗部）
                shadow_mask = np.clip(1.0 - luminance / 128.0, 0, 1)
                # 高光掩码（亮部）
                highlight_mask = np.clip((luminance - 128.0) / 127.0, 0, 1)
                
                # 应用调整
                if shadows != 0:
                    shadow_adjustment = shadows * 2.55
                    for i in range(3):
                        img_array[:, :, i] += shadow_adjustment * shadow_mask
                
                if highlights != 0:
                    highlight_adjustment = highlights * 2.55
                    for i in range(3):
                        img_array[:, :, i] += highlight_adjustment * highlight_mask
            
            # 限制像素值范围
            img_array = np.clip(img_array, 0, 255)
            
            result_img = Image.fromarray(img_array.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"综合色彩调整失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_color_effect(
        image_bytes: bytes,
        effect_type: str,
        intensity: float = 1.0,
        quality: int = 90
    ) -> bytes:
        """
        应用色彩效果
        
        Args:
            image_bytes: 输入图片的字节数据
            effect_type: 效果类型
            intensity: 效果强度 (0.0 到 2.0)
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"应用色彩效果: effect_type={effect_type}, intensity={intensity}")
        
        try:
            # 根据效果类型调用相应的处理方法
            effect_map = {
                # 色彩效果
                'pop_art': ColorEffects.apply_pop_art,
                'pastel_colors': ColorEffects.apply_pastel_colors,
                'vibrant_colors': ColorEffects.apply_vibrant_colors,
                'muted_colors': ColorEffects.apply_muted_colors,
                'earth_tones': ColorEffects.apply_earth_tones,
                'cool_tones': ColorEffects.apply_cool_tones,
                'warm_tones': ColorEffects.apply_warm_tones,
                'monochrome': ColorEffects.apply_monochrome,
                'infrared': ColorEffects.apply_infrared,
                'night_vision': ColorEffects.apply_night_vision,
                
                # 特殊效果
                'thermal': SpecialEffects.apply_thermal,
                'saturation_boost': SpecialEffects.apply_saturation_boost,
                'contrast_enhance': SpecialEffects.apply_contrast_enhance,
                'brightness_adjust': SpecialEffects.apply_brightness_adjust,
                'vibrance': SpecialEffects.apply_vibrance,
                'rainbow_effect': SpecialEffects.apply_rainbow_effect,
                'sunset_effect': SpecialEffects.apply_sunset_effect,
                'ocean_effect': SpecialEffects.apply_ocean_effect,
                
                # 风格效果
                'sepia_tone': StyleEffects.apply_sepia_tone,
                'cyanotype': StyleEffects.apply_cyanotype,
                'instagram_vintage': StyleEffects.apply_instagram_vintage,
                'vsco_film': StyleEffects.apply_vsco_film,
            }
            
            if effect_type not in effect_map:
                raise ValueError(f"不支持的效果类型: {effect_type}")
            
            return effect_map[effect_type](image_bytes, intensity, quality)
            
        except Exception as e:
            logger.error(f"色彩效果应用失败: {str(e)}")
            raise
    
    @staticmethod
    def _rgb_to_hsv_simple(rgb_array):
        """简化的RGB到HSV转换"""
        rgb = rgb_array / 255.0
        max_val = np.max(rgb, axis=2)
        min_val = np.min(rgb, axis=2)
        diff = max_val - min_val
        
        # 色相
        h = np.zeros_like(max_val)
        mask = diff != 0
        
        # 红色主导
        red_mask = mask & (rgb[:, :, 0] == max_val)
        h[red_mask] = ((rgb[red_mask, 1] - rgb[red_mask, 2]) / diff[red_mask]) / 6.0
        
        # 绿色主导
        green_mask = mask & (rgb[:, :, 1] == max_val)
        h[green_mask] = (2.0 + (rgb[green_mask, 2] - rgb[green_mask, 0]) / diff[green_mask]) / 6.0
        
        # 蓝色主导
        blue_mask = mask & (rgb[:, :, 2] == max_val)
        h[blue_mask] = (4.0 + (rgb[blue_mask, 0] - rgb[blue_mask, 1]) / diff[blue_mask]) / 6.0
        
        h = h % 1.0
        
        # 饱和度
        s = np.zeros_like(max_val)
        s[max_val != 0] = diff[max_val != 0] / max_val[max_val != 0]
        
        # 明度
        v = max_val
        
        return np.stack([h, s, v], axis=2)
    
    @staticmethod
    def _hsv_to_rgb_simple(hsv_array):
        """简化的HSV到RGB转换"""
        h = hsv_array[:, :, 0] * 6.0
        s = hsv_array[:, :, 1]
        v = hsv_array[:, :, 2]
        
        c = v * s
        x = c * (1 - np.abs((h % 2) - 1))
        m = v - c
        
        rgb = np.zeros_like(hsv_array)
        
        # 根据色相区间计算RGB
        idx = h.astype(int) % 6
        
        rgb[idx == 0] = np.stack([c[idx == 0], x[idx == 0], np.zeros_like(c[idx == 0])], axis=1)
        rgb[idx == 1] = np.stack([x[idx == 1], c[idx == 1], np.zeros_like(c[idx == 1])], axis=1)
        rgb[idx == 2] = np.stack([np.zeros_like(c[idx == 2]), c[idx == 2], x[idx == 2]], axis=1)
        rgb[idx == 3] = np.stack([np.zeros_like(c[idx == 3]), x[idx == 3], c[idx == 3]], axis=1)
        rgb[idx == 4] = np.stack([x[idx == 4], np.zeros_like(c[idx == 4]), c[idx == 4]], axis=1)
        rgb[idx == 5] = np.stack([c[idx == 5], np.zeros_like(c[idx == 5]), x[idx == 5]], axis=1)
        
        rgb += m[:, :, np.newaxis]
        return rgb * 255.0
