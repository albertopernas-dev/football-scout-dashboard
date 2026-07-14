from __future__ import annotations

from pathlib import Path

import pandas as pd

from scripts.run_provider_fixture_prototype_demo import (
    main,
    run_provider_fixture_prototype_demo,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RECORDS_SAMPLE = PROJECT_ROOT / "docs" / "examples" / "provider_fixture_records_sample.csv"
MAPPING_SAMPLE = PROJECT_ROOT / "docs" / "examples" / "provider_identity_mapping_sample.csv"


def _demo_paths(tmp_path: Path) -> tuple[Path, Path]:
    return tmp_path / "mapped.csv", tmp_path / "canonical.csv"


def _valid_cli_args(mapped_path: Path, canonical_path: Path) -> list[str]:
    return [
        "--records",
        str(RECORDS_SAMPLE),
        "--mapping",
        str(MAPPING_SAMPLE),
        "--mapped-output",
        str(mapped_path),
        "--canonical-output",
        str(canonical_path),
        "--include-optional-fields",
    ]


def test_runs_versioned_samples_end_to_end(tmp_path):
    mapped_path, canonical_path = _demo_paths(tmp_path / "nested")

    result = run_provider_fixture_prototype_demo(
        RECORDS_SAMPLE,
        MAPPING_SAMPLE,
        mapped_path,
        canonical_path,
        include_optional_fields=True,
    )

    canonical = pd.read_csv(canonical_path, keep_default_na=False)
    assert result["mapped_written"] is True
    assert result["canonical_written"] is True
    assert result["input_record_count"] == 5
    assert result["mapped_record_count"] == 2
    assert result["excluded_record_count"] == 3
    assert result["canonical_row_count"] == 2
    assert result["canonical_validation_errors"] == []
    assert mapped_path.exists()
    assert canonical_path.exists()
    assert canonical["player"].tolist() == ["Player Alpha", "Player Beta"]


def test_does_not_overwrite_mapped_output_without_force(tmp_path):
    mapped_path, canonical_path = _demo_paths(tmp_path)
    mapped_path.write_text("keep mapped", encoding="utf-8")

    result = run_provider_fixture_prototype_demo(
        RECORDS_SAMPLE,
        MAPPING_SAMPLE,
        mapped_path,
        canonical_path,
    )

    assert "already exists" in str(result["error"])
    assert result["mapped_written"] is False
    assert result["canonical_written"] is False
    assert mapped_path.read_text(encoding="utf-8") == "keep mapped"
    assert not canonical_path.exists()


def test_does_not_touch_any_output_when_canonical_exists_without_force(tmp_path):
    mapped_path, canonical_path = _demo_paths(tmp_path)
    canonical_path.write_text("keep canonical", encoding="utf-8")

    result = run_provider_fixture_prototype_demo(
        RECORDS_SAMPLE,
        MAPPING_SAMPLE,
        mapped_path,
        canonical_path,
    )

    assert "already exists" in str(result["error"])
    assert result["mapped_written"] is False
    assert result["canonical_written"] is False
    assert not mapped_path.exists()
    assert canonical_path.read_text(encoding="utf-8") == "keep canonical"


def test_invalid_mapping_stops_before_canonical_build(tmp_path):
    mapped_path, canonical_path = _demo_paths(tmp_path)
    mapping_path = tmp_path / "invalid-mapping.csv"
    mapping = pd.read_csv(MAPPING_SAMPLE, keep_default_na=False)
    mapping.loc[0, "match_status"] = "invalid"
    mapping.to_csv(mapping_path, index=False)

    result = run_provider_fixture_prototype_demo(
        RECORDS_SAMPLE,
        mapping_path,
        mapped_path,
        canonical_path,
    )

    assert "Invalid provider identity mapping" in str(result["error"])
    assert result["mapped_written"] is False
    assert result["canonical_written"] is False
    assert not mapped_path.exists()
    assert not canonical_path.exists()


def test_canonical_validation_failure_keeps_mapped_output_only(tmp_path):
    mapped_path, canonical_path = _demo_paths(tmp_path)
    records_path = tmp_path / "invalid-context-records.csv"
    records = pd.DataFrame(
        [
            {
                "provider_name": "Synthetic Provider",
                "provider_player_id": "synthetic-player-alpha",
                "provider_team_id": "synthetic-team-red",
                "provider_league_id": "synthetic-league",
                "provider_season": 2024,
                "provider_player_name": "Provider Alpha",
                "provider_team_name": "Provider Red",
                "age": 24,
                "market_value_eur": "",
                "contract_end_date": "",
                "source": "",
                "source_url": "",
                "confidence": "",
                "notes": "",
            }
        ]
    )
    records.to_csv(records_path, index=False)

    result = run_provider_fixture_prototype_demo(
        records_path,
        MAPPING_SAMPLE,
        mapped_path,
        canonical_path,
    )

    assert result["mapped_written"] is True
    assert result["canonical_written"] is False
    assert result["canonical_validation_errors"]
    assert any("source is required" in error for error in result["canonical_validation_errors"])
    assert mapped_path.exists()
    assert not canonical_path.exists()


def test_main_returns_zero_for_valid_demo(tmp_path):
    mapped_path, canonical_path = _demo_paths(tmp_path)

    assert main(_valid_cli_args(mapped_path, canonical_path)) == 0


def test_main_returns_one_on_error(tmp_path):
    mapped_path, canonical_path = _demo_paths(tmp_path)
    canonical_path.write_text("existing", encoding="utf-8")

    assert main(_valid_cli_args(mapped_path, canonical_path)) == 1


def test_main_prints_end_to_end_summary(tmp_path, capsys):
    mapped_path, canonical_path = _demo_paths(tmp_path)

    exit_code = main(_valid_cli_args(mapped_path, canonical_path))

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Input record count: 5" in output
    assert "Mapped record count: 2" in output
    assert "Excluded record count: 3" in output
    assert "Canonical row count: 2" in output
    assert "Canonical validation error count: 0" in output
    assert "Written mapped: yes" in output
    assert "Written canonical: yes" in output
