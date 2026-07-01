import json

import pytest

from scripts.inspect_api_football_payload import (
    calculate_mapping_coverage,
    compare_mapping_strategies,
    count_statistics_entries,
    count_response_records,
    extract_api_football_sample_mapping,
    extract_api_football_mappings,
    extract_response_item_keys,
    extract_statistics_contexts,
    extract_top_level_keys,
    find_richest_mapping,
    load_payload,
    map_api_football_item_with_strategy,
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


def _multi_player_payload():
    payload = _sample_payload()
    payload["response"].append(
        {
            "player": {
                "name": "Second Player",
                "age": 25,
            },
            "statistics": [
                {
                    "team": {"name": "Team B"},
                    "games": {"minutes": 0},
                    "goals": {"total": 0, "assists": 0},
                }
            ],
        }
    )
    return payload


def _multi_statistics_payload():
    return {
        "response": [
            {
                "player": {"name": "Multi Stats Player", "age": 24},
                "statistics": [
                    {
                        "team": {"name": "Team Without Minutes"},
                        "league": {"name": "League A", "season": 2024},
                        "games": {"position": "Forward"},
                        "shots": {"total": 29},
                        "passes": {"key": 13},
                        "duels": {"won": 135},
                    },
                    {
                        "team": {"name": "Team With Minutes"},
                        "league": {"name": "League A", "season": 2024},
                        "games": {"position": "Forward", "minutes": 0},
                        "goals": {"total": 0, "assists": 0},
                        "shots": {"total": 2},
                    },
                ],
            },
            {
                "player": {"name": "Single Stats Player", "age": 28},
                "statistics": [
                    {
                        "team": {"name": "Team C"},
                        "league": {"name": "League B", "season": 2024},
                        "games": {"position": "Midfielder", "minutes": 900},
                        "goals": {"total": 3},
                        "tackles": {"interceptions": 12},
                    }
                ],
            },
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


def test_extract_api_football_mappings_returns_all_players():
    mappings = extract_api_football_mappings(_multi_player_payload())

    assert len(mappings) == 2
    assert mappings[0]["player"] == "Player Name"
    assert mappings[1] == {
        "player": "Second Player",
        "age": 25,
        "team": "Team B",
        "minutes": 0,
        "goals": 0,
        "assists": 0,
    }


def test_calculate_mapping_coverage_counts_present_fields_including_zero():
    coverage = calculate_mapping_coverage(
        [
            {"player": "A", "goals": 0, "minutes": 0},
            {"player": "B", "goals": 2},
            {"player": "C", "goals": None},
        ]
    )

    assert coverage["player"] == {"present": 3, "total": 3, "coverage_pct": 100.0}
    assert coverage["goals"] == {"present": 2, "total": 3, "coverage_pct": 66.7}
    assert coverage["minutes"] == {"present": 1, "total": 3, "coverage_pct": 33.3}


def test_calculate_mapping_coverage_returns_empty_dict_for_empty_mappings():
    assert calculate_mapping_coverage([]) == {}


def test_find_richest_mapping_returns_record_with_most_fields():
    mappings = [
        {"player": "A"},
        {"player": "B", "goals": 0, "minutes": 10},
        {"player": "C", "goals": 2},
    ]

    assert find_richest_mapping(mappings) == {"player": "B", "goals": 0, "minutes": 10}
    assert find_richest_mapping([]) == {}


def test_count_statistics_entries_calculates_totals_and_average():
    assert count_statistics_entries(_multi_statistics_payload()) == {
        "players": 2,
        "total_statistics_entries": 3,
        "players_with_multiple_statistics": 1,
        "avg_statistics_per_player": 1.5,
    }
    assert count_statistics_entries({}) == {
        "players": 0,
        "total_statistics_entries": 0,
        "players_with_multiple_statistics": 0,
        "avg_statistics_per_player": 0.0,
    }


def test_extract_statistics_contexts_returns_context_for_each_statistics_entry():
    contexts = extract_statistics_contexts(_multi_statistics_payload())

    assert contexts[0] == {
        "player": "Multi Stats Player",
        "stat_index": 0,
        "team": "Team Without Minutes",
        "league": "League A",
        "season": 2024,
        "position": "Forward",
        "has_minutes": False,
        "has_goals": False,
        "has_assists": False,
        "has_shots": True,
        "has_key_passes": True,
        "has_duels_won": True,
        "has_interceptions": False,
    }
    assert contexts[1]["team"] == "Team With Minutes"
    assert contexts[1]["has_minutes"] is True
    assert contexts[1]["has_goals"] is True
    assert contexts[1]["has_assists"] is True


def test_map_api_football_item_with_strategy_first_uses_first_statistics_entry():
    item = _multi_statistics_payload()["response"][0]

    mapping = map_api_football_item_with_strategy(item, strategy="first")

    assert mapping["team"] == "Team Without Minutes"
    assert "minutes" not in mapping
    assert mapping["shots"] == 29


def test_map_api_football_item_with_strategy_richest_uses_entry_with_most_fields():
    item = _multi_statistics_payload()["response"][0]

    mapping = map_api_football_item_with_strategy(item, strategy="richest")

    assert mapping["team"] == "Team With Minutes"
    assert mapping["minutes"] == 0
    assert mapping["goals"] == 0


def test_map_api_football_item_with_strategy_prefer_minutes_prioritizes_minutes_entry():
    item = _multi_statistics_payload()["response"][0]

    mapping = map_api_football_item_with_strategy(item, strategy="prefer_minutes")

    assert mapping["team"] == "Team With Minutes"
    assert mapping["minutes"] == 0


def test_extract_api_football_mappings_keeps_first_strategy_by_default():
    mappings = extract_api_football_mappings(_multi_statistics_payload())

    assert mappings[0]["team"] == "Team Without Minutes"
    assert "minutes" not in mappings[0]


def test_compare_mapping_strategies_returns_expected_strategy_keys():
    comparison = compare_mapping_strategies(_multi_statistics_payload())

    assert set(comparison) == {"first", "richest", "prefer_minutes"}
    assert comparison["first"]["minutes"]["present"] == 1
    assert comparison["richest"]["minutes"]["present"] == 2
    assert comparison["prefer_minutes"]["minutes"]["present"] == 2
