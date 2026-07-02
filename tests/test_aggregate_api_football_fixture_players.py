import json

import pytest

from scripts.aggregate_api_football_fixture_players import load_payload, main, save_json


def _payload(player_id, fixture_id):
    return {
        "parameters": {"fixture": str(fixture_id)},
        "response": [
            {
                "team": {"id": 1, "name": "Team A"},
                "players": [
                    {
                        "player": {"id": player_id, "name": f"Player {player_id}", "photo": None},
                        "statistics": [
                            {
                                "games": {"minutes": 90, "position": "F", "rating": "7.0", "substitute": False},
                                "goals": {"total": 1, "assists": 0},
                                "passes": {"total": 20, "accuracy": "80"},
                            }
                        ],
                    }
                ],
            }
        ],
    }


def test_load_payload_reads_valid_json(tmp_path):
    path = tmp_path / "payload.json"
    payload = _payload(1, 1001)
    path.write_text(json.dumps(payload), encoding="utf-8")

    assert load_payload(path) == payload


def test_load_payload_fails_when_input_does_not_exist(tmp_path):
    with pytest.raises(SystemExit, match="Input file not found"):
        load_payload(tmp_path / "missing.json")


def test_save_json_writes_list_payload(tmp_path):
    output = tmp_path / "out" / "aggregated.json"
    data = [{"player": "A"}]

    saved = save_json(data, output)

    assert saved == output
    assert json.loads(output.read_text(encoding="utf-8")) == data


def test_main_loads_multiple_inputs_and_writes_output(tmp_path, monkeypatch):
    input_a = tmp_path / "a.json"
    input_b = tmp_path / "b.json"
    output = tmp_path / "aggregated.json"
    input_a.write_text(json.dumps(_payload(1, 1001)), encoding="utf-8")
    input_b.write_text(json.dumps(_payload(1, 1002)), encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        [
            "aggregate_api_football_fixture_players.py",
            "--input",
            str(input_a),
            "--input",
            str(input_b),
            "--output",
            str(output),
        ],
    )

    main()

    data = json.loads(output.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["appearances"] == 2
    assert data[0]["goals"] == 2.0
