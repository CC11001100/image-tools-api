"""
噪声服务模块 - 向后兼容实现
"""

from typing import Optional, Tuple, List, Dict, Any
from PIL import Image, ImageFilter
import numpy as np
import random


class NoiseService:
    """图像噪声处理服务"""
    
    def __init__(self):
        pass
        
    def add_gaussian_noise(
        self,
        image: Image.Image,
        mean: float = 0.0,
        std: float = 25.0,
        **kwargs
    ) -> Image.Image:
        """
        添加高斯噪声
        
        Args:
            image: PIL图像对象
            mean: 噪声均值
            std: 噪声标准差
            **kwargs: 其他参数
            
        Returns:
            处理后的图像
        """
        try:
            # 转换为numpy数组
            img_array = np.array(image)
            
            # 生成高斯噪声
            noise = np.random.normal(mean, std, img_array.shape)
            
            # 添加噪声
            noisy_array = img_array + noise
            
            # 限制像素值范围
            noisy_array = np.clip(noisy_array, 0, 255)
            
            # 转换回PIL图像
            return Image.fromarray(noisy_array.astype(np.uint8))
            
        except Exception as e:
            print(f"添加高斯噪声时出错: {e}")
            return image
    
    def add_salt_pepper_noise(
        self,
        image: Image.Image,
        salt_prob: float = 0.01,
        pepper_prob: float = 0.01,
        **kwargs
    ) -> Image.Image:
        """
        添加椒盐噪声
        
        Args:
            image: PIL图像对象
            salt_prob: 盐噪声概率
            pepper_prob: 胡椒噪声概率
            **kwargs: 其他参数
            
        Returns:
            处理后的图像
        """
        try:
            # 转换为numpy数组
            img_array = np.array(image)
            
            # 生成随机数组
            random_array = np.random.random(img_array.shape[:2])
            
            # 添加盐噪声（白点）
            salt_mask = random_array < salt_prob
            img_array[salt_mask] = 255
            
            # 添加胡椒噪声（黑点）
            pepper_mask = random_array > (1 - pepper_prob)
            img_array[pepper_mask] = 0
            
            # 转换回PIL图像
            return Image.fromarray(img_array.astype(np.uint8))
            
        except Exception as e:
            print(f"添加椒盐噪声时出错: {e}")
            return image
    
    def add_uniform_noise(
        self,
        image: Image.Image,
        low: float = -25.0,
        high: float = 25.0,
        **kwargs
    ) -> Image.Image:
        """
        添加均匀噪声
        
        Args:
            image: PIL图像对象
            low: 噪声下限
            high: 噪声上限
            **kwargs: 其他参数
            
        Returns:
            处理后的图像
        """
        try:
            # 转换为numpy数组
            img_array = np.array(image)
            
            # 生成均匀噪声
            noise = np.random.uniform(low, high, img_array.shape)
            
            # 添加噪声
            noisy_array = img_array + noise
            
            # 限制像素值范围
            noisy_array = np.clip(noisy_array, 0, 255)
            
            # 转换回PIL图像
            return Image.fromarray(noisy_array.astype(np.uint8))
            
        except Exception as e:
            print(f"添加均匀噪声时出错: {e}")
            return image
    
    def add_speckle_noise(
        self,
        image: Image.Image,
        variance: float = 0.1,
        **kwargs
    ) -> Image.Image:
        """
        添加斑点噪声
        
        Args:
            image: PIL图像对象
            variance: 噪声方差
            **kwargs: 其他参数
            
        Returns:
            处理后的图像
        """
        try:
            # 转换为numpy数组
            img_array = np.array(image).astype(np.float64)
            
            # 生成斑点噪声
            noise = np.random.randn(*img_array.shape) * variance
            
            # 添加噪声（乘性噪声）
            noisy_array = img_array + img_array * noise
            
            # 限制像素值范围
            noisy_array = np.clip(noisy_array, 0, 255)
            
            # 转换回PIL图像
            return Image.fromarray(noisy_array.astype(np.uint8))
            
        except Exception as e:
            print(f"添加斑点噪声时出错: {e}")
            return image
    
    def denoise_median(
        self,
        image: Image.Image,
        size: int = 3,
        **kwargs
    ) -> Image.Image:
        """
        中值滤波去噪
        
        Args:
            image: PIL图像对象
            size: 滤波器大小
            **kwargs: 其他参数
            
        Returns:
            处理后的图像
        """
        try:
            # 使用PIL的中值滤波
            return image.filter(ImageFilter.MedianFilter(size=size))
            
        except Exception as e:
            print(f"中值滤波去噪时出错: {e}")
            return image
    
    def denoise_gaussian(
        self,
        image: Image.Image,
        radius: float = 1.0,
        **kwargs
    ) -> Image.Image:
        """
        高斯滤波去噪
        
        Args:
            image: PIL图像对象
            radius: 高斯滤波半径
            **kwargs: 其他参数
            
        Returns:
            处理后的图像
        """
        try:
            # 使用PIL的高斯滤波
            return image.filter(ImageFilter.GaussianBlur(radius=radius))
            
        except Exception as e:
            print(f"高斯滤波去噪时出错: {e}")
            return image
    
    def denoise_bilateral(
        self,
        image: Image.Image,
        **kwargs
    ) -> Image.Image:
        """
        双边滤波去噪（简化实现）
        
        Args:
            image: PIL图像对象
            **kwargs: 其他参数
            
        Returns:
            处理后的图像
        """
        try:
            # 简化实现：使用高斯滤波代替
            return image.filter(ImageFilter.GaussianBlur(radius=1.5))
            
        except Exception as e:
            print(f"双边滤波去噪时出错: {e}")
            return image


# 创建全局实例
noise_service = NoiseService()

# 导出函数
def add_gaussian_noise(*args, **kwargs):
    """添加高斯噪声"""
    return noise_service.add_gaussian_noise(*args, **kwargs)

def add_salt_pepper_noise(*args, **kwargs):
    """添加椒盐噪声"""
    return noise_service.add_salt_pepper_noise(*args, **kwargs)

def add_uniform_noise(*args, **kwargs):
    """添加均匀噪声"""
    return noise_service.add_uniform_noise(*args, **kwargs)

def add_speckle_noise(*args, **kwargs):
    """添加斑点噪声"""
    return noise_service.add_speckle_noise(*args, **kwargs)

def denoise_median(*args, **kwargs):
    """中值滤波去噪"""
    return noise_service.denoise_median(*args, **kwargs)

def denoise_gaussian(*args, **kwargs):
    """高斯滤波去噪"""
    return noise_service.denoise_gaussian(*args, **kwargs)

def denoise_bilateral(*args, **kwargs):
    """双边滤波去噪"""
    return noise_service.denoise_bilateral(*args, **kwargs)
