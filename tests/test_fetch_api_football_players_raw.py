import json
from pathlib import Path

import pytest

from scripts import fetch_api_football_players_raw
from scripts.fetch_api_football_players_raw import build_parser, count_response_records, main, save_json


def test_count_response_records_returns_length_for_response_list():
    payload = {"response": [{"player": "A"}, {"player": "B"}]}

    assert count_response_records(payload) == 2


def test_count_response_records_returns_none_when_response_is_not_a_list():
    assert count_response_records({"response": {"player": "A"}}) is None
    assert count_response_records({"results": []}) is None


def test_save_json_creates_parent_directory_and_preserves_payload(tmp_path):
    output_path = tmp_path / "raw" / "api_football_players_raw.json"
    payload = {"response": [{"player": "José"}]}

    saved_path = save_json(payload, output_path)

    assert saved_path == output_path
    assert json.loads(output_path.read_text(encoding="utf-8")) == payload


def test_build_parser_parses_required_arguments_and_defaults():
    args = build_parser().parse_args(["--league-id", "140", "--season", "2024"])

    assert args.league_id == 140
    assert args.season == 2024
    assert args.page == 1
    assert args.output == Path("data/raw/api_football_players_raw.json")


def test_main_exits_when_api_key_is_empty_and_does_not_create_output(tmp_path, monkeypatch):
    output_path = tmp_path / "api_football_players_raw.json"
    monkeypatch.setattr(fetch_api_football_players_raw, "API_FOOTBALL_KEY", "")
    monkeypatch.setattr(
        "sys.argv",
        [
            "fetch_api_football_players_raw.py",
            "--league-id",
            "140",
            "--season",
            "2024",
            "--output",
            str(output_path),
        ],
    )

    with pytest.raises(SystemExit, match="API_FOOTBALL_KEY"):
        main()

    assert not output_path.exists()
