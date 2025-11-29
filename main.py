import ctypes
import sys
import os
import time
from packages import UtilsManager as utils
from packages.utils.ErrorHandler import handle_exception, SystemError, PermissionError
from packages.utils.ConfigManager import config
from packages.utils.Performance import initialize_performance_manager, start_performance_monitoring, stop_performance_monitoring
from packages.bypass.forceTop import set_console_topmost
from packages.bypass import autoTop


@handle_exception(SystemError, reraise=True, error_message="Application failed to start")
def main():
    """
    主函数，负责程序初始化和启动
    
    流程:
    1. 检查管理员权限，如果没有则尝试以管理员身份重新启动
    2. 初始化日志文件
    3. 显示程序信息
    4. 启动命令行界面
    5. 程序退出时清理资源
    """
    # 强制窗口置顶
    set_console_topmost(enable=True)
    # 定时锁焦点
    autoTop.start()

    # 检查管理员权限
    if not utils.AdmCheck():
        if utils.SysCheck()["name"] == "windows":
            # Windows系统下以管理员身份重新启动程序
            try:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, os.path.abspath(__file__), None, 1)
                sys.exit(0)
            except Exception as e:
                utils.error(f"Failed to restart with administrator privileges: {e}")
                raise PermissionError(f"Failed to restart with administrator privileges: {e}")
        else:
            # 非Windows系统不支持
            utils.error("This program must be run in Windows.")
            raise SystemError("This program must be run in Windows.")

    # 初始化日志文件
    try:
        from packages.utils import AdvancedLog
        with open(AdvancedLog.log_file, "w", encoding="ANSI") as f:
            f.truncate(0)
    except Exception as e:
        utils.error(f"Failed to initialize log file: {e}")

    # 显示程序信息
    utils.info("Starting...")
    import CommandUI
    utils.info("version : " + CommandUI.version)
    utils.info("runningDir : " + CommandUI.runningDir)
    
    # 初始化性能监控
    try:
        initialize_performance_manager()
        
        # 根据配置决定是否启用性能监控
        enable_perf_monitor = config.get("performance_monitoring", True)
        if enable_perf_monitor:
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

    # 启动命令行界面
    try:
        CommandUI.main()
    except KeyboardInterrupt:
        # 捕获Ctrl+C信号，优雅退出
        utils.info("Operation cancelled by user")
    except Exception as e:
        utils.error(f"Failed to start command UI: {e}")
        raise SystemError(f"Failed to start command UI: {e}")
    
    # 程序退出
    utils.info("Exiting...")
    # 取消置顶
    set_console_topmost(enable=False)
    
    # 停止性能监控
    try:
        stop_performance_monitoring()
        utils.info("Performance monitoring stopped")
    except Exception as e:
        utils.error(f"Failed to stop performance monitoring: {e}")
        
    utils.info("bye!")
    sys.exit(0)


if __name__ == "__main__":
    main()
