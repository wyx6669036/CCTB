# CCTB - 极域课堂系统工具

CCTB是一个用于极域课堂系统的工具集，提供了多种实用功能，包括网络通信、IP扫描、性能监控等功能。

## 功能特性

- **网络通信**: 与极域课堂系统进行通信，包括发送教师消息、启动应用程序等功能
- **IP扫描**: 快速并发扫描局域网中的活跃主机
- **性能监控**: 实时监控系统资源使用情况，自动优化性能
- **日志记录**: 高级日志记录系统，支持多种日志级别和格式
- **错误处理**: 完善的错误处理机制，提供详细的错误信息和恢复策略
- **配置管理**: 灵活的配置管理系统，支持动态加载和更新配置

## 系统要求

- Windows操作系统
- Python 3.7+
- 管理员权限（部分功能需要）

## 安装说明

1. 克隆或下载项目代码
2. 安装依赖包：
   ```
   pip install -r requirements.txt
   ```
3. 运行主程序：
   ```
   python main.py
   ```

## 使用说明

### 基本使用

程序启动后会显示命令行界面，根据提示选择相应的功能：

1. IP扫描 - 扫描局域网中的活跃主机
2. 发送教师消息 - 向指定IP发送教师消息
3. 启动应用程序 - 在指定IP上启动应用程序
4. 性能监控 - 查看系统性能统计信息
5. 配置管理 - 查看和修改系统配置

### 高级使用

#### IP扫描

```python
from packages.utils.IPscanner import scan_ips, generate_ips_from_cidr

# 扫描指定网段
cidr = "192.168.1.0/24"
ips = generate_ips_from_cidr(cidr)
alive_hosts = scan_ips(ips, workers=200, timeout_ms=500)

for ip, rtt in alive_hosts:
    print(f"Host {ip} is alive, RTT: {rtt}ms")
```

#### 发送教师消息

```python
from packages import UtilsManager as utils

# 发送消息到指定IP
success = utils.send_teacher_message("Hello, students!", "192.168.1.100")
if success:
    print("Message sent successfully")
```

#### 性能监控

```python
from packages.utils.Performance import get_performance_stats, optimize_now

# 获取性能统计
stats = get_performance_stats()
print(f"CPU: {stats['current']['cpu']}%")
print(f"Memory: {stats['current']['memory_mb']}MB")

# 立即执行优化
optimize_now()
```

## 配置说明

系统配置文件位于 `config/config.json`，包含以下配置项：

```json
{
    "version": "1.0.0",                    // 版本号
    "debug": false,                        // 调试模式
    "target_port": 7500,                   // 目标端口
    "timeout": 5,                          // 超时时间（秒）
    "max_message_length": 954,             // 最大消息长度
    "log_level": "INFO",                   // 日志级别
    "log_file": "log.txt",                 // 日志文件
    "performance_monitoring": true,        // 是否启用性能监控
    "performance_monitor_interval": 5.0,   // 性能监控间隔（秒）
    "performance_auto_optimize": true,     // 是否启用自动优化
    "performance_optimize_interval": 30.0, // 优化检查间隔（秒）
    "max_scan_workers": 500,               // 最大扫描线程数
    "memory_threshold_mb": 200,            // 内存阈值（MB）
    "cpu_threshold_percent": 80            // CPU阈值（百分比）
}
```

日志配置文件位于 `config/logging.json`，包含详细的日志配置选项。

## 开发说明

### 项目结构

```
CCTB/
├── main.py                    # 主程序入口
├── packages/                  # 核心包
│   ├── UtilsManager.py        # 工具管理器
│   └── utils/                 # 工具模块
│       ├── ConfigManager.py   # 配置管理
│       ├── ErrorHandler.py    # 错误处理
│       ├── Log.py            # 日志记录
│       ├── AdvancedLog.py    # 高级日志记录
│       ├── LogManager.py     # 日志管理器
│       ├── Performance.py    # 性能监控
│       ├── IPscanner.py      # IP扫描
│       └── fuckMythware.py   # 极域通信
├── config/                    # 配置文件
│   ├── config.json           # 主配置文件
│   └── logging.json          # 日志配置文件
├── tests/                     # 单元测试
│   ├── test_config_manager.py
│   ├── test_error_handler.py
│   ├── test_advanced_log.py
│   └── test_performance.py
└── docs/                      # 文档目录
```

### 代码规范

1. 使用类型注解
2. 遵循PEP 8代码风格
3. 所有公共函数和类必须有文档字符串
4. 使用异常处理机制处理错误
5. 编写单元测试覆盖核心功能

### 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 更新日志

### v1.0.0
- 初始版本
- 实现基本功能
- 添加性能监控
- 完善错误处理

## 常见问题

### Q: 程序无法启动，提示权限不足
A: 部分功能需要管理员权限，请以管理员身份运行程序。

### Q: IP扫描速度慢
A: 可以通过配置文件调整 `max_scan_workers` 参数增加并发线程数。

### Q: 如何查看详细日志
A: 将配置文件中的 `log_level` 设置为 `DEBUG`，并检查日志文件。

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交Issue
- 发送邮件至：[your-email@example.com]

---

感谢使用CCTB！