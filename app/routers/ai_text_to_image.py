from fastapi import APIRouter, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional
import uuid
import os
from ..services.ai_text_to_image_service import AITextToImageService
from ..services.file_upload_service import file_upload_service
from ..utils.logger import logger
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..middleware.auth_middleware import get_current_api_token

class AITextToImageByUrlRequest(BaseModel):
    """AI文字转图片URL请求模型"""
    text: str
    style: Optional[str] = "realistic"
    width: Optional[int] = 512
    height: Optional[int] = 512
    quality: Optional[int] = 90

router = APIRouter(
    tags=["ai_text_to_image"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/ai-text-to-image")
async def generate_ai_image(
    text: str = Form(...),
    style: Optional[str] = Form("realistic"),
    width: Optional[int] = Form(512),
    height: Optional[int] = Form(512),
    quality: Optional[int] = Form(90),
    api_token: str = Depends(get_current_api_token)
):
    """
    使用AI根据文本生成图片并上传到AIGC网盘
    """
    try:
        # 创建服务实例
        ai_service = AITextToImageService()

        # 生成AI图片
        image_url = await ai_service.generate_image(
            prompt=text,
            style=style,
            width=width,
            height=height,
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
            "quality": quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="ai_text_to_image",
            parameters=parameters,
            original_filename=None,
            content_type="image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="AI文本转图片生成并上传成功",
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

@router.post("/api/v1/ai-text-to-image-by-url")
async def generate_ai_image_by_url(
    request: AITextToImageByUrlRequest = Body(..., description="AI文字转图片URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    使用AI根据文本生成图片（URL方式）并上传到AIGC网盘
    """
    try:
        # 创建服务实例
        ai_service = AITextToImageService()

        # 生成AI图片
        image_url = await ai_service.generate_image(
            prompt=request.text,
            style=request.style,
            width=request.width,
            height=request.height,
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
            "quality": request.quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="ai_text_to_image",
            parameters=parameters,
            original_filename=None,
            content_type="image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="AI文本转图片生成并上传成功",
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

@router.get("/api/v1/ai-text-to-image/styles")
async def get_ai_styles():
    """获取可用的AI生成风格"""
    styles = [
        {
            "value": "realistic",
            "label": "真实风格",
            "description": "生成逼真的照片风格图片"
        },
        {
            "value": "anime",
            "label": "动漫风格",
            "description": "日式动漫插画风格"
        },
        {
            "value": "artistic",
            "label": "艺术风格",
            "description": "艺术绘画风格"
        },
        {
            "value": "cartoon",
            "label": "卡通风格",
            "description": "卡通插画风格"
        },
        {
            "value": "oil_painting",
            "label": "油画风格",
            "description": "传统油画艺术风格"
        },
        {
            "value": "watercolor",
            "label": "水彩风格",
            "description": "水彩画艺术风格"
        }
    ]
    
    return ApiResponse.success(
        message="获取AI生成风格列表成功",
        data={
            "styles": styles
        }
    )

@router.get("/presets")
async def get_prompt_presets():
    """获取预设的提示词模板"""
    presets = [
        {
            "name": "风景摄影",
            "prompt": "beautiful landscape, mountains, lake, sunset, professional photography, high quality, detailed",
            "negative_prompt": "blurry, low quality, distorted"
        },
        {
            "name": "人物肖像",
            "prompt": "portrait of a person, professional lighting, high quality, detailed face, beautiful",
            "negative_prompt": "blurry, distorted face, low quality, bad anatomy"
        },
        {
            "name": "动物摄影",
            "prompt": "cute animal, professional wildlife photography, natural lighting, high quality, detailed",
            "negative_prompt": "blurry, low quality, distorted"
        },
        {
            "name": "建筑设计",
            "prompt": "modern architecture, building design, clean lines, professional photography, high quality",
            "negative_prompt": "blurry, low quality, distorted perspective"
        },
        {
            "name": "科幻场景",
            "prompt": "futuristic sci-fi scene, high tech, cyberpunk, neon lights, detailed, high quality",
            "negative_prompt": "blurry, low quality, distorted"
        },
        {
            "name": "食物摄影",
            "prompt": "delicious food photography, professional lighting, appetizing, high quality, detailed",
            "negative_prompt": "blurry, unappetizing, low quality"
        }
    ]
    
    return {
        "status": "success",
        "presets": presets
    }