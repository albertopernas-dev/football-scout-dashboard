from pathlib import Path

import pandas as pd
import pytest

import scripts.flatten_provider_payload_advanced_sample as flatten_script
import scripts.run_advanced_provider_payload_demo as demo_script
from src.provider_market_context import validate_canonical_market_context_df


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ADVANCED_PAYLOAD_SAMPLE = (
    PROJECT_ROOT / "docs" / "examples" / "provider_payload_advanced_sample.json"
)
ADVANCED_MAPPING_SAMPLE = (
    PROJECT_ROOT
    / "docs"
    / "examples"
    / "provider_advanced_identity_mapping_sample.csv"
)


@pytest.fixture
def isolated_project_root(tmp_path, monkeypatch):
    monkeypatch.setattr(demo_script, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(flatten_script, "PROJECT_ROOT", tmp_path)
    return tmp_path


def _output_paths(project_root: Path) -> tuple[Path, Path, Path]:
    enrichment = project_root / "data" / "enrichment"
    return (
        enrichment / "flattened.generated.local.csv",
        enrichment / "mapped.generated.local.csv",
        enrichment / "canonical.generated.local.csv",
    )


def _run_demo(project_root: Path, force: bool = False) -> dict[str, object]:
    flattened, mapped, canonical = _output_paths(project_root)
    return demo_script.run_advanced_provider_payload_demo(
        ADVANCED_PAYLOAD_SAMPLE,
        ADVANCED_MAPPING_SAMPLE,
        flattened,
        mapped,
        canonical,
        include_optional_fields=True,
        force=force,
    )


def test_demo_writes_flattened_mapped_and_canonical_outputs(isolated_project_root):
    flattened_path, mapped_path, canonical_path = _output_paths(isolated_project_root)

    result = _run_demo(isolated_project_root)

    flattened = pd.read_csv(flattened_path, keep_default_na=False)
    mapped = pd.read_csv(mapped_path, keep_default_na=False)
    canonical = pd.read_csv(canonical_path, keep_default_na=False)
    assert len(flattened) == 3
    assert len(mapped) == 2
    assert len(canonical) == 2
    assert result["flattened_row_count"] == 3
    assert result["mapped_row_count"] == 2
    assert result["excluded_row_count"] == 1
    assert result["canonical_row_count"] == 2
    assert result["canonical_validation_errors"] == []
    assert validate_canonical_market_context_df(canonical) == []


def test_demo_rejects_existing_outputs_without_force(isolated_project_root):
    flattened_path, mapped_path, canonical_path = _output_paths(isolated_project_root)
    mapped_path.parent.mkdir(parents=True)
    mapped_path.write_text("existing", encoding="utf-8")

    with pytest.raises(FileExistsError, match="already exists"):
        _run_demo(isolated_project_root)

    assert not flattened_path.exists()
    assert mapped_path.read_text(encoding="utf-8") == "existing"
    assert not canonical_path.exists()


def test_demo_allows_existing_outputs_with_force(isolated_project_root):
    outputs = _output_paths(isolated_project_root)
    outputs[0].parent.mkdir(parents=True)
    for output in outputs:
        output.write_text("existing", encoding="utf-8")

    result = _run_demo(isolated_project_root, force=True)

    assert result["canonical_row_count"] == 2
    assert all(len(pd.read_csv(output)) > 0 for output in outputs)


def test_demo_rejects_output_without_local_csv_suffix(isolated_project_root):
    flattened, mapped, _ = _output_paths(isolated_project_root)
    bad_canonical = isolated_project_root / "data" / "enrichment" / "bad.csv"

    with pytest.raises(ValueError, match=r"\.local\.csv"):
        demo_script.run_advanced_provider_payload_demo(
            ADVANCED_PAYLOAD_SAMPLE,
            ADVANCED_MAPPING_SAMPLE,
            flattened,
            mapped,
            bad_canonical,
        )


def test_demo_rejects_output_outside_data_enrichment(isolated_project_root):
    flattened, mapped, _ = _output_paths(isolated_project_root)
    outside = isolated_project_root / "outside" / "canonical.local.csv"

    with pytest.raises(ValueError, match="data/enrichment"):
        demo_script.run_advanced_provider_payload_demo(
            ADVANCED_PAYLOAD_SAMPLE,
            ADVANCED_MAPPING_SAMPLE,
            flattened,
            mapped,
            outside,
        )


def test_demo_reports_summary(isolated_project_root, capsys):
    flattened, mapped, canonical = _output_paths(isolated_project_root)

    exit_code = demo_script.main(
        [
            "--input",
            str(ADVANCED_PAYLOAD_SAMPLE),
            "--mapping",
            str(ADVANCED_MAPPING_SAMPLE),
            "--flattened-output",
            str(flattened),
            "--mapped-output",
            str(mapped),
            "--canonical-output",
            str(canonical),
            "--include-optional-fields",
        ]
    )

    stdout = capsys.readouterr().out.lower()
    assert exit_code == 0
    assert "flattened rows: 3" in stdout
    assert "mapped rows: 2" in stdout
    assert "canonical rows: 2" in stdout
    assert "synthetic-only" in stdout


def test_demo_does_not_write_partial_outputs_when_precheck_fails(
    isolated_project_root,
):
    flattened_path, mapped_path, canonical_path = _output_paths(isolated_project_root)
    canonical_path.parent.mkdir(parents=True)
    canonical_path.write_text("protected", encoding="utf-8")

    with pytest.raises(FileExistsError):
        _run_demo(isolated_project_root)

    assert not flattened_path.exists()
    assert not mapped_path.exists()
    assert canonical_path.read_text(encoding="utf-8") == "protected"
