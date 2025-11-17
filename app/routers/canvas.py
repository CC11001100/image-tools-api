from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.canvas_service import CanvasService
from ..services.file_upload_service import file_upload_service
from ..services.billing_service import billing_service
from ..utils.image_utils import ImageUtils
from ..utils.billing_utils import calculate_upload_only_billing, calculate_url_download_billing, generate_operation_remark
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
    需要认证访问，按照基础费用100Token + 上传费用50Token/MB计费
    """
    call_id = None
    try:
        contents = await file.read()
        file_size = len(contents)
        
        result_bytes = CanvasService.process_canvas(
            image_bytes=contents,
            canvas_type=canvas_type,
            background_color=background_color,
            border_width=border_width,
            border_color=border_color,
            padding=padding,
            quality=quality,
        )
        
        result_size = len(result_bytes)

        # 计算预估费用
        billing_info = calculate_upload_only_billing(result_size)
        estimated_tokens = billing_info["total_cost"]

        # 准备上传参数
        parameters = {
            "canvas_type": canvas_type,
            "background_color": background_color,
            "border_width": border_width,
            "border_color": border_color,
            "padding": padding,
            "quality": quality,
            "original_size": file_size,
            "result_size": result_size
        }
        
        # 生成详细备注
        remark = generate_operation_remark(
            "/api/v1/canvas", f"画布处理({canvas_type})", billing_info,
            文件名=file.filename,
            画布类型=canvas_type,
            背景色=background_color
        )

        # 预扣费
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/canvas",
            context=parameters,
            estimated_tokens=estimated_tokens,
            remark=remark
        )

        if not call_id:
            raise HTTPException(
                status_code=402,
                detail="余额不足或预扣费失败，请检查账户余额"
            )

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
                "processing_info": parameters,
                "billing_info": billing_info
            }
        )
    except HTTPException:
        if call_id:
            await billing_service.refund_all(call_id, "HTTP异常，退还费用")
        raise
    except Exception as e:
        if call_id:
            await billing_service.refund_all(call_id, f"画布处理失败: {str(e)}")
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
    需要认证访问，按照基础费用100Token + 下载费用30Token/MB计费
    """
    call_id = None
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
            contents, content_type = ImageUtils.download_image_from_url(request.image_url)

        download_size = len(contents)
        
        # 计算预估费用
        billing_info = calculate_url_download_billing(download_size)
        estimated_tokens = billing_info["total_cost"]

        # 准备上传参数
        parameters = {
            "canvas_type": request.canvas_type,
            "background_color": request.background_color,
            "border_width": request.border_width,
            "border_color": request.border_color,
            "padding": request.padding,
            "quality": request.quality,
            "source_url": request.image_url,
            "download_size": download_size
        }
        
        # 生成详细备注
        remark = generate_operation_remark(
            "/api/v1/canvas-by-url", f"画布处理({request.canvas_type})", billing_info,
            画布类型=request.canvas_type,
            背景色=request.background_color,
            图片URL=request.image_url[:50] + "..." if len(request.image_url) > 50 else request.image_url
        )

        # 预扣费
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/canvas-by-url",
            context=parameters,
            estimated_tokens=estimated_tokens,
            remark=remark
        )

        if not call_id:
            raise HTTPException(
                status_code=402,
                detail="余额不足或预扣费失败，请检查账户余额"
            )

        result_bytes = CanvasService.process_canvas(
            image_bytes=contents,
            canvas_type=request.canvas_type,
            background_color=request.background_color,
            border_width=request.border_width,
            border_color=request.border_color,
            padding=request.padding,
            quality=request.quality,
        )

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
                "processing_info": parameters,
                "billing_info": billing_info
            }
        )
    except HTTPException:
        if call_id:
            await billing_service.refund_all(call_id, "HTTP异常，退还费用")
        raise
    except Exception as e:
        if call_id:
            await billing_service.refund_all(call_id, f"URL画布处理失败: {str(e)}")
        return ApiResponse.error(
            message=str(e),
            code=500
        )