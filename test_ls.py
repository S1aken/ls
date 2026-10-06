from ls import FilterPreset, SortPreset, format_name, StylePreset, list_dir, main 
from typing import get_type_hints
import pytest
import os


def test_list_dir_returns_files_in_current_folder(tmp_path):
    (tmp_path / "a.txt").touch()
    (tmp_path / "b.txt").touch()

    result = list_dir(str(tmp_path))

    assert sorted(result) == ["a.txt", "b.txt"]

def test_main_prints_files(tmp_path, capsys):
    (tmp_path / "c.txt").touch()

    main([str(tmp_path)])

    captured = capsys.readouterr()
    assert "c.txt" in captured.out

def test_list_dir_returns_empty_list_for_empty_folder(tmp_path):
    result = list_dir(str(tmp_path))

    assert result == []

def test_list_dir_raises_clear_error_for_missing_folder():
    with pytest.raises(FileNotFoundError, match="No such directory"):
        list_dir("olmayan_klasor")

def test_list_dir_hides_hidden_files_by_default(tmp_path):
    (tmp_path / "visible.txt").touch()
    (tmp_path / ".hidden.txt").touch()

    result = list_dir(str(tmp_path))

    assert result == ["visible.txt"]

def test_list_dir_has_type_hints():
    hints = get_type_hints(list_dir)

    assert hints == {
        "path": str,
        "preset": FilterPreset,
        "sort": SortPreset,
        "return": list[str],
    }

def test_main_has_type_hints():
    hints = get_type_hints(main)

    assert hints == {"args": list[str] | None, "return": type(None)}

def test_filter_preset_has_expected_values():
    assert [preset.value for preset in FilterPreset] == [
        "visible",
        "all",
        "files",
        "dirs",
    ]

def test_list_dir_all_preset_shows_hidden_files(tmp_path):
    (tmp_path / "visible.txt").touch()
    (tmp_path / ".hidden.txt").touch()

    result = list_dir(str(tmp_path), FilterPreset.ALL)

    assert sorted(result) == [".hidden.txt", "visible.txt"]

def test_list_dir_files_preset_shows_only_files(tmp_path):
    (tmp_path / "a.txt").touch()
    (tmp_path / "folder").mkdir()

    result = list_dir(str(tmp_path), FilterPreset.FILES)

    assert result == ["a.txt"]

def test_list_dir_dirs_preset_shows_only_folders(tmp_path):
    (tmp_path / "a.txt").touch()
    (tmp_path / "folder").mkdir()

    result = list_dir(str(tmp_path), FilterPreset.DIRS)

    assert result == ["folder"]

def test_main_filter_option_selects_preset(tmp_path, capsys):
    (tmp_path / "a.txt").touch()
    (tmp_path / "folder").mkdir()

    main([str(tmp_path), "--filter", "dirs"])

    captured = capsys.readouterr()
    assert captured.out == "folder\n"

def test_sort_preset_has_expected_values():
    assert [preset.value for preset in SortPreset] == [
        "name",
        "size",
        "date",
    ]

def test_list_dir_size_sort_orders_smallest_first(tmp_path):
    (tmp_path / "big.txt").write_text("x" * 100)
    (tmp_path / "mid.txt").write_text("x" * 10)
    (tmp_path / "small.txt").write_text("x")

    result = list_dir(str(tmp_path), sort=SortPreset.SIZE)

    assert result == ["small.txt", "mid.txt", "big.txt"]

def test_list_dir_date_sort_orders_oldest_first(tmp_path):
    old = tmp_path / "old.txt"
    new = tmp_path / "new.txt"
    old.touch()
    new.touch()
    os.utime(old, (1_000_000_000, 1_000_000_000))
    os.utime(new, (2_000_000_000, 2_000_000_000))

    result = list_dir(str(tmp_path), sort=SortPreset.DATE)

    assert result == ["old.txt", "new.txt"]

def test_main_sort_option_selects_preset(tmp_path, capsys):
    (tmp_path / "big.txt").write_text("x" * 100)
    (tmp_path / "small.txt").write_text("x")

    main([str(tmp_path), "--sort", "size"])

    captured = capsys.readouterr()
    assert captured.out == "small.txt\nbig.txt\n"

def test_style_preset_has_expected_values():
    assert [preset.value for preset in StylePreset] == [
        "plain",
        "color",
        "icons",
    ]

def test_format_name_plain_returns_name_unchanged(tmp_path):
    (tmp_path / "a.txt").touch()

    result = format_name(str(tmp_path), "a.txt", StylePreset.PLAIN)

    assert result == "a.txt"