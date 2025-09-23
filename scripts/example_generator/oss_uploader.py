#!/usr/bin/env python3
"""
OSS上传器模块
负责将文件上传到阿里云OSS
"""

from pathlib import Path
from typing import Optional, Dict


class OSSUploader:
    """OSS上传器类"""
    
    def __init__(self, oss_client):
        """
        初始化OSS上传器
        
        Args:
            oss_client: OSS客户端实例
        """
        self.oss_client = oss_client
        self.oss_urls: Dict[str, str] = {}
    
    def upload_to_oss(self, file_path: Path, object_key: str) -> Optional[str]:
        """
        上传文件到OSS
        
        Args:
            file_path: 本地文件路径
            object_key: OSS对象键
            
        Returns:
            上传成功返回URL，失败返回None
        """
        try:
            url = self.oss_client.upload_file(str(file_path), object_key)
            if url:
                self.oss_urls[object_key] = url
                return url
            return None
        except Exception as e:
            print(f"✗ 上传到OSS失败: {e}")
            return None
    
    def get_uploaded_urls(self) -> Dict[str, str]:
        """获取已上传的URL映射"""
        return self.oss_urls.copy()
    
    def check_oss_connection(self) -> bool:
        """
        检查OSS连接
        
        Returns:
            连接成功返回True，失败返回False
        """
        try:
            buckets = self.oss_client.list_buckets()
            print(f"✓ OSS连接成功，目标存储桶: {self.oss_client.bucket_name}")
            return True
        except Exception as e:
            print(f"✗ OSS连接失败: {e}")
            return False
