import numpy as np
import cv2
from .utils import process_image, add_texture


def _rough_pastels_filter(img: np.ndarray, stroke_size: int = 3, color_levels: int = 8,
                        texture_strength: float = 0.5, stroke_detail: int = 2) -> np.ndarray:
    """
    实现粗糙蜡笔效果滤镜
    
    Args:
        img: 输入图像的numpy数组
        stroke_size: 笔触大小
        color_levels: 颜色层次数量
        texture_strength: 纹理强度
        stroke_detail: 笔触细节级别
        
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
    
    # 步骤1: 使用双边滤波保持边缘
    bilateral = cv2.bilateralFilter(img_bgr, 9, 75, 75)
    
    # 步骤2: 使用中值模糊模拟蜡笔笔触
    median = cv2.medianBlur(bilateral, stroke_size)
    
    # 步骤3: 锐化以增强笔触效果
    for _ in range(stroke_detail):
        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
        median = cv2.filter2D(median, -1, kernel)
    
    # 步骤4: 颜色量化减少色彩数量
    Z = median.reshape((-1, 3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(Z, color_levels, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    quantized = res.reshape((median.shape))
    
    # 步骤5: 添加粗糙纹理
    # 首先转换为RGB
    result = cv2.cvtColor(quantized, cv2.COLOR_BGR2RGB)
    
    # 创建仿纸张纹理
    height, width = result.shape[:2]
    canvas = np.ones((height, width, 3), dtype=np.uint8) * 240  # 浅灰色画布
    
    # 添加随机噪点模拟纸张质感
    noise = np.random.randint(-40, 40, (height, width, 3))
    canvas = np.clip(canvas + noise, 0, 255).astype(np.uint8)
    
    # 使用Multiply混合模式将图像应用到画布上
    canvas_norm = canvas.astype(float) / 255.0
    result_norm = result.astype(float) / 255.0
    blended = (result_norm * canvas_norm * 255.0).astype(np.uint8)
    
    # 添加更多噪点纹理模拟蜡笔
    texture_img = add_texture(blended, texture_strength, seed=42)
    
    # 如果原图有Alpha通道，保留
    if has_alpha:
        result_rgba = np.zeros((texture_img.shape[0], texture_img.shape[1], 4), dtype=np.uint8)
        result_rgba[:, :, :3] = texture_img
        result_rgba[:, :, 3] = alpha
        return result_rgba
    
    return texture_img


def apply_rough_pastels(image_bytes: bytes, stroke_size: int = 3, color_levels: int = 8,
                       texture_strength: float = 0.5, stroke_detail: int = 2,
                       intensity: float = 1.0) -> bytes:
    """
    应用粗糙蜡笔滤镜到图像
    
    Args:
        image_bytes: 输入图片的字节数据
        stroke_size: 笔触大小（必须是奇数）
        color_levels: 颜色层次数量
        texture_strength: 纹理强度
        stroke_detail: 笔触细节级别
        intensity: 效果强度
        
    Returns:
        处理后图片的字节数据
    """
    # 确保笔触大小为奇数
    if stroke_size % 2 == 0:
        stroke_size += 1
    
    # 参数范围限制
    stroke_size = max(3, min(stroke_size, 9))
    color_levels = max(4, min(color_levels, 16))
    texture_strength = max(0.1, min(texture_strength, 1.0))
    stroke_detail = max(1, min(stroke_detail, 3))
    
    return process_image(
        image_bytes,
        _rough_pastels_filter,
        intensity=intensity,
        stroke_size=stroke_size,
        color_levels=color_levels,
        texture_strength=texture_strength,
        stroke_detail=stroke_detail
    ) 