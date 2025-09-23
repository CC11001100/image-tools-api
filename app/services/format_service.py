from PIL import Image
import io
from typing import Optional, Dict, Any
from ..utils.logger import logger


class FormatService:
    """图片格式转换服务"""
    
    # 支持的格式
    SUPPORTED_FORMATS = {
        'jpeg': {'extensions': ['.jpg', '.jpeg'], 'mode': 'RGB'},
        'png': {'extensions': ['.png'], 'mode': 'RGBA'},
        'gif': {'extensions': ['.gif'], 'mode': 'P'},
        'webp': {'extensions': ['.webp'], 'mode': 'RGBA'},
        'bmp': {'extensions': ['.bmp'], 'mode': 'RGB'},
        'tiff': {'extensions': ['.tif', '.tiff'], 'mode': 'RGB'},
    }
    
    @staticmethod
    def convert_format(
        image_bytes: bytes,
        target_format: str,
        quality: int = 90,
        optimize: bool = True,
        **kwargs
    ) -> bytes:
        """
        转换图片格式
        
        Args:
            image_bytes: 输入图片的字节数据
            target_format: 目标格式 (jpeg, png, gif, webp, bmp, tiff)
            quality: 输出质量 (1-100)，仅对有损格式有效
            optimize: 是否优化文件大小
            **kwargs: 其他格式特定参数
            
        Returns:
            转换后图片的字节数据
        """
        target_format = target_format.lower()
        logger.info(f"格式转换: 目标格式={target_format}, quality={quality}")
        
        if target_format not in FormatService.SUPPORTED_FORMATS:
            raise ValueError(f"不支持的格式: {target_format}")
        
        try:
            # 打开图像
            img = Image.open(io.BytesIO(image_bytes))
            
            # 获取格式信息
            format_info = FormatService.SUPPORTED_FORMATS[target_format]
            
            # 处理透明度
            if target_format in ['jpeg', 'bmp']:
                # JPEG和BMP不支持透明度
                if img.mode in ('RGBA', 'LA', 'P'):
                    # 创建白色背景
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if 'A' in img.mode else None)
                    img = background
            elif target_format == 'gif' and img.mode != 'P':
                # GIF需要调色板模式
                if img.mode == 'RGBA':
                    # 保留透明度
                    img = img.convert('P', palette=Image.ADAPTIVE, colors=256)
                else:
                    img = img.convert('P', palette=Image.ADAPTIVE)
            
            # 保存参数
            save_kwargs = {
                'format': target_format.upper(),
                'optimize': optimize
            }
            
            # 格式特定参数
            if target_format in ['jpeg', 'webp']:
                save_kwargs['quality'] = quality
            elif target_format == 'png':
                save_kwargs['compress_level'] = kwargs.get('compress_level', 6)
            elif target_format == 'gif':
                if 'duration' in kwargs:
                    save_kwargs['duration'] = kwargs['duration']
                if 'loop' in kwargs:
                    save_kwargs['loop'] = kwargs['loop']
            elif target_format == 'tiff':
                save_kwargs['compression'] = kwargs.get('compression', 'tiff_lzw')
            
            # 保存并返回
            output = io.BytesIO()
            img.save(output, **save_kwargs)
            
            logger.info(f"格式转换成功: {target_format.upper()}")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"格式转换失败: {e}")
            raise
    
    @staticmethod
    def convert_to_jpeg(
        image_bytes: bytes,
        quality: int = 90,
        optimize: bool = True
    ) -> bytes:
        """转换为JPEG格式"""
        return FormatService.convert_format(image_bytes, 'jpeg', quality, optimize)
    
    @staticmethod
    def convert_to_png(
        image_bytes: bytes,
        compress_level: int = 6,
        optimize: bool = True
    ) -> bytes:
        """转换为PNG格式"""
        return FormatService.convert_format(
            image_bytes, 'png', 
            optimize=optimize,
            compress_level=compress_level
        )
    
    @staticmethod
    def convert_to_webp(
        image_bytes: bytes,
        quality: int = 90,
        lossless: bool = False,
        optimize: bool = True
    ) -> bytes:
        """转换为WebP格式"""
        return FormatService.convert_format(
            image_bytes, 'webp',
            quality=quality,
            optimize=optimize,
            lossless=lossless
        )
    
    @staticmethod
    def get_image_info(image_bytes: bytes) -> Dict[str, Any]:
        """
        获取图片信息
        
        Args:
            image_bytes: 输入图片的字节数据
            
        Returns:
            包含图片信息的字典
        """
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            info = {
                'format': img.format,
                'mode': img.mode,
                'size': img.size,
                'width': img.width,
                'height': img.height,
                'info': img.info
            }
            
            # 获取文件大小
            info['file_size'] = len(image_bytes)
            
            # 获取EXIF信息（如果有）
            if hasattr(img, '_getexif') and img._getexif():
                info['exif'] = img._getexif()
            
            return info
            
        except Exception as e:
            logger.error(f"获取图片信息失败: {e}")
            raise 