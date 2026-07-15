from pathlib import Path

import pandas as pd
import pytest

import scripts.flatten_provider_payload_advanced_sample as flatten_script
from src.provider_payload_shapes import expected_advanced_payload_columns


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ADVANCED_PAYLOAD_SAMPLE = (
    PROJECT_ROOT / "docs" / "examples" / "provider_payload_advanced_sample.json"
)


@pytest.fixture
def isolated_project_root(tmp_path, monkeypatch):
    monkeypatch.setattr(flatten_script, "PROJECT_ROOT", tmp_path)
    return tmp_path


def test_cli_writes_flattened_local_csv(isolated_project_root):
    output = (
        isolated_project_root
        / "data"
        / "enrichment"
        / "advanced.generated.local.csv"
    )

    result = flatten_script.flatten_payload_file_to_csv(
        ADVANCED_PAYLOAD_SAMPLE,
        output,
    )

    saved = pd.read_csv(output, keep_default_na=False)
    assert len(result) == 3
    assert saved.columns.tolist() == expected_advanced_payload_columns()
    assert len(saved) == 3
    assert "synthetic-player-beta" in saved["provider_player_id"].tolist()


def test_cli_rejects_existing_output_without_force(isolated_project_root):
    output = isolated_project_root / "data" / "enrichment" / "existing.local.csv"
    output.parent.mkdir(parents=True)
    output.write_text("existing", encoding="utf-8")

    with pytest.raises(FileExistsError, match="already exists"):
        flatten_script.flatten_payload_file_to_csv(ADVANCED_PAYLOAD_SAMPLE, output)


def test_cli_allows_existing_output_with_force(isolated_project_root):
    output = isolated_project_root / "data" / "enrichment" / "existing.local.csv"
    output.parent.mkdir(parents=True)
    output.write_text("existing", encoding="utf-8")

    flatten_script.flatten_payload_file_to_csv(
        ADVANCED_PAYLOAD_SAMPLE,
        output,
        force=True,
    )

    saved = pd.read_csv(output, keep_default_na=False)
    assert len(saved) == 3


def test_cli_rejects_output_without_local_csv_suffix(isolated_project_root):
    output = isolated_project_root / "data" / "enrichment" / "bad.csv"

    with pytest.raises(ValueError, match=r"\.local\.csv"):
        flatten_script.flatten_payload_file_to_csv(ADVANCED_PAYLOAD_SAMPLE, output)


def test_cli_rejects_output_outside_data_enrichment(isolated_project_root):
    output = isolated_project_root / "outside" / "bad.local.csv"

    with pytest.raises(ValueError, match="data/enrichment"):
        flatten_script.flatten_payload_file_to_csv(ADVANCED_PAYLOAD_SAMPLE, output)


def test_cli_reports_summary(isolated_project_root, capsys):
    output = isolated_project_root / "data" / "enrichment" / "summary.local.csv"

    exit_code = flatten_script.main(
        [
            "--input",
            str(ADVANCED_PAYLOAD_SAMPLE),
            "--output",
            str(output),
        ]
    )

    stdout = capsys.readouterr().out.lower()
    assert exit_code == 0
    assert "rows: 3" in stdout
    assert "synthetic-only" in stdout
