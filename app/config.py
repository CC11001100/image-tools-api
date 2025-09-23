import os
from typing import Optional


class Config:
    """应用配置类"""

    # 环境配置
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # 开发模式配置
    DEVELOPMENT_MODE: bool = os.getenv("DEVELOPMENT_MODE", "true").lower() == "true"

    # 用户中心配置
    USER_CENTER_BASE_URL: str = os.getenv("USER_CENTER_BASE_URL", "https://usersystem.aigchub.vip")
    USER_CENTER_INTERNAL_TOKEN: str = os.getenv("USER_CENTER_INTERNAL_TOKEN", "aigc-hub-big-business")

    # JWT配置
    JWT_COOKIE_NAME: str = "jwt_token"

    # API配置
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))

    # 计费配置
    DEFAULT_TOKEN_COST: int = int(os.getenv("DEFAULT_TOKEN_COST", "1"))

    # AIGC网盘服务配置
    AIGC_STORAGE_BASE_URL: str = os.getenv("AIGC_STORAGE_BASE_URL", "https://aigc-network-disk.aigchub.vip")
    AIGC_STORAGE_DEFAULT_CATEGORY_ID: str = os.getenv("AIGC_STORAGE_DEFAULT_CATEGORY_ID", "1")
    AIGC_STORAGE_DEFAULT_TAGS: str = os.getenv("AIGC_STORAGE_DEFAULT_TAGS", "图片处理,AI工具")

    @classmethod
    def get_user_center_headers(cls) -> dict:
        """获取用户中心API请求头"""
        return {
            "X-Internal-API-Token": cls.USER_CENTER_INTERNAL_TOKEN,
            "Content-Type": "application/json"
        }


# 全局配置实例
config = Config()
