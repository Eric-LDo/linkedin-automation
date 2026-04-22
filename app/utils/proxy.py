import os
import random
from pathlib import Path
from typing import List, Optional


DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DEFAULT_PROXIES_PATH = DATA_DIR / "proxies.py"
DEFAULT_IPS_PATH = DATA_DIR / "ips.py"


def load_proxies(file_path: Optional[str] = None) -> List[str]:
    path = Path(file_path) if file_path else DEFAULT_PROXIES_PATH
    if not path.exists():
        return []
    namespace = {}
    exec(path.read_text(encoding="utf-8"), {}, namespace)
    proxies = namespace.get("proxies", [])
    return [p for p in proxies if isinstance(p, str)]


def pick_proxy(proxies: List[str]) -> Optional[str]:
    if not proxies:
        return None
    return random.choice(proxies)


def load_ips(file_path: Optional[str] = None) -> List[str]:
    path = Path(file_path) if file_path else DEFAULT_IPS_PATH
    if not path.exists():
        return []
    namespace = {}
    exec(path.read_text(encoding="utf-8"), {}, namespace)
    ips = namespace.get("ips", [])
    return [ip for ip in ips if isinstance(ip, str)]


def pick_ip(ips: List[str]) -> Optional[str]:
    if not ips:
        return None
    return random.choice(ips)


def get_random_proxy() -> Optional[str]:
    proxies = load_proxies()
    proxy = pick_proxy(proxies)
    if proxy:
        return proxy
    ips = load_ips()
    ip = pick_ip(ips)
    if not ip:
        return None
    port = os.getenv("PROXY_PORT", "9050")
    return f"socks5h://{ip}:{port}"
