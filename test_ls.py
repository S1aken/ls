from ls import FilterPreset, list_dir, main 
from typing import get_type_hints
import pytest


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

    assert hints == {"path": str, "preset": FilterPreset, "return": list[str]}

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