from ls import list_dir


def test_list_dir_returns_files_in_current_folder(tmp_path):
    (tmp_path / "a.txt").touch()
    (tmp_path / "b.txt").touch()

    result = list_dir(str(tmp_path))

    assert sorted(result) == ["a.txt", "b.txt"]