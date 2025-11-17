from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.blend_service import BlendService
from ..services.file_upload_service import file_upload_service
from ..services.billing_service import billing_service
from ..utils.image_utils import ImageUtils
from ..utils.billing_utils import calculate_dual_upload_billing, calculate_url_download_billing, generate_operation_remark
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..middleware.auth_middleware import get_current_api_token
from typing import Optional
from pydantic import BaseModel

class BlendByUrlRequest(BaseModel):
    """图片混合URL请求模型"""
    base_image_url: str
    blend_image_url: str
    blend_mode: str
    opacity: Optional[float] = 1.0
    quality: Optional[int] = 90

router = APIRouter(
    tags=["blend"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/blend")
async def blend_images(
    base_image: UploadFile = File(..., description="基础图片文件"),
    blend_image: UploadFile = File(..., description="混合图片文件"),
    blend_mode: str = Form(..., description="混合模式"),
    opacity: Optional[float] = Form(1.0, description="混合透明度"),
    quality: Optional[int] = Form(90, description="输出图像质量"),
    api_token: str = Depends(get_current_api_token)
):
    """
    混合两张上传的图片并上传到AIGC网盘
    需要认证访问，按照基础费用100Token + 双文件上传费用计费
    """
    call_id = None
    try:
        base_contents = await base_image.read()
        blend_contents = await blend_image.read()
        
        base_size = len(base_contents)
        blend_size = len(blend_contents)
        
        result_bytes = BlendService.blend_images(
            base_image_bytes=base_contents,
            blend_image_bytes=blend_contents,
            blend_mode=blend_mode,
            opacity=opacity,
            quality=quality,
        )
        
        result_size = len(result_bytes)

        # 计算预估费用（双文件上传）
        billing_info = calculate_dual_upload_billing(base_size, blend_size, result_size)
        estimated_tokens = billing_info["total_cost"]

        # 准备上传参数
        parameters = {
            "blend_mode": blend_mode,
            "opacity": opacity,
            "quality": quality,
            "base_filename": base_image.filename,
            "blend_filename": blend_image.filename,
            "base_size": base_size,
            "blend_size": blend_size,
            "result_size": result_size
        }
        
        # 生成详细备注
        remark = generate_operation_remark(
            "/api/v1/blend", f"图片混合({blend_mode})", billing_info,
            混合模式=blend_mode,
            透明度=opacity,
            基础图片=base_image.filename,
            混合图片=blend_image.filename
        )

        # 预扣费
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/blend",
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
            operation_type="blend",
            parameters=parameters,
            original_filename=f"{base_image.filename}_blend_{blend_image.filename}",
            content_type=base_image.content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="图片混合处理并上传成功",
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
            await billing_service.refund_all(call_id, f"图片混合失败: {str(e)}")
        return ApiResponse.error(
            message=str(e),
            code=500
        )

@router.post("/api/v1/blend-by-url")
async def blend_images_by_url(
    request: BlendByUrlRequest = Body(..., description="图片混合URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    混合两张URL图片并上传到AIGC网盘
    需要认证访问，按照基础费用100Token + 下载费用30Token/MB计费
    """
    call_id = None
    try:
        base_contents, base_content_type = ImageUtils.download_image_from_url(request.base_image_url)
        blend_contents, _ = ImageUtils.download_image_from_url(request.blend_image_url)
        
        base_size = len(base_contents)
        blend_size = len(blend_contents)
        total_download_size = base_size + blend_size
        
        # 计算预估费用（URL下载）
        billing_info = calculate_url_download_billing(total_download_size)
        estimated_tokens = billing_info["total_cost"]
        
        result_bytes = BlendService.blend_images(
            base_image_bytes=base_contents,
            blend_image_bytes=blend_contents,
            blend_mode=request.blend_mode,
            opacity=request.opacity,
            quality=request.quality,
        )

        # 准备上传参数
        parameters = {
            "blend_mode": request.blend_mode,
            "opacity": request.opacity,
            "quality": request.quality,
            "base_image_url": request.base_image_url,
            "blend_image_url": request.blend_image_url,
            "base_size": base_size,
            "blend_size": blend_size
        }
        
        # 生成详细备注
        remark = generate_operation_remark(
            "/api/v1/blend-by-url", f"URL图片混合({request.blend_mode})", billing_info,
            混合模式=request.blend_mode,
            透明度=request.opacity
        )

        # 预扣费
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/blend-by-url",
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
            operation_type="blend",
            parameters=parameters,
            original_filename=None,
            content_type=base_content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL图片混合处理并上传成功",
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
            await billing_service.refund_all(call_id, f"URL图片混合失败: {str(e)}")
        return ApiResponse.error(
            message=str(e),
            code=500
        )

