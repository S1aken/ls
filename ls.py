import os
import sys
from enum import Enum

class FilterPreset(str, Enum):
    VISIBLE = "visible"
    ALL = "all"
    FILES = "files"
    DIRS = "dirs"


def list_dir(
    path: str = ".", preset: FilterPreset = FilterPreset.VISIBLE
) -> list[str]:
    if not os.path.isdir(path):
        raise FileNotFoundError(f"No such directory: '{path}'")
    names = os.listdir(path)
    if preset == FilterPreset.ALL:
        return names
    visible = [name for name in names if not name.startswith(".")]
    if preset == FilterPreset.FILES:
        return [name for name in visible if os.path.isfile(os.path.join(path, name))]
    if preset == FilterPreset.DIRS:
        return [name for name in visible if os.path.isdir(os.path.join(path, name))]
    return visible


def main(args: list[str] | None = None) -> None:
    args = args or sys.argv[1:]
    path = args[0] if args else "."
    for name in sorted(list_dir(path)):
        print(name)


if __name__ == "__main__":
    main()