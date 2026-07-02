from __future__ import annotations

from collections import Counter
from typing import Any


SUM_FIELDS = [
    "goals",
    "assists",
    "shots",
    "shots_on",
    "saves",
    "goals_conceded",
    "passes",
    "key_passes",
    "tackles",
    "blocks",
    "interceptions",
    "duels",
    "duels_won",
    "dribbles_attempts",
    "dribbles_success",
    "fouls_drawn",
    "fouls_committed",
    "yellow_cards",
    "red_cards",
]
PER90_FIELDS = {
    "goals": "goals_per90",
    "assists": "assists_per90",
    "shots": "shots_per90",
    "shots_on": "shots_on_per90",
    "passes": "passes_per90",
    "key_passes": "key_passes_per90",
    "tackles": "tackles_per90",
    "interceptions": "interceptions_per90",
    "duels_won": "duels_won_per90",
    "dribbles_success": "dribbles_success_per90",
    "fouls_drawn": "fouls_drawn_per90",
    "fouls_committed": "fouls_committed_per90",
}


def flatten_fixture_players_payload(payload: dict) -> list[dict[str, object]]:
    response = payload.get("response")
    if not isinstance(response, list):
        return []

    fixture_id = _nested_get(payload, ("parameters", "fixture"))
    rows = []
    for team_item in response:
        if not isinstance(team_item, dict):
            continue
        team_id = _nested_get(team_item, ("team", "id"))
        team_name = _nested_get(team_item, ("team", "name"))
        players = team_item.get("players")
        if not isinstance(players, list):
            continue
        for player_item in players:
            if not isinstance(player_item, dict):
                continue
            stats = _first_statistics_item(player_item)
            rows.append(
                {
                    "fixture_id": fixture_id,
                    "team_id": team_id,
                    "team": team_name,
                    "player_id": _nested_get(player_item, ("player", "id")),
                    "player": _nested_get(player_item, ("player", "name")),
                    "photo": _nested_get(player_item, ("player", "photo")),
                    "minutes": _nested_get(stats, ("games", "minutes")),
                    "position": _nested_get(stats, ("games", "position")),
                    "rating": _nested_get(stats, ("games", "rating")),
                    "substitute": _nested_get(stats, ("games", "substitute")),
                    "captain": _nested_get(stats, ("games", "captain")),
                    "shots": _nested_get(stats, ("shots", "total")),
                    "shots_on": _nested_get(stats, ("shots", "on")),
                    "goals": _nested_get(stats, ("goals", "total")),
                    "assists": _nested_get(stats, ("goals", "assists")),
                    "saves": _nested_get(stats, ("goals", "saves")),
                    "goals_conceded": _nested_get(stats, ("goals", "conceded")),
                    "passes": _nested_get(stats, ("passes", "total")),
                    "key_passes": _nested_get(stats, ("passes", "key")),
                    "pass_accuracy": _nested_get(stats, ("passes", "accuracy")),
                    "tackles": _nested_get(stats, ("tackles", "total")),
                    "blocks": _nested_get(stats, ("tackles", "blocks")),
                    "interceptions": _nested_get(stats, ("tackles", "interceptions")),
                    "duels": _nested_get(stats, ("duels", "total")),
                    "duels_won": _nested_get(stats, ("duels", "won")),
                    "dribbles_attempts": _nested_get(stats, ("dribbles", "attempts")),
                    "dribbles_success": _nested_get(stats, ("dribbles", "success")),
                    "fouls_drawn": _nested_get(stats, ("fouls", "drawn")),
                    "fouls_committed": _nested_get(stats, ("fouls", "committed")),
                    "yellow_cards": _nested_get(stats, ("cards", "yellow")),
                    "red_cards": _nested_get(stats, ("cards", "red")),
                }
            )
    return rows


def flatten_fixture_players_payloads(payloads: list[dict]) -> list[dict[str, object]]:
    rows = []
    for payload in payloads:
        rows.extend(flatten_fixture_players_payload(payload))
    return rows


def filter_active_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row for row in rows if _to_float(row.get("minutes")) and _to_float(row.get("minutes")) > 0]


def aggregate_player_fixture_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    groups: dict[tuple[object, object], list[dict[str, object]]] = {}
    for row in filter_active_rows(rows):
        key = (row.get("player_id"), row.get("team_id"))
        groups.setdefault(key, []).append(row)

    aggregated = []
    for (_player_id, _team_id), group_rows in groups.items():
        first = group_rows[0]
        minutes = sum(_number_or_zero(row.get("minutes")) for row in group_rows)
        row = {
            "player_id": first.get("player_id"),
            "player": first.get("player"),
            "team_id": first.get("team_id"),
            "team": first.get("team"),
            "photo": first.get("photo"),
            "position": _most_common_position(group_rows),
            "appearances": len(group_rows),
            "starts": sum(1 for source in group_rows if source.get("substitute") is False),
            "minutes": minutes,
        }
        for field in SUM_FIELDS:
            row[field] = sum(_number_or_zero(source.get(field)) for source in group_rows)
        row["rating_avg"] = _weighted_average(group_rows, value_field="rating", weight_field="minutes")
        row["pass_accuracy_avg"] = _weighted_average(group_rows, value_field="pass_accuracy", weight_field="passes")
        aggregated.append(row)
    return aggregated


def add_per90_metrics(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    enriched = []
    for row in rows:
        copied = dict(row)
        minutes = _to_float(copied.get("minutes"))
        for source_field, target_field in PER90_FIELDS.items():
            if minutes is None or minutes <= 0:
                copied[target_field] = None
            else:
                copied[target_field] = round((_number_or_zero(copied.get(source_field)) / minutes) * 90, 3)
        enriched.append(copied)
    return enriched


def aggregate_fixture_player_payloads(payloads: list[dict]) -> list[dict[str, object]]:
    rows = flatten_fixture_players_payloads(payloads)
    aggregated = aggregate_player_fixture_rows(rows)
    return add_per90_metrics(aggregated)


def _first_statistics_item(player_item: dict) -> dict[str, Any]:
    statistics = player_item.get("statistics")
    if not isinstance(statistics, list) or not statistics:
        return {}
    first = statistics[0]
    return first if isinstance(first, dict) else {}


def _nested_get(record: dict, path: tuple[str, ...]) -> Any:
    value: Any = record
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def _most_common_position(rows: list[dict[str, object]]) -> object:
    positions = [row.get("position") for row in rows if row.get("position") is not None]
    if not positions:
        return None
    counts = Counter(positions)
    return max(positions, key=lambda position: counts[position])


def _weighted_average(rows: list[dict[str, object]], value_field: str, weight_field: str) -> float | None:
    weighted_total = 0.0
    weight_total = 0.0
    for row in rows:
        value = _to_float(row.get(value_field))
        weight = _to_float(row.get(weight_field))
        if value is None or weight is None or weight <= 0:
            continue
        weighted_total += value * weight
        weight_total += weight
    if weight_total <= 0:
        return None
    return round(weighted_total / weight_total, 3)


def _number_or_zero(value: object) -> float:
    parsed = _to_float(value)
    return parsed if parsed is not None else 0.0


def _to_float(value: object) -> float | None:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        if value.endswith("%"):
            value = value[:-1]
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
