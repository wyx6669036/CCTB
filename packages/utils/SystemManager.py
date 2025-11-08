"""
系统操作模块
集中管理系统相关的功能，包括权限检查、进程管理和系统信息获取
"""

import os
import sys
import ctypes
import subprocess
from typing import Dict, Any, Optional
from packages.utils.AppState import app_state
from packages.utils.Config import config
from packages.utils.Log import error, info, debug
from packages.utils.Exceptions import SystemException, ValidationException
from packages.utils.ErrorHandler import error_handler


class SystemManager:
    """
    系统管理器类
    提供系统信息获取、权限检查和进程管理功能
    """
    
    @staticmethod
    def check_admin_privileges() -> bool:
        """
        检查当前进程是否具有管理员权限
        
        返回:
            bool: 是否具有管理员权限
        """
        return error_handler.safe_execute(
            lambda: __import__('packages.utils.AdmCheck', fromlist=['checkAdm']).checkAdm(),
            context="Checking admin privileges",
            default=False
        )
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """
        获取系统信息
        
        返回:
            Dict[str, Any]: 系统信息字典
            
        异常:
            SystemException: 当获取系统信息失败时抛出异常
        """
        result = error_handler.safe_execute(
            lambda: __import__('packages.utils.SysCheck', fromlist=['sysCheck']).sysCheck(),
            context="Getting system info",
            default=None
        )
        if result is None:
            raise SystemException("Failed to get system information")
        return result
    
    @staticmethod
    def is_windows() -> bool:
        """
        检查当前系统是否为Windows
        
        返回:
            bool: 当前系统是否为Windows
        """
        try:
            system_info = SystemManager.get_system_info()
            return system_info.get("name", "").lower() == "windows"
        except Exception:
            # 如果获取系统信息失败，使用默认方法
            return sys.platform.startswith('win')
    
    @staticmethod
    def restart_as_admin() -> None:
        """
        以管理员身份重新启动当前程序
        
        异常:
            SystemException: 当重新启动失败时抛出异常
        """
        if not SystemManager.is_windows():
            raise SystemException("This operation is only supported on Windows")
        
        def _restart_admin():
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", 
                sys.executable, 
                os.path.abspath(__file__), 
                None, 1
            )
        
        result = error_handler.safe_execute(
            _restart_admin,
            context="Restarting with admin privileges",
            default=None
        )
        if result is None:
            raise SystemException("Failed to restart with admin privileges")
    
    @staticmethod
    def run_with_system_privileges(command: str, arguments: str = "") -> None:
        """
        以系统权限运行命令
        
        参数:
            command (str): 要执行的命令
            arguments (str): 命令参数
            
        异常:
            ValidationException: 当参数无效时抛出异常
            SystemException: 当执行失败时抛出异常
        """
        if not command:
            raise ValidationException("Command cannot be empty", field_name="command", field_value=command)
        
        if not SystemManager.is_windows():
            raise SystemException("This operation is only supported on Windows")
        
        running_dir = app_state.get("running_dir")
        if not running_dir:
            raise SystemException("Running directory not set in app state")
        
        def _run_with_privileges():
            # 使用PsExec以系统权限运行命令
            psexec_path = config.get_resource_path("psexec", running_dir)
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", 
                psexec_path, 
                f" -s -accepteula {command} {arguments}", 
                None, 0
            )
            info(f"Command executed with system privileges: {command}")
        
        result = error_handler.safe_execute(
            _run_with_privileges,
            context=f"Running command with system privileges: {command}",
            default=None
        )
        if result is None:
            raise SystemException("Failed to run command with system privileges")
    
    @staticmethod
    def kill_process(process_name: str) -> None:
        """
        结束指定名称的进程
        
        参数:
            process_name (str): 进程名称
            
        异常:
            ValidationException: 当参数无效时抛出异常
            SystemException: 当结束进程失败时抛出异常
        """
        if not process_name:
            raise ValidationException("Process name cannot be empty", field_name="process_name", field_value=process_name)
        
        running_dir = app_state.get("running_dir")
        if not running_dir:
            raise SystemException("Running directory not set in app state")
        
        def _kill_process():
            # 使用系统权限运行taskkill结束进程
            taskkill_path = config.get_resource_path("taskkill", running_dir)
            SystemManager.run_with_system_privileges(
                taskkill_path, 
                f"/F /IM {process_name}"
            )
            info(f"Process killed: {process_name}")
        
        result = error_handler.safe_execute(
            _kill_process,
            context=f"Killing process: {process_name}",
            default=None
        )
        if result is None:
            raise SystemException(f"Failed to kill process {process_name}")
    
    @staticmethod
    def start_application(path: str) -> None:
        """
        启动应用程序
        
        参数:
            path (str): 应用程序路径
            
        异常:
            ValidationException: 当参数无效时抛出异常
            SystemException: 当启动应用程序失败时抛出异常
        """
        if not path or not isinstance(path, str):
            raise ValidationException("Invalid application path", field_name="path", field_value=path)
        
        if not os.path.exists(path):
            raise ValidationException(f"Application does not exist: {path}", field_name="path", field_value=path)
        
        def _start_app():
            subprocess.Popen([path])
            info(f"Application started: {path}")
        
        result = error_handler.safe_execute(
            _start_app,
            context=f"Starting application: {path}",
            default=None
        )
        if result is None:
            raise SystemException(f"Failed to start application {path}")
    
    @staticmethod
    def clear_screen() -> None:
        """
        清空控制台屏幕
        
        返回:
            None
        """
        def _clear_screen():
            from packages.utils.ClearScreen import clearScreen
            clearScreen()
        
        result = error_handler.safe_execute(
            _clear_screen,
            context="Clearing screen",
            default=None
        )
        if result is None:
            # 使用备用方法清屏
            error_handler.safe_execute(
                lambda: os.system('cls' if os.name == 'nt' else 'clear'),
                context="Clearing screen with fallback method"
            )


# 创建全局系统管理器实例
system_manager = SystemManager()