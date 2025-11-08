# CCTB API文档

本文档详细描述了CCTB项目的API接口和使用方法。

## 核心模块

### ConfigManager - 配置管理器

`packages.utils.ConfigManager.ConfigManager`

配置管理器使用单例模式，提供配置的读取、设置、更新和持久化功能。

#### 方法

##### `get(key, default=None)`
获取配置值。

**参数:**
- `key` (str): 配置键名
- `default` (any): 默认值，当键不存在时返回

**返回值:**
- 配置值或默认值

**示例:**
```python
from packages.utils.ConfigManager import config

# 获取配置值
port = config.get("target_port", 7500)
debug = config.get("debug", False)
```

##### `set(key, value)`
设置配置值。

**参数:**
- `key` (str): 配置键名
- `value` (any): 配置值

**示例:**
```python
from packages.utils.ConfigManager import config

# 设置配置值
config.set("timeout", 10)
config.set("debug", True)
```

##### `update(config_dict)`
批量更新配置。

**参数:**
- `config_dict` (dict): 配置字典

**示例:**
```python
from packages.utils.ConfigManager import config

# 批量更新配置
config.update({
    "timeout": 10,
    "debug": True,
    "max_workers": 200
})
```

##### `save_to_file(file_path=None)`
保存配置到文件。

**参数:**
- `file_path` (str, 可选): 文件路径，默认为配置文件路径

**示例:**
```python
from packages.utils.ConfigManager import config

# 保存配置到文件
config.save_to_file()
```

##### `load_from_file(file_path=None)`
从文件加载配置。

**参数:**
- `file_path` (str, 可选): 文件路径，默认为配置文件路径

**示例:**
```python
from packages.utils.ConfigManager import config

# 从文件加载配置
config.load_from_file()
```

##### `load_logging_config(file_path=None)`
加载日志配置。

**参数:**
- `file_path` (str, 可选): 日志配置文件路径

**示例:**
```python
from packages.utils.ConfigManager import config

# 加载日志配置
config.load_logging_config()
```

---

### ErrorHandler - 错误处理

`packages.utils.ErrorHandler`

提供异常处理装饰器和预定义异常类。

#### 装饰器

##### `@handle_exception(exception_type, default_return=None, error_message=None, reraise=False)`
异常处理装饰器。

**参数:**
- `exception_type` (Exception or tuple): 要捕获的异常类型
- `default_return` (any): 发生异常时的默认返回值
- `error_message` (str): 自定义错误消息
- `reraise` (bool): 是否重新抛出异常

**示例:**
```python
from packages.utils.ErrorHandler import handle_exception, NetworkError

@handle_exception(NetworkError, default_return=False, error_message="Network operation failed")
def send_data(data):
    # 网络操作代码
    pass
```

#### 异常类

##### `CCTBException`
基础异常类，所有自定义异常的父类。

##### `NetworkError`
网络相关异常。

##### `SystemError`
系统相关异常。

##### `PermissionError`
权限相关异常。

##### `ValidationError`
验证相关异常。

#### 函数

##### `safe_execute(func, *args, **kwargs)`
安全执行函数，捕获所有异常。

**参数:**
- `func` (callable): 要执行的函数
- `*args`, `**kwargs`: 函数参数

**返回值:**
- 函数执行结果或None（如果发生异常）

**示例:**
```python
from packages.utils.ErrorHandler import safe_execute

# 安全执行函数
result = safe_execute(risky_function, arg1, arg2)
```

##### `validate_and_execute(validation_func, func, *args, **kwargs)`
验证后执行函数。

**参数:**
- `validation_func` (callable): 验证函数，返回True表示验证通过
- `func` (callable): 要执行的函数
- `*args`, `**kwargs`: 函数参数

**返回值:**
- 函数执行结果或None（如果验证失败或发生异常）

**示例:**
```python
from packages.utils.ErrorHandler import validate_and_execute

def validate_input(data):
    return isinstance(data, str) and len(data) > 0

# 验证后执行函数
result = validate_and_execute(validate_input, process_data, "test")
```

---

### LogManager - 日志管理器

`packages.utils.LogManager.LogManager`

日志管理器使用单例模式，提供日志记录器的创建、获取和配置功能。

#### 方法

##### `get_logger(name=None)`
获取日志记录器。

**参数:**
- `name` (str, 可选): 日志记录器名称

**返回值:**
- Logger实例

**示例:**
```python
from packages.utils.LogManager import log_manager

# 获取日志记录器
logger = log_manager.get_logger("my_module")
logger.info("This is an info message")
```

