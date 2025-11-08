"""
IPscanner.py

叫AI生成的没什么好说，可单独使用（移除对utils的依赖）
用法：
import packages.UtilsManager as utils
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
import packages.UtilsManager as utils


def get_local_ip() -> str:
    """通过 UDP 套接字发现主机对外使用的本地 IPv4 地址，不发送任何数据。"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 连接到一个公共地址（不真正发送数据）以获取本地出口地址
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        # 退回到主机名解析（可能返回 127.0.0.1）
        ip = socket.gethostbyname(socket.gethostname())
    finally:
        s.close()
    return ip


def generate_ips_from_cidr(cidr: str) -> List[str]:
    net = ipaddress.ip_network(cidr, strict=False)
    return [str(ip) for ip in net.hosts()]


def ping_host(ip: str, timeout_ms: int = 500) -> Tuple[str, bool, float]:
    """Ping 指定 IP，返回 (ip, is_alive, rtt_ms).
    在 Windows 上使用 `ping -n 1 -w timeout`。
    timeout_ms 的单位是毫秒。
    如果无法测量 RTT，则返回 rtt_ms = -1.
    """
    system = platform.system()
    if system == "Windows":
        # -n 1: 发送 1 次, -w timeout(ms)
        cmd = ["ping", "-n", "1", "-w", str(int(timeout_ms)), ip]
    else:
        # 假设类 Unix: -c 1 (count), -W timeout(s) or -w
        # 使用 timeout 秒（向上取整）
        timeout_s = max(1, int((timeout_ms + 999) // 1000))
        cmd = ["ping", "-c", "1", "-W", str(timeout_s), ip]

    start = datetime.utcnow()
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        elapsed = (datetime.utcnow() - start).total_seconds() * 1000.0
        alive = res.returncode == 0
    except Exception:
        elapsed = -1
        alive = False
    return ip, alive, elapsed if alive else -1


def scan_ips(ips: Iterable[str], workers: int = 200, timeout_ms: int = 500) -> List[Tuple[str, float]]:
    """并发扫描 IP 列表，返回存活主机的 (ip, rtt_ms) 列表，按照 IP 排序。"""
    results: List[Tuple[str, float]] = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(ping_host, ip, timeout_ms): ip for ip in ips}
        for fut in as_completed(futures):
            ip = futures[fut]
            try:
                ip, alive, rtt = fut.result()
                if alive:
                    results.append((ip, rtt))
            except Exception:
                # 忽略单个任务错误
                pass
    results.sort(key=lambda x: tuple(int(p) for p in x[0].split('.')))
    return results


def main():
    p = argparse.ArgumentParser(description="简单高效的局域网 IP 扫描工具（Windows 首选 ping）。")
    p.add_argument("--cidr", dest="cidr", help="要扫描的 CIDR（例如 192.168.1.0/24）。如果未提供且未使用 --test，则默认为自动检测的本机 /24。")
    p.add_argument("--workers", type=int, default=200, help="并发线程数（默认200）。")
    p.add_argument("--timeout", type=int, default=500, help="ping 超时（毫秒），默认 500ms）。")
    p.add_argument("--test", action="store_true", help="快速自检：自动检测本机 IP 并在 /30 小网段扫描以验证脚本工作。")
    args = p.parse_args()

    if args.test:
        local_ip = get_local_ip()
        # 选择一个 /30 来做非常快速的自检（包含 2 个可用地址）
        # 将 local_ip 转为网络地址的 base，如 192.168.1.5 -> 192.168.1.4/30
        base = ipaddress.ip_network(local_ip + "/30", strict=False).network_address
        cidr = str(ipaddress.ip_network(f"{base}/30", strict=False))
        utils.info(f"[test] Detected local IP {local_ip}, testing on {cidr}")
    else:
        if args.cidr:
            cidr = args.cidr
        else:
            # 自动检测并假设 /24
            local_ip = get_local_ip()
            prefix = 24
            cidr = f"{local_ip}/{prefix}"
            utils.info(f"Auto-detected IP {local_ip}, defaulting to {cidr}")

    try:
        ips = generate_ips_from_cidr(cidr)
    except Exception as e:
        utils.error(f"Invalid CIDR '{cidr}': {e}")
        return

    utils.info(f"Scanning {len(ips)} addresses from {cidr} with {args.workers} workers, timeout={args.timeout}ms...")
    start = datetime.utcnow()
    alive = scan_ips(ips, workers=args.workers, timeout_ms=args.timeout)
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
        return alive


if __name__ == '__main__':
    main()

