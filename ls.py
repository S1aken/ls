import argparse
import os
from enum import Enum

class FilterPreset(str, Enum):
    VISIBLE = "visible"
    ALL = "all"
    FILES = "files"
    DIRS = "dirs"

class SortPreset(str, Enum):
    NAME = "name"
    SIZE = "size"
    DATE = "date"

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
    parser = argparse.ArgumentParser(prog="myls")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument(
        "--filter",
        choices=[preset.value for preset in FilterPreset],
        default=FilterPreset.VISIBLE.value,
    )
    parsed = parser.parse_args(args)
    for name in sorted(list_dir(parsed.path, FilterPreset(parsed.filter))):
        print(name)


if __name__ == "__main__":
    main()