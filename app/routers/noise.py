from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.noise_service import NoiseService
from ..services.file_upload_service import file_upload_service
from ..services.billing_service import billing_service
from ..utils.image_utils import ImageUtils
from ..utils.billing_utils import calculate_upload_only_billing, calculate_url_download_billing
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..schemas.user_models import User
from ..middleware.auth_middleware import get_current_user, get_current_api_token
from typing import Optional
from pydantic import BaseModel

class NoiseByUrlRequest(BaseModel):
    """降噪URL请求模型"""
    image_url: str
    noise_type: str
    intensity: Optional[float] = 1.0
    quality: Optional[int] = 90

router = APIRouter(
    tags=["noise"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/noise")
async def reduce_noise(
    file: UploadFile = File(...),
    noise_type: str = Form(...),
    intensity: Optional[float] = Form(1.0),
    quality: Optional[int] = Form(90),
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """
    为上传的图片进行噪点处理并上传到AIGC网盘
    """
    api_path = "/api/v1/noise"
    call_id = None

    try:
        contents = await file.read()
        original_size = len(contents)

        result_bytes = NoiseService.add_noise(
            image_bytes=contents,
            noise_type=noise_type,
            intensity=intensity,
            quality=quality,
        )

        result_size = len(result_bytes)
        original_size = len(contents)

        # 计算预估费用
        billing_info = calculate_upload_only_billing(primary_file_size=original_size, result_size=result_size)
        estimated_tokens = billing_info["total_cost"]

        # 准备请求上下文
        context = {
            "noise_type": noise_type,
            "intensity": intensity,
            "quality": quality,
            "original_filename": file.filename,
            "original_size": original_size,
            "result_size": result_size,
            "billing_breakdown": billing_info["breakdown"]
        }

        # 预扣费
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path=api_path,
            context=context,
            estimated_tokens=estimated_tokens,
            remark=f"噪点处理 - {file.filename}"
        )

        if not call_id:
            raise HTTPException(
                status_code=402,
                detail="余额不足或预扣费失败，请检查账户余额"
            )

        # 准备上传参数
        parameters = {
            "noise_type": noise_type,
            "intensity": intensity,
            "quality": quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="noise",
            parameters=parameters,
            original_filename=file.filename,
            content_type=file.content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="噪点处理并上传成功",
            data={
                "file_info": file_info.dict(),
                "processing_info": {
                    **parameters,
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
        # 业务逻辑执行失败，返还Token
        if call_id:
            await billing_service.refund_all(call_id, f"噪点处理失败: {str(e)}")
        return ApiResponse.error(
            message=f"噪点处理失败: {str(e)}",
            code=500
        )

@router.post("/api/v1/noise-by-url")
async def reduce_noise_by_url(
    request: NoiseByUrlRequest = Body(..., description="降噪URL请求参数"),
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """
    为URL图片进行噪点处理并上传到AIGC网盘
    """
    api_path = "/api/v1/noise-by-url"
    call_id = None

    try:
        contents, content_type = ImageUtils.download_image_from_url(request.image_url)
        download_size = len(contents)
        
        result_bytes = NoiseService.add_noise(
            image_bytes=contents,
            noise_type=request.noise_type,
            intensity=request.intensity,
            quality=request.quality,
        )

        result_size = len(result_bytes)

        # 计算预估费用（下载费用 + 上传费用）
        download_billing = calculate_url_download_billing(download_size=download_size, result_size=result_size)
        upload_billing = calculate_upload_only_billing(primary_file_size=download_size, result_size=result_size)
        
        total_cost = download_billing["total_cost"] + upload_billing["total_cost"]
        
        billing_info = {
            "total_cost": total_cost,
            "breakdown": {
                "download": download_billing["breakdown"],
                "upload": upload_billing["breakdown"]
            }
        }

        # 准备请求上下文
        context = {
            "noise_type": request.noise_type,
            "intensity": request.intensity,
            "quality": request.quality,
            "source_url": request.image_url,
            "download_size": download_size,
            "result_size": result_size,
            "billing_breakdown": billing_info["breakdown"]
        }

        # 预扣费
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path=api_path,
            context=context,
            estimated_tokens=total_cost,
            remark=f"URL噪点处理 - {request.image_url}"
        )

        if not call_id:
            raise HTTPException(
                status_code=402,
                detail="余额不足或预扣费失败，请检查账户余额"
            )

        # 准备上传参数
        parameters = {
            "noise_type": request.noise_type,
            "intensity": request.intensity,
            "quality": request.quality,
            "source_url": request.image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="noise",
            parameters=parameters,
            original_filename=None,
            content_type=content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL图片噪点处理并上传成功",
            data={
                "file_info": file_info.dict(),
                "processing_info": {
                    **parameters,
                    "billing_info": billing_info,
                    "call_id": call_id,
                    "tokens_consumed": total_cost
                }
            }
        )

    except HTTPException:
        # HTTP异常直接抛出，但需要退费
        if call_id:
            await billing_service.refund_all(call_id, "HTTP异常，退还费用")
        raise
    except Exception as e:
        # 业务逻辑执行失败，返还Token
        if call_id:
            await billing_service.refund_all(call_id, f"URL噪点处理失败: {str(e)}")
        return ApiResponse.error(
            message=f"URL噪点处理失败: {str(e)}",
            code=500
        )


