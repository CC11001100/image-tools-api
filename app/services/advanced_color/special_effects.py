"""特殊效果功能"""
import numpy as np
from PIL import Image, ImageEnhance
import io
from typing import Tuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.logger import logger

# 尝试导入cv2，如果失败则使用替代方案
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False


class SpecialEffects:
    """特殊效果功能"""
    
    @staticmethod
    def apply_color_pop(image_bytes: bytes, target_color: tuple = (255, 0, 0),
                       tolerance: int = 50, intensity: float = 1.0) -> bytes:
        """
        色彩突出
        
        Args:
            image_bytes: 输入图片字节数据
            target_color: 目标颜色
            tolerance: 颜色容差
            intensity: 效果强度
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"应用色彩突出: 目标颜色={target_color}, 容差={tolerance}, 强度={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img)
            
            if CV2_AVAILABLE:
                # 转换为HSV
                hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
                target_hsv = cv2.cvtColor(np.uint8([[target_color]]), cv2.COLOR_RGB2HSV)[0, 0]
                
                # 创建颜色遮罩
                h_diff = np.abs(hsv[:, :, 0] - target_hsv[0])
                h_diff = np.minimum(h_diff, 180 - h_diff)  # 处理色相环绕
                
                mask = (h_diff < tolerance) & (hsv[:, :, 1] > 50) & (hsv[:, :, 2] > 50)
                
                # 创建灰度版本
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                gray_rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
            else:
                # 简化版本：基于RGB距离的颜色匹配
                target_array = np.array(target_color)
                color_diff = np.sqrt(np.sum((img_array - target_array) ** 2, axis=2))
                mask = color_diff < tolerance
                
                # 创建灰度版本
                gray = np.mean(img_array, axis=2, keepdims=True)
                gray_rgb = np.repeat(gray, 3, axis=2).astype(np.uint8)
            
            # 混合结果
            result_array = gray_rgb.copy()
            result_array[mask] = img_array[mask]
            
            # 应用强度
            if intensity < 1.0:
                result_array = (img_array * intensity + result_array * (1 - intensity)).astype(np.uint8)
            
            result = Image.fromarray(result_array)
            
            output = io.BytesIO()
            result.save(output, format="JPEG", quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"色彩突出失败: {e}")
            raise
    
    @staticmethod
    def apply_neon_colors(image_bytes: bytes, intensity: float = 1.0) -> bytes:
        """
        霓虹色彩效果
        
        Args:
            image_bytes: 输入图片字节数据
            intensity: 效果强度
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"应用霓虹色彩效果: 强度={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 增强对比度
            enhancer = ImageEnhance.Contrast(img)
            result = enhancer.enhance(1.5 * intensity)
            
            # 增强饱和度
            enhancer = ImageEnhance.Color(result)
            result = enhancer.enhance(2.0 * intensity)
            
            # 调整亮度
            enhancer = ImageEnhance.Brightness(result)
            result = enhancer.enhance(1.2 * intensity)
            
            if CV2_AVAILABLE:
                # 应用色相偏移创建霓虹效果
                img_array = np.array(result).astype(np.float32)
                hsv = cv2.cvtColor(img_array.astype(np.uint8), cv2.COLOR_RGB2HSV)
                
                # 偏移色相
                hsv[:, :, 0] = (hsv[:, :, 0] + 30 * intensity) % 180
                
                result_array = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
                result = Image.fromarray(result_array)
            # 如果没有CV2，保持当前结果（只有增强的对比度、饱和度和亮度）
            
            output = io.BytesIO()
            result.save(output, format="JPEG", quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"霓虹色彩失败: {e}")
            raise
