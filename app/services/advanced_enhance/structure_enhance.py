from PIL import Image
import io
import numpy as np
import cv2
from typing import Optional
from ...utils.logger import logger


class StructureEnhance:
    """结构增强"""
    
    @staticmethod
    def apply_structure_enhance(image_bytes: bytes, intensity: float = 1.0) -> bytes:
        """
        结构增强
        
        Args:
            image_bytes: 输入图片字节数据
            intensity: 增强强度
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"结构增强: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img, dtype=np.float32)
            
            # 使用双边滤波保持边缘
            bilateral = cv2.bilateralFilter(img_array.astype('uint8'), 9, 75, 75).astype(np.float32)
            
            # 计算结构信息
            structure = img_array - bilateral
            
            # 增强结构
            enhanced = img_array + intensity * structure
            
            # 限制像素值范围
            enhanced = np.clip(enhanced, 0, 255)
            
            result_img = Image.fromarray(enhanced.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"结构增强失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_micro_contrast(image_bytes: bytes, radius: int = 10, intensity: float = 1.0) -> bytes:
        """
        微对比度增强
        
        Args:
            image_bytes: 输入图片字节数据
            radius: 增强半径
            intensity: 增强强度
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"微对比度增强: radius={radius}, intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img, dtype=np.float32)
            
            # 创建局部平均
            kernel = np.ones((radius, radius)) / (radius * radius)
            
            if len(img_array.shape) == 3:
                local_mean = np.zeros_like(img_array)
                for c in range(3):
                    local_mean[:, :, c] = cv2.filter2D(img_array[:, :, c], -1, kernel)
            else:
                local_mean = cv2.filter2D(img_array, -1, kernel)
            
            # 计算局部对比度
            local_contrast = img_array - local_mean
            
            # 增强微对比度
            enhanced = img_array + intensity * local_contrast
            
            # 限制像素值范围
            enhanced = np.clip(enhanced, 0, 255)
            
            result_img = Image.fromarray(enhanced.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"微对比度增强失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_laplacian_enhance(image_bytes: bytes, intensity: float = 1.0) -> bytes:
        """
        拉普拉斯增强
        
        Args:
            image_bytes: 输入图片字节数据
            intensity: 增强强度
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"拉普拉斯增强: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img, dtype=np.float32)
            
            # 拉普拉斯核
            laplacian_kernel = np.array([
                [0, -1, 0],
                [-1, 4, -1],
                [0, -1, 0]
            ])
            
            if len(img_array.shape) == 3:
                laplacian = np.zeros_like(img_array)
                for c in range(3):
                    laplacian[:, :, c] = cv2.filter2D(img_array[:, :, c], -1, laplacian_kernel)
            else:
                laplacian = cv2.filter2D(img_array, -1, laplacian_kernel)
            
            # 应用增强
            enhanced = img_array + intensity * laplacian
            
            # 限制像素值范围
            enhanced = np.clip(enhanced, 0, 255)
            
            result_img = Image.fromarray(enhanced.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"拉普拉斯增强失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_sobel_enhance(image_bytes: bytes, intensity: float = 1.0) -> bytes:
        """
        Sobel边缘增强
        
        Args:
            image_bytes: 输入图片字节数据
            intensity: 增强强度
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"Sobel边缘增强: intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img, dtype=np.float32)
            
            if len(img_array.shape) == 3:
                # 转换为灰度进行边缘检测
                gray = cv2.cvtColor(img_array.astype('uint8'), cv2.COLOR_RGB2GRAY).astype(np.float32)
            else:
                gray = img_array.copy()
            
            # Sobel边缘检测
            sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
            
            # 归一化
            sobel_magnitude = sobel_magnitude / sobel_magnitude.max() * 255
            
            # 应用增强
            if len(img_array.shape) == 3:
                enhanced = img_array.copy()
                for c in range(3):
                    enhanced[:, :, c] += intensity * sobel_magnitude
            else:
                enhanced = img_array + intensity * sobel_magnitude
            
            # 限制像素值范围
            enhanced = np.clip(enhanced, 0, 255)
            
            result_img = Image.fromarray(enhanced.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Sobel边缘增强失败: {str(e)}")
            raise
