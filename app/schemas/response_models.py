from pydantic import BaseModel
from typing import Optional, Dict, Any, Union
from datetime import datetime


class FileInfo(BaseModel):
    """文件信息模型"""
    id: int
    filename: str
    original_name: str
    file_size: int
    file_type: str
    url: str
    preview_url: str
    description: str
    upload_time: datetime


class ImageProcessResponse(BaseModel):
    """图像处理响应模型"""
    success: bool = True
    message: str
    file: FileInfo
    processing_info: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """错误响应模型"""
    success: bool = False
    error: str
    detail: Optional[str] = None


# 统一API响应格式辅助类
class ApiResponse:
    """
    统一API响应格式辅助类
    提供标准的成功和错误响应格式：
    成功: {"code": 200, "message": "xxx", "data": {...}}
    失败: {"code": 4xx/5xx, "message": "xxx", "data": null}
    """

    @staticmethod
    def success(message: str, data: Any = None, code: int = 200) -> Dict[str, Any]:
        """
        生成成功响应

        Args:
            message: 成功消息
            data: 响应数据，默认为None
            code: HTTP状态码，默认为200

        Returns:
            统一格式的成功响应字典
        """
        return {
            "code": code,
            "message": message,
            "data": data
        }

    @staticmethod
    def error(message: str, code: int = 400, data: Any = None) -> Dict[str, Any]:
        """
        生成错误响应

        Args:
            message: 错误消息
            code: HTTP状态码，默认为400
            data: 错误相关数据，默认为None

        Returns:
            统一格式的错误响应字典
        """
        return {
            "code": code,
            "message": message,
            "data": data
        }


# 保持向后兼容
class ImageResponse(BaseModel):
    """通用图像处理响应模型（已废弃，使用ImageProcessResponse）"""
    success: bool
    message: str
    image_url: Optional[str] = None