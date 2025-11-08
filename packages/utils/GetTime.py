import datetime

def getdate():
    """获取当前日期

    Returns:
        str: 格式为 YYYY-MM-DD 的日期字符串
    """
    today = datetime.date.today()
    return today.strftime("%Y-%m-%d")

def gettime():
    """获取当前时间

    Returns:
        str: 格式为 HH:MM:SS 的时间字符串
    """
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")
