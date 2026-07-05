import os

from app import get_sqlite_data_version


def test_get_sqlite_data_version_returns_none_when_database_missing(tmp_path):
    assert get_sqlite_data_version(tmp_path / "missing.db") is None


def test_get_sqlite_data_version_returns_mtime_and_size_when_database_exists(tmp_path):
    database_path = tmp_path / "football_scout.db"
    database_path.write_bytes(b"abc")

    version = get_sqlite_data_version(database_path)

    assert version is not None
    assert version[1] == 3


def test_get_sqlite_data_version_changes_when_database_file_changes(tmp_path):
    database_path = tmp_path / "football_scout.db"
    database_path.write_bytes(b"abc")
    first_version = get_sqlite_data_version(database_path)

    database_path.write_bytes(b"abcdef")
    os.utime(database_path, None)
    second_version = get_sqlite_data_version(database_path)

    assert first_version != second_version
