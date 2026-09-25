from ls import list_dir, main


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