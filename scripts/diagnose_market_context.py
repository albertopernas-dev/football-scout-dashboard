from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_sources import load_players_data_with_metadata
from src.market_context import (
    MERGE_SOURCE_COLUMNS,
    find_duplicate_market_context_keys,
    load_market_context_csv,
    summarize_market_context_diagnostics,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Diagnose a market context CSV against the active player dataset."
    )
    parser.add_argument(
        "--market-context-csv",
        required=True,
        type=Path,
        help="Path to the market context enrichment CSV.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    players_df, metadata = load_players_data_with_metadata()
    market_context_df, validation_errors = load_market_context_csv(args.market_context_csv)

    print("Market Context Diagnostics")
    print("==========================")
    print(f"Dataset metadata: {json.dumps(metadata, ensure_ascii=False, default=str)}")
    print(f"Player rows: {len(players_df)}")
    print(f"Market context CSV: {args.market_context_csv}")
    print(f"Market context rows: {len(market_context_df)}")
    print()

    _print_validation_errors(validation_errors)
    _print_duplicates(market_context_df)

    missing_merge_columns = [
        column for column in MERGE_SOURCE_COLUMNS if column not in market_context_df.columns
    ]
    if missing_merge_columns:
        print("Merge skipped")
        print("-------------")
        print(f"Missing columns required for merge: {', '.join(missing_merge_columns)}")
        return

    diagnostics = summarize_market_context_diagnostics(
        players_df,
        market_context_df,
        validation_errors=validation_errors,
    )
    coverage = diagnostics["coverage"]
    _print_coverage(coverage)
    _print_examples("Matched player examples", diagnostics["matched_examples"])
    _print_examples("Unmatched enrichment examples", diagnostics["unmatched_enrichment_examples"])
    _print_market_context_warning(coverage)


def _print_validation_errors(validation_errors: list[str]) -> None:
    print("Validation errors")
    print("-----------------")
    if not validation_errors:
        print("None")
        print()
        return
    for error in validation_errors:
        print(f"- {error}")
    print()


def _print_duplicates(market_context_df: pd.DataFrame) -> None:
    duplicates = find_duplicate_market_context_keys(market_context_df)
    print("Duplicate market context keys")
    print("-----------------------------")
    if duplicates.empty:
        print("None")
        print()
        return
    print(f"Duplicate rows: {len(duplicates)}")
    _print_dataframe(duplicates)
    print()


def _print_coverage(coverage: dict[str, float | int]) -> None:
    print("Coverage")
    print("--------")
    for key, value in coverage.items():
        print(f"{key}: {value}")
    print()


def _print_examples(title: str, df: pd.DataFrame) -> None:
    print(title)
    print("-" * len(title))
    if df.empty:
        print("None")
    else:
        _print_dataframe(df)
    print()


def _print_dataframe(df: pd.DataFrame) -> None:
    print(df.to_string(index=False))


def _print_market_context_warning(coverage: dict[str, float | int]) -> None:
    if (
        coverage.get("age_known_pct", 0.0) == 0.0
        and coverage.get("market_value_known_pct", 0.0) == 0.0
        and coverage.get("contract_known_pct", 0.0) == 0.0
    ):
        print(
            "Warning: age, market value and contract coverage are all 0%. "
            "Opportunity Finder would still have limited market context."
        )


if __name__ == "__main__":
    main()
