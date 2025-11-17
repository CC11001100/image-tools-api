import requests
import io
from typing import Optional
from PIL import Image
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
    
    @staticmethod
    def bytes_to_image(image_bytes: bytes) -> Image.Image:
        """
        将字节数据转换为PIL Image对象
        
        Args:
            image_bytes: 图片的字节数据
            
        Returns:
            PIL Image对象
        """
        try:
            return Image.open(io.BytesIO(image_bytes))
        except Exception as e:
            logger.error(f"字节数据转换为图片失败: {e}")
            raise Exception(f"无效的图片数据: {str(e)}")
    
    @staticmethod
    def image_to_bytes(image: Image.Image, format: str = "JPEG", quality: int = 95) -> bytes:
        """
        将PIL Image对象转换为字节数据
        
        Args:
            image: PIL Image对象
            format: 输出格式 (JPEG, PNG等)
            quality: 质量 (1-100, 仅对JPEG有效)
            
        Returns:
            图片的字节数据
        """
        output = None
        try:
            # 检查图片对象是否有效
            if image is None:
                raise ValueError("图片对象为空")
            
            # 检查图片尺寸是否合理（防止内存溢出）
            width, height = image.size
            if width <= 0 or height <= 0:
                raise ValueError(f"图片尺寸无效: {width}x{height}")
            
            # 计算图片占用内存大小（估算）
            estimated_size = width * height * 4  # 假设RGBA
            if estimated_size > 500 * 1024 * 1024:  # 超过500MB
                logger.warning(f"图片尺寸过大: {width}x{height}, 估算内存: {estimated_size/1024/1024:.2f}MB")
            
            output = io.BytesIO()
            format = format.upper()
            
            if format == "JPEG":
                # 确保图片是RGB模式（JPEG不支持透明度）
                if image.mode in ("RGBA", "P", "LA"):
                    logger.info(f"转换图片模式从 {image.mode} 到 RGB")
                    # 创建白色背景
                    background = Image.new("RGB", image.size, (255, 255, 255))
                    if image.mode == "P":
                        image = image.convert("RGBA")
                    background.paste(image, mask=image.split()[-1] if image.mode in ("RGBA", "LA") else None)
                    image = background
                elif image.mode != "RGB":
                    image = image.convert("RGB")
                
                # 限制质量参数范围
                quality = max(1, min(100, quality))
                
                # 保存图片
                image.save(output, format="JPEG", quality=quality, optimize=True, progressive=True)
            elif format == "PNG":
                image.save(output, format="PNG", optimize=True)
            elif format == "WEBP":
                image.save(output, format="WEBP", quality=quality if quality < 100 else None, lossless=quality == 100)
            else:
                image.save(output, format=format)
            
            # 获取结果
            result = output.getvalue()
            
            # 检查结果是否有效
            if not result:
                raise ValueError("图片转换结果为空")
            
            logger.debug(f"图片转换成功: {format}, 质量: {quality}, 输出大小: {len(result)} bytes")
            return result
            
        except OSError as e:
            error_msg = f"图片保存I/O错误: {str(e)}"
            logger.error(error_msg)
            # 尝试降低质量重试一次
            if format == "JPEG" and quality > 50:
                logger.info("尝试降低质量重试...")
                try:
                    if output:
                        output.close()
                    return ImageUtils.image_to_bytes(image, format, quality=50)
                except Exception:
                    pass
            raise Exception(error_msg)
        except MemoryError as e:
            error_msg = f"图片处理内存不足: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"图片转换为字节数据失败: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        finally:
            # 确保释放资源
            if output:
                try:
                    output.close()
                except Exception:
                    pass