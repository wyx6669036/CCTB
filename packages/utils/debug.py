from packages.UtilsManager import Log

def debug(message, level="info"):
    if level == "info":
        Log.info(message)
    elif level == "warn":
        Log.warn(message)
    elif level == "error":
        Log.error(message)