import os
from packages import UtilsManager as utils

def clearScreen():
    """跨平台清屏函数"""
    # 方法1: 尝试使用系统命令
    try:
        os.system("cls" if os.name == "nt" else "clear")
        return
    except:
        pass

    # 方法2: 使用 ANSI 转义序列
    try:
        print("\033[2J\033[H", end="", flush=True)
        utils.Log.warn("Your system may impose certain restrictions or modifications, causing some operations to fail.")
        return
    except:
        pass

    # 方法3: 打印多行空行
    print("\n" * 100)
    utils.Log.warn("Your system may impose certain restrictions or modifications, causing some operations to fail.")

