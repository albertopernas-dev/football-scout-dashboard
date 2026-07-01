from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


DEFAULT_INPUT_PATH = Path("data/raw/api_football_players_raw.json")
CANONICAL_FIELDS = [
    "player",
    "age",
    "team",
    "league",
    "season",
    "position",
    "minutes",
    "goals",
    "assists",
    "shots",
    "key_passes",
    "duels_won",
    "interceptions",
]
METRIC_PREVIEW_FIELDS = [
    "player",
    "team",
    "position",
    "minutes",
    "goals",
    "assists",
    "shots",
    "key_passes",
    "duels_won",
    "interceptions",
]
ACTIVITY_FIELDS = ["shots", "key_passes", "duels_won", "goals", "assists", "interceptions"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect a raw API-Football players payload saved locally."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_PATH)
    return parser


def load_payload(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Payload file not found: {path}")

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Payload file is not valid JSON: {path}") from exc

    if not isinstance(payload, dict):
        raise SystemExit("Payload JSON must be an object.")

    return payload


def count_response_records(payload: dict) -> int:
    response = payload.get("response")
    if isinstance(response, list):
        return len(response)
    return 0


def extract_top_level_keys(payload: dict) -> list[str]:
    return sorted(str(key) for key in payload.keys())


def extract_response_item_keys(payload: dict) -> dict[str, list[str]]:
    item = _first_response_item(payload)
    if not item:
        return {}

    keys = {"item": sorted(str(key) for key in item.keys())}
    player = item.get("player")
    if isinstance(player, dict):
        keys["player"] = sorted(str(key) for key in player.keys())

    stats = _first_statistics_item(item)
    if stats:
        keys["statistics_0"] = sorted(str(key) for key in stats.keys())

    return keys


def count_statistics_entries(payload: dict) -> dict[str, int | float]:
    response = payload.get("response")
    if not isinstance(response, list):
        return {
            "players": 0,
            "total_statistics_entries": 0,
            "players_with_multiple_statistics": 0,
            "avg_statistics_per_player": 0.0,
        }

    players = len(response)
    total_statistics_entries = 0
    players_with_multiple_statistics = 0
    for item in response:
        statistics = item.get("statistics") if isinstance(item, dict) else None
        entry_count = len(statistics) if isinstance(statistics, list) else 0
        total_statistics_entries += entry_count
        if entry_count > 1:
            players_with_multiple_statistics += 1

    avg_statistics_per_player = round(total_statistics_entries / players, 2) if players else 0.0
    return {
        "players": players,
        "total_statistics_entries": total_statistics_entries,
        "players_with_multiple_statistics": players_with_multiple_statistics,
        "avg_statistics_per_player": avg_statistics_per_player,
    }


def extract_statistics_contexts(payload: dict) -> list[dict[str, object]]:
    response = payload.get("response")
    if not isinstance(response, list):
        return []

    contexts = []
    for item in response:
        if not isinstance(item, dict):
            continue
        player_name = _nested_get(item, ("player", "name"))
        for stat_index, stats in enumerate(_statistics_items(item)):
            contexts.append(
                {
                    "player": player_name,
                    "stat_index": stat_index,
                    "team": _nested_get(stats, ("team", "name")),
                    "league": _nested_get(stats, ("league", "name")),
                    "season": _nested_get(stats, ("league", "season")),
                    "position": _nested_get(stats, ("games", "position")),
                    "has_minutes": _nested_get(stats, ("games", "minutes")) is not None,
                    "has_goals": _nested_get(stats, ("goals", "total")) is not None,
                    "has_assists": _nested_get(stats, ("goals", "assists")) is not None,
                    "has_shots": _nested_get(stats, ("shots", "total")) is not None,
                    "has_key_passes": _nested_get(stats, ("passes", "key")) is not None,
                    "has_duels_won": _nested_get(stats, ("duels", "won")) is not None,
                    "has_interceptions": _nested_get(stats, ("tackles", "interceptions")) is not None,
                }
            )
    return contexts


def extract_api_football_sample_mapping(payload: dict) -> dict[str, object]:
    item = _first_response_item(payload)
    if not item:
        return {}

    return map_api_football_item_with_strategy(item)


def extract_api_football_mappings(payload: dict, strategy: str = "first") -> list[dict[str, object]]:
    response = payload.get("response")
    if not isinstance(response, list):
        return []

    return [map_api_football_item_with_strategy(item, strategy=strategy) for item in response if isinstance(item, dict)]


def calculate_mapping_coverage(mappings: list[dict[str, object]]) -> dict[str, dict[str, int | float]]:
    if not mappings:
        return {}

    total = len(mappings)
    coverage = {}
    for field in CANONICAL_FIELDS:
        present = sum(1 for mapping in mappings if field in mapping and mapping[field] is not None)
        coverage[field] = {
            "present": present,
            "total": total,
            "coverage_pct": round((present / total) * 100, 1),
        }
    return coverage


def find_richest_mapping(mappings: list[dict[str, object]]) -> dict[str, object]:
    if not mappings:
        return {}
    return max(mappings, key=lambda mapping: sum(1 for value in mapping.values() if value is not None))


def extract_metric_preview_rows(
    mappings: list[dict[str, object]],
    limit: int = 20,
) -> list[dict[str, object]]:
    return [
        {field: mapping.get(field) for field in METRIC_PREVIEW_FIELDS}
        for mapping in mappings[:limit]
    ]


def detect_metric_anomalies(
    mappings: list[dict[str, object]],
) -> list[dict[str, object]]:
    anomalies = []
    for mapping in mappings:
        player = mapping.get("player")
        team = mapping.get("team")
        minutes = mapping.get("minutes")
        positive_activity_fields = [
            field for field in ACTIVITY_FIELDS if _is_positive_number(mapping.get(field))
        ]

        if minutes == 0 and positive_activity_fields:
            anomalies.append(
                {
                    "player": player,
                    "team": team,
                    "type": "minutes_zero_with_activity",
                    "details": f"minutes is 0 but positive activity exists: {', '.join(positive_activity_fields)}",
                }
            )
        if minutes is None and positive_activity_fields:
            anomalies.append(
                {
                    "player": player,
                    "team": team,
                    "type": "minutes_missing_with_activity",
                    "details": f"minutes is missing but positive activity exists: {', '.join(positive_activity_fields)}",
                }
            )
        if _is_positive_number(mapping.get("goals")) and (minutes is None or minutes == 0):
            anomalies.append(
                {
                    "player": player,
                    "team": team,
                    "type": "goals_without_minutes",
                    "details": "goals is positive while minutes is missing or 0",
                }
            )
        if _is_positive_number(mapping.get("assists")) and (minutes is None or minutes == 0):
            anomalies.append(
                {
                    "player": player,
                    "team": team,
                    "type": "assists_without_minutes",
                    "details": "assists is positive while minutes is missing or 0",
                }
            )
    return anomalies


def compare_mapping_strategies(payload: dict) -> dict[str, dict[str, dict[str, int | float]]]:
    return {
        strategy: calculate_mapping_coverage(extract_api_football_mappings(payload, strategy=strategy))
        for strategy in ("first", "richest", "prefer_minutes")
    }


def map_api_football_item_with_strategy(item: dict, strategy: str = "first") -> dict[str, object]:
    statistics = _statistics_items(item)
    if strategy == "first":
        stats = statistics[0] if statistics else {}
        return _map_api_football_item_with_stats(item, stats)

    if strategy == "richest":
        return _richest_mapping_for_statistics(item, statistics)

    if strategy == "prefer_minutes":
        stats_with_minutes = [
            stats for stats in statistics if _nested_get(stats, ("games", "minutes")) is not None
        ]
        if stats_with_minutes:
            return _richest_mapping_for_statistics(item, stats_with_minutes)
        return _richest_mapping_for_statistics(item, statistics)

    raise ValueError(f"Unsupported API-Football mapping strategy: {strategy}")


def _richest_mapping_for_statistics(item: dict, statistics: list[dict[str, Any]]) -> dict[str, object]:
    if not statistics:
        return _map_api_football_item_with_stats(item, {})
    mappings = [_map_api_football_item_with_stats(item, stats) for stats in statistics]
    return find_richest_mapping(mappings)


def _map_api_football_item_with_stats(item: dict, stats: dict) -> dict[str, object]:
    row = {
        "player": _nested_get(item, ("player", "name")),
        "age": _nested_get(item, ("player", "age")),
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
    return {key: value for key, value in row.items() if value is not None}


def _first_response_item(payload: dict) -> dict[str, Any]:
    response = payload.get("response")
    if not isinstance(response, list) or not response:
        return {}
    first = response[0]
    return first if isinstance(first, dict) else {}


def _first_statistics_item(item: dict) -> dict[str, Any]:
    statistics = _statistics_items(item)
    return statistics[0] if statistics else {}


def _statistics_items(item: dict) -> list[dict[str, Any]]:
    statistics = item.get("statistics")
    if not isinstance(statistics, list) or not statistics:
        return []
    return [entry for entry in statistics if isinstance(entry, dict)]


def _nested_get(record: dict, path: tuple[str, ...]) -> Any:
    value: Any = record
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def _is_positive_number(value: object) -> bool:
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def main() -> None:
    args = build_parser().parse_args()
    payload = load_payload(args.input)
    item_keys = extract_response_item_keys(payload)
    sample_mapping = extract_api_football_sample_mapping(payload)
    mappings = extract_api_football_mappings(payload)
    coverage = calculate_mapping_coverage(mappings)
    richest_mapping = find_richest_mapping(mappings)
    statistics_summary = count_statistics_entries(payload)
    strategy_comparison = compare_mapping_strategies(payload)
    statistics_contexts = extract_statistics_contexts(payload)
    preview_mappings = extract_api_football_mappings(payload, strategy="first")
    metric_preview_rows = extract_metric_preview_rows(preview_mappings)
    metric_anomalies = detect_metric_anomalies(preview_mappings)

    print(f"Input path: {args.input}")
    print(f"Top-level keys: {extract_top_level_keys(payload)}")
    print(f"Response records: {count_response_records(payload)}")
    print(f"First response item keys: {item_keys.get('item', [])}")
    print(f"Player keys: {item_keys.get('player', [])}")
    print(f"Statistics[0] keys: {item_keys.get('statistics_0', [])}")
    print("Sample canonical mapping (first response item):")
    print(json.dumps(sample_mapping, indent=2, ensure_ascii=False))
    print("Canonical field coverage:")
    for field in CANONICAL_FIELDS:
        field_coverage = coverage.get(field)
        if field_coverage:
            print(
                f"- {field}: {field_coverage['present']}/{field_coverage['total']} "
                f"({field_coverage['coverage_pct']}%)"
            )
    print("Richest canonical mapping:")
    print(json.dumps(richest_mapping, indent=2, ensure_ascii=False))
    print("Statistics summary:")
    print(f"- Players: {statistics_summary['players']}")
    print(f"- Total statistics entries: {statistics_summary['total_statistics_entries']}")
    print(f"- Players with multiple statistics: {statistics_summary['players_with_multiple_statistics']}")
    print(f"- Avg statistics per player: {statistics_summary['avg_statistics_per_player']}")
    print("Strategy coverage comparison:")
    for strategy, strategy_coverage in strategy_comparison.items():
        print(f"{strategy}:")
        for field in CANONICAL_FIELDS:
            field_coverage = strategy_coverage.get(field)
            if field_coverage:
                print(
                    f"- {field}: {field_coverage['present']}/{field_coverage['total']} "
                    f"({field_coverage['coverage_pct']}%)"
                )
    print("Statistics contexts examples:")
    print(json.dumps(statistics_contexts[:5], indent=2, ensure_ascii=False))
    print("Metric preview rows:")
    print(json.dumps(metric_preview_rows, indent=2, ensure_ascii=False))
    print("Metric anomalies:")
    print(json.dumps(metric_anomalies[:20], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
