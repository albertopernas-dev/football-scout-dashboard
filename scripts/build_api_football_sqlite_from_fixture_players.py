from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.api_football_canonical import normalize_api_football_aggregated_players
from src.api_football_fixture_aggregation import aggregate_fixture_player_payloads
from src.config import DATABASE_PATH, PLAYERS_TABLE
from src.ingestion import load_records_to_sqlite


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build local SQLite players table from API-Football fixtures/players JSON files."
    )
    parser.add_argument("--input", type=Path, action="append")
    parser.add_argument("--input-glob")
    parser.add_argument("--database", type=Path, default=DATABASE_PATH)
    parser.add_argument("--table", default=PLAYERS_TABLE)
    parser.add_argument("--aggregated-output", type=Path)
    parser.add_argument("--canonical-output", type=Path)
    parser.add_argument("--league")
    parser.add_argument("--season", type=_parse_context_value)
    return parser


def resolve_input_paths(inputs: list[Path] | None, input_glob: str | None) -> list[Path]:
    paths: list[Path] = []
    if inputs:
        paths.extend(inputs)
    if input_glob:
        paths.extend(Path(match) for match in glob.glob(input_glob))

    resolved = sorted(dict.fromkeys(paths), key=lambda path: str(path))
    if not resolved:
        raise SystemExit("No input files resolved. Use --input or --input-glob.")
    for path in resolved:
        if not path.exists():
            raise SystemExit(f"Input file not found: {path}")
    return resolved


def load_payloads(input_paths: list[Path]) -> list[dict]:
    payloads = []
    for path in input_paths:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Input file is not valid JSON: {path}") from exc
        if not isinstance(payload, dict):
            raise SystemExit(f"Input JSON must be an object: {path}")
        payloads.append(payload)
    return payloads


def apply_context_defaults(
    records: list[dict[str, object]],
    league: object | None = None,
    season: object | None = None,
) -> list[dict[str, object]]:
    enriched = []
    for record in records:
        copied = dict(record)
        if league is not None and _is_empty(copied.get("league")):
            copied["league"] = league
        if season is not None and _is_empty(copied.get("season")):
            copied["season"] = season
        enriched.append(copied)
    return enriched


def save_json(records: list[dict[str, object]], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(records, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return output_path


def build_sqlite_from_fixture_players(
    input_paths: list[Path],
    database_path: str | Path,
    table_name: str,
    aggregated_output: Path | None = None,
    canonical_output: Path | None = None,
    league: object | None = None,
    season: object | None = None,
) -> dict[str, object]:
    payloads = load_payloads(input_paths)
    aggregated = aggregate_fixture_player_payloads(payloads)
    canonical = normalize_api_football_aggregated_players(aggregated)
    canonical = apply_context_defaults(canonical, league=league, season=season)

    if aggregated_output:
        save_json(aggregated, aggregated_output)
    if canonical_output:
        save_json(canonical, canonical_output)

    rows_loaded = load_records_to_sqlite(canonical, database_path, table_name)
    return {
        "input_files": len(input_paths),
        "aggregated_players": len(aggregated),
        "canonical_records": len(canonical),
        "database_path": Path(database_path),
        "table": table_name,
        "rows_loaded": rows_loaded,
        "aggregated_output": aggregated_output,
        "canonical_output": canonical_output,
    }


def main() -> None:
    args = build_parser().parse_args()
    input_paths = resolve_input_paths(args.input, args.input_glob)
    summary = build_sqlite_from_fixture_players(
        input_paths=input_paths,
        database_path=args.database,
        table_name=args.table,
        aggregated_output=args.aggregated_output,
        canonical_output=args.canonical_output,
        league=args.league,
        season=args.season,
    )

    print(f"Input files: {summary['input_files']}")
    print(f"Aggregated players: {summary['aggregated_players']}")
    print(f"Canonical records: {summary['canonical_records']}")
    print(f"Database path: {summary['database_path']}")
    print(f"Table: {summary['table']}")
    print(f"Rows loaded: {summary['rows_loaded']}")
    if summary["aggregated_output"]:
        print(f"Aggregated output: {summary['aggregated_output']}")
    if summary["canonical_output"]:
        print(f"Canonical output: {summary['canonical_output']}")


def _is_empty(value: object) -> bool:
    return value is None or value == ""


def _parse_context_value(value: str) -> object:
    stripped = value.strip()
    if stripped.isdigit():
        return int(stripped)
    return value


if __name__ == "__main__":
    main()
