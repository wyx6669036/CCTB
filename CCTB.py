import os
import sys
import ctypes

def run_in_program():
    program_path = input("\n请输入要运行的程序的完整路径: ")
    print('\n' +'='*30 + '\n\n控制台输出：')
    os.system('psexec -s '+ program_path)
    print("\n" + "="*30)
    print('\n程序已退出\n')

def run_out_program():
    program_path = input("\n请输入要运行的程序的完整路径: ")
    print('\n' +'='*30 + '\n\n控制台输出：')
    os.system('psexec -s -i '+ program_path)   
    print("\n" + "="*30)
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
        os.system('cls')  # 清空控制台输出
        print("\n" + "="*30)
        print("请选择一个选项:")
        print("1.关闭极域")
        print("2.强制关闭极域（适用于第一种无法关闭的情况）")
        print("3.以system权限运行程序")
        print("4.退出")
        print("="*30 + "\n")#列出支持的选项

        choice = input("\n输入选项前的数字以运行对应的功能: ")#用户选择
        os.system('cls')  # 清空控制台输出

        if choice == "1":#关闭极域
            print('\n' +'='*30 + '\n\n控制台输出：\n')
            os.system("taskkill /f /im studentmain.exe")
            print('\n' +'='*30)
            print("\n极域已关闭\n")
        elif choice == '2':#使用psexec提权至system关闭
            print('\n' + '='*30)
            print('如果有弹出窗口，请' + '点击' + 'Agree')
            print('\n控制台输出：')
            os.system('psexec -s taskkill /f /im studentmain.exe')
            print('\n' +'='*30)
            print("\n极域已关闭\n")
        elif choice == "3":#以system运行程序
            # if validate_path(program_path) and os.path.isfile(program_path):
            #     print("\n正在运行程序...\n")
            #     os.system(f'"{program_path}"')
            # else:
            #     print("\n无效的路径，请重新选择。\n")
            #人机ai写的啥啊
            os.system('cls')
            print("\n" + "="*30)
            print("请选择一个选项:")
            print("1.在程序内运行")
            print("2.在程序外运行（单独一个窗口）")
            print("="*30)

            run_program_choice = input("\n\n输入选项前的数字以运行对应的功能: ")#用户选择
            os.system('cls')  # 清空控制台输出

            if run_program_choice == '1':
                run_in_program()
            elif run_program_choice == '2':
                run_out_program()
            else:
                print("\n无效的选项，请重新选择。\n")
        elif choice == "4":#退出
            print("\n退出程序\n")
            break
        else:#无效选项
            print("\n无效的选项，请重新选择。\n")
        input("按下回车键继续...")

if __name__ == "__main__":#运行主函数
    main()