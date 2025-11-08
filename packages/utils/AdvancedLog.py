"""
高级日志记录系统
提供灵活、可配置的日志记录功能，支持多种日志级别、输出格式和存储方式
"""
import os
import sys
import logging
import logging.handlers
from enum import Enum
from typing import Optional, Union, Dict, Any
from datetime import datetime
from colorama import Fore, Style, Back, init
from packages.utils.GetTime import getdatetime
from packages.utils.ErrorHandler import handle_exception, CCTBException
from packages.utils.ConfigManager import config

# 初始化colorama
init(autoreset=True)


class LogLevel(Enum):
    """日志级别枚举"""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class LogFormat(Enum):
    """日志格式枚举"""
    SIMPLE = "simple"
    DETAILED = "detailed"
    COLORED = "colored"
    JSON = "json"


class LoggerError(CCTBException):
    """日志记录器相关异常"""
    pass


class CCTBLogger:
    """CCTB应用程序日志记录器"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CCTBLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._setup_logger()
            self._initialized = True
    
    @handle_exception(LoggerError, default_return=None)
    def _setup_logger(self):
        """设置日志记录器"""
        # 首先尝试加载日志配置
        config.load_logging_config()
        
        # 创建日志记录器
        self._logger = logging.getLogger("CCTB")
        self._logger.setLevel(logging.DEBUG)
        
        # 清除现有处理器
        self._logger.handlers.clear()
        
        # 获取配置
        log_level = config.get("log_level", "INFO").upper()
        log_file = config.get("log_file", None)
        log_format = config.get("log_format", "colored")
        enable_console = config.get("enable_console", True)
        enable_file = config.get("enable_file", True)
        console_level = config.get("console_level", "INFO").upper()
        file_level = config.get("file_level", "DEBUG").upper()
        max_file_size = config.get("max_file_size", 10*1024*1024)
        backup_count = config.get("backup_count", 5)
        debug = config.get("debug", False)
        
        # 设置日志级别
        if debug:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(getattr(logging, log_level, logging.INFO))
        
        # 创建控制台处理器
        if enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, console_level, logging.INFO))
            console_formatter = self._get_formatter(LogFormat.COLORED if log_format == "colored" else LogFormat.SIMPLE)
            console_handler.setFormatter(console_formatter)
            self._logger.addHandler(console_handler)
        
        # 如果指定了日志文件，创建文件处理器
        if log_file and enable_file:
            try:
                # 确保日志目录存在
                log_dir = os.path.dirname(log_file)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                
                # 创建文件处理器，支持日志轮转
                file_handler = logging.handlers.RotatingFileHandler(
                    log_file, 
                    maxBytes=max_file_size,
                    backupCount=backup_count,
                    encoding='utf-8'
                )
                file_handler.setLevel(getattr(logging, file_level, logging.DEBUG))
                file_formatter = self._get_formatter(LogFormat.DETAILED)
                file_handler.setFormatter(file_formatter)
                self._logger.addHandler(file_handler)
            except Exception as e:
                # 如果无法创建文件处理器，记录错误但不中断程序
                self._logger.error(f"Failed to create file handler: {str(e)}")
    
    @handle_exception(LoggerError, default_return=None)
    def _get_formatter(self, format_type: LogFormat) -> logging.Formatter:
        """
        获取指定类型的格式化器
        
        Args:
            format_type: 格式类型
            
        Returns:
            格式化器实例
        """
        if format_type == LogFormat.SIMPLE:
            return logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        
        elif format_type == LogFormat.DETAILED:
            return logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"
            )
        
        elif format_type == LogFormat.COLORED:
            # 自定义彩色格式化器
            class ColoredFormatter(logging.Formatter):
                """彩色日志格式化器"""
                
                # 定义颜色映射
                COLORS = {
                    'DEBUG': Fore.CYAN,
                    'INFO': Fore.GREEN,
                    'WARNING': Fore.YELLOW,
                    'ERROR': Fore.RED,
                    'CRITICAL': Fore.RED + Back.WHITE + Style.BRIGHT,
                }
                
                def format(self, record):
                    # 获取原始格式化消息
                    log_message = super().format(record)
                    
                    # 添加颜色
                    level_color = self.COLORS.get(record.levelname, '')
                    if level_color:
                        # 为不同级别添加不同颜色
                        time_str = f"{Fore.LIGHTBLACK_EX}[{Fore.WHITE}{getdatetime()}{Fore.LIGHTBLACK_EX}]"
                        level_str = f"{Style.BRIGHT}{level_color}{record.levelname}{Style.RESET_ALL}"
                        message_str = f"{Fore.LIGHTWHITE_EX}{record.getMessage()}{Style.RESET_ALL}"
                        
                        if record.levelno in (logging.WARNING, logging.ERROR, logging.CRITICAL):
                            # 警告和错误级别添加星号前缀
                            message_str = f"{Fore.LIGHTWHITE_EX}* {message_str}"
                        
                        return f"{time_str} {level_str} {message_str}"
                    else:
                        return log_message
            
            return ColoredFormatter("%(message)s")
        
        elif format_type == LogFormat.JSON:
            # JSON格式化器
            import json
            
            class JsonFormatter(logging.Formatter):
                """JSON格式化器"""
                
                def format(self, record):
                    log_entry = {
                        'timestamp': datetime.fromtimestamp(record.created).isoformat(),
                        'level': record.levelname,
                        'logger': record.name,
                        'message': record.getMessage(),
                        'module': record.module,
                        'function': record.funcName,
                        'line': record.lineno
                    }
                    
                    # 添加异常信息（如果有）
                    if record.exc_info:
                        log_entry['exception'] = self.formatException(record.exc_info)
                    
                    return json.dumps(log_entry, ensure_ascii=False)
            
            return JsonFormatter()
        
        # 默认返回简单格式化器
        return logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    
    @handle_exception(LoggerError, default_return=None)
    def debug(self, message: str, *args, **kwargs):
        """记录调试信息"""
        self._logger.debug(message, *args, **kwargs)
    
    @handle_exception(LoggerError, default_return=None)
    def info(self, message: str, *args, **kwargs):
        """记录一般信息"""
        self._logger.info(message, *args, **kwargs)
    
    @handle_exception(LoggerError, default_return=None)
    def warning(self, message: str, *args, **kwargs):
        """记录警告信息"""
        self._logger.warning(message, *args, **kwargs)
    
    @handle_exception(LoggerError, default_return=None)
    def warn(self, message: str, *args, **kwargs):
        """记录警告信息（warning的别名）"""
        self.warning(message, *args, **kwargs)
    
    @handle_exception(LoggerError, default_return=None)
    def error(self, message: str, *args, **kwargs):
        """记录错误信息"""
        self._logger.error(message, *args, **kwargs)
    
    @handle_exception(LoggerError, default_return=None)
    def critical(self, message: str, *args, **kwargs):
        """记录严重错误信息"""
        self._logger.critical(message, *args, **kwargs)
    
    @handle_exception(LoggerError, default_return=None)
    def exception(self, message: str, *args, **kwargs):
        """记录异常信息（包含堆栈跟踪）"""
        self._logger.exception(message, *args, **kwargs)
    
    @handle_exception(LoggerError, default_return=None)
    def log(self, level: Union[int, str], message: str, *args, **kwargs):
        """
        记录指定级别的日志
        
        Args:
            level: 日志级别（可以是LogLevel枚举、字符串或整数）
            message: 日志消息
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        
        self._logger.log(level, message, *args, **kwargs)
    
    @handle_exception(LoggerError, default_return=None)
    def set_level(self, level: Union[int, str, LogLevel]):
        """
        设置日志级别
        
        Args:
            level: 日志级别
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        elif isinstance(level, LogLevel):
            level = level.value
        
        self._logger.setLevel(level)
        
        # 更新所有处理器的级别
        for handler in self._logger.handlers:
            handler.setLevel(level)
    
    @handle_exception(LoggerError, default_return=False)
    def add_file_handler(self, file_path: str, level: Union[int, str, LogLevel] = None):
        """
        添加文件处理器
        
        Args:
            file_path: 日志文件路径
            level: 日志级别，如果为None则使用记录器的级别
        """
        if level is None:
            level = self._logger.level
        elif isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        elif isinstance(level, LogLevel):
            level = level.value
        
        try:
            # 确保日志目录存在
            log_dir = os.path.dirname(file_path)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # 创建文件处理器
            file_handler = logging.FileHandler(file_path, encoding='utf-8')
            file_handler.setLevel(level)
            file_formatter = self._get_formatter(LogFormat.DETAILED)
            file_handler.setFormatter(file_formatter)
            self._logger.addHandler(file_handler)
            
            return True
        except Exception as e:
            self.error(f"Failed to add file handler: {str(e)}")
            return False
    
    @handle_exception(LoggerError, default_return=False)
    def remove_file_handler(self, file_path: str):
        """
        移除指定路径的文件处理器
        
        Args:
            file_path: 日志文件路径
        """
        for handler in self._logger.handlers[:]:
            if isinstance(handler, (logging.FileHandler, logging.handlers.RotatingFileHandler)):
                if handler.baseFilename == os.path.abspath(file_path):
                    self._logger.removeHandler(handler)
                    handler.close()
                    return True
        
        return False


# 创建全局日志记录器实例
logger = CCTBLogger()

# 为了向后兼容，提供与旧Log模块相同的接口
@handle_exception(default_return=None, error_message="Failed to write info log")
def info(text):
    """记录信息日志（向后兼容接口）"""
    logger.info(text)

@handle_exception(default_return=None, error_message="Failed to write warning log")
def warn(text):
    """记录警告日志（向后兼容接口）"""
    logger.warn(text)

@handle_exception(default_return=None, error_message="Failed to write error log")
def error(text):
    """记录错误日志（向后兼容接口）"""
    logger.error(text)

@handle_exception(default_return=None, error_message="Failed to write debug log")
def debug(text):
    """记录调试日志（向后兼容接口）"""
    logger.debug(text)