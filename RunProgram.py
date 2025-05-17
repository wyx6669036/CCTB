import os
from colorama import Fore, init

init(autoreset=True)

def RunProgram(psexec_dir, dir, system_run, DEBUG):
    if system_run == 'y':
        os.system(psexec_dir + '-s -i -accepteula ' + dir)
        if DEBUG == True:
            print(Fore.LIGHTYELLOW_EX + f'[DEBUG] psexec_dir: {psexec_dir}')
            input(Fore.LIGHTYELLOW_EX + f'[DEBUG] dir: {dir}')
    elif system_run == 'n':
        os.system(psexec_dir + '-i -accepteula ' + dir)
        if DEBUG == True:
            print(Fore.LIGHTYELLOW_EX + f'[DEBUG] psexec_dir: {psexec_dir}')
            input(Fore.LIGHTYELLOW_EX + f'[DEBUG] dir: {dir}')
    
    print(Fore.RED + '\n程序已退出\n')
    