from __future__ import annotations

from pathlib import Path

import pandas as pd

from scripts.build_provider_market_context_canonical import (
    build_provider_market_context_canonical,
    main,
)
from src.provider_market_context import (
    CANONICAL_MARKET_CONTEXT_COLUMNS,
    OPTIONAL_PROVIDER_CONTEXT_COLUMNS,
    validate_canonical_market_context_df,
)


def _sample_records() -> list[dict[str, object]]:
    return [
        {
            "player": "Player Alpha",
            "team": "Team Red",
            "league": "Synthetic League",
            "season": 2024,
            "raw_provider_status": "reviewed",
        },
        {
            "player": "Player Beta",
            "team": "Team Blue",
            "league": "Synthetic League",
            "season": 2024,
            "age": 24,
            "market_value_eur": 1_500_000,
            "contract_end_date": "2027-06-30",
            "source": "synthetic_provider",
            "source_url": "https://example.test/player-beta",
            "confidence": "medium",
            "notes": "Synthetic reviewed example row. Not real data.",
            "provider_player_id": "synthetic-player-beta",
            "provider_team_id": "synthetic-team-blue",
            "provider_name": "Synthetic Provider",
            "fetched_at": "2026-01-01T00:00:00Z",
            "value_date": "2026-01-01",
            "contract_option_notes": "Synthetic option note.",
            "license_scope": "synthetic_example_only",
            "raw_provider_status": "reviewed",
            "raw_provider_value_text": "synthetic-only",
        },
        {
            "player": "Player Gamma",
            "team": "Team Green",
            "league": "Synthetic League",
            "season": 2024,
            "age": 29,
            "market_value_eur": "",
            "contract_end_date": "2025-06-30",
            "source": "synthetic_provider",
            "source_url": "https://example.test/player-gamma",
            "confidence": "low",
            "notes": "Synthetic partial context example. Not real data.",
            "raw_provider_status": "partial",
        },
    ]


def _write_normalized_csv(path: Path, rows: list[dict[str, object]]) -> None:
    pd.DataFrame(rows).to_csv(path, index=False)


def test_builds_minimal_canonical_csv_from_synthetic_normalized_records(tmp_path):
    input_path = tmp_path / "normalized.csv"
    output_path = tmp_path / "canonical.csv"
    _write_normalized_csv(input_path, _sample_records())

    result = build_provider_market_context_canonical(input_path, output_path)

    output = pd.read_csv(output_path, keep_default_na=False)
    assert result["written"] is True
    assert result["row_count"] == 3
    assert output.columns.tolist() == CANONICAL_MARKET_CONTEXT_COLUMNS
    assert validate_canonical_market_context_df(output) == []
    assert "raw_provider_status" not in output.columns
    assert "raw_provider_value_text" not in output.columns


def test_builds_canonical_csv_with_optional_fields_when_requested(tmp_path):
    input_path = tmp_path / "normalized.csv"
    output_path = tmp_path / "canonical.csv"
    _write_normalized_csv(input_path, _sample_records())

    build_provider_market_context_canonical(
        input_path,
        output_path,
        include_optional_fields=True,
    )

    output = pd.read_csv(output_path, keep_default_na=False)
    assert output.columns.tolist() == [
        *CANONICAL_MARKET_CONTEXT_COLUMNS,
        *OPTIONAL_PROVIDER_CONTEXT_COLUMNS,
    ]
    assert output.loc[1, "provider_player_id"] == "synthetic-player-beta"
    assert "raw_provider_status" not in output.columns


def test_does_not_overwrite_existing_output_without_force(tmp_path):
    input_path = tmp_path / "normalized.csv"
    output_path = tmp_path / "canonical.csv"
    _write_normalized_csv(input_path, _sample_records())
    output_path.write_text("existing content", encoding="utf-8")

    result = build_provider_market_context_canonical(input_path, output_path)

    assert result["written"] is False
    assert result["validation_errors"]
    assert "already exists" in result["validation_errors"][0]
    assert output_path.read_text(encoding="utf-8") == "existing content"


def test_overwrites_existing_output_with_force(tmp_path):
    input_path = tmp_path / "normalized.csv"
    output_path = tmp_path / "canonical.csv"
    _write_normalized_csv(input_path, _sample_records())
    output_path.write_text("existing content", encoding="utf-8")

    result = build_provider_market_context_canonical(input_path, output_path, force=True)

    output = pd.read_csv(output_path, keep_default_na=False)
    assert result["written"] is True
    assert output["player"].tolist() == ["Player Alpha", "Player Beta", "Player Gamma"]


def test_validation_errors_prevent_writing_output(tmp_path):
    input_path = tmp_path / "normalized.csv"
    output_path = tmp_path / "canonical.csv"
    rows = _sample_records()
    rows[1]["source"] = ""
    rows[1]["confidence"] = ""
    _write_normalized_csv(input_path, rows)

    result = build_provider_market_context_canonical(input_path, output_path)

    assert result["written"] is False
    assert not output_path.exists()
    assert any("source is required" in error for error in result["validation_errors"])
    assert any("confidence is required" in error for error in result["validation_errors"])


def test_main_returns_zero_for_valid_build(tmp_path):
    input_path = tmp_path / "normalized.csv"
    output_path = tmp_path / "canonical.csv"
    _write_normalized_csv(input_path, _sample_records())

    assert main(["--input", str(input_path), "--output", str(output_path)]) == 0
    assert output_path.exists()


def test_main_returns_one_for_missing_input(tmp_path):
    output_path = tmp_path / "canonical.csv"

    assert main(["--input", str(tmp_path / "missing.csv"), "--output", str(output_path)]) == 1
    assert not output_path.exists()


def test_main_returns_one_for_invalid_validation(tmp_path):
    input_path = tmp_path / "normalized.csv"
    output_path = tmp_path / "canonical.csv"
    rows = _sample_records()
    rows[1]["contract_end_date"] = "30/06/2027"
    _write_normalized_csv(input_path, rows)

    assert main(["--input", str(input_path), "--output", str(output_path)]) == 1
    assert not output_path.exists()


def test_versioned_normalized_sample_builds_valid_canonical_output(tmp_path):
    sample_path = (
        Path(__file__).resolve().parents[1]
        / "docs"
        / "examples"
        / "provider_market_context_normalized_records_sample.csv"
    )
    output_path = tmp_path / "canonical.csv"

    result = build_provider_market_context_canonical(
        sample_path,
        output_path,
        include_optional_fields=True,
    )

    output = pd.read_csv(output_path, keep_default_na=False)
    assert result["written"] is True
    assert result["row_count"] == 3
    assert "raw_provider_status" not in output.columns
    assert validate_canonical_market_context_df(output) == []
