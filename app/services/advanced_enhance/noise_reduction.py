from PIL import Image
import io
import numpy as np
import cv2
from typing import Optional
from ...utils.logger import logger


class NoiseReduction:
    """降噪处理"""
    
    @staticmethod
    def apply_wiener_denoise(image_bytes: bytes, noise_variance: float = 0.1) -> bytes:
        """
        维纳滤波降噪
        
        Args:
            image_bytes: 输入图片字节数据
            noise_variance: 噪声方差
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"维纳滤波降噪: noise_variance={noise_variance}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img, dtype=np.float32)
            
            # 转换到频域
            if len(img_array.shape) == 3:
                # 彩色图像，分别处理每个通道
                result = np.zeros_like(img_array)
                for c in range(3):
                    # FFT变换
                    f_transform = np.fft.fft2(img_array[:, :, c])
                    f_shift = np.fft.fftshift(f_transform)
                    
                    # 计算功率谱
                    magnitude = np.abs(f_shift)
                    power_spectrum = magnitude ** 2
                    
                    # 维纳滤波
                    wiener_filter = power_spectrum / (power_spectrum + noise_variance)
                    
                    # 应用滤波器
                    filtered = f_shift * wiener_filter
                    
                    # 逆FFT变换
                    f_ishift = np.fft.ifftshift(filtered)
                    img_back = np.fft.ifft2(f_ishift)
                    result[:, :, c] = np.real(img_back)
            else:
                # 灰度图像
                f_transform = np.fft.fft2(img_array)
                f_shift = np.fft.fftshift(f_transform)
                
                magnitude = np.abs(f_shift)
                power_spectrum = magnitude ** 2
                
                wiener_filter = power_spectrum / (power_spectrum + noise_variance)
                
                filtered = f_shift * wiener_filter
                
                f_ishift = np.fft.ifftshift(filtered)
                img_back = np.fft.ifft2(f_ishift)
                result = np.real(img_back)
            
            # 限制像素值范围
            result = np.clip(result, 0, 255)
            
            result_img = Image.fromarray(result.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"维纳滤波降噪失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_morphological_denoise(image_bytes: bytes, kernel_size: int = 3) -> bytes:
        """
        形态学降噪
        
        Args:
            image_bytes: 输入图片字节数据
            kernel_size: 形态学核大小
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"形态学降噪: kernel_size={kernel_size}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img)
            
            # 创建形态学核
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
            
            # 应用开运算（先腐蚀后膨胀）去除小的噪点
            opened = cv2.morphologyEx(img_array, cv2.MORPH_OPEN, kernel)
            
            # 应用闭运算（先膨胀后腐蚀）填充小的空洞
            result = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
            
            result_img = Image.fromarray(result)
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"形态学降噪失败: {str(e)}")
            raise
