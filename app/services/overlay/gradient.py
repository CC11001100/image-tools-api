"""渐变和特效叠加功能"""
from PIL import Image, ImageDraw, ImageFilter
from typing import Tuple
from ...utils.logger import logger
from .base import OverlayBase


class GradientEffectService:
    """渐变和特效叠加服务"""
    
    @staticmethod
    def add_gradient_overlay(
        image: Image.Image,
        gradient_type: str = "linear",
        gradient_direction: str = "to_bottom",
        start_color: str = "#000000",
        end_color: str = "#FFFFFF",
        start_opacity: float = 0.0,
        end_opacity: float = 0.8
    ) -> Image.Image:
        """添加渐变叠加效果
        
        Args:
            image: 输入图片
            gradient_type: 渐变类型 (linear, radial)
            gradient_direction: 线性渐变方向
            start_color: 起始颜色
            end_color: 结束颜色
            start_opacity: 起始透明度
            end_opacity: 结束透明度
            
        Returns:
            处理后的图片
        """
        try:
            # 转换为RGBA模式
            base = image.convert("RGBA")
            width, height = base.size
            
            # 创建渐变图层
            gradient = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            
            # 解析颜色
            start_rgb = OverlayBase.hex_to_rgb(start_color)
            end_rgb = OverlayBase.hex_to_rgb(end_color)
            
            if gradient_type == "linear":
                gradient = GradientEffectService._create_linear_gradient(
                    width, height, gradient_direction, 
                    start_rgb, end_rgb, start_opacity, end_opacity
                )
            elif gradient_type == "radial":
                gradient = GradientEffectService._create_radial_gradient(
                    width, height, start_rgb, end_rgb, start_opacity, end_opacity
                )
            
            # 合并图层
            result = Image.alpha_composite(base, gradient)
            
            # 转回原始模式
            if image.mode != "RGBA":
                result = result.convert(image.mode)
            
            logger.info(f"渐变叠加成功: 类型={gradient_type}, 方向={gradient_direction}")
            return result
            
        except Exception as e:
            logger.error(f"渐变叠加失败: {str(e)}")
            raise
    
    @staticmethod
    def add_vignette_effect(
        image: Image.Image,
        intensity: float = 0.6,
        radius: float = 1.0
    ) -> Image.Image:
        """添加暗角效果
        
        Args:
            image: 输入图片
            intensity: 暗角强度
            radius: 暗角半径
            
        Returns:
            处理后的图片
        """
        try:
            # 转换为RGBA模式
            base = image.convert("RGBA")
            width, height = base.size
            
            # 创建暗角遮罩
            mask = Image.new("L", (width, height), 255)
            draw = ImageDraw.Draw(mask)
            
            # 计算中心点和半径
            center_x, center_y = width // 2, height // 2
            max_radius = min(width, height) * radius / 2
            
            # 创建径向渐变遮罩
            for y in range(height):
                for x in range(width):
                    # 计算到中心的距离
                    distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                    
                    # 计算透明度
                    if distance < max_radius:
                        alpha = 255
                    else:
                        fade = min(1.0, (distance - max_radius) / (max_radius * 0.5))
                        alpha = int(255 * (1 - fade * intensity))
                    
                    mask.putpixel((x, y), alpha)
            
            # 应用高斯模糊使边缘更平滑
            mask = mask.filter(ImageFilter.GaussianBlur(radius=max_radius * 0.1))
            
            # 创建暗角图层
            vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            vignette.putalpha(mask)
            
            # 合并图层
            result = Image.alpha_composite(base, vignette)
            
            # 转回原始模式
            if image.mode != "RGBA":
                result = result.convert(image.mode)
            
            logger.info(f"暗角效果添加成功: 强度={intensity}, 半径={radius}")
            return result
            
        except Exception as e:
            logger.error(f"暗角效果添加失败: {str(e)}")
            raise
    
    @staticmethod
    def _create_linear_gradient(
        width: int, height: int, direction: str,
        start_color: Tuple[int, int, int], end_color: Tuple[int, int, int],
        start_opacity: float, end_opacity: float
    ) -> Image.Image:
        """创建线性渐变"""
        gradient = Image.new("RGBA", (width, height))
        
        # 根据方向确定渐变参数
        if direction == "to_bottom":
            for y in range(height):
                ratio = y / height
                color = OverlayBase.interpolate_color(start_color, end_color, ratio)
                opacity = int((start_opacity + (end_opacity - start_opacity) * ratio) * 255)
                for x in range(width):
                    gradient.putpixel((x, y), (*color, opacity))
        elif direction == "to_top":
            for y in range(height):
                ratio = 1 - (y / height)
                color = OverlayBase.interpolate_color(start_color, end_color, ratio)
                opacity = int((start_opacity + (end_opacity - start_opacity) * ratio) * 255)
                for x in range(width):
                    gradient.putpixel((x, y), (*color, opacity))
        elif direction == "to_right":
            for x in range(width):
                ratio = x / width
                color = OverlayBase.interpolate_color(start_color, end_color, ratio)
                opacity = int((start_opacity + (end_opacity - start_opacity) * ratio) * 255)
                for y in range(height):
                    gradient.putpixel((x, y), (*color, opacity))
        elif direction == "to_left":
            for x in range(width):
                ratio = 1 - (x / width)
                color = OverlayBase.interpolate_color(start_color, end_color, ratio)
                opacity = int((start_opacity + (end_opacity - start_opacity) * ratio) * 255)
                for y in range(height):
                    gradient.putpixel((x, y), (*color, opacity))
        
        return gradient
    
    @staticmethod
    def _create_radial_gradient(
        width: int, height: int,
        start_color: Tuple[int, int, int], end_color: Tuple[int, int, int],
        start_opacity: float, end_opacity: float
    ) -> Image.Image:
        """创建径向渐变"""
        gradient = Image.new("RGBA", (width, height))
        center_x, center_y = width // 2, height // 2
        max_radius = min(width, height) // 2
        
        for y in range(height):
            for x in range(width):
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                ratio = min(1.0, distance / max_radius)
                color = OverlayBase.interpolate_color(start_color, end_color, ratio)
                opacity = int((start_opacity + (end_opacity - start_opacity) * ratio) * 255)
                gradient.putpixel((x, y), (*color, opacity))
        
        return gradient 