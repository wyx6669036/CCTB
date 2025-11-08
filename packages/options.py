"""
选项处理模块
负责处理用户选择的操作选项并执行相应功能
"""

import packages.UtilsManager as utils
import CommandUI
import ctypes
import threading
import time
from colorama import Fore, init
from packages.utils.ErrorHandler import handle_exception, SystemError, ValidationError

# 初始化colorama，确保颜色重置
init(autoreset=True)


@handle_exception(ValidationError, default_return=None, error_message="Invalid option selected")
def selectOption(choice):
    """
    处理用户选择的操作选项
    
    Args:
        choice (int): 用户选择的选项编号
        
    Options:
        0: 强制结束studentmain.exe进程
        1: 启动反全屏模块
        2: 发送教师消息
    """
    # 验证输入
    if not isinstance(choice, int) or choice < 0 or choice > 2:
        raise ValidationError(f"Invalid choice: {choice}. Must be 0, 1, or 2.")
    
    utils.info("Option selected: " + str(choice))
    
    try:
        if choice == 0:
            _handle_kill_process()
        elif choice == 1:
            _handle_anti_full_screen()
        elif choice == 2:
            _handle_send_teacher_message()
    except KeyboardInterrupt:
        # 捕获并处理KeyboardInterrupt，直接返回到主菜单
        utils.info("\nOperation cancelled by user.")
        # 不重新抛出异常，让程序返回主菜单
    
    input(Fore.LIGHTYELLOW_EX + "\nPress Enter to continue..." + Fore.RESET)

@handle_exception(SystemError, default_return=None, error_message="Failed to kill process")
def _handle_kill_process():
    """
    处理强制结束studentmain.exe进程的选项
    使用PsExec以系统权限运行taskkill命令强制结束进程
    """
    # 调用psexec运行taskkill结束studentmain.exe，没有技术含量，所有系统组件用的win7的，都是从legacy拿的，反正win10+都兼容，legacy0.4写系统区分的时候给我写死了
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", 
            CommandUI.runningDir + "\\resource\\psexec.exe", 
            " -s -accepteula " + CommandUI.runningDir + "\\resource\\CCTB.Taskkill.exe /F /IM studentmain.exe", 
            None, 0
        )
        utils.info("Killed!")
    except Exception as e:
        utils.error(f"Failed to kill process: {e}")
        raise SystemError(f"Failed to kill process: {e}")

@handle_exception(SystemError, default_return=None, error_message="Failed to start anti full screen module")
def _handle_anti_full_screen():
    """
    处理反全屏模块的选项
    启动一个线程持续发送反全屏数据包
    """
    # 就是说呢，用的Coco抓包抓出来的神秘反全屏，写壳子写出了史山
    # 本来是想要新建一个窗口放后台持续发包，但是写了几天写炸了干脆放前台了，后面换gui了再尝试写
    utils.warn("This module will consume significant CPU and network resources. Do you wish to proceed?")
    
    # 神秘确认
    module2_choice = input("[Yes/No](Default N): ")
    if module2_choice.lower() == "yes" or module2_choice == "y":
        utils.info(Fore.LIGHTYELLOW_EX + "You can Press Ctrl+C to stop this module.")
        for i in ["5","4","3","2","1"]:
            utils.info(Fore.LIGHTYELLOW_EX + f"You can Press Ctrl+C to stop this module.({i})")
            time.sleep(1)
        module2_choice = True
    else:
        module2_choice = False

    if module2_choice:
        try:
            utils.info("Starting Thread...")
            # 确保之前的线程已停止
            stop_module2()
            time.sleep(0.5)  # 等待线程停止
            
            # 使用全局变量存储线程引用以便管理
            global _anti_fullscreen_thread
            _anti_fullscreen_thread = threading.Thread(target=module2_main, daemon=True)
            _anti_fullscreen_thread.start()
            utils.info("Started!")
            
            # 等待用户中断
            try:
                while _anti_fullscreen_thread.is_alive():
                    time.sleep(0.1)  # 减少睡眠时间以便更快响应Ctrl+C
            except KeyboardInterrupt:
                utils.info("\nStopping module...")
                stop_module2()
                _anti_fullscreen_thread.join(timeout=2)  # 等待线程结束，最多2秒
                if _anti_fullscreen_thread.is_alive():
                    utils.warn("Module did not stop gracefully")
                else:
                    utils.info("Module stopped!")
                # 不重新抛出KeyboardInterrupt，让用户返回主菜单
        except KeyboardInterrupt:
            # 捕获KeyboardInterrupt，确保能退出到主菜单
            utils.info("\nOperation cancelled by user.")
        except Exception as e:
            utils.error(f"Failed to start anti full screen module: {e}")
            raise SystemError(f"Failed to start anti full screen module: {e}")
    else:
        utils.info("Cancelled.")

