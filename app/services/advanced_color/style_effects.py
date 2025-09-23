"""风格效果功能"""
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


class StyleEffects:
    """风格效果功能"""
    
    @staticmethod
    def apply_vintage_film(image_bytes: bytes, film_type: str = "kodachrome", intensity: float = 1.0) -> bytes:
        """
        胶片风格
        
        Args:
            image_bytes: 输入图片字节数据
            film_type: 胶片类型
            intensity: 效果强度
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"应用胶片风格: 类型={film_type}, 强度={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img).astype(np.float32)
            
            # 不同胶片的色彩特性
            film_configs = {
                "kodachrome": {
                    "red_bias": 15,
                    "green_bias": -5,
                    "blue_bias": -10,
                    "contrast": 1.2,
                    "saturation": 1.1
                },
                "fujifilm": {
                    "red_bias": 10,
                    "green_bias": 5,
                    "blue_bias": -5,
                    "contrast": 1.1,
                    "saturation": 1.2
                },
                "agfa": {
                    "red_bias": 20,
                    "green_bias": 0,
                    "blue_bias": -15,
                    "contrast": 1.3,
                    "saturation": 0.9
                },
                "polaroid": {
                    "red_bias": 25,
                    "green_bias": 10,
                    "blue_bias": 0,
                    "contrast": 0.8,
                    "saturation": 0.8
                }
            }
            
            config = film_configs.get(film_type, film_configs["kodachrome"])
            
            # 应用色彩偏移
            img_array[:, :, 0] = np.clip(img_array[:, :, 0] + config["red_bias"] * intensity, 0, 255)
            img_array[:, :, 1] = np.clip(img_array[:, :, 1] + config["green_bias"] * intensity, 0, 255)
            img_array[:, :, 2] = np.clip(img_array[:, :, 2] + config["blue_bias"] * intensity, 0, 255)
            
            result = Image.fromarray(img_array.astype(np.uint8))
            
            # 应用对比度
            enhancer = ImageEnhance.Contrast(result)
            result = enhancer.enhance(1 + (config["contrast"] - 1) * intensity)
            
            # 应用饱和度
            enhancer = ImageEnhance.Color(result)
            result = enhancer.enhance(1 + (config["saturation"] - 1) * intensity)
            
            output = io.BytesIO()
            result.save(output, format="JPEG", quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"胶片风格失败: {e}")
            raise
    
    @staticmethod
    def apply_cinematic_look(image_bytes: bytes, look_type: str = "orange_teal", intensity: float = 1.0) -> bytes:
        """
        电影级调色
        
        Args:
            image_bytes: 输入图片字节数据
            look_type: 调色类型
            intensity: 效果强度
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"应用电影级调色: 类型={look_type}, 强度={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img).astype(np.float32)
            
            # 不同电影调色风格
            look_configs = {
                "orange_teal": {
                    "shadow_color": (20, 40, 80),
                    "highlight_color": (255, 180, 100),
                    "contrast": 1.2,
                    "saturation": 1.1
                },
                "bleach_bypass": {
                    "shadow_color": (0, 0, 0),
                    "highlight_color": (255, 255, 200),
                    "contrast": 1.5,
                    "saturation": 0.7
                },
                "matrix_green": {
                    "shadow_color": (0, 20, 0),
                    "highlight_color": (100, 255, 100),
                    "contrast": 1.3,
                    "saturation": 0.8
                },
                "noir": {
                    "shadow_color": (10, 10, 20),
                    "highlight_color": (200, 200, 220),
                    "contrast": 1.8,
                    "saturation": 0.3
                }
            }
            
            config = look_configs.get(look_type, look_configs["orange_teal"])
            
            # 计算亮度
            if CV2_AVAILABLE:
                hsv = cv2.cvtColor(img_array.astype(np.uint8), cv2.COLOR_RGB2HSV)
                brightness = hsv[:, :, 2] / 255.0
            else:
                brightness = np.mean(img_array, axis=2) / 255.0
            
            # 应用分离色调
            shadow_mask = brightness < 0.5
            highlight_mask = brightness >= 0.5
            
            result_array = img_array.copy()
            
            # 阴影色调
            shadow_strength = (0.5 - brightness) * 2
            shadow_strength = np.clip(shadow_strength, 0, 1)
            
            for i in range(3):
                result_array[:, :, i][shadow_mask] = (
                    img_array[:, :, i][shadow_mask] * (1 - shadow_strength[shadow_mask] * intensity * 0.2) +
                    config["shadow_color"][i] * shadow_strength[shadow_mask] * intensity * 0.2
                )
            
            # 高光色调
            highlight_strength = (brightness - 0.5) * 2
            highlight_strength = np.clip(highlight_strength, 0, 1)
            
            for i in range(3):
                result_array[:, :, i][highlight_mask] = (
                    img_array[:, :, i][highlight_mask] * (1 - highlight_strength[highlight_mask] * intensity * 0.2) +
                    config["highlight_color"][i] * highlight_strength[highlight_mask] * intensity * 0.2
                )
            
            result_array = np.clip(result_array, 0, 255).astype(np.uint8)
            result = Image.fromarray(result_array)
            
            # 应用对比度
            enhancer = ImageEnhance.Contrast(result)
            result = enhancer.enhance(1 + (config["contrast"] - 1) * intensity)
            
            # 应用饱和度
            enhancer = ImageEnhance.Color(result)
            result = enhancer.enhance(1 + (config["saturation"] - 1) * intensity)
            
            output = io.BytesIO()
            result.save(output, format="JPEG", quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"电影级调色失败: {e}")
            raise
