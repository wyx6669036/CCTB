# API 文档

## ErrorHandler API

### safe_execute(func, context=None, default=None)

安全执行函数，捕获并处理异常。

**参数**:
- `func` (callable): 要执行的函数
- `context` (str, optional): 错误上下文信息，默认为None
- `default` (callable, optional): 出错时执行的默认函数，默认为None

**返回值**:
- 函数执行结果或默认函数的返回值

**示例**:
```python
from packages.utils.ErrorHandler import error_handler

def risky_operation():
    return 1 / 0  # 会引发异常

result = error_handler.safe_execute(
    risky_operation, 
    context="Division operation", 
    default=lambda: 0
)
# result = 0
```

### log_error(error, context=None)

记录错误信息。

**参数**:
- `error` (Exception): 异常对象
- `context` (str, optional): 错误上下文信息，默认为None

**示例**:
```python
from packages.utils.ErrorHandler import error_handler

try:
    risky_operation()
except Exception as e:
    error_handler.log_error(e, "Risky operation context")
```

## ThreadManager API

### start_thread(target, name=None, daemon=True)

启动新线程。

**参数**:
- `target` (callable): 线程目标函数
- `name` (str, optional): 线程名称，默认为None
- `daemon` (bool, optional): 是否设置为守护线程，默认为True

**返回值**:
- `str`: 线程ID

**示例**:
```python
from packages.utils.ThreadManager import thread_manager

def my_task():
    print("Task running")

thread_id = thread_manager.start_thread(my_task, name="MyTask")
```

### stop_thread(thread_id)

停止指定线程。

**参数**:
- `thread_id` (str): 线程ID

**返回值**:
- `bool`: 是否成功停止线程

**示例**:
```python
from packages.utils.ThreadManager import thread_manager

thread_id = thread_manager.start_thread(my_task)
success = thread_manager.stop_thread(thread_id)
```

### get_thread_status(thread_id)

获取线程状态。

**参数**:
- `thread_id` (str): 线程ID

**返回值**:
- `dict`: 包含线程状态的字典

**示例**:
```python
from packages.utils.ThreadManager import thread_manager

thread_id = thread_manager.start_thread(my_task)
status = thread_manager.get_thread_status(thread_id)
print(status['status'])  # 'running', 'stopped', etc.
```

### get_all_threads()

获取所有线程信息。

**返回值**:
- `dict`: 包含所有线程信息的字典

**示例**:
```python
from packages.utils.ThreadManager import thread_manager

threads = thread_manager.get_all_threads()
for thread_id, thread_info in threads.items():
    print(f"Thread {thread_id}: {thread_info['status']}")
```

### cleanup_threads()

清理所有线程。

**示例**:
```python
from packages.utils.ThreadManager import thread_manager

thread_manager.cleanup_threads()
```

## InteractionHelper API

### get_user_input(prompt, default=None, validation=None)

获取用户输入。

**参数**:
- `prompt` (str): 提示信息
- `default` (any, optional): 默认值，默认为None
- `validation` (callable, optional): 验证函数，默认为None

**返回值**:
- `str`: 用户输入或默认值

**示例**:
```python
from packages.utils.InteractionHelper import interaction_helper

# 基本用法
name = interaction_helper.get_user_input("Enter your name: ")

# 带默认值
age = interaction_helper.get_user_input("Enter your age: ", default="18")

# 带验证
port = interaction_helper.get_user_input(
    "Enter port: ", 
    validation=lambda x: x.isdigit() and 0 < int(x) < 65536
)
```

### confirm_action(message, default=True)

显示确认对话框。

**参数**:
- `message` (str): 确认消息
- `default` (bool, optional): 默认选择，默认为True

**返回值**:
- `bool`: 用户确认结果

**示例**:
```python
from packages.utils.InteractionHelper import interaction_helper

if interaction_helper.confirm_action("Delete file?"):
    # 删除文件
    pass
```

### wait_for_keypress(message=None)

等待用户按键。

**参数**:
- `message` (str, optional): 显示的消息，默认为None

**示例**:
```python
from packages.utils.InteractionHelper import interaction_helper

interaction_helper.wait_for_keypress("Press Enter to continue...")
```

### select_option(options, prompt="Select an option")

选项选择。

**参数**:
- `options` (list): 选项列表
- `prompt` (str, optional): 提示信息，默认为"Select an option"

**返回值**:
- `int`: 选择的选项索引

