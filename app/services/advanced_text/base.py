"""高级文字服务基础工具类"""
from PIL import ImageFont
from typing import Tuple, Optional
from ...utils.logger import logger


class AdvancedTextBase:
    """高级文字服务基础工具类"""
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """将十六进制颜色转换为RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def load_font(font_family: str, font_size: int) -> ImageFont.FreeTypeFont:
        """加载字体
        
        Args:
            font_family: 字体系列
            font_size: 字体大小
            
        Returns:
            字体对象
        """
        # 尝试常见的字体路径
        font_paths = {
            "Arial": ["arial.ttf", "/System/Library/Fonts/Arial.ttf"],
            "Helvetica": ["helvetica.ttf", "/System/Library/Fonts/Helvetica.ttf"],
            "Times New Roman": ["times.ttf", "/System/Library/Fonts/Times.ttf"],
            "Courier New": ["cour.ttf", "/System/Library/Fonts/Courier.ttf"],
            "Georgia": ["georgia.ttf", "/System/Library/Fonts/Georgia.ttf"],
            "Verdana": ["verdana.ttf", "/System/Library/Fonts/Verdana.ttf"],
            "Impact": ["impact.ttf", "/System/Library/Fonts/Impact.ttf"],
            "Comic Sans MS": ["comic.ttf", "/System/Library/Fonts/Comic Sans MS.ttf"]
        }
        
        font = None
        if font_family in font_paths:
            for path in font_paths[font_family]:
                try:
                    font = ImageFont.truetype(path, font_size)
                    break
                except:
                    continue
        
        # 如果找不到指定字体，尝试默认字体
        if font is None:
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
                logger.warning(f"无法加载字体 {font_family}，使用默认字体")
        
        return font
    
    @staticmethod
    def calculate_text_position(
        position: str,
        text_width: int,
        text_height: int,
        image_width: int,
        image_height: int,
        padding: int = 20
    ) -> Tuple[int, int]:
        """计算文字位置
        
        Args:
            position: 位置参数
            text_width: 文字宽度
            text_height: 文字高度
            image_width: 图片宽度
            image_height: 图片高度
            padding: 边距
            
        Returns:
            (x, y) 坐标
        """
        positions = {
            "center": (
                (image_width - text_width) // 2,
                (image_height - text_height) // 2
            ),
            "top-left": (padding, padding),
            "top-center": (
                (image_width - text_width) // 2,
                padding
            ),
            "top-right": (
                image_width - text_width - padding,
                padding
            ),
            "middle-left": (
                padding,
                (image_height - text_height) // 2
            ),
            "middle-right": (
                image_width - text_width - padding,
                (image_height - text_height) // 2
            ),
            "bottom-left": (
                padding,
                image_height - text_height - padding
            ),
            "bottom-center": (
                (image_width - text_width) // 2,
                image_height - text_height - padding
            ),
            "bottom-right": (
                image_width - text_width - padding,
                image_height - text_height - padding
            )
        }
        
        return positions.get(position, positions["center"]) 