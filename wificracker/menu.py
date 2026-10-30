import signal
import sys
from pathlib import Path

from . import ui
from .capture import capture_handshake, capture_pmkid
from .config import load as load_cfg, save as save_cfg
from .cracker import crack_handshake
from .interface import list_interfaces, monitor_mode
from .scanner import scan
from .tools import (
    deps, hashcat, hcxtools, john, kismet, nmap, packets, wireshark, wifite,
    mdk4, aireplay, wps, bettercap, wifiphisher, hostapd_wpe, eaphammer,
)
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


def _attack_menu(cfg: dict) -> None:
    while True:
        print(ui.header("Attack"))
        print(ui.menu_item("1",  "Beacon flood (mdk4)"))
        print(ui.menu_item("2",  "Deauth storm (mdk4, per-channel broadcast)"))
        print(ui.menu_item("3",  "Auth DoS (mdk4)"))
        print(ui.menu_item("4",  "EAPOL start flood (mdk4)"))
        print(ui.menu_item("5",  "Deauth burst (aireplay-ng)"))
        print(ui.menu_item("6",  "Fake auth (aireplay-ng)"))
        print(ui.menu_item("7",  "ARP replay (aireplay-ng)"))
        print(ui.menu_item("8",  "Injection test (aireplay-ng)"))
        print(ui.menu_item("9",  "WPS scan (wash)"))
        print(ui.menu_item("10", "WPS pixie-dust (reaver -K 1)"))
        print(ui.menu_item("11", "WPS brute (reaver)"))
        print(ui.menu_item("12", "WPS bully"))
        print(ui.menu_item("13", "Bettercap MITM"))
        print(ui.menu_item("14", "Evil twin / phishing (wifiphisher)"))
        print(ui.menu_item("15", "Rogue EAP AP (hostapd-wpe)"))
        print(ui.menu_item("16", "Hostile portal (eaphammer)"))
        print(ui.menu_item("0",  "Back"))
        c = ui.prompt()
        if c == "0":
            return
        try:
            if c == "1":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                ch_s = ui.field("channel (blank = hop all) >")
                ch = int(ch_s) if ch_s else None
                wpa = ui.field("advertise as WPA? [y/N] >").lower().startswith("y")
                with monitor_mode(iface) as mon:
                    mdk4.beacon_flood(mon, channel=ch, wpa=wpa)
            elif c == "2":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                ch = int(ui.field("channel >"))
                bssid = ui.field("target bssid >") or None
                client = ui.field("client mac (blank = all) >") or None
                with monitor_mode(iface) as mon:
                    mdk4.deauth_storm(mon, ch, bssid=bssid, client=client)
            elif c == "3":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                bssid = ui.field("target bssid >")
                ch_s = ui.field("channel (blank = current) >")
                ch = int(ch_s) if ch_s else None
                with monitor_mode(iface) as mon:
                    mdk4.auth_dos(mon, bssid, channel=ch)
            elif c == "4":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                bssid = ui.field("target bssid >")
                with monitor_mode(iface) as mon:
                    mdk4.eapol_flood(mon, bssid)
            elif c == "5":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                bssid = ui.field("target bssid >")
                client = ui.field("client mac (blank = broadcast) >") or None
                count = int(ui.field("packet count [50] >") or "50")
                with monitor_mode(iface) as mon:
                    aireplay.deauth(mon, bssid, client=client, count=count)
            elif c == "6":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                essid = ui.field("target essid >")
                bssid = ui.field("target bssid >")
                my_mac = ui.field("your mac >")
                count = int(ui.field("auth count [0 = forever] >") or "0")
                with monitor_mode(iface) as mon:
                    aireplay.fake_auth(mon, essid, bssid, my_mac, count=count)
            elif c == "7":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                bssid = ui.field("target bssid >")
                my_mac = ui.field("your mac >")
                with monitor_mode(iface) as mon:
                    aireplay.arp_replay(mon, bssid, my_mac)
            elif c == "8":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                with monitor_mode(iface) as mon:
                    aireplay.injection_test(mon)
            elif c == "9":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                with monitor_mode(iface) as mon:
                    print(wps.wash(mon, timeout=30))
                ui.pause()
            elif c == "10":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                bssid = ui.field("target bssid >")
                ch_s = ui.field("channel (blank = auto) >")
                ch = int(ch_s) if ch_s else None
                with monitor_mode(iface) as mon:
                    wps.reaver_pixie(mon, bssid, channel=ch)
            elif c == "11":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                bssid = ui.field("target bssid >")
                ch_s = ui.field("channel (blank = auto) >")
                ch = int(ch_s) if ch_s else None
                delay = int(ui.field("delay seconds [1] >") or "1")
                pin = ui.field("known pin (blank for brute) >") or None
                with monitor_mode(iface) as mon:
                    wps.reaver_brute(mon, bssid, channel=ch, delay=delay, pin=pin)
            elif c == "12":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                bssid = ui.field("target bssid >")
                ch_s = ui.field("channel (blank = auto) >")
                ch = int(ch_s) if ch_s else None
                with monitor_mode(iface) as mon:
                    wps.bully(mon, bssid, channel=ch)
            elif c == "13":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                ui.warn("bettercap UI on http://127.0.0.1:80 — ctrl+c to stop")
                bettercap.launch(iface)
            elif c == "14":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                essid = ui.field("essid to clone (blank = pick) >") or None
                page = ui.field("phishing pageset [firmware-upgrade] >") or "firmware-upgrade"
                with monitor_mode(iface) as mon:
                    wifiphisher.evil_twin(mon, essid=essid, phishing_page=page)
            elif c == "15":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                essid = ui.field("rogue essid >")
                ch = int(ui.field("channel [6] >") or "6")
                hostapd_wpe.launch(iface, essid, channel=ch)
            elif c == "16":
                iface = ui.field(f"interface [{cfg['interface']}] >") or cfg["interface"]
                essid = ui.field("rogue essid >")
                ch = int(ui.field("channel [6] >") or "6")
                eaphammer.hostile_portal(iface, essid, channel=ch)
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
        "6": _attack_menu,
    }
    try:
        while True:
            print(ui.banner())
            print(ui.menu_item("1", "Scan"))
            print(ui.menu_item("2", "Info"))
            print(ui.menu_item("3", "Audit"))
            print(ui.menu_item("4", "Password"))
            print(ui.menu_item("5", "Packets"))
            print(ui.menu_item("6", "Attack"))
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
