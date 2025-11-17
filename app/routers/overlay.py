"""图片叠加路由"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from PIL import Image
import io
from typing import Optional, Tuple
from ..services.overlay_service import OverlayService
from ..services.image_service import ImageService
from ..services.file_upload_service import file_upload_service
from ..services.billing_service import billing_service
from ..utils.image_utils import ImageUtils
from ..utils.billing_utils import calculate_upload_only_billing, calculate_url_download_billing, calculate_dual_upload_billing, generate_operation_remark
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..middleware.auth_middleware import get_current_api_token
from pydantic import BaseModel

class OverlayByUrlRequest(BaseModel):
    """图片叠加URL请求模型"""
    image_url: str
    overlay_type: str = "gradient"
    quality: Optional[int] = 90

    # 渐变相关参数
    gradient_type: Optional[str] = "linear"
    gradient_direction: Optional[str] = "to_bottom"
    start_color: Optional[str] = "#000000"
    end_color: Optional[str] = "#ffffff"
    start_opacity: Optional[float] = 0.0
    end_opacity: Optional[float] = 0.8

    # 暗角效果参数
    vignette_intensity: Optional[float] = 0.6
    vignette_radius: Optional[float] = 1.2

    # 边框参数
    border_width: Optional[int] = 10
    border_color: Optional[str] = "#000000"
    border_style: Optional[str] = "solid"

class LogoByUrlRequest(BaseModel):
    """Logo叠加URL请求模型"""
    base_image_url: str
    logo_image_url: str
    position: str = "bottom-right"
    opacity: float = 1.0
    size_ratio: float = 0.2
    padding: int = 20
    output_format: str = "PNG"

router = APIRouter(
    tags=["overlay"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/overlay")
async def add_overlay(
    file: UploadFile = File(...),
    overlay_type: str = Form(...),
    opacity: Optional[float] = Form(0.8),
    quality: Optional[int] = Form(90),
    api_token: str = Depends(get_current_api_token)
):
    """
    为上传的图片添加叠加效果并上传到AIGC网盘
    """

    try:
        contents = await file.read()
        result_bytes = OverlayService.add_overlay(
            image_bytes=contents,
            overlay_type=overlay_type,
            opacity=opacity,
            quality=quality,
        )

        # 准备上传参数
        parameters = {
            "overlay_type": overlay_type,
            "opacity": opacity,
            "quality": quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="overlay",
            parameters=parameters,
            original_filename=file.filename,
            content_type=file.content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="叠加效果处理并上传成功",
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



@router.post("/api/v1/overlay-by-url")
async def add_overlay_by_url(
    request: OverlayByUrlRequest = Body(..., description="图片叠加URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    为URL图片添加叠加效果并上传到AIGC网盘
    """
    try:
        # 处理相对路径，转换为完整URL
        image_url = request.image_url
        if image_url.startswith('/examples/'):
            image_url = f"http://localhost:58889{image_url}"

        contents, content_type = ImageUtils.download_image_from_url(image_url)

        # 准备参数
        kwargs = {}
        if request.overlay_type == "gradient":
            kwargs.update({
                'gradient_type': request.gradient_type,
                'gradient_direction': request.gradient_direction,
                'start_color': request.start_color,
                'end_color': request.end_color,
                'start_opacity': request.start_opacity,
                'end_opacity': request.end_opacity
            })
        elif request.overlay_type == "vignette":
            kwargs.update({
                'intensity': request.vignette_intensity,
                'radius': request.vignette_radius
            })
        elif request.overlay_type == "border":
            # 解析颜色字符串为RGB元组
            border_color = request.border_color
            if border_color.startswith('#'):
                border_color = border_color[1:]
                border_rgb = tuple(int(border_color[i:i+2], 16) for i in (0, 2, 4))
            else:
                border_rgb = (0, 0, 0)  # 默认黑色

            kwargs.update({
                'border_width': request.border_width,
                'border_color': border_rgb,
                'border_style': request.border_style
            })

        result_bytes = OverlayService.add_overlay(
            image_bytes=contents,
            overlay_type=request.overlay_type,
            quality=request.quality,
            **kwargs
        )

        # 准备上传参数
        parameters = {
            "overlay_type": request.overlay_type,
            "quality": request.quality,
            "source_url": image_url,
            **kwargs
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="overlay",
            parameters=parameters,
            original_filename=None,
            content_type="image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL图片叠加效果处理并上传成功",
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

@router.post("/api/v1/logo")
async def add_logo(
    base_image: UploadFile = File(..., description="基础图片"),
    logo_image: UploadFile = File(..., description="Logo图片"),
    position: str = Form("bottom-right", description="位置: top-left, top-right, bottom-left, bottom-right, center"),
    opacity: float = Form(1.0, ge=0.0, le=1.0, description="透明度"),
    size_ratio: float = Form(0.2, ge=0.1, le=0.5, description="Logo大小比例"),
    padding: int = Form(20, ge=0, description="边距"),
    output_format: str = Form("PNG", description="输出格式"),
    api_token: str = Depends(get_current_api_token)
):
    """添加Logo叠加并上传到AIGC网盘"""
    try:
        base_img = await ImageService.load_image(base_image)
        logo_img = await ImageService.load_image(logo_image)
        result = OverlayService.add_logo(
            base_img, logo_img, position, opacity, size_ratio, padding
        )

        # 保存结果为字节数据
        output = io.BytesIO()
        result.save(output, format=output_format)
        result_bytes = output.getvalue()

        # 准备上传参数
        parameters = {
            "position": position,
            "opacity": opacity,
            "size_ratio": size_ratio,
            "padding": padding,
            "output_format": output_format,
            "base_filename": base_image.filename,
            "logo_filename": logo_image.filename
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="logo",
            parameters=parameters,
            original_filename=f"{base_image.filename}_with_logo",
            content_type=f"image/{output_format.lower()}"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="Logo叠加处理并上传成功",
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

@router.post("/api/v1/logo-by-url")
async def add_logo_by_url(
    request: LogoByUrlRequest = Body(..., description="Logo叠加URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """通过URL添加Logo叠加并上传到AIGC网盘"""
    try:
        base_contents, _ = ImageUtils.download_image_from_url(request.base_image_url)
        logo_contents, _ = ImageUtils.download_image_from_url(request.logo_image_url)

        base_img = Image.open(io.BytesIO(base_contents))
        logo_img = Image.open(io.BytesIO(logo_contents))

        result = OverlayService.add_logo(
            base_img, logo_img,
            request.position,
            request.opacity,
            request.size_ratio,
            request.padding
        )

        # 保存结果
        output = io.BytesIO()
        result.save(output, format=request.output_format)
        result_bytes = output.getvalue()

        # 准备上传参数
        parameters = {
            "position": request.position,
            "opacity": request.opacity,
            "size_ratio": request.size_ratio,
            "padding": request.padding,
            "output_format": request.output_format,
            "base_image_url": request.base_image_url,
            "logo_image_url": request.logo_image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="logo",
            parameters=parameters,
            original_filename=None,
            content_type=f"image/{request.output_format.lower()}"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL Logo叠加处理并上传成功",
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