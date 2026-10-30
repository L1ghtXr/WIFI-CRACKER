from ..utils import ToolError, run_quiet, which


def launch(iface: str) -> None:
    if which("bettercap") is None:
        raise ToolError("bettercap not installed (apt install bettercap)")
    run_quiet(["bettercap", "-iface", iface])


def run_caplet(iface: str, caplet_path: str) -> None:
    if which("bettercap") is None:
        raise ToolError("bettercap not installed")
    run_quiet(["bettercap", "-iface", iface, "-caplet", caplet_path])


def evaluate(iface: str, commands: str) -> None:
    if which("bettercap") is None:
        raise ToolError("bettercap not installed")
    run_quiet(["bettercap", "-iface", iface, "-eval", commands])