##### `create_logger(name, level=None, format=None, file_path=None, console_output=True)`
创建日志记录器。

**参数:**
- `name` (str): 日志记录器名称
- `level` (str or int): 日志级别
- `format` (str): 日志格式
- `file_path` (str): 日志文件路径
- `console_output` (bool): 是否输出到控制台

**返回值:**
- Logger实例

**示例:**
```python
from packages.utils.LogManager import log_manager

# 创建日志记录器
logger = log_manager.create_logger(
    "my_module",
    level="DEBUG",
    file_path="my_module.log"
)
logger.debug("This is a debug message")
```

##### `configure_from_config(config_dict=None)`
从配置字典配置日志系统。

**参数:**
- `config_dict` (dict, 可选): 配置字典

**示例:**
```python
from packages.utils.LogManager import log_manager

# 从配置字典配置日志系统
config = {
    "level": "INFO",
    "file_path": "app.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}
log_manager.configure_from_config(config)
```

##### `remove_logger(name)`
移除日志记录器。

**参数:**
- `name` (str): 日志记录器名称

**示例:**
```python
from packages.utils.LogManager import log_manager

# 移除日志记录器
log_manager.remove_logger("my_module")
```

---

### Performance - 性能监控

`packages.utils.Performance`

提供性能监控和资源优化功能。

#### 类

##### `PerformanceMonitor`
性能监控器，用于跟踪系统资源使用情况。

**方法:**

- `start_monitoring(interval=1.0)`: 开始性能监控
- `stop_monitoring()`: 停止性能监控
- `get_current_stats()`: 获取当前性能统计
- `get_average_stats()`: 获取平均性能统计
- `add_callback(callback)`: 添加性能数据回调函数

**示例:**
```python
from packages.utils.Performance import PerformanceMonitor

# 创建性能监控器
monitor = PerformanceMonitor()

# 开始监控
monitor.start_monitoring(interval=5.0)

# 获取当前统计
stats = monitor.get_current_stats()
print(f"CPU: {stats['cpu']}%, Memory: {stats['memory_mb']}MB")

# 停止监控
monitor.stop_monitoring()
```

##### `ResourceOptimizer`
资源优化器，用于管理系统资源。

**方法:**

- `add_rule(condition, action, description)`: 添加优化规则
- `start_auto_optimization(interval=30.0)`: 开始自动优化
- `stop_auto_optimization()`: 停止自动优化
- `optimize_now()`: 立即执行一次优化
- `get_rules_status()`: 获取优化规则状态

**示例:**
```python
from packages.utils.Performance import PerformanceMonitor, ResourceOptimizer

# 创建性能监控器和优化器
monitor = PerformanceMonitor()
optimizer = ResourceOptimizer(monitor)

# 添加内存优化规则
optimizer.add_rule(
    condition=lambda stats: stats.get("memory_mb", 0) > 200,
    action=lambda stats: print("High memory usage detected!"),
    description="High memory usage"
)

# 开始自动优化
optimizer.start_auto_optimization(interval=30.0)
```

#### 函数

##### `initialize_performance_manager()`
初始化性能管理器。

##### `start_performance_monitoring(interval=5.0, auto_optimize=True, optimize_interval=30.0)`
启动性能监控。

**参数:**
- `interval` (float): 监控间隔（秒）
- `auto_optimize` (bool): 是否启用自动优化
- `optimize_interval` (float): 优化检查间隔（秒）

##### `stop_performance_monitoring()`
停止性能监控。

##### `get_performance_stats()`
获取性能统计。

**返回值:**
- 包含当前统计、平均统计和规则状态的字典

##### `optimize_now()`
立即执行一次优化。

---

### IPscanner - IP扫描

`packages.utils.IPscanner`

提供IP扫描功能。

#### 函数

##### `get_local_ip()`
获取本地IP地址。

**返回值:**
- str: 本地IP地址

**示例:**
```python
from packages.utils.IPscanner import get_local_ip

# 获取本地IP
local_ip = get_local_ip()
print(f"Local IP: {local_ip}")
```

##### `generate_ips_from_cidr(cidr)`
从CIDR表示法生成IP地址列表。

**参数:**
- `cidr` (str): CIDR格式的网络地址

**返回值:**
- List[str]: IP地址列表

**示例:**
```python
from packages.utils.IPscanner import generate_ips_from_cidr

# 生成IP地址列表
cidr = "192.168.1.0/24"
ips = generate_ips_from_cidr(cidr)
print(f"Generated {len(ips)} IP addresses")
```

