"""
命令行用户界面模块
提供交互式菜单界面，支持键盘导航和选项选择
"""

import msvcrt
import os
import sys
from colorama import init, Fore, Style
from packages import UtilsManager as utils
from packages.utils.AppState import app_state
from packages.utils.UIManager import ui_manager
from packages.utils.SystemManager import system_manager
from packages.utils.NetworkManager import network_manager
from packages.utils.Exceptions import SystemException, ValidationException
from packages.utils.ErrorHandler import error_handler
from packages.utils.ThreadManager import thread_manager
from packages.utils.InteractionHelper import interaction_helper

init(autoreset=True)

texts = Fore.LIGHTBLUE_EX + """\
  ____ ____ _____ ____  
 / ___/ ___|_   _| __ ) 
| |  | |     | | |  _ \\ 
| |__| |___  | | | |_) |
 \\____\\____| |_| |____/  \n
""" + Fore.RED + """This project created by wyx6669036\n""" + Fore.RESET + "_"*60

def menu(selected_index):
    """
    显示菜单界面
    
    参数:
        selected_index (int): 当前选中的菜单项索引
        
    返回:
        None
    """
    utils.Clear()
    print(texts)
    print()
    
    # 从状态管理器获取菜单选项
    options = app_state.get("menu_options")

    for i, option in enumerate(options):
        # 获取选项文本
        option_text = option.get("text", f"Option {i}") if isinstance(option, dict) else str(option)
        
        if i == selected_index:
            # 使用加粗红色字体显示选中项
            print(Style.BRIGHT + Fore.LIGHTBLUE_EX + f"> {option_text}" + Style.RESET_ALL)
        else:
            print(f"  {option_text}")

    print("\n使用 ↑ ↓ 键选择，按 Enter 执行，按 'q' 退出")


def menu():
    """显示菜单并处理用户输入"""
    def _menu_loop():
        while True:
            # 清屏并显示菜单
            _display_menu()
            
            # 处理用户输入
            if not _handle_user_input():
                break
    
    error_handler.safe_execute(_menu_loop, context="Menu loop", 
                              default=lambda: ui_manager.display_message("Error in menu", "error"))


def _display_menu():
    """显示菜单界面"""
    # 清屏
    ui_manager.clear_screen()
    
    # 获取菜单选项和当前选中的索引
    options = ui_manager.get_menu_options()
    selected_index = app_state.get("selected_menu_index", 0)
    
    # 显示菜单
    ui_manager.display_menu()


def _handle_user_input() -> bool:
    """
    处理用户输入
    
    返回:
        bool: 是否继续运行菜单
    """
    # 获取菜单选项和当前选中的索引
    options = ui_manager.get_menu_options()
    selected_index = app_state.get("selected_menu_index", 0)
    
    # 处理用户输入
    key = msvcrt.getch()
    
    # 处理特殊按键
    if key == b'\x00':  # 箭头键前缀
        key = msvcrt.getch()
        return _handle_arrow_keys(key, selected_index, len(options))
    
    # 处理普通按键
    return _handle_regular_keys(key, selected_index, len(options))


def _handle_arrow_keys(key: bytes, selected_index: int, options_count: int) -> bool:
    """
    处理箭头键输入
    
    参数:
        key (bytes): 按键值
        selected_index (int): 当前选中的索引
        options_count (int): 选项总数
        
    返回:
        bool: 是否继续运行菜单
    """
    if key == b'H':  # 上箭头
        selected_index = (selected_index - 1) % options_count
        app_state.set("selected_menu_index", selected_index)
    elif key == b'P':  # 下箭头
        selected_index = (selected_index + 1) % options_count
        app_state.set("selected_menu_index", selected_index)
    
    return True


def _handle_regular_keys(key: bytes, selected_index: int, options_count: int) -> bool:
    """
    处理普通按键输入
    
    参数:
        key (bytes): 按键值
        selected_index (int): 当前选中的索引
        options_count (int): 选项总数
        
    返回:
        bool: 是否继续运行菜单
    """
    # Enter键
    if key == b'\r' or key == b'\n':
        ui_manager.handle_menu_selection(selected_index)
        interaction_helper.wait_for_keypress("Press Enter to continue...")
    
    # Q键退出
    elif key == b'q' or key == b'Q':
        return _handle_quit()
    
    return True


def _handle_quit() -> bool:
    """
    处理退出操作
    
    返回:
        bool: 是否继续运行菜单
    """
    # 检查是否有正在运行的线程
    running_threads = thread_manager.get_all_threads()
    if running_threads:
        if not interaction_helper.confirm_action("There are running threads. Are you sure you want to quit? (y/n): "):
            return True
    
    print("Exiting...")
    return False


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
        menu_options = ui_manager.get_menu_options()
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
        menu()
    
    error_handler.safe_execute(_main_internal, context="CommandUI main", 
                              default=lambda: (print(f"Error starting CommandUI"), 
                                             sys.exit(1)))

if __name__ == "__main__":
    main()