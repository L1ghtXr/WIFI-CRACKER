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


def _popen_args(cmd: List[str], capture: bool) -> dict:
    return dict(
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
        stderr=subprocess.STDOUT if capture else subprocess.DEVNULL,
        text=True,
    )


def run(cmd: List[str], check: bool = False) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, check=check, **_popen_args(cmd, capture=True))
    except FileNotFoundError as e:
        raise ToolError(str(e)) from e


def run_quiet(cmd: List[str]) -> None:
    try:
        subprocess.run(cmd, check=False, **_popen_args(cmd, capture=False))
    except FileNotFoundError as e:
        raise ToolError(str(e)) from e


def tool_version(binary: str) -> str:
    """Best-effort version string — tries --version, then -h, then -V."""
    if which(binary) is None:
        return ""
    for flag in ("--version", "-V", "-h"):
        try:
            r = subprocess.run(
                [binary, flag],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=5,
            )
        except (subprocess.TimeoutExpired, OSError):
            continue
        out = (r.stdout or "").strip().splitlines()
        if out:
            return out[0]
    return ""


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
