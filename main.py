"""
主程序入口
负责初始化程序、检查管理员权限、设置日志文件并启动UI界面
"""

import ctypes
import sys
import os
import threading
import CommandUI
# 导入自定义模块
from packages import UtilsManager as utils
from packages.utils.AppState import app_state
from packages.utils.Config import config
from packages.utils.SystemManager import system_manager
from packages.utils.UIManager import ui_manager
from packages.utils.NetworkManager import network_manager
from packages.utils.Exceptions import SystemException, ValidationException
from packages.utils.ErrorHandler import error_handler
from packages.utils.ThreadManager import thread_manager
from packages.utils.InteractionHelper import interaction_helper


def main():
    """主函数"""
    def _main_internal():
        # 初始化应用状态
        running_dir = os.path.dirname(os.path.abspath(__file__))
        tools_dir = os.path.join(running_dir, "tools")
        app_state.set("running_dir", running_dir)
        app_state.set("tools_dir", tools_dir)
        
        # 设置版本号
        app_state.set("version", "1.0.0")
        
        # 加载配置
        menu_options = config.get_menu_options()
        app_state.set("menu_options", menu_options)
        
        # 初始化UI状态
        app_state.set("selected_menu_index", 0)
        
        # 打印启动信息
        ui_manager.print_startup_info()
        
        # 检查管理员权限
        if system_manager.check_admin_privileges():
            app_state.set("admin_privileges", True)
            ui_manager.display_message("Admin privileges detected", "success")
        else:
            app_state.set("admin_privileges", False)
            ui_manager.display_message("Running without admin privileges", "warning")
        
        # 启动命令行界面
        CommandUI.menu()
    
    error_handler.safe_execute(_main_internal, context="Main application initialization", 
                              default=lambda: (print(f"Error starting application"), 
                                             sys.exit(1)))


def _initialize_log_file():
    """
    初始化日志文件
    删除旧的日志文件并创建新的空日志文件
    """
    def _init_log_internal():
        # 如果日志文件存在，则删除
        if os.path.exists("log.txt"):
            os.remove("log.txt")
        
        # 创建新的空日志文件
        with open("log.txt", "x", encoding="ANSI") as f:
            f.write("")
    
    error_handler.safe_execute(_init_log_internal, context="Initializing log file", 
                              default=lambda: utils.error("Failed to initialize log file"))


def _print_startup_info():
    """
    输出程序启动信息
    包括版本号和运行目录
    """
    utils.info("Starting...")
    utils.info("version : " + app_state.get("version"))
    utils.info("runningDir : " + app_state.get("running_dir"))


def _start_ui():
    """
    启动UI界面
    在新线程中运行UI主循环
    """
    def _start_ui_internal():
        # 使用线程管理器启动UI线程
        thread_id = thread_manager.start_thread(
            target=CommandUI.main,
            thread_name="ui_thread",
            daemon=True
        )
        
        if thread_id:
            # 等待UI线程结束
            thread_manager.wait_for_thread("ui_thread")
            
            utils.info("Exiting...")
            utils.info("bye!")
            sys.exit(0)
        else:
            utils.error("Failed to start UI thread")
            sys.exit(1)
    
    error_handler.safe_execute(_start_ui_internal, context="Starting UI", 
                              default=lambda: (utils.error("Error starting UI"), 
                                             sys.exit(1)))


# 调试模式开关，release请关闭
DEBUG = True  

if __name__ == "__main__":
    main()
