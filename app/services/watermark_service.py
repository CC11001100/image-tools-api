from PIL import Image, ImageDraw, ImageFont
import io
import os
import math
from typing import Tuple, List, Optional
from ..utils.logger import logger


class WatermarkService:
    """水印处理服务"""
    
    @staticmethod
    def _get_system_font(font_size: int, font_family: str = "Arial") -> ImageFont.FreeTypeFont:
        """
        获取系统字体

        Args:
            font_size: 字体大小
            font_family: 字体族名称

        Returns:
            加载的字体对象
        """
        # 字体映射
        font_map = {
            "Arial": [
                "/System/Library/Fonts/Supplemental/Arial.ttf",  # macOS
                "C:\\Windows\\Fonts\\arial.ttf",  # Windows
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            ],
            "Times": [
                "/System/Library/Fonts/Times.ttc",  # macOS
                "C:\\Windows\\Fonts\\times.ttf",  # Windows
                "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",  # Linux
            ],
            "Helvetica": [
                "/System/Library/Fonts/Helvetica.ttc",  # macOS
                "C:\\Windows\\Fonts\\arial.ttf",  # Windows fallback
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            ],
            "Georgia": [
                "/System/Library/Fonts/Georgia.ttf",  # macOS
                "C:\\Windows\\Fonts\\georgia.ttf",  # Windows
                "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",  # Linux
            ],
            "Chinese": [
                "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",  # Linux
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",  # Linux
                "/System/Library/Fonts/PingFang.ttc",  # macOS
                "/System/Library/Fonts/STHeiti Light.ttc",  # macOS
                "C:\\Windows\\Fonts\\msyh.ttc",  # Windows 微软雅黑
                "C:\\Windows\\Fonts\\simhei.ttf",  # Windows 黑体
            ]
        }

        # 获取字体路径列表
        font_paths = font_map.get(font_family, font_map["Arial"])

        # 如果是中文字符，优先使用中文字体
        if any('\u4e00' <= char <= '\u9fff' for char in font_family):
            font_paths = font_map["Chinese"] + font_paths
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, font_size)
                except Exception as e:
                    logger.warning(f"无法加载字体 {font_path}: {e}")
                    continue
        
        logger.info("使用默认字体")
        return ImageFont.load_default()
    
    @staticmethod
    def _parse_color(color: str) -> Tuple[int, int, int]:
        """
        解析颜色字符串为RGB元组
        
        Args:
            color: 颜色字符串，支持十六进制和颜色名称
            
        Returns:
            RGB颜色元组
        """
        if color.startswith("#"):
            # 十六进制颜色
            try:
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                return (r, g, b)
            except ValueError:
                logger.warning(f"无效的十六进制颜色: {color}")
                return (255, 255, 255)
        
        # 颜色名称映射
        color_map = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "red": (255, 0, 0),
            "green": (0, 128, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
        }
        
        return color_map.get(color.lower(), (255, 255, 255))
    
    @staticmethod
    def _calculate_position(
        img_size: Tuple[int, int],
        text_size: Tuple[int, int],
        position: str,
        angle: int = 0,
        margin_x: int = 20,
        margin_y: int = 20
    ) -> Tuple[int, int]:
        """
        计算水印位置，考虑旋转角度
        
        Args:
            img_size: 图片尺寸 (宽, 高)
            text_size: 文字尺寸 (宽, 高)
            position: 位置标识
            angle: 旋转角度
            
        Returns:
            水印位置坐标 (x, y)
        """
        img_width, img_height = img_size
        text_width, text_height = text_size
        
        # 如果有旋转，计算旋转后的文字尺寸
        if angle != 0:
            angle_rad = math.radians(abs(angle))
            rotated_width = (
                abs(text_width * math.cos(angle_rad)) +
                abs(text_height * math.sin(angle_rad))
            )
            rotated_height = (
                abs(text_width * math.sin(angle_rad)) +
                abs(text_height * math.cos(angle_rad))
            )
            text_width = rotated_width
            text_height = rotated_height
        
        position_map = {
            "center": (
                (img_width - text_width) // 2,
                (img_height - text_height) // 2
            ),
            "top-left": (margin_x, margin_y),
            "top-center": (
                (img_width - text_width) // 2,
                margin_y
            ),
            "top-right": (
                img_width - text_width - margin_x,
                margin_y
            ),
            "center-left": (
                margin_x,
                (img_height - text_height) // 2
            ),
            "center-right": (
                img_width - text_width - margin_x,
                (img_height - text_height) // 2
            ),
            "bottom-left": (
                margin_x,
                img_height - text_height - margin_y
            ),
            "bottom-center": (
                (img_width - text_width) // 2,
                img_height - text_height - margin_y
            ),
            "bottom-right": (
                img_width - text_width - margin_x,
                img_height - text_height - margin_y
            ),
        }
        
        return position_map.get(position, position_map["center"])

    @staticmethod
    def _draw_text_with_effects(
        draw: ImageDraw.ImageDraw,
        position: Tuple[int, int],
        text: str,
        font: ImageFont.FreeTypeFont,
        fill_color: Tuple[int, int, int, int],
        stroke_width: int = 0,
        stroke_color: Tuple[int, int, int, int] = (0, 0, 0, 255),
        shadow_offset_x: int = 0,
        shadow_offset_y: int = 0,
        shadow_color: Tuple[int, int, int, int] = (0, 0, 0, 128)
    ):
        """
        绘制带效果的文字（阴影、描边）

        Args:
            draw: ImageDraw对象
            position: 文字位置
            text: 文字内容
            font: 字体
            fill_color: 填充颜色
            stroke_width: 描边宽度
            stroke_color: 描边颜色
            shadow_offset_x: 阴影X偏移
            shadow_offset_y: 阴影Y偏移
            shadow_color: 阴影颜色
        """
        x, y = position

        # 绘制阴影
        if shadow_offset_x != 0 or shadow_offset_y != 0:
            shadow_x = x + shadow_offset_x
            shadow_y = y + shadow_offset_y
            draw.text(
                (shadow_x, shadow_y),
                text,
                font=font,
                fill=shadow_color
            )

        # 绘制描边
        if stroke_width > 0:
            for dx in range(-stroke_width, stroke_width + 1):
                for dy in range(-stroke_width, stroke_width + 1):
                    if dx != 0 or dy != 0:
                        draw.text(
                            (x + dx, y + dy),
                            text,
                            font=font,
                            fill=stroke_color
                        )

        # 绘制主文字
        draw.text(
            (x, y),
            text,
            font=font,
            fill=fill_color
        )
    
    @staticmethod
    def add_watermark(
        image_bytes: bytes,
        text: str,
        position: str = "center",
        opacity: float = 0.5,
        color: str = "white",
        font_size: int = 40,
        angle: int = 0,
        quality: int = 90,
        font_family: str = "Arial",
        margin_x: int = 20,
        margin_y: int = 20,
        stroke_width: int = 0,
        stroke_color: str = "#000000",
        shadow_offset_x: int = 0,
        shadow_offset_y: int = 0,
        shadow_color: str = "#000000",
        repeat_mode: str = "none"
    ) -> bytes:
        """
        给图片添加文字水印
        
        Args:
            image_bytes: 输入图片的字节数据
            text: 水印文字内容
            position: 水印位置
            opacity: 透明度 (0-1)
            color: 水印颜色
            font_size: 字体大小
            angle: 旋转角度
            quality: 输出质量
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"添加水印: {text}, 位置: {position}, 透明度: {opacity}")
        
        try:
            # 打开图片并转换为RGBA模式
            img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
            watermark = Image.new("RGBA", img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark)
            
            # 获取字体和颜色
            font = WatermarkService._get_system_font(font_size, font_family)
            rgb = WatermarkService._parse_color(color)
            rgba = (*rgb, int(255 * opacity))

            # 描边和阴影颜色
            stroke_rgb = WatermarkService._parse_color(stroke_color)
            stroke_rgba = (*stroke_rgb, int(255 * opacity))
            shadow_rgb = WatermarkService._parse_color(shadow_color)
            shadow_rgba = (*shadow_rgb, int(255 * opacity * 0.5))
            
            # 处理多行文字
            lines = text.split('\n')
            max_width = 0
            total_height = 0
            line_heights: List[int] = []
            
            # 计算总高度和最大宽度
            for line in lines:
                text_bbox = draw.textbbox((0, 0), line, font=font)
                line_width = text_bbox[2] - text_bbox[0]
                line_height = text_bbox[3] - text_bbox[1]
                max_width = max(max_width, line_width)
                line_heights.append(line_height)
                total_height += line_height
            
            # 计算整体位置
            x, y = WatermarkService._calculate_position(
                img.size,
                (max_width, total_height),
                position,
                angle,
                margin_x,
                margin_y
            )
            
            if angle != 0:
                # 旋转水印处理
                big_watermark = Image.new(
                    "RGBA",
                    (img.width * 2, img.height * 2),
                    (0, 0, 0, 0)
                )
                big_draw = ImageDraw.Draw(big_watermark)
                
                # 绘制每行文字
                current_y = img.height
                for i, line in enumerate(lines):
                    WatermarkService._draw_text_with_effects(
                        big_draw,
                        (img.width, current_y),
                        line,
                        font,
                        rgba,
                        stroke_width,
                        stroke_rgba,
                        shadow_offset_x,
                        shadow_offset_y,
                        shadow_rgba
                    )
                    current_y += line_heights[i]
                
                # 旋转并裁剪
                rotated = big_watermark.rotate(
                    angle,
                    resample=Image.BICUBIC,
                    expand=False
                )
                offset_x = (rotated.width - img.width) // 2
                offset_y = (rotated.height - img.height) // 2
                watermark = rotated.crop((
                    offset_x,
                    offset_y,
                    offset_x + img.width,
                    offset_y + img.height
                ))
            else:
                # 直接绘制每行文字
                current_y = y
                for i, line in enumerate(lines):
                    WatermarkService._draw_text_with_effects(
                        draw,
                        (x, current_y),
                        line,
                        font,
                        rgba,
                        stroke_width,
                        stroke_rgba,
                        shadow_offset_x,
                        shadow_offset_y,
                        shadow_rgba
                    )
                    current_y += line_heights[i]
            
            # 处理重复水印
            if repeat_mode == "tile":
                # 平铺水印
                tile_watermark = Image.new("RGBA", img.size, (0, 0, 0, 0))
                tile_draw = ImageDraw.Draw(tile_watermark)

                # 计算平铺间距
                tile_spacing_x = max_width + 50
                tile_spacing_y = total_height + 30

                for tile_x in range(0, img.width, tile_spacing_x):
                    for tile_y in range(0, img.height, tile_spacing_y):
                        current_y = tile_y
                        for i, line in enumerate(lines):
                            if current_y < img.height:
                                WatermarkService._draw_text_with_effects(
                                    tile_draw,
                                    (tile_x, current_y),
                                    line,
                                    font,
                                    rgba,
                                    stroke_width,
                                    stroke_rgba,
                                    shadow_offset_x,
                                    shadow_offset_y,
                                    shadow_rgba
                                )
                            current_y += line_heights[i]

                watermark = tile_watermark

            elif repeat_mode == "diagonal":
                # 对角线重复水印
                diag_watermark = Image.new("RGBA", img.size, (0, 0, 0, 0))
                diag_draw = ImageDraw.Draw(diag_watermark)

                # 计算对角线间距
                diagonal_spacing = max(max_width, total_height) + 100

                # 从左上到右下的对角线
                for offset in range(-img.height, img.width + img.height, diagonal_spacing):
                    for y_pos in range(0, img.height, total_height + 50):
                        x_pos = offset + y_pos
                        if 0 <= x_pos < img.width:
                            current_y = y_pos
                            for i, line in enumerate(lines):
                                if current_y < img.height:
                                    WatermarkService._draw_text_with_effects(
                                        diag_draw,
                                        (x_pos, current_y),
                                        line,
                                        font,
                                        rgba,
                                        stroke_width,
                                        stroke_rgba,
                                        shadow_offset_x,
                                        shadow_offset_y,
                                        shadow_rgba
                                    )
                                current_y += line_heights[i]

                watermark = diag_watermark

            # 合并图像
            watermarked_img = Image.alpha_composite(img, watermark)
            result_img = watermarked_img.convert("RGB")
            
            # 保存并返回
            output = io.BytesIO()
            result_img.save(output, format="JPEG", quality=quality)
            
            logger.info("水印添加成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"添加水印失败: {e}")
            raise 