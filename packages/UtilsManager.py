"""
UtilsManager
提供工具模块的统一管理，解决循环依赖问题
"""

import threading
import time
from typing import Dict, Any, Optional, Callable
from packages.utils.ErrorHandler import error_handler
from packages.utils.ThreadManager import thread_manager
from packages.utils.InteractionHelper import interaction_helper


class UtilsManager:
    """工具管理器"""
    
    def __init__(self):
        """初始化工具管理器"""
        self._modules = {}
        self._app_state = None
        self._config = None
        self._logger = error_handler.logger
        self._lock = threading.Lock()
    
    def get_app_state(self) -> Dict[str, Any]:
        """
        获取应用状态
        
        返回:
            Dict[str, Any]: 应用状态
        """
        if self._app_state is None:
            try:
                from packages.utils.AppState import app_state
                self._app_state = app_state
            except ImportError:
                self._app_state = {}
                error_handler.handle_exception(
                    ImportError("Cannot import AppState"),
                    "Getting app state"
                )
        
        return self._app_state
    
    def get_config(self) -> Dict[str, Any]:
        """
        获取配置
        
        返回:
            Dict[str, Any]: 配置
        """
        if self._config is None:
            try:
                from packages.utils.Config import config
                self._config = config
            except ImportError:
                self._config = {}
                error_handler.handle_exception(
                    ImportError("Cannot import Config"),
                    "Getting config"
                )
        
        return self._config
    
    def get_utils_module(self, module_name: str) -> Any:
        """
        获取工具模块
        
        参数:
            module_name (str): 模块名称
            
        返回:
            Any: 模块实例
        """
        with self._lock:
            if module_name in self._modules:
                return self._modules[module_name]
            
            module = None
            
            if module_name == "ip_scanner":
                module = self._get_ip_scanner_module()
            elif module_name == "anti_full_screen":
                module = self._get_anti_full_screen_module()
            elif module_name == "system_manager":
                module = self._get_system_manager_module()
            elif module_name == "network_manager":
                module = self._get_network_manager_module()
            elif module_name == "ui_manager":
                module = self._get_ui_manager_module()
            elif module_name == "interaction_helper":
                module = interaction_helper
            elif module_name == "thread_manager":
                module = thread_manager
            elif module_name == "error_handler":
                module = error_handler
            else:
                error_handler.handle_exception(
                    ValueError(f"Unknown module: {module_name}"),
                    "Getting utils module"
                )
            
            self._modules[module_name] = module
            return module
    
    def _get_ip_scanner_module(self) -> Any:
        """获取IP扫描模块"""
        try:
            from packages.utils.IPscanner import IPScanner
            return IPScanner()
        except ImportError:
            error_handler.handle_exception(
                ImportError("Cannot import IPScanner"),
                "Getting IP scanner module"
            )
            return None
    
    def _get_anti_full_screen_module(self) -> Any:
        """获取防全屏模块"""
        try:
            from packages.utils.fuckMythware import fuckMythware
            return fuckMythware()
        except ImportError:
            error_handler.handle_exception(
                ImportError("Cannot import fuckMythware"),
                "Getting anti full screen module"
            )
            return None
    
    def _get_system_manager_module(self) -> Any:
        """获取系统管理模块"""
        try:
            from packages.utils.SystemManager import system_manager
            return system_manager
        except ImportError:
            error_handler.handle_exception(
                ImportError("Cannot import SystemManager"),
                "Getting system manager module"
            )
            return None
    
    def _get_network_manager_module(self) -> Any:
        """获取网络管理模块"""
        try:
            from packages.utils.NetworkManager import network_manager
            return network_manager
        except ImportError:
            error_handler.handle_exception(
                ImportError("Cannot import NetworkManager"),
                "Getting network manager module"
            )
            return None
    
    def _get_ui_manager_module(self) -> Any:
        """获取UI管理模块"""
        try:
            from packages.utils.UIManager import ui_manager
            return ui_manager
        except ImportError:
            error_handler.handle_exception(
                ImportError("Cannot import UIManager"),
                "Getting UI manager module"
            )
            return None
    
    def get_version(self) -> str:
        """
        获取版本号
        
        返回:
            str: 版本号
        """
        try:
            app_state = self.get_app_state()
            return app_state.get("version", "1.0.0")
        except ImportError:
            return "1.0.0"
    
    def is_admin(self) -> bool:
        """
        检查是否具有管理员权限
        
        返回:
            bool: 是否具有管理员权限
        """
        system_manager = self.get_utils_module("system_manager")
        if system_manager:
            return system_manager.is_admin()
        return False
    
    def clear_screen(self) -> None:
        """清屏"""
        ui_manager = self.get_utils_module("ui_manager")
        if ui_manager:
            ui_manager.clear_screen()
    
    def get_user_input(self, prompt: str = "") -> str:
        """
        获取用户输入
        
        参数:
            prompt (str): 提示文本
            
        返回:
            str: 用户输入
        """
        return interaction_helper.get_user_input(prompt)
    
    def confirm(self, prompt: str = "Are you sure?", default: bool = False) -> bool:
        """
        获取用户确认
        
        参数:
            prompt (str): 提示文本
            default (bool): 默认值
            
        返回:
            bool: 用户是否确认
        """
        return interaction_helper.confirm_action(prompt, default)
    
    def show_message(self, message: str, message_type: str = "info") -> None:
        """
        显示消息
        
        参数:
            message (str): 消息内容
            message_type (str): 消息类型 (info, success, warning, error)
        """
        ui_manager = self.get_utils_module("ui_manager")
        if ui_manager:
            if message_type == "info":
                ui_manager.show_info(message)
            elif message_type == "success":
                ui_manager.show_success(message)
            elif message_type == "warning":
                ui_manager.show_warning(message)
            elif message_type == "error":
                ui_manager.show_error(message)
            else:
                ui_manager.show_info(message)
    
    def validate_ip(self, ip: str) -> bool:
        """
        验证IP地址
        
        参数:
            ip (str): IP地址
            
        返回:
            bool: 是否有效
        """
        network_manager = self.get_utils_module("network_manager")
        if network_manager:
            return network_manager.validate_ip(ip)
        return False
    
    def scan_network(self, ip_range: str = None) -> Dict[str, Any]:
        """
        扫描网络
        
        参数:
            ip_range (str): IP范围
            
        返回:
            Dict[str, Any]: 扫描结果
        """
        network_manager = self.get_utils_module("network_manager")
        if network_manager:
            return network_manager.scan_network(ip_range)
        return {"success": False, "message": "Network manager not available"}
    
    def restart_system(self) -> Dict[str, Any]:
        """
        重启系统
        
        返回:
            Dict[str, Any]: 操作结果
        """
        system_manager = self.get_utils_module("system_manager")
        if system_manager:
            return system_manager.restart_system()
        return {"success": False, "message": "System manager not available"}
    
    def shutdown_system(self) -> Dict[str, Any]:
        """
        关闭系统
        
        返回:
            Dict[str, Any]: 操作结果
        """
        system_manager = self.get_utils_module("system_manager")
        if system_manager:
            return system_manager.shutdown_system()
        return {"success": False, "message": "System manager not available"}
    
    def start_anti_full_screen(self, target_ip: str = None) -> Dict[str, Any]:
        """
        启动防全屏
        
        参数:
            target_ip (str): 目标IP
            
        返回:
            Dict[str, Any]: 操作结果
        """
        anti_full_screen = self.get_utils_module("anti_full_screen")
        if anti_full_screen:
            return thread_manager.start_thread(
                "anti_full_screen",
                lambda: self._run_anti_full_screen(anti_full_screen, target_ip)
            )
        return {"success": False, "message": "Anti full screen module not available"}
    
    def _run_anti_full_screen(self, anti_full_screen, target_ip: str = None) -> None:
        """运行防全屏"""
        try:
            anti_full_screen.start(target_ip)
        except Exception as e:
            error_handler.handle_exception(e, "Running anti full screen")
    
    def stop_anti_full_screen(self) -> Dict[str, Any]:
        """
        停止防全屏
        
        返回:
            Dict[str, Any]: 操作结果
        """
        return thread_manager.stop_thread("anti_full_screen")
    
    def is_anti_full_screen_running(self) -> bool:
        """
        检查防全屏是否正在运行
        
        返回:
            bool: 是否正在运行
        """
        return thread_manager.is_thread_running("anti_full_screen")
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        获取系统信息
        
        返回:
            Dict[str, Any]: 系统信息
        """
        system_manager = self.get_utils_module("system_manager")
        if system_manager:
            return system_manager.get_system_info()
        return {"success": False, "message": "System manager not available"}
    
    def get_network_info(self) -> Dict[str, Any]:
        """
        获取网络信息
        
        返回:
            Dict[str, Any]: 网络信息
        """
        network_manager = self.get_utils_module("network_manager")
        if network_manager:
            return network_manager.get_network_info()
        return {"success": False, "message": "Network manager not available"}
    
    def execute_command(self, command: str, shell: bool = True) -> Dict[str, Any]:
        """
        执行命令
        
        参数:
            command (str): 命令
            shell (bool): 是否使用shell
            
        返回:
            Dict[str, Any]: 执行结果
        """
        system_manager = self.get_utils_module("system_manager")
        if system_manager:
            return system_manager.execute_command(command, shell)
        return {"success": False, "message": "System manager not available"}
    
    def kill_process(self, process_name: str) -> Dict[str, Any]:
        """
        终止进程
        
        参数:
            process_name (str): 进程名称
            
        返回:
            Dict[str, Any]: 操作结果
        """
        system_manager = self.get_utils_module("system_manager")
        if system_manager:
            return system_manager.kill_process(process_name)
        return {"success": False, "message": "System manager not available"}
    
    def start_process(self, process_path: str, args: str = None) -> Dict[str, Any]:
        """
        启动进程
        
        参数:
            process_path (str): 进程路径
            args (str): 参数
            
        返回:
            Dict[str, Any]: 操作结果
        """
        system_manager = self.get_utils_module("system_manager")
        if system_manager:
            return system_manager.start_process(process_path, args)
        return {"success": False, "message": "System manager not available"}
    
    def get_time(self) -> str:
        """
        获取当前时间
        
        返回:
            str: 当前时间
        """
        try:
            from packages.utils.GetTime import get_time
            return get_time()
        except ImportError:
            error_handler.handle_exception(
                ImportError("Cannot import GetTime"),
                "Getting current time"
            )
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    def log_info(self, message: str) -> None:
        """
        记录信息日志
        
        参数:
            message (str): 日志消息
        """
        error_handler.log_info(message)
    
    def log_error(self, message: str, exception: Exception = None) -> None:
        """
        记录错误日志
        
        参数:
            message (str): 日志消息
            exception (Exception): 异常对象
        """
        error_handler.log_error(message, exception)
    
    def log_debug(self, message: str) -> None:
        """
        记录调试日志
        
        参数:
            message (str): 日志消息
        """
        error_handler.log_debug(message)
    
    def log_warning(self, message: str) -> None:
        """
        记录警告日志
        
        参数:
            message (str): 日志消息
        """
        error_handler.log_warning(message)
    
    def get_config_value(self, key: str, default_value: Any = None) -> Any:
        """
        获取配置值
        
        参数:
            key (str): 配置键
            default_value (Any): 默认值
            
        返回:
            Any: 配置值
        """
        config = self.get_config()
        return config.get(key, default_value)
    
    def set_config_value(self, key: str, value: Any) -> None:
        """
        设置配置值
        
        参数:
            key (str): 配置键
            value (Any): 配置值
        """
        config = self.get_config()
        config.set(key, value)
    
    def get_app_state_value(self, key: str, default_value: Any = None) -> Any:
        """
        获取应用状态值
        
        参数:
            key (str): 状态键
            default_value (Any): 默认值
            
        返回:
            Any: 状态值
        """
        app_state = self.get_app_state()
        return app_state.get(key, default_value)
    
    def set_app_state_value(self, key: str, value: Any) -> None:
        """
        设置应用状态值
        
        参数:
            key (str): 状态键
            value (Any): 状态值
        """
        app_state = self.get_app_state()
        app_state[key] = value
    
    def safe_execute(self, func: Callable, *args, default_value: Any = None, 
                    context: str = None, **kwargs) -> Any:
        """
        安全执行函数
        
        参数:
            func (Callable): 要执行的函数
            *args: 位置参数
            default_value (Any): 默认返回值
            context (str): 上下文描述
            **kwargs: 关键字参数
            
        返回:
            Any: 函数执行结果或默认值
        """
        return error_handler.safe_execute(
            func, *args, default_value=default_value, context=context, **kwargs
        )
    
    def handle_exception(self, exception: Exception, context: str = None) -> None:
        """
        处理异常
        
        参数:
            exception (Exception): 异常对象
            context (str): 上下文描述
        """
        error_handler.handle_exception(exception, context)
    
    def wait_for_keypress(self, message: str = "Press any key to continue...") -> None:
        """
        等待按键
        
        参数:
            message (str): 提示消息
        """
        interaction_helper.wait_for_keypress(message)
    
    def get_menu_choice(self, options: list, prompt: str = "Select an option:") -> int:
        """
        获取菜单选择
        
        参数:
            options (list): 选项列表
            prompt (str): 提示文本
            
        返回:
            int: 选择的索引
        """
        return interaction_helper.get_menu_choice(options, prompt)
    
    def navigate_menu(self, options: list, prompt: str = "Select an option:") -> int:
        """
        导航菜单
        
        参数:
            options (list): 选项列表
            prompt (str): 提示文本
            
        返回:
            int: 选择的索引
        """
        return interaction_helper.navigate_menu(options, prompt)


# 创建全局实例
utils_manager = UtilsManager()
