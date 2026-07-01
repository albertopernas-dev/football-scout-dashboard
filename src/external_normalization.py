from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import pandas as pd

from src.schema import normalize_columns


def _extract_records(records: object) -> list[dict[str, Any]]:
    if records is None:
        return []
    if isinstance(records, pd.DataFrame):
        return records.to_dict("records")
    if isinstance(records, dict):
        if isinstance(records.get("players"), list):
            return [record for record in records["players"] if isinstance(record, dict)]
        if isinstance(records.get("response"), list):
            return [record for record in records["response"] if isinstance(record, dict)]
        return [records]
    if isinstance(records, Iterable) and not isinstance(records, (str, bytes)):
        return [record for record in records if isinstance(record, dict)]
    return []


def _nested_get(record: dict[str, Any], path: tuple[str, ...]) -> Any:
    value: Any = record
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def _normalize_generic(records: object) -> pd.DataFrame:
    extracted = _extract_records(records)
    if not extracted:
        return pd.DataFrame()
    return normalize_columns(pd.DataFrame(extracted))


def _normalize_api_football(records: object) -> pd.DataFrame:
    extracted = _extract_records(records)
    normalized = []
    for record in extracted:
        statistics = record.get("statistics") or []
        stats = statistics[0] if statistics and isinstance(statistics[0], dict) else {}
        # TODO: aggregate multiple statistics entries by season/team when the product needs it.
        row = {
            "player": _nested_get(record, ("player", "name")),
            "age": _nested_get(record, ("player", "age")),
            "team": _nested_get(stats, ("team", "name")),
            "league": _nested_get(stats, ("league", "name")),
            "season": _nested_get(stats, ("league", "season")),
            "position": _nested_get(stats, ("games", "position")),
            "minutes": _nested_get(stats, ("games", "minutes")),
            "goals": _nested_get(stats, ("goals", "total")),
            "assists": _nested_get(stats, ("goals", "assists")),
            "shots": _nested_get(stats, ("shots", "total")),
            "key_passes": _nested_get(stats, ("passes", "key")),
            "duels_won": _nested_get(stats, ("duels", "won")),
            "interceptions": _nested_get(stats, ("tackles", "interceptions")),
        }
        normalized.append({key: value for key, value in row.items() if value is not None})
    if not normalized:
        return pd.DataFrame()
    return pd.DataFrame(normalized)


def normalize_external_players(records: object, provider: str = "generic") -> pd.DataFrame:
    if provider == "api_football":
        return _normalize_api_football(records)
    return _normalize_generic(records)
