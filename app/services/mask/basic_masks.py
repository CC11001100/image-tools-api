"""基础遮罩处理功能"""
from PIL import Image, ImageDraw
import numpy as np
import io
from typing import Tuple, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.logger import logger


class BasicMasks:
    """基础遮罩处理功能"""
    
    @staticmethod
    def apply_mask(
        image_bytes: bytes,
        mask_type: str,
        feather: int = 0,
        invert: bool = False,
        background_color: str = "#FFFFFF",
        opacity: float = 1.0,
        quality: int = 90,
        **kwargs
    ) -> bytes:
        """
        应用遮罩到图片
        
        Args:
            image_bytes: 图片字节数据
            mask_type: 遮罩类型
            feather: 羽化程度
            invert: 是否反转遮罩
            background_color: 背景颜色
            opacity: 透明度
            quality: 输出质量
            **kwargs: 其他参数
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"应用遮罩: 类型={mask_type}, 羽化={feather}, 反转={invert}")
        
        try:
            # 打开图片
            img = Image.open(io.BytesIO(image_bytes))
            width, height = img.size
            
            # 创建遮罩
            if mask_type == "circle":
                mask = BasicMasks._create_circle_mask(width, height, **kwargs)
            elif mask_type == "ellipse":
                mask = BasicMasks._create_ellipse_mask(width, height, **kwargs)
            elif mask_type == "rectangle":
                mask = BasicMasks._create_rectangle_mask(width, height, **kwargs)
            elif mask_type == "rounded_rectangle":
                mask = BasicMasks._create_rounded_rectangle_mask(width, height, **kwargs)
            elif mask_type == "heart":
                mask = BasicMasks._create_heart_mask(width, height, **kwargs)
            elif mask_type == "star":
                mask = BasicMasks._create_star_mask(width, height, **kwargs)
            else:
                raise ValueError(f"不支持的遮罩类型: {mask_type}")
            
            # 应用羽化
            if feather > 0:
                mask = BasicMasks._apply_feather(mask, feather)
            
            # 反转遮罩
            if invert:
                mask = Image.eval(mask, lambda x: 255 - x)
            
            # 应用透明度
            if opacity < 1.0:
                mask = Image.eval(mask, lambda x: int(x * opacity))
            
            # 应用遮罩
            result = BasicMasks._apply_mask_to_image(img, mask, background_color)
            
            # 保存结果
            output = io.BytesIO()
            result.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"应用遮罩失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_layer_mask(
        base_image_bytes: bytes,
        overlay_image_bytes: bytes,
        mask_bytes: bytes,
        blend_mode: str = "normal",
        opacity: float = 1.0,
        quality: int = 90
    ) -> bytes:
        """
        应用图层遮罩
        
        Args:
            base_image_bytes: 底图字节数据
            overlay_image_bytes: 覆盖图字节数据
            mask_bytes: 遮罩图字节数据
            blend_mode: 混合模式
            opacity: 透明度
            quality: 输出质量
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"应用图层遮罩: 混合模式={blend_mode}, 透明度={opacity}")
        
        try:
            # 打开图片
            base_img = Image.open(io.BytesIO(base_image_bytes))
            overlay_img = Image.open(io.BytesIO(overlay_image_bytes))
            mask_img = Image.open(io.BytesIO(mask_bytes))
            
            # 确保所有图片尺寸一致
            base_size = base_img.size
            overlay_img = overlay_img.resize(base_size, Image.Resampling.LANCZOS)
            mask_img = mask_img.resize(base_size, Image.Resampling.LANCZOS)
            
            # 转换为RGBA模式
            if base_img.mode != 'RGBA':
                base_img = base_img.convert('RGBA')
            if overlay_img.mode != 'RGBA':
                overlay_img = overlay_img.convert('RGBA')
            if mask_img.mode != 'L':
                mask_img = mask_img.convert('L')
            
            # 应用透明度到遮罩
            if opacity < 1.0:
                mask_img = Image.eval(mask_img, lambda x: int(x * opacity))
            
            # 使用遮罩合成图像
            result = Image.composite(overlay_img, base_img, mask_img)
            
            # 转换回RGB
            if result.mode == 'RGBA':
                background = Image.new('RGB', result.size, (255, 255, 255))
                background.paste(result, mask=result.split()[-1])
                result = background
            
            # 保存结果
            output = io.BytesIO()
            result.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"应用图层遮罩失败: {str(e)}")
            raise
    
    @staticmethod
    def _create_circle_mask(width: int, height: int, **kwargs) -> Image.Image:
        """创建圆形遮罩"""
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        center_x = kwargs.get('center_x', width // 2)
        center_y = kwargs.get('center_y', height // 2)
        radius = kwargs.get('radius', min(width, height) // 4)
        
        draw.ellipse([
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius
        ], fill=255)
        
        return mask
    
    @staticmethod
    def _create_ellipse_mask(width: int, height: int, **kwargs) -> Image.Image:
        """创建椭圆遮罩"""
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        center_x = kwargs.get('center_x', width // 2)
        center_y = kwargs.get('center_y', height // 2)
        radius_x = kwargs.get('radius_x', width // 4)
        radius_y = kwargs.get('radius_y', height // 4)
        
        draw.ellipse([
            center_x - radius_x, center_y - radius_y,
            center_x + radius_x, center_y + radius_y
        ], fill=255)
        
        return mask
    
    @staticmethod
    def _create_rectangle_mask(width: int, height: int, **kwargs) -> Image.Image:
        """创建矩形遮罩"""
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        x = kwargs.get('x', width // 4)
        y = kwargs.get('y', height // 4)
        w = kwargs.get('width', width // 2)
        h = kwargs.get('height', height // 2)
        
        draw.rectangle([x, y, x + w, y + h], fill=255)
        
        return mask
    
    @staticmethod
    def _create_rounded_rectangle_mask(width: int, height: int, **kwargs) -> Image.Image:
        """创建圆角矩形遮罩"""
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        x = kwargs.get('x', width // 4)
        y = kwargs.get('y', height // 4)
        w = kwargs.get('width', width // 2)
        h = kwargs.get('height', height // 2)
        radius = kwargs.get('corner_radius', 20)
        
        draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=255)
        
        return mask
    
    @staticmethod
    def _create_heart_mask(width: int, height: int, **kwargs) -> Image.Image:
        """创建心形遮罩"""
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        center_x = kwargs.get('center_x', width // 2)
        center_y = kwargs.get('center_y', height // 2)
        size = kwargs.get('size', min(width, height) // 4)
        
        # 简化的心形绘制
        points = []
        for i in range(360):
            t = np.radians(i)
            x = 16 * np.sin(t)**3
            y = -(13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t))
            points.append((center_x + x * size / 16, center_y + y * size / 16))
        
        draw.polygon(points, fill=255)
        
        return mask
    
    @staticmethod
    def _create_star_mask(width: int, height: int, **kwargs) -> Image.Image:
        """创建星形遮罩"""
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        center_x = kwargs.get('center_x', width // 2)
        center_y = kwargs.get('center_y', height // 2)
        outer_radius = kwargs.get('outer_radius', min(width, height) // 4)
        inner_radius = kwargs.get('inner_radius', outer_radius // 2)
        points_count = kwargs.get('points', 5)
        
        points = []
        for i in range(points_count * 2):
            angle = i * np.pi / points_count
            if i % 2 == 0:
                radius = outer_radius
            else:
                radius = inner_radius
            x = center_x + radius * np.cos(angle - np.pi / 2)
            y = center_y + radius * np.sin(angle - np.pi / 2)
            points.append((x, y))
        
        draw.polygon(points, fill=255)
        
        return mask
    
    @staticmethod
    def _apply_feather(mask: Image.Image, feather: int) -> Image.Image:
        """应用羽化效果"""
        from PIL import ImageFilter
        return mask.filter(ImageFilter.GaussianBlur(radius=feather))
    
    @staticmethod
    def _apply_mask_to_image(img: Image.Image, mask: Image.Image, background_color: str) -> Image.Image:
        """将遮罩应用到图片"""
        from .utils import MaskUtils
        
        # 转换背景颜色
        bg_rgb = MaskUtils.hex_to_rgb(background_color)
        
        # 创建背景
        background = Image.new('RGB', img.size, bg_rgb)
        
        # 转换图片为RGBA
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 使用遮罩合成
        result = Image.composite(img, background, mask)
        
        return result
