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


def _players_with_season() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "player": ["Ana", "Bea"],
            "age": [20, 22],
            "market_value_eur": [999, 888],
            "position": ["LW", "RW"],
            "team": ["Madrid", "Barcelona"],
            "league": ["Liga F", "Liga F"],
            "season": [2024, 2024],
            "minutes": [1200, 900],
        }
    )


def _write_market_context_csv(path):
    pd.DataFrame(
        [
            {
                "player": "Ana",
                "team": "Madrid",
                "league": "Liga F",
                "season": 2024,
                "age": 24,
                "market_value_eur": 1_500_000,
                "contract_end_date": "2026-06-30",
                "source": "manual_review",
                "source_url": "https://example.com/ana",
                "confidence": "high",
                "notes": "synthetic enrichment row",
            }
        ]
    ).to_csv(path, index=False)


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
        market_context_csv_path=None,
    )

    assert result["player"].tolist() == ["Ana", "Bea"]
    assert metadata == {
        "source": "sqlite",
        "path": str(database_path),
        "table": "players",
        "row_count": 2,
        "effective_market_context_fields": True,
    }
    assert "effective_age" in result.columns


def test_load_players_data_with_metadata_returns_external_source(tmp_path):
    result, metadata = load_players_data_with_metadata(
        database_path=tmp_path / "missing.db",
        table_name="players",
        external_url="https://example.test/players",
        csv_path=tmp_path / "missing.csv",
        fetcher=lambda url: [{"player": "External", "age": 20}],
        priority=("external", "csv"),
        market_context_csv_path=None,
    )

    assert result["player"].tolist() == ["External"]
    assert metadata == {
        "source": "external",
        "url": "https://example.test/players",
        "row_count": 1,
        "effective_market_context_fields": True,
    }
    assert "effective_age" in result.columns


def test_load_players_data_with_metadata_returns_csv_source(tmp_path):
    csv_path = tmp_path / "players.csv"
    _players().to_csv(csv_path, index=False)

    result, metadata = load_players_data_with_metadata(
        database_path=tmp_path / "missing.db",
        table_name="players",
        external_url="",
        csv_path=csv_path,
        market_context_csv_path=None,
    )

    assert result["player"].tolist() == ["Ana", "Bea"]
    assert metadata == {
        "source": "csv",
        "path": str(csv_path),
        "row_count": 2,
        "effective_market_context_fields": True,
    }
    assert "effective_age" in result.columns


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


def test_load_players_data_with_metadata_does_not_load_market_context_without_config(tmp_path, monkeypatch):
    monkeypatch.delenv("FOOTBALL_SCOUT_MARKET_CONTEXT_CSV", raising=False)
    csv_path = tmp_path / "players.csv"
    _players_with_season().to_csv(csv_path, index=False)

    result, metadata = load_players_data_with_metadata(
        database_path=tmp_path / "missing.db",
        table_name="players",
        external_url="",
        csv_path=csv_path,
    )

    assert "market_context_age" not in result.columns
    assert result.loc[0, "effective_age"] == 20
    assert result.loc[0, "effective_market_value_eur"] == 999
    assert metadata["effective_market_context_fields"] is True
    assert "market_context_enabled" not in metadata


def test_load_players_data_with_metadata_uses_market_context_env_var(tmp_path, monkeypatch):
    players_path = tmp_path / "players.csv"
    market_context_path = tmp_path / "market_context.csv"
    _players_with_season().to_csv(players_path, index=False)
    _write_market_context_csv(market_context_path)
    monkeypatch.setenv("FOOTBALL_SCOUT_MARKET_CONTEXT_CSV", str(market_context_path))

    result, metadata = load_players_data_with_metadata(
        database_path=tmp_path / "missing.db",
        table_name="players",
        external_url="",
        csv_path=players_path,
    )

    assert result.loc[0, "market_context_matched"] is True
    assert result.loc[1, "market_context_matched"] is False
    assert result.loc[0, "market_context_age"] == 24
    assert result.loc[0, "market_context_market_value_eur"] == 1_500_000
    assert result.loc[0, "effective_age"] == 24
    assert result.loc[0, "effective_market_value_eur"] == 1_500_000
    assert result.loc[0, "effective_contract_end_date"] == "2026-06-30"
    assert result.loc[0, "effective_market_context_source"] == "market_context"
    assert metadata["effective_market_context_fields"] is True
    assert metadata["market_context_enabled"] is True
    assert metadata["market_context_csv_path"] == str(market_context_path)
    assert metadata["market_context_validation_error_count"] == 0
    assert metadata["market_context_duplicate_count"] == 0
    assert metadata["market_context_matched_count"] == 1
    assert metadata["market_context_matched_pct"] == 50.0
    assert metadata["market_context_age_known_pct"] == 50.0
    assert metadata["market_context_market_value_known_pct"] == 50.0
    assert metadata["market_context_contract_known_pct"] == 50.0


