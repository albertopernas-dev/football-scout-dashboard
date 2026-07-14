from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.provider_identity_mapping import (
    PROVIDER_IDENTITY_MAPPING_COLUMNS,
    PROVIDER_RECORD_IDENTITY_COLUMNS,
    apply_provider_identity_mapping_to_records,
    find_duplicate_provider_identity_mappings,
    load_provider_identity_mapping_csv,
    required_provider_identity_mapping_columns,
    split_provider_identity_mapping_by_status,
    validate_provider_identity_mapping_df,
    validate_provider_identity_mapping_schema,
    validate_provider_identity_mapping_values,
)
from src.provider_market_context import (
    build_canonical_market_context_df,
    validate_canonical_market_context_df,
)


def _row(**overrides: object) -> dict[str, object]:
    row = {
        "provider_name": "Synthetic Provider",
        "provider_player_id": "synthetic-player-alpha",
        "provider_team_id": "synthetic-team-red",
        "provider_league_id": "synthetic-league",
        "provider_season": 2024,
        "local_player": "Player Alpha",
        "local_team": "Team Red",
        "local_league": "Synthetic League",
        "local_season": 2024,
        "match_status": "matched",
        "confidence": "high",
        "reviewed_by": "synthetic-reviewer",
        "reviewed_at": "2026-01-01",
        "notes": "Synthetic reviewed mapping.",
    }
    row.update(overrides)
    return row


def _df(rows: list[dict[str, object]]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=PROVIDER_IDENTITY_MAPPING_COLUMNS)


def _provider_record(**overrides: object) -> dict[str, object]:
    record = {
        "provider_name": "Synthetic Provider",
        "provider_player_id": "synthetic-player-alpha",
        "provider_team_id": "synthetic-team-red",
        "provider_league_id": "synthetic-league",
        "provider_season": 2024,
        "provider_player_name": "Provider Alpha",
        "provider_team_name": "Provider Red",
        "age": "",
        "market_value_eur": "",
        "contract_end_date": "",
        "source": "",
        "source_url": "",
        "confidence": "",
        "notes": "",
    }
    record.update(overrides)
    return record


def test_required_provider_identity_mapping_columns_returns_expected_list():
    assert required_provider_identity_mapping_columns() == PROVIDER_IDENTITY_MAPPING_COLUMNS


def test_validate_schema_accepts_required_columns():
    assert validate_provider_identity_mapping_schema(_df([_row()])) == []


def test_validate_schema_reports_missing_column():
    df = _df([_row()]).drop(columns=["provider_player_id"])

    errors = validate_provider_identity_mapping_schema(df)

    assert errors == ["Missing required provider identity mapping column: provider_player_id"]


def test_validate_values_accepts_valid_status_rows():
    df = _df(
        [
            _row(match_status="matched", confidence="high"),
            _row(
                provider_player_id="synthetic-player-delta",
                local_player="",
                local_team="",
                local_league="",
                local_season="",
                match_status="unmatched",
                confidence="low",
            ),
            _row(
                provider_player_id="synthetic-player-echo",
                match_status="ambiguous",
                confidence="low",
            ),
            _row(
                provider_player_id="synthetic-player-zeta",
                local_player="",
                local_team="",
                local_league="",
                local_season="",
                match_status="rejected",
                confidence="low",
            ),
        ]
    )

    assert validate_provider_identity_mapping_values(df) == []


def test_validate_values_rejects_invalid_match_status():
    errors = validate_provider_identity_mapping_values(_df([_row(match_status="maybe")]))

    assert any("Row 2: match_status must be one of" in error for error in errors)


def test_validate_values_rejects_invalid_confidence():
    errors = validate_provider_identity_mapping_values(_df([_row(confidence="certain")]))

    assert any("Row 2: confidence must be one of" in error for error in errors)


def test_validate_values_rejects_invalid_reviewed_at():
    errors = validate_provider_identity_mapping_values(_df([_row(reviewed_at="01/01/2026")]))

    assert any("Row 2: reviewed_at must be empty or ISO YYYY-MM-DD." in error for error in errors)


def test_matched_requires_local_fields():
    errors = validate_provider_identity_mapping_values(
        _df(
            [
                _row(
                    local_player="",
                    local_team="",
                    local_league="",
                    local_season="",
                )
            ]
        )
    )

    assert any("Row 2: local_player is required when match_status is matched." in error for error in errors)
    assert any("Row 2: local_team is required when match_status is matched." in error for error in errors)
    assert any("Row 2: local_league is required when match_status is matched." in error for error in errors)
    assert any("Row 2: local_season is required when match_status is matched." in error for error in errors)


def test_ambiguous_high_confidence_is_invalid():
    errors = validate_provider_identity_mapping_values(
        _df([_row(match_status="ambiguous", confidence="high")])
    )

    assert any("Row 2: ambiguous mappings cannot have high confidence." in error for error in errors)


