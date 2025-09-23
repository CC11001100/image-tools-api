from .watermark_service import WatermarkService
from .resize_service import ResizeService
from .filter_service import FilterService
from .crop_service import CropService
from .transform_service import TransformService
from ..utils.logger import logger
from typing import Optional, List, Tuple
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
import io


class ImageService:
    """图像处理服务统一入口"""
    
    @staticmethod
    def add_watermark(
        image_bytes: bytes,
        text: str,
        position: str = "center",
        opacity: float = 0.5,
        color: str = "white",
        font_size: int = 40,
        angle: int = 0,
    ) -> bytes:
        """添加水印"""
        return WatermarkService.add_watermark(
            image_bytes, text, position, opacity, color, font_size, angle
        )
    
    @staticmethod
    def resize_image(
        image_bytes: bytes,
        width: Optional[int] = None,
        height: Optional[int] = None,
        maintain_ratio: bool = True,
        quality: int = 90
    ) -> bytes:
        """调整图片大小"""
        return ResizeService.resize_image(
            image_bytes, width, height, maintain_ratio, quality
        )
    
    @staticmethod
    def apply_filter(
        image_bytes: bytes,
        filter_type: str,
        intensity: float = 1.0
    ) -> bytes:
        """应用基础滤镜"""
        return FilterService.apply_filter(image_bytes, filter_type, intensity)
    
    @staticmethod
    def crop_rectangle(
        image_bytes: bytes,
        x: int, y: int, width: int, height: int,
        quality: int = 90
    ) -> bytes:
        """矩形裁剪"""
        return CropService.crop_rectangle(image_bytes, x, y, width, height, quality)
    
    @staticmethod
    def crop_circle(
        image_bytes: bytes,
        center_x: int, center_y: int, radius: int,
        quality: int = 90
    ) -> bytes:
        """圆形裁剪"""
        return CropService.crop_circle(image_bytes, center_x, center_y, radius, quality)
    
    @staticmethod
    def crop_polygon(
        image_bytes: bytes,
        points: List[Tuple[int, int]],
        quality: int = 90
    ) -> bytes:
        """多边形裁剪"""
        return CropService.crop_polygon(image_bytes, points, quality)
    
    @staticmethod
    def crop_smart_center(
        image_bytes: bytes,
        target_width: int, target_height: int,
        quality: int = 90
    ) -> bytes:
        """智能居中裁剪"""
        return CropService.crop_smart_center(image_bytes, target_width, target_height, quality)
    
    @staticmethod
    def rotate_image(
        image_bytes: bytes,
        angle: float,
        expand: bool = True,
        fill_color: str = "white",
        quality: int = 90
    ) -> bytes:
        """旋转图片"""
        return TransformService.rotate_image(image_bytes, angle, expand, fill_color, quality)
    
    @staticmethod
    def flip_horizontal(
        image_bytes: bytes,
        quality: int = 90
    ) -> bytes:
        """水平翻转"""
        return TransformService.flip_horizontal(image_bytes, quality)
    
    @staticmethod
    def flip_vertical(
        image_bytes: bytes,
        quality: int = 90
    ) -> bytes:
        """垂直翻转"""
        return TransformService.flip_vertical(image_bytes, quality)
    
    @staticmethod
    def rotate_90_clockwise(
        image_bytes: bytes,
        quality: int = 90
    ) -> bytes:
        """顺时针旋转90度"""
        return TransformService.rotate_90_clockwise(image_bytes, quality)
    
    @staticmethod
    def rotate_90_counterclockwise(
        image_bytes: bytes,
        quality: int = 90
    ) -> bytes:
        """逆时针旋转90度"""
        return TransformService.rotate_90_counterclockwise(image_bytes, quality)
    
    @staticmethod
    def rotate_180(
        image_bytes: bytes,
        quality: int = 90
    ) -> bytes:
        """旋转180度"""
        return TransformService.rotate_180(image_bytes, quality)
    
    @staticmethod
    async def load_image(file: UploadFile) -> Image.Image:
        """从上传的文件加载图片"""
        try:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            # 转换为RGB模式以确保兼容性
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            return image
        except Exception as e:
            logger.error(f"加载图片失败: {str(e)}")
            raise ValueError(f"无法加载图片: {str(e)}")
    
    @staticmethod
    async def load_image_from_bytes(image_bytes: bytes) -> Image.Image:
        """从字节数据加载图片"""
        try:
            image = Image.open(io.BytesIO(image_bytes))
            # 转换为RGB模式以确保兼容性
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            return image
        except Exception as e:
            logger.error(f"从字节数据加载图片失败: {str(e)}")
            raise ValueError(f"无法从字节数据加载图片: {str(e)}")
    
    @staticmethod
    async def save_image(image: Image.Image, output_format: str = "PNG") -> StreamingResponse:
        """保存图片并返回StreamingResponse"""
        try:
            output = io.BytesIO()
            
            # 根据输出格式调整图片模式
            if output_format.upper() == "JPEG":
                if image.mode in ('RGBA', 'LA', 'P'):
                    # JPEG不支持透明度，转换为RGB
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    if image.mode == 'P':
                        image = image.convert('RGBA')
                    background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                    image = background
                image.save(output, format="JPEG", quality=95, optimize=True)
                media_type = "image/jpeg"
            else:
                # PNG格式保持原有模式或转换为RGBA
                if image.mode not in ('RGBA', 'RGB'):
                    image = image.convert('RGBA')
                image.save(output, format="PNG", optimize=True)
                media_type = "image/png"
            
            output.seek(0)
            return StreamingResponse(output, media_type=media_type)
            
        except Exception as e:
            logger.error(f"保存图片失败: {str(e)}")
            raise ValueError(f"无法保存图片: {str(e)}") 