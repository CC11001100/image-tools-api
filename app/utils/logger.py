import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional


class Logger:
    """日志管理器，支持文件轮转和控制台输出"""
    
    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls) -> 'Logger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """设置日志配置"""
        # 创建日志目录
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 创建logger
        self._logger = logging.getLogger("image_tools_api")
        self._logger.setLevel(logging.DEBUG)
        
        # 防止重复添加handler
        if self._logger.handlers:
            return
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        
        # 文件处理器 - 支持轮转
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / "app.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,  # 保留5个备份文件
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
    
    def get_logger(self) -> logging.Logger:
        """获取logger实例"""
        return self._logger
    
    def debug(self, message: str):
        """记录调试信息"""
        self._logger.debug(message)
    
    def info(self, message: str):
        """记录一般信息"""
        self._logger.info(message)
    
    def warning(self, message: str):
        """记录警告信息"""
        self._logger.warning(message)
    
    def error(self, message: str):
        """记录错误信息"""
        self._logger.error(message)
    
    def critical(self, message: str):
        """记录严重错误信息"""
        self._logger.critical(message)


# 创建全局logger实例
logger = Logger() 