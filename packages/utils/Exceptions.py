"""
自定义异常模块
定义应用程序特定的异常类，提供更精确的错误处理
"""


class CCTBException(Exception):
    """CCTB应用程序基础异常类"""
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code
        self.message = message


class NetworkException(CCTBException):
    """网络相关异常"""
    def __init__(self, message, target_ip=None, target_port=None):
        super().__init__(message)
        self.target_ip = target_ip
        self.target_port = target_port


class SystemException(CCTBException):
    """系统相关异常"""
    def __init__(self, message, system_component=None):
        super().__init__(message)
        self.system_component = system_component


class PermissionException(CCTBException):
    """权限相关异常"""
    pass


class ValidationException(CCTBException):
    """数据验证异常"""
    def __init__(self, message, field_name=None, field_value=None):
        super().__init__(message)
        self.field_name = field_name
        self.field_value = field_value


class ProcessException(CCTBException):
    """进程操作相关异常"""
    def __init__(self, message, process_name=None, pid=None):
        super().__init__(message)
        self.process_name = process_name
        self.pid = pid