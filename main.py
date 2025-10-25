import ctypes
import sys
import os
import CommandUI
from packages import UtilsManager as utils

def main():
    if not utils.AdmCheck.checkAdm():
        if utils.SysCheck.sysCheck()["name"] == "windows":
            # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, os.path.abspath(__file__), None, 1)
            sys.exit(0)
        else:
            utils.Log.error("This program must be run in Windows.")
            raise RuntimeError("This program must be run in Windows.")

    os.remove("log.txt")
    with open("log.txt", "x", encoding="ANSI") as f:
        f.write("")

    utils.Log.info("Starting...")
    utils.Log.info("version : " + CommandUI.version)
    utils.Log.info("runningDir : " + CommandUI.runningDir)
    utils.Log.info("toolsDir : " + str(CommandUI.toolsDir))

    CommandUI.main()

DEBUG = True  # 调试模式开关，release请关闭

if __name__ == "__main__":
    main()
