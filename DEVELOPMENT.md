# 开发文档

## 架构概述

CCTB项目采用模块化架构设计，将功能划分为独立的模块，每个模块负责特定的功能领域。这种设计提高了代码的可维护性、可扩展性和可重用性。

## 核心模块详解

### 1. ErrorHandler (错误处理模块)

**位置**: `packages/utils/ErrorHandler.py`

**功能**:
- 提供统一的错误处理机制
- 异常捕获和记录
- 错误上下文管理
- 安全执行包装器

**主要方法**:
- `safe_execute(func, context=None, default=None)`: 安全执行函数，捕获并处理异常
- `log_error(error, context=None)`: 记录错误信息
- `handle_exception(func, context=None)`: 异常处理装饰器

**使用示例**:
```python
from packages.utils.ErrorHandler import error_handler

def my_function():
    def _internal():
        # 可能出错的操作
        result = risky_operation()
        return result
    
    return error_handler.safe_execute(_internal, context="My function", 
                                    default=lambda: None)
```

### 2. ThreadManager (线程管理模块)

**位置**: `packages/utils/ThreadManager.py`

**功能**:
- 管理应用程序中的线程
- 线程创建和启动
- 线程状态监控
- 线程安全清理

**主要方法**:
- `start_thread(target, name=None, daemon=True)`: 启动新线程
- `stop_thread(thread_id)`: 停止指定线程
- `get_thread_status(thread_id)`: 获取线程状态
- `get_all_threads()`: 获取所有线程信息
- `cleanup_threads()`: 清理所有线程

**使用示例**:
```python
from packages.utils.ThreadManager import thread_manager

# 启动线程
thread_id = thread_manager.start_thread(target=my_function, name="MyThread")

# 获取线程状态
thread_status = thread_manager.get_thread_status(thread_id)

# 停止线程
thread_manager.stop_thread(thread_id)
```

### 3. InteractionHelper (用户交互模块)

**位置**: `packages/utils/InteractionHelper.py`

**功能**:
- 处理用户交互
- 用户输入获取
- 确认对话框
- 键盘输入处理

**主要方法**:
- `get_user_input(prompt, default=None, validation=None)`: 获取用户输入
- `confirm_action(message, default=True)`: 显示确认对话框
- `wait_for_keypress(message=None)`: 等待用户按键
- `select_option(options, prompt="Select an option")`: 选项选择

**使用示例**:
```python
from packages.utils.InteractionHelper import interaction_helper

# 获取用户输入
user_input = interaction_helper.get_user_input("Enter value: ", default="default")

# 确认操作
confirmed = interaction_helper.confirm_action("Are you sure?")

# 等待按键
interaction_helper.wait_for_keypress("Press Enter to continue...")
```

### 4. NetworkManager (网络管理模块)

**位置**: `packages/utils/NetworkManager.py`

**功能**:
- 处理网络相关功能
- IP扫描
- 网络连接测试
- 数据包发送

**主要方法**:
- `scan_network(ip_range, timeout=1)`: 扫描网络中的主机
- `test_connection(host, port, timeout=3)`: 测试网络连接
- `send_udp_packet(host, port, data)`: 发送UDP数据包
- `get_local_ip()`: 获取本地IP地址

**使用示例**:
```python
from packages.utils.NetworkManager import network_manager

# 扫描网络
hosts = network_manager.scan_network("192.168.1.0/24")

# 测试连接
is_connected = network_manager.test_connection("192.168.1.1", 80)

# 发送UDP数据包
network_manager.send_udp_packet("192.168.1.100", 8080, b"Hello")
```

### 5. SystemManager (系统管理模块)

**位置**: `packages/utils/SystemManager.py`

**功能**:
- 处理系统相关功能
- 进程管理
- 系统信息收集
- 权限检查

**主要方法**:
- `check_admin_privileges()`: 检查管理员权限
- `get_process_list()`: 获取进程列表
- `kill_process(pid)`: 终止进程
- `get_system_info()`: 获取系统信息
- `execute_command(command)`: 执行系统命令

**使用示例**:
```python
from packages.utils.SystemManager import system_manager

# 检查管理员权限
is_admin = system_manager.check_admin_privileges()

# 获取进程列表
processes = system_manager.get_process_list()

# 终止进程
system_manager.kill_process(1234)
```

### 6. UIManager (UI管理模块)

**位置**: `packages/utils/UIManager.py`

**功能**:
- 处理用户界面相关功能
- 菜单显示
- 消息展示
- 界面状态管理

**主要方法**:
- `display_menu(options, selected_index=0)`: 显示菜单
- `display_message(message, level="info")`: 显示消息
- `clear_screen()`: 清屏
- `print_startup_info()`: 打印启动信息

**使用示例**:
```python
from packages.utils.UIManager import ui_manager

# 显示菜单
selected = ui_manager.display_menu(["Option 1", "Option 2", "Option 3"])

# 显示消息
ui_manager.display_message("Operation completed", "success")

# 清屏
ui_manager.clear_screen()
```

## 应用程序流程

### 1. 启动流程 (main.py)

1. 初始化应用状态
2. 加载配置
3. 检查管理员权限
4. 启动UI界面

### 2. UI流程 (CommandUI.py)

1. 显示主菜单
2. 处理用户输入
3. 执行相应操作
4. 更新界面状态

## 错误处理策略

所有模块使用统一的错误处理机制：

1. **捕获异常**: 使用`error_handler.safe_execute`包装可能出错的代码
2. **记录错误**: 错误信息被记录到日志文件
3. **提供上下文**: 为每个操作提供上下文信息，便于调试
4. **优雅降级**: 提供默认行为，避免程序崩溃

## 线程管理策略

1. **线程创建**: 使用`thread_manager.start_thread`创建线程
2. **线程监控**: 定期检查线程状态
3. **线程清理**: 程序退出时清理所有线程
4. **线程安全**: 使用适当的同步机制保护共享资源

## 用户交互策略

1. **输入验证**: 验证用户输入的有效性
2. **默认值**: 为输入提供合理的默认值
3. **确认操作**: 对危险操作要求用户确认
4. **反馈**: 为操作提供及时反馈

## 扩展指南

### 添加新功能模块

1. 在`packages/utils/`目录下创建新模块文件
2. 实现模块功能，遵循现有代码风格
3. 使用统一的错误处理和线程管理机制
4. 更新相关文档

### 修改现有模块

1. 理解模块的职责和接口
2. 保持向后兼容性
3. 添加适当的错误处理
4. 更新单元测试和文档

## 代码规范

1. **命名**: 使用描述性的变量和函数名
2. **注释**: 为复杂逻辑添加注释
3. **错误处理**: 使用统一的错误处理机制
4. **文档**: 为公共方法添加文档字符串
5. **测试**: 为新功能添加测试用例

## 性能考虑

1. **资源管理**: 及时释放不再使用的资源
2. **线程管理**: 避免创建过多线程
3. **网络操作**: 使用适当的超时设置
4. **缓存**: 对频繁访问的数据使用缓存

## 安全考虑

1. **输入验证**: 验证所有用户输入
2. **权限检查**: 在执行敏感操作前检查权限
3. **数据保护**: 保护敏感数据不被泄露
4. **错误信息**: 避免在错误信息中泄露敏感信息