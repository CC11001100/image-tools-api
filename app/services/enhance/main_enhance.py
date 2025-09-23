from PIL import Image, ImageFilter, ImageEnhance
import io
import numpy as np
from typing import Optional, Tuple
from ...utils.logger import logger
from .blur_effects import BlurEffects
from .sharpen_effects import SharpenEffects


class MainEnhance:
    """主要增强处理方法"""
    
    @staticmethod
    def apply_enhance_effect(
        image_bytes: bytes,
        effect_type: str,
        **kwargs
    ) -> bytes:
        """
        应用增强效果
        
        Args:
            image_bytes: 输入图片的字节数据
            effect_type: 效果类型
            **kwargs: 效果参数
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"应用增强效果: effect_type={effect_type}")
        
        try:
            quality = kwargs.get('quality', 90)
            
            # 模糊效果
            if effect_type == 'motion_blur':
                return BlurEffects.motion_blur(
                    image_bytes,
                    angle=kwargs.get('angle', 0.0),
                    length=kwargs.get('length', 15),
                    quality=quality
                )
            elif effect_type == 'radial_blur':
                return BlurEffects.radial_blur(
                    image_bytes,
                    center_x=kwargs.get('center_x'),
                    center_y=kwargs.get('center_y'),
                    strength=kwargs.get('strength', 5.0),
                    quality=quality
                )
            elif effect_type == 'surface_blur':
                return BlurEffects.surface_blur(
                    image_bytes,
                    radius=kwargs.get('radius', 5),
                    threshold=kwargs.get('threshold', 15),
                    quality=quality
                )
            
            # 锐化效果
            elif effect_type == 'unsharp_mask':
                return SharpenEffects.unsharp_mask(
                    image_bytes,
                    radius=kwargs.get('radius', 1.0),
                    amount=kwargs.get('amount', 1.0),
                    threshold=kwargs.get('threshold', 0),
                    quality=quality
                )
            elif effect_type == 'smart_sharpen':
                return SharpenEffects.smart_sharpen(
                    image_bytes,
                    amount=kwargs.get('amount', 100.0),
                    radius=kwargs.get('radius', 1.0),
                    noise_reduction=kwargs.get('noise_reduction', 0.0),
                    quality=quality
                )
            elif effect_type == 'edge_sharpen':
                return SharpenEffects.edge_sharpen(
                    image_bytes,
                    strength=kwargs.get('strength', 1.0),
                    quality=quality
                )
            
            # 简单增强效果
            elif effect_type in ['sharpen', 'blur', 'smooth', 'detail', 'edge_enhance', 'emboss', 'find_edges', 'contour']:
                return MainEnhance._apply_simple_enhance(
                    image_bytes,
                    effect_type,
                    kwargs.get('intensity', 1.0),
                    quality
                )
            
            else:
                raise ValueError(f"不支持的增强效果类型: {effect_type}")
                
        except Exception as e:
            logger.error(f"增强效果应用失败: {str(e)}")
            raise
    
    @staticmethod
    def _apply_simple_enhance(image_bytes: bytes, effect_type: str, intensity: float, quality: int) -> bytes:
        """
        应用简单增强效果
        
        Args:
            image_bytes: 输入图片的字节数据
            effect_type: 效果类型
            intensity: 效果强度
            quality: 输出图像质量
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"应用简单增强: effect_type={effect_type}, intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # 根据效果类型应用相应的滤镜
            if effect_type == 'sharpen':
                # 锐化
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1 + intensity)
            
            elif effect_type == 'blur':
                # 模糊
                radius = max(0.1, intensity * 2)
                img = img.filter(ImageFilter.GaussianBlur(radius=radius))
            
            elif effect_type == 'smooth':
                # 平滑
                for _ in range(int(intensity)):
                    img = img.filter(ImageFilter.SMOOTH)
            
            elif effect_type == 'detail':
                # 细节增强
                for _ in range(int(intensity)):
                    img = img.filter(ImageFilter.DETAIL)
            
            elif effect_type == 'edge_enhance':
                # 边缘增强
                for _ in range(int(intensity)):
                    img = img.filter(ImageFilter.EDGE_ENHANCE)
            
            elif effect_type == 'emboss':
                # 浮雕效果
                img = img.filter(ImageFilter.EMBOSS)
                if intensity < 1.0:
                    # 与原图混合
                    original = Image.open(io.BytesIO(image_bytes))
                    img = Image.blend(original, img, intensity)
            
            elif effect_type == 'find_edges':
                # 边缘检测
                img = img.filter(ImageFilter.FIND_EDGES)
                if intensity < 1.0:
                    # 与原图混合
                    original = Image.open(io.BytesIO(image_bytes))
                    img = Image.blend(original, img, intensity)
            
            elif effect_type == 'contour':
                # 轮廓
                img = img.filter(ImageFilter.CONTOUR)
                if intensity < 1.0:
                    # 与原图混合
                    original = Image.open(io.BytesIO(image_bytes))
                    img = Image.blend(original, img, intensity)
            
            else:
                raise ValueError(f"不支持的简单增强效果: {effect_type}")
            
            # 保存结果
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"简单增强效果失败: {str(e)}")
            raise
