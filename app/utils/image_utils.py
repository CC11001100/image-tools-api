import requests
import io
from typing import Optional
from ..utils.logger import logger


class ImageUtils:
    """图片工具类"""
    
    @staticmethod
    def download_image_from_url(url: str, timeout: int = 30) -> tuple[bytes, str]:
        """
        从URL下载图片

        Args:
            url: 图片URL
            timeout: 超时时间（秒）

        Returns:
            (图片的字节数据, 内容类型)

        Raises:
            Exception: 下载失败时抛出异常
        """
        logger.info(f"开始从URL下载图片: {url}")

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()

            # 检查内容类型
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                raise ValueError(f"URL返回的不是图片类型: {content_type}")

            logger.info(f"成功下载图片，大小: {len(response.content)} bytes")
            return response.content, content_type

        except requests.exceptions.Timeout:
            logger.error(f"下载图片超时: {url}")
            raise Exception("下载图片超时")
        except requests.exceptions.RequestException as e:
            logger.error(f"下载图片失败: {e}")
            raise Exception(f"下载图片失败: {str(e)}")
        except Exception as e:
            logger.error(f"处理图片URL时出错: {e}")
            raise
    
    @staticmethod
    def validate_image_url(url: str) -> bool:
        """
        验证URL是否为有效的图片URL
        
        Args:
            url: 要验证的URL
            
        Returns:
            是否为有效的图片URL
        """
        if not url:
            return False
            
        # 基本URL格式验证
        if not url.startswith(('http://', 'https://')):
            return False
            
        # 检查常见的图片扩展名
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg')
        url_lower = url.lower()
        
        # 如果URL包含查询参数，先去掉
        url_path = url_lower.split('?')[0]
        
        # 检查是否以图片扩展名结尾
        if any(url_path.endswith(ext) for ext in image_extensions):
            return True
            
        # 对于没有扩展名的URL（如某些图片服务），返回True让后续下载时验证
        return True

    @staticmethod
    def get_filename_from_url(url: str) -> str:
        """
        从URL中提取文件名

        Args:
            url: 图片URL

        Returns:
            提取的文件名，如果无法提取则返回默认名称
        """
        try:
            # 移除查询参数
            url_path = url.split('?')[0]

            # 提取文件名
            filename = url_path.split('/')[-1]

            # 如果没有文件名或文件名为空，返回默认名称
            if not filename or filename == '':
                return "image.jpg"

            # 如果文件名没有扩展名，添加默认扩展名
            if '.' not in filename:
                filename += ".jpg"

            return filename

        except Exception as e:
            logger.error(f"从URL提取文件名失败: {e}")
            return "image.jpg"