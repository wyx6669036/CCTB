"""
统一错误处理模块
提供应用程序的统一错误处理机制，包括异常捕获、日志记录和错误恢复
"""

import sys
import traceback
from typing import Any, Callable, Optional, Type, Union
from functools import wraps


class CCTBException(Exception):
    """CCTB应用程序基础异常类"""
    def __init__(self, message: str, error_code: Optional[str] = None, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.original_error = original_error


class PermissionError(CCTBException):
    """权限相关异常"""
    pass


class NetworkError(CCTBException):
    """网络相关异常"""
    pass


class SystemError(CCTBException):
    """系统相关异常"""
    pass


class ValidationError(CCTBException):
    """数据验证异常"""
    pass


class UserInputError(CCTBException):
    """用户输入异常"""
    pass


def handle_exception(
    exception_type: Type[BaseException] = Exception,
    default_return: Any = None,
    reraise: bool = False,
    log_error: bool = True,
    error_message: Optional[str] = None,
    error_code: Optional[str] = None
):
    """
    异常处理装饰器
    
    Args:
        exception_type: 要捕获的异常类型，默认为Exception
        default_return: 发生异常时的默认返回值
        reraise: 是否重新抛出异常，默认为False
        log_error: 是否记录错误日志，默认为True
        error_message: 自定义错误消息
        error_code: 自定义错误代码
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_type as e:
                # 构建错误消息
                msg = error_message or f"Error in {func.__name__}: {str(e)}"
                
                # 记录错误日志
                if log_error:
                    print(f"ERROR: {msg} (Error code: {error_code or 'UNKNOWN'})")
                    # 记录详细的堆栈跟踪
                    print(f"ERROR: Traceback: {traceback.format_exc()}")
                
                # 如果需要重新抛出异常
                if reraise:
                    raise
                
                # 返回默认值
                return default_return
        return wrapper
    return decorator


def safe_execute(
    func: Callable,
    args: tuple = (),
    kwargs: dict = None,
    default_return: Any = None,
    log_error: bool = True,
    error_message: Optional[str] = None
) -> Any:
    """
    安全执行函数，捕获所有异常
    
    Args:
        func: 要执行的函数
        args: 函数参数元组
        kwargs: 函数关键字参数字典
        default_return: 发生异常时的默认返回值
        log_error: 是否记录错误日志
        error_message: 自定义错误消息
        
    Returns:
        函数执行结果或默认返回值
    """
    if kwargs is None:
        kwargs = {}
        
    try:
        return func(*args, **kwargs)
    except Exception as e:
        msg = error_message or f"Error executing {func.__name__}: {str(e)}"
        
        if log_error:
            print(f"ERROR: {msg}")
            print(f"ERROR: Traceback: {traceback.format_exc()}")
            
        return default_return


def validate_and_execute(
    func: Callable,
    validators: list = None,
    args: tuple = (),
    kwargs: dict = None,
    default_return: Any = None,
    log_error: bool = True
) -> Any:
    """
    验证参数并执行函数
    
    Args:
        func: 要执行的函数
        validators: 验证函数列表，每个验证函数接受args和kwargs，返回(bool, message)元组
        args: 函数参数元组
        kwargs: 函数关键字参数字典
        default_return: 发生异常时的默认返回值
        log_error: 是否记录错误日志
        
    Returns:
        函数执行结果或默认返回值
    """
    if kwargs is None:
        kwargs = None
        
    if validators is None:
        validators = []
        
    # 执行验证
    for validator in validators:
        try:
            is_valid, message = validator(*args, **(kwargs or {}))
            if not is_valid:
                if log_error:
                    print(f"ERROR: Validation failed: {message}")
                return default_return
        except Exception as e:
            if log_error:
                print(f"ERROR: Validation error: {str(e)}")
            return default_return
    
    # 执行函数
    return safe_execute(func, args, kwargs, default_return, log_error)


def create_error_handler(
    error_type: Type[CCTBException],
    error_message: str,
    error_code: Optional[str] = None,
    log_error: bool = True
) -> Callable:
    """
    创建特定类型的错误处理函数
    
    Args:
        error_type: 错误类型
        error_message: 错误消息
        error_code: 错误代码
        log_error: 是否记录错误日志
        
    Returns:
        错误处理函数
    """
    def handler(original_error: Optional[Exception] = None, **kwargs) -> None:
        message = error_message.format(**kwargs) if kwargs else error_message
        exception = error_type(message, error_code, original_error)
        
        if log_error:
            print(f"ERROR: {str(exception)}")
            
        raise exception
    
    return handler


# 预定义的错误处理函数
handle_permission_error = create_error_handler(
    PermissionError,
    "Permission denied: {details}",
    "PERM_001"
)

handle_network_error = create_error_handler(
    NetworkError,
    "Network operation failed: {details}",
    "NET_001"
)

handle_system_error = create_error_handler(
    SystemError,
    "System operation failed: {details}",
    "SYS_001"
)

handle_validation_error = create_error_handler(
    ValidationError,
    "Validation failed: {details}",
    "VAL_001"
)


def setup_global_exception_handler():
    """设置全局异常处理器，捕获未处理的异常"""
    def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
        """处理未捕获的异常"""
        if issubclass(exc_type, KeyboardInterrupt):
            # 允许KeyboardInterrupt正常退出
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
            
        print("ERROR: Unhandled exception occurred:")
        print(f"ERROR: Type: {exc_type.__name__}")
        print(f"ERROR: Value: {exc_value}")
        
        # 记录详细的堆栈跟踪
        print("ERROR: Traceback:")
        for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
            for sub_line in line.split('\n'):
                if sub_line:  # 跳过空行
                    print(f"ERROR: {sub_line}")
    
    # 设置全局异常处理器
    sys.excepthook = handle_unhandled_exception