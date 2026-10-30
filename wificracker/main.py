import sys

from .menu import main
from .tools.deps import installed
from .utils import ToolError

if __name__ == "__main__":
    try:
        main()
    except ToolError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print()