def test_validate_df_stops_after_schema_errors():
    df = _df([_row()]).drop(columns=["match_status"])

    errors = validate_provider_identity_mapping_df(df)

    assert errors == ["Missing required provider identity mapping column: match_status"]


def test_split_provider_identity_mapping_by_status_returns_all_groups_with_reset_indexes():
    df = _df(
        [
            _row(provider_player_id="matched-1", match_status="matched"),
            _row(provider_player_id="matched-2", match_status="matched"),
            _row(provider_player_id="unmatched-1", match_status="unmatched", confidence="low"),
            _row(provider_player_id="ambiguous-1", match_status="ambiguous", confidence="low"),
            _row(provider_player_id="rejected-1", match_status="rejected", confidence="low"),
        ]
    )

    groups = split_provider_identity_mapping_by_status(df)

    assert set(groups) == {"matched", "unmatched", "ambiguous", "rejected"}
    assert len(groups["matched"]) == 2
    assert len(groups["unmatched"]) == 1
    assert len(groups["ambiguous"]) == 1
    assert len(groups["rejected"]) == 1
    assert groups["matched"].index.tolist() == [0, 1]


def test_find_duplicate_provider_identity_mappings_returns_duplicate_matched_rows_only():
    duplicate = _row(provider_player_id="same-player")
    df = _df(
        [
            duplicate,
            {**duplicate, "local_player": "Player Alpha Duplicate"},
            _row(
                provider_player_id="same-unmatched",
                match_status="unmatched",
                confidence="low",
                local_player="",
                local_team="",
                local_league="",
                local_season="",
            ),
            _row(
                provider_player_id="same-unmatched",
                match_status="unmatched",
                confidence="low",
                local_player="",
                local_team="",
                local_league="",
                local_season="",
            ),
        ]
    )

    duplicates = find_duplicate_provider_identity_mappings(df)

    assert len(duplicates) == 2
    assert duplicates["provider_player_id"].tolist() == ["same-player", "same-player"]
    assert duplicates.index.tolist() == [0, 1]


def test_find_duplicate_provider_identity_mappings_returns_empty_when_columns_missing():
    df = _df([_row()]).drop(columns=["provider_player_id"])

    duplicates = find_duplicate_provider_identity_mappings(df)

    assert duplicates.empty
    assert duplicates.columns.tolist() == df.columns.tolist()


def test_load_provider_identity_mapping_csv_uses_empty_strings_for_missing_values(tmp_path):
    csv_path = tmp_path / "mapping.csv"
    _df([_row(local_player="")]).to_csv(csv_path, index=False)

    loaded = load_provider_identity_mapping_csv(csv_path)

    assert loaded.loc[0, "local_player"] == ""


def test_versioned_synthetic_sample_is_valid():
    sample_path = (
        Path(__file__).resolve().parents[1]
        / "docs"
        / "examples"
        / "provider_identity_mapping_sample.csv"
    )
    sample = pd.read_csv(sample_path, keep_default_na=False)

    assert validate_provider_identity_mapping_df(sample) == []
    groups = split_provider_identity_mapping_by_status(sample)
    assert len(groups["matched"]) == 2
    assert len(groups["unmatched"]) == 1
    assert len(groups["ambiguous"]) == 1
    assert len(groups["rejected"]) == 1
    assert find_duplicate_provider_identity_mappings(sample).empty


def test_apply_provider_identity_mapping_maps_matched_records_only():
    records = pd.DataFrame(
        [
            _provider_record(),
            _provider_record(
                provider_player_id="synthetic-player-beta",
                provider_team_id="synthetic-team-blue",
            ),
            _provider_record(
                provider_player_id="synthetic-player-delta",
                provider_team_id="synthetic-team-yellow",
            ),
        ]
    )
    mapping = _df(
        [
            _row(),
            _row(
                provider_player_id="synthetic-player-beta",
                provider_team_id="synthetic-team-blue",
                local_player="Player Beta",
                local_team="Team Blue",
            ),
            _row(
                provider_player_id="synthetic-player-delta",
                provider_team_id="synthetic-team-yellow",
                local_player="",
                local_team="",
                local_league="",
                local_season="",
                match_status="unmatched",
                confidence="low",
            ),
        ]
    )

    result = apply_provider_identity_mapping_to_records(records, mapping)

    assert result[["player", "team", "league", "season"]].to_dict("records") == [
        {
            "player": "Player Alpha",
            "team": "Team Red",
            "league": "Synthetic League",
            "season": 2024,
        },
        {
            "player": "Player Beta",
            "team": "Team Blue",
            "league": "Synthetic League",
            "season": 2024,
        },
    ]


