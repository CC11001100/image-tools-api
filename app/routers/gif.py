"""GIF处理路由"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.gif_service import GifService
from ..services.file_upload_service import file_upload_service
from ..utils.image_utils import ImageUtils
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..middleware.auth_middleware import get_current_api_token
from typing import Optional
from pydantic import BaseModel

class GifByUrlRequest(BaseModel):
    """GIF处理URL请求模型"""
    image_url: str
    fps: Optional[int] = 10
    quality: Optional[int] = 90

class VideoToGifRequest(BaseModel):
    """视频转GIF请求模型"""
    video_url: str
    fps: Optional[int] = 10
    quality: Optional[int] = 90
    width: Optional[int] = None
    height: Optional[int] = None
    start_time: Optional[float] = 0
    duration: Optional[float] = None

router = APIRouter(
    tags=["gif"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/gif")
async def process_gif(
    file: UploadFile = File(...),
    fps: Optional[int] = Form(10),
    quality: Optional[int] = Form(90),
    width: Optional[int] = Form(None),
    height: Optional[int] = Form(None),
    api_token: str = Depends(get_current_api_token)
):
    """
    处理上传的GIF文件或视频文件并上传到AIGC网盘
    """

    try:
        contents = await file.read()

        # 检查文件类型
        content_type = file.content_type or ""
        filename = file.filename or ""

        # 检查是否为视频文件
        is_video = False

        # 通过content-type检查
        if any(video_type in content_type.lower() for video_type in ['video/', 'mp4', 'avi', 'mov', 'webm']):
            is_video = True

        # 通过文件扩展名检查
        if filename:
            ext = filename.lower().split('.')[-1]
            if ext in ['mp4', 'avi', 'mov', 'webm', 'mkv', 'flv']:
                is_video = True

        if is_video:
            # 视频转GIF
            result_bytes = GifService.video_to_gif(
                video_bytes=contents,
                fps=fps,
                quality=quality,
                width=width,
                height=height
            )
            operation_type = "video_to_gif"
        else:
            # GIF处理
            result_bytes = GifService.process_gif(
                gif_bytes=contents,
                fps=fps,
                quality=quality,
                width=width,
                height=height
            )
            operation_type = "gif_process"

        # 准备上传参数
        parameters = {
            "fps": fps,
            "quality": quality,
            "width": width,
            "height": height,
            "is_video": is_video
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type=operation_type,
            parameters=parameters,
            original_filename=file.filename,
            content_type="image/gif"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="GIF处理并上传成功",
            data={
                "file_info": file_info.dict(),
                "processing_info": parameters
            }
        )
    except Exception as e:
        return ApiResponse.error(
            message=str(e),
            code=500
        )

@router.post("/api/v1/gif-by-url")
async def process_gif_by_url(
    request: GifByUrlRequest = Body(..., description="GIF处理URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    处理URL GIF文件并上传到AIGC网盘
    """
    try:
        contents, content_type = await ImageUtils.download_image_from_url(request.image_url)
        result_bytes = GifService.process_gif(
            gif_bytes=contents,
            fps=request.fps,
            quality=request.quality,
        )

        # 准备上传参数
        parameters = {
            "fps": request.fps,
            "quality": request.quality,
            "source_url": request.image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="gif_process",
            parameters=parameters,
            original_filename=None,
            content_type="image/gif"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL GIF处理并上传成功",
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

@router.post("/api/v1/video-to-gif")
async def video_to_gif(
    request: VideoToGifRequest = Body(..., description="视频转GIF请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    将视频URL转换为GIF并上传到AIGC网盘
    """
    try:
        contents, content_type = await ImageUtils.download_image_from_url(request.video_url)
        result_bytes = GifService.video_to_gif(
            video_bytes=contents,
            fps=request.fps,
            quality=request.quality,
            width=request.width,
            height=request.height,
            start_time=request.start_time,
            duration=request.duration
        )

        # 准备上传参数
        parameters = {
            "fps": request.fps,
            "quality": request.quality,
            "width": request.width,
            "height": request.height,
            "start_time": request.start_time,
            "duration": request.duration,
            "source_url": request.video_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="video_to_gif",
            parameters=parameters,
            original_filename=None,
            content_type="image/gif"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="视频转GIF并上传成功",
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