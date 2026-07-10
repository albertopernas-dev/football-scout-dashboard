from pathlib import Path

import pandas as pd
import pytest

from scripts.export_enrichment_seed import (
    ENRICHMENT_SEED_COLUMNS,
    build_enrichment_seed_df,
    existing_csv_has_reviewed_enrichment,
    write_enrichment_seed_csv,
)


def opportunities_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "player": "Player A",
                "team": "Team A",
                "league": "LaLiga",
                "season": 2024,
                "market_context_age": 24,
                "effective_age": 24,
            },
            {
                "player": "Player A",
                "team": "Team A",
                "league": "LaLiga",
                "season": 2024,
            },
            {
                "player": "Player B",
                "team": "Team B",
                "league": "LaLiga",
                "season": 2024,
            },
        ]
    )


def test_build_enrichment_seed_df_uses_exact_schema():
    seed = build_enrichment_seed_df(opportunities_df())

    assert seed.columns.tolist() == ENRICHMENT_SEED_COLUMNS


def test_build_enrichment_seed_df_fills_identity_columns_only():
    seed = build_enrichment_seed_df(opportunities_df())

    assert seed.loc[0, "player"] == "Player A"
    assert seed.loc[0, "team"] == "Team A"
    assert seed.loc[0, "league"] == "LaLiga"
    assert seed.loc[0, "season"] == 2024
    assert seed.loc[0, "age"] == ""
    assert seed.loc[0, "market_value_eur"] == ""
    assert seed.loc[0, "contract_end_date"] == ""
    assert seed.loc[0, "source"] == ""
    assert seed.loc[0, "source_url"] == ""
    assert seed.loc[0, "confidence"] == ""
    assert seed.loc[0, "notes"] == ""


def test_build_enrichment_seed_df_does_not_use_market_context_or_effective_values():
    seed = build_enrichment_seed_df(opportunities_df())

    assert seed.loc[0, "age"] == ""
    assert "effective_age" not in seed.columns
    assert "market_context_age" not in seed.columns


def test_build_enrichment_seed_df_deduplicates_identity_keys():
    seed = build_enrichment_seed_df(opportunities_df())

    assert seed["player"].tolist() == ["Player A", "Player B"]


def test_build_enrichment_seed_df_limits_rows():
    seed = build_enrichment_seed_df(opportunities_df(), top_n=1)

    assert len(seed) == 1
    assert seed.loc[0, "player"] == "Player A"


def test_write_enrichment_seed_csv_writes_csv(tmp_path):
    output_path = tmp_path / "nested" / "seed.local.csv"
    seed = build_enrichment_seed_df(opportunities_df())

    rows_written = write_enrichment_seed_csv(seed, output_path)

    loaded = pd.read_csv(output_path, keep_default_na=False)
    assert rows_written == 2
    assert loaded.columns.tolist() == ENRICHMENT_SEED_COLUMNS
    assert loaded.loc[0, "player"] == "Player A"
    assert loaded.loc[0, "age"] == ""


def test_write_enrichment_seed_csv_does_not_overwrite_without_force(tmp_path):
    output_path = tmp_path / "seed.local.csv"
    output_path.write_text("existing", encoding="utf-8")

    with pytest.raises(FileExistsError, match="already exists"):
        write_enrichment_seed_csv(build_enrichment_seed_df(opportunities_df()), output_path)

    assert output_path.read_text(encoding="utf-8") == "existing"


def test_existing_csv_has_reviewed_enrichment_returns_false_for_missing_file(tmp_path):
    assert existing_csv_has_reviewed_enrichment(tmp_path / "missing.csv") is False


def test_existing_csv_has_reviewed_enrichment_returns_false_for_empty_seed(tmp_path):
    output_path = tmp_path / "seed.local.csv"
    write_enrichment_seed_csv(build_enrichment_seed_df(opportunities_df()), output_path)

    assert existing_csv_has_reviewed_enrichment(output_path) is False


def test_existing_csv_has_reviewed_enrichment_detects_age_value(tmp_path):
    output_path = tmp_path / "seed.local.csv"
    seed = build_enrichment_seed_df(opportunities_df())
    seed.loc[0, "age"] = "0"
    seed.to_csv(output_path, index=False, encoding="utf-8")

    assert existing_csv_has_reviewed_enrichment(output_path) is True


def test_existing_csv_has_reviewed_enrichment_detects_source_or_notes(tmp_path):
    output_path = tmp_path / "seed.local.csv"
    seed = build_enrichment_seed_df(opportunities_df())
    seed.loc[0, "notes"] = " reviewed manually "
    seed.to_csv(output_path, index=False, encoding="utf-8")

    assert existing_csv_has_reviewed_enrichment(output_path) is True


def test_existing_csv_has_reviewed_enrichment_returns_true_for_unreadable_csv(tmp_path):
    assert existing_csv_has_reviewed_enrichment(tmp_path) is True


def test_write_enrichment_seed_csv_blocks_force_when_existing_csv_has_reviewed_enrichment(tmp_path):
    output_path = tmp_path / "seed.local.csv"
    seed = build_enrichment_seed_df(opportunities_df())
    seed.loc[0, "source"] = "manual_review"
    seed.to_csv(output_path, index=False, encoding="utf-8")

    with pytest.raises(FileExistsError, match="contains reviewed enrichment data"):
        write_enrichment_seed_csv(build_enrichment_seed_df(opportunities_df()), output_path, force=True)

    loaded = pd.read_csv(output_path, keep_default_na=False)
    assert loaded.loc[0, "source"] == "manual_review"


def test_write_enrichment_seed_csv_overwrites_with_force_when_no_reviewed_enrichment(tmp_path):
    output_path = tmp_path / "seed.local.csv"
    write_enrichment_seed_csv(build_enrichment_seed_df(opportunities_df()), output_path)

    rows_written = write_enrichment_seed_csv(
        build_enrichment_seed_df(opportunities_df()),
        output_path,
        force=True,
    )

    loaded = pd.read_csv(output_path, keep_default_na=False)
    assert rows_written == 2
    assert loaded.loc[0, "player"] == "Player A"


def test_write_enrichment_seed_csv_overwrites_reviewed_enrichment_with_dangerous_flag(tmp_path):
    output_path = tmp_path / "seed.local.csv"
    seed = build_enrichment_seed_df(opportunities_df())
    seed.loc[0, "confidence"] = "medium"
    seed.to_csv(output_path, index=False, encoding="utf-8")

    rows_written = write_enrichment_seed_csv(
        build_enrichment_seed_df(opportunities_df()),
        output_path,
        force_dangerously_overwrite_reviewed_data=True,
    )

    loaded = pd.read_csv(output_path, keep_default_na=False)
    assert rows_written == 2
    assert loaded.loc[0, "confidence"] == ""
