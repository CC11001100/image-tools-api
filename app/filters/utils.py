import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io
from typing import Tuple


def pil_to_numpy(img: Image.Image) -> np.ndarray:
    """将PIL图像转换为numpy数组"""
    return np.array(img)


def numpy_to_pil(arr: np.ndarray) -> Image.Image:
    """将numpy数组转换为PIL图像"""
    if arr.dtype != np.uint8:
        # 确保值在0-255范围内
        if arr.max() <= 1.0:
            arr = (arr * 255).astype(np.uint8)
        else:
            arr = np.clip(arr, 0, 255).astype(np.uint8)
    
    return Image.fromarray(arr)


def apply_filter_with_intensity(original: np.ndarray, filtered: np.ndarray, intensity: float) -> np.ndarray:
    """
    根据强度混合原始图像和滤镜效果图像
    
    Args:
        original: 原始图像的numpy数组
        filtered: 应用滤镜后的numpy数组
        intensity: 效果强度 (0.0-2.0)
        
    Returns:
        混合后的numpy数组
    """
    if intensity <= 0:
        return original
    
    if intensity >= 1.0:
        # 强化效果
        enhanced = filtered + (filtered - original) * (intensity - 1.0)
        return np.clip(enhanced, 0, 255).astype(np.uint8)
    else:
        # 减弱效果，与原图混合
        return (original * (1 - intensity) + filtered * intensity).astype(np.uint8)


def process_image(image_bytes: bytes, filter_func, intensity: float = 1.0, **kwargs) -> bytes:
    """
    通用图像处理函数
    
    Args:
        image_bytes: 输入图片的字节数据
        filter_func: 滤镜函数，接受numpy数组和其他参数，返回处理后的numpy数组
        intensity: 效果强度 (0.0-2.0)
        **kwargs: 传递给滤镜函数的其他参数
        
    Returns:
        处理后图片的字节数据
    """
    # 打开图像
    img = Image.open(io.BytesIO(image_bytes))
    
    # 保存原始格式
    img_format = img.format if img.format else "JPEG"
    
    # 转换为numpy数组处理
    img_array = pil_to_numpy(img)
    
    # 保存原始图像数组
    original_array = img_array.copy()
    
    # 应用滤镜
    filtered_array = filter_func(img_array, **kwargs)
    
    # 根据强度混合原始图像和滤镜效果
    if intensity != 1.0:
        result_array = apply_filter_with_intensity(original_array, filtered_array, intensity)
    else:
        result_array = filtered_array
    
    # 转换回PIL图像
    result_img = numpy_to_pil(result_array)
    
    # 保存到内存并返回字节数据
    output = io.BytesIO()
    result_img.save(output, format=img_format, quality=95)
    return output.getvalue()


def get_texture_noise(size: Tuple[int, int], scale: float = 1.0, seed: int = None) -> np.ndarray:
    """
    生成纹理噪声
    
    Args:
        size: (宽度, 高度)的元组
        scale: 噪声尺度
        seed: 随机种子
        
    Returns:
        噪声数组
    """
    if seed is not None:
        np.random.seed(seed)
    
    # 创建噪声
    noise = np.random.normal(0, scale, (*size, 1)) * 255
    noise = np.clip(noise, 0, 255).astype(np.uint8)
    return noise


def add_texture(img: np.ndarray, texture_scale: float = 0.1, seed: int = None) -> np.ndarray:
    """
    向图像添加纹理
    
    Args:
        img: 输入图像的numpy数组
        texture_scale: 纹理强度
        seed: 随机种子
        
    Returns:
        添加纹理后的图像
    """
    height, width = img.shape[:2]
    noise = get_texture_noise((width, height), texture_scale, seed)
    
    # 如果输入是灰度图像
    if len(img.shape) == 2:
        img = img.reshape((*img.shape, 1))
    
    # 确保噪声维度与图像匹配
    if img.shape[2] == 3:
        noise = np.repeat(noise, 3, axis=2)
    
    # 添加纹理
    textured = img + noise
    return np.clip(textured, 0, 255).astype(np.uint8)


def adjust_contrast(img: np.ndarray, factor: float) -> np.ndarray:
    """
    调整图像对比度
    
    Args:
        img: 输入图像的numpy数组
        factor: 对比度因子
        
    Returns:
        调整后的图像
    """
    pil_img = numpy_to_pil(img)
    enhancer = ImageEnhance.Contrast(pil_img)
    enhanced = enhancer.enhance(factor)
    return pil_to_numpy(enhanced) 