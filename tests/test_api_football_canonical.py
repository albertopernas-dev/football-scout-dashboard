import pandas as pd

from src.api_football_canonical import (
    normalize_api_football_aggregated_players,
    normalize_api_football_position,
)
from src.data_cleaning import clean_player_data
from src.features import add_per90_metrics


def _aggregated_records():
    return [
        {
            "player_id": 10,
            "player": "Player One",
            "team_id": 541,
            "team": "Real Madrid",
            "photo": "photo.png",
            "position": "F",
            "appearances": 2,
            "starts": 1,
            "minutes": "135",
            "goals": "3",
            "assists": 1,
            "shots": 4,
            "key_passes": 2,
            "duels_won": 10,
            "interceptions": None,
            "tackles": 3,
            "passes": 40,
            "rating_avg": 7.667,
            "pass_accuracy_avg": 85.0,
        }
    ]


def test_normalize_api_football_position_maps_known_codes():
    assert normalize_api_football_position("G") == "Goalkeeper"
    assert normalize_api_football_position("D") == "Defender"
    assert normalize_api_football_position("M") == "Midfielder"
    assert normalize_api_football_position("F") == "Forward"


def test_normalize_api_football_position_returns_none_for_unknown_or_missing():
    assert normalize_api_football_position(None) is None
    assert normalize_api_football_position("X") is None


def test_normalize_api_football_aggregated_players_preserves_core_fields_and_metrics():
    rows = normalize_api_football_aggregated_players(_aggregated_records())

    assert rows == [
        {
            "external_player_id": 10,
            "player": "Player One",
            "team": "Real Madrid",
            "league": None,
            "season": None,
            "age": None,
            "position": "Forward",
            "minutes": 135.0,
            "goals": 3.0,
            "assists": 1.0,
            "shots": 4.0,
            "key_passes": 2.0,
            "duels_won": 10.0,
            "interceptions": None,
            "market_value": None,
            "contract_end": None,
            "source": "api_football_fixture_players",
            "photo": "photo.png",
            "team_id": 541,
            "appearances": 2.0,
            "starts": 1.0,
            "tackles": 3.0,
            "passes": 40.0,
            "rating_avg": 7.667,
        }
    ]


def test_normalize_api_football_aggregated_players_does_not_invent_unknown_context():
    row = normalize_api_football_aggregated_players(_aggregated_records())[0]

    assert row["age"] is None
    assert row["market_value"] is None
    assert row["contract_end"] is None
    assert row["league"] is None
    assert row["season"] is None


def test_normalize_api_football_aggregated_players_marks_source_and_ignores_pass_accuracy():
    row = normalize_api_football_aggregated_players(_aggregated_records())[0]

    assert row["source"] == "api_football_fixture_players"
    assert "pass_accuracy_avg" not in row


def test_normalized_rows_are_compatible_with_cleaning_and_features_pipeline():
    rows = normalize_api_football_aggregated_players(_aggregated_records())
    cleaned = clean_player_data(pd.DataFrame(rows))
    featured = add_per90_metrics(cleaned)

    assert {"player", "team", "league", "age", "position", "minutes", "goals_per90"}.issubset(
        featured.columns
    )
    assert featured.loc[0, "player"] == "Player One"
    assert featured.loc[0, "age"] == 0
    assert featured.loc[0, "league"] == "Unknown"
    assert featured.loc[0, "goals_per90"] == 2.0
