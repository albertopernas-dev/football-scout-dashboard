from __future__ import annotations

import pandas as pd

from scripts.preview_provider_market_context import (
    main,
    preview_provider_market_context,
)
from src.provider_market_context import CANONICAL_MARKET_CONTEXT_COLUMNS


def _write_csv(path, rows, columns=None):
    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(path, index=False)


def _valid_identity_row():
    return {
        "player": "Player A",
        "team": "Team A",
        "league": "LaLiga",
        "season": 2024,
        "age": "",
        "market_value_eur": "",
        "contract_end_date": "",
        "source": "",
        "source_url": "",
        "confidence": "",
        "notes": "",
    }


def test_preview_valid_synthetic_csv_returns_success(tmp_path):
    csv_path = tmp_path / "canonical.csv"
    _write_csv(csv_path, [_valid_identity_row()])

    result = preview_provider_market_context(csv_path)

    assert result["row_count"] == 1
    assert result["missing_columns"] == []
    assert result["extra_columns"] == []
    assert result["validation_errors"] == []


def test_preview_reports_enrichment_without_source_confidence(tmp_path):
    csv_path = tmp_path / "canonical.csv"
    row = _valid_identity_row()
    row["age"] = 24
    _write_csv(csv_path, [row])

    result = preview_provider_market_context(csv_path)

    assert any("source is required" in error for error in result["validation_errors"])
    assert any("confidence is required" in error for error in result["validation_errors"])


def test_main_fail_on_validation_errors_returns_exit_code_one(tmp_path, capsys):
    csv_path = tmp_path / "canonical.csv"
    row = _valid_identity_row()
    row["market_value_eur"] = 1500000
    _write_csv(csv_path, [row])

    exit_code = main(
        [
            "--input",
            str(csv_path),
            "--fail-on-validation-errors",
        ]
    )

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "Validation error count:" in output


def test_preview_reports_missing_canonical_columns(tmp_path):
    csv_path = tmp_path / "canonical.csv"
    _write_csv(csv_path, [{"player": "Player A", "team": "Team A"}])

    result = preview_provider_market_context(csv_path)

    assert "league" in result["missing_columns"]
    assert "confidence" in result["missing_columns"]


def test_preview_reports_extra_columns(tmp_path):
    csv_path = tmp_path / "canonical.csv"
    row = _valid_identity_row()
    row["provider_extra"] = "ignored-for-preview"
    _write_csv(csv_path, [row])

    result = preview_provider_market_context(csv_path)

    assert result["extra_columns"] == ["provider_extra"]


def test_main_missing_file_returns_exit_code_one(tmp_path, capsys):
    missing_path = tmp_path / "missing.csv"

    exit_code = main(["--input", str(missing_path)])

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "could not be read" in output


def test_preview_respects_max_rows(tmp_path):
    csv_path = tmp_path / "canonical.csv"
    rows = []
    for index in range(3):
        row = _valid_identity_row()
        row["player"] = f"Player {index}"
        rows.append(row)
    _write_csv(csv_path, rows)

    result = preview_provider_market_context(csv_path, max_rows=2)

    assert len(result["preview_df"]) == 2
    assert result["preview_df"]["player"].tolist() == ["Player 0", "Player 1"]


def test_show_columns_prints_all_columns(tmp_path, capsys):
    csv_path = tmp_path / "canonical.csv"
    row = _valid_identity_row()
    row["provider_extra"] = "shown"
    _write_csv(csv_path, [row])

    exit_code = main(["--input", str(csv_path), "--show-columns"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "All columns:" in output
    assert "provider_extra" in output


def test_preview_uses_primary_columns_for_preview(tmp_path):
    csv_path = tmp_path / "canonical.csv"
    row = _valid_identity_row()
    row["notes"] = "Not part of compact preview."
    _write_csv(csv_path, [row])

    result = preview_provider_market_context(csv_path)

    assert result["preview_df"].columns.tolist() == [
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


def test_valid_csv_main_returns_exit_code_zero(tmp_path):
    csv_path = tmp_path / "canonical.csv"
    _write_csv(csv_path, [_valid_identity_row()], columns=CANONICAL_MARKET_CONTEXT_COLUMNS)

    assert main(["--input", str(csv_path)]) == 0
