import os
import sys
from enum import Enum

class FilterPreset(str, Enum):
    VISIBLE = "visible"
    ALL = "all"
    FILES = "files"
    DIRS = "dirs"

    
def list_dir(path: str = ".") -> list[str]:
    if not os.path.isdir(path):
        raise FileNotFoundError(f"No such directory: '{path}'")
    return [name for name in os.listdir(path) if not name.startswith(".")]


def main(args: list[str] | None = None) -> None:
    args = args or sys.argv[1:]
    path = args[0] if args else "."
    for name in sorted(list_dir(path)):
        print(name)


if __name__ == "__main__":
    main()