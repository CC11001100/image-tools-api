"""
数据库连接模块
提供MySQL和Redis连接
"""
import redis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import config
from .utils.logger import logger

# MySQL配置
try:
    engine = create_engine(
        config.get_mysql_url(),
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info(f"MySQL连接配置完成: {config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DATABASE}")
except Exception as e:
    logger.warning(f"MySQL连接配置失败: {str(e)}")
    engine = None
    SessionLocal = None
    Base = None

# Redis配置
try:
    redis_client = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        password=config.REDIS_PASSWORD if config.REDIS_PASSWORD else None,
        db=config.REDIS_DB,
        decode_responses=True
    )
    # 测试连接
    redis_client.ping()
    logger.info(f"Redis连接成功: {config.REDIS_HOST}:{config.REDIS_PORT}/{config.REDIS_DB}")
except Exception as e:
    logger.warning(f"Redis连接失败: {str(e)}")
    redis_client = None


def get_db():
    """获取数据库会话"""
    if SessionLocal is None:
        logger.warning("数据库未配置，跳过数据库操作")
        return None
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis():
    """获取Redis客户端"""
    if redis_client is None:
        logger.warning("Redis未配置，跳过Redis操作")
        return None
    return redis_client
