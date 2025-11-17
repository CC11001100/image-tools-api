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

    def process_noise(
        self,
        image_bytes: bytes,
        noise_type: str,
        intensity: float = 1.0,
        quality: int = 90,
        **kwargs
    ) -> bytes:
        """
        通用噪声添加方法
        
        Args:
            image_bytes: 图像字节数据
            noise_type: 噪声类型
            intensity: 噪声强度
            quality: 输出质量
            **kwargs: 其他参数
            
        Returns:
            处理后的图像字节数据
        """
        import io
        
        try:
            # 加载图像
            image = Image.open(io.BytesIO(image_bytes))
            
            # 确保图像模式为RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # 根据噪声类型调用相应方法
            if noise_type == "gaussian":
                # 强度转换为标准差
                std = intensity * 25.0
                processed_image = self.add_gaussian_noise(image, std=std, **kwargs)
            elif noise_type in ["salt_and_pepper", "salt_pepper"]:
                # 强度转换为概率
                prob = intensity * 0.05
                processed_image = self.add_salt_pepper_noise(
                    image, 
                    salt_prob=prob, 
                    pepper_prob=prob, 
                    **kwargs
                )
            elif noise_type == "uniform":
                # 强度转换为范围
                range_val = intensity * 25.0
                processed_image = self.add_uniform_noise(
                    image, 
                    low=-range_val, 
                    high=range_val, 
                    **kwargs
                )
            elif noise_type == "speckle":
                # 强度转换为方差
                variance = intensity * 0.1
                processed_image = self.add_speckle_noise(image, variance=variance, **kwargs)
            elif noise_type == "poisson":
                # 泊松噪声的简化实现
                processed_image = self._add_poisson_noise(image, intensity=intensity, **kwargs)
            else:
                raise ValueError(f"不支持的噪声类型: {noise_type}")
            
            # 保存到字节流
            output = io.BytesIO()
            processed_image.save(
                output, 
                format='JPEG', 
                quality=quality,
                optimize=True
            )
            
            return output.getvalue()
            
        except Exception as e:
            print(f"添加噪声时出错: {e}")
            # 如果处理失败，返回原图
            return image_bytes
    
    def _add_poisson_noise(
        self,
        image: Image.Image,
        intensity: float = 1.0,
        **kwargs
    ) -> Image.Image:
        """
        添加泊松噪声（简化实现）
        
        Args:
            image: PIL图像对象
            intensity: 噪声强度
            **kwargs: 其他参数
            
        Returns:
            处理后的图像
        """
        try:
            # 转换为numpy数组
            img_array = np.array(image).astype(np.float64)
            
            # 生成泊松噪声
            # 泊松分布的参数lambda等于像素值
            scaling_factor = intensity * 0.1
            
            # 归一化到适当范围
            normalized = img_array / 255.0
            
            # 生成泊松噪声
            noise = np.random.poisson(normalized * 100) * scaling_factor
            
            # 添加噪声
            noisy_array = img_array + noise
            
            # 限制像素值范围
            noisy_array = np.clip(noisy_array, 0, 255)
            
            # 转换回PIL图像
            return Image.fromarray(noisy_array.astype(np.uint8))
            
        except Exception as e:
            print(f"添加泊松噪声时出错: {e}")
            return image

    @classmethod
    def add_noise(
        cls,
        image_bytes: bytes,
        noise_type: str,
        intensity: float = 1.0,
        quality: int = 90,
        **kwargs
    ) -> bytes:
        """
        类方法版本的噪声添加方法
        
        Args:
            image_bytes: 图像字节数据
            noise_type: 噪声类型
            intensity: 噪声强度
            quality: 输出质量
            **kwargs: 其他参数
            
        Returns:
            处理后的图像字节数据
        """
        service = cls()
        return service.process_noise(
            image_bytes=image_bytes,
            noise_type=noise_type,
            intensity=intensity,
            quality=quality,
            **kwargs
        )


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
