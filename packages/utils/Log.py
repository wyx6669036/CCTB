"""
日志输出模块
提供彩色控制台输出和文件日志记录功能
支持不同级别的日志输出和异常记录
"""

from colorama import Fore, Style, Back, init
from packages.utils.GetTime import gettime
from packages.utils.Exceptions import CCTBException
import traceback
import os

init(autoreset=True)


def info(text):
    """
    输出信息级别日志
    
    参数:
        text (str): 要输出的日志信息
    """
    try:
        # 控制台输出
        print(Fore.LIGHTBLACK_EX + "[" + Fore.WHITE + gettime() + Style.BRIGHT + Fore.LIGHTWHITE_EX + " INF" + Fore.RESET + Fore.LIGHTBLACK_EX + "] " + Fore.LIGHTWHITE_EX + text)
        
        # 文件输出
        _write_to_file("[" + gettime() + " INF] " + text + "\n")
    except Exception as e:
        print(f"Error writing info log: {e}")


def warn(text):
    """
    输出警告级别日志
    
    参数:
        text (str): 要输出的警告信息
    """
    try:
        # 控制台输出
        print(Fore.LIGHTBLACK_EX + "[" + Fore.WHITE + gettime() + Style.BRIGHT + Fore.LIGHTYELLOW_EX + " WRN" + Fore.RESET + Fore.LIGHTBLACK_EX + "] " + Fore.LIGHTWHITE_EX + "* " + text)
        
        # 文件输出
        _write_to_file("[" + gettime() + " WRN] * " + text + "\n")
    except Exception as e:
        print(f"Error writing warn log: {e}")


def error(text, exception=None):
    """
    输出错误级别日志
    
    参数:
        text (str): 要输出的错误信息
        exception (Exception, optional): 关联的异常对象
    """
    try:
        # 控制台输出
        print(Fore.LIGHTBLACK_EX + "[" + Fore.WHITE + gettime() + " " + Back.RED + Style.BRIGHT + Fore.LIGHTWHITE_EX + "ERR" + Back.RESET + Fore.RESET + Fore.LIGHTBLACK_EX + "] " + Fore.LIGHTWHITE_EX + "* " + text)
        
        # 文件输出
        log_entry = "[" + gettime() + " ERR] * " + text + "\n"
        
        # 如果有异常对象，添加异常信息
        if exception:
            log_entry += f"Exception Type: {type(exception).__name__}\n"
            log_entry += f"Exception Message: {str(exception)}\n"
            log_entry += f"Traceback: {traceback.format_exc()}\n"
            
            # 如果是自定义异常，添加额外信息
            if isinstance(exception, CCTBException):
                if hasattr(exception, 'error_code') and exception.error_code:
                    log_entry += f"Error Code: {exception.error_code}\n"
                if hasattr(exception, 'target_ip') and exception.target_ip:
                    log_entry += f"Target IP: {exception.target_ip}\n"
                if hasattr(exception, 'target_port') and exception.target_port:
                    log_entry += f"Target Port: {exception.target_port}\n"
        
        _write_to_file(log_entry)
    except Exception as e:
        print(f"Error writing error log: {e}")


def debug(text):
    """
    输出调试级别日志
    
    参数:
        text (str): 要输出的调试信息
    """
    try:
        # 控制台输出
        print(Fore.LIGHTBLACK_EX + "[" + Fore.WHITE + gettime() + Style.BRIGHT + Fore.LIGHTCYAN_EX + " DBG" + Fore.RESET + Fore.LIGHTBLACK_EX + "] " + Fore.LIGHTWHITE_EX + text)
        
        # 文件输出
        _write_to_file("[" + gettime() + " DBG] " + text + "\n")
    except Exception as e:
        print(f"Error writing debug log: {e}")


def _write_to_file(content):
    """
    写入日志到文件的内部函数
    
    参数:
        content (str): 要写入的内容
    """
    try:
        # 确保日志目录存在
        log_dir = os.path.dirname("log.txt")
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # 写入文件
        with open("log.txt", "a", encoding="ANSI") as f:
            f.write(content)
    except IOError as e:
        print(f"IO Error writing to log file: {e}")
    except Exception as e:
        print(f"Unexpected error writing to log file: {e}")