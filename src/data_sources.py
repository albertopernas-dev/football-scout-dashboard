from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Callable
from urllib.request import urlopen

import pandas as pd

from src.config import (
    DATABASE_PATH,
    DATA_SOURCE_PRIORITY,
    EXTERNAL_PROVIDER_URL,
    PLAYERS_TABLE,
    SAMPLE_DATA_PATH,
)


Fetcher = Callable[[str], object]


def load_players_from_sqlite(database_path: str | Path, table_name: str) -> pd.DataFrame:
    path = Path(database_path)
    if not path.exists():
        return pd.DataFrame()
    try:
        with sqlite3.connect(path) as connection:
            return pd.read_sql_query(f'SELECT * FROM "{table_name}"', connection)
    except (sqlite3.Error, pd.errors.DatabaseError):
        return pd.DataFrame()


def _default_fetcher(url: str) -> object:
    with urlopen(url, timeout=10) as response:
        return response.read().decode("utf-8")


def _records_from_external_payload(payload: object) -> list[dict]:
    if hasattr(payload, "json"):
        payload = payload.json()
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")
    if isinstance(payload, str):
        payload = json.loads(payload)
    if isinstance(payload, dict):
        payload = payload.get("players", payload.get("response", []))
    if isinstance(payload, list):
        return [record for record in payload if isinstance(record, dict)]
    return []


def load_players_from_external_provider(url: str, fetcher: Fetcher | None = None) -> pd.DataFrame:
    if not url:
        return pd.DataFrame()
    try:
        payload = (fetcher or _default_fetcher)(url)
        records = _records_from_external_payload(payload)
        return pd.DataFrame(records)
    except (ValueError, TypeError, OSError):
        return pd.DataFrame()


def load_players_from_csv(path: str | Path) -> pd.DataFrame:
    csv_path = Path(path)
    if not csv_path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(csv_path)
    except (pd.errors.EmptyDataError, OSError):
        return pd.DataFrame()


def load_players_data(
    database_path: str | Path = DATABASE_PATH,
    table_name: str = PLAYERS_TABLE,
    external_url: str = EXTERNAL_PROVIDER_URL,
    csv_path: str | Path = SAMPLE_DATA_PATH,
    priority: tuple[str, ...] = DATA_SOURCE_PRIORITY,
    fetcher: Fetcher | None = None,
) -> pd.DataFrame:
    data, _metadata = load_players_data_with_metadata(
        database_path=database_path,
        table_name=table_name,
        external_url=external_url,
        csv_path=csv_path,
        priority=priority,
        fetcher=fetcher,
    )
    return data


def load_players_data_with_metadata(
    database_path: str | Path = DATABASE_PATH,
    table_name: str = PLAYERS_TABLE,
    external_url: str = EXTERNAL_PROVIDER_URL,
    csv_path: str | Path = SAMPLE_DATA_PATH,
    priority: tuple[str, ...] = DATA_SOURCE_PRIORITY,
    fetcher: Fetcher | None = None,
) -> tuple[pd.DataFrame, dict]:
    loaders = {
        "sqlite": lambda: (
            load_players_from_sqlite(database_path, table_name),
            {"source": "sqlite", "path": str(database_path), "table": table_name},
        ),
        "external": lambda: (
            load_players_from_external_provider(external_url, fetcher=fetcher),
            {"source": "external", "url": external_url},
        ),
        "csv": lambda: (
            load_players_from_csv(csv_path),
            {"source": "csv", "path": str(csv_path)},
        ),
    }

    for source in priority:
        loader = loaders.get(source)
        if loader is None:
            continue
        try:
            data, metadata = loader()
        except Exception:
            data = pd.DataFrame()
            metadata = {}
        if not data.empty:
            return data, {**metadata, "row_count": len(data)}

    raise ValueError("No player data could be loaded from SQLite, external provider, or CSV fallback.")
