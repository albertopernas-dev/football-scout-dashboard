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


def extract_api_football_sample_mapping(payload: dict) -> dict[str, object]:
    item = _first_response_item(payload)
    if not item:
        return {}

    stats = _first_statistics_item(item)
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
    statistics = item.get("statistics")
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


def main() -> None:
    args = build_parser().parse_args()
    payload = load_payload(args.input)
    item_keys = extract_response_item_keys(payload)
    sample_mapping = extract_api_football_sample_mapping(payload)

    print(f"Input path: {args.input}")
    print(f"Top-level keys: {extract_top_level_keys(payload)}")
    print(f"Response records: {count_response_records(payload)}")
    print(f"First response item keys: {item_keys.get('item', [])}")
    print(f"Player keys: {item_keys.get('player', [])}")
    print(f"Statistics[0] keys: {item_keys.get('statistics_0', [])}")
    print("Sample canonical mapping:")
    print(json.dumps(sample_mapping, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
