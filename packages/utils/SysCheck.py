"""
系统信息检查模块
获取当前运行系统的基本信息，包括系统名称和版本
"""

import platform


def sysCheck():
    """
    获取当前系统信息
    
    返回:
        dict: 包含系统名称和版本的字典
            - name: 系统名称 ("windows", "linux", "macos")
            - version: 系统版本号
            
    异常:
        ValueError: 当系统不受支持时抛出异常
    """
    system = platform.system()

    if system == 'Windows':
        return {"name": "windows", "version": platform.release()}
    elif system == 'Linux':
        return {"name": "linux", "version": platform.release()}
    elif system == 'Darwin':
        return {"name": "macos", "version": platform.release()}
    else:
        raise ValueError(f"Unsupported system: {system}")
