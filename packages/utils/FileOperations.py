"""
文件操作模块
提供文件操作相关的工具函数
"""

import os
import shutil
from typing import Union, TextIO, BinaryIO, Any


def openFile(filename: Union[str, bytes, os.PathLike], mode: str = 'r', **kwargs) -> Union[TextIO, BinaryIO]:
    """
    打开文件
    
    Args:
        filename: 文件名
        mode: 打开模式
        **kwargs: 其他传递给open()的参数
        
    Returns:
        文件对象
    """
    return open(filename, mode, **kwargs)


def readFile(filename: Union[str, bytes, os.PathLike], encoding: str = 'utf-8') -> str:
    """
    读取文件内容
    
    Args:
        filename: 文件名
        encoding: 文件编码
        
    Returns:
        str: 文件内容
    """
    with open(filename, 'r', encoding=encoding) as f:
        return f.read()


def writeFile(filename: Union[str, bytes, os.PathLike], content: str, encoding: str = 'utf-8') -> None:
    """
    写入文件内容
    
    Args:
        filename: 文件名
        content: 文件内容
        encoding: 文件编码
    """
    with open(filename, 'w', encoding=encoding) as f:
        f.write(content)


def appendFile(filename: Union[str, bytes, os.PathLike], content: str, encoding: str = 'utf-8') -> None:
    """
    追加文件内容
    
    Args:
        filename: 文件名
        content: 要追加的内容
        encoding: 文件编码
    """
    with open(filename, 'a', encoding=encoding) as f:
        f.write(content)


def copyFile(src: Union[str, bytes, os.PathLike], dst: Union[str, bytes, os.PathLike]) -> None:
    """
    复制文件
    
    Args:
        src: 源文件路径
        dst: 目标文件路径
    """
    shutil.copy2(src, dst)


def moveFile(src: Union[str, bytes, os.PathLike], dst: Union[str, bytes, os.PathLike]) -> None:
    """
    移动文件
    
    Args:
        src: 源文件路径
        dst: 目标文件路径
    """
    shutil.move(src, dst)


def deleteFile(filename: Union[str, bytes, os.PathLike]) -> None:
    """
    删除文件
    
    Args:
        filename: 文件名
    """
    os.remove(filename)


def createDir(dirname: Union[str, bytes, os.PathLike]) -> None:
    """
    创建目录
    
    Args:
        dirname: 目录名
    """
    os.makedirs(dirname, exist_ok=True)


def deleteDir(dirname: Union[str, bytes, os.PathLike]) -> None:
    """
    删除目录及其内容
    
    Args:
        dirname: 目录名
    """
    shutil.rmtree(dirname)


def listDir(dirname: Union[str, bytes, os.PathLike]) -> list:
    """
    列出目录内容
    
    Args:
        dirname: 目录名
        
    Returns:
        list: 目录内容列表
    """
    return os.listdir(dirname)


def fileSize(filename: Union[str, bytes, os.PathLike]) -> int:
    """
    获取文件大小
    
    Args:
        filename: 文件名
        
    Returns:
        int: 文件大小（字节）
    """
    return os.path.getsize(filename)


def fileExists(filename: Union[str, bytes, os.PathLike]) -> bool:
    """
    检查文件是否存在
    
    Args:
        filename: 文件名
        
    Returns:
        bool: 文件存在返回True，否则返回False
    """
    return os.path.isfile(filename)


def dirExists(dirname: Union[str, bytes, os.PathLike]) -> bool:
    """
    检查目录是否存在
    
    Args:
        dirname: 目录名
        
    Returns:
        bool: 目录存在返回True，否则返回False
    """
    return os.path.isdir(dirname)