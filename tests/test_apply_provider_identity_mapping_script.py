from __future__ import annotations

from pathlib import Path

import pandas as pd

from scripts.apply_provider_identity_mapping import (
    apply_provider_identity_mapping_cli,
    main,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RECORDS_SAMPLE = PROJECT_ROOT / "docs" / "examples" / "provider_fixture_records_sample.csv"
MAPPING_SAMPLE = PROJECT_ROOT / "docs" / "examples" / "provider_identity_mapping_sample.csv"


def test_applies_versioned_samples_and_writes_two_matched_records(tmp_path):
    output_path = tmp_path / "nested" / "mapped.csv"

    result = apply_provider_identity_mapping_cli(
        RECORDS_SAMPLE,
        MAPPING_SAMPLE,
        output_path,
    )

    output = pd.read_csv(output_path, keep_default_na=False)
    assert result["written"] is True
    assert result["input_record_count"] == 5
    assert result["mapped_record_count"] == 2
    assert result["excluded_record_count"] == 3
    assert output["player"].tolist() == ["Player Alpha", "Player Beta"]
    assert not {
        "synthetic-player-delta",
        "synthetic-player-echo",
        "synthetic-player-zeta",
    }.intersection(output["provider_player_id"])


def test_does_not_overwrite_existing_output_without_force(tmp_path):
    output_path = tmp_path / "mapped.csv"
    output_path.write_text("do not replace", encoding="utf-8")

    result = apply_provider_identity_mapping_cli(
        RECORDS_SAMPLE,
        MAPPING_SAMPLE,
        output_path,
    )

    assert result["written"] is False
    assert "already exists" in str(result["error"])
    assert output_path.read_text(encoding="utf-8") == "do not replace"


def test_force_overwrites_existing_output(tmp_path):
    output_path = tmp_path / "mapped.csv"
    output_path.write_text("replace me", encoding="utf-8")

    result = apply_provider_identity_mapping_cli(
        RECORDS_SAMPLE,
        MAPPING_SAMPLE,
        output_path,
        force=True,
    )

    output = pd.read_csv(output_path, keep_default_na=False)
    assert result["written"] is True
    assert output["player"].tolist() == ["Player Alpha", "Player Beta"]


def test_missing_records_input_returns_readable_error_without_output(tmp_path):
    output_path = tmp_path / "mapped.csv"

    result = apply_provider_identity_mapping_cli(
        tmp_path / "missing-records.csv",
        MAPPING_SAMPLE,
        output_path,
    )

    assert result["written"] is False
    assert "Records CSV could not be read" in str(result["error"])
    assert not output_path.exists()


def test_invalid_mapping_returns_error_without_output(tmp_path):
    mapping_path = tmp_path / "invalid-mapping.csv"
    output_path = tmp_path / "mapped.csv"
    mapping = pd.read_csv(MAPPING_SAMPLE, keep_default_na=False)
    mapping.loc[0, "match_status"] = "invalid"
    mapping.to_csv(mapping_path, index=False)

    result = apply_provider_identity_mapping_cli(
        RECORDS_SAMPLE,
        mapping_path,
        output_path,
    )

    assert result["written"] is False
    assert "Invalid provider identity mapping" in str(result["error"])
    assert not output_path.exists()


def test_main_returns_zero_and_prints_summary_for_valid_samples(tmp_path, capsys):
    output_path = tmp_path / "mapped.csv"

    exit_code = main(
        [
            "--records",
            str(RECORDS_SAMPLE),
            "--mapping",
            str(MAPPING_SAMPLE),
            "--output",
            str(output_path),
        ]
    )

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Input record count: 5" in output
    assert "Mapped record count: 2" in output
    assert "Unmapped/excluded record count: 3" in output
    assert "Written: yes" in output


def test_main_returns_one_on_error(tmp_path):
    exit_code = main(
        [
            "--records",
            str(tmp_path / "missing.csv"),
            "--mapping",
            str(MAPPING_SAMPLE),
            "--output",
            str(tmp_path / "mapped.csv"),
        ]
    )

    assert exit_code == 1


def test_output_preserves_expected_columns_without_internal_mapping_columns(tmp_path):
    output_path = tmp_path / "mapped.csv"

    result = apply_provider_identity_mapping_cli(
        RECORDS_SAMPLE,
        MAPPING_SAMPLE,
        output_path,
    )

    expected_columns = {
        "provider_name",
        "provider_player_id",
        "provider_team_id",
        "provider_league_id",
        "provider_season",
        "age",
        "market_value_eur",
        "contract_end_date",
        "source",
        "source_url",
        "confidence",
        "notes",
        "player",
        "team",
        "league",
        "season",
        "identity_mapping_confidence",
        "identity_mapping_reviewed_by",
        "identity_mapping_reviewed_at",
        "identity_mapping_notes",
    }
    internal_columns = {
        "local_player",
        "local_team",
        "local_league",
        "local_season",
        "match_status",
    }

    assert expected_columns.issubset(result["columns"])
    assert not internal_columns.intersection(result["columns"])
