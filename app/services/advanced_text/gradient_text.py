"""渐变文字功能"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from typing import Tuple
from ...utils.logger import logger
from .base import AdvancedTextBase


class GradientTextService:
    """渐变文字服务"""
    
    @staticmethod
    def add_gradient_text(
        image: Image.Image,
        text: str,
        position: Tuple[int, int],
        font_size: int = 36,
        start_color: Tuple[int, int, int] = (255, 0, 0),
        end_color: Tuple[int, int, int] = (0, 0, 255),
        gradient_direction: str = "horizontal"
    ) -> Image.Image:
        """添加渐变文字
        
        Args:
            image: 输入图片
            text: 文字内容
            position: 文字位置
            font_size: 字体大小
            start_color: 起始颜色
            end_color: 结束颜色
            gradient_direction: 渐变方向 (horizontal, vertical, diagonal)
            
        Returns:
            处理后的图片
        """
        try:
            img = image.copy()
            
            # 加载字体
            font = AdvancedTextBase.load_font("Arial", font_size)
            
            # 创建文字图层
            text_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
            text_draw = ImageDraw.Draw(text_layer)
            
            # 获取文字边界框
            bbox = text_draw.textbbox(position, text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # 创建渐变
            gradient = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))
            gradient_array = np.zeros((text_height, text_width, 4), dtype=np.uint8)
            
            for y in range(text_height):
                for x in range(text_width):
                    if gradient_direction == "horizontal":
                        progress = x / text_width
                    elif gradient_direction == "vertical":
                        progress = y / text_height
                    elif gradient_direction == "diagonal":
                        progress = (x + y) / (text_width + text_height)
                    else:
                        progress = 0
                    
                    # 计算渐变颜色
                    r = int(start_color[0] + (end_color[0] - start_color[0]) * progress)
                    g = int(start_color[1] + (end_color[1] - start_color[1]) * progress)
                    b = int(start_color[2] + (end_color[2] - start_color[2]) * progress)
                    gradient_array[y, x] = [r, g, b, 255]
            
            gradient = Image.fromarray(gradient_array)
            
            # 创建文字蒙版
            mask = Image.new('L', (text_width, text_height), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.text((0, 0), text, fill=255, font=font)
            
            # 应用渐变到文字
            gradient.putalpha(mask)
            text_layer.paste(gradient, position, gradient)
            
            # 合并图层
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            result = Image.alpha_composite(img, text_layer)
            
            # 转回原始模式
            if image.mode != 'RGBA':
                result = result.convert(image.mode)
            
            logger.info(f"渐变文字添加成功: 方向={gradient_direction}")
            return result
            
        except Exception as e:
            logger.error(f"添加渐变文字失败: {str(e)}")
            raise 