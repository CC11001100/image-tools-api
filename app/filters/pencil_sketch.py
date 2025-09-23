import numpy as np
import cv2
from .utils import process_image


def _pencil_sketch_filter(img: np.ndarray, sigma_s: float = 60, sigma_r: float = 0.07,
                         shade_factor: float = 0.1) -> np.ndarray:
    """
    实现铅笔素描效果滤镜
    
    Args:
        img: 输入图像的numpy数组
        sigma_s: 空间窗口半径，控制平滑度
        sigma_r: 色彩空间窗口半径，控制颜色保留程度
        shade_factor: 阴影效果因子
        
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
    
    # 使用OpenCV的铅笔素描滤镜
    gray, color = cv2.pencilSketch(img_bgr, sigma_s=sigma_s, sigma_r=sigma_r, shade_factor=shade_factor)
    
    # 将灰度素描和彩色保持混合
    gray_rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    color = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)
    
    # 使用彩色铅笔效果（可以通过调整blend_factor来控制彩色程度）
    blend_factor = 0.0  # 1.0表示完全使用彩色，0.0表示完全使用灰度
    result = cv2.addWeighted(cv2.cvtColor(gray_rgb, cv2.COLOR_BGR2RGB), 1 - blend_factor, 
                            color, blend_factor, 0)
    
    # 如果原图有Alpha通道，保留
    if has_alpha:
        result_rgba = np.zeros((result.shape[0], result.shape[1], 4), dtype=np.uint8)
        result_rgba[:, :, :3] = result
        result_rgba[:, :, 3] = alpha
        return result_rgba
    
    return result


def apply_pencil_sketch(image_bytes: bytes, sigma_s: float = 60, sigma_r: float = 0.07,
                       shade_factor: float = 0.1, intensity: float = 1.0) -> bytes:
    """
    应用铅笔素描滤镜到图像
    
    Args:
        image_bytes: 输入图片的字节数据
        sigma_s: 空间窗口半径，控制平滑度
        sigma_r: 色彩空间窗口半径，控制颜色保留程度
        shade_factor: 阴影效果因子
        intensity: 效果强度
        
    Returns:
        处理后图片的字节数据
    """
    return process_image(
        image_bytes,
        _pencil_sketch_filter,
        intensity=intensity,
        sigma_s=sigma_s,
        sigma_r=sigma_r,
        shade_factor=shade_factor
    ) 