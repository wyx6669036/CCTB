import msvcrt
import os
from colorama import init, Fore, Style
from packages import UtilsManager as utils

init(autoreset=True)

"""
变量对照表：
version：当前版本号
runningDir：当前运行目录
toolsDir：内置工具目录
"""
version = "beta 0.1.1"

runningDir = os.path.dirname(os.path.abspath(__file__))

options = [
    "1.Kill Mythware Classroom Management",
    "2.Enable \"Anti Full Screen Broadcast\" Thread",
    "3.Send teacher message",
]

# 主页面上方文字，准备改成legacy0.4信息多一点的样子，不知道会不会看着很乱，等着吧
texts = Fore.LIGHTBLUE_EX + """\
  ____ ____ _____ ____  
 / ___/ ___|_   _| __ ) 
| |  | |     | | |  _ \\ 
| |__| |___  | | | |_) |
 \\____\\____| |_| |____/  \n
""" + Fore.RED + """This project created by wyx6669036\n""" + Fore.RESET + "_"*60

def menu(selected_index):
    """显示菜单界面"""
    utils.Clear()
    print(texts)
    print()

    for i, option in enumerate(options):
        if i == selected_index:
            print(Style.BRIGHT + Fore.LIGHTBLUE_EX + f"> {option}" + Style.RESET_ALL)
        else:
            print(f"  {option}")

    print("\n使用 ↑ ↓ 键选择，按 Enter 执行，按 'q' 退出")


def main():
    selected_index = 0

    while True:
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


if __name__ == "__main__":
    main()