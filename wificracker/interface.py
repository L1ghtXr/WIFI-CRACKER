import subprocess
from contextlib import contextmanager
from typing import Iterator, List, Optional

from .utils import ToolError, require_root, run, run_quiet, which


def list_interfaces() -> List[str]:
    if which("iw"):
        out = run(["iw", "dev"]).stdout or ""
        return [ln.split()[-1] for ln in out.splitlines() if "Interface" in ln]
    out = run(["iwconfig"]).stdout or ""
    return [ln.split()[0] for ln in out.splitlines() if ln and not ln.startswith(" ")]


def is_monitor(iface: str) -> bool:
    if which("iw"):
        out = run(["iw", "dev", iface, "info"]).stdout or ""
        return "type monitor" in out
    out = run(["iwconfig", iface]).stdout or ""
    return "Mode:Monitor" in out


def _nmcli_alive() -> bool:
    try:
        r = subprocess.run(["nmcli", "general"], capture_output=True, timeout=2)
        return r.returncode == 0
    except Exception:
        return False


def _set_type(iface: str, mode: str) -> None:
    run_quiet(["ip", "link", "set", iface, "down"])
    if which("iw"):
        run_quiet(["iw", iface, "set", "type", mode])
    else:
        run_quiet(["iwconfig", iface, "mode", mode])
    run_quiet(["ip", "link", "set", iface, "up"])


def _pick_monitor_child(base: str) -> Optional[str]:
    for candidate in (f"{base}mon", f"{base}mon0"):
        if candidate in list_interfaces() and is_monitor(candidate):
            return candidate
    for iface in list_interfaces():
        if iface.startswith(base) and iface != base and is_monitor(iface):
            return iface
    return None


@contextmanager
def monitor_mode(iface: str) -> Iterator[str]:
    require_root()
    if iface not in list_interfaces():
        raise ToolError(f"interface not found: {iface}")

    if is_monitor(iface):
        yield iface
        return

    original = iface
    nm_was_up = _nmcli_alive()

    try:
        run_quiet(["rfkill", "unblock", "wifi"])
        if which("airmon-ng"):
            run_quiet(["airmon-ng", "check", "kill"])
            run_quiet(["airmon-ng", "start", iface])
            child = _pick_monitor_child(iface)
            if child and is_monitor(child):
                yield child
                return
        _set_type(original, "monitor")
        if not is_monitor(original):
            raise ToolError(f"failed to place {original} in monitor mode")
        yield original
    finally:
        try:
            if is_monitor(original):
                _set_type(original, "managed")
        except Exception:
            pass
        if nm_was_up:
            run_quiet(["systemctl", "restart", "NetworkManager"])
