<div align="center">

# WiFi Cracker

```text
 __        ___ _____ ___
 \ \      / (_)  ___|_ _|
  \ \ /\ / /| | |_   | |
   \ V  V / | |  _|  | |
    \_/\_/  |_|_|   |___|
```

### Real Wi-Fi Auditing Tooling

**One menu. Real tools. Zero fake results.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Linux-1793D1?style=for-the-badge&logo=linux&logoColor=white)](https://kernel.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Stable-brightgreen?style=for-the-badge)](.)
[![PRs](https://img.shields.io/badge/PRs-Welcome-blueviolet?style=for-the-badge)](.)
[![Author](https://img.shields.io/badge/Author-L1ghtXr-ff69b4?style=for-the-badge)](https://github.com/L1ghtXr)

**[Overview](#-overview) 路 [Features](#-features) 路 [Installation](#-installation) 路 [Usage](#-usage) 路 [Platforms](#-platform-support-matrix) 路 [Troubleshooting](#-troubleshooting) 路 [Legal](#-legal--terms)**

</div>

---

## 馃摉 Overview

**WiFi Cracker** is a menu-driven wireless security auditing toolkit that provides a unified interface for established wireless and network security utilities.

Instead of implementing fake or simulated functionality, the project invokes the actual security tools installed on the system.

Supported tooling includes:

- `aircrack-ng`
- `hcxtools`
- `hcxdumptool`
- `hashcat`
- `john`
- `kismet`
- `wifite`
- `nmap`
- `tshark`
- `scapy`

Every operation is backed by the output of the corresponding real binary.

There are:

- No simulated captures
- No fake handshake results
- No fabricated `KEY FOUND` messages
- No placeholder cracking results

A handshake is only considered valid when the underlying auditing tool confirms it. Likewise, PMKID conversion is only reported when the conversion tool produces valid output.

> **Designed for authorized security assessments only.**
>
> Only test wireless networks that you own or have explicit permission to assess.

---

## 鉁� Features

| Category | Capabilities |
|---|---|
| 馃攳 **Discovery** | `airodump-ng` scanning, Kismet live monitoring, `nmap` host discovery |
| 馃 **Handshake Capture** | Wireless capture workflow with real 4-way handshake verification |
| 馃攽 **PMKID Capture** | `hcxdumptool` + `hcxpcapngtool` with Hashcat `22000` support |
| 馃 **Hash Detection** | Automatic detection for `hc22000`, bcrypt, sha512crypt, sha256crypt, md5crypt, MD5, SHA-256 and NetNTLM |
| 馃洜 **Cracking** | `aircrack-ng`, `hashcat`, and `john` integration |
| 馃摝 **Packet Analysis** | `tshark`, `hcxpcapngtool`, and Scapy workflows |
| 馃帥 **Automation** | Wifite integration and persistent configuration |
| 鈿欙笍 **CLI** | Headless command-line interface for scripting and automation |
| 馃帹 **Interface** | ANSI-colored terminal UI, banners, menus and tool availability checks |
| 馃З **Configuration** | Persistent configuration stored under `~/.config/wificracker/` |
| 馃挜 **Attack Modules** | Authorized-lab integration for wireless stress-testing and resilience assessment |
| 馃敁 **WPS Auditing** | `wash`, Reaver and Bully integration for authorized WPS assessment |
| 馃暩 **MITM Tooling** | Bettercap integration for controlled interception testing |
| 馃懐 **Evil-Twin Assessment** | Wifiphisher integration for authorized captive-portal testing |
| 馃彚 **Rogue EAP Assessment** | `hostapd-wpe` integration for controlled enterprise-Wi-Fi testing |
| 馃幆 **EAP Assessment** | EAPHammer integration for authorized WPA-EAP / WPA-PSK testing |

---

# 馃殌 Installation

## Prerequisites

Before installing, ensure your system provides:

- **Linux**
- **Python 3.9+**
- Root privileges where required
- A wireless adapter capable of monitor mode
- A compatible adapter/driver for packet injection when required

Example compatible chipsets include:

- Atheros AR9271
- Ralink RT3070 / RT5370
- Realtek RTL8812AU
- MediaTek MT7610U

> Hardware and driver support varies by distribution and kernel version.

---

## 馃摝 Debian / Kali / Ubuntu / Parrot

Install the required dependencies:

```bash
sudo apt update && sudo apt install -y \
  aircrack-ng hcxtools hcxdumptool hashcat john kismet wifite \
  nmap tshark iw wireless-tools rfkill python3 python3-pip git
```

Clone the repository:

```bash
git clone https://github.com/L1ghtXr/wifi-cracker.git
cd wifi-cracker
```

Install Python dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

Run:

```bash
sudo python3 -m wificracker
```

---

## 馃悕 Installation from Source

For distributions where you prefer an isolated Python environment:

```bash
git clone https://github.com/L1ghtXr/wifi-cracker.git
cd wifi-cracker

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

Run:

```bash
sudo python3 -m wificracker
```

---

# 馃Л Usage

## Interactive Menu

The main interface provides a unified menu for the supported auditing workflows:

```text
鈹屸攢鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�
鈹�              WIFI SECURITY AUDITOR           鈹�
鈹溾攢鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�
鈹�                                             鈹�
鈹�  1. Scan        Discovery                   鈹�
鈹�  2. Info        Tools / Interfaces / Config 鈹�
鈹�  3. Audit       Handshake / PMKID Capture   鈹�
鈹�  4. Password    Aircrack / Hashcat / John   鈹�
鈹�  5. Packets     Tshark / HCX / Scapy        鈹�
鈹�                                             鈹�
鈹�  0. Exit                                    鈹�
鈹�                                             鈹�
鈹斺攢鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�鈹�
```

### Menu Components

**Scan**

- `airodump-ng`
- Kismet
- `nmap`

**Info**

- Installed tool detection
- Wireless interfaces
- Configuration information

**Audit**

- Handshake capture
- PMKID capture
- Capture verification

**Password**

- Aircrack-ng
- Hashcat
- John

**Packets**

- Tshark
- HCX utilities
- Scapy

**Attack**

- Beacon and wireless stress-testing
- Deauthentication testing
- Authentication / EAPOL stress testing
- WPS assessment
- Bettercap MITM tooling
- Evil-twin / captive-portal assessment
- Rogue EAP assessment
- EAPHammer enterprise Wi-Fi assessment

> **Safety:** Attack modules are intended only for isolated labs, networks
> you own, or targets covered by explicit written authorization.

---

## 馃枼锔� Headless CLI

The project can also be used without the interactive menu.

### Network Discovery

```bash
wificracker-cli scan -i wlan0 -t 30
```

### Capture

```bash
wificracker-cli capture \
  -i wlan0 \
  -b AA:BB:CC:DD:EE:FF \
  -c 6 \
  -o cap/
```

### PMKID Workflow

```bash
wificracker-cli pmkid \
  -i wlan0 \
  -o cap/ \
  --wait 90
```

### Password Audit

```bash
wificracker-cli crack \
  -f cap/hs_*.cap \
  -w /usr/share/wordlists/rockyou.txt
```

### Hashcat

```bash
wificracker-cli hashcat \
  -f cap/pmkid.hc22000 \
  -w /usr/share/wordlists/rockyou.txt
```

### Dependency Check

```bash
wificracker-cli deps
```

---

## 馃攧 Example Workflow

### Handshake 鈫� Password Audit

```bash
sudo wificracker-cli scan -i wlan0 -t 20

sudo wificracker-cli capture \
  -i wlan0 \
  -b AA:BB:CC:DD:EE:FF \
  -c 6 \
  -o cap/

wificracker-cli crack \
  -f cap/hs_aabbccddeeff-01.cap \
  -w rockyou.txt
```

### PMKID 鈫� Hashcat

```bash
sudo wificracker-cli pmkid \
  -i wlan0 \
  -o cap/ \
  --wait 120

hashcat -m 22000 \
  cap/pmkid_*.hc22000 \
  rockyou.txt
```

> Use these workflows only against networks for which you have explicit authorization.

---

# 馃捇 Platform Support Matrix

| Platform | Monitor Mode | Injection | PMKID | Status |
|---|:---:|:---:|:---:|---|
| 馃悏 Kali Linux | 鉁� | 鉁� | 鉁� | Full support |
| 馃 Parrot OS | 鉁� | 鉁� | 鉁� | Full support |
| 馃帺 BlackArch | 鉁� | 鉁� | 鉁� | Full support |
| 馃惂 Debian 12+ | 鉁� | 鉁� | 鉁� | Driver-dependent |
| 馃煚 Ubuntu 22.04+ | 鉁� | 鉁� | 鉁� | Driver-dependent |
| 馃徆 Arch / Manjaro | 鉁� | 鉁� | 鉁� | Full support |
| 馃帺 Fedora 38+ | 鉁� | 鉁� | 鉁� | Driver / SELinux dependent |
| 馃崕 macOS | 鈿狅笍 | 鈿狅笍 | 鉂� | Partial |
| 馃獰 WSL2 | 鉂� | 鉂� | 鉂� | Not supported |
| 馃獰 Windows | 鉂� | 鉂� | 鉂� | Not supported |
| 馃摫 Termux / Android | 鉂� | 鉂� | 鉂� | Not supported |
| 馃惓 Docker | 鉂� | 鉂� | 鉂� | Not supported |

### TL;DR

**Linux + a compatible wireless adapter is the recommended environment.**

Other platforms may support individual components such as packet analysis or offline password auditing, but wireless capture functionality depends heavily on access to the host wireless hardware and driver capabilities.

---

# 馃О Extended Wireless Auditing Dependencies

The optional **Attack** menu integrates additional wireless security
assessment tools:

```text
mdk4
reaver
bully
pixiewps
bettercap
hostapd-wpe
wifiphisher
eaphammer
```

On Debian/Kali-based systems:

```bash
sudo apt update && sudo apt install -y \
  aircrack-ng hcxtools hcxdumptool hashcat john kismet wifite \
  nmap tshark iw wireless-tools rfkill \
  mdk4 reaver bully pixiewps bettercap hostapd-wpe
```

Some projects may require separate installation:

```bash
pip install wifiphisher
git clone https://github.com/s0lst1c3/eaphammer ~/eaphammer
```

Run the dependency checker after installation:

```bash
wificracker-cli deps
```

> Package names and availability vary by distribution.

---

# 馃悏 Kali Linux Setup

Kali Linux provides the simplest setup because most required tools are available through its repositories.

```bash
sudo apt update && sudo apt install -y \
  aircrack-ng hcxtools hcxdumptool hashcat john kismet wifite \
  nmap tshark iw wireless-tools rfkill
```

Clone and install:

```bash
git clone https://github.com/L1ghtXr/wifi-cracker.git
cd wifi-cracker

sudo pip install -r requirements.txt
sudo pip install -e .
```

Run:

```bash
sudo python3 -m wificracker
```

### Verify Wireless Adapter

```bash
sudo airmon-ng start wlan0
iwconfig
sudo airmon-ng stop wlan0mon
```

Look for:

```text
Mode:Monitor
```

---

# 馃惂 Debian / Ubuntu Setup

Install the required packages:

```bash
sudo apt update && sudo apt install -y \
  aircrack-ng hcxtools hcxdumptool hashcat john kismet wifite \
  nmap tshark iw wireless-tools rfkill build-essential \
  linux-headers-$(uname -r) dkms
```

Install WiFi Cracker:

```bash
git clone https://github.com/L1ghtXr/wifi-cracker.git
cd wifi-cracker

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

If monitor mode is unavailable, verify that the adapter and its driver support the required functionality.

---

# 馃徆 Arch / Manjaro Setup

```bash
sudo pacman -S --needed \
  aircrack-ng hcxtools hcxdumptool hashcat \
  john kismet wifite nmap wireshark-cli \
  iw wireless_tools rfkill python python-pip git base-devel
```

Install:

```bash
git clone https://github.com/L1ghtXr/wifi-cracker.git
cd wifi-cracker

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

Run:

```bash
sudo python -m wificracker
```

---

# 馃帺 Fedora Setup

Install dependencies:

```bash
sudo dnf install -y \
  aircrack-ng hcxtools hcxdumptool hashcat \
  john kismet wifite nmap wireshark-cli \
  iw wireless-tools rfkill python3 python3-pip git
```

Install:

```bash
git clone https://github.com/L1ghtXr/wifi-cracker.git
cd wifi-cracker

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

Run:

```bash
sudo python3 -m wificracker
```

> Fedora's security policies and NetworkManager configuration may affect wireless auditing workflows. Adjust your system configuration only when appropriate for your authorized testing environment.

---

# 馃崕 macOS

macOS has significant limitations for wireless auditing.

Most built-in Wi-Fi hardware does not provide the same monitor-mode and packet-injection capabilities available under Linux.

### Available Components

The following components can still be useful:

- Scapy
- Nmap
- Tshark
- Hashcat
- Offline packet analysis

Install common tools:

```bash
brew install nmap hashcat wireshark
pip3 install scapy
```

Example host discovery:

```bash
sudo nmap -sn 192.168.1.0/24
```

Offline Hashcat workflow:

```bash
hashcat -m 22000 handshake.hc22000 rockyou.txt
```

For wireless capture, a Linux environment with a compatible USB wireless adapter is recommended.

---

# 鉂� Unsupported Platforms

## Windows / WSL2

WSL2 and standard Windows environments generally do not provide the raw wireless PHY access required by the capture stack.

Recommended environment:

- Kali Linux Live USB
- Dedicated Linux installation
- Linux VM with compatible USB Wi-Fi passthrough

---

## 馃摫 Termux / Android

Termux itself does not provide the wireless kernel capabilities required for reliable monitor-mode and injection workflows.

Even rooted devices are highly dependent on:

- Android kernel
- Wi-Fi chipset
- Driver support
- External USB adapter support

For complete auditing functionality, use a Linux host with a compatible external wireless adapter.

---

## 馃惓 Docker

Containers do not normally own the wireless PHY.

Even configurations such as:

```text
--privileged
--net=host
```

do not automatically provide the required monitor-mode functionality.

Run the wireless auditing stack directly on the host instead.

---

# 馃洜 Troubleshooting

| Problem | Recommended Action |
|---|---|
| Interface not found | Run `iw dev` and verify the exact interface name |
| Monitor mode fails | Check adapter/driver support and retry after resolving conflicting processes |
| No valid handshake | Verify channel, signal quality and authorized test setup |
| `hcxdumptool` produces no capture | Verify adapter compatibility, channel configuration and supported bands |
| `hcxpcapngtool` has nothing to convert | Verify that the capture actually contains the required material |
| Hashcat mode detection fails | Specify the appropriate `-m` mode manually |
| NetworkManager interferes | Temporarily adjust NetworkManager behavior during an authorized capture |
| Monitor mode drops | Check driver stability and wireless power-management settings |

### Reset Wireless Interface

If a test leaves the wireless interface in an unexpected state:

```bash
sudo airmon-ng stop wlan0mon 2>/dev/null

sudo systemctl restart NetworkManager

sudo ip link set wlan0 down
sudo iw wlan0 set type managed
sudo ip link set wlan0 up
```

---

# 馃И Recommended Adapters

| Adapter | Chipset | Monitor | Injection | 5 GHz |
|---|---|:---:|:---:|:---:|
| Alfa AWUS036NHA | Atheros AR9271 | 鉁� | 鉁� | 鉂� |
| Alfa AWUS036ACH | Realtek RTL8812AU | 鉁� | 鉁� | 鉁� |
| Alfa AWUS036ACHM | MediaTek MT7610U | 鉁� | 鉁� | 鉁� |
| TP-Link TL-WN722N v1 | Atheros AR9271 | 鉁� | 鉁� | 鉂� |
| Panda PAU09 | Ralink RT5572 | 鉁� | 鉁� | 鉁� |

> **Important:** TP-Link TL-WN722N v2/v3 use different chipsets from v1. Verify the exact hardware revision before purchasing.

---

# 馃搧 Project Structure

```text
wifi-cracker/
鈹溾攢鈹� README.md
鈹溾攢鈹� LICENSE
鈹溾攢鈹� requirements.txt
鈹溾攢鈹� setup.py
鈹斺攢鈹� wificracker/
    鈹溾攢鈹� __main__.py
    鈹溾攢鈹� menu.py          # Main entrypoint and menu
    鈹溾攢鈹� cli.py           # Headless CLI commands
    鈹溾攢鈹� ui.py            # ANSI colors and banner
    鈹溾攢鈹� config.py        # Persistent configuration
    鈹溾攢鈹� interface.py     # Wireless interface lifecycle
    鈹溾攢鈹� scanner.py       # airodump-ng CSV parsing
    鈹溾攢鈹� capture.py       # Handshake and PMKID capture
    鈹溾攢鈹� cracker.py       # Aircrack-ng integration
    鈹溾攢鈹� utils.py         # Subprocess helpers and errors
    鈹斺攢鈹� tools/
        鈹溾攢鈹� deps.py          # Tool availability checks
        鈹溾攢鈹� wireshark.py     # Tshark integration
        鈹溾攢鈹� kismet.py        # Kismet integration
        鈹溾攢鈹� nmap.py          # Nmap integration
        鈹溾攢鈹� hashcat.py       # Hashcat / mode detection
        鈹溾攢鈹� john.py          # John integration
        鈹溾攢鈹� hcxtools.py      # HCX utilities
        鈹溾攢鈹� wifite.py        # Wifite integration
        鈹溾攢鈹� packets.py       # Scapy integration
        鈹斺攢鈹� attacks/         # Authorized wireless assessment modules
            鈹溾攢鈹� beacon.py
            鈹溾攢鈹� deauth.py
            鈹溾攢鈹� auth_dos.py
            鈹溾攢鈹� wps.py
            鈹溾攢鈹� bettercap.py
            鈹溾攢鈹� evil_twin.py
            鈹溾攢鈹� rogue_eap.py
            鈹斺攢鈹� eaphammer.py
```

---

# 鈿欙笍 Configuration

Persistent configuration is stored at:

```text
~/.config/wificracker/
```

The configuration file is:

```text
~/.config/wificracker/config.json
```

This allows the application to retain configuration between sessions.

---

# 馃挜 Attack & Advanced Assessment Modules

The **Attack** menu groups optional integrations for controlled wireless
security testing.

| Module | Backend | Purpose |
|---|---|---|
| 馃挜 **Beacon** | `mdk4` | Beacon-frame stress testing in an authorized lab |
| 馃挜 **Deauthentication** | `mdk4`, `aireplay-ng` | Controlled client/AP resilience testing |
| 馃挜 **Authentication DoS** | `mdk4` | Authentication stress testing |
| 馃挜 **EAPOL Stress Testing** | `mdk4` | Controlled EAPOL resilience testing |
| 馃敁 **WPS Assessment** | `wash`, Reaver, Bully | Authorized WPS security assessment |
| 馃暩 **MITM Assessment** | Bettercap | Controlled interception and traffic-analysis testing |
| 馃懐 **Evil-Twin Assessment** | Wifiphisher | Authorized captive-portal awareness testing |
| 馃彚 **Rogue EAP Assessment** | `hostapd-wpe` | Enterprise Wi-Fi authentication exposure testing |
| 馃幆 **EAP / Portal Assessment** | EAPHammer | Authorized WPA-EAP / WPA-PSK assessment |

### Authorization Requirements

Before enabling an attack-oriented module:

1. Confirm that you own the target environment or have explicit written authorization.
2. Prefer an isolated test network whenever possible.
3. Keep credential and packet collection within the approved scope.
4. Protect captured traffic, hashes, authentication material and logs.
5. Stop immediately if the target falls outside the approved scope.

---

# 馃攼 Design Principles

WiFi Cracker is built around several principles:

### Real Tooling

The project acts as an interface around established security tools rather than pretending to reproduce their functionality.

### No Fake Results

The application does not generate artificial success messages or simulated captures.

### Transparent Failures

If an underlying tool fails, the failure should be visible instead of being converted into a fake success state.

### Modular Architecture

Individual tools are isolated inside the `tools/` package, making the project easier to maintain and extend.

### Authorized Testing

The project is intended for legitimate security assessments, lab environments and networks where the tester has permission.

---

# 鈿栵笍 Legal & Terms

## Authorized Use Only

This software is intended for:

- Security professionals
- Penetration testers
- Network administrators
- Security researchers
- Authorized laboratory environments

Only test networks that you own or have explicit authorization to assess.

Unauthorized access, interception, disruption or credential attacks may violate applicable laws.

Examples of relevant legislation include:

- **United States:** Computer Fraud and Abuse Act (CFAA), 18 U.S.C. 搂 1030
- **United Kingdom:** Computer Misuse Act 1990
- **European Union:** Directive 2013/40/EU
- **Indonesia:** UU ITE and applicable amendments

Laws vary by jurisdiction. You are responsible for understanding and complying with the laws applicable to your environment.

---

## No Warranty

This software is provided **"AS IS"**, without warranty of any kind, express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose and non-infringement.

---

## No Liability

In no event shall the authors or copyright holders be liable for any claim, damages or other liability arising from the software or its use.

---

## User Responsibility

You are solely responsible for:

- Verifying authorization before testing a network
- Complying with applicable laws and regulations
- Protecting captured security data
- Securing handshakes and PMKID files
- Handling any recovered credentials responsibly
- Any consequences resulting from misuse of the software

---

## Responsible Use

The maintainers do not support:

- Unauthorized network access
- Attacks against networks without permission
- Harassment or stalking
- Unauthorized surveillance
- Circumvention of applicable laws
- Activities that violate the terms of this project

---

## Security Disclosure

If you discover a security vulnerability in WiFi Cracker, please avoid publishing sensitive details in a public issue.

Contact the maintainer privately so the issue can be investigated and addressed responsibly.

---

# 馃 Contributing

Contributions are welcome.

## Development Workflow

1. Fork the repository
2. Create a feature branch:

```bash
git checkout -b feature/new-tool
```

3. Implement and test your changes
4. Verify dependency detection:

```bash
wificracker-cli deps
```

5. Submit a pull request with a clear description

---

## Pull Request Checklist

Before submitting a PR:

- [ ] New functionality uses the real underlying tool where applicable
- [ ] No fake or simulated results
- [ ] Availability checks are added to `tools/deps.py`
- [ ] Menu integration is complete
- [ ] CLI integration is added when appropriate
- [ ] Existing functionality remains intact
- [ ] Error handling is implemented
- [ ] Documentation is updated
- [ ] Changes have been tested on the target platform

---

# 馃摐 License

This project is released under the **MIT License**.

See [`LICENSE`](LICENSE) for the complete license text.

---

# 馃懁 Author

**L1ghtXr**

GitHub: **[@L1ghtXr](https://github.com/L1ghtXr)**

---

<div align="center">

### 猸� If WiFi Cracker saved you time, consider giving the repository a star.

**Built with 馃 by L1ghtXr**

</div>
