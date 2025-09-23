from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from ..services.format_service import FormatService
from ..services.file_upload_service import file_upload_service
from ..utils.image_utils import ImageUtils
from ..schemas.response_models import ErrorResponse, ImageProcessResponse, FileInfo, ApiResponse
from ..middleware.auth_middleware import get_current_api_token
from typing import Optional
from pydantic import BaseModel

class FormatByUrlRequest(BaseModel):
    """格式转换URL请求模型"""
    image_url: str
    output_format: str
    quality: Optional[int] = 90

router = APIRouter(
    tags=["format"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/format")
async def convert_format(
    file: UploadFile = File(...),
    output_format: str = Form(...),
    quality: Optional[int] = Form(90),
    api_token: str = Depends(get_current_api_token)
):
    """
    转换上传图片的格式并上传到AIGC网盘
    """
    try:
        # 读取上传的文件
        contents = await file.read()

        # 处理图片
        result_bytes = FormatService.convert_format(
            image_bytes=contents,
            target_format=output_format,
            quality=quality,
        )

        # 准备上传参数
        parameters = {
            "output_format": output_format,
            "quality": quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="format",
            parameters=parameters,
            original_filename=file.filename,
            content_type=f"image/{output_format.lower()}"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="图片格式转换并上传成功",
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

@router.post("/api/v1/format-by-url")
async def convert_format_by_url(
    request: FormatByUrlRequest = Body(..., description="格式转换URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    转换URL图片的格式并上传到AIGC网盘
    """
    try:
        # 下载图片
        contents = ImageUtils.download_image_from_url(request.image_url)

        # 处理图片
        result_bytes = FormatService.convert_format(
            image_bytes=contents,
            target_format=request.output_format,
            quality=request.quality,
        )

        # 准备上传参数
        parameters = {
            "output_format": request.output_format,
            "quality": request.quality,
            "source_url": request.image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="format",
            parameters=parameters,
            original_filename=None,
            content_type=f"image/{request.output_format.lower()}"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL图片格式转换并上传成功",
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
