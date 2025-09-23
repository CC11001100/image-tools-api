from PIL import Image
import io
from typing import Optional
from ..utils.logger import logger


class TransformService:
    """图片变换服务 - 旋转和翻转"""

    @staticmethod
    def transform_image(
        image_bytes: bytes,
        transform_type: str,
        angle: float = 0,
        quality: int = 90
    ) -> bytes:
        """
        通用图片变换方法

        Args:
            image_bytes: 输入图片的字节数据
            transform_type: 变换类型
            angle: 旋转角度（仅用于旋转操作）
            quality: 输出图像质量 (1-100)

        Returns:
            处理后图片的字节数据
        """
        logger.info(f"执行图片变换: {transform_type}")

        if transform_type == "flip-horizontal":
            return TransformService.flip_horizontal(image_bytes, quality)
        elif transform_type == "flip-vertical":
            return TransformService.flip_vertical(image_bytes, quality)
        elif transform_type == "rotate-90-cw":
            return TransformService.rotate_90_clockwise(image_bytes, quality)
        elif transform_type == "rotate-90-ccw":
            return TransformService.rotate_90_counterclockwise(image_bytes, quality)
        elif transform_type == "rotate-180":
            return TransformService.rotate_180(image_bytes, quality)
        elif transform_type == "rotate":
            return TransformService.rotate_image(image_bytes, angle, True, "white", quality)
        else:
            raise ValueError(f"不支持的变换类型: {transform_type}")
    
    @staticmethod
    def rotate_image(
        image_bytes: bytes,
        angle: float,
        expand: bool = True,
        fill_color: str = "white",
        quality: int = 90
    ) -> bytes:
        """
        旋转图片
        
        Args:
            image_bytes: 输入图片的字节数据
            angle: 旋转角度（正数为逆时针，负数为顺时针）
            expand: 是否扩展画布以包含完整的旋转图像
            fill_color: 填充颜色（当expand=False时的背景色）
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"旋转图片: angle={angle}°, expand={expand}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # 处理填充颜色
            if fill_color.startswith('#'):
                # 十六进制颜色
                fill_color = fill_color[1:]
                fill_rgb = tuple(int(fill_color[i:i+2], 16) for i in (0, 2, 4))
            else:
                # 颜色名称
                fill_rgb = fill_color
            
            # 执行旋转
            rotated_img = img.rotate(
                angle, 
                expand=expand, 
                fillcolor=fill_rgb,
                resample=Image.BICUBIC
            )
            
            # 保存并返回
            output = io.BytesIO()
            format = img.format if img.format else "JPEG"
            
            # 如果是JPEG格式且有透明度，转换为RGB
            if format == "JPEG" and rotated_img.mode in ("RGBA", "LA"):
                rotated_img = rotated_img.convert("RGB")
            
            rotated_img.save(output, format=format, quality=quality)
            
            logger.info("图片旋转成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"旋转图片失败: {e}")
            raise
    
    @staticmethod
    def flip_horizontal(
        image_bytes: bytes,
        quality: int = 90
    ) -> bytes:
        """
        水平翻转图片（镜像）
        
        Args:
            image_bytes: 输入图片的字节数据
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info("水平翻转图片")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # 执行水平翻转
            flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
            
            # 保存并返回
            output = io.BytesIO()
            format = img.format if img.format else "JPEG"
            flipped_img.save(output, format=format, quality=quality)
            
            logger.info("水平翻转成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"水平翻转失败: {e}")
            raise
    
    @staticmethod
    def flip_vertical(
        image_bytes: bytes,
        quality: int = 90
    ) -> bytes:
        """
        垂直翻转图片
        
        Args:
            image_bytes: 输入图片的字节数据
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info("垂直翻转图片")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # 执行垂直翻转
            flipped_img = img.transpose(Image.FLIP_TOP_BOTTOM)
            
            # 保存并返回
            output = io.BytesIO()
            format = img.format if img.format else "JPEG"
            flipped_img.save(output, format=format, quality=quality)
            
            logger.info("垂直翻转成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"垂直翻转失败: {e}")
            raise
    
    @staticmethod
    def rotate_90_clockwise(
        image_bytes: bytes,
        quality: int = 90
    ) -> bytes:
        """
        顺时针旋转90度
        
        Args:
            image_bytes: 输入图片的字节数据
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info("顺时针旋转90度")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # 执行90度旋转
            rotated_img = img.transpose(Image.ROTATE_270)  # PIL中ROTATE_270实际是顺时针90度
            
            # 保存并返回
            output = io.BytesIO()
            format = img.format if img.format else "JPEG"
            rotated_img.save(output, format=format, quality=quality)
            
            logger.info("顺时针旋转90度成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"顺时针旋转90度失败: {e}")
            raise
    
    @staticmethod
    def rotate_90_counterclockwise(
        image_bytes: bytes,
        quality: int = 90
    ) -> bytes:
        """
        逆时针旋转90度
        
        Args:
            image_bytes: 输入图片的字节数据
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info("逆时针旋转90度")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # 执行90度旋转
            rotated_img = img.transpose(Image.ROTATE_90)
            
            # 保存并返回
            output = io.BytesIO()
            format = img.format if img.format else "JPEG"
            rotated_img.save(output, format=format, quality=quality)
            
            logger.info("逆时针旋转90度成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"逆时针旋转90度失败: {e}")
            raise
    
    @staticmethod
    def rotate_180(
        image_bytes: bytes,
        quality: int = 90
    ) -> bytes:
        """
        旋转180度
        
        Args:
            image_bytes: 输入图片的字节数据
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info("旋转180度")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # 执行180度旋转
            rotated_img = img.transpose(Image.ROTATE_180)
            
            # 保存并返回
            output = io.BytesIO()
            format = img.format if img.format else "JPEG"
            rotated_img.save(output, format=format, quality=quality)
            
            logger.info("旋转180度成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"旋转180度失败: {e}")
            raise 