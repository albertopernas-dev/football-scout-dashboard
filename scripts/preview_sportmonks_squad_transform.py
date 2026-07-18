from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.providers.sportmonks.transform import (  # noqa: E402
    summarize_transformed_rows,
    transform_squad_payload,
)
from src.providers.sportmonks.validation import (  # noqa: E402
    SportmonksValidationError,
    validate_safe_input_path,
)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Preview a local Sportmonks squad transform without network access.",
    )
    parser.add_argument("--input", required=True, help="Explicit local JSON input path.")
    parser.add_argument("--league-id", required=True, type=int)
    parser.add_argument("--team-id", required=True, type=int)
    parser.add_argument("--season-id", required=True, type=int)
    parser.add_argument("--observed-at")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    try:
        input_path = validate_safe_input_path(Path(args.input))
        with input_path.open("r", encoding="utf-8") as input_file:
            payload = json.load(input_file)
        rows = transform_squad_payload(
            payload,
            league_id=args.league_id,
            expected_team_id=args.team_id,
            expected_season_id=args.season_id,
            observed_at=args.observed_at,
        )
    except (
        SportmonksValidationError,
        json.JSONDecodeError,
        OSError,
        TypeError,
        ValueError,
    ) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    _print_summary(summarize_transformed_rows(rows))
    return 0


def _print_summary(summary: dict) -> None:
    print(f"row_count: {summary['row_count']}")
    print(f"columns: {', '.join(summary['columns'])}")
    print(f"provider: {summary['provider']}")
    print(f"source_endpoint: {summary['source_endpoint']}")
    print(f"has_position_ids: {summary['has_position_ids']}")
    print(f"has_jersey_numbers: {summary['has_jersey_numbers']}")


if __name__ == "__main__":
    raise SystemExit(main())
