from colorama import Fore, Style, Back, init
from packages.utils.GetTime import gettime

init(autoreset=True)

def info(text):
    print(Fore.LIGHTBLACK_EX + "[" + Fore.WHITE + gettime() + Style.BRIGHT + Fore.LIGHTWHITE_EX + " INF" + Fore.RESET + Fore.LIGHTBLACK_EX + "] " + Fore.LIGHTWHITE_EX + text)
    with open("log.txt", "a", encoding="ANSI") as f:
        f.write("[" + gettime() + " INF] " + text + "\n")

def warn(text):
    print(Fore.LIGHTBLACK_EX + "[" + Fore.WHITE + gettime() + Style.BRIGHT + Fore.LIGHTYELLOW_EX + " WRN" + Fore.RESET + Fore.LIGHTBLACK_EX + "] " + Fore.LIGHTWHITE_EX + "* " + text)
    with open("log.txt", "a", encoding="ANSI") as f:
        f.write("[" + gettime() + " WRN] * " + text + "\n")

def error(text):
    print(Fore.LIGHTBLACK_EX + "[" + Fore.WHITE + gettime() + " " + Back.RED + Style.BRIGHT + Fore.LIGHTWHITE_EX + "ERR" + Back.RESET + Fore.RESET + Fore.LIGHTBLACK_EX + "] " + Fore.LIGHTWHITE_EX + "* " + text)
    with open("log.txt", "a", encoding="ANSI") as f:
        f.write("[" + gettime() + " ERR] * " + text + "\n")