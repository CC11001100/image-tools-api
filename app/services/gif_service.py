"""GIF处理服务 - 模块化版本"""
from PIL import Image
from typing import List, Tuple, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import logger
from .gif import (
    BasicConversion,
    Optimization,
    AnimationCreator,
    VideoConversion,
    ComprehensiveProcessor
)


class GifService:
    """GIF处理服务类 - 模块化版本"""
    
    @staticmethod
    def images_to_gif(
        images: List[Image.Image],
        duration: int = 500,
        loop: int = 0,
        optimize: bool = True
    ) -> bytes:
        """将图片列表转换为GIF动画"""
        return BasicConversion.images_to_gif(images, duration, loop, optimize)
    
    @staticmethod
    def gif_to_images(gif_bytes: bytes) -> List[Image.Image]:
        """将GIF动画分解为图片列表"""
        return BasicConversion.gif_to_images(gif_bytes)
    
    @staticmethod
    def optimize_gif(
        gif_bytes: bytes,
        max_colors: int = 128,
        resize_factor: float = 1.0,
        target_fps: Optional[int] = None
    ) -> bytes:
        """优化GIF文件大小"""
        return Optimization.optimize_gif(gif_bytes, max_colors, resize_factor, target_fps)
    
    @staticmethod
    def create_animated_text_gif(
        text: str,
        font_size: int = 48,
        width: int = 400,
        height: int = 200,
        bg_color: Tuple[int, int, int] = (255, 255, 255),
        text_color: Tuple[int, int, int] = (0, 0, 0),
        animation_type: str = "fade",
        duration: int = 100,
        frames: int = 10
    ) -> bytes:
        """创建动画文字GIF"""
        return AnimationCreator.create_animated_text_gif(
            text, font_size, width, height, bg_color, text_color,
            animation_type, duration, frames
        )
    
    @staticmethod
    def video_to_gif(
        video_bytes: bytes,
        fps: int = 10,
        width: Optional[int] = None,
        height: Optional[int] = None,
        start_time: float = 0,
        duration: Optional[float] = None,
        quality: int = 90
    ) -> bytes:
        """将视频转换为GIF"""
        return VideoConversion.video_to_gif(
            video_bytes, fps, width, height, start_time, duration, quality
        )
    
    @staticmethod
    def process_gif(
        gif_bytes: bytes,
        fps: Optional[int] = None,
        quality: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> bytes:
        """处理GIF文件（优化、调整帧率等）"""
        return ComprehensiveProcessor.process_gif(gif_bytes, fps, quality, width, height)
