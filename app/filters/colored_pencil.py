import numpy as np
import cv2
from .utils import process_image, add_texture


def _colored_pencil_filter(img: np.ndarray, line_size: int = 7, blur_value: int = 7,
                         edge_threshold: int = 50, texture_strength: float = 0.1) -> np.ndarray:
    """
    实现彩色铅笔效果滤镜
    
    Args:
        img: 输入图像的numpy数组
        line_size: 线条大小
        blur_value: 模糊值，用于细化边缘
        edge_threshold: 边缘检测阈值
        texture_strength: 纹理强度
        
    Returns:
        处理后的图像数组
    """
    # 保存alpha通道（如果有）
    if len(img.shape) == 3 and img.shape[2] == 4:
        has_alpha = True
        alpha = img[:, :, 3]
        img_rgb = img[:, :, :3]
    else:
        has_alpha = False
        img_rgb = img
    
    # 转为BGR
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    
    # 保持颜色，但增强边缘
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    img_gray_blur = cv2.GaussianBlur(img_gray, (blur_value, blur_value), 0)
    
    # 使用Canny边缘检测来获取线条
    edges = cv2.Canny(img_gray_blur, edge_threshold, edge_threshold * 2)
    
    # 反转边缘图像（使线条为白色，背景为黑色）
    edges = 255 - edges
    
    # 膨胀边缘使线条更粗
    kernel = np.ones((line_size, line_size), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    # 边缘模糊使线条看起来更自然
    edges = cv2.GaussianBlur(edges, (blur_value, blur_value), 0)
    
    # 创建彩色铅笔效果
    # 1. 将原始图像颜色量化
    # 这里使用K-means聚类来减少颜色数量
    Z = img_bgr.reshape((-1, 3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 8  # 颜色数量
    _, labels, centers = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    quantized = res.reshape((img_bgr.shape))
    
    # 2. 边缘与量化后的图像混合
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    # 使用边缘作为蒙版，使线条更明显
    result = cv2.bitwise_and(quantized, edges_colored)
    
    # 添加一些纹理
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    result = add_texture(result, texture_strength)
    
    # 如果原图有Alpha通道，保留
    if has_alpha:
        result_rgba = np.zeros((result.shape[0], result.shape[1], 4), dtype=np.uint8)
        result_rgba[:, :, :3] = result
        result_rgba[:, :, 3] = alpha
        return result_rgba
    
    return result


def apply_colored_pencil(image_bytes: bytes, line_size: int = 7, blur_value: int = 7,
                        edge_threshold: int = 50, texture_strength: float = 0.1,
                        intensity: float = 1.0) -> bytes:
    """
    应用彩色铅笔滤镜到图像
    
    Args:
        image_bytes: 输入图片的字节数据
        line_size: 线条大小
        blur_value: 模糊值，用于细化边缘
        edge_threshold: 边缘检测阈值
        texture_strength: 纹理强度
        intensity: 效果强度
        
    Returns:
        处理后图片的字节数据
    """
    return process_image(
        image_bytes,
        _colored_pencil_filter,
        intensity=intensity,
        line_size=line_size,
        blur_value=blur_value,
        edge_threshold=edge_threshold,
        texture_strength=texture_strength
    ) 