# CCTB - Classroom Control Tool Box

## 项目简介

CCTB (Classroom Control Tool Box) 是一个教室控制工具箱，提供多种网络和系统管理功能，适用于教育环境中的计算机教室管理。

## 功能特性

- 网络扫描与发现
- 远程命令执行
- 系统信息收集
- 进程管理
- 注册表操作
- 反全屏控制
- 消息广播

## 项目结构

```
CCTB/
├── CommandUI.py          # 命令行用户界面
├── main.py              # 主程序入口
├── packages/            # 核心功能包
│   ├── UtilsManager.py  # 工具管理器
│   ├── options.py       # 选项处理
│   └── utils/           # 工具模块
│       ├── ErrorHandler.py      # 统一错误处理
│       ├── ThreadManager.py    # 线程管理
│       ├── InteractionHelper.py # 用户交互
│       ├── NetworkManager.py   # 网络管理
│       ├── SystemManager.py    # 系统管理
│       ├── UIManager.py        # UI管理
│       └── ...                 # 其他工具模块
└── resources/           # 资源文件
    ├── CCTB.Command.exe
    ├── CCTB.Regedit.exe
    ├── CCTB.Taskkill.exe
    ├── CCTB.Taskmgr.exe
    ├── PsExec.exe
    └── zh-cn/             # 中文资源
```

## 核心模块

### ErrorHandler
提供统一的错误处理机制，包括：
- 异常捕获和记录
- 错误上下文管理
- 安全执行包装器

### ThreadManager
管理应用程序中的线程，包括：
- 线程创建和启动
- 线程状态监控
- 线程安全清理

### InteractionHelper
处理用户交互，包括：
- 用户输入获取
- 确认对话框
- 键盘输入处理

### NetworkManager
处理网络相关功能，包括：
- IP扫描
- 网络连接测试
- 数据包发送

### SystemManager
处理系统相关功能，包括：
- 进程管理
- 系统信息收集
- 权限检查

### UIManager
处理用户界面相关功能，包括：
- 菜单显示
- 消息展示
- 界面状态管理

## 使用方法

### 环境要求
- Python 3.6+
- Windows操作系统
- 管理员权限（推荐）

### 安装运行
1. 克隆或下载项目
2. 确保所有依赖模块已安装
3. 以管理员权限运行：
   ```
   python main.py
   ```
   或
   ```
   python CommandUI.py
   ```

### 基本操作
1. 启动程序后，使用方向键导航菜单
2. 按Enter键选择菜单项
3. 按Esc键返回上级菜单或退出
4. 按Ctrl+C强制退出程序

## 开发指南

### 代码结构
项目采用模块化设计，各模块职责明确：
- `main.py` - 程序入口，负责初始化和启动
- `CommandUI.py` - 命令行界面实现
- `packages/utils/` - 核心功能模块

### 错误处理
所有模块使用统一的错误处理机制：
```python
from packages.utils.ErrorHandler import error_handler

def my_function():
    def _internal():
        # 可能出错的操作
        pass
    
    error_handler.safe_execute(_internal, context="My function", 
                              default=lambda: print("Error occurred"))
```

### 线程管理
使用ThreadManager管理线程：
```python
from packages.utils.ThreadManager import thread_manager

# 启动线程
thread_id = thread_manager.start_thread(target=my_function, name="MyThread")

# 获取线程状态
thread_status = thread_manager.get_thread_status(thread_id)

# 停止线程
thread_manager.stop_thread(thread_id)
```

### 用户交互
使用InteractionHelper处理用户输入：
```python
from packages.utils.InteractionHelper import interaction_helper

# 获取用户输入
user_input = interaction_helper.get_user_input("Enter value: ", default="default")

# 确认操作
confirmed = interaction_helper.confirm_action("Are you sure?")

# 等待按键
interaction_helper.wait_for_keypress("Press Enter to continue...")
```

## 更新日志

### v1.0.0
- 初始版本发布
- 实现基本网络和系统管理功能
- 添加统一错误处理机制
- 实现模块化架构设计

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件至项目维护者

## 免责声明

本工具仅用于合法的教育环境中的计算机教室管理。使用者需确保遵守当地法律法规和学校政策，不得用于非法用途。开发者不承担因误用本工具而产生的任何法律责任。