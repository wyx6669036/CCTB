import os
import sys
import ctypes
import time
import winreg
from colorama import Fore

def main_text():# 主页面上方的文字
    print(Fore.LIGHTBLUE_EX + '  _____ _____ _______ ____  ')
    print(Fore.LIGHTBLUE_EX + ' / ____/ ____|__   __|  _ \ ')
    print(Fore.LIGHTBLUE_EX + '| |   | |       | |  | |_) |')
    print(Fore.LIGHTBLUE_EX + '| |   | |       | |  |  _ < ')
    print(Fore.LIGHTBLUE_EX + '| |___| |____   | |  | |_) |')
    print(Fore.LIGHTBLUE_EX + ' \_____\_____|  |_|  |____/ ')
    print(Fore.RED + '\nVersion 0.3\nThis project made by wyx6669036')
    print(Fore.RESET + '_'*100 + '\n')

def is_admin():# 检查权限
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    # 获取当前脚本的完整路径
    script_path = os.path.abspath(__file__)
    # 请求管理员权限
    params = f'"{script_path}"'
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

def main():# 主体
    if not is_admin():# 检查权限
        run_as_admin()
        sys.exit()

    psexec_dir = os.getcwd() + r'\psexec.exe '# 后面的空格不能删，因为在下面的代码里的参数前没有空格
    while True:
        ctypes.windll.kernel32.SetConsoleTitleW('CCTB v0.3 ——主页面')
        os.system('cls')  # 清空控制台输出
        main_text()
        print(Fore.LIGHTBLUE_EX + "请选择一个选项:")
        print(Fore.YELLOW + "1.关闭极域")
        print(Fore.YELLOW + "2.强制关闭极域（适用于第一种无法关闭的情况）")
        print(Fore.YELLOW + "3.以system权限运行程序")
        print(Fore.YELLOW + "4.禁用关机")
        print(Fore.YELLOW + "5.启用关机")
        print(Fore.YELLOW + "6.解除所有限制")
        print(Fore.YELLOW + "7.退出")# 列出支持的选项

        choice = input(Fore.LIGHTYELLOW_EX + "\n输入选项前的数字以运行对应的功能: ")# 用户选择
        os.system('cls')  # 清空控制台输出

        if choice == "1":# 关闭极域
            ctypes.windll.kernel32.SetConsoleTitleW('CCTB v0.3 ——关闭极域')
            main_text()
            print(Fore.RESET + '控制台输出：\n')
            os.system("taskkill /f /im studentmain.exe")
            print(Fore.RED + "\n极域已关闭\n")

        elif choice == '2':# 使用psexec提权至system关闭
            ctypes.windll.kernel32.SetConsoleTitleW('CCTB v0.3 ——强制关闭极域')
            main_text()
            print(Fore.LIGHTBLUE_EX + '如果有弹出窗口，请' + Fore.RED + '点击' + Fore.YELLOW + 'Agree')
            print(Fore.RESET + '\n控制台输出：')
            os.system(psexec_dir + '-s taskkill /f /im studentmain.exe')
            ctypes.windll.kernel32.SetConsoleTitleW('CCTB v0.3 ——强制关闭极域')
            print(Fore.RED + "\n极域已关闭\n")

        elif choice == "3":# 以system运行程序  # 这里原本是选择是否嵌入程序内的，但是发现直接全部单独开窗口更好，也防止傻逼在嵌入功能开gui没界面然后🐕叫
            ctypes.windll.kernel32.SetConsoleTitleW('CCTB v0.3 ——以system权限运行程序')
            os.system('cls')
            main_text()
            program_path = input(Fore.LIGHTYELLOW_EX + "请输入要运行的程序的完整路径: ")
            print(Fore.LIGHTBLUE_EX + '如果有弹出窗口，请' + Fore.RED + '点击' + Fore.YELLOW + 'Agree')
            print(Fore.RESET + '\n控制台输出：')
            os.system(psexec_dir + '-s -i '+ program_path)
            ctypes.windll.kernel32.SetConsoleTitleW('CCTB 0.3 ——以system权限运行程序') 
            print(Fore.RED + '\n程序已退出\n')

        elif choice == "4":# 禁用关机（不防电源线、长按关机键）
            main_text()    # 理论上应该叫电源选项，但是可能有人看不懂
            ctypes.windll.kernel32.SetConsoleTitleW('CCTB v0.3 ——禁用关机')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer') as key:
                winreg.SetValueEx(key,'NoClose',0,winreg.REG_DWORD,1)
                print(Fore.LIGHTCYAN_EX + '已将值 "NoClose" 设置为 "1"')# 删除开始菜单的关机按钮
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer') as key:
                winreg.SetValueEx(key,'HidePowerOptions',0,winreg.REG_DWORD,1)
                print(Fore.LIGHTCYAN_EX + '已将值 "HidePowerOptions" 设置为 "1"')# 隐藏Ctrl + Alt + Del屏幕的关机按钮（其实这个功能就能顺便隐藏开始菜单的了）
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\PolicyManager\default\Start\HideShutDown') as key:
                winreg.SetValueEx(key,'value',0,winreg.REG_DWORD,1)
                print(Fore.LIGHTCYAN_EX + '已将值 "value" 设置为 "1"')# 下面是针对登陆界面的按钮，全部搞上不怕出问题
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\PolicyManager\default\Start\HideSignOut') as key:
                winreg.SetValueEx(key,'value',0,winreg.REG_DWORD,1)
                print(Fore.LIGHTCYAN_EX + '已将值 "value" 设置为 "1"')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\PolicyManager\default\Start\HideRestart') as key:
                winreg.SetValueEx(key,'value',0,winreg.REG_DWORD,1)
                print(Fore.LIGHTCYAN_EX + '已将值 "value" 设置为 "1"')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\PolicyManager\default\Start\HideSwitchAccount') as key:
                winreg.SetValueEx(key,'value',0,winreg.REG_DWORD,1)
                print(Fore.LIGHTCYAN_EX + '已将值 "value" 设置为 "1"')

        elif choice == "5":# 启用关机
            main_text()
            ctypes.windll.kernel32.SetConsoleTitleW('CCTB v0.3 ——启用开机')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer') as key:
                winreg.SetValueEx(key,'NoClose',0,winreg.REG_DWORD,0)
                print(Fore.LIGHTCYAN_EX + '已将值 "NoClose" 设置为 "0"')# 恢复开始菜单的电源选项
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer') as key:
                winreg.SetValueEx(key,'HidePowerOptions',0,winreg.REG_DWORD,0)
                print(Fore.LIGHTCYAN_EX + '已将值 "HidePowerOptions" 设置为 "0"')# 恢复Ctrl + Alt + Del屏幕的关机按钮
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\PolicyManager\default\Start\HideShutDown') as key:
                winreg.SetValueEx(key,'value',0,winreg.REG_DWORD,0)
                print(Fore.LIGHTCYAN_EX + '已将值 "value" 设置为 "0"')# 将登陆界面的按钮还原
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\PolicyManager\default\Start\HideSignOut') as key:
                winreg.SetValueEx(key,'value',0,winreg.REG_DWORD,0)
                print(Fore.LIGHTCYAN_EX + '已将值 "value" 设置为 "0"')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\PolicyManager\default\Start\HideRestart') as key:
                winreg.SetValueEx(key,'value',0,winreg.REG_DWORD,0)
                print(Fore.LIGHTCYAN_EX + '已将值 "value" 设置为 "0"')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\PolicyManager\default\Start\HideSwitchAccount') as key:
                winreg.SetValueEx(key,'value',0,winreg.REG_DWORD,0)
                print(Fore.LIGHTCYAN_EX + '已将值 "value" 设置为 "0"')

        elif choice == "6":# 解除所有限制
            main_text()
            ctypes.windll.kernel32.SetConsoleTitleW('CCTB v0.3 ——解除所有限制')
            parent_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion", 0, winreg.KEY_WRITE)
            winreg.DeleteKey(parent_key, "Policies")# 删除本地主机的限制
            print(Fore.LIGHTCYAN_EX + '已删除本地主机Policies限制')
            parent_key.Close()
            # ========================================================================== 这是分割线，防止瞎子传奇之寻找眼珠子
            parent_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion", 0, winreg.KEY_WRITE)
            winreg.DeleteKey(parent_key, "Policies")# 删除当前用户的限制
            print(Fore.LIGHTCYAN_EX + '已删除当前用户Policies限制')
            parent_key.Close()
            print(Fore.LIGHTBLUE_EX + '如果执行过“禁用关机”，请' + Fore.RED + '重新执行' + Fore.YELLOW + '禁用关机')

        elif choice == "7":# 退出
            break

        else:# 无效选项
            main_text()
            print(Fore.RED + "无效的选项，请重新选择。\n")
        
        for i in ['3','2','1']:# 用dick想出来的倒计时，比硬堆叠好点...吧
            print(Fore.LIGHTYELLOW_EX + '返回（' + i + '）', end = '\r')
            time.sleep(1)

if __name__ == "__main__":# 运行
    main()