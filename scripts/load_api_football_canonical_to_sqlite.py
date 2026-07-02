from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import DATABASE_PATH, PLAYERS_TABLE
from src.ingestion import load_records_to_sqlite


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Load canonical API-Football player records into local SQLite."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--database", type=Path, default=DATABASE_PATH)
    parser.add_argument("--table", default=PLAYERS_TABLE)
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
    if any(not isinstance(record, dict) for record in payload):
        raise SystemExit("All records must be JSON objects.")
    return payload


def main() -> None:
    args = build_parser().parse_args()
    records = load_records(args.input)
    row_count = load_records_to_sqlite(records, args.database, args.table)

    print(f"Input path: {args.input}")
    print(f"Database path: {args.database}")
    print(f"Table: {args.table}")
    print(f"Rows loaded: {row_count}")


if __name__ == "__main__":
    main()
