from pathlib import Path
from typing import Optional, Union

from ..utils import ToolError, run


def crack(hashfile: Union[Path, str], wordlist: Optional[Union[Path, str]] = None) -> str:
    h = Path(hashfile)
    if not h.exists():
        raise ToolError(f"hash file not found: {h}")
    cmd = ["john", str(h)]
    if wordlist:
        w = Path(wordlist)
        if not w.exists():
            raise ToolError(f"wordlist not found: {w}")
        cmd = ["john", f"--wordlist={w}", str(h)]
    return run(cmd).stdout or ""


def show(hashfile: Union[Path, str]) -> str:
    h = Path(hashfile)
    if not h.exists():
        raise ToolError(f"hash file not found: {h}")
    return run(["john", "--show", str(h)]).stdout or ""
