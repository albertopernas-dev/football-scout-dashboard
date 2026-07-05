from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.build_api_football_sqlite_from_fixture_players import (
    build_sqlite_from_fixture_players,
    resolve_input_paths,
)
from scripts.fetch_api_football_fixture_players_batch import (
    _DryRunClient,
    _print_summary as _print_fetch_summary,
    extract_fixture_ids,
    fetch_fixture_players_batch,
    load_fixtures_payload,
)
from scripts.show_local_dataset_status import calculate_local_dataset_status, print_status
from src.config import API_FOOTBALL_BASE_URL, API_FOOTBALL_KEY, API_FOOTBALL_TIMEOUT_SECONDS, DATABASE_PATH, PLAYERS_TABLE
from src.providers.api_football import ApiFootballClient


DEFAULT_FIXTURE_PLAYERS_DIR = Path("data/raw/fixture_players")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Refresh local API-Football fixture player cache, SQLite and dataset status."
    )
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--fixture-players-dir", type=Path, default=DEFAULT_FIXTURE_PLAYERS_DIR)
    parser.add_argument("--database", type=Path, default=DATABASE_PATH)
    parser.add_argument("--table", default=PLAYERS_TABLE)
    parser.add_argument("--league")
    parser.add_argument("--season")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--delay-seconds", type=float, default=0.0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-build", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    return parser


def refresh_local_dataset(
    fixtures_path: Path,
    fixture_players_dir: Path,
    database_path: Path,
    table_name: str,
    league: object | None = None,
    season: object | None = None,
    limit: int = 0,
    delay_seconds: float = 0.0,
    dry_run: bool = False,
    skip_build: bool = False,
    force: bool = False,
    continue_on_error: bool = False,
) -> dict[str, object]:
    print("=== Fetch ===")
    fetch_summary = None
    if limit > 0:
        payload = load_fixtures_payload(fixtures_path)
        fixture_ids = extract_fixture_ids(payload)
        client = _build_fetch_client(dry_run=dry_run)
        fetch_summary = fetch_fixture_players_batch(
            fixture_ids=fixture_ids,
            output_dir=fixture_players_dir,
            limit=limit,
            client=client,
            force=force,
            dry_run=dry_run,
            continue_on_error=continue_on_error,
            delay_seconds=delay_seconds,
        )
        _print_fetch_summary(fetch_summary)
    else:
        print("Fetch skipped.")

    stopped_early = bool(fetch_summary and fetch_summary.get("stopped_early"))

    print("=== Build SQLite ===")
    build_summary = None
    if dry_run:
        print("Dry run: true")
        print("No SQLite build performed.")
    elif skip_build:
        print("SQLite build skipped.")
    elif stopped_early:
        print("Fetch stopped early; SQLite build skipped.")
    else:
        input_paths = resolve_input_paths(
            None,
            str(fixture_players_dir / "api_football_fixture_players_*.json"),
        )
        build_summary = build_sqlite_from_fixture_players(
            input_paths=input_paths,
            database_path=database_path,
            table_name=table_name,
            league=league,
            season=season,
        )
        print(f"Input files: {build_summary['input_files']}")
        print(f"Aggregated players: {build_summary['aggregated_players']}")
        print(f"Canonical records: {build_summary['canonical_records']}")
        print(f"Database path: {build_summary['database_path']}")
        print(f"Table: {build_summary['table']}")
        print(f"Rows loaded: {build_summary['rows_loaded']}")

    print("=== Dataset status ===")
    status = calculate_local_dataset_status(
        fixtures_path=fixtures_path,
        fixture_players_dir=fixture_players_dir,
        database_path=database_path,
        table_name=table_name,
        league=league,
        season=season,
    )
    print_status(status)

    return {
        "fetch_executed": limit > 0,
        "fetch_summary": fetch_summary,
        "build_executed": build_summary is not None,
        "build_summary": build_summary,
        "status": status,
    }


def main() -> None:
    args = build_parser().parse_args()
    refresh_local_dataset(
        fixtures_path=args.fixtures,
        fixture_players_dir=args.fixture_players_dir,
        database_path=args.database,
        table_name=args.table,
        league=args.league,
        season=args.season,
        limit=args.limit,
        delay_seconds=args.delay_seconds,
        dry_run=args.dry_run,
        skip_build=args.skip_build,
        force=args.force,
        continue_on_error=args.continue_on_error,
    )


def _build_fetch_client(dry_run: bool):
    if dry_run:
        return _DryRunClient()
    if not API_FOOTBALL_KEY:
        raise SystemExit("API_FOOTBALL_KEY is not defined. Set it before fetching API-Football data.")
    return ApiFootballClient(
        api_key=API_FOOTBALL_KEY,
        base_url=API_FOOTBALL_BASE_URL,
        timeout_seconds=API_FOOTBALL_TIMEOUT_SECONDS,
    )


if __name__ == "__main__":
    main()
