import time
import random
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends, Request
from ..services.resize_service import ResizeService
from ..services.file_upload_service import file_upload_service
from ..services.billing_service import billing_service
from ..utils.image_utils import ImageUtils
from ..utils.billing_utils import calculate_resize_billing
from ..schemas.response_models import ErrorResponse, ImageProcessResponse, FileInfo, ApiResponse
from ..schemas.user_models import User
from ..middleware.auth_middleware import get_current_user, get_current_api_token
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ResizeByUrlRequest(BaseModel):
    """调整图片大小的URL请求模型"""
    image_url: str
    width: Optional[int] = None
    height: Optional[int] = None
    maintain_aspect: Optional[bool] = True
    quality: Optional[int] = 90

# 移除测试模式的可选token函数，现在强制要求认证

router = APIRouter(
    tags=["resize"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/resize")
async def resize_image(
    file: UploadFile = File(...),
    width: Optional[int] = Form(None),
    height: Optional[int] = Form(None),
    maintain_aspect: Optional[bool] = Form(True),
    quality: Optional[int] = Form(90),
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """
    调整上传图片的大小并上传到AIGC网盘
    需要认证访问，按照基础费用100Token + 上传费用50Token/MB计费
    """
    api_path = "/api/v1/resize"
    call_id = f"resize_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"

    try:
        # 读取上传的文件
        contents = await file.read()
        original_size = len(contents)

        # 处理图片
        result_bytes = ResizeService.resize_image(
            image_bytes=contents,
            width=width,
            height=height,
            maintain_ratio=maintain_aspect,
            quality=quality,
        )

        result_size = len(result_bytes)

        # 计算预估费用（基础费用 + 上传费用）
        billing_info = calculate_resize_billing(upload_size_bytes=result_size)
        estimated_tokens = billing_info["total_cost"]

        # 准备请求上下文
        context = {
            "width": width,
            "height": height,
            "maintain_aspect": maintain_aspect,
            "quality": quality,
            "original_filename": file.filename,
            "original_size": original_size,
            "result_size": result_size,
            "billing_breakdown": billing_info["breakdown"]
        }

        # 1. 预扣费
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path=api_path,
            context=context,
            estimated_tokens=estimated_tokens,
            remark=f"图片缩放处理 - {file.filename}"
        )

        if not call_id:
            raise HTTPException(
                status_code=402,
                detail="余额不足或预扣费失败，请检查账户余额"
            )

        # 2. 执行业务逻辑 - 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="resize",
            parameters=context,
            original_filename=file.filename,
            content_type=file.content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 3. 成功完成，无需追加扣费（预估准确）
        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="图片缩放处理并上传成功",
            data={
                "file_info": file_info.dict(),
                "processing_info": {
                    **context,
                    "billing_info": billing_info,
                    "call_id": call_id,
                    "tokens_consumed": estimated_tokens
                }
            }
        )

    except HTTPException:
        # HTTP异常直接抛出，但需要退费
        if call_id:
            await billing_service.refund_all(call_id, "HTTP异常，退还费用")
        raise
    except Exception as e:
        # 4. 业务逻辑执行失败，返还Token
        if call_id:
            await billing_service.refund_all(call_id, f"图片处理失败: {str(e)}")
        return ApiResponse.error(
            message=f"图片处理失败: {str(e)}",
            code=500
        )

@router.post("/api/v1/resize-by-url")
async def resize_image_by_url(
    request_obj: Request,
    request: ResizeByUrlRequest = Body(..., description="调整图片大小的URL请求参数"),
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """
    调整URL图片的大小并上传到AIGC网盘
    """

    call_id = None
    try:
        # 处理相对路径，转换为完整URL
        if request.image_url.startswith('/'):
            # 相对路径，转换为本地文件路径
            import os
            file_path = os.path.join(os.getcwd(), "public" + request.image_url)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    contents = f.read()
            else:
                raise HTTPException(status_code=404, detail=f"本地文件不存在: {file_path}")
        else:
            # 完整URL，下载图片
            contents, _ = ImageUtils.download_image_from_url(request.image_url)

        # 计算预估费用
        billing_info = calculate_url_download_billing(len(contents))
        estimated_tokens = billing_info["total_cost"]
        
        # 准备请求上下文
        context = {
            "width": request.width,
            "height": request.height,
            "maintain_aspect": request.maintain_aspect,
            "quality": request.quality,
            "image_url": request.image_url
        }
        
        # 生成详细备注
        remark = generate_operation_remark(
            "/api/v1/resize-by-url", f"缩放({request.width}x{request.height})", billing_info,
            目标尺寸=f"{request.width}x{request.height}",
            保持比例=request.maintain_aspect,
            图片URL=request.image_url[:50] + "..." if len(request.image_url) > 50 else request.image_url
        )
        
        # 预扣费 - 先付费再服务
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/resize-by-url",
            context=context,
            estimated_tokens=estimated_tokens,
            remark=remark
        )
        
        if not call_id:
            raise HTTPException(
                status_code=402,
                detail="余额不足或预扣费失败，请检查账户余额"
            )

        # 处理图片
        result_bytes = ResizeService.resize_image(
            image_bytes=contents,
            width=request.width,
            height=request.height,
            maintain_ratio=request.maintain_aspect,
            quality=request.quality,
        )

        # 准备上传参数
        parameters = {
            "width": request.width,
            "height": request.height,
            "maintain_aspect": request.maintain_aspect,
            "quality": request.quality,
            "source_url": request.image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="resize",
            parameters=parameters,
            original_filename=None,
            content_type="image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="图片缩放处理并上传成功",
            data={
                "file_info": file_info.dict(),
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
            await billing_service.refund_all(call_id, f"URL图片处理失败: {str(e)}")
        return ApiResponse.error(
            message=f"URL图片处理失败: {str(e)}",
            code=500
        )


