import cv2
import numpy as np
from .utils import process_image, add_texture, adjust_contrast


def _acrylic_painting_filter(img: np.ndarray, brush_size: int = 7, texture_strength: float = 0.3) -> np.ndarray:
    """丙烯画效果"""
    # 丙烯画特点：鲜艳的颜色，清晰的边缘，厚重的质感
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # 双边滤波保持边缘清晰
    bilateral = cv2.bilateralFilter(img_bgr, 15, 80, 80)
    
    # 增强饱和度
    hsv = cv2.cvtColor(bilateral, cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.3, 0, 255)
    enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    # 添加笔触纹理
    result = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)
    result = add_texture(result, texture_strength)
    
    return result


def _tempera_filter(img: np.ndarray, opacity: float = 0.8) -> np.ndarray:
    """蛋彩画效果"""
    # 蛋彩画特点：半透明，细腻的笔触
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # 轻微模糊
    blurred = cv2.GaussianBlur(img_bgr, (3, 3), 0)
    
    # 降低饱和度，增加透明感
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * opacity, 0, 255)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.1, 0, 255)
    
    result = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    return result


def _gouache_filter(img: np.ndarray, matte_factor: float = 0.7) -> np.ndarray:
    """水粉画效果"""
    # 水粉画特点：不透明，柔和的色彩
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # 中值滤波产生平坦色块
    median = cv2.medianBlur(img_bgr, 5)
    
    # 降低对比度，产生哑光效果
    matte = median * matte_factor + 128 * (1 - matte_factor)
    matte = np.clip(matte, 0, 255).astype(np.uint8)
    
    result = cv2.cvtColor(matte, cv2.COLOR_BGR2RGB)
    return result


def _impasto_filter(img: np.ndarray, thickness: float = 1.5) -> np.ndarray:
    """厚涂画效果"""
    # 厚涂特点：厚重的颜料层，立体感强
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # 强化边缘
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    
    # 厚化边缘
    kernel = np.ones((3, 3), np.uint8)
    thick_edges = cv2.dilate(edges, kernel, iterations=int(thickness))
    
    # 应用厚涂效果
    edges_bgr = cv2.cvtColor(thick_edges, cv2.COLOR_GRAY2BGR)
    result = cv2.addWeighted(img_bgr, 0.8, edges_bgr, 0.2, 0)
    
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    return result


def _glazing_filter(img: np.ndarray, transparency: float = 0.3) -> np.ndarray:
    """透明画法效果"""
    # 透明画法特点：层层叠叠的透明色彩
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # 创建多个色彩层
    layer1 = cv2.GaussianBlur(img_bgr, (5, 5), 0)
    layer2 = cv2.GaussianBlur(img_bgr, (9, 9), 0)
    
    # 混合图层
    blended = cv2.addWeighted(layer1, 0.6, layer2, 0.4, 0)
    
    # 添加透明效果
    result = cv2.addWeighted(img_bgr, 1 - transparency, blended, transparency, 0)
    
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    return result


def _scumbling_filter(img: np.ndarray, roughness: float = 0.5) -> np.ndarray:
    """干擦画法效果"""
    # 干擦画法特点：不完全覆盖，产生纹理效果
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # 创建随机遮罩
    h, w = img_bgr.shape[:2]
    mask = np.random.random((h, w)) > roughness
    
    # 应用干擦效果
    scumbled = img_bgr.copy()
    for i in range(3):
        channel = scumbled[:, :, i]
        channel[mask] = np.clip(channel[mask] * 0.7 + 50, 0, 255)
        scumbled[:, :, i] = channel
    
    result = cv2.cvtColor(scumbled, cv2.COLOR_BGR2RGB)
    return result


def _underpainting_filter(img: np.ndarray, base_tone: str = "warm") -> np.ndarray:
    """底色画法效果"""
    # 底色画法特点：统一的底色调
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # 创建底色
    if base_tone == "warm":
        base = np.full_like(img_bgr, [40, 60, 120])  # 橙色调
    elif base_tone == "cool":
        base = np.full_like(img_bgr, [120, 80, 40])  # 蓝色调
    else:  # neutral
        base = np.full_like(img_bgr, [80, 80, 80])   # 灰色调
    
    # 混合底色和原图
    result = cv2.addWeighted(base, 0.3, img_bgr, 0.7, 0)
    
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    return result


# 导出函数
def apply_acrylic_painting(image_bytes: bytes, brush_size: int = 7, texture_strength: float = 0.3, intensity: float = 1.0) -> bytes:
    """应用丙烯画效果"""
    return process_image(image_bytes, _acrylic_painting_filter, intensity=intensity, 
                        brush_size=brush_size, texture_strength=texture_strength)


def apply_tempera(image_bytes: bytes, opacity: float = 0.8, intensity: float = 1.0) -> bytes:
    """应用蛋彩画效果"""
    return process_image(image_bytes, _tempera_filter, intensity=intensity, opacity=opacity)


def apply_gouache(image_bytes: bytes, matte_factor: float = 0.7, intensity: float = 1.0) -> bytes:
    """应用水粉画效果"""
    return process_image(image_bytes, _gouache_filter, intensity=intensity, matte_factor=matte_factor)


def apply_impasto(image_bytes: bytes, thickness: float = 1.5, intensity: float = 1.0) -> bytes:
    """应用厚涂画效果"""
    return process_image(image_bytes, _impasto_filter, intensity=intensity, thickness=thickness)


def apply_glazing(image_bytes: bytes, transparency: float = 0.3, intensity: float = 1.0) -> bytes:
    """应用透明画法效果"""
    return process_image(image_bytes, _glazing_filter, intensity=intensity, transparency=transparency)


def apply_scumbling(image_bytes: bytes, roughness: float = 0.5, intensity: float = 1.0) -> bytes:
    """应用干擦画法效果"""
    return process_image(image_bytes, _scumbling_filter, intensity=intensity, roughness=roughness)


def apply_underpainting(image_bytes: bytes, base_tone: str = "warm", intensity: float = 1.0) -> bytes:
    """应用底色画法效果"""
    return process_image(image_bytes, _underpainting_filter, intensity=intensity, base_tone=base_tone) 