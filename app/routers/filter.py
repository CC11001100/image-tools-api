import time
import random
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.image_service import ImageService
from ..services.file_upload_service import file_upload_service
from ..services.billing_service import billing_service
from ..utils.image_utils import ImageUtils
from ..utils.billing_utils import calculate_upload_only_billing, calculate_url_download_billing, generate_operation_remark
from ..schemas.request_models import FilterType
from ..schemas.response_models import ErrorResponse, ImageProcessResponse, FileInfo, ApiResponse
from ..schemas.user_models import User
from ..middleware.auth_middleware import get_current_user, get_current_api_token
from typing import Optional
from enum import Enum
from pydantic import BaseModel

class FilterByUrlRequest(BaseModel):
    """滤镜URL请求模型"""
    image_url: str
    filter_type: str
    intensity: Optional[float] = 1.0

# 滤镜描述字典
FILTER_DESCRIPTIONS = {
    # 基础滤镜
    "grayscale": "转换为灰度",
    "sepia": "棕褐色复古效果",
    "blur": "高斯模糊",
    "sharpen": "锐化",
    "brightness": "亮度调整",
    "contrast": "对比度调整",
    
    # 色彩效果
    "saturate": "饱和度增强",
    "desaturate": "去饱和",
    "warm": "暖色调",
    "cool": "冷色调",
    "vintage": "复古色彩",
    "hueshift": "色调偏移",
    "gamma": "伽马校正",
    "levels": "色阶调整",
    
    # 艺术效果
    "emboss": "浮雕效果",
    "posterize": "色调分离",
    "solarize": "曝光过度",
    "invert": "反色",
    "edge_enhance": "边缘增强",
    "smooth": "平滑",
    "detail": "细节增强",
    
    # 黑白效果
    "monochrome": "单色黑白",
    "dramatic_bw": "戏剧性黑白",
    "infrared": "红外效果",
    "high_contrast_bw": "高对比度黑白",
    
    # 复古和胶片效果
    "film_grain": "胶片颗粒",
    "retro": "复古风格",
    "polaroid": "宝丽来效果",
    "lomo": "LOMO风格",
    "analog": "模拟胶片",
    "crossprocess": "交叉处理",
    
    # 特殊效果
    "dream": "梦幻效果",
    "glow": "发光效果",
    "soft_focus": "柔焦",
    "noise": "噪点",
    "vignette": "暗角效果",
    "mosaic": "马赛克",
    
    # 滤镜效果
    "find_edges": "边缘检测",
    "contour": "轮廓",
    "edge_enhance_more": "强边缘增强",
    "smooth_more": "强平滑",
    "unsharp_mask": "反锐化遮罩",
    
    # 创意效果
    "pencil": "铅笔画",
    "sketch": "素描",
    "cartoon": "卡通效果",
    "hdr": "HDR效果",
    "cyberpunk": "赛博朋克",
    "noir": "黑色电影",
    "faded": "褪色效果",
    "pastel": "柔和色彩",
}

