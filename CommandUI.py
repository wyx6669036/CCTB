import msvcrt
import os
from colorama import init, Fore, Style
from utils import UtilsManager as utils
from utils.impl.ErrorHandler import handle_exception, UserInputError
from utils.impl.ConfigManager import config

init(autoreset=True)

"""
变量对照表：
version：当前版本号
runningDir：当前运行目录
toolsDir：内置工具目录
"""
version = "beta 0.1.2"

runningDir = os.path.dirname(os.path.abspath(__file__))

options = [
    "1.Kill Mythware Classroom Management",
    "2.Enable \"Anti Full Screen Broadcast\" Thread",
    "3.Send teacher message",
    "4.Start application",
]

# 主页面上方文字，准备改成legacy0.4信息多一点的样子，不知道会不会看着很乱，等着吧
texts = Fore.LIGHTBLUE_EX + """\
   ____    ____   _____   ____  
  / ___|  / ___| |_   _| | __ ) 
 | |     | |       | |   |  _ \ 
 | |___  | |___    | |   | |_) |
  \____|  \____|   |_|   |____/ 
                                
""" + Fore.RED + """This project created by wyx6669036\n""" + Fore.RESET + "_"*60

@handle_exception(UserInputError, default_return=None, error_message="Menu display failed")
def menu(selected_index):
    """显示菜单界面"""
    utils.Clear()
    print(texts)
    print()

    for i, option in enumerate(options):
        if i == selected_index:
            # 使用加粗蓝色字体显示选中项
            print(Style.BRIGHT + Fore.LIGHTBLUE_EX + f"> {option}" + Style.RESET_ALL)
        else:
            print(f"  {option}")

    print("\n使用 ↑ ↓ 键选择，按 Enter 执行，按 'q' 退出")


@handle_exception(UserInputError, default_return=None, error_message="Command UI operation failed")
def main():
    selected_index = 0

    while True:
        try:
            menu(selected_index)

            # 等待按键输入
            key = msvcrt.getch()

            # 处理特殊按键（箭头键）
            if key == b'\xe0':  # 箭头键前缀
                key = msvcrt.getch()
                if key == b'H':  # 上箭头
                    selected_index = (selected_index - 1) % len(options)
                elif key == b'P':  # 下箭头
                    selected_index = (selected_index + 1) % len(options)
            # 处理普通按键
            elif key == b'\r':  # 回车键
                utils.selectOption(selected_index)
            elif key.lower() == b'q':  # 退出
                break
            # 其他按键不做处理，继续循环
            
        except KeyboardInterrupt:
            # 处理Ctrl+C中断
            print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
            continue
        except Exception as e:
            # 处理其他异常
            utils.error(f"An error occurred: {e}")
            print(f"\n{Fore.YELLOW}Press any key to continue or 'q' to quit...{Style.RESET_ALL}")
            key = msvcrt.getch()
            if key == b'q':
                break


if __name__ == "__main__":
    main()