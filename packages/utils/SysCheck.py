import platform

"""
检查系统版本工具
使用方法：
import packages.UtilsManager as utils
utils.SysCheck()

返回值：json
eg.:{"name":"windows","version":"11"}
"""

def sysCheck():
    system = platform.system()

    if system == 'Windows':
        return {"name": "windows", "version": platform.release()}
    elif system == 'Linux':
        return {"name": "linux", "version": platform.release()}
    elif system == 'Darwin':
        return {"name": "macos", "version": platform.release()}
    else:
        raise ValueError(f"Unsupported system: {system}")
