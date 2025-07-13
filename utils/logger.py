"""
日志处理工具类
提供统一的日志记录功能
"""

import logging
from datetime import datetime
from typing import Optional


class Logger:
    """日志处理类"""
    
    def __init__(self, name: str = "TARS", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            # 创建控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            
            # 创建格式化器
            formatter = logging.Formatter(
                '[%(asctime)s.%(msecs)03d] %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            
            # 添加处理器到日志器
            self.logger.addHandler(console_handler)
    
    def _get_timestamp(self) -> str:
        """获取精确到毫秒的时间戳"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    def info(self, message: str) -> None:
        """记录信息日志"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """记录警告日志"""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """记录错误日志"""
        self.logger.error(message)
    
    def debug(self, message: str) -> None:
        """记录调试日志"""
        self.logger.debug(message)
    
    def log_message(self, message: str) -> None:
        """兼容原有接口的日志方法"""
        self.info(message)


# 全局日志实例
logger = Logger() 