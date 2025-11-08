"""
InteractionHelper
提供统一的用户交互机制，减少代码重复
"""

import time
import msvcrt
from typing import List, Dict, Any, Optional, Callable
from packages.utils.UIManager import ui_manager
from packages.utils.ErrorHandler import error_handler


class InteractionHelper:
    """统一的用户交互类"""
    
    @staticmethod
    def get_user_input(prompt: str, validator: Optional[Callable] = None, 
                      error_message: str = "Invalid input, please try again") -> str:
        """
        获取用户输入，支持验证
        
        参数:
            prompt (str): 提示信息
            validator (Optional[Callable]): 验证函数，返回True表示验证通过
            error_message (str): 验证失败时的错误信息
            
        返回:
            str: 用户输入
        """
        while True:
            try:
                user_input = input(prompt).strip()
                
                # 如果提供了验证函数，则进行验证
                if validator and not validator(user_input):
                    ui_manager.display_message(error_message, "error")
                    continue
                    
                return user_input
                
            except Exception as e:
                error_handler.handle_exception(e, "Getting user input")
                ui_manager.display_message("Error reading input, please try again", "error")
    
    @staticmethod
    def get_menu_choice(options: List[Dict[str, Any]], prompt: str = "Please select an option") -> int:
        """
        获取菜单选择
        
        参数:
            options (List[Dict[str, Any]]): 选项列表
            prompt (str): 提示信息
            
        返回:
            int: 选择的选项索引
        """
        # 显示选项
        for i, option in enumerate(options):
            ui_manager.display_message(f"{i}. {option.get('name', 'Unknown')}")
            
        # 获取用户选择
        while True:
            try:
                choice = input(f"{prompt} (0-{len(options)-1}): ")
                choice_index = int(choice)
                
                if 0 <= choice_index < len(options):
                    return choice_index
                    
                ui_manager.display_message(f"Please enter a number between 0 and {len(options)-1}", "error")
                
            except ValueError:
                ui_manager.display_message("Please enter a valid number", "error")
            except Exception as e:
                error_handler.handle_exception(e, "Getting menu choice")
                ui_manager.display_message("Error processing choice, please try again", "error")
    
    @staticmethod
    def confirm_action(prompt: str = "Are you sure? (y/n): ") -> bool:
        """
        确认用户操作
        
        参数:
            prompt (str): 确认提示信息
            
        返回:
            bool: 用户是否确认
        """
        while True:
            try:
                choice = input(prompt).strip().lower()
                return choice in ['y', 'yes']
            except Exception as e:
                error_handler.handle_exception(e, "Confirming action")
                return False
    
    @staticmethod
    def wait_for_keypress(keys: List[bytes] = None, timeout: Optional[float] = None) -> Optional[bytes]:
        """
        等待按键
        
        参数:
            keys (List[bytes]): 要等待的按键列表，None表示任意按键
            timeout (Optional[float]): 超时时间（秒），None表示无限等待
            
        返回:
            Optional[bytes]: 按下的键，超时返回None
        """
        start_time = None
        
        if timeout is not None:
            start_time = time.time()
            
        while True:
            # 检查超时
            if start_time and (time.time() - start_time) > timeout:
                return None
                
            # 检查是否有按键
            if msvcrt.kbhit():
                key = msvcrt.getch()
                
                # 处理特殊键
                if key == b'\x00':  # 特殊键前缀
                    key = msvcrt.getch()
                    
                # 如果指定了按键列表，检查是否匹配
                if keys is None or key in keys:
                    return key
                    
            # 短暂休眠，避免CPU占用过高
            time.sleep(0.01)
    
    @staticmethod
    def navigate_menu(options: List[Dict[str, Any]], initial_selection: int = 0) -> int:
        """
        使用键盘导航菜单
        
        参数:
            options (List[Dict[str, Any]]): 选项列表
            initial_selection (int): 初始选中的索引
            
        返回:
            int: 最终选择的选项索引
        """
        selected_index = initial_selection
        
        while True:
            # 显示菜单
            ui_manager.clear_screen()
            
            for i, option in enumerate(options):
                # 高亮显示选中项
                if i == selected_index:
                    ui_manager.display_message(f"> {option.get('name', 'Unknown')} <", "highlight")
                else:
                    ui_manager.display_message(f"  {option.get('name', 'Unknown')}")
            
            # 等待用户输入
            key = InteractionHelper.wait_for_keypress([b'\x00', b'\r', b'\n', b'q', b'Q'])
            
            if key is None:
                continue
                
            # 处理特殊键
            if key == b'\x00':  # 箭头键前缀
                arrow_key = InteractionHelper.wait_for_keypress([b'H', b'P'], timeout=0.1)
                if arrow_key == b'H':  # 上箭头
                    selected_index = (selected_index - 1) % len(options)
                elif arrow_key == b'P':  # 下箭头
                    selected_index = (selected_index + 1) % len(options)
                    
            # Enter键确认选择
            elif key == b'\r' or key == b'\n':
                return selected_index
                
            # Q键退出
            elif key == b'q' or key == b'Q':
                return -1


# 创建全局交互助手实例
interaction_helper = InteractionHelper()