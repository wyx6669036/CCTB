"""
网络操作模块
集中管理网络相关的功能，包括IP扫描和数据包发送
"""

import socket
import time
import threading
from typing import List, Tuple, Optional, Callable
from packages.utils.AppState import app_state
from packages.utils.Config import config
from packages.utils.Log import error, info, debug
from packages.utils.Exceptions import NetworkException, ValidationException
from packages.utils.ErrorHandler import error_handler


class NetworkManager:
    """
    网络管理器类
    提供网络扫描和数据包发送功能
    """
    
    @staticmethod
    def validate_ip_address(ip_address: str) -> bool:
        """
        验证IP地址格式
        
        参数:
            ip_address (str): IP地址字符串
            
        返回:
            bool: IP地址是否有效
        """
        return error_handler.safe_execute(
            NetworkManager._validate_ip_internal, ip_address,
            context="Validating IP address",
            default=False
        )
    
    @staticmethod
    def _validate_ip_internal(ip_address: str) -> bool:
        """内部IP验证实现"""
        try:
            socket.inet_aton(ip_address)
            return True
        except socket.error:
            return False
    
    @staticmethod
    def validate_port(port: int) -> bool:
        """
        验证端口号是否有效
        
        参数:
            port (int): 端口号
            
        返回:
            bool: 端口号是否有效
        """
        return 0 < port < 65536
    
    @staticmethod
    def scan_network(network_range: str = "192.168.1.1/24") -> List[Tuple[str, str]]:
        """
        扫描网络中的活跃主机
        
        参数:
            network_range (str): 网络范围，格式为"192.168.1.1/24"
            
        返回:
            List[Tuple[str, str]]: 活跃主机列表，每个元素为(IP地址, MAC地址)元组
            
        异常:
            NetworkException: 当网络扫描失败时抛出异常
        """
        return error_handler.safe_execute(
            NetworkManager._scan_network_internal, network_range,
            context="Scanning network",
            default=[]
        )
    
    @staticmethod
    def _scan_network_internal(network_range: str) -> List[Tuple[str, str]]:
        """内部网络扫描实现"""
        try:
            from packages.utils.IPscanner import main as ip_scanner
            return ip_scanner()
        except Exception as e:
            error_handler.handle_exception(e, "Network scan")
            raise NetworkException(f"Failed to scan network: {e}") from e
    
    @staticmethod
    def send_udp_packet(data: bytes, target_ip: str, target_port: int) -> None:
        """
        发送UDP数据包
        
        参数:
            data (bytes): 要发送的数据
            target_ip (str): 目标IP地址
            target_port (int): 目标端口
            
        异常:
            ValidationException: 当参数无效时抛出异常
            NetworkException: 当发送失败时抛出异常
        """
        # 验证参数
        if not NetworkManager.validate_ip_address(target_ip):
            raise ValidationException("Invalid IP address", field_name="target_ip", field_value=target_ip)
        
        if not NetworkManager.validate_port(target_port):
            raise ValidationException("Invalid port number", field_name="target_port", field_value=target_port)
        
        if not data:
            raise ValidationException("Data cannot be empty", field_name="data", field_value=data)
        
        error_handler.safe_execute(
            NetworkManager._send_udp_packet_internal, data, target_ip, target_port,
            context=f"Sending UDP packet to {target_ip}:{target_port}"
        )
    
    @staticmethod
    def _send_udp_packet_internal(data: bytes, target_ip: str, target_port: int) -> None:
        """内部UDP数据包发送实现"""
        # 创建UDP套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        try:
            # 发送数据包
            sock.sendto(data, (target_ip, target_port))
            info(f"[+] Sent to {target_ip}:{target_port}")
        except socket.error as e:
            error_handler.handle_exception(e, f"Network error sending to {target_ip}")
            raise NetworkException(f"Failed to send data to {target_ip}:{target_port}", 
                                  target_ip=target_ip, target_port=target_port) from e
        except Exception as e:
            error_handler.handle_exception(e, f"Unexpected error sending to {target_ip}")
            raise NetworkException(f"Unexpected error sending to {target_ip}:{target_port}", 
                                  target_ip=target_ip, target_port=target_port) from e
        finally:
            sock.close()


class AntiFullScreenManager:
    """
    反全屏管理器
    负责管理反全屏功能的启动和停止
    """
    
    def __init__(self):
        self.thread = None
        self.stop_event = threading.Event()
    
    def start(self, callback: Optional[Callable] = None) -> None:
        """
        启动反全屏功能
        
        参数:
            callback (Optional[Callable]): 回调函数，用于处理扫描到的IP
            
        异常:
            RuntimeError: 当反全屏功能已在运行时抛出异常
        """
        if self.is_running():
            raise RuntimeError("Anti-full-screen is already running")
        
        # 重置停止事件
        self.stop_event.clear()
        
        # 创建并启动线程
        self.thread = threading.Thread(target=self._run_loop, args=(callback,))
        self.thread.daemon = True
        self.thread.start()
        
        # 注册线程到状态管理器
        app_state.register_thread("anti_full_screen", self.thread)
        
        # 更新反全屏状态
        app_state.set("anti_full_screen_active", True)
        
        info("Anti-full-screen thread started")
    
    def stop(self) -> None:
        """
        停止反全屏功能
        
        返回:
            None
        """
        if not self.is_running():
            return
        
        # 设置停止事件
        self.stop_event.set()
        
        # 等待线程结束
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
        
        # 从状态管理器中注销线程
        app_state.unregister_thread("anti_full_screen")
        
        # 更新反全屏状态
        app_state.set("anti_full_screen_active", False)
        
        info("Anti-full-screen thread stopped")
    
    def is_running(self) -> bool:
        """
        检查反全屏功能是否正在运行
        
        返回:
            bool: 反全屏功能是否正在运行
        """
        return self.thread is not None and self.thread.is_alive()
    
    def _run_loop(self, callback: Optional[Callable] = None) -> None:
        """
        反全屏功能的主循环
        
        参数:
            callback (Optional[Callable]): 回调函数，用于处理扫描到的IP
            
        返回:
            None
        """
        try:
            while not self.stop_event.is_set():
                # 扫描网络
                ip_list = NetworkManager.scan_network()
                
                # 对每个IP发送反全屏包
                for ip_info in ip_list:
                    if self.stop_event.is_set():
                        break
                    
                    ip_address = ip_info[0]
                    try:
                        from packages.utils.fuckMythware import anti_full_screen
                        anti_full_screen(ip_address)
                        
                        # 调用回调函数
                        if callback:
                            callback(ip_address)
                    except Exception as e:
                        error_handler.handle_exception(e, f"Anti-full-screen packet to {ip_address}", level="debug")
                
                # 等待指定间隔
                self.stop_event.wait(config.anti_full_screen_interval)
        except Exception as e:
            error_handler.handle_exception(e, "Anti-full-screen loop")
        finally:
            # 确保状态被更新
            app_state.set("anti_full_screen_active", False)
            app_state.unregister_thread("anti_full_screen")


# 创建全局网络管理器实例
network_manager = NetworkManager()
anti_full_screen_manager = AntiFullScreenManager()