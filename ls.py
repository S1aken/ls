import argparse
import os
from collections.abc import Callable
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


Filter = Callable[[str, str], bool]
SortKey = Callable[[str, str], str | float]

FILTERS: dict[FilterPreset, Filter] = {
    FilterPreset.VISIBLE: lambda path, name: not name.startswith("."),
    FilterPreset.ALL: lambda path, name: True,
    FilterPreset.FILES: lambda path, name: (
        not name.startswith(".") and os.path.isfile(os.path.join(path, name))
    ),
    FilterPreset.DIRS: lambda path, name: (
        not name.startswith(".") and os.path.isdir(os.path.join(path, name))
    ),
}

SORT_KEYS: dict[SortPreset, SortKey] = {
    SortPreset.NAME: lambda path, name: name,
    SortPreset.SIZE: lambda path, name: os.path.getsize(os.path.join(path, name)),
}


def list_dir(
    path: str = ".",
    preset: FilterPreset = FilterPreset.VISIBLE,
    sort: SortPreset = SortPreset.NAME,
) -> list[str]:
    if not os.path.isdir(path):
        raise FileNotFoundError(f"No such directory: '{path}'")
    keep = FILTERS[preset]
    key = SORT_KEYS[sort]
    names = [name for name in os.listdir(path) if keep(path, name)]
    return sorted(names, key=lambda name: key(path, name))


def main(args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="myls")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument(
        "--filter",
        choices=[preset.value for preset in FilterPreset],
        default=FilterPreset.VISIBLE.value,
    )
    parsed = parser.parse_args(args)
    for name in list_dir(parsed.path, FilterPreset(parsed.filter)):
        print(name)


if __name__ == "__main__":
    main()