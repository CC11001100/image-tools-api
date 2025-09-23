"""色调处理功能"""
import numpy as np
from PIL import Image
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


class ToneProcessing:
    """色调处理功能"""
    
    @staticmethod
    def apply_split_toning(image_bytes: bytes, highlight_color: tuple = (255, 255, 200),
                          shadow_color: tuple = (100, 100, 150), intensity: float = 1.0) -> bytes:
        """
        分离色调
        
        Args:
            image_bytes: 输入图片字节数据
            highlight_color: 高光色调
            shadow_color: 阴影色调
            intensity: 调整强度
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"应用分离色调: 高光={highlight_color}, 阴影={shadow_color}, 强度={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img).astype(np.float32)
            
            # 转换为HSV以获得亮度信息
            if CV2_AVAILABLE:
                hsv = cv2.cvtColor(img_array.astype(np.uint8), cv2.COLOR_RGB2HSV)
                brightness = hsv[:, :, 2] / 255.0
            else:
                # 使用简化的亮度计算
                brightness = np.mean(img_array, axis=2) / 255.0
            
            # 创建高光和阴影遮罩
            highlight_mask = brightness > 0.5
            shadow_mask = brightness <= 0.5
            
            # 应用色调
            result_array = img_array.copy()
            
            # 高光色调
            highlight_strength = (brightness - 0.5) * 2  # 0-1范围
            highlight_strength = np.clip(highlight_strength, 0, 1)
            
            for i in range(3):
                result_array[:, :, i][highlight_mask] = (
                    img_array[:, :, i][highlight_mask] * (1 - highlight_strength[highlight_mask] * intensity * 0.3) +
                    highlight_color[i] * highlight_strength[highlight_mask] * intensity * 0.3
                )
            
            # 阴影色调
            shadow_strength = (0.5 - brightness) * 2  # 0-1范围
            shadow_strength = np.clip(shadow_strength, 0, 1)
            
            for i in range(3):
                result_array[:, :, i][shadow_mask] = (
                    img_array[:, :, i][shadow_mask] * (1 - shadow_strength[shadow_mask] * intensity * 0.3) +
                    shadow_color[i] * shadow_strength[shadow_mask] * intensity * 0.3
                )
            
            result_array = np.clip(result_array, 0, 255).astype(np.uint8)
            result = Image.fromarray(result_array)
            
            output = io.BytesIO()
            result.save(output, format="JPEG", quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"分离色调失败: {e}")
            raise
    
    @staticmethod
    def apply_color_grading(image_bytes: bytes, shadows: tuple = (0, 0, 0),
                           midtones: tuple = (0, 0, 0), highlights: tuple = (0, 0, 0),
                           intensity: float = 1.0) -> bytes:
        """
        色彩分级
        
        Args:
            image_bytes: 输入图片字节数据
            shadows: 阴影调整
            midtones: 中间调调整
            highlights: 高光调整
            intensity: 调整强度
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"应用色彩分级: 阴影={shadows}, 中间调={midtones}, 高光={highlights}, 强度={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img).astype(np.float32)
            
            # 转换为HSV获得亮度
            if CV2_AVAILABLE:
                hsv = cv2.cvtColor(img_array.astype(np.uint8), cv2.COLOR_RGB2HSV)
                brightness = hsv[:, :, 2] / 255.0
            else:
                # 使用简化的亮度计算
                brightness = np.mean(img_array, axis=2) / 255.0
            
            # 创建权重遮罩
            shadow_weight = np.maximum(0, 1 - brightness * 2)  # 0-0.5映射到1-0
            highlight_weight = np.maximum(0, (brightness - 0.5) * 2)  # 0.5-1映射到0-1
            midtone_weight = 1 - shadow_weight - highlight_weight
            
            result_array = img_array.copy()
            
            # 应用色彩分级
            for i in range(3):
                adjustment = (shadows[i] * shadow_weight +
                            midtones[i] * midtone_weight +
                            highlights[i] * highlight_weight) * intensity
                
                result_array[:, :, i] = np.clip(img_array[:, :, i] + adjustment, 0, 255)
            
            result = Image.fromarray(result_array.astype(np.uint8))
            
            output = io.BytesIO()
            result.save(output, format="JPEG", quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"色彩分级失败: {e}")
            raise
