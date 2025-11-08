"""
清屏功能模块
提供跨平台的清屏功能，支持多种清屏方法
"""

import os
from packages import UtilsManager as utils


def clearScreen():
    """
    跨平台清屏函数
    尝试多种方法清屏，确保在不同环境下都能工作
    
    返回:
        None
    """
    # 方法1: 尝试使用系统命令
    try:
        os.system("cls" if os.name == "nt" else "clear")
        return
    except Exception as e:
        utils.Log.warn(f"Failed to clear screen using system command: {e}")

    # 方法2: 使用 ANSI 转义序列
    try:
        print("\033[2J\033[H", end="", flush=True)
        utils.Log.warn("Your system may impose certain restrictions or modifications, causing some operations to fail.")
        return
    except Exception as e:
        utils.Log.warn(f"Failed to clear screen using ANSI escape sequences: {e}")

    # 方法3: 打印多行空行
    try:
        print("\n" * 100)
        utils.Log.warn("Your system may impose certain restrictions or modifications, causing some operations to fail.")
    except Exception as e:
        utils.Log.error(f"Failed to clear screen using line breaks: {e}")

