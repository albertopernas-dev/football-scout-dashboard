import json

import pytest

from scripts.inspect_api_football_fixture_players_payload import (
    _is_positive_number,
    calculate_field_coverage,
    detect_fixture_player_anomalies,
    extract_preview_rows,
    flatten_fixture_players,
    load_payload,
)


def _fixture_players_payload():
    return {
        "parameters": {"fixture": "1208494"},
        "response": [
            {
                "team": {"id": 541, "name": "Team A"},
                "players": [
                    {
                        "player": {"id": 1, "name": "Starter", "photo": "starter.png"},
                        "statistics": [
                            {
                                "games": {
                                    "minutes": 90,
                                    "number": 9,
                                    "position": "F",
                                    "rating": "7.5",
                                    "substitute": False,
                                    "captain": True,
                                },
                                "shots": {"total": 3, "on": 2},
                                "goals": {"total": 1, "assists": 1, "saves": None, "conceded": 0},
                                "passes": {"total": 34, "key": 2, "accuracy": "88%"},
                                "tackles": {"total": 1, "blocks": 0, "interceptions": 1},
                                "duels": {"total": 8, "won": 5},
                                "dribbles": {"attempts": 2, "success": 1},
                                "fouls": {"drawn": 2, "committed": 1},
                                "cards": {"yellow": 0, "red": 0},
                            }
                        ],
                    },
                    {
                        "player": {"id": 2, "name": "No Stats", "photo": None},
                        "statistics": [],
                    },
                ],
            },
            {
                "team": {"id": 542, "name": "Team B"},
                "players": [
                    {
                        "player": {"id": 3, "name": "Zero Minutes Activity", "photo": "zero.png"},
                        "statistics": [
                            {
                                "games": {"minutes": 0, "number": 14, "position": "M"},
                                "shots": {"total": 1, "on": 1},
                                "goals": {"total": 0, "assists": 0},
                                "passes": {"total": 0, "key": 0, "accuracy": "100%"},
                            }
                        ],
                    },
                    {
                        "player": {"id": 4, "name": "No Rating", "photo": "rating.png"},
                        "statistics": [
                            {
                                "games": {"minutes": 45, "number": 5, "position": "D"},
                                "passes": {"total": None, "accuracy": "80%"},
                            }
                        ],
                    },
                ],
            },
        ],
    }


def test_load_payload_reads_valid_json(tmp_path):
    path = tmp_path / "payload.json"
    payload = _fixture_players_payload()
    path.write_text(json.dumps(payload), encoding="utf-8")

    assert load_payload(path) == payload


def test_load_payload_fails_when_file_does_not_exist(tmp_path):
    with pytest.raises(SystemExit, match="Payload file not found"):
        load_payload(tmp_path / "missing.json")


def test_flatten_fixture_players_returns_one_row_per_player():
    rows = flatten_fixture_players(_fixture_players_payload())

    assert len(rows) == 4
    assert [row["player"] for row in rows] == [
        "Starter",
        "No Stats",
        "Zero Minutes Activity",
        "No Rating",
    ]


def test_flatten_fixture_players_extracts_fixture_id_from_parameters():
    rows = flatten_fixture_players(_fixture_players_payload())

    assert {row["fixture_id"] for row in rows} == {"1208494"}


def test_flatten_fixture_players_uses_none_for_missing_fields():
    row = flatten_fixture_players(_fixture_players_payload())[1]

    assert row["player"] == "No Stats"
    assert row["minutes"] is None
    assert row["rating"] is None
    assert row["shots"] is None


def test_calculate_field_coverage_counts_zero_as_present():
    rows = flatten_fixture_players(_fixture_players_payload())
    coverage = calculate_field_coverage(rows)

    assert coverage["minutes"]["present"] == 3
    assert coverage["goals"]["present"] == 2
    assert coverage["red_cards"]["present"] == 1


def test_extract_preview_rows_respects_limit():
    rows = flatten_fixture_players(_fixture_players_payload())

    assert len(extract_preview_rows(rows, limit=2)) == 2


def test_detect_fixture_player_anomalies_detects_minutes_missing():
    rows = flatten_fixture_players(_fixture_players_payload())

    anomalies = detect_fixture_player_anomalies(rows)

    assert "minutes_missing" in [anomaly["type"] for anomaly in anomalies]


def test_detect_fixture_player_anomalies_detects_minutes_zero_with_activity():
    rows = flatten_fixture_players(_fixture_players_payload())

    anomalies = detect_fixture_player_anomalies(rows)

    assert any(
        anomaly["player"] == "Zero Minutes Activity"
        and anomaly["type"] == "minutes_zero_with_activity"
        for anomaly in anomalies
    )


def test_detect_fixture_player_anomalies_detects_rating_missing_with_minutes():
    rows = flatten_fixture_players(_fixture_players_payload())

    anomalies = detect_fixture_player_anomalies(rows)

    assert any(
        anomaly["player"] == "No Rating" and anomaly["type"] == "rating_missing_with_minutes"
        for anomaly in anomalies
    )


def test_detect_fixture_player_anomalies_detects_pass_accuracy_without_passes():
    rows = flatten_fixture_players(_fixture_players_payload())

    anomalies = detect_fixture_player_anomalies(rows)

    assert any(
        anomaly["player"] == "Zero Minutes Activity"
        and anomaly["type"] == "pass_accuracy_without_passes"
        for anomaly in anomalies
    )
    assert any(
        anomaly["player"] == "No Rating"
        and anomaly["type"] == "pass_accuracy_without_passes"
        for anomaly in anomalies
    )


def test_is_positive_number_handles_invalid_strings():
    assert _is_positive_number(1) is True
    assert _is_positive_number("2.5") is True
    assert _is_positive_number(0) is False
    assert _is_positive_number(None) is False
    assert _is_positive_number("not-a-number") is False
