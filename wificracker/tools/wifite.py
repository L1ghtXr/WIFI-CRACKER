from typing import List, Optional

from ..utils import ToolError, run_quiet, which


def launch(iface: str, extra: Optional[List[str]] = None) -> None:
    if which("wifite") is None:
        raise ToolError("wifite not installed")
    cmd = ["wifite", "-i", iface]
    if extra:
        cmd.extend(extra)
    run_quiet(cmd)