@handle_exception(SystemError, default_return=None, error_message="Failed to send teacher message")
def _handle_send_teacher_message():
    """
    处理发送教师消息的选项
    收集目标IP和消息内容，然后启动线程发送消息
    """
    import signal
    
    # 依旧是Coco写的神秘代码，效果是学生端看到老师发来的消息
    utils.info("Where would you like to send it?(eg. 192.168.153.130)")
    utils.info("If you dont input any args, it will send to all ips.")
    module3_choice = input("[IP](Default All): ")
    module3_text = input("[Text]: ")
    
    # 验证输入
    if not module3_text:
        utils.error("Message text cannot be empty")
        raise ValidationError("Message text cannot be empty")
    
    # 如果用户输入为空，默认设置为 "all"
    if not module3_choice.strip():
        module3_choice = "all"
    
    # 设置信号处理器以确保Ctrl+C能被正确捕获
    def signal_handler(signum, frame):
        raise KeyboardInterrupt()
    
    original_handler = signal.signal(signal.SIGINT, signal_handler)
    
    try:
        Thread = threading.Thread(target=module3_main, args=(module3_choice, module3_text), daemon=True)
        Thread.start()
        
        # 等待用户中断或线程结束
        try:
            while Thread.is_alive():
                time.sleep(0.1)  # 减少睡眠时间以便更快响应Ctrl+C
        except KeyboardInterrupt:
            utils.info("\nStopping message sending...")
            # module3_main 会自动处理 KeyboardInterrupt
            Thread.join(timeout=2)  # 等待线程结束，最多2秒
            if Thread.is_alive():
                utils.warn("Message sending did not stop gracefully")
            else:
                utils.info("Message sending stopped!")
            # 不重新抛出KeyboardInterrupt，让用户返回主菜单
    except KeyboardInterrupt:
        # 捕获KeyboardInterrupt，确保能退出到主菜单
        utils.info("\nOperation cancelled by user.")
    except Exception as e:
        utils.error(f"Failed to start message sending thread: {e}")
        raise SystemError(f"Failed to start message sending thread: {e}")
    finally:
        # 恢复原始信号处理器
        signal.signal(signal.SIGINT, original_handler)

# 全局变量，用于控制module2_main线程的运行状态
_module2_running = True
_anti_fullscreen_thread = None

def stop_module2():
    """停止module2_main线程"""
    global _module2_running, _anti_fullscreen_thread
    _module2_running = False
    
    # 如果线程存在，等待它结束
    if _anti_fullscreen_thread and _anti_fullscreen_thread.is_alive():
        _anti_fullscreen_thread.join(timeout=1)  # 等待最多1秒

def module2_main(status=True):
    """
    反全屏模块的主函数
    
    Args:
        status (bool): 控制循环是否继续
    """
    global _module2_running
    _module2_running = status
    
    while _module2_running:
        try:
            ip_list = utils.ip_scanner()
            if ip_list and len(ip_list) > 0:  # 确保列表不为空且有效
                for i in ip_list:
                    # 检查是否应该继续运行
                    if not _module2_running:
                        break
                    # 确保IP地址格式正确
                    if i and len(i) >= 1 and i[0]:
                        utils.anti_full_screen(i[0])
                    else:
                        utils.warn(f"Invalid IP format: {i}")
            else:
                utils.warn("No active hosts found. Retrying in 0.3 seconds...")
            time.sleep(0.3)
        except KeyboardInterrupt:
            # 捕获Ctrl+C信号，退出循环
            utils.info("Module interrupted by user.")
            break
        except Exception as e:
            utils.error(f"Error in module2_main: {e}")
            time.sleep(1)  # 发生错误时等待更长时间再重试

def module3_main(choice, text):
    """
    发送教师消息模块的主函数
    
    Args:
        choice (str): 目标IP地址，空字符串或"all"表示发送给所有IP
        text (str): 要发送的消息内容
    """
    try:
        # 处理用户输入的"all"或空字符串，都表示发送给所有IP
        if choice == "" or choice.lower() == "all":
            ip_list = utils.ip_scanner()
            if ip_list and len(ip_list) > 0:  # 确保列表不为空且有效
                for i in ip_list:
                    # 检查是否应该继续运行
                    # 确保IP地址格式正确
                    if i and len(i) >= 1 and i[0]:
                        ips = i[0]
                        # 验证IP地址格式
                        if _is_valid_ip(ips):
                            utils.info(f"Sending message:[{text}]...")
                            utils.send_teacher_message(text, ips)
                        else:
                            utils.warn(f"Invalid IP address format: {ips}")
                    else:
                        utils.warn(f"Invalid IP format: {i}")
                utils.info("Finished.")
            else:
                utils.warn("No active hosts found. Message not sent.")
        else:
            ips = choice
            # 验证IP地址格式
            if _is_valid_ip(ips):
                utils.info(f"Sending message:[{text}]...")
                utils.send_teacher_message(text, ips)
            else:
                utils.error(f"Invalid IP address format: {ips}")
                raise ValidationError(f"Invalid IP address format: {ips}")
    except KeyboardInterrupt:
        utils.info("Message sending interrupted by user.")
    except ValidationError:
        # 重新抛出ValidationError，让上层处理
        raise
    except Exception as e:
        utils.error(f"Error in module3_main: {e}")
        import traceback
        traceback.print_exc()


def _is_valid_ip(ip):
    """
    验证IP地址格式是否正确
    
    Args:
        ip (str): 要验证的IP地址
        
    Returns:
        bool: IP地址格式正确返回True，否则返回False
    """
    try:
        import socket
        import re
        
        # 确保IP地址不是空字符串
        if not ip or not ip.strip():
            return False
            
        # 使用正则表达式验证IPv4格式
        ip_pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
        match = re.match(ip_pattern, ip.strip())
        if not match:
            return False
            
        # 检查每个部分是否在0-255范围内
        for part in match.groups():
            num = int(part)
            if num < 0 or num > 255:
                return False
                
        # 使用socket.inet_aton进行最终验证
        socket.inet_aton(ip.strip())
        return True
    except socket.error:
        return False
    except ValueError:
        return False
    except Exception:
        return False