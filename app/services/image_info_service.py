"""图片信息提取服务"""
from PIL import Image
from PIL.ExifTags import TAGS
from typing import Dict, Any, Optional, Tuple
import io
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import logger


class ImageInfoService:
    """图片信息提取服务类"""
    
    @staticmethod
    def get_image_info(image: Image.Image, original_bytes: Optional[bytes] = None) -> Dict[str, Any]:
        """
        获取图片的详细信息
        
        Args:
            image: PIL Image对象
            original_bytes: 原始图片字节数据（用于计算文件大小）
            
        Returns:
            包含图片详细信息的字典
        """
        try:
            logger.info(f"开始提取图片信息: 格式={image.format}, 尺寸={image.size}")
            
            # 基础信息
            info = {
                "format": image.format or "Unknown",
                "width": image.width,
                "height": image.height,
                "mode": image.mode,
                "size_bytes": len(original_bytes) if original_bytes else 0,
            }
            
            # DPI信息
            dpi = image.info.get('dpi')
            if dpi:
                info["dpi"] = list(dpi) if isinstance(dpi, tuple) else dpi
            else:
                info["dpi"] = None
            
            # 透明通道检测
            info["has_alpha"] = ImageInfoService._has_alpha_channel(image)
            
            # 颜色空间
            info["color_space"] = ImageInfoService._get_color_space(image)
            
            # GIF特殊信息
            if image.format == "GIF":
                gif_info = ImageInfoService._get_gif_info(image)
                info.update(gif_info)
            else:
                info["frame_count"] = 1
                info["is_animated"] = False
            
            # EXIF信息 - 暂时禁用以避免序列化问题
            # exif_data = ImageInfoService._get_exif_info(image)
            # if exif_data:
            #     info["exif"] = exif_data
            # else:
            info["exif"] = None
            
            # ICC配置文件
            icc_profile = image.info.get('icc_profile')
            if icc_profile:
                info["icc_profile"] = {
                    "present": True,
                    "size_bytes": len(icc_profile)
                }
            else:
                info["icc_profile"] = None
            
            # 额外信息
            info["aspect_ratio"] = round(image.width / image.height, 2) if image.height > 0 else 0
            info["megapixels"] = round((image.width * image.height) / 1000000, 2)
            
            # 格式化文件大小（人类可读）
            if info["size_bytes"] > 0:
                info["size_formatted"] = ImageInfoService._format_bytes(info["size_bytes"])
            else:
                info["size_formatted"] = "Unknown"
            
            logger.info(f"图片信息提取成功: {info['format']} {info['width']}x{info['height']}")
            return info
            
        except Exception as e:
            logger.error(f"提取图片信息失败: {str(e)}")
            raise
    
    @staticmethod
    def _has_alpha_channel(image: Image.Image) -> bool:
        """检测图片是否有透明通道"""
        return image.mode in ('RGBA', 'LA', 'PA') or (
            image.mode == 'P' and 'transparency' in image.info
        )
    
    @staticmethod
    def _get_color_space(image: Image.Image) -> str:
        """获取颜色空间信息"""
        mode_map = {
            '1': 'Binary (1-bit)',
            'L': 'Grayscale (8-bit)',
            'P': 'Palette (8-bit)',
            'RGB': 'RGB (24-bit)',
            'RGBA': 'RGBA (32-bit)',
            'CMYK': 'CMYK',
            'YCbCr': 'YCbCr',
            'LAB': 'LAB',
            'HSV': 'HSV',
            'LA': 'Grayscale + Alpha',
            'PA': 'Palette + Alpha',
            'I': 'Integer (32-bit)',
            'F': 'Float (32-bit)',
        }
        return mode_map.get(image.mode, image.mode)
    
    @staticmethod
    def _get_gif_info(image: Image.Image) -> Dict[str, Any]:
        """获取GIF特殊信息"""
        gif_info = {
            "frame_count": 1,
            "is_animated": False,
            "duration": None,
            "loop": None
        }
        
        try:
            # 计算帧数
            frame_count = 0
            while True:
                try:
                    image.seek(frame_count)
                    frame_count += 1
                except EOFError:
                    break
            
            gif_info["frame_count"] = frame_count
            gif_info["is_animated"] = frame_count > 1
            
            # 重置到第一帧
            image.seek(0)
            
            # 获取持续时间（第一帧）
            duration = image.info.get('duration')
            if duration:
                gif_info["duration"] = duration
            
            # 获取循环次数
            loop = image.info.get('loop')
            if loop is not None:
                gif_info["loop"] = loop
            
        except Exception as e:
            logger.warning(f"获取GIF信息时出错: {str(e)}")
        
        return gif_info
    
    @staticmethod
    def _get_exif_info(image: Image.Image) -> Optional[Dict[str, Any]]:
        """提取EXIF信息"""
        try:
            exif_data = image.getexif()
            if not exif_data:
                return None
            
            exif_dict = {}
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                
                # 转换值为可JSON序列化的格式
                try:
                    # 尝试JSON序列化测试
                    import json
                    
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8', errors='ignore')
                        except:
                            value = f"<bytes: {len(value)} bytes>"
                    elif isinstance(value, (tuple, list)):
                        # 递归处理列表/元组中的每个元素
                        value = [str(item) if not isinstance(item, (int, float, str, bool, type(None))) else item for item in value]
                    elif not isinstance(value, (int, float, str, bool, type(None))):
                        # 其他类型统一转字符串
                        value = str(value)
                    
                    # 验证是否可序列化
                    json.dumps(value)
                    exif_dict[str(tag)] = value
                    
                except Exception as e:
                    # 跳过无法处理的字段
                    logger.debug(f"跳过EXIF字段 {tag}: {str(e)}")
                    continue
            
            return exif_dict if exif_dict else None
            
        except Exception as e:
            logger.warning(f"提取EXIF信息时出错: {str(e)}")
            return None
    
    @staticmethod
    def _format_bytes(size_bytes: int) -> str:
        """格式化字节大小为人类可读格式"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
