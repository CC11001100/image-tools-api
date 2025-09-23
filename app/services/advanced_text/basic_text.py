"""基础高级文字功能"""
from PIL import Image, ImageDraw, ImageFilter
from typing import Tuple, Optional, List
from ...utils.logger import logger
from .base import AdvancedTextBase


class BasicTextService:
    """基础高级文字服务"""
    
    @staticmethod
    def add_advanced_text(
        image: Image.Image,
        text: str,
        font_family: str = "Arial",
        font_size: int = 48,
        font_color: str = "#000000",
        position: str = "center",
        x_offset: int = 0,
        y_offset: int = 0,
        rotation: int = 0,
        stroke_width: int = 0,
        stroke_color: str = "#FFFFFF",
        shadow_offset_x: int = 0,
        shadow_offset_y: int = 0,
        shadow_blur: int = 0,
        shadow_color: str = "#000000",
        opacity: float = 1.0,
        line_spacing: int = 5,
        max_width: Optional[int] = None
    ) -> Image.Image:
        """添加高级文字效果
        
        Args:
            image: 输入图片
            text: 文字内容
            font_family: 字体系列
            font_size: 字体大小
            font_color: 字体颜色
            position: 文字位置
            x_offset: X轴偏移量
            y_offset: Y轴偏移量
            rotation: 旋转角度
            stroke_width: 描边宽度
            stroke_color: 描边颜色
            shadow_offset_x: 阴影X偏移
            shadow_offset_y: 阴影Y偏移
            shadow_blur: 阴影模糊度
            shadow_color: 阴影颜色
            opacity: 不透明度
            line_spacing: 行间距
            max_width: 最大宽度（自动换行）
            
        Returns:
            处理后的图片
        """
        try:
            # 转换为RGBA模式
            img = image.convert("RGBA")
            width, height = img.size
            
            # 加载字体
            font = AdvancedTextBase.load_font(font_family, font_size)
            
            # 解析颜色
            text_color = AdvancedTextBase.hex_to_rgb(font_color)
            stroke_rgb = AdvancedTextBase.hex_to_rgb(stroke_color)
            shadow_rgb = AdvancedTextBase.hex_to_rgb(shadow_color)
            
            # 处理文字换行
            lines = BasicTextService._process_text_lines(text, font, max_width)
            
            # 计算总文字区域大小
            total_text_width, total_text_height = BasicTextService._calculate_text_area(
                lines, font, line_spacing
            )
            
            # 根据位置参数计算起始坐标
            start_x, start_y = AdvancedTextBase.calculate_text_position(
                position, total_text_width, total_text_height, width, height
            )
            
            # 应用偏移
            start_x += x_offset
            start_y += y_offset
            
            # 创建文字图层
            text_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
            
            # 处理阴影
            if shadow_offset_x != 0 or shadow_offset_y != 0 or shadow_blur > 0:
                shadow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                BasicTextService._draw_text_lines(
                    shadow_layer, lines, font, 
                    start_x + shadow_offset_x, start_y + shadow_offset_y,
                    line_spacing, shadow_rgb, stroke_width, shadow_rgb
                )
                
                # 应用模糊
                if shadow_blur > 0:
                    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=shadow_blur))
                
                # 合并阴影
                text_layer = Image.alpha_composite(text_layer, shadow_layer)
            
            # 绘制主文字
            BasicTextService._draw_text_lines(
                text_layer, lines, font, start_x, start_y, line_spacing,
                text_color, stroke_width, stroke_rgb
            )
            
            # 应用旋转
            if rotation != 0:
                # 计算旋转中心
                center_x = start_x + total_text_width // 2
                center_y = start_y + total_text_height // 2
                
                # 创建临时图层进行旋转
                temp_layer = text_layer.rotate(rotation, center=(center_x, center_y), expand=False)
                text_layer = temp_layer
            
            # 应用不透明度
            if opacity < 1.0:
                alpha = text_layer.split()[3]
                alpha = alpha.point(lambda p: int(p * opacity))
                text_layer.putalpha(alpha)
            
            # 合并图层
            result = Image.alpha_composite(img, text_layer)
            
            # 转回原始模式
            if image.mode != "RGBA":
                result = result.convert(image.mode)
            
            logger.info(f"高级文字添加成功: 文字='{text[:20]}...', 位置={position}, 旋转={rotation}°, 行数={len(lines)}")
            return result
            
        except Exception as e:
            logger.error(f"高级文字添加失败: {str(e)}")
            raise 
    
    @staticmethod
    def _process_text_lines(text: str, font, max_width: Optional[int] = None) -> List[str]:
        """处理文字换行"""
        # 处理手动换行符
        lines = text.split('\n')
        
        if max_width is None:
            return lines
        
        # 自动换行处理
        processed_lines = []
        for line in lines:
            if not line.strip():
                processed_lines.append("")
                continue
                
            # 检查是否需要换行
            test_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
            line_width = test_draw.textbbox((0, 0), line, font=font)[2]
            
            if line_width <= max_width:
                processed_lines.append(line)
            else:
                # 需要换行，按单词分割
                words = line.split(' ')
                current_line = ""
                
                for word in words:
                    test_line = current_line + (" " if current_line else "") + word
                    test_width = test_draw.textbbox((0, 0), test_line, font=font)[2]
                    
                    if test_width <= max_width:
                        current_line = test_line
                    else:
                        if current_line:
                            processed_lines.append(current_line)
                            current_line = word
                        else:
                            # 单个单词太长，强制换行
                            processed_lines.append(word)
                
                if current_line:
                    processed_lines.append(current_line)
        
        return processed_lines
    
    @staticmethod
    def _calculate_text_area(lines: List[str], font, line_spacing: int) -> Tuple[int, int]:
        """计算文字区域总大小"""
        if not lines:
            return 0, 0
        
        test_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        max_width = 0
        total_height = 0
        
        for i, line in enumerate(lines):
            if line.strip():  # 非空行
                bbox = test_draw.textbbox((0, 0), line, font=font)
                line_width = bbox[2] - bbox[0]
                line_height = bbox[3] - bbox[1]
                max_width = max(max_width, line_width)
            else:
                # 空行使用字体高度
                bbox = test_draw.textbbox((0, 0), "A", font=font)
                line_height = bbox[3] - bbox[1]
            
            total_height += line_height
            if i < len(lines) - 1:  # 不是最后一行
                total_height += line_spacing
        
        return max_width, total_height
    
    @staticmethod
    def _draw_text_lines(
        layer: Image.Image, 
        lines: List[str], 
        font, 
        start_x: int, 
        start_y: int,
        line_spacing: int,
        text_color: Tuple[int, int, int],
        stroke_width: int = 0,
        stroke_color: Tuple[int, int, int] = (255, 255, 255)
    ):
        """在图层上绘制多行文字"""
        draw = ImageDraw.Draw(layer)
        current_y = start_y
        
        for line in lines:
            if line.strip():  # 非空行
                if stroke_width > 0:
                    draw.text((start_x, current_y), line, font=font, 
                             fill=text_color, stroke_width=stroke_width, 
                             stroke_fill=stroke_color)
                else:
                    draw.text((start_x, current_y), line, font=font, fill=text_color)
            
            # 计算行高并移动到下一行
            bbox = draw.textbbox((0, 0), line if line.strip() else "A", font=font)
            line_height = bbox[3] - bbox[1]
            current_y += line_height + line_spacing 