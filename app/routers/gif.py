"""GIF处理路由"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.gif_service import GifService
from ..services.file_upload_service import file_upload_service
from ..utils.image_utils import ImageUtils
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..middleware.auth_middleware import get_current_api_token
from typing import Optional, List
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

class CreateGifByUrlRequest(BaseModel):
    """图片合成GIF URL请求模型"""
    image_urls: List[str]
    duration: Optional[int] = 500
    loop: Optional[int] = 0
    quality: Optional[int] = 90
    optimize: Optional[bool] = True

class ExtractGifByUrlRequest(BaseModel):
    """GIF帧提取URL请求模型"""
    gif_url: str
    output_format: Optional[str] = "JPEG"
    quality: Optional[int] = 90
    start_frame: Optional[int] = 0
    end_frame: Optional[int] = None
    step: Optional[int] = 1

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
        contents, content_type = ImageUtils.download_image_from_url(request.image_url)
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
    file: UploadFile = File(...),
    fps: Optional[int] = Form(10),
    quality: Optional[int] = Form(90),
    width: Optional[int] = Form(None),
    height: Optional[int] = Form(None),
    start_time: Optional[float] = Form(0),
    duration: Optional[float] = Form(None),
    api_token: str = Depends(get_current_api_token)
):
    """
    将上传的视频文件转换为GIF并上传到AIGC网盘
    """
    try:
        contents = await file.read()
        result_bytes = GifService.video_to_gif(
            video_bytes=contents,
            fps=fps,
            quality=quality,
            width=width,
            height=height,
            start_time=start_time,
            duration=duration
        )

        # 准备上传参数
        parameters = {
            "fps": fps,
            "quality": quality,
            "width": width,
            "height": height,
            "start_time": start_time,
            "duration": duration
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="video_to_gif",
            parameters=parameters,
            original_filename=file.filename,
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

@router.post("/api/v1/video-to-gif-by-url")
async def video_to_gif_by_url(
    request: VideoToGifRequest = Body(..., description="视频转GIF请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    将视频URL转换为GIF并上传到AIGC网盘
    """
    try:
        contents, content_type = ImageUtils.download_image_from_url(request.video_url)
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

