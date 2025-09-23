"""GIF动画创建功能"""
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple
import numpy as np
from app.utils.logger import logger


class AnimationCreator:
    """GIF动画创建功能"""
    
    @staticmethod
    def create_animated_text_gif(
        text: str,
        font_size: int = 48,
        width: int = 400,
        height: int = 200,
        bg_color: Tuple[int, int, int] = (255, 255, 255),
        text_color: Tuple[int, int, int] = (0, 0, 0),
        animation_type: str = "fade",
        duration: int = 100,
        frames: int = 10
    ) -> bytes:
        """
        创建动画文字GIF
        
        Args:
            text: 文字内容
            font_size: 字体大小
            width: 画布宽度
            height: 画布高度
            bg_color: 背景颜色
            text_color: 文字颜色
            animation_type: 动画类型 (fade, slide, bounce)
            duration: 每帧持续时间
            frames: 总帧数
            
        Returns:
            GIF字节数据
        """
        logger.info(f"创建动画文字GIF: '{text}', 动画类型={animation_type}, 帧数={frames}")
        
        try:
            from .basic_conversion import BasicConversion
            
            images = []
            
            # 尝试加载字体
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            for i in range(frames):
                # 创建帧
                img = Image.new('RGB', (width, height), bg_color)
                draw = ImageDraw.Draw(img)
                
                # 计算文字位置
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                if animation_type == "fade":
                    # 淡入淡出效果
                    alpha = int(255 * (i / frames))
                    fade_color = tuple(
                        int(bg_color[j] + (text_color[j] - bg_color[j]) * i / frames)
                        for j in range(3)
                    )
                    x = (width - text_width) // 2
                    y = (height - text_height) // 2
                    draw.text((x, y), text, fill=fade_color, font=font)
                    
                elif animation_type == "slide":
                    # 滑动效果
                    x = int((width + text_width) * i / frames - text_width)
                    y = (height - text_height) // 2
                    draw.text((x, y), text, fill=text_color, font=font)
                    
                elif animation_type == "bounce":
                    # 弹跳效果
                    x = (width - text_width) // 2
                    y_offset = abs(np.sin(i * np.pi / frames)) * height // 4
                    y = int((height - text_height) // 2 - y_offset)
                    draw.text((x, y), text, fill=text_color, font=font)
                
                images.append(img)
            
            # 创建GIF
            return BasicConversion.images_to_gif(images, duration, loop=0)
            
        except Exception as e:
            logger.error(f"创建动画文字GIF失败: {str(e)}")
            raise
