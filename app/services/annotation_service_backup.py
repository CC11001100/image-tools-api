"""
标注服务模块 - 向后兼容实现
"""

from typing import Optional, Tuple, List, Dict, Any
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os


class AnnotationService:
    """图像标注服务"""
    
    def __init__(self):
        self.default_font_size = 16
        self.default_color = (255, 0, 0, 255)  # 红色
    
    @staticmethod
    def add_annotation(
        image_bytes: bytes,
        annotation_type: str,
        text: str = None,
        color: str = "#FF0000",
        position: str = "0,0",
        size: float = 1.0,
        quality: int = 90,
        **kwargs
    ) -> bytes:
        """
        为图片添加标注（静态方法）
        
        Args:
            image_bytes: 输入图片的字节数据
            annotation_type: 标注类型 (text, rectangle, circle, arrow)
            text: 标注文本
            color: 标注颜色
            position: 标注位置
            size: 标注大小
            quality: 输出质量
            **kwargs: 其他参数
            
        Returns:
            处理后图片的字节数据
        """
        try:
            # 打开图片
            image = Image.open(io.BytesIO(image_bytes))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # 创建图像副本
            result_image = image.copy()
            draw = ImageDraw.Draw(result_image)
            
            # 解析颜色
            if color.startswith('#'):
                color = color[1:]
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            color_rgb = (r, g, b, 255)
            
            # 解析位置
            pos_parts = position.split(',')
            
            if annotation_type == 'text' and text:
                # 文字标注
                x, y = int(pos_parts[0]), int(pos_parts[1])
                font_size = int(16 * size)
                try:
                    font = ImageFont.load_default()
                    draw.text((x, y), text, fill=color_rgb, font=font)
                except Exception as e:
                    print(f"添加文字标注时出错: {e}")
                    
            elif annotation_type == 'rectangle':
                # 矩形标注
                if len(pos_parts) >= 4:
                    x, y, w, h = map(int, pos_parts[:4])
                    width = max(1, int(2 * size))
                    draw.rectangle([x, y, x + w, y + h], outline=color_rgb, width=width)
                    
            elif annotation_type == 'circle':
                # 圆形标注
                if len(pos_parts) >= 3:
                    x, y, radius = map(int, pos_parts[:3])
                    radius = int(radius * size)
                    width = max(1, int(2 * size))
                    bbox = [x - radius, y - radius, x + radius, y + radius]
                    draw.ellipse(bbox, outline=color_rgb, width=width)
                    
            elif annotation_type == 'arrow':
                # 箭头标注
                if len(pos_parts) >= 4:
                    x1, y1, x2, y2 = map(int, pos_parts[:4])
                    width = max(1, int(2 * size))
                    draw.line([x1, y1, x2, y2], fill=color_rgb, width=width)
                    
                    # 添加箭头头部
                    import math
                    angle = math.atan2(y2 - y1, x2 - x1)
                    arrow_length = 10 * size
                    arrow_angle = math.pi / 6
                    
                    x3 = x2 - arrow_length * math.cos(angle - arrow_angle)
                    y3 = y2 - arrow_length * math.sin(angle - arrow_angle)
                    x4 = x2 - arrow_length * math.cos(angle + arrow_angle)
                    y4 = y2 - arrow_length * math.sin(angle + arrow_angle)
                    
                    draw.line([x2, y2, x3, y3], fill=color_rgb, width=width)
                    draw.line([x2, y2, x4, y4], fill=color_rgb, width=width)
            
            # 保存结果
            output = io.BytesIO()
            result_image.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            print(f"添加标注时出错: {e}")
            # 返回原图
            return image_bytes
        
    def add_annotation_instance(
        self,
        image: Image.Image,
        annotations: List[Dict[str, Any]],
        **kwargs
    ) -> Image.Image:
        """
        在图片上添加标注（实例方法，保持向后兼容）
        
        Args:
            image: PIL图像对象
            annotations: 标注列表，每个标注包含类型、位置、文本等信息
            **kwargs: 其他参数
            
        Returns:
            处理后的图像
        """
        try:
            # 创建图像副本
            result_image = image.copy()
            draw = ImageDraw.Draw(result_image)
            
            for annotation in annotations:
                annotation_type = annotation.get('type', 'text')
                
                if annotation_type == 'text':
                    self._add_text_annotation(draw, annotation)
                elif annotation_type == 'rectangle':
                    self._add_rectangle_annotation(draw, annotation)
                elif annotation_type == 'circle':
                    self._add_circle_annotation(draw, annotation)
                elif annotation_type == 'arrow':
                    self._add_arrow_annotation(draw, annotation)
            
            return result_image
            
        except Exception as e:
            print(f"添加标注时出错: {e}")
            return image
    
    def _add_text_annotation(self, draw: ImageDraw.Draw, annotation: Dict[str, Any]):
        """添加文字标注"""
        text = annotation.get('text', '')
        position = annotation.get('position', (10, 10))
        color = annotation.get('color', self.default_color)
        font_size = annotation.get('font_size', self.default_font_size)
        
        try:
            font = ImageFont.load_default()
            draw.text(position, text, fill=color, font=font)
        except Exception as e:
            print(f"添加文字标注时出错: {e}")
    
    def _add_rectangle_annotation(self, draw: ImageDraw.Draw, annotation: Dict[str, Any]):
        """添加矩形标注"""
        bbox = annotation.get('bbox', [10, 10, 100, 100])
        color = annotation.get('color', self.default_color)
        width = annotation.get('width', 2)
        
        try:
            draw.rectangle(bbox, outline=color, width=width)
        except Exception as e:
            print(f"添加矩形标注时出错: {e}")
    
    def _add_circle_annotation(self, draw: ImageDraw.Draw, annotation: Dict[str, Any]):
        """添加圆形标注"""
        center = annotation.get('center', (50, 50))
        radius = annotation.get('radius', 20)
        color = annotation.get('color', self.default_color)
        width = annotation.get('width', 2)
        
        try:
            bbox = [
                center[0] - radius,
                center[1] - radius,
                center[0] + radius,
                center[1] + radius
            ]
            draw.ellipse(bbox, outline=color, width=width)
        except Exception as e:
            print(f"添加圆形标注时出错: {e}")
    
    def _add_arrow_annotation(self, draw: ImageDraw.Draw, annotation: Dict[str, Any]):
        """添加箭头标注"""
        start = annotation.get('start', (10, 10))
        end = annotation.get('end', (50, 50))
        color = annotation.get('color', self.default_color)
        width = annotation.get('width', 2)
        
        try:
            # 绘制箭头线
            draw.line([start, end], fill=color, width=width)
            
            # 简单的箭头头部（三角形）
            import math
            angle = math.atan2(end[1] - start[1], end[0] - start[0])
            arrow_length = 10
            arrow_angle = math.pi / 6
            
            # 箭头的两个边
            x1 = end[0] - arrow_length * math.cos(angle - arrow_angle)
            y1 = end[1] - arrow_length * math.sin(angle - arrow_angle)
            x2 = end[0] - arrow_length * math.cos(angle + arrow_angle)
            y2 = end[1] - arrow_length * math.sin(angle + arrow_angle)
            
            draw.line([end, (x1, y1)], fill=color, width=width)
            draw.line([end, (x2, y2)], fill=color, width=width)
            
        except Exception as e:
            print(f"添加箭头标注时出错: {e}")


# 创建全局实例
annotation_service = AnnotationService()

# 导出函数
def add_annotation(*args, **kwargs):
    """添加标注到图片"""
    return annotation_service.add_annotation_instance(*args, **kwargs)
