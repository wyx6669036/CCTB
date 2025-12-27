import win32gui
import win32con
import sys
import os
from utils import UtilsManager as utils


def set_console_topmost(enable: bool = True):
    """
    设置命令行窗口置顶/取消置顶
    :param enable: True=置顶，False=取消置顶
    """
    # 获取当前命令行窗口的句柄（关键：通过进程ID定位窗口）
    console_title = f"Python {sys.version.split()[0]} - {os.path.abspath(sys.argv[0])}"
    hwnd = win32gui.FindWindow(None, console_title)

    if not hwnd:
        # 若未找到窗口（可能是交互式环境或标题被修改），尝试通过进程ID查找
        import win32process

        # 获取当前进程ID
        pid = os.getpid()
        hwnd = None

        def enum_windows_callback(win_hwnd, pid):
            nonlocal hwnd  # 引用外层的 hwnd 变量
            # 检查窗口是否属于目标进程，且是可见的命令行窗口
            if win32gui.IsWindowVisible(win_hwnd):
                _, window_pid = win32process.GetWindowThreadProcessId(win_hwnd)
                if window_pid == pid:
                    hwnd = win_hwnd  # 将找到的窗口句柄赋值给外层 hwnd
                    return False  # 找到后停止枚举
            return True

        # 枚举所有窗口，匹配当前进程ID
        win32gui.EnumWindows(enum_windows_callback, pid)

    if not hwnd:
        utils.warn("Could not find window!")
        return

    # 设置窗口置顶属性（HWND_TOPMOST = -1 表示始终置顶）
    if enable:
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,  # 置顶层级（-1）
            0, 0, 0, 0,  # x, y, 宽, 高（0表示不改变）
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE  # 仅修改置顶属性，不移动/缩放窗口
        )
        utils.info("forceTop successfully")
    else:
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_NOTOPMOST,  # 取消置顶（-2）
            0, 0, 0, 0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
        )