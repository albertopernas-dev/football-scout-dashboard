import json

import pytest

from scripts.inspect_api_football_payload import (
    count_response_records,
    extract_api_football_sample_mapping,
    extract_response_item_keys,
    extract_top_level_keys,
    load_payload,
)


def _sample_payload():
    return {
        "response": [
            {
                "player": {
                    "name": "Player Name",
                    "age": 22,
                },
                "statistics": [
                    {
                        "team": {"name": "Team A"},
                        "league": {"name": "League A", "season": 2025},
                        "games": {"position": "Attacker", "minutes": 1200},
                        "goals": {"total": 10, "assists": 4},
                        "shots": {"total": 40},
                        "passes": {"key": 22},
                        "duels": {"won": 80},
                        "tackles": {"interceptions": 18},
                    }
                ],
            }
        ]
    }


def test_load_payload_reads_valid_json(tmp_path):
    path = tmp_path / "payload.json"
    payload = {"response": [{"player": {"name": "Ana"}}]}
    path.write_text(json.dumps(payload), encoding="utf-8")

    assert load_payload(path) == payload


def test_load_payload_fails_clearly_when_file_does_not_exist(tmp_path):
    with pytest.raises(SystemExit, match="Payload file not found"):
        load_payload(tmp_path / "missing.json")


def test_count_response_records_returns_zero_when_response_is_missing_or_not_list():
    assert count_response_records({}) == 0
    assert count_response_records({"response": {"player": "Ana"}}) == 0
    assert count_response_records({"response": [1, 2]}) == 2


def test_extract_top_level_keys_returns_sorted_keys():
    assert extract_top_level_keys({"response": [], "paging": {}, "errors": []}) == [
        "errors",
        "paging",
        "response",
    ]


def test_extract_response_item_keys_returns_first_item_relevant_keys():
    keys = extract_response_item_keys(_sample_payload())

    assert keys == {
        "item": ["player", "statistics"],
        "player": ["age", "name"],
        "statistics_0": [
            "duels",
            "games",
            "goals",
            "league",
            "passes",
            "shots",
            "tackles",
            "team",
        ],
    }


def test_extract_api_football_sample_mapping_transforms_nested_payload():
    assert extract_api_football_sample_mapping(_sample_payload()) == {
        "player": "Player Name",
        "age": 22,
        "team": "Team A",
        "league": "League A",
        "season": 2025,
        "position": "Attacker",
        "minutes": 1200,
        "goals": 10,
        "assists": 4,
        "shots": 40,
        "key_passes": 22,
        "duels_won": 80,
        "interceptions": 18,
    }


def test_extract_api_football_sample_mapping_does_not_break_when_optional_fields_are_missing():
    payload = {"response": [{"player": {"name": "Ana"}, "statistics": [{}]}]}

    assert extract_api_football_sample_mapping(payload) == {"player": "Ana"}
