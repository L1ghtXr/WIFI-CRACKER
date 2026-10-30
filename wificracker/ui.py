import os
import sys


RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"


def _enable_windows_ansi() -> None:
    if os.name == "nt":
        os.system("")


_enable_windows_ansi()


def color(text: str, c: str) -> str:
    return f"{c}{text}{RESET}"


BANNER = (
    f"{CYAN}"
    " __        ___ _____ ___ \n"
    " \\ \\      / (_)  ___|_ _|\n"
    "  \\ \\ /\\ / /| | |_   | | \n"
    "   \\ V  V / | |  _|  | | \n"
    "    \\_/\\_/  |_|_|   |___|\n"
    f"{RESET}\n"
    f"{YELLOW} BY L1ghtXr{RESET}\n"
    f"{CYAN} ---------------------{RESET}\n"
)


def banner() -> str:
    return BANNER


def header(text: str) -> str:
    return f"\n{CYAN} --- {text} ---{RESET}"


def line() -> str:
    return f"{CYAN} ---------------------{RESET}"


def menu_item(num: str, label: str) -> str:
    return f" {YELLOW}{num}.{RESET} {WHITE}{label}{RESET}"


def prompt(text: str = " Select > ") -> str:
    try:
        return input(f"{YELLOW}{text}{RESET}").strip()
    except EOFError:
        return "0"


def field(text: str) -> str:
    try:
        return input(f"  {DIM}{text}{RESET} ").strip()
    except EOFError:
        return ""


def ok(msg: str) -> None:
    print(f" {GREEN}{msg}{RESET}")


def warn(msg: str) -> None:
    print(f" {YELLOW}{msg}{RESET}")


def err(msg: str) -> None:
    print(f" {RED}{msg}{RESET}", file=sys.stderr)


def info(msg: str) -> None:
    print(f" {WHITE}{msg}{RESET}")


def pause() -> None:
    try:
        input(f"\n {DIM}press Enter to continue...{RESET}")
    except EOFError:
        pass