router = APIRouter(
    tags=["filter"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.get("/api/v1/filter/list")
async def list_filters():
    """
    列出所有可用的基础滤镜及其描述
    """
    return ApiResponse.success(
        message="获取滤镜列表成功",
        data={
            "filters": FILTER_DESCRIPTIONS,
            "total": len(FILTER_DESCRIPTIONS),
            "categories": {
                "basic": ["grayscale", "sepia", "blur", "sharpen", "brightness", "contrast"],
                "color": ["saturate", "desaturate", "warm", "cool", "vintage", "hueshift", "gamma", "levels"],
                "artistic": ["emboss", "posterize", "solarize", "invert", "edge_enhance", "smooth", "detail"],
                "blackwhite": ["monochrome", "dramatic_bw", "infrared", "high_contrast_bw"],
                "retro": ["film_grain", "retro", "polaroid", "lomo", "analog", "crossprocess"],
                "special": ["dream", "glow", "soft_focus", "noise", "vignette", "mosaic"],
                "filter": ["find_edges", "contour", "edge_enhance_more", "smooth_more", "unsharp_mask"],
                "creative": ["pencil", "sketch", "cartoon", "hdr", "cyberpunk", "noir", "faded", "pastel"]
            }
        }
    )

@router.post("/api/v1/filter")
async def apply_filter(
    file: UploadFile = File(...),
    filter_type: str = Form(...),
    intensity: Optional[float] = Form(1.0),
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """
    对上传图片应用滤镜效果
    需要认证访问，按照基础费用100Token + 上传费用50Token/MB计费
    """
    api_path = "/api/v1/filter"
    call_id = None

    try:
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="上传的文件不是图片格式")

        try:
            filter_enum = FilterType(filter_type)
        except ValueError:
            valid_filters = ", ".join([f.value for f in FilterType])
            raise HTTPException(status_code=400, detail=f"无效的滤镜类型。支持的滤镜有: {valid_filters}")

        # 读取上传的文件
        contents = await file.read()
        original_size = len(contents)

        # 处理图片
        result_bytes = ImageService.apply_filter(
            image_bytes=contents,
            filter_type=filter_enum.value,
            intensity=intensity,
        )

        result_size = len(result_bytes)

        # 计算预估费用
        billing_info = calculate_upload_only_billing(upload_size_bytes=result_size)
        estimated_tokens = billing_info["total_cost"]

        # 准备请求上下文
        context = {
            "filter_type": filter_type,
            "intensity": intensity,
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
            remark=f"滤镜处理 - {file.filename}"
        )

        if not call_id:
            raise HTTPException(
                status_code=402,
                detail="余额不足或预扣费失败，请检查账户余额"
            )

        # 准备上传参数
        parameters = {
            "filter_type": filter_type,
            "intensity": intensity,
            "original_filename": file.filename,
            "original_size": len(contents),
            "result_size": len(result_bytes)
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="filter",
            parameters=parameters,
            original_filename=file.filename,
            content_type=file.content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="滤镜处理并上传成功",
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
        # 4. 业务逻辑执行失败，返还Token
        if call_id:
            await billing_service.refund_all(call_id, f"滤镜处理失败: {str(e)}")
        return ApiResponse.error(
            message=f"滤镜处理失败: {str(e)}",
            code=500
        )



@router.post("/api/v1/filter-by-url")
async def apply_filter_by_url(
    request: FilterByUrlRequest = Body(..., description="滤镜URL请求参数"),
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """
    对URL图片应用滤镜效果并上传到AIGC网盘
    """
    api_path = "/api/v1/filter-by-url"
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
                content_type = "image/jpeg"  # 默认类型
            else:
                raise HTTPException(status_code=404, detail=f"本地文件不存在: {file_path}")
        else:
            # 完整URL，下载图片
            contents, content_type = ImageUtils.download_image_from_url(request.image_url)

        try:
            filter_enum = FilterType(request.filter_type)
        except ValueError:
            valid_filters = ", ".join([f.value for f in FilterType])
            raise HTTPException(status_code=400, detail=f"无效的滤镜类型。支持的滤镜有: {valid_filters}")

        result_bytes = ImageService.apply_filter(
            image_bytes=contents,
            filter_type=filter_enum.value,
            intensity=request.intensity,
        )

        original_size = len(contents)
        result_size = len(result_bytes)

        # 计算预估费用
        billing_info = calculate_url_download_billing(
            download_size_bytes=original_size,
            upload_size_bytes=result_size
        )
        estimated_tokens = billing_info["total_cost"]

        # 准备请求上下文
        context = {
            "filter_type": request.filter_type,
            "intensity": request.intensity,
            "source_url": request.image_url,
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
            remark=f"滤镜处理URL - {request.image_url}"
        )

        if not call_id:
            raise HTTPException(
                status_code=402,
                detail="余额不足或预扣费失败，请检查账户余额"
            )

        # 准备上传参数
        parameters = {
            "filter_type": request.filter_type,
            "intensity": request.intensity,
            "source_url": request.image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="filter",
            parameters=parameters,
            original_filename=None,
            content_type=content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="滤镜处理并上传成功",
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
        if call_id:
            await billing_service.refund_all(call_id, "HTTP异常，退还费用")
        raise
    except Exception as e:
        if call_id:
            await billing_service.refund_all(call_id, f"滤镜处理失败: {str(e)}")
        return ApiResponse.error(
            message=f"滤镜处理失败: {str(e)}",
            code=500
        )
