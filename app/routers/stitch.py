from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.stitch_service import StitchService
from ..services.file_upload_service import file_upload_service
from ..utils.image_utils import ImageUtils
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..middleware.auth_middleware import get_current_api_token
from typing import Optional, List
from pydantic import BaseModel

class StitchByUrlRequest(BaseModel):
    """图片拼接URL请求模型"""
    image_urls: List[str]
    direction: str
    spacing: Optional[int] = 0
    quality: Optional[int] = 90

router = APIRouter(
    tags=["stitch"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/stitch")
async def stitch_images(
    files: List[UploadFile] = File(...),
    direction: str = Form(...),
    spacing: Optional[int] = Form(0),
    quality: Optional[int] = Form(90),
    api_token: str = Depends(get_current_api_token)
):
    """
    拼接多张上传的图片并上传到AIGC网盘
    """

    try:
        contents = []
        filenames = []
        for file in files:
            content = await file.read()
            contents.append(content)
            filenames.append(file.filename)

        result_bytes = StitchService.stitch_images(
            image_bytes_list=contents,
            direction=direction,
            spacing=spacing,
            quality=quality,
        )

        # 准备上传参数
        parameters = {
            "direction": direction,
            "spacing": spacing,
            "quality": quality,
            "image_count": len(files),
            "filenames": filenames
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="stitch",
            parameters=parameters,
            original_filename=f"stitched_{len(files)}_images",
            content_type="image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="图片拼接处理并上传成功",
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

@router.post("/api/v1/stitch-by-url")
async def stitch_images_by_url(
    request: StitchByUrlRequest = Body(..., description="图片拼接URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    拼接多个URL图片并上传到AIGC网盘
    """
    try:
        contents = []
        for url in request.image_urls:
            content, _ = await ImageUtils.download_image_from_url(url)
            contents.append(content)

        result_bytes = StitchService.stitch_images(
            image_bytes_list=contents,
            direction=request.direction,
            spacing=request.spacing,
            quality=request.quality,
        )

        # 准备上传参数
        parameters = {
            "direction": request.direction,
            "spacing": request.spacing,
            "quality": request.quality,
            "image_count": len(request.image_urls),
            "image_urls": request.image_urls
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="stitch",
            parameters=parameters,
            original_filename=None,
            content_type="image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL图片拼接处理并上传成功",
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

class StitchByUrlTestRequest(BaseModel):
    """图片拼接URL测试请求模型（单图片）"""
    image_url: str
    direction: str = "horizontal"
    gap: Optional[int] = 0
    background_color: Optional[str] = "#ffffff"
    quality: Optional[int] = 90

@router.post("/api/v1/stitch-by-url-test")
async def stitch_images_by_url_test(
    request: StitchByUrlTestRequest = Body(..., description="图片拼接URL测试请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    拼接URL图片（测试端点）并上传到AIGC网盘
    为了演示拼接效果，将同一张图片拼接两次
    """
    try:
        # 处理相对路径，转换为完整URL
        image_url = request.image_url
        if image_url.startswith('/examples/'):
            image_url = f"http://localhost:58889{image_url}"

        # 下载图片
        content, _ = ImageUtils.download_image_from_url(image_url)

        # 为了演示拼接效果，将同一张图片拼接两次
        contents = [content, content]

        result_bytes = StitchService.stitch_images(
            image_bytes_list=contents,
            direction=request.direction,
            spacing=request.gap,
            quality=request.quality,
        )

        # 准备上传参数
        parameters = {
            "direction": request.direction,
            "spacing": request.gap,
            "quality": request.quality,
            "background_color": request.background_color,
            "source_url": image_url,
            "image_count": 2
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="stitch_test",
            parameters=parameters,
            original_filename=None,
            content_type="image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="测试版本图片拼接处理并上传成功",
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