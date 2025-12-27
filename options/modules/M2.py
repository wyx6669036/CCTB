import threading
import time
from utils import UtilsManager as utils
from utils.impl.ErrorHandler import handle_exception, ValidationError


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
