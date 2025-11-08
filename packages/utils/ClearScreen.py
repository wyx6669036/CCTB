import os
from packages import UtilsManager as utils

"""
使用方法：
import packages.UtilsManager as utils
utils.Clear

返回值：None
清屏处理：
1.若可以使用cls，首先尝试cls
2.尝试使用unicode转译字符
3.换号

注意：后面两种若使用，基本可以说是系统有较大限制，整个程序不保证能正常运行
"""

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
        utils.warn("Your system may impose certain restrictions or modifications, causing some operations to fail.")
        return
    except:
        pass

    # 方法3: 打印多行空行
    print("\n" * 100)
    utils.warn("Your system may impose certain restrictions or modifications, causing some operations to fail.")

