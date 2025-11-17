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
    
    @staticmethod
    def add_text(
        image_bytes: bytes,
        text: str,
        position: str = "center",
        font_size: int = 32,
        font_color: str = "#000000",
        background_color: Optional[str] = None,
        quality: int = 90
    ) -> bytes:
        """
        为图片添加文字（静态方法）
        
        Args:
            image_bytes: 输入图片的字节数据
            text: 要添加的文字
            position: 文字位置
            font_size: 字体大小
            font_color: 字体颜色（十六进制）
            background_color: 背景颜色（十六进制，可选）
            quality: 输出质量
            
        Returns:
            处理后图片的字节数据
        """
        try:
            # 打开图片
            img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
            
            # 创建绘图对象
            draw = ImageDraw.Draw(img)
            
            # 加载字体
            try:
                # 尝试加载系统字体
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
            except Exception:
                try:
                    # 尝试其他常见字体路径
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
                except Exception:
                    # 使用默认字体
                    font = ImageFont.load_default()
            
            # 解析颜色
            def hex_to_rgb(hex_color):
                hex_color = hex_color.lstrip('#')
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
            text_color = hex_to_rgb(font_color) + (255,)  # 添加alpha通道
            
            # 计算文字位置
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            img_width, img_height = img.size
            
            # 根据position参数计算坐标
            positions = {
                "center": ((img_width - text_width) // 2, (img_height - text_height) // 2),
                "top-left": (20, 20),
                "top-center": ((img_width - text_width) // 2, 20),
                "top-right": (img_width - text_width - 20, 20),
                "middle-left": (20, (img_height - text_height) // 2),
                "middle-right": (img_width - text_width - 20, (img_height - text_height) // 2),
                "bottom-left": (20, img_height - text_height - 20),
                "bottom-center": ((img_width - text_width) // 2, img_height - text_height - 20),
                "bottom-right": (img_width - text_width - 20, img_height - text_height - 20)
            }
            
            x, y = positions.get(position, positions["center"])
            
            # 如果有背景颜色，先绘制背景
            if background_color:
                bg_color = hex_to_rgb(background_color) + (255,)
                padding = 5
                draw.rectangle(
                    [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
                    fill=bg_color
                )
            
            # 绘制文字
            draw.text((x, y), text, fill=text_color, font=font)
            
            # 转换回RGB模式并保存
            if img.mode == "RGBA":
                # 创建白色背景
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])  # 使用alpha通道作为mask
                img = background
            
            # 保存为字节
            output = io.BytesIO()
            img.save(output, format="JPEG", quality=quality)
            return output.getvalue()
            
        except Exception as e:
            print(f"添加文字时出错: {e}")
            return image_bytes  # 返回原始图片
        
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
