from fastapi import APIRouter
from .watermark.text_watermark import router as text_watermark_router
from .watermark.image_watermark import router as image_watermark_router
from ..schemas.response_models import ErrorResponse

# 创建主路由器
router = APIRouter(
    tags=["watermark"],
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)

# 包含子路由
router.include_router(text_watermark_router)
router.include_router(image_watermark_router)
