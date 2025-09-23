import numpy as np
import cv2
from .utils import process_image, add_texture


def _fresco_filter(img: np.ndarray, roughness: float = 0.8, cracks: float = 0.6, 
                 color_decay: float = 0.4) -> np.ndarray:
    """
    实现壁画效果滤镜
    
    Args:
        img: 输入图像的numpy数组
        roughness: 粗糙度，控制纹理强度
        cracks: 裂痕强度，控制裂痕程度
        color_decay: 颜色褪色程度
        
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
    
    # 步骤1: 模糊以模拟壁画的平滑表面
    blurred = cv2.GaussianBlur(img_bgr, (5, 5), 0)
    
    # 步骤2: 降低饱和度模拟老化
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # 降低饱和度
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * (1 - color_decay), 0, 255).astype(np.uint8)
    # 降低亮度
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * (0.9 - color_decay * 0.3), 0, 255).astype(np.uint8)
    
    # 转回BGR
    aged = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    # 步骤3: 创建随机噪声作为纹理
    height, width = img_bgr.shape[:2]
    
    # 纹理噪声
    texture = np.random.normal(0.5, roughness, (height, width))
    texture = np.clip(texture, 0, 1)
    texture = (texture * 255).astype(np.uint8)
    
    # 创建裂痕效果（更大的噪声点）
    if cracks > 0:
        crack_mask = np.random.random((height, width)) > (1 - cracks * 0.05)
        crack_intensity = np.random.randint(30, 80, (height, width))
        texture[crack_mask] = crack_intensity[crack_mask]
    
    # 模糊纹理使其看起来更自然
    texture = cv2.GaussianBlur(texture, (5, 5), 0)
    
    # 将纹理应用到图像上
    texture_bgr = cv2.cvtColor(texture, cv2.COLOR_GRAY2BGR)
    
    # 使用相乘混合模式模拟壁画纹理
    result = cv2.multiply(aged, texture_bgr / 255.0, scale=1.0).astype(np.uint8)
    
    # 增加一些噪点和颗粒感
    grain = np.random.normal(0, 5, result.shape).astype(np.int16)
    result = np.clip(result.astype(np.int16) + grain, 0, 255).astype(np.uint8)
    
    # 转为RGB
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    
    # 如果原图有Alpha通道，保留
    if has_alpha:
        result_rgba = np.zeros((result.shape[0], result.shape[1], 4), dtype=np.uint8)
        result_rgba[:, :, :3] = result
        result_rgba[:, :, 3] = alpha
        return result_rgba
    
    return result


def apply_fresco(image_bytes: bytes, roughness: float = 0.8, cracks: float = 0.6,
               color_decay: float = 0.4, intensity: float = 1.0) -> bytes:
    """
    应用壁画滤镜到图像
    
    Args:
        image_bytes: 输入图片的字节数据
        roughness: 粗糙度，控制纹理强度
        cracks: 裂痕强度，控制裂痕程度
        color_decay: 颜色褪色程度
        intensity: 效果强度
        
    Returns:
        处理后图片的字节数据
    """
    # 参数范围限制
    roughness = max(0.1, min(roughness, 1.5))
    cracks = max(0.0, min(cracks, 1.0))
    color_decay = max(0.0, min(color_decay, 0.8))
    
    return process_image(
        image_bytes,
        _fresco_filter,
        intensity=intensity,
        roughness=roughness,
        cracks=cracks,
        color_decay=color_decay
    ) 