"""
配置管理模块
集中管理应用程序的全局配置和状态，减少全局变量的使用
"""

import os
from typing import Dict, Any, Optional
from packages.utils.ErrorHandler import handle_exception, CCTBException


class ConfigError(CCTBException):
    """配置相关异常"""
    pass


class ConfigManager:
    """配置管理器，集中管理应用程序配置"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._config = {
                # 应用程序基本配置
                "debug": False,
                
                # 网络配置
                "target_port": 4705,
                "timeout": 5,
                
                # 系统配置
                "min_python_version": (3, 11),
                "supported_platforms": ["win32"],
                
                # 日志配置
                "log_level": "INFO",
                "log_file": None,
                
                # 其他配置
                "max_message_length": 954,
                "max_path_length": 906
            }
            self._initialized = True
    
    @handle_exception(ConfigError, default_return=None)
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            配置值
        """
        return self._config.get(key, default)
    
    @handle_exception(ConfigError, default_return=False)
    def set(self, key: str, value: Any) -> bool:
        """
        设置配置值
        
        Args:
            key: 配置键
            value: 配置值
            
        Returns:
            设置成功返回True，失败返回False
        """
        self._config[key] = value
        return True
    
    @handle_exception(ConfigError, default_return=False)
    def update(self, config_dict: Dict[str, Any]) -> bool:
        """
        批量更新配置
        
        Args:
            config_dict: 配置字典
            
        Returns:
            更新成功返回True，失败返回False
        """
        self._config.update(config_dict)
        return True
    
    @handle_exception(ConfigError, default_return=None)
    def get_all(self) -> Dict[str, Any]:
        """
        获取所有配置
        
        Returns:
            配置字典
        """
        return self._config.copy()
    
    @handle_exception(ConfigError, default_return=False)
    def load_from_file(self, file_path: str) -> bool:
        """
        从文件加载配置
        
        Args:
            file_path: 配置文件路径
            
        Returns:
            加载成功返回True，失败返回False
        """
        try:
            import json
            with open(file_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                self._config.update(config_data)
            return True
        except Exception as e:
            raise ConfigError(f"Failed to load config from {file_path}: {str(e)}")
    
    @handle_exception(ConfigError, default_return=False)
    def save_to_file(self, file_path: str) -> bool:
        """
        保存配置到文件
        
        Args:
            file_path: 配置文件路径
            
        Returns:
            保存成功返回True，失败返回False
        """
        try:
            import json
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            raise ConfigError(f"Failed to save config to {file_path}: {str(e)}")
    
    @handle_exception(ConfigError, default_return=False)
    def load_logging_config(self, config_path: str = None) -> bool:
        """
        加载日志配置
        
        Args:
            config_path: 日志配置文件路径，如果为None则使用默认路径
            
        Returns:
            加载成功返回True，失败返回False
        """
        if config_path is None:
            # 默认日志配置文件路径
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                "config",
                "logging.json"
            )
        
        try:
            import json
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    logging_config = json.load(f)
                
                # 更新日志相关配置
                log_config = {
                    "log_level": logging_config.get("log_level", "INFO"),
                    "log_file": logging_config.get("log_file"),
                    "log_format": logging_config.get("log_format", "colored"),
                    "max_file_size": logging_config.get("max_file_size", 10485760),
                    "backup_count": logging_config.get("backup_count", 5),
                    "enable_console": logging_config.get("enable_console", True),
                    "enable_file": logging_config.get("enable_file", True),
                    "console_level": logging_config.get("console_level", "INFO"),
                    "file_level": logging_config.get("file_level", "DEBUG")
                }
                
                self._config.update(log_config)
                return True
            else:
                # 如果配置文件不存在，使用默认配置
                return False
        except Exception as e:
            raise ConfigError(f"Failed to load logging config from {config_path}: {str(e)}")


# 创建全局配置管理器实例
config = ConfigManager()