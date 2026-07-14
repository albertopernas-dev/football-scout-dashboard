from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.apply_provider_identity_mapping import (  # noqa: E402
    apply_provider_identity_mapping_cli,
)
from scripts.build_provider_market_context_canonical import (  # noqa: E402
    build_provider_market_context_canonical,
)


def run_provider_fixture_prototype_demo(
    records_path: Path,
    mapping_path: Path,
    mapped_output_path: Path,
    canonical_output_path: Path,
    include_optional_fields: bool = False,
    force: bool = False,
) -> dict[str, object]:
    records_path = Path(records_path)
    mapping_path = Path(mapping_path)
    mapped_output_path = Path(mapped_output_path)
    canonical_output_path = Path(canonical_output_path)

    for output_path in (mapped_output_path, canonical_output_path):
        if output_path.exists() and not force:
            return _result(
                records_path,
                mapping_path,
                mapped_output_path,
                canonical_output_path,
                error=f"Output already exists: {output_path}. Use --force to overwrite.",
            )

    mapping_result = apply_provider_identity_mapping_cli(
        records_path,
        mapping_path,
        mapped_output_path,
        force=force,
    )
    if not mapping_result["written"]:
        return _result(
            records_path,
            mapping_path,
            mapped_output_path,
            canonical_output_path,
            input_record_count=int(mapping_result["input_record_count"]),
            mapped_record_count=int(mapping_result["mapped_record_count"]),
            excluded_record_count=int(mapping_result["excluded_record_count"]),
            mapped_written=False,
            error=str(mapping_result["error"]),
        )

    canonical_result = build_provider_market_context_canonical(
        mapped_output_path,
        canonical_output_path,
        include_optional_fields=include_optional_fields,
        force=force,
    )
    validation_errors = list(canonical_result["validation_errors"])
    canonical_written = bool(canonical_result["written"])
    error = None
    if not canonical_written:
        error = "Canonical Market Context build failed."
        if validation_errors:
            error = f"{error} {'; '.join(validation_errors)}"

    return _result(
        records_path,
        mapping_path,
        mapped_output_path,
        canonical_output_path,
        input_record_count=int(mapping_result["input_record_count"]),
        mapped_record_count=int(mapping_result["mapped_record_count"]),
        excluded_record_count=int(mapping_result["excluded_record_count"]),
        canonical_row_count=int(canonical_result["row_count"]),
        canonical_column_count=int(canonical_result["column_count"]),
        canonical_validation_errors=validation_errors,
        mapped_written=True,
        canonical_written=canonical_written,
        error=error,
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the offline synthetic provider fixture prototype demo.",
    )
    parser.add_argument("--records", required=True, help="Normalized provider records CSV.")
    parser.add_argument("--mapping", required=True, help="Reviewed identity mapping CSV.")
    parser.add_argument("--mapped-output", required=True, help="Intermediate mapped CSV path.")
    parser.add_argument("--canonical-output", required=True, help="Canonical output CSV path.")
    parser.add_argument(
        "--include-optional-fields",
        action="store_true",
        help="Preserve recognized optional provider fields in canonical output.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite both outputs if they already exist.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    result = run_provider_fixture_prototype_demo(
        Path(args.records),
        Path(args.mapping),
        Path(args.mapped_output),
        Path(args.canonical_output),
        include_optional_fields=args.include_optional_fields,
        force=args.force,
    )
    _print_result(result)
    return 0 if result["mapped_written"] and result["canonical_written"] else 1


def _result(
    records_path: Path,
    mapping_path: Path,
    mapped_output_path: Path,
    canonical_output_path: Path,
    input_record_count: int = 0,
    mapped_record_count: int = 0,
    excluded_record_count: int = 0,
    canonical_row_count: int = 0,
    canonical_column_count: int = 0,
    canonical_validation_errors: list[str] | None = None,
    mapped_written: bool = False,
    canonical_written: bool = False,
    error: str | None = None,
) -> dict[str, object]:
    return {
        "records_path": str(records_path),
        "mapping_path": str(mapping_path),
        "mapped_output_path": str(mapped_output_path),
        "canonical_output_path": str(canonical_output_path),
        "input_record_count": input_record_count,
        "mapped_record_count": mapped_record_count,
        "excluded_record_count": excluded_record_count,
        "canonical_row_count": canonical_row_count,
        "canonical_column_count": canonical_column_count,
        "canonical_validation_errors": list(canonical_validation_errors or []),
        "mapped_written": mapped_written,
        "canonical_written": canonical_written,
        "error": error,
    }


def _print_result(result: dict[str, Any]) -> None:
    print(f"Records path: {result['records_path']}")
    print(f"Mapping path: {result['mapping_path']}")
    print(f"Mapped output path: {result['mapped_output_path']}")
    print(f"Canonical output path: {result['canonical_output_path']}")
    print(f"Input record count: {result['input_record_count']}")
    print(f"Mapped record count: {result['mapped_record_count']}")
    print(f"Excluded record count: {result['excluded_record_count']}")
    print(f"Canonical row count: {result['canonical_row_count']}")
    print(f"Canonical column count: {result['canonical_column_count']}")
    print(
        "Canonical validation error count: "
        f"{len(result['canonical_validation_errors'])}"
    )
    print(f"Written mapped: {'yes' if result['mapped_written'] else 'no'}")
    print(f"Written canonical: {'yes' if result['canonical_written'] else 'no'}")
    if result["error"]:
        print(f"Error: {result['error']}")


if __name__ == "__main__":
    raise SystemExit(main())