**示例**:
```python
from packages.utils.InteractionHelper import interaction_helper

options = ["Option 1", "Option 2", "Option 3"]
selected = interaction_helper.select_option(options, "Choose an option:")
print(f"You selected: {options[selected]}")
```

## NetworkManager API

### scan_network(ip_range, timeout=1)

扫描网络中的主机。

**参数**:
- `ip_range` (str): IP范围，如"192.168.1.0/24"
- `timeout` (int, optional): 超时时间（秒），默认为1

**返回值**:
- `list`: 活跃主机列表

**示例**:
```python
from packages.utils.NetworkManager import network_manager

hosts = network_manager.scan_network("192.168.1.0/24")
for host in hosts:
    print(f"Host found: {host}")
```

### test_connection(host, port, timeout=3)

测试网络连接。

**参数**:
- `host` (str): 主机地址
- `port` (int): 端口号
- `timeout` (int, optional): 超时时间（秒），默认为3

**返回值**:
- `bool`: 连接是否成功

**示例**:
```python
from packages.utils.NetworkManager import network_manager

if network_manager.test_connection("192.168.1.1", 80):
    print("Connection successful")
else:
    print("Connection failed")
```

### send_udp_packet(host, port, data)

发送UDP数据包。

**参数**:
- `host` (str): 目标主机
- `port` (int): 目标端口
- `data` (bytes): 要发送的数据

**示例**:
```python
from packages.utils.NetworkManager import network_manager

network_manager.send_udp_packet("192.168.1.100", 8080, b"Hello")
```

### get_local_ip()

获取本地IP地址。

**返回值**:
- `str`: 本地IP地址

**示例**:
```python
from packages.utils.NetworkManager import network_manager

local_ip = network_manager.get_local_ip()
print(f"Local IP: {local_ip}")
```

## SystemManager API

### check_admin_privileges()

检查管理员权限。

**返回值**:
- `bool`: 是否具有管理员权限

**示例**:
```python
from packages.utils.SystemManager import system_manager

if system_manager.check_admin_privileges():
    print("Running with admin privileges")
else:
    print("Running without admin privileges")
```

### get_process_list()

获取进程列表。

**返回值**:
- `list`: 进程信息列表

**示例**:
```python
from packages.utils.SystemManager import system_manager

processes = system_manager.get_process_list()
for process in processes:
    print(f"PID: {process['pid']}, Name: {process['name']}")
```

### kill_process(pid)

终止进程。

**参数**:
- `pid` (int): 进程ID

**返回值**:
- `bool`: 是否成功终止进程

**示例**:
```python
from packages.utils.SystemManager import system_manager

success = system_manager.kill_process(1234)
if success:
    print("Process killed successfully")
else:
    print("Failed to kill process")
```

### get_system_info()

获取系统信息。

**返回值**:
- `dict`: 系统信息字典

**示例**:
```python
from packages.utils.SystemManager import system_manager

info = system_manager.get_system_info()
print(f"OS: {info['os']}")
print(f"Architecture: {info['architecture']}")
```

### execute_command(command)

执行系统命令。

**参数**:
- `command` (str): 要执行的命令

**返回值**:
- `dict`: 包含执行结果的字典

**示例**:
```python
from packages.utils.SystemManager import system_manager

result = system_manager.execute_command("dir")
print(f"Output: {result['output']}")
print(f"Error: {result['error']}")
print(f"Return code: {result['return_code']}")
```

## UIManager API

### display_menu(options, selected_index=0)

显示菜单。

**参数**:
- `options` (list): 选项列表
- `selected_index` (int, optional): 默认选中项索引，默认为0

**返回值**:
- `int`: 用户选择的选项索引

**示例**:
```python
from packages.utils.UIManager import ui_manager

options = ["Option 1", "Option 2", "Option 3"]
selected = ui_manager.display_menu(options)
print(f"You selected: {options[selected]}")
```

### display_message(message, level="info")

显示消息。

**参数**:
- `message` (str): 消息内容
- `level` (str, optional): 消息级别，默认为"info"

**示例**:
```python
from packages.utils.UIManager import ui_manager

ui_manager.display_message("Operation completed", "success")
ui_manager.display_message("An error occurred", "error")
```

### clear_screen()

清屏。

**示例**:
```python
from packages.utils.UIManager import ui_manager

ui_manager.clear_screen()
```

### print_startup_info()

打印启动信息。

**示例**:
```python
from packages.utils.UIManager import ui_manager

ui_manager.print_startup_info()
```