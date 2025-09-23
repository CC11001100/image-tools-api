from PIL import Image, ImageFilter, ImageEnhance
import io
import numpy as np
import cv2
from typing import Optional, Tuple
from ...utils.logger import logger


class SharpenEffects:
    """锐化效果处理"""
    
    @staticmethod
    def unsharp_mask(
        image_bytes: bytes,
        radius: float = 1.0,
        amount: float = 1.0,
        threshold: int = 0,
        quality: int = 90
    ) -> bytes:
        """
        USM锐化（反锐化掩模）
        
        Args:
            image_bytes: 输入图片的字节数据
            radius: 模糊半径
            amount: 锐化强度
            threshold: 阈值
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"USM锐化: radius={radius}, amount={amount}, threshold={threshold}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img, dtype=np.float32)
            
            # 创建模糊版本
            blurred = cv2.GaussianBlur(img_array, (0, 0), radius)
            
            # 计算差值（高频信息）
            high_freq = img_array - blurred
            
            # 应用阈值
            if threshold > 0:
                mask = np.abs(high_freq) >= threshold
                high_freq = high_freq * mask
            
            # 应用锐化
            sharpened = img_array + amount * high_freq
            
            # 限制像素值范围
            sharpened = np.clip(sharpened, 0, 255)
            
            result_img = Image.fromarray(sharpened.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"USM锐化失败: {str(e)}")
            raise
    
    @staticmethod
    def smart_sharpen(
        image_bytes: bytes,
        amount: float = 100.0,
        radius: float = 1.0,
        noise_reduction: float = 0.0,
        quality: int = 90
    ) -> bytes:
        """
        智能锐化
        
        Args:
            image_bytes: 输入图片的字节数据
            amount: 锐化强度 (0-500)
            radius: 锐化半径 (0.1-64)
            noise_reduction: 噪点减少 (0-100)
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"智能锐化: amount={amount}, radius={radius}, noise_reduction={noise_reduction}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img, dtype=np.float32)
            
            # 噪点减少预处理
            if noise_reduction > 0:
                # 使用双边滤波减少噪点
                noise_kernel_size = int(noise_reduction / 10) * 2 + 1
                img_array = cv2.bilateralFilter(img_array.astype('uint8'), noise_kernel_size, 
                                              noise_reduction, noise_reduction).astype(np.float32)
            
            # 边缘检测
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array.astype('uint8'), cv2.COLOR_RGB2GRAY).astype(np.float32)
            else:
                gray = img_array.copy()
            
            # 使用Laplacian算子检测边缘
            edges = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)
            edges = np.abs(edges)
            
            # 归一化边缘强度
            if edges.max() > 0:
                edges = edges / edges.max()
            
            # 创建自适应锐化掩模
            blur_radius = max(0.5, radius)
            blurred = cv2.GaussianBlur(img_array, (0, 0), blur_radius)
            
            # 计算高频信息
            high_freq = img_array - blurred
            
            # 根据边缘强度调整锐化强度
            if len(img_array.shape) == 3:
                # 彩色图像
                adaptive_amount = amount / 100.0
                for c in range(3):
                    high_freq[:, :, c] *= edges * adaptive_amount
                sharpened = img_array + high_freq
            else:
                # 灰度图像
                adaptive_amount = amount / 100.0
                high_freq *= edges * adaptive_amount
                sharpened = img_array + high_freq
            
            # 限制像素值范围
            sharpened = np.clip(sharpened, 0, 255)
            
            result_img = Image.fromarray(sharpened.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"智能锐化失败: {str(e)}")
            raise
    
    @staticmethod
    def edge_sharpen(
        image_bytes: bytes,
        strength: float = 1.0,
        quality: int = 90
    ) -> bytes:
        """
        边缘锐化
        
        Args:
            image_bytes: 输入图片的字节数据
            strength: 锐化强度
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"边缘锐化: strength={strength}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img, dtype=np.float32)
            
            # 定义边缘检测核
            edge_kernel = np.array([
                [-1, -1, -1],
                [-1,  8, -1],
                [-1, -1, -1]
            ]) * strength
            
            # 应用边缘检测
            if len(img_array.shape) == 3:
                # 彩色图像
                result = np.zeros_like(img_array)
                for c in range(3):
                    edges = cv2.filter2D(img_array[:, :, c], -1, edge_kernel)
                    result[:, :, c] = img_array[:, :, c] + edges
            else:
                # 灰度图像
                edges = cv2.filter2D(img_array, -1, edge_kernel)
                result = img_array + edges
            
            # 限制像素值范围
            result = np.clip(result, 0, 255)
            
            result_img = Image.fromarray(result.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"边缘锐化失败: {str(e)}")
            raise
