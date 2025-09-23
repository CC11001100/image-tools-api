"""裁剪遮罩处理功能"""
from PIL import Image, ImageDraw
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.logger import logger


class ClippingMasks:
    """裁剪遮罩处理功能"""
    
    @staticmethod
    def apply_clipping_mask(
        image: Image.Image,
        shape: str = "circle",
        padding: int = 0
    ) -> Image.Image:
        """
        应用剪贴蒙版
        
        Args:
            image: 输入图片
            shape: 形状 (circle, ellipse, rounded_rect)
            padding: 内边距
            
        Returns:
            处理后的图片
        """
        logger.info(f"应用剪贴蒙版: 形状={shape}, 内边距={padding}")
        
        try:
            # 转换为RGBA
            img = image.convert("RGBA")
            width, height = img.size
            
            # 创建蒙版
            mask = Image.new("L", (width, height), 0)
            draw = ImageDraw.Draw(mask)
            
            if shape == "circle":
                # 圆形蒙版
                size = min(width, height) - 2 * padding
                x = (width - size) // 2
                y = (height - size) // 2
                draw.ellipse([x, y, x + size, y + size], fill=255)
                
            elif shape == "ellipse":
                # 椭圆形蒙版
                draw.ellipse([padding, padding, width - padding, height - padding], fill=255)
                
            elif shape == "rounded_rect":
                # 圆角矩形蒙版
                radius = min(width, height) // 10
                draw.rounded_rectangle(
                    [padding, padding, width - padding, height - padding],
                    radius=radius,
                    fill=255
                )
            
            # 应用蒙版
            img.putalpha(mask)
            
            logger.info(f"剪贴蒙版应用成功: 形状={shape}")
            return img
            
        except Exception as e:
            logger.error(f"剪贴蒙版应用失败: {str(e)}")
            raise
