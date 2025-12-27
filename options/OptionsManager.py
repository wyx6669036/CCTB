"""
选项处理模块
负责处理用户选择的操作选项并执行相应功能
"""
from colorama import Fore, init

import CommandUI
import utils.UtilsManager as utils
from options.modules.M0 import _handle_kill_process
from options.modules.M1 import _handle_anti_full_screen
from options.modules.M2 import _handle_send_teacher_message
from options.modules.M3 import _handle_start_application
from utils.impl.ErrorHandler import handle_exception, ValidationError

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
    if not isinstance(choice, int) or choice < 0 or choice > len(CommandUI.options):
        utils.error(f"Invalid choice: {choice}.")
        raise ValidationError(f"Invalid choice: {choice}.")
    
    utils.info("Option selected: " + str(choice))
    
    try:
        match choice:
            case 0:
                _handle_kill_process()
            case 1:
                _handle_anti_full_screen()
            case 2:
                _handle_send_teacher_message()
            case 3:
                _handle_start_application()
    except KeyboardInterrupt:
        # 捕获并处理KeyboardInterrupt，直接返回到主菜单
        utils.info("\nOperation cancelled by user.")
        # 不重新抛出异常，让程序返回主菜单
    
    input(Fore.LIGHTYELLOW_EX + "\nPress Enter to continue..." + Fore.RESET)

