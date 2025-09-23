# 水印路由模块化导出
from .text_watermark import router as text_watermark_router
from .image_watermark import router as image_watermark_router
from .models import WatermarkByUrlRequest, ImageWatermarkByUrlRequest, WatermarkImageByUrlRequest

__all__ = [
    'text_watermark_router',
    'image_watermark_router',
    'WatermarkByUrlRequest',
    'ImageWatermarkByUrlRequest', 
    'WatermarkImageByUrlRequest'
]
