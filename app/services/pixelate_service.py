from PIL import Image, ImageFilter
import io
import numpy as np
from typing import Optional, Tuple, List
from ..utils.logger import logger


class PixelateService:
    """马赛克/像素化服务"""
    
    @staticmethod
    def pixelate_full(
        image_bytes: bytes,
        pixel_size: int = 10,
        quality: int = 90
    ) -> bytes:
        """
        全图马赛克处理
        
        Args:
            image_bytes: 输入图片的字节数据
            pixel_size: 像素块大小
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"全图马赛克处理: pixel_size={pixel_size}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # 获取原始尺寸
            original_size = img.size
            
            # 计算缩小后的尺寸
            small_size = (
                max(1, original_size[0] // pixel_size),
                max(1, original_size[1] // pixel_size)
            )
            
            # 缩小图片
            small_img = img.resize(small_size, Image.NEAREST)
            
            # 放大回原始尺寸
            pixelated_img = small_img.resize(original_size, Image.NEAREST)
            
            # 保存并返回
            output = io.BytesIO()
            format = img.format if img.format else "JPEG"
            pixelated_img.save(output, format=format, quality=quality)
            
            logger.info("全图马赛克处理成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"全图马赛克处理失败: {e}")
            raise
    
    @staticmethod
    def pixelate_region(
        image_bytes: bytes,
        x: int, y: int, width: int, height: int,
        pixel_size: int = 10,
        quality: int = 90
    ) -> bytes:
        """
        区域马赛克处理
        
        Args:
            image_bytes: 输入图片的字节数据
            x: 区域起始X坐标
            y: 区域起始Y坐标
            width: 区域宽度
            height: 区域高度
            pixel_size: 像素块大小
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"区域马赛克处理: region=({x},{y},{width},{height}), pixel_size={pixel_size}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # 验证区域边界
            img_width, img_height = img.size
            x = max(0, min(x, img_width))
            y = max(0, min(y, img_height))
            width = max(1, min(width, img_width - x))
            height = max(1, min(height, img_height - y))
            
            # 提取要处理的区域
            region = img.crop((x, y, x + width, y + height))
            
            # 对区域进行马赛克处理
            small_size = (
                max(1, width // pixel_size),
                max(1, height // pixel_size)
            )
            small_region = region.resize(small_size, Image.NEAREST)
            pixelated_region = small_region.resize((width, height), Image.NEAREST)
            
            # 将处理后的区域粘贴回原图
            result_img = img.copy()
            result_img.paste(pixelated_region, (x, y))
            
            # 保存并返回
            output = io.BytesIO()
            format = img.format if img.format else "JPEG"
            result_img.save(output, format=format, quality=quality)
            
            logger.info("区域马赛克处理成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"区域马赛克处理失败: {e}")
            raise
    
    @staticmethod
    def pixelate_multiple_regions(
        image_bytes: bytes,
        regions: List[Tuple[int, int, int, int]],
        pixel_size: int = 10,
        quality: int = 90
    ) -> bytes:
        """
        多区域马赛克处理
        
        Args:
            image_bytes: 输入图片的字节数据
            regions: 区域列表，每个区域为 (x, y, width, height)
            pixel_size: 像素块大小
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"多区域马赛克处理: {len(regions)}个区域, pixel_size={pixel_size}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            result_img = img.copy()
            
            for x, y, width, height in regions:
                # 验证区域边界
                img_width, img_height = img.size
                x = max(0, min(x, img_width))
                y = max(0, min(y, img_height))
                width = max(1, min(width, img_width - x))
                height = max(1, min(height, img_height - y))
                
                # 提取要处理的区域
                region = result_img.crop((x, y, x + width, y + height))
                
                # 对区域进行马赛克处理
                small_size = (
                    max(1, width // pixel_size),
                    max(1, height // pixel_size)
                )
                small_region = region.resize(small_size, Image.NEAREST)
                pixelated_region = small_region.resize((width, height), Image.NEAREST)
                
                # 将处理后的区域粘贴回原图
                result_img.paste(pixelated_region, (x, y))
            
            # 保存并返回
            output = io.BytesIO()
            format = img.format if img.format else "JPEG"
            result_img.save(output, format=format, quality=quality)
            
            logger.info("多区域马赛克处理成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"多区域马赛克处理失败: {e}")
            raise
    
    @staticmethod
    def blur_region(
        image_bytes: bytes,
        x: int, y: int, width: int, height: int,
        blur_radius: float = 5.0,
        quality: int = 90
    ) -> bytes:
        """
        区域模糊处理（另一种隐私保护方式）
        
        Args:
            image_bytes: 输入图片的字节数据
            x: 区域起始X坐标
            y: 区域起始Y坐标
            width: 区域宽度
            height: 区域高度
            blur_radius: 模糊半径
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"区域模糊处理: region=({x},{y},{width},{height}), blur_radius={blur_radius}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # 验证区域边界
            img_width, img_height = img.size
            x = max(0, min(x, img_width))
            y = max(0, min(y, img_height))
            width = max(1, min(width, img_width - x))
            height = max(1, min(height, img_height - y))
            
            # 提取要处理的区域
            region = img.crop((x, y, x + width, y + height))
            
            # 对区域进行模糊处理
            blurred_region = region.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            
            # 将处理后的区域粘贴回原图
            result_img = img.copy()
            result_img.paste(blurred_region, (x, y))
            
            # 保存并返回
            output = io.BytesIO()
            format = img.format if img.format else "JPEG"
            result_img.save(output, format=format, quality=quality)
            
            logger.info("区域模糊处理成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"区域模糊处理失败: {e}")
            raise
    
    @staticmethod
    def create_retro_pixel_art(
        image_bytes: bytes,
        colors: int = 16,
        pixel_size: int = 8,
        quality: int = 90
    ) -> bytes:
        """
        创建复古像素艺术效果
        
        Args:
            image_bytes: 输入图片的字节数据
            colors: 颜色数量
            pixel_size: 像素块大小
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"创建复古像素艺术: colors={colors}, pixel_size={pixel_size}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # 获取原始尺寸
            original_size = img.size
            
            # 缩小图片
            small_size = (
                max(1, original_size[0] // pixel_size),
                max(1, original_size[1] // pixel_size)
            )
            small_img = img.resize(small_size, Image.NEAREST)
            
            # 减少颜色数量
            quantized_img = small_img.quantize(colors=colors)
            
            # 转换回RGB模式
            rgb_img = quantized_img.convert('RGB')
            
            # 放大回原始尺寸
            pixel_art = rgb_img.resize(original_size, Image.NEAREST)
            
            # 保存并返回
            output = io.BytesIO()
            format = img.format if img.format else "JPEG"
            pixel_art.save(output, format=format, quality=quality)
            
            logger.info("复古像素艺术创建成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"创建复古像素艺术失败: {e}")
            raise 