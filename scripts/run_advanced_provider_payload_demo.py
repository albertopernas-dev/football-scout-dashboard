from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.flatten_provider_payload_advanced_sample import (  # noqa: E402
    flatten_payload_file_to_csv,
)
from src.provider_identity_mapping import (  # noqa: E402
    apply_provider_identity_mapping_to_records,
    load_provider_identity_mapping_csv,
)
from src.provider_market_context import (  # noqa: E402
    build_canonical_market_context_df,
    validate_canonical_market_context_df,
)
from src.provider_payload_shapes import (  # noqa: E402
    flatten_advanced_synthetic_provider_payload,
    load_json_payload,
)


def run_advanced_provider_payload_demo(
    input_path: str | Path,
    mapping_path: str | Path,
    flattened_output_path: str | Path,
    mapped_output_path: str | Path,
    canonical_output_path: str | Path,
    include_optional_fields: bool = False,
    force: bool = False,
) -> dict[str, object]:
    resolved_input = _resolve_project_path(input_path)
    resolved_mapping = _resolve_project_path(mapping_path)
    output_paths = [
        _validated_output_path(flattened_output_path),
        _validated_output_path(mapped_output_path),
        _validated_output_path(canonical_output_path),
    ]
    if len(set(output_paths)) != len(output_paths):
        raise ValueError("Flattened, mapped and canonical output paths must be distinct.")

    if not force:
        for output_path in output_paths:
            if output_path.exists():
                raise FileExistsError(
                    f"Output file already exists: {output_path}. Use --force to overwrite."
                )

    payload = load_json_payload(resolved_input)
    flattened_df = flatten_advanced_synthetic_provider_payload(payload)
    mapping_df = load_provider_identity_mapping_csv(resolved_mapping)
    mapped_df = apply_provider_identity_mapping_to_records(flattened_df, mapping_df)
    canonical_df = build_canonical_market_context_df(
        mapped_df.to_dict("records"),
        include_optional_fields=include_optional_fields,
    )
    validation_errors = validate_canonical_market_context_df(canonical_df)
    if validation_errors:
        formatted_errors = "\n".join(f"- {error}" for error in validation_errors)
        raise ValueError(f"Canonical Market Context validation failed:\n{formatted_errors}")

    flattened_output, mapped_output, canonical_output = output_paths
    flatten_payload_file_to_csv(
        resolved_input,
        flattened_output,
        force=force,
    )
    mapped_output.parent.mkdir(parents=True, exist_ok=True)
    mapped_df.to_csv(mapped_output, index=False)
    canonical_output.parent.mkdir(parents=True, exist_ok=True)
    canonical_df.to_csv(canonical_output, index=False)

    return {
        "input_path": str(resolved_input),
        "mapping_path": str(resolved_mapping),
        "flattened_output_path": str(flattened_output),
        "mapped_output_path": str(mapped_output),
        "canonical_output_path": str(canonical_output),
        "flattened_row_count": int(len(flattened_df)),
        "mapped_row_count": int(len(mapped_df)),
        "excluded_row_count": int(len(flattened_df) - len(mapped_df)),
        "canonical_row_count": int(len(canonical_df)),
        "canonical_columns": canonical_df.columns.tolist(),
        "canonical_validation_errors": validation_errors,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the advanced synthetic provider payload demo locally and offline.",
    )
    parser.add_argument("--input", required=True, type=Path, help="Synthetic JSON input path.")
    parser.add_argument("--mapping", required=True, type=Path, help="Reviewed mapping CSV path.")
    parser.add_argument(
        "--flattened-output",
        required=True,
        type=Path,
        help="Flattened .local.csv output inside data/enrichment/.",
    )
    parser.add_argument(
        "--mapped-output",
        required=True,
        type=Path,
        help="Mapped .local.csv output inside data/enrichment/.",
    )
    parser.add_argument(
        "--canonical-output",
        required=True,
        type=Path,
        help="Canonical .local.csv output inside data/enrichment/.",
    )
    parser.add_argument(
        "--include-optional-fields",
        action="store_true",
        help="Preserve recognized optional provider fields in canonical output.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite all existing synthetic output files.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    try:
        result = run_advanced_provider_payload_demo(
            args.input,
            args.mapping,
            args.flattened_output,
            args.mapped_output,
            args.canonical_output,
            include_optional_fields=args.include_optional_fields,
            force=args.force,
        )
    except (FileExistsError, OSError, ValueError, pd.errors.ParserError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    _print_result(result)
    return 0


def _validated_output_path(output_path: str | Path) -> Path:
    path = _resolve_project_path(output_path)
    enrichment_root = (PROJECT_ROOT / "data" / "enrichment").resolve()
    if not path.name.lower().endswith(".local.csv"):
        raise ValueError("Every output path must end in .local.csv.")
    if not path.is_relative_to(enrichment_root):
        raise ValueError("Every output path must be inside project data/enrichment.")
    return path


def _resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate
    return candidate.resolve()


def _print_result(result: dict[str, Any]) -> None:
    print(f"Input path: {result['input_path']}")
    print(f"Mapping path: {result['mapping_path']}")
    print(f"Flattened output path: {result['flattened_output_path']}")
    print(f"Mapped output path: {result['mapped_output_path']}")
    print(f"Canonical output path: {result['canonical_output_path']}")
    print(f"Flattened rows: {result['flattened_row_count']}")
    print(f"Mapped rows: {result['mapped_row_count']}")
    print(f"Excluded rows: {result['excluded_row_count']}")
    print(f"Canonical rows: {result['canonical_row_count']}")
    print(f"Canonical columns: {', '.join(result['canonical_columns'])}")
    print(
        "Validation error count: "
        f"{len(result['canonical_validation_errors'])}"
    )
    print(
        "Warning: synthetic-only demo; no real provider integration. "
        "Outputs remain local and ignored."
    )


if __name__ == "__main__":
    raise SystemExit(main())
