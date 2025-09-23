import numpy as np
import cv2
from .utils import process_image, adjust_contrast


def _poster_edges_filter(img: np.ndarray, posterize_levels: int = 6, 
                       edge_thickness: int = 1, edge_threshold: int = 100) -> np.ndarray:
    """
    实现海报边缘效果滤镜
    
    Args:
        img: 输入图像的numpy数组
        posterize_levels: 海报化级别，控制颜色数量
        edge_thickness: 边缘线条粗细
        edge_threshold: 边缘检测阈值
        
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
    
    # 强化对比度，使边缘更明显
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    enhanced_lab = cv2.merge((cl, a, b))
    enhanced_bgr = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    # 颜色量化（减少颜色数量）
    # 使用k-means聚类进行更好的颜色量化
    Z = enhanced_bgr.reshape((-1, 3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(Z, posterize_levels, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    posterized = res.reshape((enhanced_bgr.shape))
    
    # 边缘检测
    gray = cv2.cvtColor(enhanced_bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, edge_threshold, edge_threshold * 2)
    
    # 加粗边缘
    kernel = np.ones((edge_thickness, edge_thickness), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    # 反转边缘（黑色变为白色）并增强对比度
    edges = 255 - edges
    edges = cv2.equalizeHist(edges)
    
    # 将边缘叠加到量化后的图像上
    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    # 使用乘法混合模式
    result = cv2.multiply(posterized, edges_bgr / 255.0).astype(np.uint8)
    
    # 转回RGB
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    
    # 如果原图有Alpha通道，保留
    if has_alpha:
        result_rgba = np.zeros((result.shape[0], result.shape[1], 4), dtype=np.uint8)
        result_rgba[:, :, :3] = result
        result_rgba[:, :, 3] = alpha
        return result_rgba
    
    return result


def apply_poster_edges(image_bytes: bytes, posterize_levels: int = 6, 
                      edge_thickness: int = 1, edge_threshold: int = 100,
                      intensity: float = 1.0) -> bytes:
    """
    应用海报边缘滤镜到图像
    
    Args:
        image_bytes: 输入图片的字节数据
        posterize_levels: 海报化级别，控制颜色数量
        edge_thickness: 边缘线条粗细
        edge_threshold: 边缘检测阈值
        intensity: 效果强度
        
    Returns:
        处理后图片的字节数据
    """
    # 参数范围限制
    posterize_levels = max(2, min(posterize_levels, 16))
    edge_thickness = max(1, min(edge_thickness, 5))
    
    return process_image(
        image_bytes,
        _poster_edges_filter,
        intensity=intensity,
        posterize_levels=posterize_levels,
        edge_thickness=edge_thickness,
        edge_threshold=edge_threshold
    ) 