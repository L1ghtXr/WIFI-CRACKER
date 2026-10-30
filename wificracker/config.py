import json
from pathlib import Path


CONFIG_DIR = Path.home() / ".config" / "wificracker"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULTS = {
    "interface": "wlan0",
    "wordlist": "/usr/share/wordlists/rockyou.txt",
    "output_dir": "cap",
    "capture_wait": 120,
    "scan_duration": 20,
}


def load() -> dict:
    data = dict(DEFAULTS)
    if CONFIG_FILE.exists():
        try:
            data.update(json.loads(CONFIG_FILE.read_text()))
        except Exception:
            pass
    return data


def save(cfg: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))
