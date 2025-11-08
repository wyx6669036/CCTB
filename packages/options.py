import packages.UtilsManager as utils
import CommandUI
import ctypes
import threading
import time
from colorama import Fore, init

init(autoreset=True)

def selectOption(choice):
    utils.info("Option selected: " + str(choice))
    if choice == 0:
        # 调用psexec运行taskkill结束studentmain.exe，没有技术含量，所有系统组件用的win7的，都是从legacy拿的，反正win10+都兼容，legacy0.4写系统区分的时候给我写死了
        ctypes.windll.shell32.ShellExecuteW(None, "runas", CommandUI.runningDir + "\\resource\\psexec.exe", " -s -accepteula " + CommandUI.runningDir + "\\resource\\CCTB.Taskkill.exe /F /IM studentmain.exe", None, 0)
        utils.info("Killed!")
    elif choice == 1:
        # 就是说呢，用的Coco抓包抓出来的神秘反全屏，写壳子写出了史山
        # 本来是想要新建一个窗口放后台持续发包，但是写了几天写炸了干脆放前台了，后面换gui了再尝试写
        utils.warn("This module will consume significant CPU and network resources. Do you wish to proceed?") # 神秘确认
        module2_choice = input("[Yes/No](Default N): ")
        if module2_choice.lower() == "yes" or module2_choice == "y":
            utils.info(Fore.LIGHTYELLOW_EX + "You can Press Ctrl+C to stop this module.")
            for i in ["5","4","3","2","1"]:
                utils.info(Fore.LIGHTYELLOW_EX + f"You can Press Ctrl+C to stop this module.({i})")
                time.sleep(1)
            module2_choice = True
        else:
            module2_choice = False
        # 这里写几分钟才写好，麻烦死了

        if module2_choice:
            try:
                utils.info("Starting Thread...")
                Thread = threading.Thread(target=module2_main())
                Thread.start()
                utils.info("Started!")
            except KeyboardInterrupt:
                utils.info("Stopped!")
                pass
        else:
            utils.info("Cancelled.")
            pass

    elif choice == 2:
        # 依旧是Coco写的神秘代码，效果是学生端看到老师发来的消息
        utils.info("Where would you like to send it?(eg. 192.168.153.130)")
        utils.info("If you dont input any args, it will send to all ips.")
        module3_choice = input("[IP](Default All): ")
        module3_text = input("[Text]: ")
        Thread = threading.Thread(target=module3_main(module3_choice, module3_text))
    else:
        utils.error("Invalid choice.")

    input(Fore.LIGHTYELLOW_EX + "\nPress Enter to continue..." + Fore.RESET)

def module2_main(status=True):
    while status: # 循环强制全班屏幕广播窗口化
        for i in utils.ip_scanner():
            utils.anti_full_screen(i[0])
            time.sleep(0.03)

def module3_main(choice, text):
    if choice == "": # 发送教室消息，不填是默认向所有人发送
        try:
            for i in utils.ip_scanner():
                ips = i[0]
                utils.info(f"Sending message:[{text}]...")
                utils.send_teacher_message(text, ips)
            utils.info("Finished.")
        except KeyboardInterrupt:
            utils.info("User input stopped.")
        except Exception as e:
            utils.error(e)
    else: # 如果不为空，尝试向对应ip发送，若ip不存在/瞎填，会报错但是有catch并转换为utils.error
        try:
            ips = choice
            utils.info(f"Sending message:[{text}]...")
            utils.send_teacher_message(text, ips)
        except KeyboardInterrupt:
            utils.info("User input stopped.")
        except Exception as e:
            utils.error(e)