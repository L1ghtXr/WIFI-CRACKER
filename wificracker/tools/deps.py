from dataclasses import dataclass
from typing import Callable, Dict, List

from ..utils import which


@dataclass(frozen=True)
class Tool:
    name: str
    check: Callable[[], bool]
    category: str
    purpose: str
    install: str


def _bin(name: str) -> Callable[[], bool]:
    return lambda: which(name) is not None


def _scapy() -> bool:
    try:
        import scapy.all  # noqa: F401
        return True
    except ImportError:
        return False


REGISTRY: List[Tool] = [
    Tool("Aircrack-ng",        _bin("aircrack-ng"),    "Wireless auditing",     "Audit Wi-Fi network security",                            "apt install aircrack-ng"),
    Tool("Wireshark/tshark",   _bin("tshark"),         "Packet analysis",       "Analyze traffic/protocols",                               "apt install tshark"),
    Tool("Kismet",             _bin("kismet"),         "Wireless discovery",    "Monitor & discover Wi-Fi networks/devices",               "apt install kismet"),
    Tool("Nmap",               _bin("nmap"),           "Network scanning",      "Map hosts and services on your own network",              "apt install nmap"),
    Tool("Hashcat",            _bin("hashcat"),        "Password auditing",     "Test password strength from lawfully obtained hashes",    "apt install hashcat"),
    Tool("John the Ripper",    _bin("john"),           "Password auditing",     "Offline password/hash audit",                             "apt install john"),
    Tool("hcxtools",           _bin("hcxpcapngtool"),  "Wi-Fi protocol testing","Analyze Wi-Fi authentication data for security testing",  "apt install hcxtools"),
    Tool("hcxdumptool",        _bin("hcxdumptool"),    "Wireless assessment",   "PMKID / handshake capture for authorized Wi-Fi audits",   "apt install hcxdumptool"),
    Tool("Wifite",             _bin("wifite"),         "Wireless assessment",   "Automate Wi-Fi audit in authorized environments",         "apt install wifite"),
    Tool("Scapy",              _scapy,                 "Packet crafting/testing","Craft and analyze packets for labs",                      "pip install scapy"),
]


def installed(tool: Tool) -> bool:
    try:
        return tool.check()
    except Exception:
        return False


def snapshot() -> Dict[str, bool]:
    return {t.name: installed(t) for t in REGISTRY}
