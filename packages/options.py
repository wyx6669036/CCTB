"""
选项处理模块
处理用户选择的各个功能选项
"""

import packages.UtilsManager as utils
import CommandUI
import ctypes
import threading
import time
from colorama import Fore, init
from packages.utils.AppState import app_state
from packages.utils.UIManager import ui_manager
from packages.utils.SystemManager import system_manager
from packages.utils.NetworkManager import network_manager
from packages.utils.Exceptions import SystemException, ValidationException
from packages.utils.ErrorHandler import error_handler
from packages.utils.ThreadManager import thread_manager
from packages.utils.InteractionHelper import interaction_helper

init(autoreset=True)


def selectOption(choice):
    """
    处理用户选择的功能选项
    
    参数:
        choice (int): 用户选择的选项编号
        
    返回:
        None
    """
    error_handler.log_info(f"Option selected: {choice}")
    
    # 使用字典映射选项到处理函数
    option_handlers = {
        0: _handle_kill_student_main,
        1: _handle_anti_full_screen,
        2: _handle_send_message
    }
    
    # 获取处理函数并执行
    handler = option_handlers.get(choice)
    if handler:
        error_handler.safe_execute(handler, context="Executing selected option")
    else:
        error_handler.handle_exception(ValueError("Invalid choice"), "Selecting option")

    interaction_helper.wait_for_keypress(f"{Fore.LIGHTYELLOW_EX}\nPress Enter to continue...{Fore.RESET}")


def _handle_kill_student_main():
    """
    处理选项0：结束studentmain.exe进程
    使用系统管理器强制结束进程
    """
    def _kill_student_main_internal():
        # 使用系统管理器结束进程
        result = system_manager.kill_process("studentmain.exe")
        
        if result.get("success", False):
            ui_manager.display_message("StudentMain.exe process has been terminated", "success")
        else:
            ui_manager.display_message(f"Failed to kill StudentMain.exe: {result.get('message', 'Unknown error')}", "error")
    
    error_handler.safe_execute(_kill_student_main_internal, context="Killing studentmain.exe process")


def _handle_anti_full_screen():
    """
    处理选项1：反全屏功能
    启动一个线程持续发送反全屏包
    """
    def _anti_full_screen_internal():
        # 警告用户此模块会消耗大量CPU和网络资源
        utils.warn("This module will consume significant CPU and network resources. Do you wish to proceed?")
        
        # 获取用户确认
        module2_choice = interaction_helper.get_user_input("[Yes/No](Default N): ")
        if module2_choice.lower() in ["yes", "y"]:
            utils.info(Fore.LIGHTYELLOW_EX + "You can Press Ctrl+C to stop this module.")
            
            # 倒计时提示
            for i in ["5", "4", "3", "2", "1"]:
                utils.info(Fore.LIGHTYELLOW_EX + f"You can Press Ctrl+C to stop this module.({i})")
                time.sleep(1)
            
            # 启动反全屏模块
            _start_anti_full_screen_thread()
        else:
            utils.info("Cancelled.")
    
    error_handler.safe_execute(_anti_full_screen_internal, context="Handling anti-full screen option")


def _start_anti_full_screen_thread():
    """
    启动反全屏功能的线程
    """
    # 检查是否已经有反全屏线程在运行
    if app_state.is_thread_running("anti_full_screen"):
        ui_manager.display_message("Anti-full screen thread is already running", "warning")
        return
    
    def _start_thread_internal():
        utils.info("Starting Thread...")
        
        # 使用线程管理器启动线程
        thread_id = thread_manager.start_thread(
            target=_module2_main,
            thread_name="anti_full_screen",
            daemon=True
        )
        
        if thread_id:
            # 更新反全屏状态
            app_state.set("anti_full_screen_active", True)
            app_state.set("anti_full_screen_running", True)
            
            ui_manager.display_message("Anti-full screen thread started", "success")
        else:
            ui_manager.display_message("Failed to start anti-full screen thread", "error")
    
    error_handler.safe_execute(_start_thread_internal, context="Starting anti-full screen thread")


def _module2_main():
    """
    反全屏模块的主函数
    持续扫描IP并发送反全屏包
    """
    # 初始化上次检查时间
    last_check_time = time.time()
    
    while app_state.get("anti_full_screen_running", False):
        try:
            # 检查是否需要发送反全屏数据包
            if _should_send_anti_full_screen_packet(last_check_time):
                _send_anti_full_screen_packet()
                last_check_time = time.time()
            
            # 短暂休眠，减少CPU占用
            time.sleep(0.1)
            
        except Exception as e:
            error_handler.handle_exception(e, "Anti-full screen main loop")
            time.sleep(1)  # 出错时等待更长时间


def _should_send_anti_full_screen_packet(last_check_time: float) -> bool:
    """
    判断是否需要发送反全屏数据包
    
    参数:
        last_check_time (float): 上次检查的时间
        
    返回:
        bool: 是否需要发送数据包
    """
    # 每隔0.5秒检查一次
    return time.time() - last_check_time >= 0.5


def _send_anti_full_screen_packet():
    """发送反全屏数据包"""
    def _send_packet_internal():
        # 检查是否有可用的目标IP
        target_ips = network_manager.get_target_ips()
        if not target_ips:
            return
            
        # 发送UDP数据包到每个目标IP
        for ip in target_ips:
            network_manager.send_udp_packet(ip, 80, "AntiFullScreen")
    
    error_handler.safe_execute(_send_packet_internal, context="Sending anti-full screen packet")


def _handle_send_message():
    """
    处理选项2：发送消息功能
    提示用户输入目标IP地址
    """
    def _send_message_internal():
        utils.info("Where would you like to send it?(eg. 192.168.153.130)")
        utils.info("If you dont input any args, it will send to all ips.")
        
        # 获取用户输入
        target_ip = interaction_helper.get_user_input("Enter target IP or press Enter for all: ")
        
        # 如果没有输入，则发送到所有IP
        if not target_ip.strip():
            target_ips = network_manager.get_target_ips()
            if not target_ips:
                ui_manager.display_message("No target IPs available", "warning")
                return
                
            utils.info(f"Sending message to all {len(target_ips)} IPs...")
            for ip in target_ips:
                network_manager.send_udp_packet(ip, 80, "Hello")
        else:
            # 验证IP地址
            if not network_manager.validate_ip(target_ip):
                ui_manager.display_message(f"Invalid IP address: {target_ip}", "error")
                return
                
            utils.info(f"Sending message to {target_ip}...")
            network_manager.send_udp_packet(target_ip, 80, "Hello")
            
        ui_manager.display_message("Message sent successfully", "success")
    
    error_handler.safe_execute(_send_message_internal, context="Handling send message option")
