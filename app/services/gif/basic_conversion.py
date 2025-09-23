"""GIF基础转换功能"""
from PIL import Image, ImageSequence
from typing import List, Tuple, Optional
import io
import numpy as np
from app.utils.logger import logger


class BasicConversion:
    """GIF基础转换功能"""
    
    @staticmethod
    def images_to_gif(
        images: List[Image.Image],
        duration: int = 500,
        loop: int = 0,
        optimize: bool = True
    ) -> bytes:
        """
        将图片列表转换为GIF动画
        
        Args:
            images: 图片列表
            duration: 每帧持续时间（毫秒）
            loop: 循环次数（0为无限循环）
            optimize: 是否优化
            
        Returns:
            GIF字节数据
        """
        logger.info(f"将{len(images)}张图片转换为GIF，持续时间: {duration}ms")
        
        try:
            if not images:
                raise ValueError("图片列表不能为空")
            
            # 确保所有图片尺寸一致
            first_size = images[0].size
            processed_images = []
            
            for i, img in enumerate(images):
                if img.size != first_size:
                    # 调整尺寸到第一张图片的大小
                    img = img.resize(first_size, Image.Resampling.LANCZOS)
                
                # 转换为RGB模式（GIF需要）
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                processed_images.append(img)
            
            # 创建GIF
            output = io.BytesIO()
            processed_images[0].save(
                output,
                format='GIF',
                save_all=True,
                append_images=processed_images[1:],
                duration=duration,
                loop=loop,
                optimize=optimize
            )
            
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"图片转GIF失败: {str(e)}")
            raise
    
    @staticmethod
    def gif_to_images(gif_bytes: bytes) -> List[Image.Image]:
        """
        将GIF动画分解为图片列表
        
        Args:
            gif_bytes: GIF字节数据
            
        Returns:
            图片列表
        """
        logger.info("将GIF分解为图片序列")
        
        try:
            gif = Image.open(io.BytesIO(gif_bytes))
            
            if not getattr(gif, 'is_animated', False):
                # 静态图片，直接返回
                return [gif.copy()]
            
            frames = []
            for frame in ImageSequence.Iterator(gif):
                # 复制帧并转换为RGB
                frame_copy = frame.copy()
                if frame_copy.mode != 'RGB':
                    frame_copy = frame_copy.convert('RGB')
                frames.append(frame_copy)
            
            logger.info(f"成功提取{len(frames)}帧")
            return frames
            
        except Exception as e:
            logger.error(f"GIF分解失败: {str(e)}")
            raise
