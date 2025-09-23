"""
阿里云OSS客户端
用于管理示例图片的云存储
"""

import oss2
import os
import io
from typing import Optional, List, Dict, Any
from ..utils.logger import logger
from ..config import config


class OSSClient:
    """阿里云OSS客户端"""
    
    def __init__(self):
        # OSS配置信息（从环境变量获取）
        self.access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID", "")
        self.access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "")
        self.endpoint = "oss-cn-beijing.aliyuncs.com"
        self.bucket_name = "aigchub-static"
        self.region = "cn-beijing"
        
        # 初始化OSS认证和bucket
        self.auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        self.bucket = oss2.Bucket(self.auth, self.endpoint, self.bucket_name)
        
        # 示例图片存储目录前缀
        self.examples_prefix = "image-tools-api/examples/"
        
    def list_buckets(self) -> List[str]:
        """列出所有存储桶"""
        try:
            service = oss2.Service(self.auth, self.endpoint)
            buckets = service.list_buckets()
            return [bucket.name for bucket in buckets.buckets]
        except Exception as e:
            logger.error(f"列出存储桶失败: {str(e)}")
            return []
    
    def upload_file(self, file_path: str, object_key: str, content_type: str = "image/jpeg") -> Optional[str]:
        """
        上传文件到OSS
        
        Args:
            file_path: 本地文件路径
            object_key: OSS对象键（文件在OSS中的路径）
            content_type: 文件MIME类型
            
        Returns:
            上传成功返回文件URL，失败返回None
        """
        try:
            # 添加示例图片前缀
            full_object_key = self.examples_prefix + object_key
            
            # 上传文件
            with open(file_path, 'rb') as f:
                result = self.bucket.put_object(
                    full_object_key, 
                    f,
                    headers={'Content-Type': content_type}
                )
            
            if result.status == 200:
                # 生成公网访问URL
                url = f"https://{self.bucket_name}.{self.endpoint}/{full_object_key}"
                logger.info(f"文件上传成功: {file_path} -> {url}")
                return url
            else:
                logger.error(f"文件上传失败: {file_path}, 状态码: {result.status}")
                return None
                
        except Exception as e:
            logger.error(f"上传文件异常: {file_path} - {str(e)}")
            return None
    
    def upload_bytes(self, file_bytes: bytes, object_key: str, content_type: str = "image/jpeg") -> Optional[str]:
        """
        上传字节数据到OSS
        
        Args:
            file_bytes: 文件字节数据
            object_key: OSS对象键
            content_type: 文件MIME类型
            
        Returns:
            上传成功返回文件URL，失败返回None
        """
        try:
            # 添加示例图片前缀
            full_object_key = self.examples_prefix + object_key
            
            # 上传字节数据
            result = self.bucket.put_object(
                full_object_key,
                io.BytesIO(file_bytes),
                headers={'Content-Type': content_type}
            )
            
            if result.status == 200:
                # 生成公网访问URL
                url = f"https://{self.bucket_name}.{self.endpoint}/{full_object_key}"
                logger.info(f"字节数据上传成功: {object_key} -> {url}")
                return url
            else:
                logger.error(f"字节数据上传失败: {object_key}, 状态码: {result.status}")
                return None
                
        except Exception as e:
            logger.error(f"上传字节数据异常: {object_key} - {str(e)}")
            return None
    
    def delete_file(self, object_key: str) -> bool:
        """
        删除OSS中的文件
        
        Args:
            object_key: OSS对象键
            
        Returns:
            删除成功返回True，失败返回False
        """
        try:
            # 添加示例图片前缀
            full_object_key = self.examples_prefix + object_key
            
            result = self.bucket.delete_object(full_object_key)
            if result.status == 204:
                logger.info(f"文件删除成功: {object_key}")
                return True
            else:
                logger.error(f"文件删除失败: {object_key}, 状态码: {result.status}")
                return False
                
        except Exception as e:
            logger.error(f"删除文件异常: {object_key} - {str(e)}")
            return False
    
    def file_exists(self, object_key: str) -> bool:
        """
        检查文件是否存在
        
        Args:
            object_key: OSS对象键
            
        Returns:
            文件存在返回True，不存在返回False
        """
        try:
            # 添加示例图片前缀
            full_object_key = self.examples_prefix + object_key
            
            return self.bucket.object_exists(full_object_key)
        except Exception as e:
            logger.error(f"检查文件存在异常: {object_key} - {str(e)}")
            return False
    
    def list_files(self, prefix: str = "") -> List[str]:
        """
        列出指定前缀的所有文件
        
        Args:
            prefix: 文件前缀
            
        Returns:
            文件列表
        """
        try:
            # 添加示例图片前缀
            full_prefix = self.examples_prefix + prefix
            
            files = []
            for obj in oss2.ObjectIterator(self.bucket, prefix=full_prefix):
                # 移除前缀，只返回相对路径
                relative_path = obj.key[len(self.examples_prefix):]
                files.append(relative_path)
            
            return files
        except Exception as e:
            logger.error(f"列出文件异常: {prefix} - {str(e)}")
            return []
    
    def get_file_url(self, object_key: str) -> str:
        """
        获取文件的公网访问URL
        
        Args:
            object_key: OSS对象键
            
        Returns:
            文件的公网访问URL
        """
        full_object_key = self.examples_prefix + object_key
        return f"https://{self.bucket_name}.{self.endpoint}/{full_object_key}"


# 全局实例
oss_client = OSSClient()
