"""渐变遮罩处理功能"""
from PIL import Image
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.logger import logger


class GradientMasks:
    """渐变遮罩处理功能"""
    
    @staticmethod
    def apply_gradient_mask(
        image: Image.Image,
        gradient_type: str = "linear",
        direction: str = "horizontal",
        start_opacity: float = 1.0,
        end_opacity: float = 0.0
    ) -> Image.Image:
        """
        应用渐变蒙版
        
        Args:
            image: 输入图片
            gradient_type: 渐变类型 (linear, radial)
            direction: 方向 (horizontal, vertical, diagonal)
            start_opacity: 起始透明度
            end_opacity: 结束透明度
            
        Returns:
            处理后的图片
        """
        logger.info(f"应用渐变蒙版: 类型={gradient_type}, 方向={direction}, 透明度={start_opacity}-{end_opacity}")
        
        try:
            # 转换为RGBA
            img = image.convert("RGBA")
            width, height = img.size
            
            # 创建渐变蒙版
            mask = Image.new("L", (width, height))
            
            if gradient_type == "linear":
                # 线性渐变
                mask_array = np.zeros((height, width), dtype=np.uint8)
                
                if direction == "horizontal":
                    for x in range(width):
                        alpha = start_opacity + (end_opacity - start_opacity) * x / width
                        mask_array[:, x] = int(alpha * 255)
                        
                elif direction == "vertical":
                    for y in range(height):
                        alpha = start_opacity + (end_opacity - start_opacity) * y / height
                        mask_array[y, :] = int(alpha * 255)
                        
                elif direction == "diagonal":
                    for y in range(height):
                        for x in range(width):
                            progress = (x + y) / (width + height)
                            alpha = start_opacity + (end_opacity - start_opacity) * progress
                            mask_array[y, x] = int(alpha * 255)
                
                mask = Image.fromarray(mask_array)
                
            elif gradient_type == "radial":
                # 径向渐变
                center_x, center_y = width // 2, height // 2
                max_radius = np.sqrt(center_x**2 + center_y**2)
                
                mask_array = np.zeros((height, width), dtype=np.uint8)
                
                for y in range(height):
                    for x in range(width):
                        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                        progress = distance / max_radius
                        alpha = start_opacity + (end_opacity - start_opacity) * progress
                        mask_array[y, x] = int(np.clip(alpha * 255, 0, 255))
                
                mask = Image.fromarray(mask_array)
            
            # 应用蒙版
            img.putalpha(mask)
            
            logger.info(f"渐变蒙版应用成功: 类型={gradient_type}, 方向={direction}")
            return img
            
        except Exception as e:
            logger.error(f"渐变蒙版应用失败: {str(e)}")
            raise
