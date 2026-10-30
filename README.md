<div align="center">WiFi Cracker

 __        ___ _____ ___
 \ \      / (_)  ___|_ _|
  \ \ /\ / /| | |_   | |
   \ V  V / | |  _|  | |
    \_/\_/  |_|_|   |___|

Real Wi-Fi Auditing Tooling

One menu. Real tools. Zero fake results.

""Python" (https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)" (https://python.org)
""Platform" (https://img.shields.io/badge/Platform-Linux-1793D1?style=for-the-badge&logo=linux&logoColor=white)" (https://kernel.org)
""License" (https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)" (LICENSE)
""Status" (https://img.shields.io/badge/Status-Stable-brightgreen?style=for-the-badge)" (.)
""PRs" (https://img.shields.io/badge/PRs-Welcome-blueviolet?style=for-the-badge)" (.)
""Author" (https://img.shields.io/badge/Author-L1ghtXr-ff69b4?style=for-the-badge)" (.)

"Overview" (#-overview) · "Features" (#-features) · "Installation" (#-installation) · "Usage" (#-usage) · "Platforms" (#-platform-support-matrix) · "Troubleshooting" (#-troubleshooting) · "Legal" (#-legal--terms)

</div>---

📖 Overview

WiFi Cracker is a menu-driven wireless security auditing toolkit that provides a unified interface for established wireless and network security utilities.

Instead of implementing fake or simulated functionality, the project invokes the actual security tools installed on the system.

Supported tooling includes:

- "aircrack-ng"
- "hcxtools"
- "hcxdumptool"
- "hashcat"
- "john"
- "kismet"
- "wifite"
- "nmap"
- "tshark"
- "scapy"

Every operation is backed by the output of the corresponding real binary.

There are:

- No simulated captures
- No fake handshake results
- No fabricated "KEY FOUND" messages
- No placeholder cracking results

A handshake is only considered valid when the underlying auditing tool confirms it. Likewise, PMKID conversion is only reported when the conversion tool produces valid output.

«Designed for authorized security assessments only.

Only test wireless networks that you own or have explicit permission to assess.»

---

✨ Features

Category| Capabilities
🔍 Discovery| "airodump-ng" scanning, Kismet live monitoring, "nmap" host discovery
🤝 Handshake Capture| Wireless capture workflow with real 4-way handshake verification
🔑 PMKID Capture| "hcxdumptool" + "hcxpcapngtool" with Hashcat "22000" support
🧠 Hash Detection| Automatic detection for "hc22000", bcrypt, sha512crypt, sha256crypt, md5crypt, MD5, SHA-256 and NetNTLM
🛠 Cracking| "aircrack-ng", "hashcat", and "john" integration
📦 Packet Analysis| "tshark", "hcxpcapngtool", and Scapy workflows
🎛 Automation| Wifite integration and persistent configuration
⚙️ CLI| Headless command-line interface for scripting and automation
🎨 Interface| ANSI-colored terminal UI, banners, menus and tool availability checks
🧩 Configuration| Persistent configuration stored under "~/.config/wificracker/"

---

🚀 Installation

Prerequisites

Before installing, ensure your system provides:

- Linux
- Python 3.9+
- Root privileges where required
- A wireless adapter capable of monitor mode
- A compatible adapter/driver for packet injection when required

Example compatible chipsets include:

- Atheros AR9271
- Ralink RT3070 / RT5370
- Realtek RTL8812AU
- MediaTek MT7610U

«Hardware and driver support varies by distribution and kernel version.»

---

📦 Debian / Kali / Ubuntu / Parrot

Install the required dependencies:

sudo apt update && sudo apt install -y \
  aircrack-ng hcxtools hcxdumptool hashcat john kismet wifite \
  nmap tshark iw wireless-tools rfkill python3 python3-pip git

Clone the repository:

git clone https://github.com/L1ghtXr/wifi-cracker.git
cd wifi-cracker

Install Python dependencies:

pip install -r requirements.txt
pip install -e .

Run:

sudo python3 -m wificracker

---

🐍 Installation from Source

For distributions where you prefer an isolated Python environment:

git clone https://github.com/L1ghtXr/wifi-cracker.git
cd wifi-cracker

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .

Run:

sudo python3 -m wificracker

---

🧭 Usage

Interactive Menu

The main interface provides a unified menu for the supported auditing workflows:

┌─────────────────────────────────────────────┐
│              WIFI SECURITY AUDITOR           │
├─────────────────────────────────────────────┤
│                                             │
│  1. Scan        Discovery                   │
│  2. Info        Tools / Interfaces / Config │
│  3. Audit       Handshake / PMKID Capture   │
│  4. Password    Aircrack / Hashcat / John   │
│  5. Packets     Tshark / HCX / Scapy        │
│                                             │
│  0. Exit                                    │
│                                             │
└─────────────────────────────────────────────┘

Menu Components

Scan

- "airodump-ng"
- Kismet
- "nmap"

Info

- Installed tool detection
- Wireless interfaces
- Configuration information

Audit

- Handshake capture
- PMKID capture
- Capture verification

Password

- Aircrack-ng
- Hashcat
- John

Packets

- Tshark
- HCX utilities
- Scapy

---

🖥️ Headless CLI

The project can also be used without the interactive menu.

Network Discovery

wificracker-cli scan -i wlan0 -t 30

Capture

wificracker-cli capture \
  -i wlan0 \
  -b AA:BB:CC:DD:EE:FF \
  -c 6 \
  -o cap/

PMKID Workflow

wificracker-cli pmkid \
  -i wlan0 \
  -o cap/ \
  --wait 90

Password Audit

wificracker-cli crack \
  -f cap/hs_*.cap \
  -w /usr/share/wordlists/rockyou.txt

Hashcat

wificracker-cli hashcat \
  -f cap/pmkid.hc22000 \
  -w /usr/share/wordlists/rockyou.txt

Dependency Check

wificracker-cli deps

---

🔄 Example Workflow

Handshake → Password Audit

sudo wificracker-cli scan -i wlan0 -t 20

sudo wificracker-cli capture \
  -i wlan0 \
  -b AA:BB:CC:DD:EE:FF \
  -c 6 \
  -o cap/

wificracker-cli crack \
  -f cap/hs_aabbccddeeff-01.cap \
  -w rockyou.txt

PMKID → Hashcat

sudo wificracker-cli pmkid \
  -i wlan0 \
  -o cap/ \
  --wait 120

hashcat -m 22000 \
  cap/pmkid_*.hc22000 \
  rockyou.txt

«Use these workflows only against networks for which you have explicit authorization.»

---

💻 Platform Support Matrix

Platform| Monitor Mode| Injection| PMKID| Status
🐉 Kali Linux| ✅| ✅| ✅| Full support
🦜 Parrot OS| ✅| ✅| ✅| Full support
🎩 BlackArch| ✅| ✅| ✅| Full support
🐧 Debian 12+| ✅| ✅| ✅| Driver-dependent
🟠 Ubuntu 22.04+| ✅| ✅| ✅| Driver-dependent
🏹 Arch / Manjaro| ✅| ✅| ✅| Full support
🎩 Fedora 38+| ✅| ✅| ✅| Driver / SELinux dependent
🍎 macOS| ⚠️| ⚠️| ❌| Partial
🪟 WSL2| ❌| ❌| ❌| Not supported
🪟 Windows| ❌| ❌| ❌| Not supported
📱 Termux / Android| ❌| ❌| ❌| Not supported
🐳 Docker| ❌| ❌| ❌| Not supported

TL;DR

Linux + a compatible wireless adapter is the recommended environment.

Other platforms may support individual components such as packet analysis or offline password auditing, but wireless capture functionality depends heavily on access to the host wireless hardware and driver capabilities.

---

🐉 Kali Linux Setup

Kali Linux provides the simplest setup because most required tools are available through its repositories.

sudo apt update && sudo apt install -y \
  aircrack-ng hcxtools hcxdumptool hashcat john kismet wifite \
  nmap tshark iw wireless-tools rfkill

Clone and install:

git clone https://github.com/L1ghtXr/wifi-cracker.git
cd wifi-cracker

sudo pip install -r requirements.txt
sudo pip install -e .

Run:

sudo python3 -m wificracker

Verify Wireless Adapter

sudo airmon-ng start wlan0
iwconfig
sudo airmon-ng stop wlan0mon

Look for:

Mode:Monitor

---

🐧 Debian / Ubuntu Setup

Install the required packages:

sudo apt update && sudo apt install -y \
  aircrack-ng hcxtools hcxdumptool hashcat john kismet wifite \
  nmap tshark iw wireless-tools rfkill build-essential \
  linux-headers-$(uname -r) dkms

Install WiFi Cracker:

git clone https://github.com/L1ghtXr/wifi-cracker.git
cd wifi-cracker

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .

If monitor mode is unavailable, verify that the adapter and its driver support the required functionality.

---

🏹 Arch / Manjaro Setup

sudo pacman -S --needed \
  aircrack-ng hcxtools hcxdumptool hashcat \
  john kismet wifite nmap wireshark-cli \
  iw wireless_tools rfkill python python-pip git base-devel

Install:

git clone https://github.com/L1ghtXr/wifi-cracker.git
cd wifi-cracker

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .

Run:

sudo python -m wificracker

---

🎩 Fedora Setup

Install dependencies:

sudo dnf install -y \
  aircrack-ng hcxtools hcxdumptool hashcat \
  john kismet wifite nmap wireshark-cli \
  iw wireless-tools rfkill python3 python3-pip git

Install:

git clone https://github.com/L1ghtXr/wifi-cracker.git
cd wifi-cracker

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .

Run:

sudo python3 -m wificracker

«Fedora's security policies and NetworkManager configuration may affect wireless auditing workflows. Adjust your system configuration only when appropriate for your authorized testing environment.»

---

🍎 macOS

macOS has significant limitations for wireless auditing.

Most built-in Wi-Fi hardware does not provide the same monitor-mode and packet-injection capabilities available under Linux.

Available Components

The following components can still be useful:

- Scapy
- Nmap
- Tshark
- Hashcat
- Offline packet analysis

Install common tools:

brew install nmap hashcat wireshark
pip3 install scapy

Example host discovery:

sudo nmap -sn 192.168.1.0/24

Offline Hashcat workflow:

hashcat -m 22000 handshake.hc22000 rockyou.txt

For wireless capture, a Linux environment with a compatible USB wireless adapter is recommended.

---

❌ Unsupported Platforms

Windows / WSL2

WSL2 and standard Windows environments generally do not provide the raw wireless PHY access required by the capture stack.

Recommended environment:

- Kali Linux Live USB
- Dedicated Linux installation
- Linux VM with compatible USB Wi-Fi passthrough

---

📱 Termux / Android

Termux itself does not provide the wireless kernel capabilities required for reliable monitor-mode and injection workflows.

Even rooted devices are highly dependent on:

- Android kernel
- Wi-Fi chipset
- Driver support
- External USB adapter support

For complete auditing functionality, use a Linux host with a compatible external wireless adapter.

---

🐳 Docker

Containers do not normally own the wireless PHY.

Even configurations such as:

--privileged
--net=host

do not automatically provide the required monitor-mode functionality.

Run the wireless auditing stack directly on the host instead.

---

🛠 Troubleshooting

Problem| Recommended Action
Interface not found| Run "iw dev" and verify the exact interface name
Monitor mode fails| Check adapter/driver support and retry after resolving conflicting processes
No valid handshake| Verify channel, signal quality and authorized test setup
"hcxdumptool" produces no capture| Verify adapter compatibility, channel configuration and supported bands
"hcxpcapngtool" has nothing to convert| Verify that the capture actually contains the required material
Hashcat mode detection fails| Specify the appropriate "-m" mode manually
NetworkManager interferes| Temporarily adjust NetworkManager behavior during an authorized capture
Monitor mode drops| Check driver stability and wireless power-management settings

Reset Wireless Interface

If a test leaves the wireless interface in an unexpected state:

sudo airmon-ng stop wlan0mon 2>/dev/null

sudo systemctl restart NetworkManager

sudo ip link set wlan0 down
sudo iw wlan0 set type managed
sudo ip link set wlan0 up

---

🧪 Recommended Adapters

Adapter| Chipset| Monitor| Injection| 5 GHz
Alfa AWUS036NHA| Atheros AR9271| ✅| ✅| ❌
Alfa AWUS036ACH| Realtek RTL8812AU| ✅| ✅| ✅
Alfa AWUS036ACHM| MediaTek MT7610U| ✅| ✅| ✅
TP-Link TL-WN722N v1| Atheros AR9271| ✅| ✅| ❌
Panda PAU09| Ralink RT5572| ✅| ✅| ✅

«Important: TP-Link TL-WN722N v2/v3 use different chipsets from v1. Verify the exact hardware revision before purchasing.»

---

📁 Project Structure

wifi-cracker/
├── README.md
├── LICENSE
├── requirements.txt
├── setup.py
└── wificracker/
    ├── __main__.py
    ├── menu.py          # Main entrypoint and menu
    ├── cli.py           # Headless CLI commands
    ├── ui.py            # ANSI colors and banner
    ├── config.py        # Persistent configuration
    ├── interface.py     # Wireless interface lifecycle
    ├── scanner.py       # airodump-ng CSV parsing
    ├── capture.py       # Handshake and PMKID capture
    ├── cracker.py       # Aircrack-ng integration
    ├── utils.py         # Subprocess helpers and errors
    └── tools/
        ├── deps.py          # Tool availability checks
        ├── wireshark.py     # Tshark integration
        ├── kismet.py        # Kismet integration
        ├── nmap.py          # Nmap integration
        ├── hashcat.py       # Hashcat / mode detection
        ├── john.py          # John integration
        ├── hcxtools.py      # HCX utilities
        ├── wifite.py        # Wifite integration
        └── packets.py       # Scapy integration

---

⚙️ Configuration

Persistent configuration is stored at:

~/.config/wificracker/

The configuration file is:

~/.config/wificracker/config.json

This allows the application to retain configuration between sessions.

---

🔐 Design Principles

WiFi Cracker is built around several principles:

Real Tooling

The project acts as an interface around established security tools rather than pretending to reproduce their functionality.

No Fake Results

The application does not generate artificial success messages or simulated captures.

Transparent Failures

If an underlying tool fails, the failure should be visible instead of being converted into a fake success state.

Modular Architecture

Individual tools are isolated inside the "tools/" package, making the project easier to maintain and extend.

Authorized Testing

The project is intended for legitimate security assessments, lab environments and networks where the tester has permission.

---

⚖️ Legal & Terms

Authorized Use Only

This software is intended for:

- Security professionals
- Penetration testers
- Network administrators
- Security researchers
- Authorized laboratory environments

Only test networks that you own or have explicit authorization to assess.

Unauthorized access, interception, disruption or credential attacks may violate applicable laws.

Examples of relevant legislation include:

- United States: Computer Fraud and Abuse Act (CFAA), 18 U.S.C. § 1030
- United Kingdom: Computer Misuse Act 1990
- European Union: Directive 2013/40/EU
- Indonesia: UU ITE and applicable amendments

Laws vary by jurisdiction. You are responsible for understanding and complying with the laws applicable to your environment.

---

No Warranty

This software is provided "AS IS", without warranty of any kind, express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose and non-infringement.

---

No Liability

In no event shall the authors or copyright holders be liable for any claim, damages or other liability arising from the software or its use.

---

User Responsibility

You are solely responsible for:

- Verifying authorization before testing a network
- Complying with applicable laws and regulations
- Protecting captured security data
- Securing handshakes and PMKID files
- Handling any recovered credentials responsibly
- Any consequences resulting from misuse of the software

---

Responsible Use

The maintainers do not support:

- Unauthorized network access
- Attacks against networks without permission
- Harassment or stalking
- Unauthorized surveillance
- Circumvention of applicable laws
- Activities that violate the terms of this project

---

Security Disclosure

If you discover a security vulnerability in WiFi Cracker, please avoid publishing sensitive details in a public issue.

Contact the maintainer privately so the issue can be investigated and addressed responsibly.

---

🤝 Contributing

Contributions are welcome.

Development Workflow

1. Fork the repository
2. Create a feature branch:

git checkout -b feature/new-tool

3. Implement and test your changes
4. Verify dependency detection:

wificracker-cli deps

5. Submit a pull request with a clear description

---

Pull Request Checklist

Before submitting a PR:

- [ ] New functionality uses the real underlying tool where applicable
- [ ] No fake or simulated results
- [ ] Availability checks are added to "tools/deps.py"
- [ ] Menu integration is complete
- [ ] CLI integration is added when appropriate
- [ ] Existing functionality remains intact
- [ ] Error handling is implemented
- [ ] Documentation is updated
- [ ] Changes have been tested on the target platform

---

📜 License

This project is released under the MIT License.

See ""LICENSE"" (LICENSE) for the complete license text.

---

👤 Author

L1ghtXr

GitHub: "@L1ghtXr" (https://github.com/L1ghtXr)

---

<div align="center">⭐ If WiFi Cracker saved you time, consider giving the repository a star.

Built with 🥔 by L1ghtXr

</div>
