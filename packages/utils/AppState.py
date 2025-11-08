"""
应用状态管理模块
提供集中式的状态管理，避免全局变量的使用
"""

import threading
from typing import Dict, Any, Optional


class AppState:
    """
    应用状态管理类
    使用单例模式确保全局只有一个状态实例
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AppState, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # 初始化状态数据
        self._state = {
            # 应用基本信息
            "version": "beta 0.1.1",
            "running_dir": None,
            "tools_dir": None,
            
            # UI状态
            "selected_menu_index": 0,
            "menu_options": [
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
            ],
            
            # 线程状态
            "active_threads": {},
            
            # 功能模块状态
            "anti_full_screen_active": False,
            
            # 系统状态
            "admin_privileges": False,
            "system_info": None,
            
            # 日志状态
            "log_file_path": "log.txt",
            "log_initialized": False,
        }
        
        self._initialized = True
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取状态值
        
        参数:
            key (str): 状态键
            default (Any): 默认值，当键不存在时返回
            
        返回:
            Any: 状态值
        """
        return self._state.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        设置状态值
        
        参数:
            key (str): 状态键
            value (Any): 状态值
            
        返回:
            None
        """
        self._state[key] = value
    
    def update(self, updates: Dict[str, Any]) -> None:
        """
        批量更新状态
        
        参数:
            updates (Dict[str, Any]): 要更新的键值对
            
        返回:
            None
        """
        self._state.update(updates)
    
    def register_thread(self, name: str, thread: threading.Thread) -> None:
        """
        注册活动线程
        
        参数:
            name (str): 线程名称
            thread (threading.Thread): 线程对象
            
        返回:
            None
        """
        self._state["active_threads"][name] = thread
    
    def unregister_thread(self, name: str) -> None:
        """
        注销活动线程
        
        参数:
            name (str): 线程名称
            
        返回:
            None
        """
        if name in self._state["active_threads"]:
            del self._state["active_threads"][name]
    
    def is_thread_active(self, name: str) -> bool:
        """
        检查线程是否活动
        
        参数:
            name (str): 线程名称
            
        返回:
            bool: 线程是否活动
        """
        thread = self._state["active_threads"].get(name)
        if thread is None:
            return False
        return thread.is_alive()
    
    def stop_thread(self, name: str) -> bool:
        """
        停止指定线程
        
        参数:
            name (str): 线程名称
            
        返回:
            bool: 是否成功停止线程
        """
        thread = self._state["active_threads"].get(name)
        if thread is None or not thread.is_alive():
            return False
        
        # 注意：Python中没有直接安全停止线程的方法
        # 这里只是示例，实际实现可能需要使用事件标志或其他机制
        return False
    
    def get_all_state(self) -> Dict[str, Any]:
        """
        获取所有状态的副本
        
        返回:
            Dict[str, Any]: 状态字典的副本
        """
        return self._state.copy()


# 创建全局状态实例
app_state = AppState()