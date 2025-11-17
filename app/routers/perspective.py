from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.perspective_service import PerspectiveService
from ..services.file_upload_service import file_upload_service
from ..services.billing_service import billing_service
from ..utils.billing_utils import calculate_upload_only_billing, calculate_url_download_billing, generate_operation_remark
from ..utils.image_utils import ImageUtils
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..middleware.auth_middleware import get_current_api_token
from typing import Optional
from pydantic import BaseModel

class PerspectiveByUrlRequest(BaseModel):
    """透视修正URL请求模型"""
    image_url: str
    points: Optional[str] = None
    auto_document: Optional[bool] = False
    quality: Optional[int] = 90

router = APIRouter(
    tags=["perspective"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/perspective")
async def correct_perspective(
    file: UploadFile = File(...),
    points: Optional[str] = Form(None),
    auto_document: Optional[bool] = Form(False),
    quality: Optional[int] = Form(90),
    api_token: str = Depends(get_current_api_token)
):
    """
    修正上传图片的透视并上传到AIGC网盘
    需要认证访问，按照基础费用100Token + 上传费用50Token/MB计费
    """
    call_id = None
    try:
        contents = await file.read()
        file_size = len(contents)
        
        result_bytes = PerspectiveService.process_perspective(
            image_bytes=contents,
            points=points,
            auto_document=auto_document,
            quality=quality,
        )
        
        result_size = len(result_bytes)

        # 计算预估费用
        billing_info = calculate_upload_only_billing(result_size)
        estimated_tokens = billing_info["total_cost"]

        # 准备上传参数
        parameters = {
            "points": points,
            "auto_document": auto_document,
            "quality": quality,
            "original_size": file_size,
            "result_size": result_size
        }
        
        # 生成详细备注
        remark = generate_operation_remark(
            "/api/v1/perspective", "透视修正", billing_info,
            文件名=file.filename,
            自动文档=auto_document
        )

        # 预扣费
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/perspective",
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
            operation_type="perspective",
            parameters=parameters,
            original_filename=file.filename,
            content_type=file.content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="透视修正处理并上传成功",
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
            await billing_service.refund_all(call_id, f"透视修正失败: {str(e)}")
        return ApiResponse.error(
            message=str(e),
            code=500
        )

@router.post("/api/v1/perspective-by-url")
async def correct_perspective_by_url(
    request: PerspectiveByUrlRequest = Body(..., description="透视修正URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    修正URL图片的透视并上传到AIGC网盘
    需要认证访问，按照基础费用100Token + 下载费用30Token/MB计费
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

        result_bytes = PerspectiveService.process_perspective(
            image_bytes=contents,
            points=request.points,
            auto_document=request.auto_document,
            quality=request.quality,
        )

        # 准备上传参数
        parameters = {
            "points": request.points,
            "auto_document": request.auto_document,
            "quality": request.quality,
            "source_url": request.image_url,
            "download_size": download_size
        }
        
        # 生成详细备注
        remark = generate_operation_remark(
            "/api/v1/perspective-by-url", "URL透视修正", billing_info,
            自动文档=request.auto_document,
            图片URL=request.image_url[:50] + "..." if len(request.image_url) > 50 else request.image_url
        )

        # 预扣费
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/perspective-by-url",
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
            operation_type="perspective",
            parameters=parameters,
            original_filename=None,
            content_type=content_type or "image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL图片透视修正处理并上传成功",
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
            await billing_service.refund_all(call_id, f"URL透视修正失败: {str(e)}")
        return ApiResponse.error(
            message=str(e),
            code=500
        )