def test_load_players_data_with_metadata_accepts_explicit_market_context_path(tmp_path):
    players_path = tmp_path / "players.csv"
    market_context_path = tmp_path / "market_context.csv"
    _players_with_season().to_csv(players_path, index=False)
    _write_market_context_csv(market_context_path)

    result, metadata = load_players_data_with_metadata(
        database_path=tmp_path / "missing.db",
        table_name="players",
        external_url="",
        csv_path=players_path,
        market_context_csv_path=market_context_path,
    )

    assert "market_context_source" in result.columns
    assert metadata["market_context_enabled"] is True


def test_load_players_data_with_metadata_handles_missing_market_context_file(tmp_path):
    players_path = tmp_path / "players.csv"
    _players_with_season().to_csv(players_path, index=False)
    missing_market_context_path = tmp_path / "missing_market_context.csv"

    result, metadata = load_players_data_with_metadata(
        database_path=tmp_path / "missing.db",
        table_name="players",
        external_url="",
        csv_path=players_path,
        market_context_csv_path=missing_market_context_path,
    )

    assert result["player"].tolist() == ["Ana", "Bea"]
    assert "market_context_age" not in result.columns
    assert "effective_age" in result.columns
    assert metadata["effective_market_context_fields"] is True
    assert metadata["market_context_enabled"] is False
    assert metadata["market_context_csv_path"] == str(missing_market_context_path)
    assert "Market context CSV not found" in metadata["market_context_load_error"]


def test_market_context_does_not_overwrite_existing_player_values(tmp_path):
    players_path = tmp_path / "players.csv"
    market_context_path = tmp_path / "market_context.csv"
    _players_with_season().to_csv(players_path, index=False)
    _write_market_context_csv(market_context_path)

    result, _metadata = load_players_data_with_metadata(
        database_path=tmp_path / "missing.db",
        table_name="players",
        external_url="",
        csv_path=players_path,
        market_context_csv_path=market_context_path,
    )

    assert result.loc[0, "age"] == 20
    assert result.loc[0, "market_value_eur"] == 999
    assert result.loc[0, "market_context_age"] == 24
    assert result.loc[0, "market_context_market_value_eur"] == 1_500_000
    assert result.loc[0, "effective_age"] == 24
    assert result.loc[0, "effective_market_value_eur"] == 1_500_000


def test_sample_market_context_is_not_loaded_by_default(tmp_path, monkeypatch):
    monkeypatch.delenv("FOOTBALL_SCOUT_MARKET_CONTEXT_CSV", raising=False)
    players_path = tmp_path / "players.csv"
    pd.DataFrame(
        {
            "player": ["Jude Bellingham"],
            "team": ["Real Madrid"],
            "league": ["LaLiga"],
            "season": [2024],
        }
    ).to_csv(players_path, index=False)

    result, metadata = load_players_data_with_metadata(
        database_path=tmp_path / "missing.db",
        table_name="players",
        external_url="",
        csv_path=players_path,
    )

    assert "market_context_matched" not in result.columns
    assert "effective_age" in result.columns
    assert metadata["effective_market_context_fields"] is True
    assert "market_context_enabled" not in metadata


def test_load_players_from_csv_returns_empty_for_missing_file(tmp_path):
    result = load_players_from_csv(tmp_path / "missing.csv")

    assert result.empty
