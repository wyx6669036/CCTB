"""
路径检查模块
提供路径操作相关的工具函数
"""

import os
from typing import Union


def pathExists(path: Union[str, bytes, os.PathLike]) -> bool:
    """
    检查路径是否存在
    
    Args:
        path: 要检查的路径
        
    Returns:
        bool: 路径存在返回True，否则返回False
    """
    return os.path.exists(path)


def isFile(path: Union[str, bytes, os.PathLike]) -> bool:
    """
    检查路径是否为文件
    
    Args:
        path: 要检查的路径
        
    Returns:
        bool: 是文件返回True，否则返回False
    """
    return os.path.isfile(path)


def isDir(path: Union[str, bytes, os.PathLike]) -> bool:
    """
    检查路径是否为目录
    
    Args:
        path: 要检查的路径
        
    Returns:
        bool: 是目录返回True，否则返回False
    """
    return os.path.isdir(path)


def isAbs(path: Union[str, bytes, os.PathLike]) -> bool:
    """
    检查路径是否为绝对路径
    
    Args:
        path: 要检查的路径
        
    Returns:
        bool: 是绝对路径返回True，否则返回False
    """
    return os.path.isabs(path)


def joinPath(*paths) -> str:
    """
    连接多个路径部分
    
    Args:
        *paths: 要连接的路径部分
        
    Returns:
        str: 连接后的路径
    """
    return os.path.join(*paths)


def getDirName(path: Union[str, bytes, os.PathLike]) -> str:
    """
    获取路径的目录部分
    
    Args:
        path: 要处理的路径
        
    Returns:
        str: 目录部分
    """
    return os.path.dirname(path)


def getBaseName(path: Union[str, bytes, os.PathLike]) -> str:
    """
    获取路径的基本名称部分
    
    Args:
        path: 要处理的路径
        
    Returns:
        str: 基本名称部分
    """
    return os.path.basename(path)


def splitPath(path: Union[str, bytes, os.PathLike]) -> tuple:
    """
    分割路径为目录和基本名称
    
    Args:
        path: 要分割的路径
        
    Returns:
        tuple: (目录部分, 基本名称部分)
    """
    return os.path.split(path)


def splitExt(path: Union[str, bytes, os.PathLike]) -> tuple:
    """
    分割路径的扩展名
    
    Args:
        path: 要分割的路径
        
    Returns:
        tuple: (路径部分, 扩展名部分)
    """
    return os.path.splitext(path)


def normalizePath(path: Union[str, bytes, os.PathLike]) -> str:
    """
    规范化路径
    
    Args:
        path: 要规范化的路径
        
    Returns:
        str: 规范化后的路径
    """
    return os.path.normpath(path)


def absPath(path: Union[str, bytes, os.PathLike]) -> str:
    """
    获取绝对路径
    
    Args:
        path: 要转换的路径
        
    Returns:
        str: 绝对路径
    """
    return os.path.abspath(path)