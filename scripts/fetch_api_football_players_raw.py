from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import API_FOOTBALL_BASE_URL, API_FOOTBALL_KEY, API_FOOTBALL_TIMEOUT_SECONDS
from src.providers.api_football import ApiFootballClient


DEFAULT_OUTPUT_PATH = Path("data/raw/api_football_players_raw.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch raw API-Football players payload for local inspection."
    )
    parser.add_argument("--league-id", type=int, required=True)
    parser.add_argument("--season", type=int, required=True)
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    return parser


def count_response_records(payload: dict) -> int | None:
    response = payload.get("response")
    if isinstance(response, list):
        return len(response)
    return None


def save_json(payload: dict, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    args = build_parser().parse_args()

    if not API_FOOTBALL_KEY:
        raise SystemExit("API_FOOTBALL_KEY is not defined. Set it before fetching API-Football data.")

    client = ApiFootballClient(
        api_key=API_FOOTBALL_KEY,
        base_url=API_FOOTBALL_BASE_URL,
        timeout_seconds=API_FOOTBALL_TIMEOUT_SECONDS,
    )
    payload = client.fetch_players(
        league_id=args.league_id,
        season=args.season,
        page=args.page,
    )
    output_path = save_json(payload, args.output)
    response_count = count_response_records(payload)

    print(f"League ID: {args.league_id}")
    print(f"Season: {args.season}")
    print(f"Page: {args.page}")
    print(f"Output path: {output_path}")
    if response_count is not None:
        print(f"Response records: {response_count}")
    else:
        print("Response records: unknown")


if __name__ == "__main__":
    main()
