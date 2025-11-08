"""
系统信息检查模块
用于获取当前操作系统的基本信息
"""

import platform
from packages.utils.ErrorHandler import handle_exception, SystemError


@handle_exception(SystemError, default_return={"name": "unknown"}, error_message="Failed to get system information")
def sysCheck():
    """
    获取当前操作系统的基本信息
    
    Returns:
        dict: 包含系统信息的字典，包含以下键:
            - name: 系统名称 ('windows', 'linux', 'darwin' 或 'unknown')
            - platform: 系统平台信息
            - version: 系统版本信息
            
    Raises:
        SystemError: 当系统检查过程中发生错误时抛出
    """
    try:
        # 获取系统名称
        system_name = platform.system().lower()
        
        # 标准化系统名称
        if system_name == "windows":
            name = "windows"
        elif system_name == "linux":
            name = "linux"
        elif system_name == "darwin":
            name = "darwin"  # macOS
        else:
            name = "unknown"
        
        # 返回系统信息
        return {
            "name": name,
            "platform": platform.platform(),
            "version": platform.version()
        }
    except Exception as e:
        raise SystemError(f"Error getting system information: {e}")


if __name__ == "__main__":
    # 测试代码
    system_info = sysCheck()
    print(f"System Name: {system_info['name']}")
    print(f"Platform: {system_info['platform']}")
    print(f"Version: {system_info['version']}")
