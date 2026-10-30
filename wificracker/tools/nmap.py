from ..utils import run


def host_discovery(subnet: str) -> str:
    return run(["nmap", "-sn", "-T4", subnet]).stdout or ""


def service_scan(target: str) -> str:
    return run(["nmap", "-sV", "-T4", target]).stdout or ""


def full_scan(target: str) -> str:
    return run(["nmap", "-A", "-T4", target]).stdout or ""
