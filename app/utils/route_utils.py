from functools import wraps
from fastapi import HTTPException, Form
from fastapi.responses import Response
from typing import Callable, Any, Dict
import inspect
from .image_utils import ImageUtils
from .logger import logger


def create_url_endpoint(original_handler: Callable) -> Callable:
    """
    为现有的图片处理端点创建一个URL版本
    
    Args:
        original_handler: 原始的处理函数
        
    Returns:
        处理URL输入的新函数
    """
    
    @wraps(original_handler)
    async def url_handler(
        image_url: str = Form(..., description="图片URL"),
        **kwargs
    ):
        """处理图片URL的端点"""
        try:
            # 验证URL
            if not ImageUtils.validate_image_url(image_url):
                raise HTTPException(status_code=400, detail="无效的图片URL")
            
            # 下载图片
            image_data = ImageUtils.download_image_from_url(image_url)
            
            # 创建一个模拟的UploadFile对象
            class FakeUploadFile:
                def __init__(self, content: bytes, filename: str = "image.jpg"):
                    self.content = content
                    self.filename = filename
                
                async def read(self):
                    return self.content
            
            # 获取原始函数的签名
            sig = inspect.signature(original_handler)
            params = sig.parameters
            
            # 构建新的参数
            new_kwargs = kwargs.copy()
            
            # 找到file参数的名称（可能是file或其他名称）
            file_param_name = None
            for param_name, param in params.items():
                if 'UploadFile' in str(param.annotation):
                    file_param_name = param_name
                    break
            
            if file_param_name:
                # 从URL中提取文件名
                filename = image_url.split('/')[-1].split('?')[0] or 'image.jpg'
                new_kwargs[file_param_name] = FakeUploadFile(image_data, filename)
            
            # 调用原始处理函数
            return await original_handler(**new_kwargs)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"处理图片URL时出错: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # 更新函数文档
    url_handler.__doc__ = f"{original_handler.__doc__} (URL版本)"
    
    return url_handler 