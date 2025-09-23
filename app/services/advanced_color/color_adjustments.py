"""高级色彩调整功能"""
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import io
from typing import Optional, Tuple, Dict, Any
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


class ColorAdjustments:
    """高级色彩调整功能"""
    
    @staticmethod
    def apply_curves(image_bytes: bytes, curve_points: list = None, intensity: float = 1.0) -> bytes:
        """
        应用曲线调整
        
        Args:
            image_bytes: 输入图片字节数据
            curve_points: 曲线控制点列表
            intensity: 调整强度
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"应用曲线调整: 强度={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 默认曲线点（S型曲线）
            if curve_points is None:
                curve_points = [(0, 0), (64, 48), (128, 128), (192, 208), (255, 255)]
            
            # 创建查找表
            lut = []
            for i in range(256):
                # 线性插值计算曲线值
                value = ColorAdjustments._interpolate_curve(i, curve_points)
                # 应用强度
                adjusted_value = int(i + (value - i) * intensity)
                lut.append(max(0, min(255, adjusted_value)))
            
            # 应用查找表
            if CV2_AVAILABLE:
                img_array = np.array(img)
                for channel in range(3):
                    img_array[:, :, channel] = np.array(lut)[img_array[:, :, channel]]
                result_img = Image.fromarray(img_array)
            else:
                # 使用PIL的point方法
                result_img = img.point(lut * 3)
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"曲线调整失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_channel_mixer(image_bytes: bytes, red_weights: tuple = (1, 0, 0), 
                           green_weights: tuple = (0, 1, 0), blue_weights: tuple = (0, 0, 1)) -> bytes:
        """
        应用通道混合器
        
        Args:
            image_bytes: 输入图片字节数据
            red_weights: 红色通道权重 (R, G, B)
            green_weights: 绿色通道权重 (R, G, B)
            blue_weights: 蓝色通道权重 (R, G, B)
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"应用通道混合器: R={red_weights}, G={green_weights}, B={blue_weights}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img, dtype=np.float32)
            height, width, channels = img_array.shape
            
            # 分离通道
            r_channel = img_array[:, :, 0]
            g_channel = img_array[:, :, 1]
            b_channel = img_array[:, :, 2]
            
            # 应用通道混合
            new_r = (r_channel * red_weights[0] + 
                    g_channel * red_weights[1] + 
                    b_channel * red_weights[2])
            
            new_g = (r_channel * green_weights[0] + 
                    g_channel * green_weights[1] + 
                    b_channel * green_weights[2])
            
            new_b = (r_channel * blue_weights[0] + 
                    g_channel * blue_weights[1] + 
                    b_channel * blue_weights[2])
            
            # 合并通道并限制范围
            result_array = np.stack([new_r, new_g, new_b], axis=2)
            result_array = np.clip(result_array, 0, 255).astype(np.uint8)
            
            result_img = Image.fromarray(result_array)
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"通道混合失败: {str(e)}")
            raise
    
    @staticmethod
    def _interpolate_curve(x: int, points: list) -> int:
        """插值计算曲线值"""
        # 找到x所在的区间
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            
            if x1 <= x <= x2:
                # 线性插值
                if x2 == x1:
                    return y1
                t = (x - x1) / (x2 - x1)
                return int(y1 + t * (y2 - y1))
        
        # 超出范围的情况
        if x < points[0][0]:
            return points[0][1]
        else:
            return points[-1][1]
