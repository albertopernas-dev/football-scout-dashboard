from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.provider_payload_shapes import (  # noqa: E402
    flatten_advanced_synthetic_provider_payload,
    load_json_payload,
)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Flatten the advanced synthetic provider payload to local normalized CSV records."
        )
    )
    parser.add_argument("--input", required=True, type=Path, help="Synthetic JSON input path.")
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Output path inside data/enrichment/ ending in .local.csv.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing synthetic output file.",
    )
    return parser


def flatten_payload_file_to_csv(
    input_path: str | Path,
    output_path: str | Path,
    force: bool = False,
) -> pd.DataFrame:
    resolved_output = _validated_output_path(output_path)
    if resolved_output.exists() and not force:
        raise FileExistsError(
            f"Output file already exists: {resolved_output}. Use --force to overwrite."
        )

    resolved_input = _resolve_project_path(input_path)
    payload = load_json_payload(resolved_input)
    records = flatten_advanced_synthetic_provider_payload(payload)

    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    records.to_csv(resolved_output, index=False)
    return records


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    try:
        records = flatten_payload_file_to_csv(
            args.input,
            args.output,
            force=args.force,
        )
        resolved_input = _resolve_project_path(args.input)
        resolved_output = _validated_output_path(args.output)
    except (FileExistsError, OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    provider_names = _unique_provider_names(records)
    print(f"Input path: {resolved_input}")
    print(f"Output path: {resolved_output}")
    print(f"Rows: {len(records)}")
    print(f"Columns ({len(records.columns)}): {', '.join(records.columns)}")
    print(f"Provider name(s): {', '.join(provider_names) if provider_names else 'None'}")
    print("Warning: synthetic-only output; no real provider integration is performed.")
    return 0


def _validated_output_path(output_path: str | Path) -> Path:
    path = _resolve_project_path(output_path)
    enrichment_root = (PROJECT_ROOT / "data" / "enrichment").resolve()

    if not path.name.lower().endswith(".local.csv"):
        raise ValueError("Output path must end in .local.csv.")
    if not path.is_relative_to(enrichment_root):
        raise ValueError("Output path must be inside the project data/enrichment directory.")
    return path


def _resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate
    return candidate.resolve()


def _unique_provider_names(records: pd.DataFrame) -> list[str]:
    if "provider_name" not in records.columns:
        return []
    names = records["provider_name"].dropna().astype(str).str.strip()
    return sorted(name for name in names.unique().tolist() if name)


if __name__ == "__main__":
    raise SystemExit(main())
