from ..utils import ToolError, run_quiet, which


def launch(iface: str) -> None:
    if which("kismet") is None:
        raise ToolError("kismet not installed")
    print(" kismet ui -> http://localhost:2501  (ctrl+c to stop)")
    run_quiet(["kismet", "-c", iface])
