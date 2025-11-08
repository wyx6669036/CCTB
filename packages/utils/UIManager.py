"""
用户界面模块
集中管理UI相关的功能，包括菜单显示、用户输入和界面交互
"""

import os
import sys
from typing import List, Dict, Any, Optional, Callable
from packages.utils.AppState import app_state
from packages.utils.Config import config
from packages.utils.Log import error, info, debug
from packages.utils.ErrorHandler import error_handler
from packages.utils.Exceptions import ValidationException, SystemException


class UIManager:
    """
    用户界面管理器类
    提供菜单显示、用户输入和界面交互功能
    """
    
    @staticmethod
    def clear_screen() -> None:
        """
        清空控制台屏幕
        
        返回:
            None
        """
        try:
            from packages.utils.ClearScreen import clearScreen
            clearScreen()
        except Exception as e:
            error_handler.handle_exception(e, "Failed to clear screen")
            # 使用备用方法清屏
            os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_startup_info() -> None:
        """
        打印启动信息
        
        返回:
            None
        """
        version = app_state.get("version", "Unknown")
        running_dir = app_state.get("running_dir", "Unknown")
        print(f"Version: {version}")
        print(f"Running in: {running_dir}")
    
    @staticmethod
    def get_menu_options() -> List[Dict[str, Any]]:
        """
        获取菜单选项
        
        返回:
            List[Dict[str, Any]]: 菜单选项列表
        """
        return app_state.get("menu_options", [])
    
    @staticmethod
    def display_menu() -> None:
        """
        显示菜单
        
        返回:
            None
        """
        options = UIManager.get_menu_options()
        selected_index = app_state.get("selected_menu_index", 0)
        
        try:
            from packages.utils.Color import colorama as c
        except ImportError:
            # 如果colorama不可用，使用普通输出
            c = None
        
        print("\n" + "="*40)
        print("CCTB - Classroom Control Tool Box")
        print("="*40)
        
        for i, option in enumerate(options):
            text = option.get("text", f"Option {i}")
            if i == selected_index:
                if c:
                    print(f"{c.Fore.GREEN} > {text}{c.Style.RESET_ALL}")
                else:
                    print(f" > {text}")
            else:
                print(f"   {text}")
        
        print("="*40)
        print("Use arrow keys to navigate, Enter to select, Q to quit")
    
    @staticmethod
    def get_user_input(prompt: str = "") -> str:
        """
        获取用户输入
        
        参数:
            prompt (str): 提示信息
            
        返回:
            str: 用户输入
        """
        try:
            from packages.utils.Color import colorama as c
        except ImportError:
            c = None
        
        if c:
            return input(f"{c.Fore.CYAN}{prompt}{c.Style.RESET_ALL}")
        else:
            return input(prompt)
    
    @staticmethod
    def display_message(message: str, message_type: str = "info") -> None:
        """
        显示消息
        
        参数:
            message (str): 消息内容
            message_type (str): 消息类型 (info, success, warning, error)
            
        返回:
            None
        """
        try:
            from packages.utils.Color import colorama as c
        except ImportError:
            c = None
        
        prefix = ""
        if c:
            if message_type == "success":
                prefix = f"{c.Fore.GREEN}[SUCCESS] "
            elif message_type == "warning":
                prefix = f"{c.Fore.YELLOW}[WARNING] "
            elif message_type == "error":
                prefix = f"{c.Fore.RED}[ERROR] "
            else:
                prefix = f"{c.Fore.CYAN}[INFO] "
            
            print(f"{prefix}{message}{c.Style.RESET_ALL}")
        else:
            if message_type == "success":
                prefix = "[SUCCESS] "
            elif message_type == "warning":
                prefix = "[WARNING] "
            elif message_type == "error":
                prefix = "[ERROR] "
            else:
                prefix = "[INFO] "
            
            print(f"{prefix}{message}")
    
    @staticmethod
    def handle_menu_selection(selected_index: int) -> None:
        """
        处理菜单选择
        
        参数:
            selected_index (int): 选中的菜单索引
            
        返回:
            None
        """
        options = UIManager.get_menu_options()
        if 0 <= selected_index < len(options):
            selected_option = options[selected_index]
            option_name = selected_option.get("name", f"option_{selected_index}")
            action = selected_option.get("action")
            
            if action:
                try:
                    # 执行菜单项对应的操作
                    if callable(action):
                        action()
                    else:
                        UIManager.display_message(f"Executing: {option_name}", "info")
                        # 这里可以根据实际需求扩展，例如调用特定的函数
                except Exception as e:
                    error_handler.handle_exception(e, f"Failed to execute menu option {option_name}")
                    UIManager.display_message(f"Failed to execute: {option_name}", "error")
            else:
                UIManager.display_message(f"Selected: {option_name}", "info")
    
    @staticmethod
    def confirm_action(prompt: str = "Are you sure? (y/n): ") -> bool:
        """
        确认操作
        
        参数:
            prompt (str): 确认提示
            
        返回:
            bool: 用户是否确认
        """
        response = UIManager.get_user_input(prompt).lower()
        return response in ('y', 'yes', '是')
    
    @staticmethod
    def select_option(options: List[str], prompt: str = "Select an option:") -> int:
        """
        从选项列表中选择一个选项
        
        参数:
            options (List[str]): 选项列表
            prompt (str): 提示信息
            
        返回:
            int: 选中的选项索引
            
        异常:
            ValidationException: 当选项列表为空时抛出异常
        """
        if not options:
            raise ValidationException("Options list cannot be empty", field_name="options", field_value=options)
        
        while True:
            UIManager.display_message(prompt, "info")
            for i, option in enumerate(options):
                print(f"  {i+1}. {option}")
            
            try:
                choice = int(UIManager.get_user_input("Enter option number: "))
                if 1 <= choice <= len(options):
                    return choice - 1
                else:
                    UIManager.display_message("Invalid option number. Please try again.", "warning")
            except ValueError:
                UIManager.display_message("Please enter a valid number.", "warning")


# 创建全局UI管理器实例
ui_manager = UIManager()