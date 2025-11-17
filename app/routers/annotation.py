"""标注路由"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.annotation_service import AnnotationService
from ..services.file_upload_service import file_upload_service
from ..services.billing_service import billing_service
from ..utils.billing_utils import calculate_upload_only_billing, calculate_url_download_billing, generate_operation_remark
from ..utils.image_utils import ImageUtils
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..middleware.auth_middleware import get_current_api_token
from typing import Optional
from pydantic import BaseModel

class AnnotationByUrlRequest(BaseModel):
    """图片标注URL请求模型"""
    image_url: str
    annotation_type: str
    text: Optional[str] = None
    color: Optional[str] = "#FF0000"
    position: Optional[str] = "0,0"
    size: Optional[float] = 1.0
    quality: Optional[int] = 90

router = APIRouter(
    tags=["annotation"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/annotation")
async def add_annotation(
    file: UploadFile = File(...),
    annotation_type: str = Form(...),
    text: Optional[str] = Form(None),
    color: Optional[str] = Form("#FF0000"),
    position: Optional[str] = Form("0,0"),
    size: Optional[float] = Form(1.0),
    quality: Optional[int] = Form(90),
    api_token: str = Depends(get_current_api_token)
):
    """
    为上传的图片添加标注并上传到AIGC网盘
    """
    try:
        contents = await file.read()
        result_bytes = AnnotationService.add_annotation(
            image_bytes=contents,
            annotation_type=annotation_type,
            text=text,
            color=color,
            position=position,
            size=size,
            quality=quality,
        )

        # 准备上传参数
        parameters = {
            "annotation_type": annotation_type,
            "text": text,
            "color": color,
            "position": position,
            "size": size,
            "quality": quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="annotation",
            parameters=parameters,
            original_filename=file.filename,
            content_type=file.content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="标注处理并上传成功",
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

@router.post("/api/v1/annotation-by-url")
async def add_annotation_by_url(
    request: AnnotationByUrlRequest = Body(..., description="图片标注URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    为URL图片添加标注并上传到AIGC网盘
    """
    try:
        contents, content_type = ImageUtils.download_image_from_url(request.image_url)
        result_bytes = AnnotationService.add_annotation(
            image_bytes=contents,
            annotation_type=request.annotation_type,
            text=request.text,
            color=request.color,
            position=request.position,
            size=request.size,
            quality=request.quality,
        )

        # 准备上传参数
        parameters = {
            "annotation_type": request.annotation_type,
            "text": request.text,
            "color": request.color,
            "position": request.position,
            "size": request.size,
            "quality": request.quality,
            "source_url": request.image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="annotation",
            parameters=parameters,
            original_filename=None,
            content_type=content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL图片标注处理并上传成功",
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


