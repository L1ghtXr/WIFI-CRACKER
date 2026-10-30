import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from typing import List, Optional


class ToolError(RuntimeError):
    pass


def require_root() -> None:
    if os.geteuid() != 0:
        raise ToolError("must run as root (monitor mode + injection + raw sockets need it)")


def which(name: str) -> Optional[str]:
    return shutil.which(name)


def require_binary(*names: str) -> None:
    missing = [n for n in names if which(n) is None]
    if missing:
        raise ToolError(f"missing binaries: {', '.join(missing)}")


def run(cmd: List[str], check: bool = False) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, check=check, capture_output=True, text=True)
    except FileNotFoundError as e:
        raise ToolError(str(e)) from e


def run_quiet(cmd: List[str]) -> None:
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)


@dataclass
class Network:
    bssid: str
    channel: int
    rssi: int
    privacy: str
    cipher: str
    auth: str
    essid: str
    beacons: int = 0


_BSSID_RE = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")


def is_bssid(value: str) -> bool:
    return bool(_BSSID_RE.match(value))


def parse_handshake_count(aircrack_output: str) -> int:
    m = re.search(r"(\d+)\s+handshake", aircrack_output, re.IGNORECASE)
    return int(m.group(1)) if m else 0
