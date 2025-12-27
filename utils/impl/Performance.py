"""
性能优化模块
提供系统性能监控和优化功能
"""

from __future__ import annotations
import gc
import os
import psutil
import threading
import time
from typing import Dict, List, Callable, Any
from collections import deque
from utils import UtilsManager as utils
from utils.impl.ErrorHandler import handle_exception, SystemError


class PerformanceMonitor:
    """性能监控器，用于跟踪系统资源使用情况"""
    
    def __init__(self, max_history: int = 100):
        """
        初始化性能监控器
        
        Args:
            max_history: 最大历史记录数量
        """
        self.max_history = max_history
        self.cpu_history = deque(maxlen=max_history)
        self.memory_history = deque(maxlen=max_history)
        self.thread_count_history = deque(maxlen=max_history)
        self.monitoring = False
        self.monitor_thread = None
        self.monitor_interval = 1.0  # 默认1秒采样间隔
        self.callbacks: List[Callable[[Dict[str, Any]], None]] = []
        
    def start_monitoring(self, interval: float = 1.0):
        """
        开始性能监控
        
        Args:
            interval: 监控间隔（秒）
        """
        if self.monitoring:
            return
            
        self.monitor_interval = interval
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        utils.info(f"Performance monitoring started with {interval}s interval")
        
    def stop_monitoring(self):
        """停止性能监控"""
        if not self.monitoring:
            return
            
        self.monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2.0)
        utils.info("Performance monitoring stopped")
        
    def _monitor_loop(self):
        """监控循环"""
        process = psutil.Process(os.getpid())
        
        while self.monitoring:
            try:
                # 收集性能数据
                cpu_percent = process.cpu_percent()
                memory_info = process.memory_info()
                memory_mb = memory_info.rss / (1024 * 1024)  # 转换为MB
                thread_count = process.num_threads()
                
                # 存储历史数据
                self.cpu_history.append(cpu_percent)
                self.memory_history.append(memory_mb)
                self.thread_count_history.append(thread_count)
                
                # 调用回调函数
                perf_data = {
                    "cpu": cpu_percent,
                    "memory_mb": memory_mb,
                    "threads": thread_count,
                    "timestamp": time.time()
                }
                
                for callback in self.callbacks:
                    try:
                        callback(perf_data)
                    except Exception as e:
                        utils.error(f"Performance callback error: {e}")
                        
                time.sleep(self.monitor_interval)
            except Exception as e:
                utils.error(f"Performance monitoring error: {e}")
                time.sleep(self.monitor_interval)
                
    def add_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """
        添加性能数据回调函数
        
        Args:
            callback: 回调函数，接收性能数据字典
        """
        self.callbacks.append(callback)
        
    def get_current_stats(self) -> Dict[str, Any]:
        """
        获取当前性能统计
        
        Returns:
            包含当前性能统计的字典
        """
        try:
            process = psutil.Process(os.getpid())
            cpu_percent = process.cpu_percent()
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / (1024 * 1024)
            thread_count = process.num_threads()
            
            return {
                "cpu": cpu_percent,
                "memory_mb": memory_mb,
                "threads": thread_count,
                "timestamp": time.time()
            }
        except Exception as e:
            utils.error(f"Failed to get performance stats: {e}")
            return {
                "cpu": 0,
                "memory_mb": 0,
                "threads": 0,
                "timestamp": time.time()
            }
            
    def get_average_stats(self) -> Dict[str, float]:
        """
        获取平均性能统计
        
        Returns:
            包含平均性能统计的字典
        """
        if not self.cpu_history:
            return {"cpu": 0, "memory_mb": 0, "threads": 0}
            
        return {
            "cpu": sum(self.cpu_history) / len(self.cpu_history),
            "memory_mb": sum(self.memory_history) / len(self.memory_history),
            "threads": sum(self.thread_count_history) / len(self.thread_count_history)
        }


