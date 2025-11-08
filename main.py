"""
启动cmdui的前置，可以直接启动cmdui绕过这个
主要用于获取管理员权限，创建/删除log文件
目前没办法在点击窗口右上角的X关闭时输出Exiting和bye，不过这俩玩意不重要
"""
import ctypes
import sys
import os
import threading
import CommandUI
from packages import UtilsManager as utils

def main():
    if not utils.AdmCheck():
        if utils.SysCheck()["name"] == "windows":
            # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, os.path.abspath(__file__), None, 1)
            sys.exit(0)
        else:
            utils.error("This program must be run in Windows.")
            raise RuntimeError("This program must be run in Windows.")

    os.remove("log.txt")
    with open("log.txt", "x", encoding="ANSI") as f:
        f.write("")

    utils.info("Starting...")
    utils.info("version : " + CommandUI.version)
    utils.info("runningDir : " + CommandUI.runningDir)

    Thread = threading.Thread(target=CommandUI.main())
    Thread.start()
    Thread.join()
    utils.info("Exiting...")
    utils.info("bye!")
    sys.exit(0)

DEBUG = True  # 调试模式开关，release请关闭

if __name__ == "__main__":
    main()
