import cv2
import numpy as np
from PIL import Image, ImageFilter
from .utils import process_image


def _emboss_filter(img: np.ndarray, strength: float = 1.0, angle: float = 45.0) -> np.ndarray:
    """
    实现浮雕效果滤镜
    
    Args:
        img: 输入图像的numpy数组
        strength: 浮雕强度
        angle: 光照角度
        
    Returns:
        处理后的图像数组
    """
    # 转换为灰度图
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img
    
    # 根据角度创建浮雕核
    angle_rad = np.deg2rad(angle)
    kernel = np.array([
        [-2 * np.cos(angle_rad), -np.cos(angle_rad), 0],
        [-np.sin(angle_rad), 0, np.sin(angle_rad)],
        [0, np.cos(angle_rad), 2 * np.cos(angle_rad)]
    ])
    
    # 应用浮雕效果
    embossed = cv2.filter2D(gray, -1, kernel)
    
    # 增加中性灰度偏移
    embossed = embossed + 128
    embossed = np.clip(embossed, 0, 255)
    
    # 调整强度
    if strength != 1.0:
        embossed = gray * (1 - strength) + embossed * strength
        embossed = np.clip(embossed, 0, 255)
    
    # 转换回RGB
    if len(img.shape) == 3:
        result = cv2.cvtColor(embossed.astype(np.uint8), cv2.COLOR_GRAY2RGB)
    else:
        result = embossed.astype(np.uint8)
    
    return result


def _neon_glow_filter(img: np.ndarray, glow_radius: int = 5, intensity: float = 1.5) -> np.ndarray:
    """
    实现霓虹灯光效果滤镜
    
    Args:
        img: 输入图像的numpy数组
        glow_radius: 发光半径
        intensity: 发光强度
        
    Returns:
        处理后的图像数组
    """
    # 边缘检测
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img
    
    # 使用Canny边缘检测
    edges = cv2.Canny(gray, 50, 150)
    
    # 膨胀边缘
    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    # 高斯模糊创建发光效果
    glow = cv2.GaussianBlur(edges.astype(np.float32), (0, 0), glow_radius)
    
    # 创建彩色发光效果
    if len(img.shape) == 3:
        # 基于原图颜色创建发光
        result = img.astype(np.float32)
        
        # 提取边缘处的颜色
        edge_mask = edges > 0
        for i in range(3):
            channel = result[:, :, i]
            edge_colors = channel[edge_mask]
            if len(edge_colors) > 0:
                avg_color = np.mean(edge_colors)
            else:
                avg_color = 128
            
            # 应用发光效果
            glow_colored = glow * (avg_color / 255.0)
            result[:, :, i] = np.clip(result[:, :, i] + glow_colored * intensity, 0, 255)
    else:
        # 灰度图像
        result = gray.astype(np.float32) + glow * intensity
        result = np.clip(result, 0, 255)
    
    return result.astype(np.uint8)


def _glass_effect_filter(img: np.ndarray, displacement: int = 10) -> np.ndarray:
    """
    实现玻璃效果滤镜
    
    Args:
        img: 输入图像的numpy数组
        displacement: 位移量
        
    Returns:
        处理后的图像数组
    """
    h, w = img.shape[:2]
    
    # 创建随机位移图
    dx = np.random.randint(-displacement, displacement, (h, w))
    dy = np.random.randint(-displacement, displacement, (h, w))
    
    # 创建坐标网格
    x, y = np.meshgrid(np.arange(w), np.arange(h))
    
    # 应用位移
    x_new = np.clip(x + dx, 0, w - 1)
    y_new = np.clip(y + dy, 0, h - 1)
    
    # 重映射图像
    if len(img.shape) == 3:
        result = img[y_new, x_new]
    else:
        result = img[y_new, x_new]
    
    # 轻微模糊以平滑效果
    result = cv2.GaussianBlur(result, (3, 3), 0)
    
    return result


def _metallic_filter(img: np.ndarray, metal_type: str = "silver") -> np.ndarray:
    """
    实现金属质感滤镜
    
    Args:
        img: 输入图像的numpy数组
        metal_type: 金属类型 ("silver", "gold", "copper", "bronze")
        
    Returns:
        处理后的图像数组
    """
    # 转换为灰度图
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img
    
    # 增强对比度
    gray = cv2.equalizeHist(gray)
    
    # 创建金属光泽
    # 使用双边滤波保持边缘
    metallic = cv2.bilateralFilter(gray, 9, 75, 75)
    
    # 添加高光
    _, highlights = cv2.threshold(metallic, 200, 255, cv2.THRESH_BINARY)
    metallic = cv2.addWeighted(metallic, 0.8, highlights, 0.2, 0)
    
    # 根据金属类型着色
    if len(img.shape) == 3:
        result = np.zeros_like(img)
        
        if metal_type == "gold":
            # 金色
            result[:, :, 0] = metallic * 0.7  # R
            result[:, :, 1] = metallic * 0.6  # G
            result[:, :, 2] = metallic * 0.3  # B
        elif metal_type == "copper":
            # 铜色
            result[:, :, 0] = metallic * 0.8  # R
            result[:, :, 1] = metallic * 0.5  # G
            result[:, :, 2] = metallic * 0.3  # B
        elif metal_type == "bronze":
            # 青铜色
            result[:, :, 0] = metallic * 0.6  # R
            result[:, :, 1] = metallic * 0.5  # G
            result[:, :, 2] = metallic * 0.3  # B
        else:  # silver
            # 银色
            result[:, :, 0] = metallic * 0.9  # R
            result[:, :, 1] = metallic * 0.9  # G
            result[:, :, 2] = metallic * 0.95  # B
    else:
        result = metallic
    
    return result.astype(np.uint8)


# 导出的应用函数
def apply_emboss(image_bytes: bytes, strength: float = 1.0, angle: float = 45.0) -> bytes:
    """应用浮雕效果"""
    return process_image(image_bytes, _emboss_filter, strength=strength, angle=angle)


def apply_neon_glow(image_bytes: bytes, glow_radius: int = 5, intensity: float = 1.5) -> bytes:
    """应用霓虹灯光效果"""
    return process_image(image_bytes, _neon_glow_filter, glow_radius=glow_radius, intensity=intensity)


def apply_glass_effect(image_bytes: bytes, displacement: int = 10) -> bytes:
    """应用玻璃效果"""
    return process_image(image_bytes, _glass_effect_filter, displacement=displacement)


def apply_metallic(image_bytes: bytes, metal_type: str = "silver") -> bytes:
    """应用金属质感效果"""
    return process_image(image_bytes, _metallic_filter, metal_type=metal_type) 