from PIL import Image
import io
import numpy as np
import cv2
from typing import Optional
from ...utils.logger import logger


class AdvancedSharpen:
    """高级锐化增强"""
    
    @staticmethod
    def apply_high_pass_sharpen(image_bytes: bytes, radius: float = 2.0, intensity: float = 1.0) -> bytes:
        """
        高通锐化
        
        Args:
            image_bytes: 输入图片字节数据
            radius: 高通滤波半径
            intensity: 锐化强度
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"高通锐化: radius={radius}, intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img, dtype=np.float32)
            
            # 应用高斯模糊
            blurred = cv2.GaussianBlur(img_array, (0, 0), radius)
            
            # 计算高通滤波结果
            high_pass = img_array - blurred
            
            # 应用锐化
            sharpened = img_array + intensity * high_pass
            
            # 限制像素值范围
            sharpened = np.clip(sharpened, 0, 255)
            
            result_img = Image.fromarray(sharpened.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"高通锐化失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_adaptive_sharpen(image_bytes: bytes, threshold: float = 0.5, intensity: float = 1.0) -> bytes:
        """
        自适应锐化
        
        Args:
            image_bytes: 输入图片字节数据
            threshold: 边缘检测阈值
            intensity: 锐化强度
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"自适应锐化: threshold={threshold}, intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img, dtype=np.float32)
            
            # 转换为灰度图进行边缘检测
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array.astype('uint8'), cv2.COLOR_RGB2GRAY).astype(np.float32)
            else:
                gray = img_array.copy()
            
            # 使用Sobel算子检测边缘
            sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            edge_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
            
            # 归一化边缘强度
            edge_magnitude = edge_magnitude / edge_magnitude.max()
            
            # 创建自适应掩模
            adaptive_mask = np.where(edge_magnitude > threshold, intensity, 0)
            
            # 应用高通滤波
            blurred = cv2.GaussianBlur(img_array, (0, 0), 1.0)
            high_pass = img_array - blurred
            
            # 根据边缘强度应用锐化
            if len(img_array.shape) == 3:
                for c in range(3):
                    img_array[:, :, c] += high_pass[:, :, c] * adaptive_mask
            else:
                img_array += high_pass * adaptive_mask
            
            # 限制像素值范围
            img_array = np.clip(img_array, 0, 255)
            
            result_img = Image.fromarray(img_array.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"自适应锐化失败: {str(e)}")
            raise
