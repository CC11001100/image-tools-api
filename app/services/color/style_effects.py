from PIL import Image, ImageEnhance
import io
import numpy as np
from typing import Tuple
from ...utils.logger import logger


class StyleEffects:
    """风格化色彩效果处理"""
    
    @staticmethod
    def apply_sepia_tone(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用棕褐色调效果"""
        logger.info(f"应用棕褐色调: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img, dtype=np.float32)
            
            # 棕褐色调矩阵
            sepia_matrix = np.array([
                [0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]
            ])
            
            # 应用棕褐色调
            sepia_array = np.dot(img_array, sepia_matrix.T)
            
            # 根据强度混合原图和棕褐色调
            result_array = img_array * (1 - intensity) + sepia_array * intensity
            
            result_img = Image.fromarray(np.clip(result_array, 0, 255).astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"棕褐色调效果失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_cyanotype(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用蓝晒效果"""
        logger.info(f"应用蓝晒效果: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 转换为灰度
            gray = img.convert('L')
            gray_array = np.array(gray, dtype=np.float32)
            
            # 创建蓝晒效果（蓝色单色调）
            result_array = np.zeros((gray_array.shape[0], gray_array.shape[1], 3), dtype=np.float32)
            
            # 反转灰度值并映射到蓝色
            inverted = 255 - gray_array
            result_array[:, :, 0] = inverted * 0.2  # 少量红色
            result_array[:, :, 1] = inverted * 0.4  # 中等绿色
            result_array[:, :, 2] = inverted * 0.8  # 主要蓝色
            
            # 根据强度混合
            if intensity < 1.0:
                original_array = np.array(img, dtype=np.float32)
                result_array = original_array * (1 - intensity) + result_array * intensity
            
            result_img = Image.fromarray(np.clip(result_array, 0, 255).astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"蓝晒效果失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_instagram_vintage(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用Instagram复古效果"""
        logger.info(f"应用Instagram复古效果: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img, dtype=np.float32)
            
            # 复古效果：降低对比度，增加暖色调，轻微模糊
            vintage_matrix = np.array([
                [1.1, 0.1, 0.0],
                [0.1, 1.0, 0.0],
                [0.0, 0.0, 0.9]
            ])
            
            # 应用颜色矩阵
            vintage_array = np.dot(img_array, vintage_matrix.T)
            
            # 降低对比度
            vintage_array = (vintage_array - 128) * 0.8 + 128
            
            # 增加一点亮度
            vintage_array += 20 * intensity
            
            # 根据强度混合
            result_array = img_array * (1 - intensity) + vintage_array * intensity
            
            result_img = Image.fromarray(np.clip(result_array, 0, 255).astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Instagram复古效果失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_vsco_film(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用VSCO胶片效果"""
        logger.info(f"应用VSCO胶片效果: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img, dtype=np.float32)
            
            # 胶片效果：S曲线调整，轻微去饱和，增加颗粒感
            
            # S曲线调整（增强对比度但保持柔和）
            normalized = img_array / 255.0
            s_curve = np.where(normalized < 0.5, 
                              2 * normalized * normalized,
                              1 - 2 * (1 - normalized) * (1 - normalized))
            film_array = s_curve * 255
            
            # 轻微去饱和
            gray = 0.299 * film_array[:, :, 0] + 0.587 * film_array[:, :, 1] + 0.114 * film_array[:, :, 2]
            for i in range(3):
                film_array[:, :, i] = gray + (film_array[:, :, i] - gray) * 0.85
            
            # 增加轻微的暖色调
            film_array[:, :, 0] *= 1.05  # 轻微增加红色
            film_array[:, :, 2] *= 0.95  # 轻微减少蓝色
            
            # 根据强度混合
            result_array = img_array * (1 - intensity) + film_array * intensity
            
            result_img = Image.fromarray(np.clip(result_array, 0, 255).astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"VSCO胶片效果失败: {str(e)}")
            raise
