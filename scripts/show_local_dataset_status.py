from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.fetch_api_football_fixture_players_batch import (
    extract_fixture_ids,
    load_fixtures_payload,
    output_path_for_fixture,
)
from src.config import DATABASE_PATH, PLAYERS_TABLE
from src.data_quality import calculate_data_quality_metrics
from src.data_sources import load_players_from_sqlite


DEFAULT_FIXTURE_PLAYERS_DIR = Path("data/raw/fixture_players")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Show local dataset status for API-Football fixture player cache and SQLite."
    )
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--fixture-players-dir", type=Path, default=DEFAULT_FIXTURE_PLAYERS_DIR)
    parser.add_argument("--database", type=Path, default=DATABASE_PATH)
    parser.add_argument("--table", default=PLAYERS_TABLE)
    parser.add_argument("--league")
    parser.add_argument("--season")
    return parser


def calculate_local_dataset_status(
    fixtures_path: Path,
    fixture_players_dir: Path,
    database_path: Path,
    table_name: str,
    league: object | None = None,
    season: object | None = None,
) -> dict[str, object]:
    payload = load_fixtures_payload(fixtures_path)
    fixture_ids = extract_fixture_ids(payload)
    cached_fixture_ids = [
        fixture_id for fixture_id in fixture_ids if output_path_for_fixture(fixture_players_dir, fixture_id).exists()
    ]
    missing_fixture_ids = [fixture_id for fixture_id in fixture_ids if fixture_id not in set(cached_fixture_ids)]
    sqlite_data = load_players_from_sqlite(database_path, table_name)
    quality = calculate_data_quality_metrics(sqlite_data)
    source = "sqlite" if Path(database_path).exists() and not sqlite_data.empty else "missing"

    return {
        "league": league,
        "season": season,
        "fixtures_path": fixtures_path,
        "fixtures_in_fixtures_file": len(fixture_ids),
        "fixture_players_dir": fixture_players_dir,
        "cached_fixture_player_files": len(cached_fixture_ids),
        "missing_fixture_player_files": len(missing_fixture_ids),
        "cached_pct": _pct(len(cached_fixture_ids), len(fixture_ids)),
        "cached_fixture_ids": cached_fixture_ids,
        "missing_fixture_ids": missing_fixture_ids,
        "sqlite_source": source,
        "sqlite_path": Path(database_path),
        "sqlite_table": table_name,
        "sqlite_rows": quality["players_count"],
        "teams_count": quality["teams_count"],
        "leagues_count": quality["leagues_count"],
        "total_minutes": quality["total_minutes"],
        "age_known_pct": quality["age_known_pct"],
        "market_value_known_pct": quality["market_value_known_pct"],
        "contract_known_pct": quality["contract_known_pct"],
    }


def main() -> None:
    args = build_parser().parse_args()
    status = calculate_local_dataset_status(
        fixtures_path=args.fixtures,
        fixture_players_dir=args.fixture_players_dir,
        database_path=args.database,
        table_name=args.table,
        league=args.league,
        season=args.season,
    )
    print_status(status)


def print_status(status: dict[str, object]) -> None:
    if status.get("league") is not None:
        print(f"League: {status['league']}")
    if status.get("season") is not None:
        print(f"Season: {status['season']}")
    print(f"Fixtures file: {status['fixtures_path']}")
    print(f"Fixtures in fixtures file: {status['fixtures_in_fixtures_file']}")
    print(f"Fixture players dir: {status['fixture_players_dir']}")
    print(f"Cached fixture player files: {status['cached_fixture_player_files']}")
    print(f"Missing fixture player files: {status['missing_fixture_player_files']}")
    print(f"Cached pct: {status['cached_pct']}%")
    print(f"SQLite source: {status['sqlite_source']}")
    print(f"SQLite path: {status['sqlite_path']}")
    print(f"SQLite table: {status['sqlite_table']}")
    print(f"SQLite rows: {status['sqlite_rows']}")
    print(f"Teams: {status['teams_count']}")
    print(f"Leagues: {status['leagues_count']}")
    print(f"Total minutes: {status['total_minutes']}")
    print(f"Age known pct: {status['age_known_pct']}%")
    print(f"Market value known pct: {status['market_value_known_pct']}%")
    print(f"Contract known pct: {status['contract_known_pct']}%")


def _pct(count: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((count / total) * 100, 1)


if __name__ == "__main__":
    main()
