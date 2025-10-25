import packages.UtilsManager as utils
import CommandUI
import ctypes
from colorama import Fore, init

init(autoreset=True)

def selectOption(choice):
    utils.debug("Option selected: " + str(choice), "info")
    if choice == 0:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", CommandUI.toolsDir["psexec"] + "psexec.exe", " -s -accepteula " + CommandUI.toolsDir["taskkill"] + "CCTB.Taskkill.Win7.exe /F /IM studentmain.exe", None, 0)
        utils.debug("Killed!", "info")
    elif choice == 1:
        utils.ip_scanner()
        utils.debug("Finished!", "info")
    else:
        utils.debug("Invalid choice.", "error")

    input(Fore.LIGHTYELLOW_EX + "\nPress Enter to continue..." + Fore.RESET)