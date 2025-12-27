"""
日志管理器模块
提供统一的日志管理接口，支持日志记录器的创建、配置和管理
"""

from typing import Dict, Optional, Union, List
from utils.impl.AdvancedLog import CCTBLogger, LogLevel, LogFormat
from utils.impl.ConfigManager import config
from utils.impl.ErrorHandler import handle_exception, CCTBException


class LogManagerError(CCTBException):
    """日志管理器相关异常"""
    pass


class LogManager:
    """日志管理器，负责管理应用程序中的所有日志记录器"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LogManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._loggers: Dict[str, CCTBLogger] = {}
            self._default_logger = None
            self._initialized = True
    
    @handle_exception(LogManagerError, default_return=None)
    def get_logger(self, name: str = "CCTB", create_if_missing: bool = True) -> Optional[CCTBLogger]:
        """
        获取指定名称的日志记录器
        
        Args:
            name: 日志记录器名称
            create_if_missing: 如果日志记录器不存在是否创建
            
        Returns:
            日志记录器实例，如果不存在且create_if_missing为False则返回None
        """
        if name in self._loggers:
            return self._loggers[name]
        
        if create_if_missing:
            return self.create_logger(name)
        
        return None
    
    @handle_exception(LogManagerError, default_return=None)
    def create_logger(self, name: str, level: Union[LogLevel, str, int] = None, 
                     format_type: LogFormat = None, log_file: str = None) -> Optional[CCTBLogger]:
        """
        创建新的日志记录器
        
        Args:
            name: 日志记录器名称
            level: 日志级别
            format_type: 日志格式类型
            log_file: 日志文件路径
            
        Returns:
            新创建的日志记录器实例
        """
        if name in self._loggers:
            return self._loggers[name]
        
        # 创建新的日志记录器
        logger = CCTBLogger()
        logger._logger.name = name
        
        # 设置日志级别
        if level is not None:
            if isinstance(level, str):
                level = LogLevel[level.upper()]
            elif isinstance(level, int):
                level = LogLevel(level)
            
            logger.set_level(level)
        
        # 设置日志格式
        if format_type is not None:
            # 这里可以扩展为支持不同的格式类型
            pass
        
        # 添加文件处理器
        if log_file is not None:
            logger.add_file_handler(log_file)
        
        self._loggers[name] = logger
        
        # 如果这是第一个创建的日志记录器，设为默认
        if self._default_logger is None:
            self._default_logger = logger
        
        return logger
    
    @handle_exception(LogManagerError, default_return=None)
    def get_default_logger(self) -> Optional[CCTBLogger]:
        """
        获取默认日志记录器
        
        Returns:
            默认日志记录器实例
        """
        if self._default_logger is None:
            self._default_logger = self.get_logger("CCTB")
        
        return self._default_logger
    
    @handle_exception(LogManagerError, default_return=None)
    def set_default_logger(self, name: str) -> bool:
        """
        设置默认日志记录器
        
        Args:
            name: 日志记录器名称
            
        Returns:
            设置成功返回True，失败返回False
        """
        if name in self._loggers:
            self._default_logger = self._loggers[name]
            return True
        
        return False
    
    @handle_exception(LogManagerError, default_return=None)
    def list_loggers(self) -> List[str]:
        """
        获取所有日志记录器名称列表
        
        Returns:
            日志记录器名称列表
        """
        return list(self._loggers.keys())
    
    @handle_exception(LogManagerError, default_return=None)
    def remove_logger(self, name: str) -> bool:
        """
        移除指定的日志记录器
        
        Args:
            name: 日志记录器名称
            
        Returns:
            移除成功返回True，失败返回False
        """
        if name in self._loggers:
            # 如果移除的是默认日志记录器，需要重新设置默认
            if self._default_logger == self._loggers[name]:
                self._default_logger = None
            
            del self._loggers[name]
            return True
        
        return False
    
    @handle_exception(LogManagerError, default_return=None)
    def configure_from_config(self) -> bool:
        """
        从配置文件配置日志管理器
        
        Returns:
            配置成功返回True，失败返回False
        """
        try:
            # 加载日志配置
            config.load_logging_config()
            
            # 获取日志配置
            loggers_config = config.get("loggers", {})
            
            # 为每个配置的日志记录器创建或更新日志记录器
            for logger_name, logger_config in loggers_config.items():
                level = logger_config.get("level", "INFO")
                handlers = logger_config.get("handlers", [])
                
                # 获取或创建日志记录器
                logger = self.get_logger(logger_name)
                
                if logger:
                    # 设置日志级别
                    logger.set_level(level)
                    
                    # 配置处理器
                    if "console" in handlers and not config.get("enable_console", True):
                        # 如果配置了控制台处理器但全局禁用了控制台，则移除
                        pass  # 这里可以扩展为移除控制台处理器
                    
                    if "file" in handlers and config.get("enable_file", True):
                        # 如果配置了文件处理器且启用了文件日志
                        log_file = config.get("log_file")
                        if log_file:
                            logger.add_file_handler(log_file)
            
            return True
        except Exception as e:
            raise LogManagerError(f"Failed to configure log manager: {str(e)}")
    
    @handle_exception(LogManagerError, default_return=None)
    def create_module_logger(self, module_name: str) -> Optional[CCTBLogger]:
        """
        为指定模块创建日志记录器
        
        Args:
            module_name: 模块名称
            
        Returns:
            模块日志记录器实例
        """
        logger_name = f"CCTB.{module_name}"
        return self.get_logger(logger_name)


# 创建全局日志管理器实例
log_manager = LogManager()

# 为了向后兼容，提供与旧Log模块相同的接口
@handle_exception(default_return=None, error_message="Failed to write info log")
def info(text):
    """记录信息日志（向后兼容接口）"""
    log_manager.get_default_logger().info(text)

@handle_exception(default_return=None, error_message="Failed to write warning log")
def warn(text):
    """记录警告日志（向后兼容接口）"""
    log_manager.get_default_logger().warn(text)

@handle_exception(default_return=None, error_message="Failed to write error log")
def error(text):
    """记录错误日志（向后兼容接口）"""
    log_manager.get_default_logger().error(text)

@handle_exception(default_return=None, error_message="Failed to write debug log")
def debug(text):
    """记录调试日志（向后兼容接口）"""
    log_manager.get_default_logger().debug(text)