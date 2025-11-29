import win32api
import win32gui
import win32con
import win32process
import ctypes
import time
import threading
import sys
import os
from packages import UtilsManager as utils

# 全局配置
TOPMOST_INTERVAL = 120  # 自动前置间隔（秒）= 2分钟
FOCUS_LOCK_DURATION = 0.5  # 焦点锁定时间（秒）
CONSOLE_TITLE = "Auto-Topmost Console"  # 自定义窗口标题（避免中文乱码）

def get_console_handle():
    """获取当前命令行窗口句柄（多重方案确保找到）"""
    # 1. 按自定义标题查找（优先）
    hwnd = win32gui.FindWindow(None, CONSOLE_TITLE)
    if hwnd and win32gui.IsWindowVisible(hwnd):
        return hwnd

    # 2. 按默认标题查找（Python x.x.x - 脚本路径）
    default_title = f"Python {sys.version.split()[0]} - {os.path.abspath(sys.argv[0])}"
    hwnd = win32gui.FindWindow(None, default_title)
    if hwnd and win32gui.IsWindowVisible(hwnd):
        return hwnd

    # 3. 按进程ID枚举查找（兜底）
    pid = os.getpid()
    target_hwnd = None

    def enum_window_callback(win_hwnd, lparam):
        nonlocal target_hwnd
        if win32gui.IsWindowVisible(win_hwnd):
            _, window_pid = win32process.GetWindowThreadProcessId(win_hwnd)
            if window_pid == lparam:
                target_hwnd = win_hwnd
                return False  # 找到后停止枚举
        return True

    win32gui.EnumWindows(enum_window_callback, pid)
    return target_hwnd if target_hwnd and win32gui.IsWindowVisible(target_hwnd) else None

def force_foreground_and_focus(hwnd):
    """强制将窗口置于前台并锁定焦点"""
    if not hwnd:
        utils.info(f"Could not find window")
        return

    try:
        # 1. 先取消置顶再重新置顶（确保层级优先）
        win32gui.SetWindowPos(
            hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
        )
        win32gui.SetWindowPos(
            hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
        )

        # 2. 强制激活窗口（解决部分窗口激活失败问题）
        ctypes.windll.user32.AttachThreadInput(
            win32api.GetCurrentThreadId(),
            win32gui.GetWindowThreadProcessId(hwnd)[0],
            True
        )
        win32gui.SetForegroundWindow(hwnd)
        ctypes.windll.user32.AttachThreadInput(
            win32api.GetCurrentThreadId(),
            win32gui.GetWindowThreadProcessId(hwnd)[0],
            False
        )

        # 3. 锁定焦点（0.5秒内阻止焦点切换）
        utils.info(f"autoTop successfully")
        time.sleep(FOCUS_LOCK_DURATION)

    except Exception as e:
        utils.warn(f"autoTop failed")

def auto_topmost_loop():
    """定时前置窗口的循环线程"""
    hwnd = get_console_handle()
    if not hwnd:
        utils.warn("Could not find window!")
        return

    # 初始置顶
    win32gui.SetWindowPos(
        hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
    )

    # 定时循环
    while True:
        time.sleep(TOPMOST_INTERVAL)
        force_foreground_and_focus(hwnd)

def start():
    try:
        # 启动定时前置线程（不阻塞主线程，可添加自己的业务逻辑）
        topmost_thread = threading.Thread(target=auto_topmost_loop, daemon=True)
        topmost_thread.start()


    except KeyboardInterrupt:
        # 退出时取消置顶（可选）
        hwnd = get_console_handle()
        if hwnd:
            win32gui.SetWindowPos(
                hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
            )