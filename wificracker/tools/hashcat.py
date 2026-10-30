import re
from pathlib import Path
from typing import Optional, Union

from ..utils import ToolError, run


_HC22000 = re.compile(r"^WPA\*", re.MULTILINE)
_BCRYPT = re.compile(r"^\$2[aby]\$")
_SHA512CRYPT = re.compile(r"^\$6\$")
_SHA256CRYPT = re.compile(r"^\$5\$")
_MD5CRYPT = re.compile(r"^\$1\$")
_HEX32 = re.compile(r"^[0-9a-fA-F]{32}$")
_HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


def detect_mode(hashfile: Union[Path, str]) -> int:
    text = Path(hashfile).read_text(errors="ignore").strip()
    if _HC22000.search(text):
        return 22000
    first = text.splitlines()[0].strip() if text else ""
    if _BCRYPT.match(first):
        return 3200
    if _SHA512CRYPT.match(first):
        return 1800
    if _SHA256CRYPT.match(first):
        return 7400
    if _MD5CRYPT.match(first):
        return 500
    if _HEX32.match(first):
        return 0
    if _HEX64.match(first):
        return 1400
    if first.count(":") == 1 and len(first.split(":")[0]) == 32:
        return 1000
    raise ToolError("could not auto-detect hash mode; pass --mode explicitly")


def crack(
    hashfile: Union[Path, str],
    wordlist: Union[Path, str],
    mode: Optional[int] = None,
    potfile: Optional[Union[Path, str]] = None,
    force: bool = False,
) -> str:
    h = Path(hashfile)
    w = Path(wordlist)
    if not h.exists():
        raise ToolError(f"hash file not found: {h}")
    if not w.exists():
        raise ToolError(f"wordlist not found: {w}")
    m = mode if mode is not None else detect_mode(h)
    cmd = [
        "hashcat",
        "-m", str(m),
        "-a", "0",
        str(h), str(w),
        "--quiet",
    ]
    if force:
        cmd.append("--force")
    if potfile:
        cmd += ["--potfile-path", str(potfile)]
    return run(cmd).stdout or ""


def show_potfile(mode: int, potfile: Optional[Union[Path, str]] = None) -> str:
    cmd = ["hashcat", "-m", str(mode), "--show"]
    if potfile:
        cmd += ["--potfile-path", str(potfile)]
    return run(cmd).stdout or ""
