import httpx
import io
from typing import Optional, Dict, Any
from ..utils.logger import logger


class AIGCStorageClient:
    """AIGC网盘服务客户端"""
    
    def __init__(self, base_url: str = "https://aigc-network-disk.aigchub.vip"):
        self.base_url = base_url
        self.timeout = 30
    
    async def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
        api_token: str,
        description: str = "",
        category_id: str = "1",
        tags: str = "",
        content_type: str = "image/jpeg"
    ) -> Optional[Dict[str, Any]]:
        """
        上传文件到AIGC网盘
        
        Args:
            file_bytes: 文件字节数据
            filename: 文件名
            api_token: 用户API token
            description: 文件描述
            category_id: 分类ID，默认为"1"（图片分类）
            tags: 标签，多个标签用逗号分隔
            content_type: 文件MIME类型
            
        Returns:
            上传成功时返回网盘API响应数据，失败时返回None
        """
        logger.info(f"开始上传文件到AIGC网盘: {filename}, 大小: {len(file_bytes)} bytes")
        
        try:
            url = f"{self.base_url}/api/files/upload"
            
            # 准备请求头
            headers = {
                "Authorization": api_token
            }
            
            # 准备multipart/form-data数据
            files = {
                "file": (filename, io.BytesIO(file_bytes), content_type)
            }
            
            data = {
                "description": description,
                "category_id": category_id,
                "tags": tags
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    headers=headers,
                    files=files,
                    data=data
                )
            
            if response.status_code != 200:
                logger.error(f"文件上传失败: HTTP {response.status_code} - {response.text}")
                return None
            
            response_data = response.json()
            
            if response_data.get("code") != 200:
                logger.error(f"文件上传失败: {response_data.get('detail', '未知错误')}")
                return None
            
            logger.info(f"文件上传成功: {response_data.get('file', {}).get('url', 'N/A')}")
            return response_data
            
        except httpx.TimeoutException:
            logger.error(f"文件上传超时: {filename}")
            return None
        except httpx.RequestError as e:
            logger.error(f"文件上传请求失败: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"文件上传异常: {str(e)}")
            return None
    
    def extract_file_url(self, upload_response: Dict[str, Any]) -> Optional[str]:
        """
        从上传响应中提取文件URL
        
        Args:
            upload_response: 上传API的响应数据
            
        Returns:
            文件URL，如果提取失败返回None
        """
        try:
            return upload_response.get("file", {}).get("url")
        except Exception as e:
            logger.error(f"提取文件URL失败: {str(e)}")
            return None
    
    def extract_preview_url(self, upload_response: Dict[str, Any]) -> Optional[str]:
        """
        从上传响应中提取预览URL
        
        Args:
            upload_response: 上传API的响应数据
            
        Returns:
            预览URL，如果提取失败返回None
        """
        try:
            return upload_response.get("file", {}).get("preview_url")
        except Exception as e:
            logger.error(f"提取预览URL失败: {str(e)}")
            return None


# 全局实例
aigc_storage_client = AIGCStorageClient()
