from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import uuid
import os
from ..services.text_to_image_service import TextToImageService
from ..services.file_upload_service import file_upload_service
from ..utils.logger import logger
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..middleware.auth_middleware import get_current_api_token

class TextToImageByUrlRequest(BaseModel):
    """文字转图片URL请求模型"""
    text: str
    style: Optional[str] = "default"
    width: Optional[int] = 800
    height: Optional[int] = 600
    font_size: Optional[int] = 32
    font_color: Optional[str] = "#000000"
    background_color: Optional[str] = "#FFFFFF"
    quality: Optional[int] = 90

router = APIRouter(
    tags=["text_to_image"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/text-to-image")
async def generate_text_image(
    text: str = Form(...),
    style: Optional[str] = Form("default"),
    width: Optional[int] = Form(800),
    height: Optional[int] = Form(600),
    font_size: Optional[int] = Form(32),
    font_color: Optional[str] = Form("#000000"),
    background_color: Optional[str] = Form("#FFFFFF"),
    quality: Optional[int] = Form(90),
    api_token: str = Depends(get_current_api_token)
):
    """
    生成文字图片并上传到AIGC网盘
    """
    try:
        # 创建服务实例
        text_to_image_service = TextToImageService()

        # 生成文字图片
        image_url = await text_to_image_service.create_text_image(
            text=text,
            width=width,
            height=height,
            font_size=font_size,
            font_color=font_color,
            background_color=background_color,
        )

        # 读取生成的图片文件
        import os
        from PIL import Image
        import io

        # 从URL获取文件路径
        filename = image_url.split('/')[-1]
        filepath = os.path.join("public/generated", filename)

        # 读取图片并转换为字节
        with Image.open(filepath) as img:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=quality)
            result_bytes = img_byte_arr.getvalue()

        # 准备上传参数
        parameters = {
            "text": text,
            "style": style,
            "width": width,
            "height": height,
            "font_size": font_size,
            "font_color": font_color,
            "background_color": background_color,
            "quality": quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="text_to_image",
            parameters=parameters,
            original_filename=None,
            content_type="image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="文字图片生成并上传成功",
            data={
                "file": file_info.dict(),
                "processing_info": parameters
        
            }
        )
    except Exception as e:
        return ApiResponse.error(
            message=str(e),
            code=500
        )

@router.post("/api/v1/text-to-image-by-url")
async def generate_text_image_by_url(
    request: TextToImageByUrlRequest = Body(..., description="文字转图片URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    生成文字图片（URL方式）并上传到AIGC网盘
    """
    try:
        # 创建服务实例
        text_to_image_service = TextToImageService()

        # 生成文字图片
        image_url = await text_to_image_service.create_text_image(
            text=request.text,
            width=request.width,
            height=request.height,
            font_size=request.font_size,
            font_color=request.font_color,
            background_color=request.background_color,
        )

        # 读取生成的图片文件
        import os
        from PIL import Image
        import io

        # 从URL获取文件路径
        filename = image_url.split('/')[-1]
        filepath = os.path.join("public/generated", filename)

        # 读取图片并转换为字节
        with Image.open(filepath) as img:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=request.quality)
            result_bytes = img_byte_arr.getvalue()

        # 准备上传参数
        parameters = {
            "text": request.text,
            "style": request.style,
            "width": request.width,
            "height": request.height,
            "font_size": request.font_size,
            "font_color": request.font_color,
            "background_color": request.background_color,
            "quality": request.quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="text_to_image",
            parameters=parameters,
            original_filename=None,
            content_type="image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="文字图片生成并上传成功",
            data={
                "file": file_info.dict(),
                "processing_info": parameters
        
            }
        )
    except Exception as e:
        return ApiResponse.error(
            message=str(e),
            code=500
        )

@router.get("/presets")
async def get_background_presets():
    """获取预设的背景样式"""
    presets = [
        {
            "name": "经典白底黑字",
            "background_color": "#FFFFFF",
            "font_color": "#000000",
            "background_style": "solid"
        },
        {
            "name": "深色主题",
            "background_color": "#2C3E50",
            "font_color": "#FFFFFF",
            "background_style": "solid"
        },
        {
            "name": "温暖渐变",
            "background_style": "gradient",
            "gradient_start": "#FF6B6B",
            "gradient_end": "#FFE66D",
            "font_color": "#FFFFFF",
            "gradient_direction": "diagonal"
        },
        {
            "name": "海洋渐变",
            "background_style": "gradient",
            "gradient_start": "#4ECDC4",
            "gradient_end": "#44A08D",
            "font_color": "#FFFFFF",
            "gradient_direction": "vertical"
        },
        {
            "name": "紫色梦幻",
            "background_style": "gradient",
            "gradient_start": "#667eea",
            "gradient_end": "#764ba2",
            "font_color": "#FFFFFF",
            "gradient_direction": "horizontal"
        },
        {
            "name": "日落黄昏",
            "background_style": "gradient",
            "gradient_start": "#f093fb",
            "gradient_end": "#f5576c",
            "font_color": "#FFFFFF",
            "gradient_direction": "diagonal"
        },
        {
            "name": "森林绿意",
            "background_style": "gradient",
            "gradient_start": "#56ab2f",
            "gradient_end": "#a8e6cf",
            "font_color": "#FFFFFF",
            "gradient_direction": "vertical"
        },
        {
            "name": "商务蓝",
            "background_color": "#3498DB",
            "font_color": "#FFFFFF",
            "background_style": "solid"
        }
    ]
    
    return JSONResponse({
        "status": "success",
        "presets": presets
    })

@router.get("/fonts")
async def get_available_fonts():
    """获取可用的字体列表"""
    fonts = [
        "Arial",
        "Helvetica",
        "Times New Roman",
        "Georgia",
        "Verdana",
        "Tahoma",
        "Trebuchet MS",
        "Impact",
        "Comic Sans MS",
        "Courier New"
    ]
    
    return JSONResponse({
        "status": "success",
        "fonts": fonts
    })