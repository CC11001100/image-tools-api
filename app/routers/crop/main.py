from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends, Request
from ...services.crop_service import CropService
from ...services.file_upload_service import file_upload_service
from ...services.billing_service import billing_service
from ...utils.image_utils import ImageUtils
from ...utils.billing_utils import (
    calculate_upload_only_billing, calculate_url_download_billing,
    generate_operation_remark
)
from ...schemas.response_models import ErrorResponse, ImageProcessResponse, FileInfo, ApiResponse
from ...schemas.user_models import User
from ...middleware.auth_middleware import get_current_user, get_current_api_token
from typing import Optional
from pydantic import BaseModel
import io

# 导入子路由
from . import rectangle, shape, smart

class CropByUrlRequest(BaseModel):
    """图片裁剪URL请求模型"""
    image_url: str
    crop_type: str
    x: Optional[int] = 0
    y: Optional[int] = 0
    width: Optional[int] = None
    height: Optional[int] = None
    quality: Optional[int] = 90

router = APIRouter(
    tags=["crop"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

# 包含子路由
router.include_router(rectangle.router)
router.include_router(shape.router)
router.include_router(smart.router)

@router.post("/api/v1/crop")
async def crop_image(
    file: UploadFile = File(...),
    crop_type: str = Form(...),
    x: Optional[int] = Form(0),
    y: Optional[int] = Form(0),
    width: Optional[int] = Form(None),
    height: Optional[int] = Form(None),
    quality: Optional[int] = Form(90),
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """
    裁剪上传的图片并上传到AIGC网盘
    """

    call_id = None
    try:
        # 读取上传的文件
        contents = await file.read()
        original_size = len(contents)

        # 计算预估费用 - 先用原始大小估算，实际处理后会更新
        billing_info = calculate_upload_only_billing(primary_file_size=original_size, result_size=original_size)
        estimated_tokens = billing_info["total_cost"]
        
        # 准备请求上下文
        context = {
            "crop_type": crop_type,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "quality": quality,
            "filename": file.filename
        }
        
        # 生成详细备注
        remark = generate_operation_remark(
            "/api/v1/crop", f"图片裁剪({crop_type})", billing_info,
            裁剪类型=crop_type,
            坐标=f"({x},{y})",
            尺寸=f"{width}x{height}" if width and height else "自动",
            文件名=file.filename
        )
        
        # 预扣费 - 先付费再服务
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/crop",
            context=context,
            estimated_tokens=estimated_tokens,
            remark=remark
        )
        
        if not call_id:
            raise HTTPException(
                status_code=402,
                detail="余额不足或预扣费失败，请检查账户余额"
            )

        # 处理图片 - 根据裁剪类型调用不同方法
        if crop_type == "rectangle" or crop_type == "center":
            if crop_type == "center":
                # 居中裁剪，需要计算坐标
                from PIL import Image
                img = Image.open(io.BytesIO(contents))
                img_width, img_height = img.size

                if width is None:
                    width = min(img_width, img_height)
                if height is None:
                    height = min(img_width, img_height)

                x = (img_width - width) // 2
                y = (img_height - height) // 2

            result_bytes = CropService.crop_rectangle(
                image_bytes=contents,
                x=x,
                y=y,
                width=width,
                height=height,
                quality=quality,
            )
        elif crop_type == "smart_center":
            result_bytes = CropService.crop_smart_center(
                image_bytes=contents,
                target_width=width or 300,
                target_height=height or 300,
                quality=quality,
            )
        else:
            raise ValueError(f"不支持的裁剪类型: {crop_type}")

        # 准备上传参数
        parameters = {
            "crop_type": crop_type,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "quality": quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="crop",
            parameters=parameters,
            original_filename=file.filename,
            content_type=file.content_type or "image/jpeg"
        )

        if not upload_response:
            logger.error("文件上传失败")
            raise HTTPException(status_code=500, detail="文件上传失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="图片裁剪处理并上传成功",
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
            await billing_service.refund_all(call_id, f"图片裁剪处理失败: {str(e)}")
        return ApiResponse.error(
            message=f"图片裁剪处理失败: {str(e)}",
            code=500
        )

@router.post("/api/v1/crop-by-url")
async def crop_image_by_url(
    request: CropByUrlRequest = Body(..., description="图片裁剪URL请求参数"),
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """
    裁剪URL图片并上传到AIGC网盘
    """
    call_id = None
    try:
        # 预扣费
        call_id = await billing_service.pre_charge(
            user_id=current_user.id,
            operation_type="crop",
            estimated_cost=10
        )
        
        # 下载图片
        contents = ImageUtils.download_image_from_url(request.image_url)

        # 处理图片 - 根据裁剪类型调用不同方法
        if request.crop_type == "rectangle" or request.crop_type == "center":
            if request.crop_type == "center":
                # 居中裁剪，需要计算坐标
                from PIL import Image
                img = Image.open(io.BytesIO(contents))
                img_width, img_height = img.size

                width = request.width or min(img_width, img_height)
                height = request.height or min(img_width, img_height)

                x = (img_width - width) // 2
                y = (img_height - height) // 2
            else:
                x, y, width, height = request.x, request.y, request.width, request.height

            result_bytes = CropService.crop_rectangle(
                image_bytes=contents,
                x=x,
                y=y,
                width=width,
                height=height,
                quality=request.quality,
            )
        elif request.crop_type == "smart_center":
            result_bytes = CropService.crop_smart_center(
                image_bytes=contents,
                target_width=request.width or 300,
                target_height=request.height or 300,
                quality=request.quality,
            )
        else:
            raise ValueError(f"不支持的裁剪类型: {request.crop_type}")

        # 准备上传参数
        parameters = {
            "crop_type": request.crop_type,
            "x": request.x,
            "y": request.y,
            "width": request.width,
            "height": request.height,
            "quality": request.quality,
            "source_url": request.image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="crop",
            parameters=parameters,
            original_filename=None,
            content_type="image/jpeg"
        )

        if not upload_response:
            logger.error("文件上传失败")
            raise HTTPException(status_code=500, detail="文件上传失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        # 计算实际费用并结算
        billing_info = await billing_service.calculate_and_settle(
            call_id=call_id,
            user_id=current_user.id,
            operation_type="crop",
            input_size=len(contents),
            output_size=len(result_bytes),
            processing_time=0,
            success=True
        )

        return ApiResponse.success(
            message="图片裁剪处理并上传成功",
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
            await billing_service.refund_all(call_id, f"图片裁剪处理失败: {str(e)}")
        return ApiResponse.error(
            message=f"图片裁剪处理失败: {str(e)}",
            code=500
        )


