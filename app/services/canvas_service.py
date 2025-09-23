from PIL import Image, ImageOps
import io
from typing import Optional, Tuple, Union
from ..utils.logger import logger


class CanvasService:
    """画布调整服务"""

    @staticmethod
    def process_canvas(
        image_bytes: bytes,
        canvas_type: str,
        background_color: str = "#FFFFFF",
        border_width: int = 0,
        border_color: str = "#000000",
        padding: int = 0,
        quality: int = 90
    ) -> bytes:
        """
        通用画布处理方法

        Args:
            image_bytes: 输入图片的字节数据
            canvas_type: 画布类型
            background_color: 背景颜色
            border_width: 边框宽度
            border_color: 边框颜色
            padding: 内边距
            quality: 输出图像质量 (1-100)

        Returns:
            处理后图片的字节数据
        """
        logger.info(f"执行画布处理: {canvas_type}")

        if canvas_type == "border" or border_width > 0:
            return CanvasService.add_border(image_bytes, border_width, border_color, quality)
        elif canvas_type == "padding" or padding > 0:
            return CanvasService.add_padding(image_bytes, padding, background_color, quality)
        elif canvas_type == "expand":
            # 默认扩展画布
            return CanvasService.expand_canvas(image_bytes, 50, 50, 50, 50, background_color, quality)
        else:
            # 默认添加边框
            return CanvasService.add_border(image_bytes, border_width or 10, border_color, quality)
    
    @staticmethod
    def expand_canvas(
        image_bytes: bytes,
        top: int = 0,
        bottom: int = 0,
        left: int = 0,
        right: int = 0,
        fill_color: Union[str, Tuple[int, int, int]] = "white",
        quality: int = 90
    ) -> bytes:
        """
        扩展画布
        
        Args:
            image_bytes: 输入图片的字节数据
            top: 顶部扩展像素
            bottom: 底部扩展像素
            left: 左侧扩展像素
            right: 右侧扩展像素
            fill_color: 填充颜色
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"扩展画布: top={top}, bottom={bottom}, left={left}, right={right}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # 处理填充颜色
            if isinstance(fill_color, str) and fill_color.startswith('#'):
                # 十六进制颜色
                fill_color = fill_color[1:]
                fill_rgb = tuple(int(fill_color[i:i+2], 16) for i in (0, 2, 4))
            else:
                fill_rgb = fill_color
            
            # 计算新画布尺寸
            new_width = img.width + left + right
            new_height = img.height + top + bottom
            
            # 创建新画布
            if img.mode == 'RGBA':
                # 对于RGBA图像，创建透明背景
                new_img = Image.new('RGBA', (new_width, new_height), (255, 255, 255, 0))
            else:
                new_img = Image.new(img.mode, (new_width, new_height), fill_rgb)
            
            # 将原图粘贴到新画布
            new_img.paste(img, (left, top))
            
            # 保存并返回
            output = io.BytesIO()
            format = img.format if img.format else "JPEG"
            
            # 如果是JPEG格式且有透明度，转换为RGB
            if format == "JPEG" and new_img.mode == "RGBA":
                # 创建白色背景
                background = Image.new('RGB', new_img.size, fill_rgb)
                background.paste(new_img, mask=new_img.split()[3])
                new_img = background
            
            new_img.save(output, format=format, quality=quality)
            
            logger.info("画布扩展成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"扩展画布失败: {e}")
            raise
    
    @staticmethod
    def add_border(
        image_bytes: bytes,
        border_width: int = 10,
        border_color: Union[str, Tuple[int, int, int]] = "black",
        quality: int = 90
    ) -> bytes:
        """
        添加边框
        
        Args:
            image_bytes: 输入图片的字节数据
            border_width: 边框宽度
            border_color: 边框颜色
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"添加边框: width={border_width}, color={border_color}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # 处理边框颜色
            if isinstance(border_color, str) and border_color.startswith('#'):
                # 十六进制颜色
                border_color = border_color[1:]
                border_rgb = tuple(int(border_color[i:i+2], 16) for i in (0, 2, 4))
            else:
                border_rgb = border_color
            
            # 使用ImageOps添加边框
            bordered_img = ImageOps.expand(img, border=border_width, fill=border_rgb)
            
            # 保存并返回
            output = io.BytesIO()
            format = img.format if img.format else "JPEG"
            bordered_img.save(output, format=format, quality=quality)
            
            logger.info("边框添加成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"添加边框失败: {e}")
            raise
    
    @staticmethod
    def add_padding(
        image_bytes: bytes,
        padding: int = 20,
        padding_color: Union[str, Tuple[int, int, int]] = "white",
        quality: int = 90
    ) -> bytes:
        """
        添加内边距（留白）
        
        Args:
            image_bytes: 输入图片的字节数据
            padding: 内边距大小
            padding_color: 内边距颜色
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"添加内边距: padding={padding}")
        
        # 使用expand_canvas实现
        return CanvasService.expand_canvas(
            image_bytes,
            top=padding,
            bottom=padding,
            left=padding,
            right=padding,
            fill_color=padding_color,
            quality=quality
        )
    
    @staticmethod
    def change_aspect_ratio(
        image_bytes: bytes,
        target_ratio: str = "16:9",
        position: str = "center",
        fill_color: Union[str, Tuple[int, int, int]] = "black",
        quality: int = 90
    ) -> bytes:
        """
        修改画布比例
        
        Args:
            image_bytes: 输入图片的字节数据
            target_ratio: 目标比例 (如 "16:9", "4:3", "1:1", "9:16")
            position: 图片位置 ("center", "top", "bottom", "left", "right")
            fill_color: 填充颜色
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"修改画布比例: ratio={target_ratio}, position={position}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # 解析目标比例
            ratio_parts = target_ratio.split(':')
            target_width_ratio = float(ratio_parts[0])
            target_height_ratio = float(ratio_parts[1])
            target_aspect = target_width_ratio / target_height_ratio
            
            # 当前比例
            current_aspect = img.width / img.height
            
            # 计算新尺寸
            if current_aspect > target_aspect:
                # 图片更宽，需要增加高度
                new_width = img.width
                new_height = int(img.width / target_aspect)
            else:
                # 图片更高，需要增加宽度
                new_width = int(img.height * target_aspect)
                new_height = img.height
            
            # 计算扩展量
            width_diff = new_width - img.width
            height_diff = new_height - img.height
            
            # 根据位置计算边距
            if position == "center":
                left = width_diff // 2
                right = width_diff - left
                top = height_diff // 2
                bottom = height_diff - top
            elif position == "top":
                left = width_diff // 2
                right = width_diff - left
                top = 0
                bottom = height_diff
            elif position == "bottom":
                left = width_diff // 2
                right = width_diff - left
                top = height_diff
                bottom = 0
            elif position == "left":
                left = 0
                right = width_diff
                top = height_diff // 2
                bottom = height_diff - top
            elif position == "right":
                left = width_diff
                right = 0
                top = height_diff // 2
                bottom = height_diff - top
            else:
                # 默认居中
                left = width_diff // 2
                right = width_diff - left
                top = height_diff // 2
                bottom = height_diff - top
            
            # 扩展画布
            return CanvasService.expand_canvas(
                image_bytes,
                top=top,
                bottom=bottom,
                left=left,
                right=right,
                fill_color=fill_color,
                quality=quality
            )
            
        except Exception as e:
            logger.error(f"修改画布比例失败: {e}")
            raise 