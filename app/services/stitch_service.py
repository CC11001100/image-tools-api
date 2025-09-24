"""
stitch_service - 图片拼接服务
"""

from PIL import Image, ImageDraw
import io
from typing import List, Tuple, Optional, Union
import logging

logger = logging.getLogger(__name__)

class StitchService:
    """图片拼接服务"""

    @staticmethod
    def stitch_images(
        images: List[Image.Image],
        direction: str = "horizontal",
        alignment: str = "center",
        spacing: int = 0,
        background_color: str = "white",
        resize_mode: str = "none",
        quality: int = 95
    ) -> Image.Image:
        """
        拼接多张图片

        Args:
            images: 图片列表
            direction: 拼接方向 ("horizontal" 或 "vertical")
            alignment: 对齐方式 ("start", "center", "end")
            spacing: 图片间距
            background_color: 背景颜色
            resize_mode: 调整模式 ("none", "fit", "fill")
            quality: 输出质量

        Returns:
            拼接后的图片
        """
        if not images:
            raise ValueError("至少需要一张图片")

        # 简单的水平拼接实现
        if direction == "horizontal":
            total_width = sum(img.width for img in images) + spacing * (len(images) - 1)
            max_height = max(img.height for img in images)

            result = Image.new('RGB', (total_width, max_height), background_color)
            x_offset = 0

            for img in images:
                y_offset = 0
                if alignment == "center":
                    y_offset = (max_height - img.height) // 2
                elif alignment == "end":
                    y_offset = max_height - img.height

                result.paste(img, (x_offset, y_offset))
                x_offset += img.width + spacing

        else:  # vertical
            max_width = max(img.width for img in images)
            total_height = sum(img.height for img in images) + spacing * (len(images) - 1)

            result = Image.new('RGB', (max_width, total_height), background_color)
            y_offset = 0

            for img in images:
                x_offset = 0
                if alignment == "center":
                    x_offset = (max_width - img.width) // 2
                elif alignment == "end":
                    x_offset = max_width - img.width

                result.paste(img, (x_offset, y_offset))
                y_offset += img.height + spacing

        return result
