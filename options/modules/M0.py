import ctypes
import CommandUI
from utils import UtilsManager as utils
from utils.impl.ErrorHandler import handle_exception


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