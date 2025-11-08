"""
时间获取模块
用于获取当前日期和时间信息
"""

import datetime
from packages.utils.ErrorHandler import handle_exception, SystemError


@handle_exception(SystemError, default_return="1970-01-01", error_message="Failed to get current date")
def getdate():
    """
    获取当前日期
    
    Returns:
        str: 格式为"YYYY-MM-DD"的日期字符串
        
    Raises:
        SystemError: 当获取日期失败时抛出
    """
    try:
        return datetime.datetime.now().strftime("%Y-%m-%d")
    except Exception as e:
        raise SystemError(f"Error getting current date: {e}")


@handle_exception(SystemError, default_return="00:00:00", error_message="Failed to get current time")
def gettime():
    """
    获取当前时间
    
    Returns:
        str: 格式为"HH:MM:SS"的时间字符串
        
    Raises:
        SystemError: 当获取时间失败时抛出
    """
    try:
        return datetime.datetime.now().strftime("%H:%M:%S")
    except Exception as e:
        raise SystemError(f"Error getting current time: {e}")


@handle_exception(SystemError, default_return="1970-01-01 00:00:00", error_message="Failed to get current date and time")
def getdatetime():
    """
    获取当前日期和时间
    
    Returns:
        str: 格式为"YYYY-MM-DD HH:MM:SS"的日期时间字符串
        
    Raises:
        SystemError: 当获取日期时间失败时抛出
    """
    try:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        raise SystemError(f"Error getting current date and time: {e}")


if __name__ == "__main__":
    # 测试代码
    print(f"Date: {getdate()}")
    print(f"Time: {gettime()}")
    print(f"DateTime: {getdatetime()}")
