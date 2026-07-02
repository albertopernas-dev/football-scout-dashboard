from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.api_football_fixture_aggregation import aggregate_fixture_player_payloads


DEFAULT_OUTPUT_PATH = Path("data/raw/api_football_fixture_players_aggregated.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Aggregate local API-Football fixtures/players payloads by player and team."
    )
    parser.add_argument("--input", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    return parser


def load_payload(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Input file not found: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Input file is not valid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"Input JSON must be an object: {path}")
    return payload


def save_json(payload: list[dict[str, object]], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    args = build_parser().parse_args()
    payloads = [load_payload(path) for path in args.input]
    aggregated = aggregate_fixture_player_payloads(payloads)
    output_path = save_json(aggregated, args.output)

    print(f"Input files: {len(args.input)}")
    print(f"Aggregated players: {len(aggregated)}")
    print(f"Output path: {output_path}")
    print("Preview:")
    print(json.dumps(aggregated[:10], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
