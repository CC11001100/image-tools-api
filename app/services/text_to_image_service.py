from PIL import Image, ImageDraw, ImageFont
import os
import uuid
from typing import Optional
import textwrap
import math
from ..utils.logger import logger

class TextToImageService:
    def __init__(self):
        self.output_dir = "public/generated"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def hex_to_rgb(self, hex_color: str) -> tuple:
        """将十六进制颜色转换为RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_gradient_background(self, width: int, height: int, start_color: str, 
                                 end_color: str, direction: str) -> Image.Image:
        """创建渐变背景"""
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)
        
        start_rgb = self.hex_to_rgb(start_color)
        end_rgb = self.hex_to_rgb(end_color)
        
        if direction == "horizontal":
            for x in range(width):
                ratio = x / width
                r = int(start_rgb[0] * (1 - ratio) + end_rgb[0] * ratio)
                g = int(start_rgb[1] * (1 - ratio) + end_rgb[1] * ratio)
                b = int(start_rgb[2] * (1 - ratio) + end_rgb[2] * ratio)
                draw.line([(x, 0), (x, height)], fill=(r, g, b))
        elif direction == "vertical":
            for y in range(height):
                ratio = y / height
                r = int(start_rgb[0] * (1 - ratio) + end_rgb[0] * ratio)
                g = int(start_rgb[1] * (1 - ratio) + end_rgb[1] * ratio)
                b = int(start_rgb[2] * (1 - ratio) + end_rgb[2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
        elif direction == "diagonal":
            for x in range(width):
                for y in range(height):
                    ratio = (x + y) / (width + height)
                    r = int(start_rgb[0] * (1 - ratio) + end_rgb[0] * ratio)
                    g = int(start_rgb[1] * (1 - ratio) + end_rgb[1] * ratio)
                    b = int(start_rgb[2] * (1 - ratio) + end_rgb[2] * ratio)
                    image.putpixel((x, y), (r, g, b))
        
        return image
    
    def get_font(self, font_family: str, font_size: int) -> ImageFont.ImageFont:
        """获取字体对象"""
        try:
            # 尝试使用系统字体
            if font_family == "Arial":
                return ImageFont.truetype("arial.ttf", font_size)
            elif font_family == "Times New Roman":
                return ImageFont.truetype("times.ttf", font_size)
            elif font_family == "Helvetica":
                return ImageFont.truetype("helvetica.ttf", font_size)
            else:
                # 如果找不到指定字体，使用默认字体
                return ImageFont.load_default()
        except:
            # 如果无法加载字体，使用默认字体
            return ImageFont.load_default()
    
    def wrap_text(self, text: str, font: ImageFont.ImageFont, max_width: int) -> list:
        """文字换行处理"""
        lines = []
        words = text.split()
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            bbox = font.getbbox(test_line)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    async def create_text_image(self, text: str, width: int = 800, height: int = 600,
                              font_size: int = 48, font_family: str = "Arial",
                              font_color: str = "#000000", background_color: str = "#FFFFFF",
                              background_style: str = "solid", text_align: str = "center",
                              vertical_align: str = "middle", padding: int = 50,
                              line_spacing: float = 1.2, shadow: bool = False,
                              shadow_color: str = "#808080", shadow_offset_x: int = 2,
                              shadow_offset_y: int = 2, border: bool = False,
                              border_color: str = "#000000", border_width: int = 2,
                              gradient_start: str = "#FF6B6B", gradient_end: str = "#4ECDC4",
                              gradient_direction: str = "horizontal") -> str:
        """生成文字图片"""
        
        # 创建背景
        if background_style == "gradient":
            image = self.create_gradient_background(width, height, gradient_start, gradient_end, gradient_direction)
        else:
            bg_color = self.hex_to_rgb(background_color)
            image = Image.new('RGB', (width, height), bg_color)
        
        draw = ImageDraw.Draw(image)
        
        # 添加边框
        if border:
            border_rgb = self.hex_to_rgb(border_color)
            for i in range(border_width):
                draw.rectangle([i, i, width-1-i, height-1-i], outline=border_rgb)
        
        # 获取字体
        font = self.get_font(font_family, font_size)
        
        # 文字换行
        max_text_width = width - 2 * padding
        lines = self.wrap_text(text, font, max_text_width)
        
        # 计算文字总高度
        line_height = int(font_size * line_spacing)
        total_text_height = len(lines) * line_height
        
        # 计算起始Y位置
        if vertical_align == "top":
            start_y = padding
        elif vertical_align == "bottom":
            start_y = height - padding - total_text_height
        else:  # middle
            start_y = (height - total_text_height) // 2
        
        # 绘制文字
        font_rgb = self.hex_to_rgb(font_color)
        shadow_rgb = self.hex_to_rgb(shadow_color) if shadow else None
        
        for i, line in enumerate(lines):
            # 计算当前行的位置
            y = start_y + i * line_height
            
            # 计算X位置
            bbox = font.getbbox(line)
            text_width = bbox[2] - bbox[0]
            
            if text_align == "left":
                x = padding
            elif text_align == "right":
                x = width - padding - text_width
            else:  # center
                x = (width - text_width) // 2
            
            # 绘制阴影
            if shadow:
                draw.text((x + shadow_offset_x, y + shadow_offset_y), line, 
                         font=font, fill=shadow_rgb)
            
            # 绘制文字
            draw.text((x, y), line, font=font, fill=font_rgb)
        
        # 保存图片
        filename = f"text_image_{uuid.uuid4().hex}.png"
        filepath = os.path.join(self.output_dir, filename)
        image.save(filepath, "PNG")
        
        # 返回URL
        image_url = f"/generated/{filename}"
        logger.info(f"文字图片已生成: {image_url}")
        
        return image_url 