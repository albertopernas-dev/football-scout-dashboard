from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.api_football_canonical import normalize_api_football_aggregated_players


DEFAULT_OUTPUT_PATH = Path("data/raw/api_football_players_canonical.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Normalize aggregated API-Football fixture player records to the app canonical schema."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    return parser


def load_records(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        raise SystemExit(f"Input file not found: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Input file is not valid JSON: {path}") from exc
    if not isinstance(payload, list):
        raise SystemExit(f"Input JSON must be a list: {path}")
    return [record for record in payload if isinstance(record, dict)]


def save_json(records: list[dict[str, object]], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(records, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    args = build_parser().parse_args()
    records = load_records(args.input)
    normalized = normalize_api_football_aggregated_players(records)
    output_path = save_json(normalized, args.output)

    print(f"Input path: {args.input}")
    print(f"Output path: {output_path}")
    print(f"Input records: {len(records)}")
    print(f"Normalized records: {len(normalized)}")
    print("Preview:")
    print(json.dumps(normalized[:10], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
