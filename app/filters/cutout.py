import numpy as np
import cv2
from .utils import process_image


def _cutout_filter(img: np.ndarray, levels: int = 5, edge_thickness: int = 2, 
                 edge_threshold: int = 50) -> np.ndarray:
    """
    实现木刻/剪纸效果滤镜
    
    Args:
        img: 输入图像的numpy数组
        levels: 颜色层次数量
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
    
    # 步骤1: 提取边缘
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, edge_threshold, edge_threshold * 2)
    
    # 加粗边缘
    kernel = np.ones((edge_thickness, edge_thickness), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    # 步骤2: 颜色量化（减少色彩层次）
    # 要求BGR形式
    div = 256 // levels
    quantized = (img_bgr // div) * div
    
    # 步骤3: 将边缘和量化后的图像合并
    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    result = cv2.subtract(quantized, edges_bgr)
    
    # 转回RGB
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    
    # 如果原图有Alpha通道，保留
    if has_alpha:
        result_rgba = np.zeros((result.shape[0], result.shape[1], 4), dtype=np.uint8)
        result_rgba[:, :, :3] = result
        result_rgba[:, :, 3] = alpha
        return result_rgba
    
    return result


def apply_cutout(image_bytes: bytes, levels: int = 5, edge_thickness: int = 2, 
               edge_threshold: int = 50, intensity: float = 1.0) -> bytes:
    """
    应用木刻/剪纸滤镜到图像
    
    Args:
        image_bytes: 输入图片的字节数据
        levels: 颜色层次数量
        edge_thickness: 边缘线条粗细
        edge_threshold: 边缘检测阈值
        intensity: 效果强度
        
    Returns:
        处理后图片的字节数据
    """
    # 参数范围限制
    levels = max(2, min(levels, 8))
    edge_thickness = max(1, min(edge_thickness, 5))
    
    return process_image(
        image_bytes,
        _cutout_filter,
        intensity=intensity,
        levels=levels,
        edge_thickness=edge_thickness,
        edge_threshold=edge_threshold
    ) 