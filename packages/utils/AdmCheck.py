import ctypes
import os
from packages.utils import SysCheck

"""
使用方法：
import packages.UtilsManager as utils
utils.AdmCheck

返回值：True/False
"""

def checkAdm():
    system = SysCheck.sysCheck()
    try:
        if system["name"] == "windows":
            if ctypes.windll.shell32.IsUserAnAdmin() == 1:
                return True
            else:
                return False
        elif system["name"] == "linux" or SysCheck.sysCheck()["name"] == "darwin":
            return os.getuid() == 0
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")