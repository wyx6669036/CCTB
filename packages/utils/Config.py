"""
应用配置管理模块
集中管理应用程序的所有配置项
"""

import os
from typing import Dict, Any


class Config:
    """
    配置管理类
    使用单例模式确保全局只有一个配置实例
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # 应用程序基本配置
        self.app_name = "CCTB"
        self.version = "beta 0.1.1"
        self.author = "wyx6669036"
        
        # 网络配置
        self.default_target_port = 4705
        self.anti_full_screen_interval = 0.3  # 反全屏发送间隔(秒)
        
        # UI配置
        self.ui_colors = {
            "title": "LIGHTBLUE_EX",
            "author": "RED",
            "selected": "LIGHTBLUE_EX",
            "warning": "LIGHTYELLOW_EX"
        }
        
        # 菜单选项配置
        self.menu_options = [
            {
                "text": "1.Kill Mythware Classroom Management",
                "name": "kill_mythware",
                "action": None  # Will be set later when implementing the actual functionality
            },
            {
                "text": "2.Enable \"Anti Full Screen Broadcast\" Thread",
                "name": "anti_full_screen",
                "action": None  # Will be set later when implementing the actual functionality
            },
            {
                "text": "3.Send teacher message",
                "name": "send_message",
                "action": None  # Will be set later when implementing the actual functionality
            }
        ]
        
        # 资源文件配置
        self.resource_files = {
            "psexec": "psexec.exe",
            "taskkill": "CCTB.Taskkill.exe",
            "command": "CCTB.Command.exe",
            "regedit": "CCTB.Regedit.exe",
            "taskmgr": "CCTB.Taskmgr.exe"
        }
        
        # 日志配置
        self.log_file = "log.txt"
        self.log_levels = {
            "debug": 0,
            "info": 1,
            "warn": 2,
            "error": 3
        }
        
        # 系统要求配置
        self.required_system = "windows"
        
        self._initialized = True
    
    def get_resource_path(self, resource_name: str, running_dir: str) -> str:
        """
        获取资源文件的完整路径
        
        参数:
            resource_name (str): 资源文件名称
            running_dir (str): 应用程序运行目录
            
        返回:
            str: 资源文件的完整路径
        """
        if resource_name in self.resource_files:
            return os.path.join(running_dir, "resource", self.resource_files[resource_name])
        return os.path.join(running_dir, "resource", resource_name)
    
    def get_menu_options(self) -> list:
        """
        获取菜单选项列表
        
        返回:
            list: 菜单选项列表
        """
        return self.menu_options.copy()
    
    def get_ui_color(self, color_name: str) -> str:
        """
        获取UI颜色配置
        
        参数:
            color_name (str): 颜色名称
            
        返回:
            str: 颜色值
        """
        return self.ui_colors.get(color_name, "RESET")
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        """
        更新配置
        
        参数:
            updates (Dict[str, Any]): 要更新的配置项
            
        返回:
            None
        """
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)


# 创建全局配置实例
config = Config()