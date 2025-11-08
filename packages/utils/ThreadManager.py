"""
ThreadManager
提供统一的线程管理机制，减少代码重复
"""

import threading
import time
from typing import Dict, Callable, Optional, Any
from packages.utils.AppState import app_state
from packages.utils.ErrorHandler import error_handler


class ThreadManager:
    """统一的线程管理类"""
    
    def __init__(self):
        """初始化线程管理器"""
        self._threads: Dict[str, threading.Thread] = {}
        self._stop_flags: Dict[str, threading.Event] = {}
    
    def start_thread(self, name: str, target: Callable, args: tuple = (), kwargs: dict = None, 
                    daemon: bool = True) -> bool:
        """
        启动新线程
        
        参数:
            name (str): 线程名称
            target (Callable): 线程目标函数
            args (tuple): 目标函数的位置参数
            kwargs (dict): 目标函数的关键字参数
            daemon (bool): 是否设置为守护线程
            
        返回:
            bool: 是否成功启动线程
        """
        if self.is_thread_running(name):
            error_handler.logger.warning(f"Thread {name} is already running")
            return False
            
        # 创建停止标志
        stop_flag = threading.Event()
        self._stop_flags[name] = stop_flag
        
        # 创建并启动线程
        thread = threading.Thread(
            target=self._thread_wrapper,
            args=(name, target, stop_flag, args, kwargs or {}),
            daemon=daemon
        )
        
        self._threads[name] = thread
        thread.start()
        
        # 注册到应用状态
        app_state.register_thread(name, thread)
        
        error_handler.logger.info(f"Thread {name} started")
        return True
    
    def stop_thread(self, name: str, timeout: float = 5.0) -> bool:
        """
        停止指定线程
        
        参数:
            name (str): 线程名称
            timeout (float): 等待线程结束的超时时间
            
        返回:
            bool: 是否成功停止线程
        """
        if not self.is_thread_running(name):
            return True
            
        # 设置停止标志
        if name in self._stop_flags:
            self._stop_flags[name].set()
            
        # 等待线程结束
        thread = self._threads.get(name)
        if thread and thread.is_alive():
            thread.join(timeout)
            
        # 从应用状态中注销
        app_state.unregister_thread(name)
        
        # 清理资源
        self._threads.pop(name, None)
        self._stop_flags.pop(name, None)
        
        error_handler.logger.info(f"Thread {name} stopped")
        return True
    
    def stop_all_threads(self, timeout: float = 5.0) -> None:
        """
        停止所有线程
        
        参数:
            timeout (float): 等待每个线程结束的超时时间
        """
        # 复制线程名称列表，避免在迭代过程中修改字典
        thread_names = list(self._threads.keys())
        
        for name in thread_names:
            self.stop_thread(name, timeout)
    
    def is_thread_running(self, name: str) -> bool:
        """
        检查线程是否正在运行
        
        参数:
            name (str): 线程名称
            
        返回:
            bool: 线程是否正在运行
        """
        thread = self._threads.get(name)
        return thread is not None and thread.is_alive()
    
    def get_thread_status(self, name: str) -> str:
        """
        获取线程状态
        
        参数:
            name (str): 线程名称
            
        返回:
            str: 线程状态描述
        """
        if name not in self._threads:
            return "Not created"
            
        thread = self._threads[name]
        if not thread.is_alive():
            return "Stopped"
            
        if name in self._stop_flags and self._stop_flags[name].is_set():
            return "Stopping"
            
        return "Running"
    
    def _thread_wrapper(self, name: str, target: Callable, stop_flag: threading.Event, 
                       args: tuple, kwargs: dict) -> None:
        """
        线程包装函数，处理异常和停止信号
        
        参数:
            name (str): 线程名称
            target (Callable): 目标函数
            stop_flag (threading.Event): 停止标志
            args (tuple): 目标函数的位置参数
            kwargs (dict): 目标函数的关键字参数
        """
        try:
            # 检查目标函数是否接受stop_flag参数
            import inspect
            sig = inspect.signature(target)
            if 'stop_flag' in sig.parameters:
                kwargs['stop_flag'] = stop_flag
                
            # 执行目标函数
            target(*args, **kwargs)
            
        except Exception as e:
            error_handler.handle_exception(e, f"Thread {name} execution")
        finally:
            # 线程结束时清理资源
            app_state.unregister_thread(name)
            self._threads.pop(name, None)
            self._stop_flags.pop(name, None)
            error_handler.logger.info(f"Thread {name} ended")


# 创建全局线程管理器实例
thread_manager = ThreadManager()