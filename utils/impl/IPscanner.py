"""
局域网IP扫描模块
用于快速并发扫描局域网中的活跃主机
IPscanner.py

叫AI生成的没什么好说，可单独使用（移除对utils的依赖）
用法：
import utils.implManager as utils
utils.ip_scanner()

返回值(eg.)：[("192.168.153.1",200)]
若ping被禁用可能无法正常运行，依赖他的功能可能需要手动输入ip地址

快速的并发局域网主机探测器（Windows 优先使用 ping）。
用法示例：
  python IPscanner.py --cidr 192.168.1.0/24
  python IPscanner.py --test            # 自动检测本机 IP 并在 /30 小网段做快速自检

实现说明：
- 自动检测本机 IPv4 地址（通过 UDP 套接字连接到公网上的地址）
- 默认假设 /24（当使用 --auto 或未指定时），但提供 --cidr 覆盖
- 使用 subprocess 调用系统 ping（Windows: -n, -w）以避免需要管理员权限
- 使用 ThreadPoolExecutor 并发执行 ping
"""

from __future__ import annotations
import argparse
import ipaddress
import platform
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Iterable, List, Tuple
import utils.implManager as utils
from utils.impl.ErrorHandler import handle_exception, NetworkError, SystemError


@handle_exception(NetworkError, default_return="127.0.0.1", error_message="Failed to get local IP address")
def get_local_ip() -> str:
    """
    通过UDP套接字发现主机对外使用的本地IPv4地址，不发送任何数据
    
    Returns:
        str: 本地IP地址
        
    Raises:
        NetworkError: 当获取本地IP失败时抛出
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 连接到一个公共地址（不真正发送数据）以获取本地出口地址
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception as e:
        # 退回到主机名解析（可能返回127.0.0.1）
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except Exception as inner_e:
            raise NetworkError(f"Failed to get local IP: {e}, {inner_e}")
    finally:
        s.close()
    return ip


@handle_exception(NetworkError, default_return=[], error_message="Failed to generate IPs from CIDR")
def generate_ips_from_cidr(cidr: str) -> List[str]:
    """
    从CIDR表示法生成IP地址列表
    
    Args:
        cidr: CIDR格式的网络地址，如"192.168.1.0/24"
        
    Returns:
        List[str]: IP地址列表
        
    Raises:
        NetworkError: 当CIDR格式无效时抛出
    """
    try:
        net = ipaddress.ip_network(cidr, strict=False)
        return [str(ip) for ip in net.hosts()]
    except Exception as e:
        raise NetworkError(f"Invalid CIDR '{cidr}': {e}")


@handle_exception(NetworkError, default_return=("127.0.0.1", False, -1), error_message="Failed to ping host")
def ping_host(ip: str, timeout_ms: int = 500) -> Tuple[str, bool, float]:
    """
    Ping指定IP地址
    
    Args:
        ip: 要ping的IP地址
        timeout_ms: 超时时间（毫秒）
        
    Returns:
        Tuple[str, bool, float]: (ip, 是否存活, 延迟毫秒)
        
    Raises:
        NetworkError: 当ping操作失败时抛出
    """
    system = platform.system()
    if system == "Windows":
        # -n 1: 发送1次, -w timeout(ms)
        cmd = ["ping", "-n", "1", "-w", str(int(timeout_ms)), ip]
    else:
        # 假设类Unix: -c 1 (count), -W timeout(s) or -w
        # 使用timeout秒（向上取整）
        timeout_s = max(1, int((timeout_ms + 999) // 1000))
        cmd = ["ping", "-c", "1", "-W", str(timeout_s), ip]

    start = datetime.utcnow()
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        elapsed = (datetime.utcnow() - start).total_seconds() * 1000.0
        alive = res.returncode == 0
    except Exception as e:
        raise NetworkError(f"Failed to ping {ip}: {e}")
    return ip, alive, elapsed if alive else -1


@handle_exception(NetworkError, default_return=[], error_message="Failed to scan IPs")
def scan_ips(ips: Iterable[str], workers: int = 200, timeout_ms: int = 500) -> List[Tuple[str, float]]:
    """
    并发扫描IP列表
    
    Args:
        ips: 要扫描的IP地址列表
        workers: 并发线程数
        timeout_ms: ping超时时间（毫秒）
        
    Returns:
        List[Tuple[str, float]]: 存活主机的(IP, 延迟毫秒)列表，按IP排序
        
    Raises:
        NetworkError: 当扫描过程中发生错误时抛出
    """
    results: List[Tuple[str, float]] = []
    # 限制最大线程数以避免资源耗尽
    max_workers = min(workers, 500)
    
    try:
        # 检查解释器是否正在关闭
        import sys
        if hasattr(sys, 'is_finalizing') and sys.is_finalizing():
            utils.warn("System is shutting down, skipping IP scan")
            return []
            
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            # 使用生成器表达式而不是列表推导式，减少内存使用
            future_to_ip = {ex.submit(ping_host, ip, timeout_ms): ip for ip in ips}
            for fut in as_completed(future_to_ip):
                # 再次检查解释器是否正在关闭
                if hasattr(sys, 'is_finalizing') and sys.is_finalizing():
                    utils.warn("System is shutting down, cancelling remaining IP scans")
                    break
                    
                ip = future_to_ip[fut]
                try:
                    ip, alive, rtt = fut.result()
                    if alive:
                        results.append((ip, rtt))
                except Exception as e:
                    # 忽略单个任务错误，但记录日志
                    utils.warn(f"Error scanning {ip}: {e}")
    except RuntimeError as e:
        if "cannot schedule new futures after interpreter shutdown" in str(e):
            utils.warn("System is shutting down, IP scan cancelled")
            return []
        raise
    except Exception as e:
        raise NetworkError(f"Failed to scan IPs: {e}")
        
    # 使用更高效的排序方法
    results.sort(key=lambda x: tuple(map(int, x[0].split('.'))))
    return results


@handle_exception(SystemError, default_return=None, error_message="IP scanner failed")
def main():
    """
    主函数，处理命令行参数并执行扫描
    
    支持的参数:
    --cidr: 要扫描的CIDR网络
    --workers: 并发线程数
    --timeout: ping超时时间（毫秒）
    --test: 快速自检模式
    
    Raises:
        SystemError: 当扫描过程中发生系统级错误时抛出
    """
    p = argparse.ArgumentParser(description="简单高效的局域网IP扫描工具（Windows首选ping）。")
    p.add_argument("--cidr", dest="cidr", help="要扫描的CIDR（例如192.168.1.0/24）。如果未提供且未使用--test，则默认为自动检测的本机/24。")
    p.add_argument("--workers", type=int, default=200, help="并发线程数（默认200）。")
    p.add_argument("--timeout", type=int, default=500, help="ping超时（毫秒），默认500ms）。")
    p.add_argument("--test", action="store_true", help="快速自检：自动检测本机IP并在/30小网段扫描以验证脚本工作。")
    
    try:
        args = p.parse_args()
    except Exception as e:
        raise SystemError(f"Failed to parse arguments: {e}")

    try:
        if args.test:
            local_ip = get_local_ip()
            # 选择一个/30来做非常快速的自检（包含2个可用地址）
            # 将local_ip转为网络地址的base，如192.168.1.5 -> 192.168.1.4/30
            base = ipaddress.ip_network(local_ip + "/30", strict=False).network_address
            cidr = str(ipaddress.ip_network(f"{base}/30", strict=False))
            utils.info(f"[test] Detected local IP {local_ip}, testing on {cidr}")
        else:
            if args.cidr:
                cidr = args.cidr
            else:
                # 自动检测并假设/24
                local_ip = get_local_ip()
                prefix = 24
                cidr = f"{local_ip}/{prefix}"
                utils.info(f"Auto-detected IP {local_ip}, defaulting to {cidr}")

        ips = generate_ips_from_cidr(cidr)
    except Exception as e:
        raise SystemError(f"Failed to prepare scan: {e}")

    utils.info(f"Scanning {len(ips)} addresses from {cidr} with {args.workers} workers, timeout={args.timeout}ms...")
    start = datetime.utcnow()
    
    try:
        alive = scan_ips(ips, workers=args.workers, timeout_ms=args.timeout)
    except Exception as e:
        raise SystemError(f"Scan failed: {e}")
        
    elapsed = (datetime.utcnow() - start).total_seconds()

    utils.info(f"Scan finished in {elapsed:.2f}s. Hosts up: {len(alive)}")
    if alive:
        utils.info("Live hosts:")
        for ip, rtt in alive:
            try:
                name = socket.gethostbyaddr(ip)[0]
            except Exception:
                name = ""
            utils.info(f"  {ip}\t{rtt:.0f}ms\t{name}")

        utils.info(str(alive))
    
    # 总是返回alive列表，即使为空
    return alive


if __name__ == '__main__':
    main()

