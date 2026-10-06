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

class StylePreset(str, Enum):
    PLAIN = "plain"
    COLOR = "color"
    ICONS = "icons"


class ColorPreset(str, Enum):
    BLUE = "blue"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"


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
    SortPreset.DATE: lambda path, name: os.path.getmtime(os.path.join(path, name)),
}


Formatter = Callable[[str, str, ColorPreset], str]

COLOR_CODES: dict[ColorPreset, str] = {
    ColorPreset.BLUE: "34",
    ColorPreset.RED: "31",
    ColorPreset.GREEN: "32",
    ColorPreset.YELLOW: "33",
}


def with_icon(path: str, name: str, color: ColorPreset) -> str:
    icon = "📁" if os.path.isdir(os.path.join(path, name)) else "📄"
    return f"{icon} {name}"


def with_color(path: str, name: str, color: ColorPreset) -> str:
    if os.path.isdir(os.path.join(path, name)):
        return f"\033[{COLOR_CODES[color]}m{name}\033[0m"
    return name


FORMATTERS: dict[StylePreset, Formatter] = {
    StylePreset.PLAIN: lambda path, name, color: name,
    StylePreset.COLOR: with_color,
    StylePreset.ICONS: with_icon,
}


def format_name(
    path: str,
    name: str,
    style: StylePreset = StylePreset.PLAIN,
    color: ColorPreset = ColorPreset.BLUE,
) -> str:
    return FORMATTERS[style](path, name, color)


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
    parser.add_argument(
        "--sort",
        choices=[preset.value for preset in SortPreset],
        default=SortPreset.NAME.value,
    )
    parser.add_argument(
        "--style",
        choices=[preset.value for preset in StylePreset],
        default=StylePreset.PLAIN.value,
    )
    parsed = parser.parse_args(args)
    style = StylePreset(parsed.style)
    names = list_dir(
        parsed.path, FilterPreset(parsed.filter), SortPreset(parsed.sort)
    )
    for name in names:
        print(format_name(parsed.path, name, style))


if __name__ == "__main__":
    main()