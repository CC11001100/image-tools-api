from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.color_service import ColorService
from ..services.file_upload_service import file_upload_service
from ..services.billing_service import billing_service, BillingCallType
from ..utils.image_utils import ImageUtils
from ..utils.billing_utils import calculate_url_download_billing, generate_operation_remark
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..schemas.user_models import User
from ..middleware.auth_middleware import get_current_user, get_current_api_token
from typing import Optional
from pydantic import BaseModel

class ColorByUrlRequest(BaseModel):
    """颜色调整URL请求模型"""
    image_url: str
    adjustment_type: str
    intensity: Optional[float] = 1.0
    quality: Optional[int] = 90

    # HSL调整参数
    hue_shift: Optional[float] = 0.0
    saturation_scale: Optional[float] = 1.0
    lightness_scale: Optional[float] = 1.0

    # 色彩平衡参数
    red_bias: Optional[float] = 0.0
    green_bias: Optional[float] = 0.0
    blue_bias: Optional[float] = 0.0

    # 色阶参数
    black_point: Optional[int] = 0
    white_point: Optional[int] = 255
    gamma: Optional[float] = 1.0

    # 色温色调参数
    temperature: Optional[float] = 0.0
    tint: Optional[float] = 0.0

    # 双色调参数
    shadow_color: Optional[str] = "#000000"
    highlight_color: Optional[str] = "#ffffff"

    # 自动校正参数
    preserve_tone: Optional[bool] = True

router = APIRouter(
    tags=["color"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/color")
async def adjust_color(
    file: UploadFile = File(...),
    adjustment_type: str = Form(...),
    intensity: Optional[float] = Form(1.0),
    quality: Optional[int] = Form(90),
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """
    调整上传图片的颜色并上传到AIGC网盘
    """
    call_id = None
    try:
        # 预扣费
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/color",
            context={
                "adjustment_type": adjustment_type,
                "intensity": intensity,
                "quality": quality
            },
            estimated_tokens=10,
            remark="颜色调整处理"
        )
        contents = await file.read()
        # 根据adjustment_type调用相应的方法
        if adjustment_type == "brightness":
            result_bytes = ColorService.adjust_color(
                image_bytes=contents,
                brightness=intensity * 50,  # 将intensity转换为亮度值
                quality=quality,
            )
        elif adjustment_type == "contrast":
            result_bytes = ColorService.adjust_color(
                image_bytes=contents,
                contrast=intensity * 50,  # 将intensity转换为对比度值
                quality=quality,
            )
        elif adjustment_type == "saturation":
            result_bytes = ColorService.adjust_color(
                image_bytes=contents,
                saturation=intensity * 50,  # 将intensity转换为饱和度值
                quality=quality,
            )
        else:
            # 使用apply_color_effect方法处理其他效果
            result_bytes = ColorService.apply_color_effect(
                image_bytes=contents,
                effect_type=adjustment_type,
                intensity=intensity,
                quality=quality,
            )

        # 准备上传参数
        parameters = {
            "adjustment_type": adjustment_type,
            "intensity": intensity,
            "quality": quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="color",
            parameters=parameters,
            original_filename=file.filename,
            content_type=file.content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        # 确认扣费
        await billing_service.confirm_charge(call_id, api_token)
        
        billing_info = {
            "call_id": call_id,
            "estimated_tokens": 10,
            "status": "completed"
        }

        return ApiResponse.success(
            message="颜色调整处理并上传成功",
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
            await billing_service.refund_all(call_id, f"颜色调整失败: {str(e)}")
        return ApiResponse.error(
            message=f"颜色调整失败: {str(e)}",
            code=500
        )

@router.post("/api/v1/color-by-url")
async def adjust_color_by_url(
    request: ColorByUrlRequest = Body(..., description="颜色调整URL请求参数"),
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """
    调整URL图片的颜色并上传到AIGC网盘
    """
    call_id = None
    try:
        # 预扣费
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/color-by-url",
            context={
                "image_url": request.image_url,
                "adjustment_type": request.adjustment_type,
                "intensity": request.intensity,
                "quality": request.quality
            },
            estimated_tokens=10,
            remark="URL图片颜色调整处理"
        )
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

        # 获取原始图片大小
        original_size = len(contents)

        # 根据adjustment_type调用相应的方法
        if request.adjustment_type == "brightness":
            result_bytes = ColorService.adjust_color(
                image_bytes=contents,
                brightness=request.intensity * 50,
                quality=request.quality,
            )
        elif request.adjustment_type == "contrast":
            result_bytes = ColorService.adjust_color(
                image_bytes=contents,
                contrast=request.intensity * 50,
                quality=request.quality,
            )
        elif request.adjustment_type == "saturation":
            result_bytes = ColorService.adjust_color(
                image_bytes=contents,
                saturation=request.intensity * 50,
                quality=request.quality,
            )
        elif request.adjustment_type == "hue":
            result_bytes = ColorService.adjust_color(
                image_bytes=contents,
                hue=request.hue_shift,
                quality=request.quality,
            )
        else:
            # 使用apply_color_effect方法处理其他效果
            result_bytes = ColorService.apply_color_effect(
                image_bytes=contents,
                effect_type=request.adjustment_type,
                intensity=request.intensity,
                quality=request.quality,
            )

        # 获取处理后图片大小
        result_size = len(result_bytes)

        # 准备上传参数
        parameters = {
            "adjustment_type": request.adjustment_type,
            "intensity": request.intensity,
            "quality": request.quality,
            "hue_shift": request.hue_shift,
            "saturation_scale": request.saturation_scale,
            "lightness_scale": request.lightness_scale,
            "red_bias": request.red_bias,
            "green_bias": request.green_bias,
            "blue_bias": request.blue_bias,
            "black_point": request.black_point,
            "white_point": request.white_point,
            "gamma": request.gamma,
            "temperature": request.temperature,
            "tint": request.tint,
            "shadow_color": request.shadow_color,
            "highlight_color": request.highlight_color,
            "preserve_tone": request.preserve_tone,
            "source_url": request.image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="color",
            parameters=parameters,
            original_filename=None,
            content_type=content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        # 确认扣费
        await billing_service.confirm_charge(call_id, api_token)
        
        billing_info = {
            "call_id": call_id,
            "estimated_tokens": 10,
            "status": "completed"
        }

        return ApiResponse.success(
            message="URL图片颜色调整处理并上传成功",
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
            await billing_service.refund_all(call_id, f"颜色调整失败: {str(e)}")
        return ApiResponse.error(
            message=f"颜色调整失败: {str(e)}",
            code=500
        )
