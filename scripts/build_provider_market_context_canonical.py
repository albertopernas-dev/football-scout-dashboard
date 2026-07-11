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
    build_canonical_market_context_df,
    validate_canonical_market_context_df,
)


def build_provider_market_context_canonical(
    input_path: Path,
    output_path: Path,
    include_optional_fields: bool = False,
    force: bool = False,
) -> dict[str, object]:
    input_path = Path(input_path)
    output_path = Path(output_path)

    if output_path.exists() and not force:
        return _result(
            input_path=input_path,
            output_path=output_path,
            row_count=0,
            column_count=0,
            columns=[],
            validation_errors=[
                f"Output already exists: {output_path}. Use --force to overwrite.",
            ],
            written=False,
        )

    try:
        records_df = pd.read_csv(input_path, keep_default_na=False)
    except (FileNotFoundError, OSError, pd.errors.ParserError) as error:
        return _result(
            input_path=input_path,
            output_path=output_path,
            row_count=0,
            column_count=0,
            columns=[],
            validation_errors=[f"Input could not be read: {error}"],
            written=False,
        )

    canonical_df = build_canonical_market_context_df(
        records_df.to_dict("records"),
        include_optional_fields=include_optional_fields,
    )
    validation_errors = validate_canonical_market_context_df(canonical_df)
    if validation_errors:
        return _result(
            input_path=input_path,
            output_path=output_path,
            row_count=int(len(canonical_df)),
            column_count=int(len(canonical_df.columns)),
            columns=canonical_df.columns.tolist(),
            validation_errors=validation_errors,
            written=False,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canonical_df.to_csv(output_path, index=False)

    return _result(
        input_path=input_path,
        output_path=output_path,
        row_count=int(len(canonical_df)),
        column_count=int(len(canonical_df.columns)),
        columns=canonical_df.columns.tolist(),
        validation_errors=[],
        written=True,
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a canonical Market Context CSV from normalized local records.",
    )
    parser.add_argument("--input", required=True, help="Path to normalized local records CSV.")
    parser.add_argument("--output", required=True, help="Path for canonical Market Context CSV.")
    parser.add_argument(
        "--include-optional-fields",
        action="store_true",
        help="Preserve recognized optional provider context columns.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output if it already exists.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    result = build_provider_market_context_canonical(
        Path(args.input),
        Path(args.output),
        include_optional_fields=args.include_optional_fields,
        force=args.force,
    )
    _print_result(result)
    if result["validation_errors"] or not result["written"]:
        return 1
    return 0


def _result(
    input_path: Path,
    output_path: Path,
    row_count: int,
    column_count: int,
    columns: list[str],
    validation_errors: list[str],
    written: bool,
) -> dict[str, object]:
    return {
        "input_path": str(input_path),
        "output_path": str(output_path),
        "row_count": row_count,
        "column_count": column_count,
        "validation_errors": validation_errors,
        "written": written,
        "columns": columns,
    }


def _print_result(result: dict[str, Any]) -> None:
    print(f"Input path: {result['input_path']}")
    print(f"Output path: {result['output_path']}")
    print(f"Row count: {result['row_count']}")
    print(f"Column count: {result['column_count']}")
    print(f"Validation error count: {len(result['validation_errors'])}")
    print(f"Written: {'yes' if result['written'] else 'no'}")

    validation_errors = result["validation_errors"]
    if validation_errors:
        print("Validation errors:")
        for error in validation_errors:
            print(f"- {error}")


if __name__ == "__main__":
    raise SystemExit(main())
