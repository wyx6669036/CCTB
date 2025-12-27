# CCTB 开发指南

本文档为CCTB项目的开发者提供详细的开发指南和规范。

## 开发环境设置

### 系统要求

- Windows 10/11
- Python 3.8+
- 管理员权限（部分功能需要）

### 克隆项目

```bash
git clone <repository-url>
cd CCTB
```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置文件

复制并编辑配置文件：

```bash
cp config/config.json.example config/config.json
```

## 项目结构

```
CCTB/
├── main.py                 # 主程序入口
├── requirements.txt        # 依赖列表
├── README.md              # 项目说明
├── config/                # 配置文件目录
│   ├── config.json        # 主配置文件
│   └── logging.json       # 日志配置
├── packages/              # 核心代码包
│   ├── CommandUI.py       # 命令行界面
│   ├── UtilsManager.py    # 工具管理器
│   └── utils/             # 工具模块
│       ├── ConfigManager.py    # 配置管理
│       ├── ErrorHandler.py     # 错误处理
│       ├── LogManager.py        # 日志管理
│       ├── Performance.py       # 性能监控
│       ├── IPscanner.py         # IP扫描
│       └── fuckMythware.py      # 极域通信
├── tests/                 # 测试文件
│   ├── test_config_manager.py
│   ├── test_error_handler.py
│   ├── test_log_manager.py
│   ├── test_performance.py
│   ├── test_ip_scanner.py
│   └── test_fuck_mythware.py
└── docs/                  # 文档
    ├── API.md            # API文档
    ├── DEVELOPMENT.md    # 开发指南
    └── CHANGELOG.md      # 更新日志
```

## 代码规范

### 命名规范

- 类名：使用PascalCase（大驼峰命名法），如 `ConfigManager`
- 函数和变量名：使用snake_case（下划线命名法），如 `get_local_ip`
- 常量：使用全大写字母和下划线，如 `MAX_WORKERS`
- 私有成员：以单下划线开头，如 `_private_method`

### 文档字符串

所有公共函数和类都应有详细的文档字符串，使用以下格式：

```python
def function_name(param1, param2):
    """
    函数功能的简短描述。
    
    详细描述（可选）。
    
    Args:
        param1 (type): 参数1的描述
        param2 (type): 参数2的描述
    
    Returns:
        type: 返回值的描述
    
    Raises:
        ExceptionType: 异常的描述
    
    Example:
        >>> result = function_name("value1", "value2")
        >>> print(result)
        expected_output
    """
    # 函数实现
```

### 类型提示

使用类型提示提高代码可读性和可维护性：

```python
from typing import List, Dict, Optional, Union, Tuple, Callable

def process_data(
    data: List[Dict[str, Union[str, int]]],
    filter_func: Optional[Callable[[Dict[str, Union[str, int]]], bool]] = None
) -> Tuple[List[Dict[str, Union[str, int]]], int]:
    """
    处理数据列表。
    
    Args:
        data: 要处理的数据列表
        filter_func: 可选的过滤函数
    
    Returns:
        包含处理后的数据列表和处理数量的元组
    """
    # 函数实现
```

### 异常处理

使用自定义异常类和装饰器进行错误处理：

```python
from utils.impl.ErrorHandler import handle_exception, CCTBException

class CustomError(CCTBException):
    """自定义异常类。"""
    pass

@handle_exception(CustomError, default_return=None, error_message="操作失败")
def risky_operation(param: str) -> Optional[str]:
    """
    执行可能有风险的操作。
    
    Args:
        param: 操作参数
    
    Returns:
        操作结果，如果失败则返回None
    """
    # 可能抛出CustomError的代码
    return result
```

### 日志记录

使用统一的日志记录器：

```python
from utils.impl.LogManager import log_manager

logger = log_manager.get_logger(__name__)

def some_function():
    logger.info("开始执行函数")
    try:
        # 函数实现
        logger.info("函数执行成功")
    except Exception as e:
        logger.error(f"函数执行失败: {str(e)}")
        raise
```

## 开发流程

### 1. 功能开发

1. 创建功能分支：
   ```bash
   git checkout -b feature/new-feature
   ```

2. 编写代码，遵循代码规范

3. 添加单元测试：
   ```python
   import unittest
   from utils.impl.module import function_to_test
   
   class TestNewFeature(unittest.TestCase):
       def test_function(self):
           result = function_to_test("test_input")
           self.assertEqual(result, "expected_output")
   ```

4. 运行测试：
   ```bash
   python -m pytest tests/test_new_feature.py -v
   ```

5. 提交代码：
   ```bash
   git add .
   git commit -m "feat: 添加新功能"
   ```

### 2. 代码审查

1. 创建拉取请求
2. 等待代码审查
3. 根据反馈修改代码
4. 合并到主分支

### 3. 发布流程

1. 更新版本号
2. 更新CHANGELOG.md
3. 创建发布标签
4. 构建发布包

## 测试指南

### 单元测试

使用Python的unittest框架编写单元测试：

```python
import unittest
from unittest.mock import patch, MagicMock
from utils.impl.module import ClassToTest

class TestClassToTest(unittest.TestCase):
    def setUp(self):
        """测试前的设置。"""
        self.instance = ClassToTest()
    
    def tearDown(self):
        """测试后的清理。"""
        pass
    
    def test_method_success(self):
        """测试方法在正常情况下的行为。"""
        result = self.instance.method("test_input")
        self.assertEqual(result, "expected_output")
    
    def test_method_failure(self):
        """测试方法在异常情况下的行为。"""
        with self.assertRaises(ValueError):
            self.instance.method(None)
    
    @patch('utils.impl.module.external_dependency')
    def test_method_with_mock(self, mock_dependency):
        """测试方法使用模拟对象。"""
        mock_dependency.return_value = "mocked_value"
        result = self.instance.method("test_input")
        self.assertEqual(result, "expected_output_with_mock")
```

