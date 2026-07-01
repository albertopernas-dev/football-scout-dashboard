import pandas as pd

from src.external_normalization import normalize_external_players


def test_normalize_external_players_accepts_flat_generic_list_with_aliases():
    records = [
        {
            "Name": "Ana",
            "Edad": 20,
            "Club": "Madrid",
            "Liga": "Liga F",
            "Minutos": 1200,
            "Goles": 8,
        }
    ]

    result = normalize_external_players(records)

    assert result.loc[0, "player"] == "Ana"
    assert result.loc[0, "age"] == 20
    assert result.loc[0, "team"] == "Madrid"
    assert result.loc[0, "minutes"] == 1200
    assert result.loc[0, "goals"] == 8


def test_normalize_external_players_accepts_players_dict():
    payload = {"players": [{"player": "Ana", "team": "Madrid"}]}

    result = normalize_external_players(payload)

    assert result[["player", "team"]].to_dict("records") == [{"player": "Ana", "team": "Madrid"}]


def test_normalize_external_players_accepts_response_dict():
    payload = {"response": [{"player": "Ana", "team": "Madrid"}]}

    result = normalize_external_players(payload)

    assert result[["player", "team"]].to_dict("records") == [{"player": "Ana", "team": "Madrid"}]


def test_normalize_external_players_accepts_dataframe():
    frame = pd.DataFrame({"Jugador": ["Ana"], "Equipo": ["Madrid"]})

    result = normalize_external_players(frame)

    assert result[["player", "team"]].to_dict("records") == [{"player": "Ana", "team": "Madrid"}]


def test_normalize_external_players_handles_empty_input():
    assert normalize_external_players([]).empty
    assert normalize_external_players({"players": []}).empty


def test_normalize_external_players_handles_missing_optional_fields():
    result = normalize_external_players([{"player": "Ana"}])

    assert result.loc[0, "player"] == "Ana"
    assert "xg" not in result.columns


def test_normalize_external_players_api_football_nested_structure():
    payload = [
        {
            "player": {"name": "Player Name", "age": 22},
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

    result = normalize_external_players(payload, provider="api_football")

    assert result.to_dict("records") == [
        {
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
    ]
