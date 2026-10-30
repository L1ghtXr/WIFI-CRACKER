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
    # --- recon / audit ---
    Tool("Aircrack-ng",        _bin("aircrack-ng"),    "Wireless auditing",      "Audit Wi-Fi network security",                           "apt install aircrack-ng"),
    Tool("Wireshark/tshark",   _bin("tshark"),         "Packet analysis",        "Analyze traffic/protocols",                              "apt install tshark"),
    Tool("Kismet",             _bin("kismet"),         "Wireless discovery",     "Monitor & discover Wi-Fi networks/devices",              "apt install kismet"),
    Tool("Nmap",               _bin("nmap"),           "Network scanning",       "Map hosts and services on your own network",             "apt install nmap"),
    Tool("Hashcat",            _bin("hashcat"),        "Password auditing",      "Test password strength from lawfully obtained hashes",   "apt install hashcat"),
    Tool("John the Ripper",    _bin("john"),           "Password auditing",      "Offline password/hash audit",                            "apt install john"),
    Tool("hcxtools",           _bin("hcxpcapngtool"),  "Wi-Fi protocol testing", "Analyze Wi-Fi authentication data",                      "apt install hcxtools"),
    Tool("hcxdumptool",        _bin("hcxdumptool"),    "Wireless assessment",    "PMKID / handshake capture",                              "apt install hcxdumptool"),
    Tool("Wifite",             _bin("wifite"),         "Wireless assessment",    "Automate Wi-Fi audit in authorized environments",        "apt install wifite"),
    Tool("Scapy",              _scapy,                 "Packet crafting/testing","Craft and analyze packets for labs",                     "pip install scapy"),

    # --- attack ---
    Tool("mdk4",               _bin("mdk4"),           "Wireless attack",        "Beacon flood, deauth, auth DoS, EAPOL flood",            "apt install mdk4"),
    Tool("Aireplay-ng",        _bin("aireplay-ng"),    "Wireless attack",        "Deauth, fake auth, ARP replay, injection test",          "apt install aircrack-ng"),
    Tool("Reaver",             _bin("reaver"),         "WPS attack",             "WPS PIN brute + pixie-dust",                             "apt install reaver"),
    Tool("Bully",              _bin("bully"),          "WPS attack",             "WPS PIN brute (alt to reaver)",                          "apt install bully"),
    Tool("Wash",               _bin("wash"),           "WPS scan",               "Scan for WPS-enabled APs",                               "apt install reaver"),
    Tool("Pixiewps",           _bin("pixiewps"),       "WPS attack",             "Offline WPS pixie-dust computation",                     "apt install pixiewps"),
    Tool("Bettercap",          _bin("bettercap"),      "MITM / attack",          "MITM, BLE, Wi-Fi attack framework",                      "apt install bettercap"),
    Tool("Wifiphisher",        _bin("wifiphisher"),    "Evil twin / phishing",   "Rogue AP + captive portal credential harvesting",        "pip install wifiphisher"),
    Tool("hostapd-wpe",        _bin("hostapd-wpe"),    "Rogue AP (EAP)",         "Rogue enterprise AP for EAP credential capture",         "apt install hostapd-wpe"),
    Tool("EAPHammer",          _bin("eaphammer"),      "Rogue AP (EAP)",         "Hostile portal + WPA-EAP credential capture",            "git clone https://github.com/s0lst1c3/eaphammer"),
]


def installed(tool: Tool) -> bool:
    try:
        return tool.check()
    except Exception:
        return False


def snapshot() -> Dict[str, bool]:
    return {t.name: installed(t) for t in REGISTRY}
