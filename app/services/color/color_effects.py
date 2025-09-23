from PIL import Image, ImageEnhance
import io
import numpy as np
from typing import Tuple
from ...utils.logger import logger


class ColorEffects:
    """色彩效果处理"""
    
    @staticmethod
    def apply_pop_art(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用波普艺术效果"""
        logger.info(f"应用波普艺术效果: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 增强对比度和饱和度
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.5 * intensity)
            
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(2.0 * intensity)
            
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"波普艺术效果失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_pastel_colors(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用粉彩色效果"""
        logger.info(f"应用粉彩色效果: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img, dtype=np.float32)
            
            # 提高亮度，降低饱和度
            img_array = img_array + (255 - img_array) * 0.3 * intensity
            
            result_img = Image.fromarray(np.clip(img_array, 0, 255).astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"粉彩色效果失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_vibrant_colors(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用鲜艳色彩效果"""
        logger.info(f"应用鲜艳色彩效果: intensity={intensity}")
        
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
            logger.error(f"鲜艳色彩效果失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_muted_colors(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用柔和色彩效果"""
        logger.info(f"应用柔和色彩效果: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 降低饱和度
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1 - intensity * 0.5)
            
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"柔和色彩效果失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_earth_tones(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用大地色调效果"""
        logger.info(f"应用大地色调效果: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img, dtype=np.float32)
            
            # 增强棕色和橙色调
            earth_matrix = np.array([
                [1.0 + 0.1 * intensity, 0.05 * intensity, -0.05 * intensity],
                [0.05 * intensity, 1.0, 0.05 * intensity],
                [-0.1 * intensity, -0.05 * intensity, 0.9]
            ])
            
            # 应用颜色矩阵
            img_array = np.dot(img_array, earth_matrix.T)
            
            result_img = Image.fromarray(np.clip(img_array, 0, 255).astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"大地色调效果失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_cool_tones(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用冷色调效果"""
        logger.info(f"应用冷色调效果: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img, dtype=np.float32)
            
            # 增强蓝色，减少红色
            img_array[:, :, 0] *= (1 - 0.2 * intensity)  # 减少红色
            img_array[:, :, 2] *= (1 + 0.2 * intensity)  # 增加蓝色
            
            result_img = Image.fromarray(np.clip(img_array, 0, 255).astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"冷色调效果失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_warm_tones(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用暖色调效果"""
        logger.info(f"应用暖色调效果: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img, dtype=np.float32)
            
            # 增强红色和黄色，减少蓝色
            img_array[:, :, 0] *= (1 + 0.2 * intensity)  # 增加红色
            img_array[:, :, 1] *= (1 + 0.1 * intensity)  # 增加绿色（黄色）
            img_array[:, :, 2] *= (1 - 0.2 * intensity)  # 减少蓝色
            
            result_img = Image.fromarray(np.clip(img_array, 0, 255).astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"暖色调效果失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_monochrome(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用单色效果"""
        logger.info(f"应用单色效果: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 转换为灰度
            gray = img.convert('L')
            
            # 根据强度混合原图和灰度图
            if intensity < 1.0:
                img_array = np.array(img, dtype=np.float32)
                gray_array = np.array(gray.convert('RGB'), dtype=np.float32)
                
                result_array = img_array * (1 - intensity) + gray_array * intensity
                result_img = Image.fromarray(result_array.astype('uint8'))
            else:
                result_img = gray.convert('RGB')
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"单色效果失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_infrared(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用红外效果"""
        logger.info(f"应用红外效果: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img, dtype=np.float32)
            
            # 红外效果：交换红色和绿色通道，增强对比度
            infrared_array = img_array.copy()
            infrared_array[:, :, 0] = img_array[:, :, 1]  # 绿色 -> 红色
            infrared_array[:, :, 1] = img_array[:, :, 0]  # 红色 -> 绿色
            
            # 增强对比度
            infrared_array = (infrared_array - 128) * (1 + intensity) + 128
            
            result_img = Image.fromarray(np.clip(infrared_array, 0, 255).astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"红外效果失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_night_vision(image_bytes: bytes, intensity: float, quality: int) -> bytes:
        """应用夜视效果"""
        logger.info(f"应用夜视效果: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 转换为灰度
            gray = img.convert('L')
            gray_array = np.array(gray, dtype=np.float32)
            
            # 增强亮度和对比度
            gray_array = (gray_array - 128) * (1 + intensity) + 128 + 50 * intensity
            gray_array = np.clip(gray_array, 0, 255)
            
            # 创建绿色夜视效果
            result_array = np.zeros((gray_array.shape[0], gray_array.shape[1], 3), dtype=np.float32)
            result_array[:, :, 1] = gray_array  # 绿色通道
            result_array[:, :, 0] = gray_array * 0.3  # 少量红色
            
            result_img = Image.fromarray(result_array.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"夜视效果失败: {str(e)}")
            raise
