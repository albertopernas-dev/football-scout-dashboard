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
    get_market_context_csv_path,
)
from src.market_context import (
    calculate_market_context_enrichment_coverage,
    find_duplicate_market_context_keys,
    load_market_context_csv,
    merge_market_context,
)


Fetcher = Callable[[str], object]
_MARKET_CONTEXT_PATH_UNSET = object()


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
    market_context_csv_path: str | Path | None | object = _MARKET_CONTEXT_PATH_UNSET,
) -> pd.DataFrame:
    data, _metadata = load_players_data_with_metadata(
        database_path=database_path,
        table_name=table_name,
        external_url=external_url,
        csv_path=csv_path,
        priority=priority,
        fetcher=fetcher,
        market_context_csv_path=market_context_csv_path,
    )
    return data


def load_players_data_with_metadata(
    database_path: str | Path = DATABASE_PATH,
    table_name: str = PLAYERS_TABLE,
    external_url: str = EXTERNAL_PROVIDER_URL,
    csv_path: str | Path = SAMPLE_DATA_PATH,
    priority: tuple[str, ...] = DATA_SOURCE_PRIORITY,
    fetcher: Fetcher | None = None,
    market_context_csv_path: str | Path | None | object = _MARKET_CONTEXT_PATH_UNSET,
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
            base_metadata = {**metadata, "row_count": len(data)}
            return _apply_optional_market_context(
                data,
                base_metadata,
                market_context_csv_path=market_context_csv_path,
            )

    raise ValueError("No player data could be loaded from SQLite, external provider, or CSV fallback.")


def _apply_optional_market_context(
    data: pd.DataFrame,
    metadata: dict,
    market_context_csv_path: str | Path | None | object = _MARKET_CONTEXT_PATH_UNSET,
) -> tuple[pd.DataFrame, dict]:
    if market_context_csv_path is _MARKET_CONTEXT_PATH_UNSET:
        resolved_path = get_market_context_csv_path()
    elif market_context_csv_path is None:
        resolved_path = None
    else:
        resolved_path = get_market_context_csv_path(market_context_csv_path)

    if resolved_path is None:
        return data, metadata

    if not resolved_path.exists():
        return data, {
            **metadata,
            "market_context_enabled": False,
            "market_context_csv_path": str(resolved_path),
            "market_context_load_error": f"Market context CSV not found: {resolved_path}",
        }

    try:
        market_context, validation_errors = load_market_context_csv(resolved_path)
        enriched = merge_market_context(data, market_context)
        coverage = calculate_market_context_enrichment_coverage(enriched)
        duplicate_count = int(len(find_duplicate_market_context_keys(market_context)))
        enriched_metadata = {
            **metadata,
            "market_context_enabled": True,
            "market_context_csv_path": str(resolved_path),
            "market_context_validation_error_count": len(validation_errors),
            "market_context_duplicate_count": duplicate_count,
            "market_context_matched_count": coverage["matched_count"],
            "market_context_matched_pct": coverage["matched_pct"],
            "market_context_age_known_pct": coverage["age_known_pct"],
            "market_context_market_value_known_pct": coverage["market_value_known_pct"],
            "market_context_contract_known_pct": coverage["contract_known_pct"],
        }
        if validation_errors:
            enriched_metadata["market_context_validation_errors"] = validation_errors
        return enriched, enriched_metadata
    except Exception as exc:
        return data, {
            **metadata,
            "market_context_enabled": False,
            "market_context_csv_path": str(resolved_path),
            "market_context_load_error": str(exc),
        }