@router.post("/api/v1/create-gif")
async def create_gif_from_images(
    files: List[UploadFile] = File(..., description="要合成GIF的图片文件列表"),
    duration: Optional[int] = Form(500, description="每帧持续时间(毫秒)"),
    loop: Optional[int] = Form(0, description="循环次数(0为无限循环)"),
    quality: Optional[int] = Form(90, description="输出质量"),
    optimize: Optional[bool] = Form(True, description="是否优化"),
    api_token: str = Depends(get_current_api_token)
):
    """
    将多张图片合成为GIF动画并上传到AIGC网盘
    """
    try:
        if len(files) < 2:
            raise HTTPException(status_code=400, detail="至少需要2张图片才能创建GIF")
        
        # 读取所有图片
        images = []
        for file in files:
            contents = await file.read()
            image = ImageUtils.bytes_to_image(contents)
            images.append(image)
        
        # 创建GIF
        result_bytes = GifService.images_to_gif(
            images=images,
            duration=duration,
            loop=loop,
            optimize=optimize
        )
        
        # 准备上传参数
        parameters = {
            "duration": duration,
            "loop": loop,
            "quality": quality,
            "optimize": optimize,
            "frame_count": len(images)
        }
        
        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="create_gif",
            parameters=parameters,
            original_filename=f"created_gif_{len(images)}_frames.gif",
            content_type="image/gif"
        )
        
        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")
        
        # 构造响应
        file_info = FileInfo(**upload_response["file"])
        
        return ApiResponse.success(
            message="图片合成GIF并上传成功",
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

@router.post("/api/v1/create-gif-by-url")
async def create_gif_from_urls(
    request: CreateGifByUrlRequest = Body(..., description="图片合成GIF URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    从URL图片列表创建GIF动画并上传到AIGC网盘
    """
    try:
        if len(request.image_urls) < 2:
            raise HTTPException(status_code=400, detail="至少需要2张图片才能创建GIF")
        
        # 下载所有图片
        images = []
        for url in request.image_urls:
            contents, _ = ImageUtils.download_image_from_url(url)
            image = ImageUtils.bytes_to_image(contents)
            images.append(image)
        
        # 创建GIF
        result_bytes = GifService.images_to_gif(
            images=images,
            duration=request.duration,
            loop=request.loop,
            optimize=request.optimize
        )
        
        # 准备上传参数
        parameters = {
            "duration": request.duration,
            "loop": request.loop,
            "quality": request.quality,
            "optimize": request.optimize,
            "frame_count": len(images),
            "source_urls": request.image_urls
        }
        
        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="create_gif",
            parameters=parameters,
            original_filename=f"created_gif_{len(images)}_frames.gif",
            content_type="image/gif"
        )
        
        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")
        
        # 构造响应
        file_info = FileInfo(**upload_response["file"])
        
        return ApiResponse.success(
            message="URL图片合成GIF并上传成功",
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

@router.post("/api/v1/extract-gif")
async def extract_gif_frames(
    file: UploadFile = File(..., description="要提取帧的GIF文件"),
    output_format: Optional[str] = Form("JPEG", description="输出格式(JPEG/PNG)"),
    quality: Optional[int] = Form(90, description="输出质量"),
    start_frame: Optional[int] = Form(0, description="起始帧索引"),
    end_frame: Optional[int] = Form(None, description="结束帧索引"),
    step: Optional[int] = Form(1, description="帧间隔"),
    api_token: str = Depends(get_current_api_token)
):
    """
    从GIF文件中提取帧图片并上传到AIGC网盘
    """
    try:
        contents = await file.read()
        
        # 提取GIF帧
        frames = GifService.gif_to_images(contents)
        
        if not frames:
            raise HTTPException(status_code=400, detail="GIF文件中没有找到有效帧")
        
        # 应用帧范围和步长
        total_frames = len(frames)
        end_frame = end_frame if end_frame is not None else total_frames
        end_frame = min(end_frame, total_frames)
        
        selected_frames = frames[start_frame:end_frame:step]
        
        if not selected_frames:
            raise HTTPException(status_code=400, detail="根据指定参数没有提取到任何帧")
        
        # 转换帧为字节数据
        frame_files = []
        for i, frame in enumerate(selected_frames):
            frame_bytes = ImageUtils.image_to_bytes(frame, format=output_format, quality=quality)
            frame_files.append({
                "data": frame_bytes,
                "filename": f"frame_{start_frame + i * step:04d}.{output_format.lower()}",
                "content_type": f"image/{output_format.lower()}"
            })
        
        # 准备上传参数
        parameters = {
            "output_format": output_format,
            "quality": quality,
            "start_frame": start_frame,
            "end_frame": end_frame,
            "step": step,
            "total_frames": total_frames,
            "extracted_frames": len(selected_frames)
        }
        
        # 批量上传帧图片
        uploaded_files = []
        for frame_file in frame_files:
            upload_response = await file_upload_service.upload_processed_image(
                image_bytes=frame_file["data"],
                api_token=api_token,
                operation_type="extract_gif",
                parameters=parameters,
                original_filename=frame_file["filename"],
                content_type=frame_file["content_type"]
            )
            
            if upload_response:
                uploaded_files.append(FileInfo(**upload_response["file"]))
        
        if not uploaded_files:
            raise HTTPException(status_code=500, detail="帧图片上传到网盘失败")
        
        return ApiResponse.success(
            message=f"GIF帧提取并上传成功，共提取{len(uploaded_files)}帧",
            data={
                "files": [file.dict() for file in uploaded_files],
                "processing_info": parameters
            }
        )
    except Exception as e:
        return ApiResponse.error(
            message=str(e),
            code=500
        )

@router.post("/api/v1/extract-gif-by-url")
async def extract_gif_frames_by_url(
    request: ExtractGifByUrlRequest = Body(..., description="GIF帧提取URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    从URL GIF文件中提取帧图片并上传到AIGC网盘
    """
    try:
        # 下载GIF文件
        contents, _ = ImageUtils.download_image_from_url(request.gif_url)
        
        # 提取GIF帧
        frames = GifService.gif_to_images(contents)
        
        if not frames:
            raise HTTPException(status_code=400, detail="GIF文件中没有找到有效帧")
        
        # 应用帧范围和步长
        total_frames = len(frames)
        end_frame = request.end_frame if request.end_frame is not None else total_frames
        end_frame = min(end_frame, total_frames)
        
        selected_frames = frames[request.start_frame:end_frame:request.step]
        
        if not selected_frames:
            raise HTTPException(status_code=400, detail="根据指定参数没有提取到任何帧")
        
        # 转换帧为字节数据
        frame_files = []
        for i, frame in enumerate(selected_frames):
            frame_bytes = ImageUtils.image_to_bytes(frame, format=request.output_format, quality=request.quality)
            frame_files.append({
                "data": frame_bytes,
                "filename": f"frame_{request.start_frame + i * request.step:04d}.{request.output_format.lower()}",
                "content_type": f"image/{request.output_format.lower()}"
            })
        
        # 准备上传参数
        parameters = {
            "output_format": request.output_format,
            "quality": request.quality,
            "start_frame": request.start_frame,
            "end_frame": end_frame,
            "step": request.step,
            "total_frames": total_frames,
            "extracted_frames": len(selected_frames),
            "source_url": request.gif_url
        }
        
        # 批量上传帧图片
        uploaded_files = []
        for frame_file in frame_files:
            upload_response = await file_upload_service.upload_processed_image(
                image_bytes=frame_file["data"],
                api_token=api_token,
                operation_type="extract_gif",
                parameters=parameters,
                original_filename=frame_file["filename"],
                content_type=frame_file["content_type"]
            )
            
            if upload_response:
                uploaded_files.append(FileInfo(**upload_response["file"]))
        
        if not uploaded_files:
            raise HTTPException(status_code=500, detail="帧图片上传到网盘失败")
        
        return ApiResponse.success(
            message=f"URL GIF帧提取并上传成功，共提取{len(uploaded_files)}帧",
            data={
                "files": [file.dict() for file in uploaded_files],
                "processing_info": parameters
            }
        )
    except Exception as e:
        return ApiResponse.error(
            message=str(e),
            code=500
        )