from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ...services.transform_service import TransformService
from ...services.file_upload_service import file_upload_service
from ...services.billing_service import billing_service
from ...utils.image_utils import ImageUtils
from ...schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ...schemas.user_models import User
from ...middleware.auth_middleware import get_current_user, get_current_api_token
from typing import Optional
from pydantic import BaseModel

# 导入子路由
from . import rotate, flip

class TransformByUrlRequest(BaseModel):
    """图片变换URL请求模型"""
    image_url: str
    transform_type: str
    angle: Optional[float] = 0
    quality: Optional[int] = 90

router = APIRouter(
    tags=["transform"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

# 包含子路由
router.include_router(rotate.router)
router.include_router(flip.router)

@router.post("/api/v1/transform")
async def transform_image(
    file: UploadFile = File(...),
    transform_type: str = Form(...),
    angle: Optional[float] = Form(0),
    quality: Optional[int] = Form(90),
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """
    对上传的图片进行变换并上传到AIGC网盘
    """
    call_id = None
    try:
        # 预扣费
        call_id = await billing_service.pre_charge(
            user_id=current_user.id,
            operation_type="transform",
            estimated_cost=10
        )
        contents = await file.read()
        result_bytes = TransformService.transform_image(
            image_bytes=contents,
            transform_type=transform_type,
            angle=angle,
            quality=quality,
        )

        # 准备上传参数
        parameters = {
            "transform_type": transform_type,
            "angle": angle,
            "quality": quality
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="transform",
            parameters=parameters,
            original_filename=file.filename,
            content_type=file.content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        # 计算实际费用并结算
        billing_info = await billing_service.calculate_and_settle(
            call_id=call_id,
            user_id=current_user.id,
            operation_type="transform",
            input_size=len(contents),
            output_size=len(result_bytes),
            processing_time=0,
            success=True
        )

        return ApiResponse.success(
            message="图片变换处理并上传成功",
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
            await billing_service.refund_all(call_id, f"图片变换失败: {str(e)}")
        return ApiResponse.error(
            message=f"图片变换失败: {str(e)}",
            code=500
        )

@router.post("/api/v1/transform-by-url")
async def transform_image_by_url(
    request: TransformByUrlRequest = Body(..., description="图片变换URL请求参数"),
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """
    对URL图片进行变换并上传到AIGC网盘
    """
    call_id = None
    try:
        # 预扣费
        call_id = await billing_service.pre_charge(
            user_id=current_user.id,
            operation_type="transform",
            estimated_cost=10
        )
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

        result_bytes = TransformService.transform_image(
            image_bytes=contents,
            transform_type=request.transform_type,
            angle=request.angle,
            quality=request.quality,
        )

        # 准备上传参数
        parameters = {
            "transform_type": request.transform_type,
            "angle": request.angle,
            "quality": request.quality,
            "source_url": request.image_url
        }

        # 上传到网盘
        upload_response = await file_upload_service.upload_processed_image(
            image_bytes=result_bytes,
            api_token=api_token,
            operation_type="transform",
            parameters=parameters,
            original_filename=None,
            content_type=content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        # 计算实际费用并结算
        billing_info = await billing_service.calculate_and_settle(
            call_id=call_id,
            user_id=current_user.id,
            operation_type="transform",
            input_size=len(contents),
            output_size=len(result_bytes),
            processing_time=0,
            success=True
        )

        return ApiResponse.success(
            message="图片变换处理并上传成功",
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
            await billing_service.refund_all(call_id, f"图片变换失败: {str(e)}")
        return ApiResponse.error(
            message=f"图片变换失败: {str(e)}",
            code=500
        )