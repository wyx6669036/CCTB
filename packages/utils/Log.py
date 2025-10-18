from colorama import Fore, Style, Back
from packages.utils.GetTime import gettime

def info(text):
    print(Fore.LIGHTBLACK_EX + "[" + Fore.WHITE + gettime() + Style.BRIGHT + Fore.LIGHTWHITE_EX + " INF" + Fore.RESET + Fore.LIGHTBLACK_EX + "] " + Fore.LIGHTWHITE_EX + text)

def warn(text):
    print(Fore.LIGHTBLACK_EX + "[" + Fore.WHITE + gettime() + Style.BRIGHT + Fore.LIGHTYELLOW_EX + " WRN" + Fore.RESET + Fore.LIGHTBLACK_EX + "] " + Fore.LIGHTWHITE_EX + "* " + text)

def error(text):
    print(Fore.LIGHTBLACK_EX + "[" + Fore.WHITE + gettime() + " " + Back.RED + Style.BRIGHT + Fore.LIGHTWHITE_EX + "ERR" + Back.RESET + Fore.RESET + Fore.LIGHTBLACK_EX + "] " + Fore.LIGHTWHITE_EX + "* " + text)
