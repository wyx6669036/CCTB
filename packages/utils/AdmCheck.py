"""
管理员权限检查模块
用于检查当前程序是否以管理员权限运行
"""

import ctypes
import os
from packages.utils import SysCheck
from packages.utils.ErrorHandler import handle_exception, PermissionError


@handle_exception(PermissionError, default_return=False, error_message="Failed to check administrator privileges")
def checkAdm():
    """
    检查当前程序是否以管理员权限运行
    
    Returns:
        bool: 如果是管理员权限返回True，否则返回False
        
    Note:
        - Windows系统使用ctypes.windll.shell32.IsUserAnAdmin()检查
        - Linux和macOS系统通过检查用户ID是否为0(root)来判断
        - 其他系统默认返回False
        
    Raises:
        PermissionError: 当权限检查过程中发生错误时抛出
    """
    system = SysCheck.sysCheck()
    try:
        if system["name"] == "windows":
            # Windows系统检查管理员权限
            if ctypes.windll.shell32.IsUserAnAdmin() == 1:
                return True
            else:
                return False
        elif system["name"] == "linux" or SysCheck.sysCheck()["name"] == "darwin":
            # Linux和macOS系统检查root权限
            return os.getuid() == 0
        else:
            # 其他系统默认返回False
            return False
    except Exception as e:
        print(f"Error: {e}")
        raise PermissionError(f"Error checking administrator privileges: {e}")