"""图片信息提取接口"""
import time
import random
from fastapi import APIRouter, UploadFile, File, HTTPException, Body, Depends
from ..services.image_info_service import ImageInfoService
from ..services.billing_service import billing_service
from ..utils.image_utils import ImageUtils
from ..schemas.response_models import ErrorResponse, ApiResponse
from ..schemas.user_models import User
from ..middleware.auth_middleware import get_current_user, get_current_api_token
from pydantic import BaseModel
from PIL import Image
import io

class ImageInfoByUrlRequest(BaseModel):
    """图片信息URL请求模型"""
    image_url: str

router = APIRouter(
    tags=["image-info"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

# 图片信息接口的计费：基础费用10 Token
BASE_COST = 10

@router.post("/api/v1/image-info")
async def get_image_info(
    file: UploadFile = File(..., description="要获取信息的图片文件"),
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """
    获取上传图片的详细信息
    
    返回包括：
    - 图片格式、尺寸、模式
    - 文件大小
    - DPI信息
    - 透明通道
    - 颜色空间
    - GIF特殊信息（帧数、动画等）
    - EXIF数据
    - ICC配置文件信息
    
    计费：基础费用10 Token
    """
    api_path = "/api/v1/image-info"
    call_id = None

    try:
        # 读取上传的文件
        contents = await file.read()
        original_size = len(contents)

        # 打开图片
        image = Image.open(io.BytesIO(contents))

        # 获取图片信息
        image_info = ImageInfoService.get_image_info(image, contents)

        # 计算费用
        estimated_tokens = BASE_COST

        # 准备请求上下文
        context = {
            "original_filename": file.filename,
            "original_size": original_size,
            "format": image_info.get("format"),
            "dimensions": f"{image_info.get('width')}x{image_info.get('height')}"
        }

        # 预扣费
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path=api_path,
            context=context,
            estimated_tokens=estimated_tokens,
            remark=f"图片信息查询 - {file.filename}"
        )

        if not call_id:
            raise HTTPException(
                status_code=402,
                detail="余额不足或预扣费失败，请检查账户余额"
            )

        # 返回图片信息
        return ApiResponse.success(
            message="图片信息获取成功",
            data={
                "image_info": image_info,
                "billing_info": {
                    "base_cost": BASE_COST,
                    "total_cost": estimated_tokens,
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
            await billing_service.refund_all(call_id, f"图片信息获取失败: {str(e)}")
        return ApiResponse.error(
            message=f"图片信息获取失败: {str(e)}",
            code=500
        )


@router.post("/api/v1/image-info-by-url")
async def get_image_info_by_url(
    request: ImageInfoByUrlRequest = Body(..., description="图片URL请求参数"),
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """
    通过URL获取图片的详细信息
    
    支持：
    - HTTP/HTTPS图片URL
    - 本地相对路径（以/开头）
    
    返回与文件上传模式相同的图片信息
    
    计费：基础费用10 Token
    """
    api_path = "/api/v1/image-info-by-url"
    call_id = None

    try:
        # 处理相对路径或下载URL图片
        if request.image_url.startswith('/'):
            # 相对路径，转换为本地文件路径
            import os
            file_path = os.path.join(os.getcwd(), "frontend/public" + request.image_url)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    contents = f.read()
            else:
                raise HTTPException(status_code=404, detail=f"本地文件不存在: {file_path}")
        else:
            # 完整URL，下载图片
            contents, _ = ImageUtils.download_image_from_url(request.image_url)

        original_size = len(contents)

        # 打开图片
        image = Image.open(io.BytesIO(contents))

        # 获取图片信息
        image_info = ImageInfoService.get_image_info(image, contents)

        # 计算费用
        estimated_tokens = BASE_COST

        # 准备请求上下文
        context = {
            "image_url": request.image_url,
            "original_size": original_size,
            "format": image_info.get("format"),
            "dimensions": f"{image_info.get('width')}x{image_info.get('height')}"
        }

        # 预扣费
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path=api_path,
            context=context,
            estimated_tokens=estimated_tokens,
            remark=f"图片信息查询(URL) - {request.image_url[:100]}"
        )

        if not call_id:
            raise HTTPException(
                status_code=402,
                detail="余额不足或预扣费失败，请检查账户余额"
            )

        # 返回图片信息
        return ApiResponse.success(
            message="图片信息获取成功",
            data={
                "image_info": image_info,
                "billing_info": {
                    "base_cost": BASE_COST,
                    "total_cost": estimated_tokens,
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
            await billing_service.refund_all(call_id, f"图片信息获取失败: {str(e)}")
        return ApiResponse.error(
            message=f"图片信息获取失败: {str(e)}",
            code=500
        )
