"""
调试信息输出模块
提供统一的调试信息输出接口，支持不同级别的日志输出
"""

from packages.utils import Log


def debug(message, level="info"):
    """
    输出调试信息
    
    参数:
        message (str): 要输出的调试信息
        level (str): 日志级别，可选值为 "info", "warn", "error"，默认为 "info"
        
    返回:
        None
    """
    if level == "info":
        Log.info(message)
    elif level == "warn":
        Log.warn(message)
    elif level == "error":
        Log.error(message)
    else:
        # 如果传入未知的日志级别，默认使用info级别
        Log.info(f"[{level.upper()}] {message}")