from pathlib import Path
from typing import Optional, Union

from ..utils import ToolError, run


def convert_to_hashcat(pcap: Union[Path, str], out: Optional[Union[Path, str]] = None) -> Path:
    p = Path(pcap)
    if not p.exists():
        raise ToolError(f"pcap not found: {p}")
    out_path = Path(out) if out else p.with_suffix(".hc22000")
    run(["hcxpcapngtool", "-o", str(out_path), str(p)])
    if not out_path.exists() or out_path.stat().st_size == 0:
        raise ToolError("no PMKID/handshake in pcapng — nothing to convert")
    return out_path


def inspect(hashfile: Union[Path, str]) -> str:
    h = Path(hashfile)
    if not h.exists():
        raise ToolError(f"hash file not found: {h}")
    return run(["hcxhashtool", "-i", str(h), "--info=stdout"]).stdout or ""


def pmkid_to_hashcat(pcapng: Union[Path, str]) -> Path:
    return convert_to_hashcat(pcapng)
