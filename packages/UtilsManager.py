"""
UtilsManager
把所有（并非）功能整合为一个，使用时仅需import packages.UtilsManager as utils即可
有些功能没有整合到，要么用的不多要么懒得搞，到时候再说
格式可以参考下面添加
"""

# 导入错误处理模块
from packages.utils.ErrorHandler import (
    handle_exception, safe_execute, validate_and_execute,
    CCTBException, PermissionError, NetworkError, SystemError, ValidationError,
    handle_permission_error, handle_network_error, handle_system_error, handle_validation_error,
    setup_global_exception_handler
)

# 设置全局异常处理器
setup_global_exception_handler()


def ip_scanner(*args, **kwargs):
    """Run the IP scanner main() and return its result (lazy import).
    Mirrors the previous 'from packages.utils.IPscanner import main as ip_scanner'.
    """
    from packages.utils.IPscanner import main as _main
    return _main(*args, **kwargs)


def anti_full_screen(target_ip, target_port=None):
    """Call the anti_full_screen implementation (lazy import)."""
    from packages.utils.fuckMythware import anti_full_screen as _af
    if target_port is None:
        return _af(target_ip)
    return _af(target_ip, target_port)


def send_teacher_message(text, target_ip, target_port=None):
    """发送教师消息，带有错误处理"""
    from packages.utils.fuckMythware import send_teacher_message as _stm
    
    @handle_exception(NetworkError, default_return=False, error_message="Failed to send teacher message")
    def _send():
        if target_port is None:
            return _stm(text, target_ip)
        return _stm(text, target_ip, target_port)
    
    return _send()


def start_applicaion(path, target_ip, target_port=None):
    """启动应用程序，带有错误处理"""
    from packages.utils.fuckMythware import start_applicaion as _sa
    
    @handle_exception(NetworkError, default_return=False, error_message="Failed to start application")
    def _start():
        if target_port is None:
            return _sa(path, target_ip)
        return _sa(path, target_ip, target_port)
    
    return _start()

# Optionally provide direct module access helpers if other code expects attributes
def get_utils_module(name: str):
    """Return a utils submodule by name (e.g. 'IPscanner', 'fuckMythware')."""
    import importlib
    return importlib.import_module(f"packages.utils.{name}")

def AdmCheck():
    """检查管理员权限，带有错误处理"""
    from packages.utils.AdmCheck import checkAdm as _AdmCheck
    
    @handle_exception(PermissionError, default_return=False, error_message="Failed to check administrator privileges")
    def _check():
        return _AdmCheck()
    
    return _check()


def SysCheck():
    """检查系统信息，带有错误处理"""
    from packages.utils.SysCheck import sysCheck as _SysCheck
    
    @handle_exception(SystemError, default_return={"name": "unknown", "version": "unknown"}, 
                     error_message="Failed to check system information")
    def _check():
        return _SysCheck()
    
    return _check()

def info(message):
    """记录信息日志，带有错误处理"""
    from packages.utils.Log import info as _info
    
    @handle_exception(default_return=None, error_message="Failed to log info message")
    def _log():
        return _info(message)
    
    return _log()

def warn(message):
    """记录警告日志，带有错误处理"""
    from packages.utils.Log import warn as _warn
    
    @handle_exception(default_return=None, error_message="Failed to log warning message")
    def _log():
        return _warn(message)
    
    return _log()

def error(message):
    """记录错误日志，带有错误处理"""
    from packages.utils.Log import error as _error
    
    @handle_exception(default_return=None, error_message="Failed to log error message")
    def _log():
        return _error(message)
    
    return _log()

def Clear():
    """清屏，带有错误处理"""
    from packages.utils.ClearScreen import clearScreen as _Clear
    
    @handle_exception(default_return=None, error_message="Failed to clear screen")
    def _clear():
        return _Clear()
    
    return _clear()

def selectOption(choice):
    """处理选项，带有错误处理"""
    from packages.options import selectOption as _selectOption
    
    @handle_exception(default_return=None, error_message="Failed to process option")
    def _select():
        return _selectOption(choice)
    
    return _select()

def get_performance_stats():
    """获取性能统计，带有错误处理"""
    from packages.utils.Performance import get_performance_stats as _get_stats
    
    @handle_exception(default_return={}, error_message="Failed to get performance stats")
    def _stats():
        return _get_stats()
    
    return _stats()

def optimize_performance():
    """立即执行性能优化，带有错误处理"""
    from packages.utils.Performance import optimize_now as _optimize
    
    @handle_exception(default_return=None, error_message="Failed to optimize performance")
    def _opt():
        return _optimize()
    
    return _opt()

def getdate():
    """获取当前日期，带有错误处理"""
    from packages.utils.GetTime import getdate as _getdate
    
    @handle_exception(default_return="unknown-date", error_message="Failed to get date")
    def _get():
        return _getdate()
    
    return _get()

def gettime():
    """获取当前时间，带有错误处理"""
    from packages.utils.GetTime import gettime as _gettime
    
    @handle_exception(default_return="unknown-time", error_message="Failed to get time")
    def _get():
        return _gettime()
    
    return _get()

def getdatetime():
    """获取当前日期时间，带有错误处理"""
    from packages.utils.GetTime import getdatetime as _getdatetime
    
    @handle_exception(default_return="unknown-datetime", error_message="Failed to get datetime")
    def _get():
        return _getdatetime()
    
    return _get()

def getLocalIP():
    """获取本地IP地址，带有错误处理"""
    from packages.utils.IPscanner import get_local_ip as _get_local_ip
    
    @handle_exception(default_return="127.0.0.1", error_message="Failed to get local IP")
    def _get():
        return _get_local_ip()
    
    return _get()

def scanIPs(network_range):
    """扫描指定网络范围内的IP，带有错误处理"""
    from packages.utils.IPscanner import scan_ips as _scan_ips
    
    @handle_exception(default_return=[], error_message="Failed to scan IPs")
    def _scan():
        return _scan_ips(network_range)
    
    return _scan()

def pathExists(path):
    """检查路径是否存在，带有错误处理"""
    from packages.utils.PathCheck import pathExists as _pathExists
    
    @handle_exception(default_return=False, error_message="Failed to check path existence")
    def _check():
        return _pathExists(path)
    
    return _check()

def checkAdm():
    """检查管理员权限，带有错误处理（别名方法）"""
    return AdmCheck()

def sysCheck():
    """检查系统信息，带有错误处理（别名方法）"""
    return SysCheck()

def clearScreen():
    """清屏，带有错误处理（别名方法）"""
    return Clear()

def openFile(filename, mode='r', **kwargs):
    """打开文件，带有错误处理"""
    from packages.utils.FileOperations import openFile as _openFile
    
    @handle_exception(default_return=None, error_message="Failed to open file")
    def _open():
        return _openFile(filename, mode, **kwargs)
    
    return _open()
