from PIL import Image, ImageFilter
import io
import numpy as np
import cv2
from typing import Optional, Tuple
from ...utils.logger import logger


class BlurEffects:
    """模糊效果处理"""
    
    @staticmethod
    def motion_blur(
        image_bytes: bytes,
        angle: float = 0.0,
        length: int = 15,
        quality: int = 90
    ) -> bytes:
        """
        运动模糊效果
        
        Args:
            image_bytes: 输入图片的字节数据
            angle: 运动角度（度）
            length: 模糊长度
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"运动模糊: angle={angle}, length={length}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img)
            
            # 创建运动模糊核
            kernel = np.zeros((length, length))
            
            # 计算中心点
            center = length // 2
            
            # 将角度转换为弧度
            angle_rad = np.deg2rad(angle)
            
            # 计算运动方向上的点
            for i in range(length):
                offset = i - center
                x = int(center + offset * np.cos(angle_rad))
                y = int(center + offset * np.sin(angle_rad))
                
                # 确保坐标在核范围内
                if 0 <= x < length and 0 <= y < length:
                    kernel[y, x] = 1
            
            # 归一化核
            kernel = kernel / np.sum(kernel)
            
            # 应用卷积
            if len(img_array.shape) == 3:
                # 彩色图像
                result = np.zeros_like(img_array)
                for channel in range(img_array.shape[2]):
                    result[:, :, channel] = cv2.filter2D(img_array[:, :, channel], -1, kernel)
            else:
                # 灰度图像
                result = cv2.filter2D(img_array, -1, kernel)
            
            result_img = Image.fromarray(result.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"运动模糊失败: {str(e)}")
            raise
    
    @staticmethod
    def radial_blur(
        image_bytes: bytes,
        center_x: Optional[int] = None,
        center_y: Optional[int] = None,
        strength: float = 5.0,
        quality: int = 90
    ) -> bytes:
        """
        径向模糊效果
        
        Args:
            image_bytes: 输入图片的字节数据
            center_x: 模糊中心X坐标（None为图像中心）
            center_y: 模糊中心Y坐标（None为图像中心）
            strength: 模糊强度
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"径向模糊: center=({center_x}, {center_y}), strength={strength}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img)
            height, width = img_array.shape[:2]
            
            # 设置默认中心点
            if center_x is None:
                center_x = width // 2
            if center_y is None:
                center_y = height // 2
            
            # 创建距离映射
            y, x = np.ogrid[:height, :width]
            distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            
            # 归一化距离
            max_distance = np.sqrt(width**2 + height**2) / 2
            normalized_distance = distance / max_distance
            
            # 计算模糊半径（基于距离）
            blur_radius = normalized_distance * strength
            
            # 应用径向模糊
            result = img_array.copy().astype(np.float32)
            
            for i in range(height):
                for j in range(width):
                    radius = int(blur_radius[i, j])
                    if radius > 0:
                        # 创建局部模糊区域
                        y1 = max(0, i - radius)
                        y2 = min(height, i + radius + 1)
                        x1 = max(0, j - radius)
                        x2 = min(width, j + radius + 1)
                        
                        # 计算平均值
                        if len(img_array.shape) == 3:
                            for c in range(img_array.shape[2]):
                                result[i, j, c] = np.mean(img_array[y1:y2, x1:x2, c])
                        else:
                            result[i, j] = np.mean(img_array[y1:y2, x1:x2])
            
            result_img = Image.fromarray(result.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"径向模糊失败: {str(e)}")
            raise
    
    @staticmethod
    def surface_blur(
        image_bytes: bytes,
        radius: int = 5,
        threshold: int = 15,
        quality: int = 90
    ) -> bytes:
        """
        表面模糊效果（保边模糊）
        
        Args:
            image_bytes: 输入图片的字节数据
            radius: 模糊半径
            threshold: 边缘阈值
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"表面模糊: radius={radius}, threshold={threshold}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img)
            
            # 使用双边滤波实现表面模糊
            if len(img_array.shape) == 3:
                # 彩色图像
                result = cv2.bilateralFilter(img_array, radius * 2 + 1, threshold * 2, radius * 2)
            else:
                # 灰度图像
                result = cv2.bilateralFilter(img_array, radius * 2 + 1, threshold * 2, radius * 2)
            
            result_img = Image.fromarray(result)
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"表面模糊失败: {str(e)}")
            raise
