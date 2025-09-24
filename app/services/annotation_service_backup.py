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
        
    def add_annotation(
        self,
        image: Image.Image,
        annotations: List[Dict[str, Any]],
        **kwargs
    ) -> Image.Image:
        """
        在图片上添加标注
        
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
    return annotation_service.add_annotation(*args, **kwargs)
