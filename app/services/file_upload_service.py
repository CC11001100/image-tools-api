import uuid
import os
from typing import Optional, Dict, Any, Tuple
from ..services.aigc_storage_client import aigc_storage_client
from ..services.oss_client import OSSClient
from ..config import config
from ..utils.logger import logger


class FileUploadService:
    """文件上传服务"""
    
    def __init__(self):
        self.storage_client = aigc_storage_client
        self.oss_client = OSSClient()
        self.default_category_id = config.AIGC_STORAGE_DEFAULT_CATEGORY_ID
        self.default_tags = config.AIGC_STORAGE_DEFAULT_TAGS
    
    def generate_filename(self, original_filename: Optional[str] = None, file_extension: str = "jpg") -> str:
        """
        生成唯一的文件名
        
        Args:
            original_filename: 原始文件名（可选）
            file_extension: 文件扩展名，不包含点号
            
        Returns:
            生成的唯一文件名
        """
        unique_id = uuid.uuid4().hex
        
        # 确保扩展名不包含点号
        if file_extension.startswith('.'):
            file_extension = file_extension[1:]
        
        return f"processed_{unique_id}.{file_extension}"
    
    def get_file_extension_from_content_type(self, content_type: str) -> str:
        """
        根据MIME类型获取文件扩展名
        
        Args:
            content_type: MIME类型
            
        Returns:
            文件扩展名（不包含点号）
        """
        content_type_map = {
            "image/jpeg": "jpg",
            "image/jpg": "jpg", 
            "image/png": "png",
            "image/gif": "gif",
            "image/bmp": "bmp",
            "image/webp": "webp",
            "image/tiff": "tiff",
            "image/svg+xml": "svg"
        }
        
        return content_type_map.get(content_type.lower(), "jpg")
    
    def generate_description(self, operation_type: str, parameters: Dict[str, Any] = None) -> str:
        """
        根据操作类型和参数生成文件描述
        
        Args:
            operation_type: 操作类型（如 "resize", "crop", "filter" 等）
            parameters: 操作参数
            
        Returns:
            生成的文件描述
        """
        if parameters is None:
            parameters = {}
        
        base_description = f"通过图片工具API进行{operation_type}处理的图片"
        
        # 根据不同操作类型添加具体描述
        if operation_type == "resize":
            width = parameters.get("width")
            height = parameters.get("height")
            if width and height:
                base_description += f"，调整尺寸为{width}x{height}"
            elif width:
                base_description += f"，调整宽度为{width}"
            elif height:
                base_description += f"，调整高度为{height}"
        
        elif operation_type == "crop":
            crop_type = parameters.get("crop_type")
            if crop_type:
                base_description += f"，裁剪类型：{crop_type}"
        
        elif operation_type == "format":
            output_format = parameters.get("output_format")
            if output_format:
                base_description += f"，转换为{output_format.upper()}格式"
        
        elif operation_type == "watermark":
            text = parameters.get("text")
            if text:
                base_description += f"，添加水印：{text}"
        
        elif operation_type == "filter":
            filter_type = parameters.get("filter_type")
            if filter_type:
                base_description += f"，应用滤镜：{filter_type}"
        
        return base_description
    
    def generate_tags(self, operation_type: str, parameters: Dict[str, Any] = None) -> str:
        """
        根据操作类型和参数生成标签
        
        Args:
            operation_type: 操作类型
            parameters: 操作参数
            
        Returns:
            生成的标签字符串（逗号分隔）
        """
        tags = [self.default_tags, operation_type]
        
        if parameters:
            # 添加特定参数作为标签
            if operation_type == "filter" and parameters.get("filter_type"):
                tags.append(parameters["filter_type"])
            elif operation_type == "format" and parameters.get("output_format"):
                tags.append(parameters["output_format"])
            elif operation_type == "crop" and parameters.get("crop_type"):
                tags.append(parameters["crop_type"])
        
        return ",".join(tags)
    
    async def upload_processed_image(
        self,
        image_bytes: bytes,
        api_token: str,
        operation_type: str,
        parameters: Dict[str, Any] = None,
        original_filename: Optional[str] = None,
        content_type: str = "image/jpeg"
    ) -> Optional[Dict[str, Any]]:
        """
        上传处理后的图片到网盘
        
        Args:
            image_bytes: 图片字节数据
            api_token: 用户API token
            operation_type: 操作类型
            parameters: 操作参数
            original_filename: 原始文件名
            content_type: 文件MIME类型
            
        Returns:
            上传成功时返回完整的网盘响应，失败时返回None
        """
        try:
            # 生成文件名
            file_extension = self.get_file_extension_from_content_type(content_type)
            filename = self.generate_filename(original_filename, file_extension)
            
            # 生成描述和标签
            description = self.generate_description(operation_type, parameters)
            tags = self.generate_tags(operation_type, parameters)
            
            logger.info(f"准备上传图片: {filename}, 操作类型: {operation_type}")
            

            # 首先尝试上传到AIGC网盘
            upload_response = await self.storage_client.upload_file(
                file_bytes=image_bytes,
                filename=filename,
                api_token=api_token,
                description=description,
                category_id=self.default_category_id,
                tags=tags,
                content_type=content_type
            )

            if upload_response:
                logger.info(f"AIGC网盘上传成功: {filename}")
                return upload_response

            # AIGC网盘上传失败，检查是否有OSS配置
            logger.warning(f"AIGC网盘上传失败，检查OSS备用上传: {filename}")

            # 检查OSS配置
            if hasattr(self.oss_client, 'access_key_id') and self.oss_client.access_key_id:
                # 生成OSS对象键
                oss_object_key = f"processed/{operation_type}/{filename}"

                # 上传到OSS
                oss_url = self.oss_client.upload_bytes(
                    file_bytes=image_bytes,
                    object_key=oss_object_key,
                    content_type=content_type
                )

                if oss_url:
                    logger.info(f"OSS备用上传成功: {filename} -> {oss_url}")

                    # 构造兼容AIGC网盘格式的响应
                    oss_response = {
                        "code": 200,
                        "message": "文件上传成功（OSS备用）",
                        "file": {
                            "id": f"oss_{uuid.uuid4().hex}",
                            "filename": filename,
                            "original_filename": original_filename or filename,
                            "file_size": len(image_bytes),
                            "content_type": content_type,
                            "file_url": oss_url,
                            "preview_url": oss_url,
                            "download_url": oss_url,
                            "description": description,
                            "tags": tags,
                            "upload_source": "oss_backup"
                        }
                    }
                    return oss_response
                else:
                    logger.error(f"OSS备用上传也失败: {filename}")
            else:
                logger.warning("OSS配置未设置，无法使用备用上传")

            # 所有上传方式都失败，返回None
            logger.error(f"所有上传方式都失败: {filename}")
            return None
                
        except Exception as e:
            logger.error(f"上传处理后图片时发生异常: {str(e)}")
            return None
    
    def extract_urls(self, upload_response: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
        """
        从上传响应中提取URL
        
        Args:
            upload_response: 网盘上传响应
            
        Returns:
            (文件URL, 预览URL) 的元组
        """
        file_url = self.storage_client.extract_file_url(upload_response)
        preview_url = self.storage_client.extract_preview_url(upload_response)
        return file_url, preview_url


# 全局实例
file_upload_service = FileUploadService()
