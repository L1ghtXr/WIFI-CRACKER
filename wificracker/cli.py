import sys
from pathlib import Path

import click

from .capture import capture_handshake, capture_pmkid
from .cracker import crack_handshake
from .interface import monitor_mode
from .scanner import scan
from .tools import deps, hashcat, hcxtools
from .utils import ToolError


@click.group()
def main() -> None:
    """wificracker headless subcommands."""


@main.command("scan")
@click.option("-i", "--interface", required=True)
@click.option("-t", "--time", "duration", default=20, show_default=True)
def scan_cmd(interface: str, duration: int) -> None:
    with monitor_mode(interface) as mon:
        for n in scan(mon, duration=duration):
            click.echo(f"{n.essid}\t{n.bssid}\tch={n.channel}\trssi={n.rssi}\t{n.privacy}")


@main.command("capture")
@click.option("-i", "--interface", required=True)
@click.option("-b", "--bssid", required=True)
@click.option("-c", "--channel", required=True, type=int)
@click.option("-o", "--out", default="cap", show_default=True)
@click.option("--wait", default=120, show_default=True)
@click.option("--client", default=None)
def capture(interface: str, bssid: str, channel: int, out: str, wait: int, client) -> None:
    with monitor_mode(interface) as mon:
        p = capture_handshake(mon, bssid, channel, Path(out), wait_seconds=wait, client=client)
    click.echo(str(p))


@main.command("pmkid")
@click.option("-i", "--interface", required=True)
@click.option("-o", "--out", default="cap", show_default=True)
@click.option("--wait", default=120, show_default=True)
def pmkid(interface: str, out: str, wait: int) -> None:
    with monitor_mode(interface) as mon:
        p = capture_pmkid(mon, Path(out), timeout_seconds=wait)
    click.echo(str(p))
    click.echo(str(hcxtools.convert_to_hashcat(p)))


@main.command("crack")
@click.option("-f", "--file", "pcap", required=True, type=click.Path(exists=True, path_type=Path))
@click.option("-w", "--wordlist", required=True, type=click.Path(exists=True, path_type=Path))
@click.option("-b", "--bssid", default=None)
def crack(pcap: Path, wordlist: Path, bssid) -> None:
    pw = crack_handshake(pcap, wordlist, bssid=bssid)
    if pw:
        click.echo(pw)
    else:
        click.echo("no match", err=True)
        sys.exit(2)


@main.command("hashcat")
@click.option("-f", "--file", "hashfile", required=True, type=click.Path(exists=True, path_type=Path))
@click.option("-w", "--wordlist", required=True, type=click.Path(exists=True, path_type=Path))
@click.option("-m", "--mode", type=int, default=None)
def hashcat_cmd(hashfile: Path, wordlist: Path, mode) -> None:
    click.echo(hashcat.crack(hashfile, wordlist, mode=mode))


@main.command("deps")
def deps_cmd() -> None:
    for tool in deps.REGISTRY:
        ok = deps.installed(tool)
        click.echo(f"{'ok' if ok else 'missing':<8} {tool.name:<22} {tool.category}")


if __name__ == "__main__":
    try:
        main()
    except ToolError as e:
        click.echo(f"error: {e}", err=True)
        sys.exit(1)
