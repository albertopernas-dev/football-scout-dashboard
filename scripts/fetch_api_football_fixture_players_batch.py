from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import API_FOOTBALL_BASE_URL, API_FOOTBALL_KEY, API_FOOTBALL_TIMEOUT_SECONDS
from src.providers.api_football import ApiFootballClient


DEFAULT_OUTPUT_DIR = Path("data/raw/fixture_players")


class FixturePlayersClient(Protocol):
    def get(self, endpoint: str, params: dict | None = None) -> dict:
        ...


@dataclass(frozen=True)
class DownloadItem:
    fixture_id: int
    output_path: Path


@dataclass(frozen=True)
class DownloadPlan:
    found: int
    cached: list[DownloadItem]
    to_download: list[DownloadItem]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch API-Football fixtures/players payloads in batch from a local fixtures JSON."
    )
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--status", action="append", default=None)
    return parser


def load_fixtures_payload(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Fixtures file not found: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Fixtures file is not valid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise SystemExit("Fixtures JSON must be an object.")
    if not isinstance(payload.get("response"), list):
        raise SystemExit("Fixtures JSON must contain a response list.")
    return payload


def extract_fixture_ids(payload: dict, statuses: set[str] | None = None) -> list[int]:
    response = payload.get("response")
    if not isinstance(response, list):
        return []

    seen = set()
    fixture_ids = []
    for item in response:
        if not isinstance(item, dict):
            continue
        if statuses is not None:
            status = _nested_get(item, ("fixture", "status", "short"))
            if status not in statuses:
                continue
        fixture_id = _to_int(_nested_get(item, ("fixture", "id")))
        if fixture_id is None or fixture_id in seen:
            continue
        seen.add(fixture_id)
        fixture_ids.append(fixture_id)
    return fixture_ids


def output_path_for_fixture(output_dir: Path, fixture_id: int) -> Path:
    return output_dir / f"api_football_fixture_players_{fixture_id}.json"


def resolve_download_plan(
    fixture_ids: list[int],
    output_dir: Path,
    limit: int,
    force: bool = False,
) -> DownloadPlan:
    cached = []
    pending = []
    for fixture_id in fixture_ids:
        output_path = output_path_for_fixture(output_dir, fixture_id)
        item = DownloadItem(fixture_id=fixture_id, output_path=output_path)
        if output_path.exists() and not force:
            cached.append(item)
        else:
            pending.append(item)

    limited_pending = pending[: max(limit, 0)]
    return DownloadPlan(found=len(fixture_ids), cached=cached, to_download=limited_pending)


def save_json(payload: dict, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return output_path


def fetch_fixture_players_batch(
    fixture_ids: list[int],
    output_dir: Path,
    limit: int,
    client: FixturePlayersClient,
    force: bool = False,
    dry_run: bool = False,
) -> dict[str, object]:
    plan = resolve_download_plan(fixture_ids, output_dir, limit=limit, force=force)
    downloaded = 0

    if not dry_run:
        for item in plan.to_download:
            payload = client.get("fixtures/players", params={"fixture": item.fixture_id})
            save_json(payload, item.output_path)
            downloaded += 1

    return {
        "fixtures_found": plan.found,
        "already_cached": len(plan.cached),
        "planned_downloads": len(plan.to_download),
        "downloaded": downloaded,
        "skipped": len(plan.cached),
        "output_dir": output_dir,
        "dry_run": dry_run,
        "planned_fixture_ids": [item.fixture_id for item in plan.to_download],
        "cached_fixture_ids": [item.fixture_id for item in plan.cached],
    }


def main() -> None:
    args = build_parser().parse_args()
    statuses = _parse_statuses(args.status)
    payload = load_fixtures_payload(args.fixtures)
    fixture_ids = extract_fixture_ids(payload, statuses=statuses)

    if args.dry_run:
        client = _DryRunClient()
    else:
        if not API_FOOTBALL_KEY:
            raise SystemExit("API_FOOTBALL_KEY is not defined. Set it before fetching API-Football data.")
        client = ApiFootballClient(
            api_key=API_FOOTBALL_KEY,
            base_url=API_FOOTBALL_BASE_URL,
            timeout_seconds=API_FOOTBALL_TIMEOUT_SECONDS,
        )

    summary = fetch_fixture_players_batch(
        fixture_ids=fixture_ids,
        output_dir=args.output_dir,
        limit=args.limit,
        client=client,
        force=args.force,
        dry_run=args.dry_run,
    )
    _print_summary(summary)


def _parse_statuses(values: list[str] | None) -> set[str] | None:
    if not values:
        return None
    statuses = set()
    for value in values:
        statuses.update(part.strip() for part in value.split(",") if part.strip())
    return statuses or None


def _print_summary(summary: dict[str, object]) -> None:
    print(f"Fixtures found: {summary['fixtures_found']}")
    print(f"Already cached: {summary['already_cached']}")
    print(f"Planned downloads: {summary['planned_downloads']}")
    print(f"Downloaded: {summary['downloaded']}")
    print(f"Skipped: {summary['skipped']}")
    print(f"Output dir: {summary['output_dir']}")
    print(f"Dry run: {str(summary['dry_run']).lower()}")
    print(f"Planned fixture IDs: {summary['planned_fixture_ids']}")
    print(f"Cached fixture IDs: {summary['cached_fixture_ids']}")


def _nested_get(record: dict, path: tuple[str, ...]) -> object:
    value: object = record
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def _to_int(value: object) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


class _DryRunClient:
    def get(self, endpoint: str, params: dict | None = None) -> dict:
        raise RuntimeError("Dry-run should not call API-Football.")


if __name__ == "__main__":
    main()
