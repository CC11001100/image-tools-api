from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional
import re
from datetime import datetime

from ..services.user_center_client import user_center_client
from ..schemas.user_models import User, UserStatus
from ..config import config
from ..utils.logger import logger


class AuthMiddleware(BaseHTTPMiddleware):
    """认证中间件"""
    
    # 不需要认证的路径
    EXCLUDED_PATHS = {
        "/",
        "/docs",
        "/openapi.json",
        "/redoc",
        "/favicon.ico",
        "/api/health"
    }

    # 不需要认证的路径前缀
    EXCLUDED_PATH_PREFIXES = {
        "/docs",
        "/openapi.json",
        "/redoc",
        "/static"
    }
    
    def __init__(self, app):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        # 检查是否需要认证
        # 跳过健康检查路径的日志输出以减少CPU占用
        if request.url.path not in {"/api/health", "/health"}:
            logger.debug(f"认证中间件检查路径: {request.url.path}")
        
        if self._should_skip_auth(request.url.path):
            return await call_next(request)
        
        # 获取用户信息
        user = await self._get_user_from_request(request)
        
        if not user:
            return JSONResponse(
                status_code=401,
                content={"code": 401, "message": "未授权访问，请先登录"}
            )
        
        # 将用户信息添加到请求状态中
        request.state.user = user
        request.state.api_token = user.api_token
        
        return await call_next(request)
    
    def _should_skip_auth(self, path: str) -> bool:
        """检查路径是否需要跳过认证"""
        # 精确匹配
        if path in self.EXCLUDED_PATHS:
            return True

        # 前缀匹配
        for excluded_prefix in self.EXCLUDED_PATH_PREFIXES:
            if path.startswith(excluded_prefix):
                return True

        # 兼容旧的前缀匹配逻辑
        for excluded_path in self.EXCLUDED_PATHS:
            if path.startswith(excluded_path + "/"):
                return True

        return False
    
    async def _get_user_from_request(self, request: Request) -> Optional[User]:
        """从请求中获取用户信息"""


        # 生产模式：正常的用户中心验证
        # 1. 优先从Authorization头获取api_token
        authorization = request.headers.get("Authorization")
        if authorization:
            api_token = self._extract_api_token(authorization)
            if api_token:
                user = await user_center_client.get_user_by_api_token(api_token)
                if user:
                    logger.info(f"通过API token认证用户: {user.nickname}")
                    return user

        # 2. 从cookie中获取jwt_token
        jwt_token = request.cookies.get(config.JWT_COOKIE_NAME)
        if jwt_token:
            user = await user_center_client.get_user_by_jwt_token(jwt_token)
            if user:
                logger.info(f"通过JWT token认证用户: {user.nickname}")
                return user

        logger.warning("未找到有效的认证信息")
        return None
    
    def _extract_api_token(self, authorization: str) -> Optional[str]:
        """从Authorization头中提取API token"""
        if not authorization:
            return None

        # 移除可能的"Bearer "前缀（不区分大小写）
        if authorization.lower().startswith("bearer "):
            return authorization[7:].strip()

        # 直接返回token（兼容不带Bearer前缀的情况）
        return authorization.strip()


def get_current_user(request: Request) -> User:
    """获取当前用户（用于依赖注入）"""
    if not hasattr(request.state, 'user'):
        raise HTTPException(status_code=401, detail="未授权访问")
    return request.state.user


def get_current_api_token(request: Request) -> str:
    """获取当前用户的API token（用于依赖注入）"""
    if not hasattr(request.state, 'api_token'):
        raise HTTPException(status_code=401, detail="未授权访问")
    return request.state.api_token
