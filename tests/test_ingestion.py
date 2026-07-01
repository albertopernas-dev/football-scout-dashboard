import pandas as pd
import pytest

from src.data_sources import load_players_from_sqlite
from src.ingestion import load_csv_to_sqlite, load_external_to_sqlite


def test_load_csv_to_sqlite_creates_players_table_and_returns_row_count(tmp_path):
    csv_path = tmp_path / "players.csv"
    database_path = tmp_path / "football_scout.db"
    pd.DataFrame(
        {
            "player": ["Ana", "Bea"],
            "age": [20, 22],
            "position": ["LW", "RW"],
        }
    ).to_csv(csv_path, index=False)

    row_count = load_csv_to_sqlite(csv_path, database_path, "players")
    loaded = load_players_from_sqlite(database_path, "players")

    assert row_count == 2
    assert loaded["player"].tolist() == ["Ana", "Bea"]
    assert loaded["position"].tolist() == ["LW", "RW"]


def test_load_csv_to_sqlite_replaces_existing_players_table(tmp_path):
    csv_path = tmp_path / "players.csv"
    database_path = tmp_path / "football_scout.db"
    pd.DataFrame({"player": ["Ana"]}).to_csv(csv_path, index=False)
    load_csv_to_sqlite(csv_path, database_path, "players")
    pd.DataFrame({"player": ["Bea", "Clara"]}).to_csv(csv_path, index=False)

    row_count = load_csv_to_sqlite(csv_path, database_path, "players")
    loaded = load_players_from_sqlite(database_path, "players")

    assert row_count == 2
    assert loaded["player"].tolist() == ["Bea", "Clara"]


def test_load_csv_to_sqlite_raises_clear_error_for_missing_csv(tmp_path):
    with pytest.raises(FileNotFoundError, match="CSV file not found"):
        load_csv_to_sqlite(tmp_path / "missing.csv", tmp_path / "football_scout.db", "players")


def test_load_external_to_sqlite_loads_mocked_provider_data(tmp_path):
    database_path = tmp_path / "football_scout.db"

    def fetcher(url):
        return [{"player": "External", "age": 19, "position": "LW"}]

    row_count = load_external_to_sqlite(
        "https://example.test/players",
        database_path,
        "players",
        fetcher=fetcher,
    )
    loaded = load_players_from_sqlite(database_path, "players")

    assert row_count == 1
    assert loaded.to_dict("records") == [{"player": "External", "age": 19, "position": "LW"}]


def test_load_external_to_sqlite_rejects_empty_url(tmp_path):
    with pytest.raises(ValueError, match="EXTERNAL_PROVIDER_URL"):
        load_external_to_sqlite("", tmp_path / "football_scout.db", "players", fetcher=lambda url: [])


def test_load_external_to_sqlite_rejects_empty_provider_response(tmp_path):
    with pytest.raises(ValueError, match="No player data returned"):
        load_external_to_sqlite(
            "https://example.test/players",
            tmp_path / "football_scout.db",
            "players",
            fetcher=lambda url: [],
        )


def test_load_external_to_sqlite_uses_injected_fetcher_without_real_network(tmp_path):
    calls = []

    def fetcher(url):
        calls.append(url)
        return {"players": [{"player": "Injected"}]}

    row_count = load_external_to_sqlite(
        "https://example.test/players",
        tmp_path / "football_scout.db",
        "players",
        fetcher=fetcher,
    )

    assert row_count == 1
    assert calls == ["https://example.test/players"]


def test_load_external_to_sqlite_normalizes_provider_payload(tmp_path):
    database_path = tmp_path / "football_scout.db"

    def fetcher(url):
        return [
            {
                "player": {"name": "Player Name", "age": 22},
                "statistics": [
                    {
                        "team": {"name": "Team A"},
                        "league": {"name": "League A", "season": 2025},
                        "games": {"position": "Attacker", "minutes": 1200},
                        "goals": {"total": 10, "assists": 4},
                    }
                ],
            }
        ]

    row_count = load_external_to_sqlite(
        "https://example.test/players",
        database_path,
        "players",
        fetcher=fetcher,
        provider="api_football",
    )
    loaded = load_players_from_sqlite(database_path, "players")

    assert row_count == 1
    assert loaded.loc[0, "player"] == "Player Name"
    assert loaded.loc[0, "team"] == "Team A"
    assert loaded.loc[0, "goals"] == 10


def test_load_external_to_sqlite_normalizes_api_football_response_payload(tmp_path):
    database_path = tmp_path / "football_scout.db"

    def fetcher(url):
        return {
            "response": [
                {
                    "player": {"name": "Player Name", "age": 22},
                    "statistics": [
                        {
                            "team": {"name": "Team A"},
                            "league": {"name": "League A", "season": 2025},
                            "games": {"position": "Attacker", "minutes": 1200},
                            "goals": {"total": 10, "assists": 4},
                        }
                    ],
                }
            ]
        }

    row_count = load_external_to_sqlite(
        "https://example.test/players",
        database_path,
        "players",
        fetcher=fetcher,
        provider="api_football",
    )
    loaded = load_players_from_sqlite(database_path, "players")

    assert row_count == 1
    assert loaded.loc[0, "player"] == "Player Name"
    assert loaded.loc[0, "team"] == "Team A"
    assert loaded.loc[0, "goals"] == 10
