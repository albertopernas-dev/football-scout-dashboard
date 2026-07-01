import sqlite3

import pandas as pd
import pytest

from src.data_sources import (
    load_players_data,
    load_players_data_with_metadata,
    load_players_from_csv,
    load_players_from_external_provider,
    load_players_from_sqlite,
)


def _players() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "player": ["Ana", "Bea"],
            "age": [20, 22],
            "position": ["LW", "RW"],
            "team": ["Madrid", "Barcelona"],
            "league": ["Liga F", "Liga F"],
            "minutes": [1200, 900],
        }
    )


def _write_sqlite(path, table_name="players", df=None):
    players = df if df is not None else _players()
    with sqlite3.connect(path) as connection:
        players.to_sql(table_name, connection, index=False, if_exists="replace")


def test_load_players_from_sqlite_reads_existing_database_and_table(tmp_path):
    database_path = tmp_path / "players.db"
    _write_sqlite(database_path)

    result = load_players_from_sqlite(database_path, "players")

    assert result["player"].tolist() == ["Ana", "Bea"]


def test_load_players_data_falls_back_to_csv_when_sqlite_missing(tmp_path):
    csv_path = tmp_path / "players.csv"
    _players().to_csv(csv_path, index=False)

    result = load_players_data(
        database_path=tmp_path / "missing.db",
        table_name="players",
        external_url="",
        csv_path=csv_path,
    )

    assert result["player"].tolist() == ["Ana", "Bea"]


def test_load_players_data_falls_back_to_csv_when_sqlite_table_missing(tmp_path):
    database_path = tmp_path / "players.db"
    csv_path = tmp_path / "players.csv"
    with sqlite3.connect(database_path):
        pass
    _players().to_csv(csv_path, index=False)

    result = load_players_data(
        database_path=database_path,
        table_name="players",
        external_url="",
        csv_path=csv_path,
    )

    assert result["player"].tolist() == ["Ana", "Bea"]


def test_load_players_from_external_provider_accepts_list_response():
    def fetcher(url):
        return [{"player": "External", "age": 19}]

    result = load_players_from_external_provider("https://example.test/players", fetcher=fetcher)

    assert result.to_dict("records") == [{"player": "External", "age": 19}]


def test_load_players_from_external_provider_accepts_players_dict_response():
    def fetcher(url):
        return {"players": [{"player": "External", "age": 19}]}

    result = load_players_from_external_provider("https://example.test/players", fetcher=fetcher)

    assert result.to_dict("records") == [{"player": "External", "age": 19}]


def test_load_players_from_external_provider_accepts_response_dict_response():
    def fetcher(url):
        return {"response": [{"player": "Ana", "age": 20}]}

    result = load_players_from_external_provider("https://example.test/players", fetcher=fetcher)

    assert result.to_dict("records") == [{"player": "Ana", "age": 20}]


def test_load_players_data_raises_clear_error_when_no_source_has_data(tmp_path):
    with pytest.raises(ValueError, match="No player data could be loaded"):
        load_players_data(
            database_path=tmp_path / "missing.db",
            table_name="players",
            external_url="",
            csv_path=tmp_path / "missing.csv",
        )


def test_load_players_data_respects_source_priority(tmp_path):
    database_path = tmp_path / "players.db"
    csv_path = tmp_path / "players.csv"
    _write_sqlite(database_path, df=pd.DataFrame({"player": ["SQLite"], "age": [21]}))
    pd.DataFrame({"player": ["CSV"], "age": [22]}).to_csv(csv_path, index=False)

    result = load_players_data(
        database_path=database_path,
        table_name="players",
        external_url="https://example.test/players",
        csv_path=csv_path,
        fetcher=lambda url: [{"player": "External", "age": 20}],
        priority=("external", "sqlite", "csv"),
    )

    assert result["player"].tolist() == ["External"]


def test_load_players_data_with_metadata_returns_sqlite_source(tmp_path):
    database_path = tmp_path / "players.db"
    _write_sqlite(database_path)

    result, metadata = load_players_data_with_metadata(
        database_path=database_path,
        table_name="players",
        external_url="",
        csv_path=tmp_path / "missing.csv",
    )

    assert result["player"].tolist() == ["Ana", "Bea"]
    assert metadata == {
        "source": "sqlite",
        "path": str(database_path),
        "table": "players",
        "row_count": 2,
    }


def test_load_players_data_with_metadata_returns_external_source(tmp_path):
    result, metadata = load_players_data_with_metadata(
        database_path=tmp_path / "missing.db",
        table_name="players",
        external_url="https://example.test/players",
        csv_path=tmp_path / "missing.csv",
        fetcher=lambda url: [{"player": "External", "age": 20}],
        priority=("external", "csv"),
    )

    assert result["player"].tolist() == ["External"]
    assert metadata == {
        "source": "external",
        "url": "https://example.test/players",
        "row_count": 1,
    }


def test_load_players_data_with_metadata_returns_csv_source(tmp_path):
    csv_path = tmp_path / "players.csv"
    _players().to_csv(csv_path, index=False)

    result, metadata = load_players_data_with_metadata(
        database_path=tmp_path / "missing.db",
        table_name="players",
        external_url="",
        csv_path=csv_path,
    )

    assert result["player"].tolist() == ["Ana", "Bea"]
    assert metadata == {
        "source": "csv",
        "path": str(csv_path),
        "row_count": 2,
    }


def test_load_players_data_still_returns_only_dataframe(tmp_path):
    csv_path = tmp_path / "players.csv"
    _players().to_csv(csv_path, index=False)

    result = load_players_data(
        database_path=tmp_path / "missing.db",
        table_name="players",
        external_url="",
        csv_path=csv_path,
    )

    assert isinstance(result, pd.DataFrame)
    assert result["player"].tolist() == ["Ana", "Bea"]


def test_load_players_from_csv_returns_empty_for_missing_file(tmp_path):
    result = load_players_from_csv(tmp_path / "missing.csv")

    assert result.empty
