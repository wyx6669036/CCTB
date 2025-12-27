# CCTB

是的停更了几个月之久的CCTB回来了

> ⚠️ 注意：本工具仅用于学习和研究目的，请在合法合规的前提下使用。

## 项目简介

CCTB 是一个针对极域电子教室系统的控制工具箱，提供了多种实用功能来管理和控制运行极域电子教室的计算机。该项目基于对极域电子教室协议的抓包分析，可以实现对教室网络中学生端的控制。

## 目前拥有的功能

1. **结束极域进程** - 强制终止学生端的 `studentmain.exe` 进程
2. **反全屏广播** - 阻止教师端的全屏广播，使屏幕广播窗口化
3. **发送教师消息** - 伪装成教师向学生端发送消息


## 系统要求

- Windows 8.1+（可自行使用python3.7-编译使Windows7使用，但不保证稳定性）
- Python 3.13+（开发python版本为3.13）
- 管理员权限运行（可自动获取）

## 运行

我们更推荐你等待正式版/pre-release发布，而不是自行下载源码使用  
尽管我们的源码比最初稳定很多，但是我们仍旧不建议下载源码，这可能造成许多麻烦  

如果你真的要使用源码运行，我们也可以提供使用教程

### 安装依赖

```
bash
pip install -r requirements.txt
```
### 运行

```
bash
python main.py
```
你可以选择运行CommandUI.py或main.py，但是更推荐运行main.py  
main.py能够帮助你自动获取管理员权限，并保证日志正常运行  
除非你手动删除日志，否则在你手动运行CommandUI.py时，你的日志会接着上一次继续写入

## 配置说明

系统配置文件位于 `config/config.json`，包含以下配置项：

```json
{
    "debug": false,                        // 调试模式
    "target_port": 7500,                   // 目标端口
    "timeout": 5,                          // 超时时间（秒）
    "max_message_length": 954,             // 最大消息长度
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

