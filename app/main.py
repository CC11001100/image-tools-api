from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from .routers import watermark_main, resize, filter, art_filter, perspective, blend, stitch, format
from .routers import overlay, mask, gif, advanced_text, annotation, canvas, color
from .routers import noise, pixelate, text_to_image, ai_text_to_image, auth_example
from .routers.transform.main import router as transform_router
from .routers.enhance.main import router as enhance_router
from .routers.crop.main import router as crop_router
from .middleware.auth_middleware import AuthMiddleware
from .schemas.response_models import ApiResponse
from .utils.logger import logger

app = FastAPI(
    title="Image Tools API",
    description="API for image processing operations like watermarking, resizing, and filtering",
    version="0.1.0",
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加认证中间件
app.add_middleware(AuthMiddleware)

# 包含各个功能的路由，不添加前缀（路由本身已有前缀）
app.include_router(watermark_main.router)
app.include_router(resize.router)
app.include_router(filter.router)
app.include_router(art_filter.router)
app.include_router(crop_router)
app.include_router(transform_router)
app.include_router(perspective.router)
app.include_router(canvas.router)
app.include_router(color.router)
app.include_router(blend.router)
app.include_router(stitch.router)
app.include_router(format.router)
app.include_router(overlay.router)
app.include_router(mask.router)
app.include_router(gif.router)
app.include_router(advanced_text.router)
app.include_router(annotation.router)
app.include_router(enhance_router)
app.include_router(noise.router)
app.include_router(pixelate.router)
app.include_router(text_to_image.router)
app.include_router(ai_text_to_image.router)
app.include_router(auth_example.router)

# 添加静态文件服务，用于提供示例文件
app.mount("/api/examples", StaticFiles(directory="public/examples"), name="examples")
# 添加测试图片静态文件服务 - 移到API路由之后
# app.mount("/", StaticFiles(directory="public", html=True), name="static")

@app.get("/api/")
async def root():
    logger.info("访问API根路径")
    return ApiResponse.success(
        message="Image Tools API 服务正常运行",
        data={
            "service": "Image Tools API",
            "version": "1.0.0",
            "docs_url": "/api/docs"
        }
    )

@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return ApiResponse.success(
        message="服务健康状态正常",
        data={
            "service": "Image Tools API",
            "version": "1.0.0",
            "status": "running"
        }
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"验证错误: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content=ApiResponse.error(
            message=f"参数验证失败: {str(exc)}",
            code=400
        )
    )

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request, exc):
    logger.error(f"请求验证错误: {str(exc)}")
    return JSONResponse(
        status_code=422,
        content=ApiResponse.error(
            message=f"请求参数验证失败: {str(exc)}",
            code=422
        )
    )

@app.exception_handler(404)
async def not_found_handler(request, exc):
    logger.warning(f"404错误: {request.url}")
    return JSONResponse(
        status_code=404,
        content=ApiResponse.error(
            message="请求的资源不存在",
            code=404
        )
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP异常: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse.error(
            message=str(exc.detail),
            code=exc.status_code
        )
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"全局异常处理: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ApiResponse.error(
            message=f"服务器内部错误: {str(exc)}",
            code=500
        )
    )

# 在所有API路由定义完成后，添加静态文件服务
app.mount("/static", StaticFiles(directory="public", html=True), name="static")

if __name__ == "__main__":
    logger.info("启动Image Tools API服务")
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=58888, reload=True)