"""
CCTB主程序入口 - 测试版本
用于启动应用程序并处理管理员权限检查
"""

import ctypes
import sys
import os
import signal
import threading
import CommandUI
from packages import UtilsManager as utils
from packages.utils.ErrorHandler import handle_exception, SystemError, PermissionError
from packages.utils.ConfigManager import config
from packages.utils.Performance import initialize_performance_manager, start_performance_monitoring, stop_performance_monitoring


# 设置信号处理函数
def signal_handler(sig, frame):
    """处理Ctrl+C信号"""
    utils.info("Received interrupt signal, stopping all threads...")
    try:
        # 停止所有可能运行的线程
        from packages.options import stop_module2
        stop_module2()
        utils.info("All threads stopped. Exiting...")
    except Exception as e:
        utils.error(f"Error stopping threads: {e}")
    finally:
        sys.exit(0)


@handle_exception(SystemError, reraise=True, error_message="Application failed to start")
def main():
    """
    主函数，负责程序初始化和启动
    
    流程:
    1. 检查管理员权限，如果没有则尝试以管理员身份重新启动
    2. 初始化日志文件
    3. 显示程序信息
    4. 注册信号处理函数
    5. 启动命令行界面线程
    6. 等待线程结束并退出程序
    """
    # 注册信号处理函数
    signal.signal(signal.SIGINT, signal_handler)
    
    # 跳过管理员权限检查，直接继续
    print("Skipping administrator check for testing...")
    
    # 初始化日志文件
    # 先删除旧的日志文件，然后创建新的空日志文件
    try:
        if os.path.exists("log.txt"):
            os.remove("log.txt")
        with open("log.txt", "x", encoding="ANSI") as f:
            f.write("")
    except Exception as e:
        utils.error(f"Failed to initialize log file: {e}")
        # 不抛出异常，继续运行程序

    # 显示程序信息
    utils.info("Starting...")
    utils.info("version : " + CommandUI.version)
    utils.info("runningDir : " + CommandUI.runningDir)
    
    # 初始化性能监控
    try:
        initialize_performance_manager()
        
        # 根据配置决定是否启用性能监控
        enable_perf_monitor = config.get("performance_monitoring", True)
        if enable_perf_monitor:
            # 获取性能监控配置
            monitor_interval = config.get("performance_monitor_interval", 5.0)
            auto_optimize = config.get("performance_auto_optimize", True)
            optimize_interval = config.get("performance_optimize_interval", 30.0)
            
            start_performance_monitoring(
                interval=monitor_interval,
                auto_optimize=auto_optimize,
                optimize_interval=optimize_interval
            )
            utils.info(f"Performance monitoring enabled (interval: {monitor_interval}s)")
    except Exception as e:
        utils.error(f"Failed to initialize performance monitoring: {e}")
        # 不抛出异常，继续运行程序

    # 启动命令行界面线程
    try:
        Thread = threading.Thread(target=CommandUI.main, daemon=True)
        Thread.start()
        Thread.join()
    except Exception as e:
        utils.error(f"Failed to start command UI: {e}")
        raise SystemError(f"Failed to start command UI: {e}")
    
    # 程序退出
    utils.info("Exiting...")
    
    # 停止性能监控
    try:
        stop_performance_monitoring()
        utils.info("Performance monitoring stopped")
    except Exception as e:
        utils.error(f"Failed to stop performance monitoring: {e}")
        
    utils.info("bye!")
    sys.exit(0)

# 从配置管理器获取调试标志
DEBUG = config.get("debug", False)  

if __name__ == "__main__":
    main()