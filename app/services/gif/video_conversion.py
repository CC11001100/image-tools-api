"""GIF视频转换功能"""
from typing import Optional
import tempfile
import os
import subprocess
from app.utils.logger import logger


class VideoConversion:
    """GIF视频转换功能"""
    
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
        """
        将视频转换为GIF
        
        Args:
            video_bytes: 视频字节数据
            fps: 目标帧率
            width: 目标宽度（None表示保持原始比例）
            height: 目标高度（None表示保持原始比例）
            start_time: 开始时间（秒）
            duration: 持续时间（秒，None表示到结尾）
            quality: 质量（1-100）
            
        Returns:
            GIF字节数据
        """
        logger.info(f"视频转GIF: FPS={fps}, 尺寸={width}x{height}, 开始时间={start_time}s, 持续时间={duration}s")
        
        temp_video_path = None
        temp_gif_path = None
        
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_video:
                temp_video.write(video_bytes)
                temp_video_path = temp_video.name
            
            with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as temp_gif:
                temp_gif_path = temp_gif.name
            
            # 构建基础ffmpeg命令
            cmd = ['ffmpeg', '-i', temp_video_path]
            
            # 添加开始时间
            if start_time > 0:
                cmd.extend(['-ss', str(start_time)])
            
            # 添加持续时间
            if duration:
                cmd.extend(['-t', str(duration)])
            
            # 构建视频滤镜
            filters = [f'fps={fps}']
            
            # 添加尺寸滤镜
            if width or height:
                if width and height:
                    filters.append(f'scale={width}:{height}')
                elif width:
                    filters.append(f'scale={width}:-1')
                else:
                    filters.append(f'scale=-1:{height}')
            
            # 应用滤镜
            cmd.extend(['-vf', ','.join(filters)])
            
            # 添加输出参数
            cmd.extend(['-y', temp_gif_path])
            
            # 执行ffmpeg命令
            logger.info(f"执行ffmpeg命令: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"ffmpeg错误: {result.stderr}")
                raise RuntimeError(f"视频转换失败: {result.stderr}")
            
            # 检查输出文件是否存在
            if not os.path.exists(temp_gif_path):
                raise RuntimeError("GIF文件生成失败")
            
            # 读取生成的GIF
            with open(temp_gif_path, 'rb') as f:
                gif_data = f.read()
            
            if len(gif_data) == 0:
                raise RuntimeError("生成的GIF文件为空")
            
            logger.info(f"成功将视频转换为GIF: {len(video_bytes)}字节 -> {len(gif_data)}字节")
            return gif_data
            
        except Exception as e:
            logger.error(f"视频转GIF失败: {str(e)}")
            raise
        finally:
            # 清理临时文件
            if temp_video_path and os.path.exists(temp_video_path):
                os.unlink(temp_video_path)
            if temp_gif_path and os.path.exists(temp_gif_path):
                os.unlink(temp_gif_path)
