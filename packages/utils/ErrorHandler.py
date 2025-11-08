"""
ErrorHandler
提供统一的错误处理机制，减少代码重复
"""

import logging
from typing import Optional, Callable, Any
from packages.utils.Exceptions import SystemException, ValidationException


class ErrorHandler:
    """统一的错误处理类"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        初始化错误处理器
        
        参数:
            logger (Optional[logging.Logger]): 日志记录器实例
        """
        self.logger = logger or logging.getLogger(__name__)
    
    def handle_exception(self, e: Exception, context: str = "", reraise: bool = False) -> Optional[Any]:
        """
        统一处理异常
        
        参数:
            e (Exception): 异常实例
            context (str): 异常发生的上下文
            reraise (bool): 是否重新抛出异常
            
        返回:
            Optional[Any]: 根据情况可能返回None或特定值
        """
        error_msg = f"{context}: {str(e)}" if context else str(e)
        
        if isinstance(e, ValidationException):
            self.logger.error(f"Validation error: {error_msg}")
        elif isinstance(e, SystemException):
            self.logger.error(f"System error: {error_msg}")
        else:
            self.logger.error(f"Unexpected error: {error_msg}")
        
        if reraise:
            raise e
            
        return None
    
    def safe_execute(self, func: Callable, *args, context: str = "", default: Any = None, **kwargs) -> Any:
        """
        安全执行函数，自动捕获异常
        
        参数:
            func (Callable): 要执行的函数
            *args: 函数的位置参数
            context (str): 执行上下文
            default (Any): 发生异常时的默认返回值
            **kwargs: 函数的关键字参数
            
        返回:
            Any: 函数执行结果或默认值
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.handle_exception(e, context or f"Executing {func.__name__}")
            return default


# 创建全局错误处理器实例
error_handler = ErrorHandler()