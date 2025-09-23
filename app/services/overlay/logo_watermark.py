"""Logo和水印叠加功能"""
from PIL import Image
from typing import Tuple
from ...utils.logger import logger
from .base import OverlayBase


class LogoWatermarkService:
    """Logo和水印叠加服务"""
    
    @staticmethod
    def add_logo(
        base_image: Image.Image,
        logo_image: Image.Image,
        position: str = "bottom-right",
        opacity: float = 1.0,
        size_ratio: float = 0.2,
        padding: int = 20
    ) -> Image.Image:
        """添加Logo叠加
        
        Args:
            base_image: 基础图片
            logo_image: Logo图片
            position: 位置
            opacity: 透明度
            size_ratio: Logo相对于基础图片的大小比例
            padding: 边距
            
        Returns:
            处理后的图片
        """
        try:
            # 转换为RGBA模式
            base = base_image.convert("RGBA")
            logo = logo_image.convert("RGBA")
            
            # 计算Logo大小
            base_width, base_height = base.size
            max_logo_size = int(min(base_width, base_height) * size_ratio)
            
            # 保持Logo宽高比
            logo_width, logo_height = logo.size
            ratio = min(max_logo_size / logo_width, max_logo_size / logo_height)
            new_size = (int(logo_width * ratio), int(logo_height * ratio))
            logo = logo.resize(new_size, Image.Resampling.LANCZOS)
            
            # 调整透明度
            if opacity < 1.0:
                alpha = logo.split()[3]
                alpha = alpha.point(lambda p: p * opacity)
                logo.putalpha(alpha)
            
            # 计算位置
            x, y = OverlayBase.calculate_position(
                base.size, logo.size, position, padding
            )
            
            # 叠加Logo
            base.paste(logo, (x, y), logo)
            
            # 转回原始模式
            if base_image.mode != "RGBA":
                base = base.convert(base_image.mode)
            
            logger.info(f"Logo叠加成功: 位置={position}, 透明度={opacity}")
            return base
            
        except Exception as e:
            logger.error(f"Logo叠加失败: {str(e)}")
            raise
    
    @staticmethod
    def add_image_watermark(
        base_image: Image.Image,
        watermark_image: Image.Image,
        opacity: float = 0.3,
        tile: bool = False,
        spacing: int = 50
    ) -> Image.Image:
        """添加图片水印
        
        Args:
            base_image: 基础图片
            watermark_image: 水印图片
            opacity: 透明度
            tile: 是否平铺
            spacing: 平铺间距
            
        Returns:
            处理后的图片
        """
        try:
            # 转换为RGBA模式
            base = base_image.convert("RGBA")
            watermark = watermark_image.convert("RGBA")
            
            # 调整水印透明度
            if opacity < 1.0:
                alpha = watermark.split()[3]
                alpha = alpha.point(lambda p: p * opacity)
                watermark.putalpha(alpha)
            
            if tile:
                # 平铺水印
                base_width, base_height = base.size
                wm_width, wm_height = watermark.size
                
                # 创建临时图层
                overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
                
                # 平铺水印
                for x in range(0, base_width, wm_width + spacing):
                    for y in range(0, base_height, wm_height + spacing):
                        overlay.paste(watermark, (x, y), watermark)
                
                # 合并图层
                base = Image.alpha_composite(base, overlay)
            else:
                # 居中单个水印
                x = (base.width - watermark.width) // 2
                y = (base.height - watermark.height) // 2
                base.paste(watermark, (x, y), watermark)
            
            # 转回原始模式
            if base_image.mode != "RGBA":
                base = base.convert(base_image.mode)
            
            logger.info(f"图片水印添加成功: 透明度={opacity}, 平铺={tile}")
            return base
            
        except Exception as e:
            logger.error(f"图片水印添加失败: {str(e)}")
            raise 