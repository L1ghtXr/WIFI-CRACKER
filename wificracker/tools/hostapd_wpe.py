from pathlib import Path
from typing import Optional

from ..utils import ToolError, run_quiet, which


_CFG_TEMPLATE = """interface={iface}
driver=nl80211
ssid={essid}
channel={channel}
hw_mode=g

ieee8021x=1
eap_server=1
eap_user_file=/etc/hostapd-wpe/hostapd.eap_user
ca_cert=/etc/hostapd-wpe/certs/ca.pem
server_cert=/etc/hostapd-wpe/certs/server.pem
private_key=/etc/hostapd-wpe/certs/server.key
dh_file=/etc/hostapd-wpe/certs/dh
auth_algs=3
wpa_key_mgmt=WPA-EAP
wpa_pairwise=CCMP
wpa=2
"""


def build_config(iface: str, essid: str, channel: int,
                 out: str = "/tmp/hostapd-wpe.conf") -> Path:
    p = Path(out)
    p.write_text(_CFG_TEMPLATE.format(iface=iface, essid=essid, channel=channel))
    return p


def launch(iface: str, essid: str, channel: int = 6,
           out: Optional[str] = None) -> None:
    if which("hostapd-wpe") is None:
        raise ToolError("hostapd-wpe not installed (apt install hostapd-wpe)")
    cfg = build_config(iface, essid, channel, out or "/tmp/hostapd-wpe.conf")
    run_quiet(["hostapd-wpe", str(cfg)])
