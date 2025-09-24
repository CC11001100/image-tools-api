"""
文字服务模块 - 向后兼容实现
"""

from typing import Optional, Tuple, List, Dict, Any
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os


class TextService:
    """文字处理服务"""
    
    def __init__(self):
        self.default_font_size = 24
        self.default_color = (0, 0, 0, 255)  # 黑色
        
    def add_text_to_image(
        self,
        image: Image.Image,
        text: str,
        position: Tuple[int, int] = (10, 10),
        font_size: int = 24,
        color: Tuple[int, int, int, int] = (0, 0, 0, 255),
        font_path: Optional[str] = None,
        **kwargs
    ) -> Image.Image:
        """
        在图片上添加文字
        
        Args:
            image: PIL图像对象
            text: 要添加的文字
            position: 文字位置 (x, y)
            font_size: 字体大小
            color: 文字颜色 RGBA
            font_path: 字体文件路径
            **kwargs: 其他参数
            
        Returns:
            处理后的图像
        """
        try:
            # 创建图像副本
            result_image = image.copy()
            draw = ImageDraw.Draw(result_image)
            
            # 加载字体
            try:
                if font_path and os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    # 使用默认字体
                    font = ImageFont.load_default()
            except Exception:
                font = ImageFont.load_default()
            
            # 绘制文字
            draw.text(position, text, fill=color, font=font)
            
            return result_image
            
        except Exception as e:
            print(f"添加文字时出错: {e}")
            return image
    
    def get_text_size(
        self,
        text: str,
        font_size: int = 24,
        font_path: Optional[str] = None
    ) -> Tuple[int, int]:
        """
        获取文字尺寸
        
        Args:
            text: 文字内容
            font_size: 字体大小
            font_path: 字体文件路径
            
        Returns:
            文字尺寸 (width, height)
        """
        try:
            # 加载字体
            try:
                if font_path and os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    font = ImageFont.load_default()
            except Exception:
                font = ImageFont.load_default()
            
            # 获取文字边界框
            bbox = font.getbbox(text)
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            
            return (width, height)
            
        except Exception as e:
            print(f"获取文字尺寸时出错: {e}")
            return (100, 20)  # 返回默认尺寸


# 创建全局实例
text_service = TextService()

# 导出函数
def add_text_to_image(*args, **kwargs):
    """添加文字到图片"""
    return text_service.add_text_to_image(*args, **kwargs)

def get_text_size(*args, **kwargs):
    """获取文字尺寸"""
    return text_service.get_text_size(*args, **kwargs)
