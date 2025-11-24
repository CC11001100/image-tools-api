import os
from typing import Optional
from urllib.parse import quote_plus


class Config:
    """应用配置类"""

    # 环境配置
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")

    # 开发模式配置
    DEVELOPMENT_MODE: bool = os.getenv("DEVELOPMENT_MODE", "false").lower() == "true"

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

    # MySQL配置
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "image_tools_api")
    
    # Redis配置
    REDIS_HOST: str = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))

    @classmethod
    def get_user_center_headers(cls) -> dict:
        """获取用户中心API请求头"""
        return {
            "X-Internal-API-Token": cls.USER_CENTER_INTERNAL_TOKEN,
            "Content-Type": "application/json"
        }
    
    @classmethod
    def get_mysql_url(cls) -> str:
        """获取MySQL连接URL"""
        password = quote_plus(cls.MYSQL_PASSWORD) if cls.MYSQL_PASSWORD else ""
        return f"mysql+pymysql://{cls.MYSQL_USER}:{password}@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DATABASE}?charset=utf8mb4"
    
    @classmethod
    def get_redis_url(cls) -> str:
        """获取Redis连接URL"""
        if cls.REDIS_PASSWORD:
            return f"redis://:{cls.REDIS_PASSWORD}@{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"
        return f"redis://{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"


# 全局配置实例
config = Config()