class ResourceOptimizer:
    """资源优化器，用于管理系统资源"""
    
    def __init__(self, monitor: PerformanceMonitor):
        """
        初始化资源优化器
        
        Args:
            monitor: 性能监控器实例
        """
        self.monitor = monitor
        self.optimization_rules = []
        self.auto_optimize = False
        self.optimization_interval = 30.0  # 默认30秒检查一次
        self.optimize_thread = None
        self.optimizing = False
        
        # 默认优化规则
        self._setup_default_rules()
        
    def _setup_default_rules(self):
        """设置默认优化规则"""
        # 内存使用过高时触发垃圾回收
        self.add_rule(
            condition=lambda stats: stats.get("memory_mb", 0) > 200,  # 超过200MB
            action=lambda stats: self._optimize_memory(),
            description="High memory usage - trigger garbage collection"
        )
        
        # CPU使用过高时记录警告
        self.add_rule(
            condition=lambda stats: stats.get("cpu", 0) > 80,  # 超过80%
            action=lambda stats: utils.warn(f"High CPU usage: {stats.get('cpu', 0):.1f}%"),
            description="High CPU usage - log warning"
        )
        
    def add_rule(self, condition: Callable[[Dict[str, Any]], bool], 
                 action: Callable[[Dict[str, Any]], None], 
                 description: str = ""):
        """
        添加优化规则
        
        Args:
            condition: 条件函数，接收性能统计，返回布尔值
            action: 动作函数，接收性能统计
            description: 规则描述
        """
        rule = {
            "condition": condition,
            "action": action,
            "description": description,
            "enabled": True,
            "trigger_count": 0,
            "last_triggered": 0
        }
        self.optimization_rules.append(rule)
        
    def start_auto_optimization(self, interval: float = 30.0):
        """
        开始自动优化
        
        Args:
            interval: 检查间隔（秒）
        """
        if self.optimizing:
            return
            
        self.optimization_interval = interval
        self.auto_optimize = True
        self.optimizing = True
        self.optimize_thread = threading.Thread(target=self._optimize_loop, daemon=True)
        self.optimize_thread.start()
        utils.info(f"Auto optimization started with {interval}s interval")
        
    def stop_auto_optimization(self):
        """停止自动优化"""
        if not self.optimizing:
            return
            
        self.optimizing = False
        self.auto_optimize = False
        if self.optimize_thread and self.optimize_thread.is_alive():
            self.optimize_thread.join(timeout=2.0)
        utils.info("Auto optimization stopped")
        
    def _optimize_loop(self):
        """优化循环"""
        while self.optimizing:
            try:
                stats = self.monitor.get_current_stats()
                self._check_rules(stats)
                time.sleep(self.optimization_interval)
            except Exception as e:
                utils.error(f"Auto optimization error: {e}")
                time.sleep(self.optimization_interval)
                
    def _check_rules(self, stats: Dict[str, Any]):
        """检查并执行优化规则"""
        current_time = time.time()
        
        for rule in self.optimization_rules:
            if not rule["enabled"]:
                continue
                
            try:
                if rule["condition"](stats):
                    rule["action"](stats)
                    rule["trigger_count"] += 1
                    rule["last_triggered"] = current_time
                    
                    if rule["description"]:
                        utils.debug(f"Optimization rule triggered: {rule['description']}")
            except Exception as e:
                utils.error(f"Error executing optimization rule: {e}")
                
    def _optimize_memory(self):
        """执行内存优化"""
        try:
            # 获取优化前的内存使用
            before_mb = self.monitor.get_current_stats().get("memory_mb", 0)
            
            # 强制垃圾回收
            collected = gc.collect()
            
            # 获取优化后的内存使用
            after_mb = self.monitor.get_current_stats().get("memory_mb", 0)
            saved_mb = before_mb - after_mb
            
            utils.info(f"Memory optimization: collected {collected} objects, freed {saved_mb:.2f} MB")
        except Exception as e:
            utils.error(f"Memory optimization failed: {e}")
            
    def optimize_now(self):
        """立即执行一次优化"""
        stats = self.monitor.get_current_stats()
        self._check_rules(stats)
        
    def get_rules_status(self) -> List[Dict[str, Any]]:
        """
        获取优化规则状态
        
        Returns:
            规则状态列表
        """
        return [
            {
                "description": rule["description"],
                "enabled": rule["enabled"],
                "trigger_count": rule["trigger_count"],
                "last_triggered": rule["last_triggered"]
            }
            for rule in self.optimization_rules
        ]


# 全局性能监控器和优化器实例
_monitor = None
_optimizer = None


@handle_exception(SystemError, default_return=None, error_message="Failed to initialize performance manager")
def initialize_performance_manager():
    """初始化性能管理器"""
    global _monitor, _optimizer
    
    if _monitor is None:
        _monitor = PerformanceMonitor()
        _optimizer = ResourceOptimizer(_monitor)
        
        # 添加性能监控回调，记录到日志
        def log_performance(stats):
            if stats.get("cpu", 0) > 70 or stats.get("memory_mb", 0) > 150:
                utils.warn(f"High resource usage: CPU {stats.get('cpu', 0):.1f}%, Memory {stats.get('memory_mb', 0):.1f}MB")
                
        _monitor.add_callback(log_performance)
        
        utils.info("Performance manager initialized")


@handle_exception(SystemError, default_return=None, error_message="Failed to start performance monitoring")
def start_performance_monitoring(interval: float = 5.0, auto_optimize: bool = True, 
                                optimize_interval: float = 30.0):
    """
    启动性能监控
    
    Args:
        interval: 监控间隔（秒）
        auto_optimize: 是否启用自动优化
        optimize_interval: 优化检查间隔（秒）
    """
    if _monitor is None:
        initialize_performance_manager()
        
    _monitor.start_monitoring(interval)
    
    if auto_optimize:
        _optimizer.start_auto_optimization(optimize_interval)


@handle_exception(SystemError, default_return=None, error_message="Failed to stop performance monitoring")
def stop_performance_monitoring():
    """停止性能监控"""
    if _monitor:
        _monitor.stop_monitoring()
    if _optimizer:
        _optimizer.stop_auto_optimization()


def get_performance_stats() -> Dict[str, Any]:
    """
    获取当前性能统计
    
    Returns:
        性能统计字典
    """
    if _monitor is None:
        return {}
        
    current = _monitor.get_current_stats()
    average = _monitor.get_average_stats()
    
    return {
        "current": current,
        "average": average,
        "rules": _optimizer.get_rules_status() if _optimizer else []
    }


def optimize_now():
    """立即执行一次优化"""
    if _optimizer:
        _optimizer.optimize_now()