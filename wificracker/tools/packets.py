from typing import List, Tuple

from ..utils import require_root


def icmp_ping(target: str, count: int = 4) -> None:
    require_root()
    from scapy.all import ICMP, IP, sr1

    for _ in range(count):
        reply = sr1(IP(dst=target) / ICMP(), timeout=1, verbose=False)
        print(f"  {target} -> {reply.summary() if reply else 'no reply'}")


def arp_scan(subnet: str, iface: str) -> List[Tuple[str, str]]:
    require_root()
    from scapy.all import ARP, Ether, srp

    answered = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet),
                   timeout=3, iface=iface, verbose=False)[0]
    return [(recv.hwsrc, recv.psrc) for _, recv in answered]


def sniff_packets(iface: str, count: int = 20, display_filter: str = "") -> None:
    require_root()
    from scapy.all import IP, sniff

    packets = sniff(iface=iface, count=count, filter=display_filter or None)
    for p in packets:
        if IP in p:
            print(f"  {p[IP].src:<16} -> {p[IP].dst:<16} proto={p[IP].proto} len={len(p)}")
