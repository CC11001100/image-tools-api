import numpy as np
import cv2
from .utils import process_image, add_texture, adjust_contrast


def _dry_brush_filter(img: np.ndarray, brush_size: int = 5, detail_level: int = 25,
                    texture_strength: float = 0.15, contrast: float = 1.5) -> np.ndarray:
    """
    实现干画笔效果滤镜
    
    Args:
        img: 输入图像的numpy数组
        brush_size: 画笔大小
        detail_level: 细节级别，值越小细节越多
        texture_strength: 纹理强度
        contrast: 对比度调整
        
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
    
    # 应用中值滤波模拟干画笔效果
    median = cv2.medianBlur(img_bgr, brush_size)
    
    # 使用双边滤波保留边缘
    bilateral = cv2.bilateralFilter(median, 9, 75, 75)
    
    # 锐化图像以增强笔触效果
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])
    sharpened = cv2.filter2D(bilateral, -1, kernel)
    
    # 颜色量化来模拟干笔颜料效果
    # 减少颜色数量
    Z = sharpened.reshape((-1, 3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = detail_level  # 颜色数量
    _, labels, centers = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    quantized = res.reshape((sharpened.shape))
    
    # 增强边缘
    edges = cv2.Canny(cv2.cvtColor(quantized, cv2.COLOR_BGR2GRAY), 50, 150)
    edges = cv2.dilate(edges, None)
    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    # 合并边缘与量化图像
    # 确保类型一致
    edges_weighted = (edges_bgr * 0.3).astype(quantized.dtype)
    result = cv2.subtract(quantized, edges_weighted)
    
    # 转为RGB
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    
    # 增加对比度
    result = adjust_contrast(result, contrast)
    
    # 添加纹理
    result = add_texture(result, texture_strength)
    
    # 如果原图有Alpha通道，保留
    if has_alpha:
        result_rgba = np.zeros((result.shape[0], result.shape[1], 4), dtype=np.uint8)
        result_rgba[:, :, :3] = result
        result_rgba[:, :, 3] = alpha
        return result_rgba
    
    return result


def apply_dry_brush(image_bytes: bytes, brush_size: int = 5, detail_level: int = 25,
                  texture_strength: float = 0.15, contrast: float = 1.5, 
                  intensity: float = 1.0) -> bytes:
    """
    应用干画笔滤镜到图像
    
    Args:
        image_bytes: 输入图片的字节数据
        brush_size: 画笔大小
        detail_level: 细节级别，值越小细节越多
        texture_strength: 纹理强度
        contrast: 对比度调整
        intensity: 效果强度
        
    Returns:
        处理后图片的字节数据
    """
    # 确保参数在有效范围内
    brush_size = max(3, min(brush_size, 15))
    if brush_size % 2 == 0:
        brush_size += 1  # 确保为奇数
    
    detail_level = max(5, min(detail_level, 50))
    
    return process_image(
        image_bytes,
        _dry_brush_filter,
        intensity=intensity,
        brush_size=brush_size,
        detail_level=detail_level,
        texture_strength=texture_strength,
        contrast=contrast
    ) 