def test_apply_provider_identity_mapping_preserves_records_and_adds_review_metadata():
    records = pd.DataFrame(
        [
            _provider_record(
                age=24,
                market_value_eur=1_500_000,
                contract_end_date="2027-06-30",
                source="synthetic_provider",
                source_url="https://example.test/player-alpha",
                confidence="medium",
                notes="Synthetic market context.",
            )
        ]
    )

    result = apply_provider_identity_mapping_to_records(records, _df([_row()]))

    for column in [
        *PROVIDER_RECORD_IDENTITY_COLUMNS,
        "age",
        "market_value_eur",
        "contract_end_date",
        "source",
        "source_url",
        "confidence",
        "notes",
    ]:
        assert result.loc[0, column] == records.loc[0, column]
    assert result.loc[0, "identity_mapping_confidence"] == "high"
    assert result.loc[0, "identity_mapping_reviewed_by"] == "synthetic-reviewer"
    assert result.loc[0, "identity_mapping_reviewed_at"] == "2026-01-01"
    assert result.loc[0, "identity_mapping_notes"] == "Synthetic reviewed mapping."


def test_apply_provider_identity_mapping_does_not_leak_internal_mapping_columns():
    result = apply_provider_identity_mapping_to_records(
        pd.DataFrame([_provider_record()]),
        _df([_row()]),
    )

    assert not {
        "local_player",
        "local_team",
        "local_league",
        "local_season",
        "match_status",
    }.intersection(result.columns)


def test_apply_provider_identity_mapping_rejects_missing_record_identity_columns():
    records = pd.DataFrame([_provider_record()]).drop(columns=["provider_player_id"])

    with pytest.raises(ValueError, match="provider_player_id"):
        apply_provider_identity_mapping_to_records(records, _df([_row()]))


def test_apply_provider_identity_mapping_rejects_existing_canonical_identity_columns():
    records = pd.DataFrame([{**_provider_record(), "player": "Existing Player"}])

    with pytest.raises(ValueError, match="canonical identity columns"):
        apply_provider_identity_mapping_to_records(records, _df([_row()]))


def test_apply_provider_identity_mapping_rejects_invalid_mapping():
    mapping = _df([_row(match_status="maybe")])

    with pytest.raises(ValueError, match="match_status must be one of"):
        apply_provider_identity_mapping_to_records(pd.DataFrame([_provider_record()]), mapping)


def test_apply_provider_identity_mapping_rejects_duplicate_matched_mapping():
    duplicate = _row()
    mapping = _df([duplicate, {**duplicate, "local_player": "Other Player"}])

    with pytest.raises(ValueError, match="duplicate matched provider identities"):
        apply_provider_identity_mapping_to_records(pd.DataFrame([_provider_record()]), mapping)


def test_apply_provider_identity_mapping_returns_empty_output_with_expected_columns():
    records = pd.DataFrame(
        [_provider_record(provider_player_id="not-reviewed", provider_team_id="unknown-team")]
    )

    result = apply_provider_identity_mapping_to_records(records, _df([_row()]))

    assert result.empty
    assert result.columns.tolist() == [
        *records.columns,
        "player",
        "team",
        "league",
        "season",
        "identity_mapping_confidence",
        "identity_mapping_reviewed_by",
        "identity_mapping_reviewed_at",
        "identity_mapping_notes",
    ]


def test_versioned_fixture_records_sample_applies_reviewed_mapping():
    examples_path = Path(__file__).resolve().parents[1] / "docs" / "examples"
    records = pd.read_csv(
        examples_path / "provider_fixture_records_sample.csv",
        keep_default_na=False,
    )
    mapping = pd.read_csv(
        examples_path / "provider_identity_mapping_sample.csv",
        keep_default_na=False,
    )

    result = apply_provider_identity_mapping_to_records(records, mapping)

    assert len(result) == 2
    assert result["player"].tolist() == ["Player Alpha", "Player Beta"]
    assert result["team"].tolist() == ["Team Red", "Team Blue"]
    assert result["league"].tolist() == ["Synthetic League", "Synthetic League"]
    assert result["season"].tolist() == [2024, 2024]
    provider_player_ids = result["provider_player_id"].tolist()
    assert "synthetic-player-delta" not in provider_player_ids
    assert "synthetic-player-echo" not in provider_player_ids
    assert "synthetic-player-zeta" not in provider_player_ids

    alpha = result.loc[result["player"] == "Player Alpha"].iloc[0]
    beta = result.loc[result["player"] == "Player Beta"].iloc[0]
    assert alpha["confidence"] == ""
    assert beta["confidence"] == "medium"
    assert beta["identity_mapping_confidence"] == "medium"

    canonical = build_canonical_market_context_df(
        result.to_dict("records"),
        include_optional_fields=True,
    )
    assert validate_canonical_market_context_df(canonical) == []
