"""边框叠加功能"""
from PIL import Image, ImageDraw
from typing import Tuple
from ...utils.logger import logger


class BorderService:
    """边框叠加服务"""
    
    @staticmethod
    def add_border(
        image: Image.Image,
        border_width: int = 10,
        border_color: Tuple[int, int, int] = (0, 0, 0),
        border_style: str = "solid"
    ) -> Image.Image:
        """添加边框
        
        Args:
            image: 输入图片
            border_width: 边框宽度
            border_color: 边框颜色
            border_style: 边框样式 (solid, double, rounded)
            
        Returns:
            处理后的图片
        """
        try:
            width, height = image.size
            
            if border_style == "solid":
                # 创建新图片
                new_width = width + 2 * border_width
                new_height = height + 2 * border_width
                bordered = Image.new(image.mode, (new_width, new_height), border_color)
                bordered.paste(image, (border_width, border_width))
                
            elif border_style == "double":
                # 双线边框
                outer_width = border_width
                inner_width = border_width // 3
                gap = border_width // 3
                
                # 外边框
                new_width = width + 2 * outer_width
                new_height = height + 2 * outer_width
                bordered = Image.new(image.mode, (new_width, new_height), border_color)
                
                # 中间间隙（白色）
                gap_box = Image.new(image.mode, 
                    (width + 2 * (outer_width - inner_width), 
                     height + 2 * (outer_width - inner_width)), 
                    (255, 255, 255))
                bordered.paste(gap_box, (inner_width, inner_width))
                
                # 内边框
                inner_box = Image.new(image.mode,
                    (width + 2 * gap, height + 2 * gap),
                    border_color)
                bordered.paste(inner_box, (outer_width - gap, outer_width - gap))
                
                # 粘贴原图
                bordered.paste(image, (outer_width, outer_width))
                
            elif border_style == "rounded":
                # 圆角边框
                new_width = width + 2 * border_width
                new_height = height + 2 * border_width
                bordered = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
                
                # 绘制圆角矩形
                draw = ImageDraw.Draw(bordered)
                radius = border_width * 2
                draw.rounded_rectangle(
                    [(0, 0), (new_width - 1, new_height - 1)],
                    radius=radius,
                    fill=border_color
                )
                
                # 创建内部遮罩
                mask = Image.new("L", (width, height), 255)
                bordered.paste(image, (border_width, border_width), mask)
                
                # 转换回原始模式
                if image.mode != "RGBA":
                    bordered = bordered.convert(image.mode)
            else:
                bordered = image.copy()
            
            logger.info(f"边框添加成功: 宽度={border_width}, 样式={border_style}")
            return bordered
            
        except Exception as e:
            logger.error(f"边框添加失败: {str(e)}")
            raise 