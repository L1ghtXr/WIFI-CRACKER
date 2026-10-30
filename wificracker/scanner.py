import tempfile
from pathlib import Path
from typing import List

from .utils import Network, ToolError, run, run_quiet


def set_channel(iface: str, channel: int) -> None:
    run_quiet(["iw", "dev", iface, "set", "channel", str(channel)])


def scan(iface: str, duration: int = 20) -> List[Network]:
    with tempfile.TemporaryDirectory() as tmp:
        prefix = Path(tmp) / "scan"
        run([
            "timeout", str(duration),
            "airodump-ng",
            "--write-interval", "1",
            "--output-format", "csv,pcap",
            "-w", str(prefix),
            iface,
        ])
        candidates = sorted(Path(tmp).glob("scan-*.csv"))
        if not candidates:
            raise ToolError("airodump-ng produced no csv output")
        return _parse_csv(candidates[0])


def _parse_csv(path: Path) -> List[Network]:
    out: List[Network] = []
    try:
        text = path.read_text(errors="ignore")
    except OSError:
        return out

    in_ap_block = True
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            in_ap_block = False
            continue
        if not in_ap_block:
            break
        if line.startswith("BSSID"):
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 14:
            continue
        try:
            ch = int(parts[3])
            rssi = int(parts[8])
            beacons = int(parts[9]) if parts[9] else 0
        except ValueError:
            continue
        privacy = parts[5]
        if "WPA" not in privacy.upper() and "WEP" not in privacy.upper():
            continue
        out.append(Network(
            bssid=parts[0].upper(),
            channel=ch,
            rssi=rssi,
            privacy=privacy,
            cipher=parts[6],
            auth=parts[7],
            essid=parts[13] or "<hidden>",
            beacons=beacons,
        ))
    out.sort(key=lambda n: n.rssi, reverse=True)
    return out
