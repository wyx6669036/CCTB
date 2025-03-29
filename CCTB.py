import os
import sys
import ctypes
import time
import winreg

def main_text():
    print('  _____ _____ _______ ____  ')
    print(' / ____/ ____|__   __|  _ \ ')
    print('| |   | |       | |  | |_) |')
    print('| |   | |       | |  |  _ < ')
    print('| |___| |____   | |  | |_) |')
    print(' \_____\_____|  |_|  |____/ ')
    print('\nVersion 0.2\nThis project made by wyx6669036')
    print('_'*100 + '\n')

def run_in_program():
    main_text()
    program_path = input("请输入要运行的程序的完整路径: ")
    print('如果有弹出窗口，请' + '点击' + 'Agree')
    print('\n控制台输出：')
    os.system('psexec -s '+ program_path)
    ctypes.windll.kernel32.SetConsoleTitleW('CCTB v1.0 ——程序嵌入')
    print('\n程序已退出\n')

def run_out_program():
    main_text()
    program_path = input("请输入要运行的程序的完整路径: ")
    print('如果有弹出窗口，请' + '点击' + 'Agree')
    print('\n控制台输出：')
    os.system('psexec -s -i '+ program_path)
    ctypes.windll.kernel32.SetConsoleTitleW('CCTB v1.0 ——外部窗口') 
    print('\n程序已退出\n')

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    # 获取当前脚本的完整路径
    script_path = os.path.abspath(__file__)
    # 使用 ShellExecuteEx 请求管理员权限
    params = f'"{script_path}"'
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

def main():#主函数
    if not is_admin():
        # print("请以管理员权限运行此程序。")      #果然不该让傻逼ai帮忙写的
        # input("按下回车键退出...")   #还得我手动删一遍
        run_as_admin()
        sys.exit()

    while True:
        ctypes.windll.kernel32.SetConsoleTitleW('CCTB v1.0 ——主页面')
        os.system('cls')  # 清空控制台输出
        main_text()
        print("请选择一个选项:")
        print("1.关闭极域")
        print("2.强制关闭极域（适用于第一种无法关闭的情况）")
        print("3.以system权限运行程序")
        print("4.禁用关机")
        print("5.启用关机")
        print("6.退出")#列出支持的选项

        choice = input("\n输入选项前的数字以运行对应的功能: ")#用户选择
        os.system('cls')  # 清空控制台输出

        if choice == "1":#关闭极域
            ctypes.windll.kernel32.SetConsoleTitleW('CCTB v1.0 ——关闭极域')
            main_text()
            print('控制台输出：\n')
            os.system("taskkill /f /im studentmain.exe")
            print("\n极域已关闭\n")
        elif choice == '2':#使用psexec提权至system关闭
            ctypes.windll.kernel32.SetConsoleTitleW('CCTB v1.0 ——强制关闭极域')
            main_text()
            print('如果有弹出窗口，请' + '点击' + 'Agree')
            print('\n控制台输出：')
            os.system('psexec -s taskkill /f /im studentmain.exe')
            ctypes.windll.kernel32.SetConsoleTitleW('CCTB v1.0 ——强制关闭极域')
            print("\n极域已关闭\n")
        elif choice == "3":#以system运行程序
            # if validate_path(program_path) and os.path.isfile(program_path):
            #     print(Fore.GREEN + "\n正在运行程序...\n")
            #     os.system(f'"{program_path}"')
            # else:
            #     print("\n无效的路径，请重新选择。\n")
            #人机ai写的啥啊
            ctypes.windll.kernel32.SetConsoleTitleW('CCTB v1.0 ——以system权限运行程序')
            os.system('cls')
            main_text()
            print("请选择一个选项:")
            print("1.在程序内运行")
            print("2.在程序外运行（单独一个窗口）")#二级菜单

            run_program_choice = input("\n输入选项前的数字以运行对应的功能: ")#用户选择
            os.system('cls')  # 清空控制台输出

            if run_program_choice == '1':
                ctypes.windll.kernel32.SetConsoleTitleW('CCTB v1.0 ——程序嵌入')
                run_in_program()
            elif run_program_choice == '2':
                ctypes.windll.kernel32.SetConsoleTitleW('CCTB v1.0 ——外部窗口')
                run_out_program()
            else:
                main_text()
                print("无效的选项，请重新选择。\n")
        elif choice == "4":#禁用关机（不防电源线、长按关机键）
            main_text()    #理论上应该叫电源选项，但是可能有人看不懂
            ctypes.windll.kernel32.SetConsoleTitleW('CCTB v1.0 ——禁用关机')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer') as key:
                winreg.SetValueEx(key,'NoClose',0,winreg.REG_DWORD,1)
                print('已将值 "NoClose" 设置为 "1"')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer') as key:
                winreg.SetValueEx(key,'HidePowerOptions',0,winreg.REG_DWORD,1)
                print('已将值 "HidePowerOptions" 设置为 "1"')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\PolicyManager\default\Start\HideShutDown') as key:
                winreg.SetValueEx(key,'value',0,winreg.REG_DWORD,1)
                print('已将值 "value" 设置为 "1"')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\PolicyManager\default\Start\HideSignOut') as key:
                winreg.SetValueEx(key,'value',0,winreg.REG_DWORD,1)
                print('已将值 "value" 设置为 "1"')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\PolicyManager\default\Start\HideRestart') as key:
                winreg.SetValueEx(key,'value',0,winreg.REG_DWORD,1)
                print('已将值 "value" 设置为 "1"')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\PolicyManager\default\Start\HideSwitchAccount') as key:
                winreg.SetValueEx(key,'value',0,winreg.REG_DWORD,1)
                print('已将值 "value" 设置为 "1"')
        elif choice == "5":#启用关机
            main_text()
            ctypes.windll.kernel32.SetConsoleTitleW('CCTB v1.0 ——启用开机')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer') as key:
                winreg.SetValueEx(key,'NoClose',0,winreg.REG_DWORD,0)
                print('已将值 "NoClose" 设置为 "0"')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer') as key:
                winreg.SetValueEx(key,'HidePowerOptions',0,winreg.REG_DWORD,0)
                print('已将值 "HidePowerOptions" 设置为 "0"')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\PolicyManager\default\Start\HideShutDown') as key:
                winreg.SetValueEx(key,'value',0,winreg.REG_DWORD,0)
                print('已将值 "value" 设置为 "0"')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\PolicyManager\default\Start\HideSignOut') as key:
                winreg.SetValueEx(key,'value',0,winreg.REG_DWORD,0)
                print('已将值 "value" 设置为 "0"')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\PolicyManager\default\Start\HideRestart') as key:
                winreg.SetValueEx(key,'value',0,winreg.REG_DWORD,0)
                print('已将值 "value" 设置为 "0"')
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\PolicyManager\default\Start\HideSwitchAccount') as key:
                winreg.SetValueEx(key,'value',0,winreg.REG_DWORD,0)
                print('已将值 "value" 设置为 "0"')
        elif choice == "6":#退出
            break
        else:#无效选项
            main_text()
            print("无效的选项，请重新选择。\n")
        # print('返回（3）')
        # time.sleep(3)
        print('返回（3）',end='\r')
        time.sleep(1)
        print('返回（2）',end='\r')
        time.sleep(1)
        print('返回（1）',end='\r')
        time.sleep(1)

if __name__ == "__main__":#运行主函数
    main()