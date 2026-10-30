from pathlib import Path
from typing import Optional, Union

from ..utils import ToolError, run, run_quiet


def live_capture(iface: str, count: int = 100, out: Union[Path, str] = "capture.pcap") -> Path:
    out_path = Path(out)
    run(["tshark", "-i", iface, "-c", str(count), "-w", str(out_path)])
    if not out_path.exists():
        raise ToolError("tshark produced no file")
    return out_path


def analyze(pcap: Union[Path, str], display_filter: Optional[str] = None) -> str:
    p = Path(pcap)
    if not p.exists():
        raise ToolError(f"pcap not found: {p}")
    cmd = ["tshark", "-r", str(p)]
    if display_filter:
        cmd += ["-Y", display_filter]
    return run(cmd).stdout or ""


def open_gui(pcap: Union[Path, str]) -> None:
    p = Path(pcap)
    if not p.exists():
        raise ToolError(f"pcap not found: {p}")
    run_quiet(["wireshark", str(p)])
