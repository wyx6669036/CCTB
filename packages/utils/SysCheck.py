import platform


def sysCheck():
    system = platform.system()

    if system == 'Windows':
        return {"name": "windows", "version": platform.release()}
    elif system == 'Linux':
        return {"name": "linux", "version": platform.release()}
    elif system == 'Darwin':
        return {"name": "macos", "version": platform.release()}
    else:
        raise ValueError(f"Unsupported system: {system}")
