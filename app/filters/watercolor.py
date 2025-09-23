import numpy as np
import cv2
from .utils import process_image, add_texture


def _watercolor_filter(img: np.ndarray, sigma_s: float = 60, sigma_r: float = 0.6, 
                      texture_strength: float = 0.1) -> np.ndarray:
    """
    实现水彩画效果滤镜
    
    Args:
        img: 输入图像的numpy数组
        sigma_s: 空间窗口半径，控制平滑度
        sigma_r: 色彩空间窗口半径，控制颜色保留程度
        texture_strength: 纹理强度
        
    Returns:
        处理后的图像数组
    """
    # 保存alpha通道（如果有）
    if len(img.shape) == 3 and img.shape[2] == 4:
        has_alpha = True
        alpha = img[:, :, 3]
        img_color = img[:, :, :3]
    else:
        has_alpha = False
        img_color = img
    
    # 转为BGR
    if len(img_color.shape) == 3:
        img_bgr = cv2.cvtColor(img_color, cv2.COLOR_RGB2BGR)
    else:
        img_bgr = img_color
    
    # 使用双边滤波进行平滑，保留边缘
    smoothed = cv2.bilateralFilter(img_bgr, 0, sigma_r * 100, sigma_s)
    
    # 边缘检测
    edges = cv2.Canny(cv2.cvtColor(smoothed, cv2.COLOR_BGR2GRAY), 100, 200)
    edges = cv2.dilate(edges, None)
    
    # 将边缘叠加到图像上
    mask = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    # 确保类型一致
    mask = (mask * 0.7).astype(smoothed.dtype)
    result = cv2.subtract(smoothed, mask)
    
    # 添加一点点噪声纹理模拟水彩效果
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    result = add_texture(result, texture_strength)
    
    # 如果原图有Alpha通道，保留
    if has_alpha:
        result_rgba = np.zeros((result.shape[0], result.shape[1], 4), dtype=np.uint8)
        result_rgba[:, :, :3] = result
        result_rgba[:, :, 3] = alpha
        return result_rgba
    
    return result


def apply_watercolor(image_bytes: bytes, sigma_s: float = 60, sigma_r: float = 0.6, 
                    texture_strength: float = 0.1, intensity: float = 1.0) -> bytes:
    """
    应用水彩滤镜到图像
    
    Args:
        image_bytes: 输入图片的字节数据
        sigma_s: 空间窗口半径，控制平滑度
        sigma_r: 色彩空间窗口半径，控制颜色保留程度
        texture_strength: 纹理强度
        intensity: 效果强度
        
    Returns:
        处理后图片的字节数据
    """
    return process_image(
        image_bytes,
        _watercolor_filter,
        intensity=intensity,
        sigma_s=sigma_s,
        sigma_r=sigma_r,
        texture_strength=texture_strength
    ) 