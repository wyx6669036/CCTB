"""
UtilsManager
把所有（并非）功能整合为一个，使用时仅需import packages.UtilsManager as utils即可
有些功能没有整合到，要么用的不多要么懒得搞，到时候再说
格式可以参考下面添加
"""


def ip_scanner(*args, **kwargs):
    """Run the IP scanner main() and return its result (lazy import).
    Mirrors the previous 'from packages.utils.IPscanner import main as ip_scanner'.
    """
    from packages.utils.IPscanner import main as _main
    return _main(*args, **kwargs)


def anti_full_screen(target_ip, target_port=None):
    """Call the anti_full_screen implementation (lazy import)."""
    from packages.utils.fuckMythware import anti_full_screen as _af
    if target_port is None:
        return _af(target_ip)
    return _af(target_ip, target_port)


def send_teacher_message(text, target_ip, target_port=None):
    from packages.utils.fuckMythware import send_teacher_message as _stm
    if target_port is None:
        return _stm(text, target_ip)
    return _stm(text, target_ip, target_port)


def start_applicaion(path, target_ip, target_port=None):
    from packages.utils.fuckMythware import start_applicaion as _sa
    if target_port is None:
        return _sa(path, target_ip)
    return _sa(path, target_ip, target_port)

# Optionally provide direct module access helpers if other code expects attributes
def get_utils_module(name: str):
    """Return a utils submodule by name (e.g. 'IPscanner', 'fuckMythware')."""
    import importlib
    return importlib.import_module(f"packages.utils.{name}")

def AdmCheck():
    from packages.utils.AdmCheck import checkAdm as _AdmCheck
    return _AdmCheck()

def SysCheck():
    from packages.utils.SysCheck import sysCheck as _SysCheck
    return _SysCheck()

def info(message):
    from packages.utils.Log import info as _info
    return _info(message)

def warn(message):
    from packages.utils.Log import warn as _warn
    return _warn(message)

def error(message):
    from packages.utils.Log import error as _error
    return _error(message)

def Clear():
    from packages.utils.ClearScreen import clearScreen as _Clear
    return _Clear()

def selectOption(choice):
    from packages.options import selectOption as _selectOption
    return _selectOption(choice)
