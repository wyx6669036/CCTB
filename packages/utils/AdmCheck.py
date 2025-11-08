"""
管理员权限检查模块
用于检查当前程序是否以管理员权限运行
支持Windows、Linux和macOS系统
"""

import ctypes
import os
from packages.utils import SysCheck


def checkAdm():
    """
    检查当前程序是否以管理员权限运行
    
    返回:
        bool: 如果具有管理员权限返回True，否则返回False
        
    异常:
        Exception: 当检查过程中发生错误时捕获并打印错误信息
    """
    system = SysCheck.sysCheck()
    try:
        if system["name"] == "windows":
            # Windows系统使用ctypes检查管理员权限
            return ctypes.windll.shell32.IsUserAnAdmin() == 1
        elif system["name"] in ["linux", "macos"]:
            # Linux和macOS系统检查用户ID是否为0（root）
            return os.getuid() == 0
        else:
            # 不支持的系统返回False
            return False
    except Exception as e:
        print(f"Error checking admin privileges: {e}")
        return False