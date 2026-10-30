import re
from pathlib import Path
from typing import Optional

from .utils import ToolError, run


_KEY_RE = re.compile(r"KEY FOUND!\s*\[\s*(.+?)\s*\]", re.IGNORECASE)


def crack_handshake(pcap: Path, wordlist: Path, bssid: Optional[str] = None) -> Optional[str]:
    if not pcap.exists():
        raise ToolError(f"pcap not found: {pcap}")
    if not wordlist.exists():
        raise ToolError(f"wordlist not found: {wordlist}")
    cmd = ["aircrack-ng", "-w", str(wordlist), "-q"]
    if bssid:
        cmd += ["-b", bssid]
    cmd.append(str(pcap))
    out = run(cmd).stdout or ""
    m = _KEY_RE.search(out)
    return m.group(1) if m else None