### 集成测试

编写集成测试来验证组件之间的交互：

```python
import unittest
from utils.impl.ConfigManager import config
from utils.impl.LogManager import log_manager

class TestConfigLoggingIntegration(unittest.TestCase):
    def test_config_logging_integration(self):
        """测试配置和日志管理器的集成。"""
        # 设置配置
        config.set("log_level", "DEBUG")
        
        # 配置日志系统
        log_manager.configure_from_config(config.get_all())
        
        # 获取日志记录器
        logger = log_manager.get_logger("test")
        
        # 验证日志级别
        self.assertEqual(logger.level, 10)  # DEBUG级别
```

### 性能测试

使用性能监控模块进行性能测试：

```python
import unittest
import time
from utils.impl.Performance import PerformanceMonitor

class TestPerformance(unittest.TestCase):
    def test_performance_monitor(self):
        """测试性能监控功能。"""
        monitor = PerformanceMonitor()
        
        # 开始监控
        monitor.start_monitoring(interval=0.1)
        
        # 执行一些操作
        time.sleep(0.5)
        
        # 获取统计信息
        stats = monitor.get_current_stats()
        
        # 验证统计信息
        self.assertIn("cpu", stats)
        self.assertIn("memory_mb", stats)
        self.assertIn("thread_count", stats)
        
        # 停止监控
        monitor.stop_monitoring()
```

### 运行测试

运行所有测试：
```bash
python -m pytest tests/ -v
```

运行特定测试文件：
```bash
python -m pytest tests/test_config_manager.py -v
```

运行特定测试类：
```bash
python -m pytest tests/test_config_manager.py::TestConfigManager -v
```

运行特定测试方法：
```bash
python -m pytest tests/test_config_manager.py::TestConfigManager::test_get -v
```

## 性能优化指南

### 1. 性能监控

使用性能监控模块识别性能瓶颈：

```python
from utils.impl.Performance import initialize_performance_manager, get_performance_stats

# 初始化性能监控
initialize_performance_manager()

# 获取性能统计
stats = get_performance_stats()
print(f"CPU使用率: {stats['current']['cpu']}%")
print(f"内存使用: {stats['current']['memory_mb']}MB")
```

### 2. 优化技巧

- 使用生成器表达式代替列表推导式，减少内存使用
- 合理使用多线程，避免过度并发
- 缓存重复计算的结果
- 使用更高效的数据结构和算法
- 避免不必要的对象创建和销毁

### 3. 资源管理

- 使用上下文管理器管理资源
- 及时释放不再使用的资源
- 设置合理的超时时间
- 限制并发操作的数量

## 调试指南

### 1. 日志调试

启用详细日志记录：

```python
from utils.impl.LogManager import log_manager

# 创建调试日志记录器
logger = log_manager.create_logger(
    "debug",
    level="DEBUG",
    file_path="debug.log"
)

# 记录调试信息
logger.debug("变量值: %s", variable)
logger.debug("函数调用: %s", function_name)
```

### 2. 异常调试

使用异常处理捕获和记录错误：

```python
from utils.impl.ErrorHandler import handle_exception

@handle_exception(Exception, reraise=True)
def debug_function():
    try:
        # 可能出错的代码
        pass
    except Exception as e:
        # 记录异常详情
        import traceback
        logger.error(f"异常详情: {traceback.format_exc()}")
        raise
```

### 3. 性能调试

使用性能监控识别性能问题：

```python
from utils.impl.Performance import PerformanceMonitor

# 创建性能监控器
monitor = PerformanceMonitor()

# 添加回调函数
def performance_callback(stats):
    if stats['cpu'] > 80:
        logger.warning(f"高CPU使用率: {stats['cpu']}%")
    if stats['memory_mb'] > 500:
        logger.warning(f"高内存使用: {stats['memory_mb']}MB")

monitor.add_callback(performance_callback)

# 开始监控
monitor.start_monitoring(interval=1.0)
```

## 贡献指南

### 1. 提交代码

1. Fork项目
2. 创建功能分支
3. 编写代码和测试
4. 确保所有测试通过
5. 提交Pull Request

### 2. 代码审查

- 代码必须符合项目规范
- 必须有适当的测试覆盖
- 必须有清晰的提交信息
- 必须更新相关文档

### 3. 问题报告

使用GitHub Issues报告问题，包括：

- 问题的详细描述
- 重现步骤
- 期望的行为
- 实际的行为
- 环境信息（操作系统、Python版本等）

## 常见问题

### 1. 权限问题

某些功能需要管理员权限，确保以管理员身份运行程序。

### 2. 网络问题

确保网络连接正常，防火墙设置允许程序访问网络。

### 3. 配置问题

检查配置文件是否正确设置，特别是IP地址和端口配置。

### 4. 依赖问题

确保所有依赖都已正确安装，可以使用以下命令检查：

```bash
pip freeze
```

## 版本控制

使用语义化版本控制（Semantic Versioning）：

- 主版本号：不兼容的API修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正

版本号格式：MAJOR.MINOR.PATCH

示例：1.0.0, 1.1.0, 1.1.1, 2.0.0

## 发布流程

1. 更新版本号
2. 更新CHANGELOG.md
3. 运行完整测试套件
4. 创建发布标签
5. 构建发布包
6. 发布到分发平台

## 资源链接

- [Python官方文档](https://docs.python.org/)
- [unittest文档](https://docs.python.org/3/library/unittest.html)
- [语义化版本控制](https://semver.org/)
- [PEP 8 - Python代码风格指南](https://www.python.org/dev/peps/pep-0008/)