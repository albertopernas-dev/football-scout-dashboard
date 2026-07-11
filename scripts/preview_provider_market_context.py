from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.provider_market_context import (  # noqa: E402
    CANONICAL_MARKET_CONTEXT_COLUMNS,
    OPTIONAL_PROVIDER_CONTEXT_COLUMNS,
    validate_canonical_market_context_df,
)


PREVIEW_COLUMNS = [
    "player",
    "team",
    "league",
    "season",
    "age",
    "market_value_eur",
    "contract_end_date",
    "source",
    "confidence",
]


def preview_provider_market_context(
    input_path: str | Path,
    max_rows: int = 5,
    show_columns: bool = False,
) -> dict[str, Any]:
    csv_path = Path(input_path)
    df = pd.read_csv(csv_path, keep_default_na=False)
    columns = df.columns.tolist()
    missing_columns = [
        column for column in CANONICAL_MARKET_CONTEXT_COLUMNS if column not in df.columns
    ]
    known_columns = {*CANONICAL_MARKET_CONTEXT_COLUMNS, *OPTIONAL_PROVIDER_CONTEXT_COLUMNS}
    extra_columns = [column for column in df.columns if column not in known_columns]
    validation_errors = validate_canonical_market_context_df(df)
    preview_columns = [column for column in PREVIEW_COLUMNS if column in df.columns]

    return {
        "file_path": str(csv_path),
        "row_count": int(len(df)),
        "columns": columns,
        "missing_columns": missing_columns,
        "extra_columns": extra_columns,
        "validation_errors": validation_errors,
        "preview_df": df.loc[:, preview_columns].head(max_rows).copy(),
        "show_columns": bool(show_columns),
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate and preview a local canonical Market Context CSV.",
    )
    parser.add_argument("--input", required=True, help="Path to canonical Market Context CSV.")
    parser.add_argument("--max-rows", type=int, default=5, help="Preview row limit.")
    parser.add_argument(
        "--show-columns",
        action="store_true",
        help="Print all columns found in the input file.",
    )
    parser.add_argument(
        "--fail-on-validation-errors",
        action="store_true",
        help="Return exit code 1 when validation errors are found.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    try:
        result = preview_provider_market_context(
            args.input,
            max_rows=args.max_rows,
            show_columns=args.show_columns,
        )
    except (FileNotFoundError, OSError, pd.errors.ParserError) as error:
        print(f"Input file could not be read: {args.input}")
        print(f"Error: {error}")
        return 1

    _print_preview_result(result)
    if args.fail_on_validation_errors and result["validation_errors"]:
        return 1
    return 0


def _print_preview_result(result: dict[str, Any]) -> None:
    print(f"File path: {result['file_path']}")
    print(f"Row count: {result['row_count']}")
    print(f"Column count: {len(result['columns'])}")

    if result["show_columns"]:
        print("All columns:")
        for column in result["columns"]:
            print(f"- {column}")

    print("Missing canonical columns:")
    _print_list_or_none(result["missing_columns"])

    print("Extra columns:")
    _print_list_or_none(result["extra_columns"])

    validation_errors = result["validation_errors"]
    print(f"Validation error count: {len(validation_errors)}")
    if validation_errors:
        print("Validation errors:")
        for error in validation_errors[:10]:
            print(f"- {error}")

    print("Preview:")
    preview_df = result["preview_df"]
    if preview_df.empty:
        print("(no rows)")
    else:
        print(preview_df.to_string(index=False))


def _print_list_or_none(values: list[str]) -> None:
    if not values:
        print("- None")
        return
    for value in values:
        print(f"- {value}")


if __name__ == "__main__":
    raise SystemExit(main())
