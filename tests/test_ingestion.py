import pandas as pd
import pytest

from src.data_sources import load_players_from_sqlite
from src.ingestion import load_csv_to_sqlite


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