##### `ping_host(ip, timeout_ms=500)`
Ping指定IP地址。

**参数:**
- `ip` (str): 要ping的IP地址
- `timeout_ms` (int): 超时时间（毫秒）

**返回值:**
- Tuple[str, bool, float]: (ip, 是否存活, 延迟毫秒)

**示例:**
```python
from packages.utils.IPscanner import ping_host

# Ping主机
ip, alive, rtt = ping_host("192.168.1.1", timeout_ms=1000)
if alive:
    print(f"Host {ip} is alive, RTT: {rtt}ms")
else:
    print(f"Host {ip} is not reachable")
```

##### `scan_ips(ips, workers=200, timeout_ms=500)`
并发扫描IP列表。

**参数:**
- `ips` (Iterable[str]): 要扫描的IP地址列表
- `workers` (int): 并发线程数
- `timeout_ms` (int): ping超时时间（毫秒）

**返回值:**
- List[Tuple[str, float]]: 存活主机的(IP, 延迟毫秒)列表，按IP排序

**示例:**
```python
from packages.utils.IPscanner import scan_ips, generate_ips_from_cidr

# 扫描网段
cidr = "192.168.1.0/24"
ips = generate_ips_from_cidr(cidr)
alive_hosts = scan_ips(ips, workers=200, timeout_ms=500)

for ip, rtt in alive_hosts:
    print(f"Host {ip} is alive, RTT: {rtt}ms")
```

---

### fuckMythware - 极域通信

`packages.utils.fuckMythware`

提供与极域课堂系统通信的功能。

#### 函数

##### `anti_full_screen(target_ip, target_port=None)`
反全屏功能。

**参数:**
- `target_ip` (str): 目标IP地址
- `target_port` (int, 可选): 目标端口，默认从配置获取

**返回值:**
- bool: 操作是否成功

**示例:**
```python
from packages.utils.fuckMythware import anti_full_screen

# 反全屏
success = anti_full_screen("192.168.1.100")
if success:
    print("Anti full screen command sent successfully")
```

##### `send_teacher_message(text, target_ip, target_port=None)`
发送教师消息。

**参数:**
- `text` (str): 消息文本
- `target_ip` (str): 目标IP地址
- `target_port` (int, 可选): 目标端口，默认从配置获取

**返回值:**
- bool: 操作是否成功

**示例:**
```python
from packages.utils.fuckMythware import send_teacher_message

# 发送教师消息
success = send_teacher_message("Hello, students!", "192.168.1.100")
if success:
    print("Message sent successfully")
```

##### `start_applicaion(path, target_ip, target_port=None)`
启动应用程序。

**参数:**
- `path` (str): 应用程序路径
- `target_ip` (str): 目标IP地址
- `target_port` (int, 可选): 目标端口，默认从配置获取

**返回值:**
- bool: 操作是否成功

**示例:**
```python
from packages.utils.fuckMythware import start_applicaion

# 启动应用程序
success = start_applicaion("C:\\Windows\\System32\\notepad.exe", "192.168.1.100")
if success:
    print("Application started successfully")
```

---

### UtilsManager - 工具管理器

`packages.UtilsManager`

提供对各种工具函数的统一访问接口，带有错误处理。

#### 函数

##### `ip_scanner(*args, **kwargs)`
运行IP扫描器。

##### `anti_full_screen(target_ip, target_port=None)`
调用反全屏功能。

##### `send_teacher_message(text, target_ip, target_port=None)`
发送教师消息，带有错误处理。

##### `start_applicaion(path, target_ip, target_port=None)`
启动应用程序，带有错误处理。

##### `AdmCheck()`
检查管理员权限，带有错误处理。

##### `SysCheck()`
检查系统信息，带有错误处理。

##### `info(message)`
记录信息日志，带有错误处理。

##### `warn(message)`
记录警告日志，带有错误处理。

##### `error(message)`
记录错误日志，带有错误处理。

##### `Clear()`
清屏，带有错误处理。

##### `selectOption(choice)`
处理选项，带有错误处理。

##### `get_performance_stats()`
获取性能统计，带有错误处理。

##### `optimize_performance()`
立即执行性能优化，带有错误处理。

**示例:**
```python
from packages import UtilsManager as utils

# 使用工具管理器
utils.info("Starting application")
if not utils.AdmCheck():
    utils.error("Administrator privileges required")
    
# 获取性能统计
stats = utils.get_performance_stats()
utils.info(f"CPU usage: {stats['current']['cpu']}%")
```