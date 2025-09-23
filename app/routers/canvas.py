from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.canvas_service import CanvasService
from ..services.file_upload_service import file_upload_service
from ..utils.image_utils import ImageUtils
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..middleware.auth_middleware import get_current_api_token
from typing import Optional
from pydantic import BaseModel

class CanvasByUrlRequest(BaseModel):
    """画布处理URL请求模型"""
    image_url: str
    canvas_type: str
    background_color: Optional[str] = "#FFFFFF"
    border_width: Optional[int] = 0
    border_color: Optional[str] = "#000000"
    padding: Optional[int] = 0
    quality: Optional[int] = 90

router = APIRouter(
    tags=["canvas"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/canvas")
async def process_canvas(
    file: UploadFile = File(...),
    canvas_type: str = Form(...),
    background_color: Optional[str] = Form("#FFFFFF"),
    border_width: Optional[int] = Form(0),
    border_color: Optional[str] = Form("#000000"),
    padding: Optional[int] = Form(0),
    quality: Optional[int] = Form(90),
    api_token: str = Depends(get_current_api_token)
):
    """
    为图片添加画布效果并上传到AIGC网盘
    """
    try:
        contents = await file.read()
        result_bytes = CanvasService.process_canvas(
            image_bytes=contents,
            canvas_type=canvas_type,
            background_color=background_color,
            border_width=border_width,
            border_color=border_color,
            padding=padding,
            quality=quality,
        )

        # 准备上传参数
        parameters = {
            "canvas_type": canvas_type,
            "background_color": background_color,
            "border_width": border_width,
            "border_color": border_color,
            "padding": padding,
            "quality": quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="canvas",
            parameters=parameters,
            original_filename=file.filename,
            content_type=file.content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="画布处理并上传成功",
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

@router.post("/api/v1/canvas-by-url")
async def process_canvas_by_url(
    request: CanvasByUrlRequest = Body(..., description="画布处理URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    为URL图片添加画布效果并上传到AIGC网盘
    """
    try:
        # 处理相对路径，转换为完整URL
        if request.image_url.startswith('/'):
            # 相对路径，转换为本地文件路径
            import os
            file_path = os.path.join(os.getcwd(), "frontend/public" + request.image_url)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    contents = f.read()
                content_type = "image/jpeg"  # 默认类型
            else:
                raise HTTPException(status_code=404, detail=f"本地文件不存在: {file_path}")
        else:
            # 完整URL，下载图片
            contents, content_type = await ImageUtils.download_image_from_url(request.image_url)

        result_bytes = CanvasService.process_canvas(
            image_bytes=contents,
            canvas_type=request.canvas_type,
            background_color=request.background_color,
            border_width=request.border_width,
            border_color=request.border_color,
            padding=request.padding,
            quality=request.quality,
        )

        # 准备上传参数
        parameters = {
            "canvas_type": request.canvas_type,
            "background_color": request.background_color,
            "border_width": request.border_width,
            "border_color": request.border_color,
            "padding": request.padding,
            "quality": request.quality,
            "source_url": request.image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="canvas",
            parameters=parameters,
            original_filename=None,
            content_type=content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL图片画布处理并上传成功",
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