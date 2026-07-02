import json

import pytest

from scripts.normalize_api_football_aggregated_players import load_records, main, save_json


def _aggregated_records():
    return [
        {
            "player_id": 10,
            "player": "Player One",
            "team": "Real Madrid",
            "position": "F",
            "minutes": 90,
            "goals": 1,
            "assists": 0,
        }
    ]


def test_load_records_reads_input_list(tmp_path):
    input_path = tmp_path / "aggregated.json"
    records = _aggregated_records()
    input_path.write_text(json.dumps(records), encoding="utf-8")

    assert load_records(input_path) == records


def test_load_records_fails_when_input_does_not_exist(tmp_path):
    with pytest.raises(SystemExit, match="Input file not found"):
        load_records(tmp_path / "missing.json")


def test_load_records_fails_when_json_is_not_list(tmp_path):
    input_path = tmp_path / "aggregated.json"
    input_path.write_text(json.dumps({"player": "A"}), encoding="utf-8")

    with pytest.raises(SystemExit, match="Input JSON must be a list"):
        load_records(input_path)


def test_save_json_writes_output_list(tmp_path):
    output_path = tmp_path / "canonical.json"
    records = [{"player": "A"}]

    saved = save_json(records, output_path)

    assert saved == output_path
    assert json.loads(output_path.read_text(encoding="utf-8")) == records


def test_main_loads_input_and_writes_normalized_output(tmp_path, monkeypatch):
    input_path = tmp_path / "aggregated.json"
    output_path = tmp_path / "canonical.json"
    input_path.write_text(json.dumps(_aggregated_records()), encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        [
            "normalize_api_football_aggregated_players.py",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ],
    )

    main()

    output = json.loads(output_path.read_text(encoding="utf-8"))
    assert isinstance(output, list)
    assert output[0]["player"] == "Player One"
    assert output[0]["position"] == "Forward"
    assert output[0]["source"] == "api_football_fixture_players"
