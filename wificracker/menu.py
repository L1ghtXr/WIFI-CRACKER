import signal
import sys
from pathlib import Path

from . import ui
from .capture import capture_handshake, capture_pmkid
from .config import load as load_cfg, save as save_cfg
from .cracker import crack_handshake
from .interface import list_interfaces, monitor_mode
from .scanner import scan
from .tools import deps, hashcat, hcxtools, john, kismet, nmap, packets, wireshark, wifite
from .utils import ToolError


def _sigint(_sig, _frm) -> None:
    print()
    raise KeyboardInterrupt


signal.signal(signal.SIGINT, _sigint)


def _scan_menu(cfg: dict) -> None:
    while True:
        print(ui.header("Scan"))
        print(ui.menu_item("1", "Wi-Fi networks (airodump-ng)"))
        print(ui.menu_item("2", "Kismet live monitor"))
        print(ui.menu_item("3", "Nmap host discovery"))
        print(ui.menu_item("0", "Back"))
        c = ui.prompt()
        if c == "0":
            return
        try:
            if c == "1":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                duration = int(ui.field(f"seconds [{cfg['scan_duration']}] >") or cfg["scan_duration"])
                with monitor_mode(iface) as mon:
                    nets = scan(mon, duration=duration)
                if not nets:
                    ui.warn("no wpa/wpa2 networks found")
                else:
                    ui.info(f"{'ESSID':<32} {'BSSID':<18} {'CH':>3} {'RSSI':>5}  ENC")
                    for n in nets:
                        print(f"  {n.essid[:32]:<32} {n.bssid:<18} {n.channel:>3} {n.rssi:>5}  {n.privacy}")
                ui.pause()
            elif c == "2":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                kismet.launch(iface)
            elif c == "3":
                subnet = ui.field("subnet (192.168.1.0/24) >")
                print(nmap.host_discovery(subnet))
                ui.pause()
        except ToolError as e:
            ui.err(str(e))
            ui.pause()


def _info_menu(cfg: dict) -> None:
    print(ui.header("Info"))
    snap = deps.snapshot()
    for tool in deps.REGISTRY:
        ok = snap[tool.name]
        tag = ui.color("[ok]", ui.GREEN) if ok else ui.color("[--]", ui.RED)
        print(f" {tag} {tool.name:<22} {tool.category:<24} {tool.purpose}")
        if not ok:
            print(f"       {ui.DIM}install: {tool.install}{ui.RESET}")
    print(ui.line())
    ui.info("interfaces:")
    ifaces = list_interfaces()
    if not ifaces:
        ui.warn("  (no wireless interfaces detected)")
    for iface in ifaces:
        print(f"  {iface}")
    print(ui.line())
    ui.info("config:")
    for k, v in cfg.items():
        print(f"  {k} = {v}")
    ui.pause()


def _audit_menu(cfg: dict) -> None:
    while True:
        print(ui.header("Audit"))
        print(ui.menu_item("1", "Capture WPA 4-way handshake"))
        print(ui.menu_item("2", "Capture PMKID (hcxdumptool)"))
        print(ui.menu_item("3", "Wifite automated audit"))
        print(ui.menu_item("0", "Back"))
        c = ui.prompt()
        if c == "0":
            return
        try:
            if c == "1":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                bssid = ui.field("target bssid >")
                channel = int(ui.field("channel >"))
                client = ui.field("client mac (blank for broadcast) >") or None
                out = Path(ui.field(f"output dir [{cfg['output_dir']}] >") or cfg["output_dir"])
                wait = int(ui.field(f"wait seconds [{cfg['capture_wait']}] >") or cfg["capture_wait"])
                with monitor_mode(iface) as mon:
                    cap = capture_handshake(mon, bssid, channel, out, wait_seconds=wait, client=client)
                ui.ok(f"handshake saved: {cap}")
                ui.pause()
            elif c == "2":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                out = Path(ui.field(f"output dir [{cfg['output_dir']}] >") or cfg["output_dir"])
                wait = int(ui.field(f"duration seconds [{cfg['capture_wait']}] >") or cfg["capture_wait"])
                with monitor_mode(iface) as mon:
                    pcapng = capture_pmkid(mon, out, timeout_seconds=wait)
                ui.ok(f"pcapng saved: {pcapng}")
                hc = hcxtools.convert_to_hashcat(pcapng)
                ui.ok(f"hashcat file: {hc}")
                ui.pause()
            elif c == "3":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                wifite.launch(iface)
        except ToolError as e:
            ui.err(str(e))
            ui.pause()


