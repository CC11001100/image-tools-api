from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import Response
from ..services.stitch_service import StitchService
from ..services.file_upload_service import file_upload_service
from ..services.billing_service import billing_service
from ..utils.image_utils import ImageUtils
from ..utils.billing_utils import calculate_upload_only_billing, calculate_url_download_billing, generate_operation_remark
from ..schemas.response_models import ErrorResponse, ApiResponse, ImageProcessResponse, FileInfo
from ..middleware.auth_middleware import get_current_api_token
from typing import Optional, List
from pydantic import BaseModel

class StitchByUrlRequest(BaseModel):
    """图片拼接URL请求模型"""
    image_urls: List[str]
    direction: str
    spacing: Optional[int] = 0
    quality: Optional[int] = 90

router = APIRouter(
    tags=["stitch"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

@router.post("/api/v1/stitch")
async def stitch_images(
    files: List[UploadFile] = File(...),
    direction: str = Form(...),
    spacing: Optional[int] = Form(0),
    quality: Optional[int] = Form(90),
    api_token: str = Depends(get_current_api_token)
):
    """
    拼接多张上传的图片并上传到AIGC网盘
    需要认证访问，按照基础费用100Token + 上传费用50Token/MB计费
    """
    call_id = None
    try:
        contents = []
        filenames = []
        total_size = 0
        for file in files:
            content = await file.read()
            contents.append(content)
            filenames.append(file.filename)
            total_size += len(content)

        # 将字节数据转换为PIL Image对象
        images = []
        for content in contents:
            image = ImageUtils.bytes_to_image(content)
            images.append(image)
        
        result_image = StitchService.stitch_images(
            images=images,
            direction=direction,
            spacing=spacing,
            quality=quality,
        )
        
        # 将结果转换为字节
        result_bytes = ImageUtils.image_to_bytes(result_image, format="JPEG", quality=quality)
        result_size = len(result_bytes)

        # 计算预估费用（多文件上传，按结果大小计费）
        billing_info = calculate_upload_only_billing(result_size)
        estimated_tokens = billing_info["total_cost"]

        # 准备上传参数
        parameters = {
            "direction": direction,
            "spacing": spacing,
            "quality": quality,
            "image_count": len(files),
            "filenames": filenames,
            "total_input_size": total_size,
            "result_size": result_size
        }
        
        # 生成详细备注
        remark = generate_operation_remark(
            "/api/v1/stitch", f"拼接{len(files)}张图片({direction})", billing_info,
            图片数量=len(files),
            拼接方向=direction,
            间距=spacing
        )

        # 预扣费
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/stitch",
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
            operation_type="stitch",
            parameters=parameters,
            original_filename=f"stitched_{len(files)}_images",
            content_type="image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="图片拼接处理并上传成功",
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
            await billing_service.refund_all(call_id, f"图片拼接失败: {str(e)}")
        return ApiResponse.error(
            message=str(e),
            code=500
        )

@router.post("/api/v1/stitch-by-url")
async def stitch_images_by_url(
    request: StitchByUrlRequest = Body(..., description="图片拼接URL请求参数"),
    api_token: str = Depends(get_current_api_token)
):
    """
    拼接多个URL图片并上传到AIGC网盘
    需要认证访问，按照基础费用100Token + 下载费用30Token/MB计费
    """
    call_id = None
    try:
        # 下载并转换图片
        images = []
        total_download_size = 0
        for url in request.image_urls:
            content, _ = ImageUtils.download_image_from_url(url)
            total_download_size += len(content)
            image = ImageUtils.bytes_to_image(content)
            images.append(image)

        # 计算预估费用
        billing_info = calculate_url_download_billing(total_download_size)
        estimated_tokens = billing_info["total_cost"]

        result_image = StitchService.stitch_images(
            images=images,
            direction=request.direction,
            spacing=request.spacing,
            quality=request.quality,
        )
        
        # 将结果转换为字节
        result_bytes = ImageUtils.image_to_bytes(result_image, format="JPEG", quality=request.quality)

        # 准备上传参数
        parameters = {
            "direction": request.direction,
            "spacing": request.spacing,
            "quality": request.quality,
            "image_count": len(request.image_urls),
            "image_urls": request.image_urls,
            "total_download_size": total_download_size
        }
        
        # 生成详细备注
        remark = generate_operation_remark(
            "/api/v1/stitch-by-url", f"URL拼接{len(request.image_urls)}张图片({request.direction})", billing_info,
            图片数量=len(request.image_urls),
            拼接方向=request.direction
        )

        # 预扣费
        call_id = await billing_service.pre_charge(
            api_token=api_token,
            api_path="/api/v1/stitch-by-url",
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
            operation_type="stitch",
            parameters=parameters,
            original_filename=None,
            content_type="image/jpeg"
        )

        if not upload_response:
            raise HTTPException(status_code=500, detail="文件上传到网盘失败")

        # 构造响应
        file_info = FileInfo(**upload_response["file"])

        return ApiResponse.success(
            message="URL图片拼接处理并上传成功",
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
            await billing_service.refund_all(call_id, f"URL图片拼接失败: {str(e)}")
        return ApiResponse.error(
            message=str(e),
            code=500
        )

class StitchByUrlTestRequest(BaseModel):
    """图片拼接URL测试请求模型（单图片）"""
    image_url: str
    direction: str = "horizontal"
    gap: Optional[int] = 0
    background_color: Optional[str] = "#ffffff"
    quality: Optional[int] = 90

