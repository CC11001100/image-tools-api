"""统一文字路由"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.text_service import TextService
from ..services.file_upload_service import file_upload_service
from ..utils.image_utils import ImageUtils
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..middleware.auth_middleware import get_current_api_token
from typing import Optional
from pydantic import BaseModel

class TextByUrlRequest(BaseModel):
    """文字添加URL请求模型"""
    image_url: str
    text: str
    position: Optional[str] = "center"
    font_size: Optional[int] = 32
    font_color: Optional[str] = "#000000"
    background_color: Optional[str] = None
    quality: Optional[int] = 90

router = APIRouter(
    tags=["advanced_text"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/text")
async def add_text(
    file: UploadFile = File(...),
    text: str = Form(...),
    position: Optional[str] = Form("center"),
    font_size: Optional[int] = Form(32),
    font_color: Optional[str] = Form("#000000"),
    background_color: Optional[str] = Form(None),
    quality: Optional[int] = Form(90),
    api_token: str = Depends(get_current_api_token)
):
    """
    为上传的图片添加文字并上传到AIGC网盘
    """
    try:
        contents = await file.read()
        result_bytes = TextService.add_text(
            image_bytes=contents,
            text=text,
            position=position,
            font_size=font_size,
            font_color=font_color,
            background_color=background_color,
            quality=quality,
        )

        # 准备上传参数
        parameters = {
            "text": text,
            "position": position,
            "font_size": font_size,
            "font_color": font_color,
            "background_color": background_color,
            "quality": quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="advanced_text",
            parameters=parameters,
            original_filename=file.filename,
            content_type=file.content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="文字添加处理并上传成功",
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

@router.post("/api/v1/text-by-url")
async def add_text_by_url(
    request: TextByUrlRequest = Body(..., description="文字添加URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    为URL图片添加文字并上传到AIGC网盘
    """
    try:
        contents, content_type = await ImageUtils.download_image_from_url(request.image_url)
        result_bytes = TextService.add_text(
            image_bytes=contents,
            text=request.text,
            position=request.position,
            font_size=request.font_size,
            font_color=request.font_color,
            background_color=request.background_color,
            quality=request.quality,
        )

        # 准备上传参数
        parameters = {
            "text": request.text,
            "position": request.position,
            "font_size": request.font_size,
            "font_color": request.font_color,
            "background_color": request.background_color,
            "quality": request.quality,
            "source_url": request.image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="advanced_text",
            parameters=parameters,
            original_filename=None,
            content_type=content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL图片文字添加处理并上传成功",
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


# 临时测试路由 - 简化版本，不涉及认证和计费
@router.post("/api/v1/text-by-url-test")
async def add_text_by_url_test(
    request: TextByUrlRequest = Body(..., description="文字添加URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    为URL图片添加文字 - 测试版本，上传到AIGC网盘
    """
    try:
        # 处理相对路径URL
        image_url = request.image_url
        if image_url.startswith('/examples/'):
            # 转换为完整URL
            image_url = f"http://localhost:58889{image_url}"

        # 下载图片
        contents, content_type = ImageUtils.download_image_from_url(image_url)

        # 处理图片
        result_bytes = TextService.add_text(
            image_bytes=contents,
            text=request.text,
            position=request.position,
            font_size=request.font_size,
            font_color=request.font_color,
            background_color=request.background_color,
            quality=request.quality,
        )

        # 准备上传参数
        parameters = {
            "text": request.text,
            "position": request.position,
            "font_size": request.font_size,
            "font_color": request.font_color,
            "background_color": request.background_color,
            "quality": request.quality,
            "source_url": image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="advanced_text_test",
            parameters=parameters,
            original_filename=None,
            content_type=content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="测试版本文字添加处理并上传成功",
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