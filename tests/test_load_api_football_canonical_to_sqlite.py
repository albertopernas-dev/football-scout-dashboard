import json

import pytest

from scripts.load_api_football_canonical_to_sqlite import load_records, main
from src.data_sources import load_players_data_with_metadata, load_players_from_sqlite


def _records():
    return [
        {
            "player": "Player One",
            "team": "Real Madrid",
            "position": "Forward",
            "age": None,
            "minutes": 90,
            "goals": 1,
        }
    ]


def test_load_records_reads_valid_list(tmp_path):
    input_path = tmp_path / "canonical.json"
    input_path.write_text(json.dumps(_records()), encoding="utf-8")

    assert load_records(input_path) == _records()


def test_load_records_fails_when_input_missing(tmp_path):
    with pytest.raises(SystemExit, match="Input file not found"):
        load_records(tmp_path / "missing.json")


def test_load_records_fails_when_json_is_not_list(tmp_path):
    input_path = tmp_path / "canonical.json"
    input_path.write_text(json.dumps({"player": "A"}), encoding="utf-8")

    with pytest.raises(SystemExit, match="Input JSON must be a list"):
        load_records(input_path)


def test_load_records_fails_when_any_record_is_not_dict(tmp_path):
    input_path = tmp_path / "canonical.json"
    input_path.write_text(json.dumps([{"player": "A"}, "bad"]), encoding="utf-8")

    with pytest.raises(SystemExit, match="All records must be JSON objects"):
        load_records(input_path)


def test_main_loads_json_into_custom_sqlite_table(tmp_path, monkeypatch):
    input_path = tmp_path / "canonical.json"
    database_path = tmp_path / "football_scout.db"
    input_path.write_text(json.dumps(_records()), encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        [
            "load_api_football_canonical_to_sqlite.py",
            "--input",
            str(input_path),
            "--database",
            str(database_path),
            "--table",
            "players",
        ],
    )

    main()

    loaded = load_players_from_sqlite(database_path, "players")
    assert loaded["player"].tolist() == ["Player One"]
    assert loaded.loc[0, "team"] == "Real Madrid"


def test_loaded_records_are_available_through_data_sources_metadata(tmp_path, monkeypatch):
    input_path = tmp_path / "canonical.json"
    database_path = tmp_path / "football_scout.db"
    input_path.write_text(json.dumps(_records()), encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        [
            "load_api_football_canonical_to_sqlite.py",
            "--input",
            str(input_path),
            "--database",
            str(database_path),
            "--table",
            "players",
        ],
    )
    main()

    loaded, metadata = load_players_data_with_metadata(
        database_path=database_path,
        table_name="players",
        external_url="",
        csv_path=tmp_path / "missing.csv",
    )

    assert loaded["player"].tolist() == ["Player One"]
    assert metadata["source"] == "sqlite"
    assert metadata["row_count"] == 1
