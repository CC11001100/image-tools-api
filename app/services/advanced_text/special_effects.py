"""特效文字功能"""
from PIL import Image, ImageDraw
import math
from typing import Tuple
from ...utils.logger import logger
from .base import AdvancedTextBase


class SpecialEffectsTextService:
    """特效文字服务"""
    
    @staticmethod
    def add_curved_text(
        image: Image.Image,
        text: str,
        center: Tuple[int, int],
        radius: int,
        font_size: int = 24,
        color: Tuple[int, int, int] = (0, 0, 0),
        start_angle: float = 0,
        arc_angle: float = 180,
        direction: str = "clockwise"
    ) -> Image.Image:
        """添加弯曲文字
        
        Args:
            image: 输入图片
            text: 文字内容
            center: 圆心位置
            radius: 半径
            font_size: 字体大小
            color: 文字颜色
            start_angle: 起始角度
            arc_angle: 弧度角度
            direction: 方向 (clockwise, counterclockwise)
            
        Returns:
            处理后的图片
        """
        try:
            img = image.copy()
            
            # 加载字体
            font = AdvancedTextBase.load_font("Arial", font_size)
            
            # 创建文字图层
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            text_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
            
            # 计算每个字符的角度
            char_count = len(text)
            if char_count == 0:
                return img
            
            angle_per_char = arc_angle / char_count
            
            # 绘制每个字符
            for i, char in enumerate(text):
                # 创建单个字符的图片
                char_img = Image.new('RGBA', (font_size * 2, font_size * 2), (0, 0, 0, 0))
                char_draw = ImageDraw.Draw(char_img)
                
                # 获取字符大小
                bbox = char_draw.textbbox((0, 0), char, font=font)
                char_width = bbox[2] - bbox[0]
                char_height = bbox[3] - bbox[1]
                
                # 绘制字符
                char_draw.text((font_size - char_width//2, font_size - char_height//2), 
                             char, fill=color, font=font)
                
                # 计算字符位置和角度
                if direction == "clockwise":
                    angle = start_angle + i * angle_per_char
                else:
                    angle = start_angle - i * angle_per_char
                
                angle_rad = math.radians(angle)
                
                # 计算字符位置
                x = center[0] + int(radius * math.cos(angle_rad))
                y = center[1] + int(radius * math.sin(angle_rad))
                
                # 旋转字符
                if direction == "clockwise":
                    char_img = char_img.rotate(-angle - 90, expand=True)
                else:
                    char_img = char_img.rotate(-angle + 90, expand=True)
                
                # 粘贴字符
                paste_x = x - char_img.width // 2
                paste_y = y - char_img.height // 2
                text_layer.paste(char_img, (paste_x, paste_y), char_img)
            
            # 合并图层
            result = Image.alpha_composite(img, text_layer)
            
            # 转回原始模式
            if image.mode != 'RGBA':
                result = result.convert(image.mode)
            
            logger.info(f"弯曲文字添加成功: 半径={radius}, 方向={direction}")
            return result
            
        except Exception as e:
            logger.error(f"添加弯曲文字失败: {str(e)}")
            raise
    
    @staticmethod
    def add_3d_text(
        image: Image.Image,
        text: str,
        position: Tuple[int, int],
        font_size: int = 48,
        text_color: Tuple[int, int, int] = (255, 255, 255),
        shadow_color: Tuple[int, int, int] = (128, 128, 128),
        depth: int = 5,
        direction: str = "bottom-right"
    ) -> Image.Image:
        """添加3D文字效果
        
        Args:
            image: 输入图片
            text: 文字内容
            position: 文字位置
            font_size: 字体大小
            text_color: 文字颜色
            shadow_color: 阴影颜色
            depth: 3D深度
            direction: 阴影方向
            
        Returns:
            处理后的图片
        """
        try:
            img = image.copy()
            
            # 加载字体
            font = AdvancedTextBase.load_font("Arial", font_size)
            
            draw = ImageDraw.Draw(img)
            
            # 计算阴影偏移
            offsets = {
                "bottom-right": (1, 1),
                "bottom-left": (-1, 1),
                "top-right": (1, -1),
                "top-left": (-1, -1)
            }
            offset_x, offset_y = offsets.get(direction, (1, 1))
            
            # 绘制多层阴影
            for i in range(depth, 0, -1):
                shadow_x = position[0] + offset_x * i
                shadow_y = position[1] + offset_y * i
                draw.text((shadow_x, shadow_y), text, fill=shadow_color, font=font)
            
            # 绘制主文字
            draw.text(position, text, fill=text_color, font=font)
            
            logger.info(f"3D文字添加成功: 深度={depth}, 方向={direction}")
            return img
            
        except Exception as e:
            logger.error(f"添加3D文字失败: {str(e)}")
            raise 