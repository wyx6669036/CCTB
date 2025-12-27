"""
选项处理模块
负责处理用户选择的操作选项并执行相应功能
"""

import utils.UtilsManager as utils
from colorama import Fore, init
from utils.impl.ErrorHandler import handle_exception, SystemError, ValidationError

from modules.M0 import _handle_kill_process
from modules.M1 import _handle_anti_full_screen
from modules.M2 import _handle_send_teacher_message

# 初始化colorama，确保颜色重置
init(autoreset=True)


@handle_exception(ValidationError, default_return=None, error_message="Invalid option selected")
def selectOption(choice):
    """
    处理用户选择的操作选项
    
    Args:
        choice (int): 用户选择的选项编号
        
    Options:
        0: 强制结束studentmain.exe进程
        1: 启动反全屏模块
        2: 发送教师消息
    """
    # 验证输入
    if not isinstance(choice, int) or choice < 0 or choice > 2:
        raise ValidationError(f"Invalid choice: {choice}. Must be 0, 1, or 2.")
    
    utils.info("Option selected: " + str(choice))
    
    try:
        if choice == 0:
            _handle_kill_process()
        elif choice == 1:
            _handle_anti_full_screen()
        elif choice == 2:
            _handle_send_teacher_message()
    except KeyboardInterrupt:
        # 捕获并处理KeyboardInterrupt，直接返回到主菜单
        utils.info("\nOperation cancelled by user.")
        # 不重新抛出异常，让程序返回主菜单
    
    input(Fore.LIGHTYELLOW_EX + "\nPress Enter to continue..." + Fore.RESET)

