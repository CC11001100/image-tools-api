from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.perspective_service import PerspectiveService
from ..services.file_upload_service import file_upload_service
from ..utils.image_utils import ImageUtils
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..middleware.auth_middleware import get_current_api_token
from typing import Optional
from pydantic import BaseModel

class PerspectiveByUrlRequest(BaseModel):
    """透视修正URL请求模型"""
    image_url: str
    points: Optional[str] = None
    auto_document: Optional[bool] = False
    quality: Optional[int] = 90

router = APIRouter(
    tags=["perspective"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/perspective")
async def correct_perspective(
    file: UploadFile = File(...),
    points: Optional[str] = Form(None),
    auto_document: Optional[bool] = Form(False),
    quality: Optional[int] = Form(90),
    api_token: str = Depends(get_current_api_token)
):
    """
    修正上传图片的透视并上传到AIGC网盘
    """

    try:
        contents = await file.read()
        result_bytes = PerspectiveService.process_perspective(
            image_bytes=contents,
            points=points,
            auto_document=auto_document,
            quality=quality,
        )

        # 准备上传参数
        parameters = {
            "points": points,
            "auto_document": auto_document,
            "quality": quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="perspective",
            parameters=parameters,
            original_filename=file.filename,
            content_type=file.content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="透视修正处理并上传成功",
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

@router.post("/api/v1/perspective-by-url")
async def correct_perspective_by_url(
    request: PerspectiveByUrlRequest = Body(..., description="透视修正URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    修正URL图片的透视并上传到AIGC网盘
    """
    try:
        # 处理相对路径，转换为完整URL
        if request.image_url.startswith('/'):
            # 相对路径，转换为本地文件路径
            import os
            file_path = os.path.join(os.getcwd(), "public" + request.image_url)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    contents = f.read()
                content_type = "image/jpeg"  # 默认类型
            else:
                raise HTTPException(status_code=404, detail=f"本地文件不存在: {file_path}")
        else:
            # 完整URL，下载图片
            contents, content_type = await ImageUtils.download_image_from_url(request.image_url)

        result_bytes = PerspectiveService.process_perspective(
            image_bytes=contents,
            points=request.points,
            auto_document=request.auto_document,
            quality=request.quality,
        )

        # 准备上传参数
        parameters = {
            "points": request.points,
            "auto_document": request.auto_document,
            "quality": request.quality,
            "source_url": request.image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="perspective",
            parameters=parameters,
            original_filename=None,
            content_type=content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL图片透视修正处理并上传成功",
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