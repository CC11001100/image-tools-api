import cv2
import numpy as np
from typing import Tuple, Optional
from .utils import process_image


def _oil_painting_filter(img: np.ndarray, radius: int = 5, intensity: float = 10.0) -> np.ndarray:
    """
    实现油画效果滤镜
    
    Args:
        img: 输入图像的numpy数组
        radius: 邻域半径，值越大效果越明显
        intensity: 量化强度，值越大颜色分块效果越明显
        
    Returns:
        处理后的图像数组
    """
    # 确保参数有效
    radius = max(1, min(radius, 20))
    intensity = max(1.0, min(intensity, 20.0))
    
    # 转换为BGR格式，以便使用OpenCV
    if len(img.shape) == 3 and img.shape[2] == 4:  # 带有Alpha通道
        has_alpha = True
        alpha = img[:, :, 3]
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    else:
        has_alpha = False
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # 应用油画效果
    # 使用简化的油画效果实现，因为cv2.xphoto在某些版本中不可用
    # 使用双边滤波模拟油画效果
    oil_painting = cv2.bilateralFilter(img_bgr, radius * 2, intensity * 10, intensity * 10)
    
    # 添加一些量化效果
    oil_painting = (oil_painting // int(intensity)) * int(intensity)
    
    # 转换回RGB格式
    result = cv2.cvtColor(oil_painting, cv2.COLOR_BGR2RGB)
    
    # 如果原图有Alpha通道，保留
    if has_alpha:
        result_rgba = np.zeros((result.shape[0], result.shape[1], 4), dtype=np.uint8)
        result_rgba[:, :, :3] = result
        result_rgba[:, :, 3] = alpha
        return result_rgba
    
    return result


def apply_oil_painting(image_bytes: bytes, radius: int = 5, intensity: float = 10.0) -> bytes:
    """
    应用油画滤镜到图像
    
    Args:
        image_bytes: 输入图片的字节数据
        radius: 邻域半径，值越大效果越明显
        intensity: 量化强度，值越大颜色分块效果越明显
        
    Returns:
        处理后图片的字节数据
    """
    return process_image(
        image_bytes,
        _oil_painting_filter,
        radius=radius,
        intensity=intensity
    ) 