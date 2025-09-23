"""形状遮罩处理功能"""
from PIL import Image, ImageDraw
import numpy as np
from typing import Tuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.logger import logger
from .utils import MaskUtils


class ShapeMasks:
    """形状遮罩处理功能"""
    
    @staticmethod
    def create_shape_mask(
        size: Tuple[int, int],
        shape: str = "rectangle",
        params: dict = None
    ) -> Image.Image:
        """
        创建形状蒙版
        
        Args:
            size: 蒙版大小
            shape: 形状类型
            params: 形状参数
            
        Returns:
            蒙版图片
        """
        logger.info(f"创建形状蒙版: 形状={shape}, 尺寸={size}")
        
        try:
            if params is None:
                params = {}
                
            width, height = size
            mask = Image.new("L", (width, height), 0)
            draw = ImageDraw.Draw(mask)
            
            if shape == "rectangle":
                x1 = params.get("x1", width // 4)
                y1 = params.get("y1", height // 4)
                x2 = params.get("x2", width * 3 // 4)
                y2 = params.get("y2", height * 3 // 4)
                draw.rectangle([x1, y1, x2, y2], fill=255)
                
            elif shape == "star":
                # 五角星
                center_x, center_y = width // 2, height // 2
                outer_radius = min(width, height) // 3
                inner_radius = outer_radius // 2
                
                points = []
                for i in range(10):
                    angle = i * np.pi / 5 - np.pi / 2
                    radius = outer_radius if i % 2 == 0 else inner_radius
                    x = center_x + radius * np.cos(angle)
                    y = center_y + radius * np.sin(angle)
                    points.append((x, y))
                
                draw.polygon(points, fill=255)
                
            elif shape == "heart":
                # 心形
                center_x, center_y = width // 2, height // 2
                scale = min(width, height) // 4
                
                points = []
                for t in np.linspace(0, 2 * np.pi, 100):
                    x = 16 * (np.sin(t) ** 3)
                    y = -(13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t))
                    points.append((center_x + x * scale // 16, center_y + y * scale // 16))
                
                draw.polygon(points, fill=255)
            
            logger.info(f"形状蒙版创建成功: 形状={shape}")
            return mask
            
        except Exception as e:
            logger.error(f"形状蒙版创建失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_shape_mask(
        image: Image.Image,
        mask_type: str = "circle",
        feather: int = 0,
        invert: bool = False,
        background_color: str = "#FFFFFF",
        opacity: float = 1.0
    ) -> Image.Image:
        """
        应用形状遮罩
        
        Args:
            image: 输入图片
            mask_type: 遮罩类型 (circle, rectangle, ellipse, rounded_rectangle, heart, star)
            feather: 羽化程度
            invert: 是否反转遮罩
            background_color: 背景颜色
            opacity: 遮罩不透明度
            
        Returns:
            处理后的图片
        """
        logger.info(f"应用形状遮罩: 类型={mask_type}, 羽化={feather}, 反转={invert}")
        
        try:
            # 转换为RGBA
            img = image.convert("RGBA")
            width, height = img.size
            
            # 创建遮罩
            mask = Image.new("L", (width, height), 0)
            draw = ImageDraw.Draw(mask)
            
            # 根据类型绘制不同形状
            if mask_type == "circle":
                # 圆形遮罩
                size = min(width, height)
                x = (width - size) // 2
                y = (height - size) // 2
                draw.ellipse([x, y, x + size, y + size], fill=255)
                
            elif mask_type == "rectangle":
                # 矩形遮罩
                padding = min(width, height) // 10
                draw.rectangle([padding, padding, width - padding, height - padding], fill=255)
                
            elif mask_type == "ellipse":
                # 椭圆形遮罩
                padding = min(width, height) // 20
                draw.ellipse([padding, padding, width - padding, height - padding], fill=255)
                
            elif mask_type == "rounded_rectangle":
                # 圆角矩形遮罩
                padding = min(width, height) // 10
                radius = min(width, height) // 8
                draw.rounded_rectangle(
                    [padding, padding, width - padding, height - padding],
                    radius=radius,
                    fill=255
                )
                
            elif mask_type == "heart":
                # 心形遮罩
                center_x, center_y = width // 2, height // 2
                scale = min(width, height) // 6
                
                points = []
                for t in np.linspace(0, 2 * np.pi, 100):
                    x = 16 * (np.sin(t) ** 3)
                    y = -(13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t))
                    points.append((center_x + x * scale // 16, center_y + y * scale // 16))
                
                draw.polygon(points, fill=255)
                
            elif mask_type == "star":
                # 五角星遮罩
                center_x, center_y = width // 2, height // 2
                outer_radius = min(width, height) // 4
                inner_radius = outer_radius // 2
                
                points = []
                for i in range(10):
                    angle = i * np.pi / 5 - np.pi / 2
                    radius = outer_radius if i % 2 == 0 else inner_radius
                    x = center_x + radius * np.cos(angle)
                    y = center_y + radius * np.sin(angle)
                    points.append((x, y))
                
                draw.polygon(points, fill=255)
            
            # 应用羽化效果
            if feather > 0:
                from PIL import ImageFilter
                mask = mask.filter(ImageFilter.GaussianBlur(radius=feather))
            
            # 反转遮罩
            if invert:
                mask = Image.eval(mask, lambda x: 255 - x)
            
            # 调整不透明度
            if opacity < 1.0:
                mask = Image.eval(mask, lambda x: int(x * opacity))
            
            # 解析背景颜色
            bg_color = MaskUtils.hex_to_rgb(background_color)
            
            # 创建带背景的结果图片
            result = Image.new("RGBA", (width, height), (*bg_color, 255))
            
            # 将原图片应用遮罩后合成到结果上
            img.putalpha(mask)
            result = Image.alpha_composite(result, img)
            
            logger.info(f"形状遮罩应用成功: 类型={mask_type}, 羽化={feather}, 反转={invert}")
            return result
            
        except Exception as e:
            logger.error(f"形状遮罩应用失败: {str(e)}")
            raise
