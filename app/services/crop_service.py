from PIL import Image, ImageDraw
import io
from typing import Optional, Tuple, List
from ..utils.logger import logger


class CropService:
    """图片裁剪服务"""
    
    @staticmethod
    def _validate_crop_area(
        image_size: Tuple[int, int],
        x: int, y: int, width: int, height: int
    ) -> Tuple[int, int, int, int]:
        """验证并调整裁剪区域"""
        img_width, img_height = image_size
        
        # 确保坐标不为负数
        x = max(0, x)
        y = max(0, y)
        
        # 确保裁剪区域不超出图片边界
        if x + width > img_width:
            width = img_width - x
        if y + height > img_height:
            height = img_height - y
        
        # 确保宽高至少为1
        width = max(1, width)
        height = max(1, height)
        
        return x, y, width, height
    
    @staticmethod
    def crop_rectangle(
        image_bytes: bytes,
        x: int, y: int, width: int, height: int,
        quality: int = 90
    ) -> bytes:
        """
        矩形裁剪
        
        Args:
            image_bytes: 输入图片的字节数据
            x: 裁剪起始X坐标
            y: 裁剪起始Y坐标
            width: 裁剪宽度
            height: 裁剪高度
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"矩形裁剪: x={x}, y={y}, width={width}, height={height}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # 验证裁剪区域
            x, y, width, height = CropService._validate_crop_area(
                img.size, x, y, width, height
            )
            
            # 执行裁剪
            crop_box = (x, y, x + width, y + height)
            cropped_img = img.crop(crop_box)
            
            # 保存并返回
            output = io.BytesIO()
            format = img.format if img.format else "JPEG"
            cropped_img.save(output, format=format, quality=quality)
            
            logger.info("矩形裁剪成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"矩形裁剪失败: {e}")
            raise
    
    @staticmethod
    def crop_circle(
        image_bytes: bytes,
        center_x: int, center_y: int, radius: int,
        quality: int = 90
    ) -> bytes:
        """
        圆形裁剪
        
        Args:
            image_bytes: 输入图片的字节数据
            center_x: 圆心X坐标
            center_y: 圆心Y坐标
            radius: 圆半径
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据（PNG格式，支持透明背景）
        """
        logger.info(f"圆形裁剪: center=({center_x}, {center_y}), radius={radius}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
            
            # 创建圆形蒙版
            mask = Image.new("L", img.size, 0)
            draw = ImageDraw.Draw(mask)
            
            # 绘制圆形
            left = center_x - radius
            top = center_y - radius
            right = center_x + radius
            bottom = center_y + radius
            
            draw.ellipse([left, top, right, bottom], fill=255)
            
            # 应用蒙版
            result = Image.new("RGBA", img.size, (0, 0, 0, 0))
            result.paste(img, mask=mask)
            
            # 裁剪到圆形边界框
            crop_box = (
                max(0, left),
                max(0, top),
                min(img.width, right),
                min(img.height, bottom)
            )
            result = result.crop(crop_box)
            
            # 保存并返回
            output = io.BytesIO()
            result.save(output, format="PNG", quality=quality)
            
            logger.info("圆形裁剪成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"圆形裁剪失败: {e}")
            raise
    
    @staticmethod
    def crop_polygon(
        image_bytes: bytes,
        points: List[Tuple[int, int]],
        quality: int = 90
    ) -> bytes:
        """
        多边形裁剪
        
        Args:
            image_bytes: 输入图片的字节数据
            points: 多边形顶点坐标列表 [(x1, y1), (x2, y2), ...]
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据（PNG格式，支持透明背景）
        """
        logger.info(f"多边形裁剪: {len(points)}个顶点")
        
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
            
            # 创建多边形蒙版
            mask = Image.new("L", img.size, 0)
            draw = ImageDraw.Draw(mask)
            
            # 绘制多边形
            draw.polygon(points, fill=255)
            
            # 应用蒙版
            result = Image.new("RGBA", img.size, (0, 0, 0, 0))
            result.paste(img, mask=mask)
            
            # 计算边界框并裁剪
            if points:
                min_x = min(point[0] for point in points)
                max_x = max(point[0] for point in points)
                min_y = min(point[1] for point in points)
                max_y = max(point[1] for point in points)
                
                crop_box = (
                    max(0, min_x),
                    max(0, min_y),
                    min(img.width, max_x),
                    min(img.height, max_y)
                )
                result = result.crop(crop_box)
            
            # 保存并返回
            output = io.BytesIO()
            result.save(output, format="PNG", quality=quality)
            
            logger.info("多边形裁剪成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"多边形裁剪失败: {e}")
            raise
    
    @staticmethod
    def crop_smart_center(
        image_bytes: bytes,
        target_width: int, target_height: int,
        quality: int = 90
    ) -> bytes:
        """
        智能居中裁剪 - 保持比例并居中裁剪到目标尺寸
        
        Args:
            image_bytes: 输入图片的字节数据
            target_width: 目标宽度
            target_height: 目标高度
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"智能居中裁剪: {target_width}x{target_height}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # 计算原图和目标的比例
            original_ratio = img.width / img.height
            target_ratio = target_width / target_height
            
            if original_ratio > target_ratio:
                # 原图更宽，需要裁剪左右
                new_width = int(img.height * target_ratio)
                new_height = img.height
                x = (img.width - new_width) // 2
                y = 0
            else:
                # 原图更高，需要裁剪上下
                new_width = img.width
                new_height = int(img.width / target_ratio)
                x = 0
                y = (img.height - new_height) // 2
            
            # 执行裁剪
            crop_box = (x, y, x + new_width, y + new_height)
            cropped_img = img.crop(crop_box)
            
            # 调整到目标尺寸
            resized_img = cropped_img.resize((target_width, target_height), Image.LANCZOS)
            
            # 保存并返回
            output = io.BytesIO()
            format = img.format if img.format else "JPEG"
            resized_img.save(output, format=format, quality=quality)
            
            logger.info("智能居中裁剪成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"智能居中裁剪失败: {e}")
            raise 