from __future__ import annotations

import json
from pathlib import Path


POSITION_MAP = {
    "G": "Goalkeeper",
    "D": "Defender",
    "M": "Midfielder",
    "F": "Forward",
}


def normalize_api_football_position(position: object) -> str | None:
    if position is None:
        return None
    return POSITION_MAP.get(str(position).strip().upper())


def normalize_api_football_aggregated_players(records: list[dict[str, object]]) -> list[dict[str, object]]:
    return [_normalize_record(record) for record in records if isinstance(record, dict)]


def normalize_api_football_aggregated_file(input_path: Path) -> list[dict[str, object]]:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Aggregated API-Football input must be a list of records.")
    return normalize_api_football_aggregated_players(payload)


def _normalize_record(record: dict[str, object]) -> dict[str, object]:
    return {
        "external_player_id": record.get("player_id"),
        "player": record.get("player"),
        "team": record.get("team"),
        "league": record.get("league"),
        "season": record.get("season"),
        "age": None,
        "position": normalize_api_football_position(record.get("position")),
        "minutes": _to_float(record.get("minutes")),
        "goals": _to_float(record.get("goals")),
        "assists": _to_float(record.get("assists")),
        "shots": _to_float(record.get("shots")),
        "key_passes": _to_float(record.get("key_passes")),
        "duels_won": _to_float(record.get("duels_won")),
        "interceptions": _to_float(record.get("interceptions")),
        "market_value": None,
        "contract_end": None,
        "source": "api_football_fixture_players",
        "photo": record.get("photo"),
        "team_id": record.get("team_id"),
        "appearances": _to_float(record.get("appearances")),
        "starts": _to_float(record.get("starts")),
        "tackles": _to_float(record.get("tackles")),
        "passes": _to_float(record.get("passes")),
        "rating_avg": _to_float(record.get("rating_avg")),
    }


def _to_float(value: object) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
