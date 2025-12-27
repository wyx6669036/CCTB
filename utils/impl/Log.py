"""
日志记录模块 - 使用新的高级日志系统
提供向后兼容的日志记录接口，内部使用LogManager和AdvancedLog
"""

# 导入新的日志管理系统
from utils.impl.LogManager import log_manager, info as _info, warn as _warn, error as _error, debug as _debug

# 为了向后兼容，导出相同的函数
info = _info
warn = _warn
error = _error
debug = _debug

# 导出日志管理器，以便其他模块可以直接使用
__all__ = ['info', 'warn', 'error', 'debug', 'log_manager']