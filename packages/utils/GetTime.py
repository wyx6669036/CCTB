"""
时间获取模块
提供获取当前日期和时间的功能
"""

import datetime


def getdate():
    """
    获取当前日期

    返回:
        str: 格式为 YYYY-MM-DD 的日期字符串
    """
    try:
        today = datetime.date.today()
        return today.strftime("%Y-%m-%d")
    except Exception as e:
        return "1900-01-01"  # 返回默认日期以避免程序崩溃


def gettime():
    """
    获取当前时间

    返回:
        str: 格式为 HH:MM:SS 的时间字符串
    """
    try:
        now = datetime.datetime.now()
        return now.strftime("%H:%M:%S")
    except Exception as e:
        return "00:00:00"  # 返回默认时间以避免程序崩溃
