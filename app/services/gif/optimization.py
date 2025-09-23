"""GIF优化处理功能"""
from PIL import Image, ImageSequence
from typing import Optional
import io
from app.utils.logger import logger


class Optimization:
    """GIF优化处理功能"""
    
    @staticmethod
    def optimize_gif(
        gif_bytes: bytes,
        max_colors: int = 128,
        resize_factor: float = 1.0,
        target_fps: Optional[int] = None
    ) -> bytes:
        """
        优化GIF文件大小
        
        Args:
            gif_bytes: 原始GIF字节数据
            max_colors: 最大颜色数
            resize_factor: 缩放比例
            target_fps: 目标帧率
            
        Returns:
            优化后的GIF字节数据
        """
        logger.info(f"优化GIF: 最大颜色数={max_colors}, 缩放比例={resize_factor}, 目标FPS={target_fps}")
        
        try:
            gif = Image.open(io.BytesIO(gif_bytes))
            frames = []
            durations = []
            
            # 获取原始帧信息
            original_duration = gif.info.get('duration', 100)
            
            # 处理每一帧
            frame_count = 0
            for i, frame in enumerate(ImageSequence.Iterator(gif)):
                # 如果设置了目标FPS，可能需要跳过一些帧
                if target_fps and i % (30 // target_fps) != 0:
                    continue
                
                # 缩放
                if resize_factor != 1.0:
                    new_size = (
                        int(frame.width * resize_factor),
                        int(frame.height * resize_factor)
                    )
                    frame = frame.resize(new_size, Image.Resampling.LANCZOS)
                
                # 减少颜色数
                if frame.mode != 'P':
                    frame = frame.convert('P', palette=Image.ADAPTIVE, colors=max_colors)
                else:
                    # 重新量化已经是P模式的图片
                    frame = frame.quantize(colors=max_colors)
                
                frames.append(frame)
                durations.append(frame.info.get('duration', original_duration))
                frame_count += 1
            
            if not frames:
                raise ValueError("优化后没有剩余帧")
            
            # 保存优化后的GIF
            output = io.BytesIO()
            frames[0].save(
                output,
                format='GIF',
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=gif.info.get('loop', 0),
                optimize=True
            )
            
            original_size = len(gif_bytes)
            optimized_size = output.tell()
            compression_ratio = (1 - optimized_size / original_size) * 100
            
            logger.info(
                f"GIF优化成功: {original_size}字节 -> {optimized_size}字节 "
                f"(压缩率{compression_ratio:.1f}%), {frame_count}帧"
            )
            
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"优化GIF失败: {str(e)}")
            raise
