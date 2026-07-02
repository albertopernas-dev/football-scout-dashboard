from src.api_football_fixture_aggregation import (
    add_per90_metrics,
    aggregate_fixture_player_payloads,
    aggregate_player_fixture_rows,
    filter_active_rows,
    flatten_fixture_players_payload,
    flatten_fixture_players_payloads,
)


def _fixture_payload(fixture_id="1001"):
    return {
        "parameters": {"fixture": fixture_id},
        "response": [
            {
                "team": {"id": 541, "name": "Team A"},
                "players": [
                    {
                        "player": {"id": 1, "name": "Player One", "photo": "one.png"},
                        "statistics": [
                            {
                                "games": {
                                    "minutes": 90,
                                    "position": "F",
                                    "rating": "8.0",
                                    "substitute": False,
                                    "captain": True,
                                },
                                "shots": {"total": 4, "on": 2},
                                "goals": {"total": 1, "assists": 1, "saves": None, "conceded": 0},
                                "passes": {"total": 30, "key": 3, "accuracy": "80"},
                                "tackles": {"total": 1, "blocks": None, "interceptions": 2},
                                "duels": {"total": 10, "won": 6},
                                "dribbles": {"attempts": 3, "success": 2},
                                "fouls": {"drawn": 2, "committed": 1},
                                "cards": {"yellow": 1, "red": 0},
                            }
                        ],
                    },
                    {
                        "player": {"id": 2, "name": "Unused", "photo": "unused.png"},
                        "statistics": [],
                    },
                ],
            }
        ],
    }


def _second_fixture_payload():
    return {
        "parameters": {"fixture": "1002"},
        "response": [
            {
                "team": {"id": 541, "name": "Team A"},
                "players": [
                    {
                        "player": {"id": 1, "name": "Player One", "photo": "one.png"},
                        "statistics": [
                            {
                                "games": {
                                    "minutes": "45",
                                    "position": "F",
                                    "rating": "7.0",
                                    "substitute": True,
                                    "captain": False,
                                },
                                "shots": {"total": None, "on": 1},
                                "goals": {"total": 2, "assists": None},
                                "passes": {"total": "10", "key": 1, "accuracy": "100"},
                                "tackles": {"total": 2, "blocks": 1, "interceptions": None},
                                "duels": {"total": 5, "won": 4},
                                "dribbles": {"attempts": 1, "success": 1},
                                "fouls": {"drawn": 1, "committed": 2},
                                "cards": {"yellow": 0, "red": 0},
                            }
                        ],
                    }
                ],
            }
        ],
    }


def test_flatten_fixture_players_payload_returns_one_row_per_player():
    rows = flatten_fixture_players_payload(_fixture_payload())

    assert len(rows) == 2
    assert rows[0]["fixture_id"] == "1001"
    assert rows[0]["team_id"] == 541
    assert rows[0]["player_id"] == 1
    assert rows[0]["minutes"] == 90
    assert rows[1]["player"] == "Unused"
    assert rows[1]["minutes"] is None


def test_flatten_fixture_players_payloads_concatenates_rows():
    rows = flatten_fixture_players_payloads([_fixture_payload(), _second_fixture_payload()])

    assert len(rows) == 3
    assert [row["fixture_id"] for row in rows] == ["1001", "1001", "1002"]


def test_filter_active_rows_keeps_only_positive_minutes():
    rows = [{"minutes": 90}, {"minutes": "45"}, {"minutes": 0}, {"minutes": None}, {"minutes": "bad"}]

    assert filter_active_rows(rows) == [{"minutes": 90}, {"minutes": "45"}]


def test_aggregate_player_fixture_rows_groups_and_sums_metrics():
    rows = flatten_fixture_players_payloads([_fixture_payload(), _second_fixture_payload()])

    aggregated = aggregate_player_fixture_rows(rows)

    assert len(aggregated) == 1
    player = aggregated[0]
    assert player["player_id"] == 1
    assert player["team_id"] == 541
    assert player["appearances"] == 2
    assert player["starts"] == 1
    assert player["minutes"] == 135.0
    assert player["goals"] == 3.0
    assert player["assists"] == 1.0
    assert player["shots"] == 4.0
    assert player["passes"] == 40.0
    assert player["blocks"] == 1.0


def test_aggregate_player_fixture_rows_uses_most_frequent_position():
    rows = [
        {"player_id": 1, "team_id": 1, "player": "A", "team": "T", "minutes": 10, "position": "F"},
        {"player_id": 1, "team_id": 1, "player": "A", "team": "T", "minutes": 10, "position": "M"},
        {"player_id": 1, "team_id": 1, "player": "A", "team": "T", "minutes": 10, "position": "F"},
    ]

    assert aggregate_player_fixture_rows(rows)[0]["position"] == "F"


def test_aggregate_player_fixture_rows_calculates_weighted_averages():
    rows = flatten_fixture_players_payloads([_fixture_payload(), _second_fixture_payload()])

    player = aggregate_player_fixture_rows(rows)[0]

    assert player["rating_avg"] == 7.667
    assert player["pass_accuracy_avg"] == 85.0


def test_add_per90_metrics_calculates_and_rounds_values():
    rows = [{"minutes": 45, "goals": 1, "assists": 2, "shots": 3, "passes": 10}]

    enriched = add_per90_metrics(rows)

    assert enriched[0]["goals_per90"] == 2.0
    assert enriched[0]["assists_per90"] == 4.0
    assert enriched[0]["shots_per90"] == 6.0
    assert enriched[0]["passes_per90"] == 20.0


def test_add_per90_metrics_uses_none_when_minutes_are_not_positive():
    enriched = add_per90_metrics([{"minutes": 0, "goals": 1}])

    assert enriched[0]["goals_per90"] is None


def test_aggregate_fixture_player_payloads_runs_full_pipeline():
    aggregated = aggregate_fixture_player_payloads([_fixture_payload(), _second_fixture_payload()])

    assert len(aggregated) == 1
    assert aggregated[0]["minutes"] == 135.0
    assert aggregated[0]["goals_per90"] == 2.0
