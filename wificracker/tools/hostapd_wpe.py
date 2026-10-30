from pathlib import Path
from typing import Optional

from ..utils import ToolError, run_quiet, which


_DEFAULT_CERT_DIR = Path("/etc/hostapd-wpe/certs")
_DEFAULT_EAP_USER = Path("/etc/hostapd-wpe/hostapd.eap_user")


_CFG_TEMPLATE = """interface={iface}
driver=nl80211
ssid={essid}
channel={channel}
hw_mode=g

ieee8021x=1
eap_server=1
eap_user_file={eap_user}
ca_cert={certs}/ca.pem
server_cert={certs}/server.pem
private_key={certs}/server.key
dh_file={certs}/dh
auth_algs=3
wpa_key_mgmt=WPA-EAP
wpa_pairwise=CCMP
wpa=2
"""


def _preflight(certs: Path, eap_user: Path) -> None:
    if which("hostapd-wpe") is None:
        raise ToolError("hostapd-wpe not installed (apt install hostapd-wpe)")
    missing = [p for p in (
        certs / "ca.pem",
        certs / "server.pem",
        certs / "server.key",
        certs / "dh",
        eap_user,
    ) if not p.exists()]
    if missing:
        raise ToolError(
            "hostapd-wpe certs missing — run 'hostapd-wpe-setup' "
            "or copy certs into /etc/hostapd-wpe/certs/: "
            + ", ".join(str(m) for m in missing)
        )


def build_config(
    iface: str,
    essid: str,
    channel: int,
    certs: Path = _DEFAULT_CERT_DIR,
    eap_user: Path = _DEFAULT_EAP_USER,
    out: str = "/tmp/hostapd-wpe.conf",
) -> Path:
    p = Path(out)
    p.write_text(_CFG_TEMPLATE.format(
        iface=iface, essid=essid, channel=channel,
        certs=str(certs), eap_user=str(eap_user),
    ))
    return p


def launch(
    iface: str,
    essid: str,
    channel: int = 6,
    certs: Path = _DEFAULT_CERT_DIR,
    eap_user: Path = _DEFAULT_EAP_USER,
    out: Optional[str] = None,
) -> None:
    _preflight(certs, eap_user)
    cfg = build_config(iface, essid, channel, certs=certs, eap_user=eap_user,
                       out=out or "/tmp/hostapd-wpe.conf")
    run_quiet(["hostapd-wpe", str(cfg)])
