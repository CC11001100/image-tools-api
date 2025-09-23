from PIL import Image, ImageEnhance
import io
import numpy as np
from typing import Tuple
from ...utils.logger import logger


class SpecialEffects:
    """特殊色彩效果处理"""
    
    @staticmethod
    def apply_thermal(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用热成像效果"""
        logger.info(f"应用热成像效果: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 转换为灰度
            gray = img.convert('L')
            gray_array = np.array(gray, dtype=np.float32)
            
            # 创建热成像颜色映射
            result_array = np.zeros((gray_array.shape[0], gray_array.shape[1], 3), dtype=np.float32)
            
            # 根据亮度值映射到热成像颜色
            normalized = gray_array / 255.0
            
            # 蓝色到红色的渐变
            result_array[:, :, 0] = normalized * 255 * intensity  # 红色
            result_array[:, :, 1] = (1 - normalized) * normalized * 4 * 255 * intensity  # 绿色（中间值）
            result_array[:, :, 2] = (1 - normalized) * 255 * intensity  # 蓝色
            
            result_img = Image.fromarray(np.clip(result_array, 0, 255).astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"热成像效果失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_saturation_boost(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用饱和度增强效果"""
        logger.info(f"应用饱和度增强: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 增强饱和度
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1 + intensity)
            
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"饱和度增强失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_contrast_enhance(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用对比度增强效果"""
        logger.info(f"应用对比度增强: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 增强对比度
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1 + intensity)
            
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"对比度增强失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_brightness_adjust(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用亮度调整效果"""
        logger.info(f"应用亮度调整: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 调整亮度
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1 + intensity)
            
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"亮度调整失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_vibrance(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用自然饱和度（vibrance）效果"""
        logger.info(f"应用自然饱和度: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img, dtype=np.float32)
            
            # 计算每个像素的饱和度
            max_rgb = np.max(img_array, axis=2)
            min_rgb = np.min(img_array, axis=2)
            saturation = (max_rgb - min_rgb) / (max_rgb + 1e-6)
            
            # 对低饱和度区域应用更强的增强
            vibrance_factor = 1 + intensity * (1 - saturation)
            
            # 计算灰度值
            gray = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2]
            
            # 应用自然饱和度增强
            for i in range(3):
                img_array[:, :, i] = gray + (img_array[:, :, i] - gray) * vibrance_factor
            
            result_img = Image.fromarray(np.clip(img_array, 0, 255).astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"自然饱和度增强失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_rainbow_effect(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用彩虹效果"""
        logger.info(f"应用彩虹效果: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img, dtype=np.float32)
            height, width = img_array.shape[:2]
            
            # 创建彩虹渐变
            rainbow_array = np.zeros_like(img_array)
            
            for y in range(height):
                hue = (y / height) * 360  # 0-360度色相
                
                # HSV到RGB转换（简化版）
                c = 1.0
                x = c * (1 - abs((hue / 60) % 2 - 1))
                m = 0
                
                if 0 <= hue < 60:
                    r, g, b = c, x, 0
                elif 60 <= hue < 120:
                    r, g, b = x, c, 0
                elif 120 <= hue < 180:
                    r, g, b = 0, c, x
                elif 180 <= hue < 240:
                    r, g, b = 0, x, c
                elif 240 <= hue < 300:
                    r, g, b = x, 0, c
                else:
                    r, g, b = c, 0, x
                
                rainbow_array[y, :, 0] = (r + m) * 255
                rainbow_array[y, :, 1] = (g + m) * 255
                rainbow_array[y, :, 2] = (b + m) * 255
            
            # 混合原图和彩虹效果
            result_array = img_array * (1 - intensity) + rainbow_array * intensity
            
            result_img = Image.fromarray(np.clip(result_array, 0, 255).astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"彩虹效果失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_sunset_effect(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用日落效果"""
        logger.info(f"应用日落效果: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img, dtype=np.float32)
            
            # 增强暖色调
            sunset_matrix = np.array([
                [1.0 + 0.3 * intensity, 0.1 * intensity, -0.1 * intensity],
                [0.1 * intensity, 1.0 + 0.1 * intensity, -0.05 * intensity],
                [-0.2 * intensity, -0.1 * intensity, 0.8]
            ])
            
            # 应用颜色矩阵
            img_array = np.dot(img_array, sunset_matrix.T)
            
            result_img = Image.fromarray(np.clip(img_array, 0, 255).astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"日落效果失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_ocean_effect(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用海洋效果"""
        logger.info(f"应用海洋效果: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img, dtype=np.float32)
            
            # 增强蓝绿色调
            ocean_matrix = np.array([
                [0.8, 0.1 * intensity, 0.1 * intensity],
                [0.1 * intensity, 1.0 + 0.2 * intensity, 0.1 * intensity],
                [0.2 * intensity, 0.2 * intensity, 1.0 + 0.3 * intensity]
            ])
            
            # 应用颜色矩阵
            img_array = np.dot(img_array, ocean_matrix.T)
            
            result_img = Image.fromarray(np.clip(img_array, 0, 255).astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"海洋效果失败: {str(e)}")
            raise
