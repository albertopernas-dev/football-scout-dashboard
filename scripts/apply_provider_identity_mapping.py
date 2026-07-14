from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.provider_identity_mapping import (  # noqa: E402
    apply_provider_identity_mapping_to_records,
    load_provider_identity_mapping_csv,
)


def apply_provider_identity_mapping_cli(
    records_path: Path,
    mapping_path: Path,
    output_path: Path,
    force: bool = False,
) -> dict[str, object]:
    records_path = Path(records_path)
    mapping_path = Path(mapping_path)
    output_path = Path(output_path)

    if output_path.exists() and not force:
        return _result(
            records_path=records_path,
            mapping_path=mapping_path,
            output_path=output_path,
            error=f"Output already exists: {output_path}. Use --force to overwrite.",
        )

    try:
        records_df = pd.read_csv(records_path, keep_default_na=False)
    except (FileNotFoundError, OSError, pd.errors.ParserError) as error:
        return _result(
            records_path=records_path,
            mapping_path=mapping_path,
            output_path=output_path,
            error=f"Records CSV could not be read: {error}",
        )

    try:
        mapping_df = load_provider_identity_mapping_csv(mapping_path)
    except (FileNotFoundError, OSError, pd.errors.ParserError) as error:
        return _result(
            records_path=records_path,
            mapping_path=mapping_path,
            output_path=output_path,
            input_record_count=int(len(records_df)),
            error=f"Mapping CSV could not be read: {error}",
        )

    try:
        mapped_df = apply_provider_identity_mapping_to_records(records_df, mapping_df)
    except ValueError as error:
        return _result(
            records_path=records_path,
            mapping_path=mapping_path,
            output_path=output_path,
            input_record_count=int(len(records_df)),
            error=str(error),
        )

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        mapped_df.to_csv(output_path, index=False)
    except OSError as error:
        return _result(
            records_path=records_path,
            mapping_path=mapping_path,
            output_path=output_path,
            input_record_count=int(len(records_df)),
            mapped_record_count=int(len(mapped_df)),
            excluded_record_count=int(len(records_df) - len(mapped_df)),
            columns=mapped_df.columns.tolist(),
            error=f"Mapped output could not be written: {error}",
        )

    return _result(
        records_path=records_path,
        mapping_path=mapping_path,
        output_path=output_path,
        input_record_count=int(len(records_df)),
        mapped_record_count=int(len(mapped_df)),
        excluded_record_count=int(len(records_df) - len(mapped_df)),
        columns=mapped_df.columns.tolist(),
        error=None,
        written=True,
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Apply a reviewed identity mapping to local provider records.",
    )
    parser.add_argument("--records", required=True, help="Path to normalized provider records CSV.")
    parser.add_argument("--mapping", required=True, help="Path to reviewed identity mapping CSV.")
    parser.add_argument("--output", required=True, help="Path for the mapped local CSV.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output if it already exists.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    result = apply_provider_identity_mapping_cli(
        Path(args.records),
        Path(args.mapping),
        Path(args.output),
        force=args.force,
    )
    _print_result(result)
    return 0 if result["written"] else 1


def _result(
    records_path: Path,
    mapping_path: Path,
    output_path: Path,
    input_record_count: int = 0,
    mapped_record_count: int = 0,
    excluded_record_count: int = 0,
    columns: list[str] | None = None,
    error: str | None = None,
    written: bool = False,
) -> dict[str, object]:
    return {
        "records_path": str(records_path),
        "mapping_path": str(mapping_path),
        "output_path": str(output_path),
        "input_record_count": input_record_count,
        "mapped_record_count": mapped_record_count,
        "excluded_record_count": excluded_record_count,
        "columns": list(columns or []),
        "error": error,
        "written": written,
    }


def _print_result(result: dict[str, Any]) -> None:
    print(f"Records path: {result['records_path']}")
    print(f"Mapping path: {result['mapping_path']}")
    print(f"Output path: {result['output_path']}")
    print(f"Input record count: {result['input_record_count']}")
    print(f"Mapped record count: {result['mapped_record_count']}")
    print(f"Unmapped/excluded record count: {result['excluded_record_count']}")
    print(f"Written: {'yes' if result['written'] else 'no'}")
    if result["error"]:
        print(f"Error: {result['error']}")


if __name__ == "__main__":
    raise SystemExit(main())