def _password_menu(cfg: dict) -> None:
    while True:
        print(ui.header("Password"))
        print(ui.menu_item("1", "Aircrack-ng (WPA handshake)"))
        print(ui.menu_item("2", "Hashcat (auto mode)"))
        print(ui.menu_item("3", "John the Ripper"))
        print(ui.menu_item("0", "Back"))
        c = ui.prompt()
        if c == "0":
            return
        try:
            if c == "1":
                pcap = Path(ui.field("pcap path >"))
                wl = Path(ui.field(f"wordlist [{cfg['wordlist']}] >") or cfg["wordlist"])
                pw = crack_handshake(pcap, wl)
                ui.ok(f"password: {pw}") if pw else ui.warn("no match")
                ui.pause()
            elif c == "2":
                h = Path(ui.field("hash file >"))
                wl = Path(ui.field(f"wordlist [{cfg['wordlist']}] >") or cfg["wordlist"])
                mode_s = ui.field("mode (blank = auto) >")
                mode = int(mode_s) if mode_s else None
                out = hashcat.crack(h, wl, mode=mode)
                if out.strip():
                    ui.ok(out.strip())
                else:
                    ui.warn("no match or hashcat already potted")
                ui.pause()
            elif c == "3":
                h = Path(ui.field("hash file >"))
                wl_s = ui.field(f"wordlist [{cfg['wordlist']}, blank = default] >")
                wl = Path(wl_s) if wl_s else None
                print(john.crack(h, wordlist=wl))
                ui.pause()
        except ToolError as e:
            ui.err(str(e))
            ui.pause()


def _packets_menu(cfg: dict) -> None:
    while True:
        print(ui.header("Packets"))
        print(ui.menu_item("1", "tshark live capture"))
        print(ui.menu_item("2", "tshark analyze pcap"))
        print(ui.menu_item("3", "hcxpcapngtool pcapng -> hc22000"))
        print(ui.menu_item("4", "Scapy ARP scan"))
        print(ui.menu_item("5", "Scapy sniff"))
        print(ui.menu_item("0", "Back"))
        c = ui.prompt()
        if c == "0":
            return
        try:
            if c == "1":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                count = int(ui.field("packet count [100] >") or "100")
                out = ui.field("output [capture.pcap] >") or "capture.pcap"
                ui.ok(f"saved: {wireshark.live_capture(iface, count, out)}")
                ui.pause()
            elif c == "2":
                pcap = Path(ui.field("pcap path >"))
                df = ui.field("display filter (blank for none) >") or None
                print(wireshark.analyze(pcap, display_filter=df))
                ui.pause()
            elif c == "3":
                pcap = Path(ui.field("pcapng/pcap path >"))
                ui.ok(f"saved: {hcxtools.convert_to_hashcat(pcap)}")
                ui.pause()
            elif c == "4":
                subnet = ui.field("subnet (192.168.1.0/24) >")
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                for mac, ip in packets.arp_scan(subnet, iface):
                    print(f"  {ip:<16} {mac}")
                ui.pause()
            elif c == "5":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                count = int(ui.field("packet count [20] >") or "20")
                packets.sniff_packets(iface, count)
                ui.pause()
        except ToolError as e:
            ui.err(str(e))
            ui.pause()


def main() -> None:
    cfg = load_cfg()
    actions = {
        "1": _scan_menu,
        "2": _info_menu,
        "3": _audit_menu,
        "4": _password_menu,
        "5": _packets_menu,
    }
    try:
        while True:
            print(ui.banner())
            print(ui.menu_item("1", "Scan"))
            print(ui.menu_item("2", "Info"))
            print(ui.menu_item("3", "Audit"))
            print(ui.menu_item("4", "Password"))
            print(ui.menu_item("5", "Packets"))
            print(ui.menu_item("0", "Exit"))
            print()
            choice = ui.prompt()
            if choice == "0":
                print(ui.color(" bye.", ui.CYAN))
                save_cfg(cfg)
                return
            fn = actions.get(choice)
            if fn is None:
                ui.warn("invalid choice")
                ui.pause()
                continue
            try:
                fn(cfg)
            except KeyboardInterrupt:
                print(ui.color("\n aborted", ui.YELLOW))
            except ToolError as e:
                ui.err(str(e))
                ui.pause()
    except KeyboardInterrupt:
        save_cfg(cfg)
        print()


if __name__ == "__main__":
    try:
        main()
    except ToolError as e:
        ui.err(str(e))
        sys.exit(1)
