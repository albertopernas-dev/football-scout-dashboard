from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


OUTPUT_FIELDS = [
    "fixture_id",
    "team_id",
    "team",
    "player_id",
    "player",
    "photo",
    "minutes",
    "number",
    "position",
    "rating",
    "substitute",
    "captain",
    "shots",
    "shots_on",
    "goals",
    "assists",
    "saves",
    "goals_conceded",
    "passes",
    "key_passes",
    "pass_accuracy",
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
ACTIVITY_FIELDS = [
    "shots",
    "goals",
    "assists",
    "passes",
    "tackles",
    "duels",
    "duels_won",
    "key_passes",
    "interceptions",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect a raw API-Football fixtures/players payload saved locally."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=20)
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


def flatten_fixture_players(payload: dict) -> list[dict[str, object]]:
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
            row = {
                "fixture_id": fixture_id,
                "team_id": team_id,
                "team": team_name,
                "player_id": _nested_get(player_item, ("player", "id")),
                "player": _nested_get(player_item, ("player", "name")),
                "photo": _nested_get(player_item, ("player", "photo")),
                "minutes": _nested_get(stats, ("games", "minutes")),
                "number": _nested_get(stats, ("games", "number")),
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
            rows.append(row)
    return rows


def calculate_field_coverage(rows: list[dict[str, object]]) -> dict[str, dict[str, int | float]]:
    if not rows:
        return {}

    total = len(rows)
    coverage = {}
    for field in OUTPUT_FIELDS:
        present = sum(1 for row in rows if row.get(field) is not None)
        coverage[field] = {
            "present": present,
            "total": total,
            "coverage_pct": round((present / total) * 100, 1),
        }
    return coverage


def extract_preview_rows(rows: list[dict[str, object]], limit: int = 20) -> list[dict[str, object]]:
    return rows[:limit]


def detect_fixture_player_anomalies(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    anomalies = []
    for row in rows:
        player = row.get("player")
        team = row.get("team")
        minutes = row.get("minutes")
        positive_activity_fields = [
            field for field in ACTIVITY_FIELDS if _is_positive_number(row.get(field))
        ]

        if minutes is None:
            anomalies.append(
                {
                    "player": player,
                    "team": team,
                    "type": "minutes_missing",
                    "details": "minutes is missing",
                }
            )
        if minutes == 0 and positive_activity_fields:
            anomalies.append(
                {
                    "player": player,
                    "team": team,
                    "type": "minutes_zero_with_activity",
                    "details": f"minutes is 0 but positive activity exists: {', '.join(positive_activity_fields)}",
                }
            )
        if _is_positive_number(minutes) and row.get("rating") is None:
            anomalies.append(
                {
                    "player": player,
                    "team": team,
                    "type": "rating_missing_with_minutes",
                    "details": "rating is missing while minutes is positive",
                }
            )
        if row.get("pass_accuracy") is not None and not _is_positive_number(row.get("passes")):
            anomalies.append(
                {
                    "player": player,
                    "team": team,
                    "type": "pass_accuracy_without_passes",
                    "details": "pass_accuracy is present while passes is missing or 0",
                }
            )
    return anomalies


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


def _is_positive_number(value: object) -> bool:
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def main() -> None:
    args = build_parser().parse_args()
    payload = load_payload(args.input)
    rows = flatten_fixture_players(payload)
    coverage = calculate_field_coverage(rows)
    anomalies = detect_fixture_player_anomalies(rows)
    teams = sorted({row["team"] for row in rows if row.get("team") is not None})

    print(f"Input path: {args.input}")
    print(f"Fixture ID: {_nested_get(payload, ('parameters', 'fixture'))}")
    print(f"Teams: {teams}")
    print(f"Rows: {len(rows)}")
    print("Field coverage:")
    for field in OUTPUT_FIELDS:
        field_coverage = coverage.get(field)
        if field_coverage:
            print(
                f"- {field}: {field_coverage['present']}/{field_coverage['total']} "
                f"({field_coverage['coverage_pct']}%)"
            )
    print("Preview rows:")
    print(json.dumps(extract_preview_rows(rows, limit=args.limit), indent=2, ensure_ascii=False))
    print("Anomalies:")
    print(json.dumps(anomalies[:20], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
