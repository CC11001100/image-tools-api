from pydantic import BaseModel
from typing import Optional


class WatermarkByUrlRequest(BaseModel):
    """水印URL请求模型"""
    image_url: str
    watermark_text: str
    position: Optional[str] = "center"
    font_size: Optional[int] = 36
    font_color: Optional[str] = "#000000"
    font_family: Optional[str] = "Arial"
    opacity: Optional[float] = 0.5
    margin_x: Optional[int] = 20
    margin_y: Optional[int] = 20
    rotation: Optional[int] = 0
    stroke_width: Optional[int] = 0
    stroke_color: Optional[str] = "#000000"
    shadow_offset_x: Optional[int] = 0
    shadow_offset_y: Optional[int] = 0
    shadow_color: Optional[str] = "#000000"
    repeat_mode: Optional[str] = "none"  # none, tile, diagonal
    quality: Optional[int] = 90


class ImageWatermarkByUrlRequest(BaseModel):
    """图片水印URL请求模型"""
    image_url: str
    watermark_image_url: str
    position: Optional[str] = "center"
    opacity: Optional[float] = 0.5
    scale: Optional[float] = 1.0
    quality: Optional[int] = 90


class WatermarkImageByUrlRequest(BaseModel):
    """图片水印URL请求模型"""
    image_url: str
    watermark_image_url: str
    position: Optional[str] = "center"
    opacity: Optional[float] = 0.5
    scale: Optional[float] = 1.0
    quality: Optional[int] = 90
