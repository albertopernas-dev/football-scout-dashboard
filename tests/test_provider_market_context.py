import pandas as pd

from src.provider_market_context import (
    CANONICAL_MARKET_CONTEXT_COLUMNS,
    OPTIONAL_PROVIDER_CONTEXT_COLUMNS,
    build_canonical_market_context_df,
    canonicalize_provider_record,
    validate_canonical_market_context_df,
)


def test_build_canonical_market_context_df_empty_records_returns_canonical_columns():
    df = build_canonical_market_context_df([])

    assert df.empty
    assert df.columns.tolist() == CANONICAL_MARKET_CONTEXT_COLUMNS


def test_build_canonical_market_context_df_full_record_returns_columns_in_order():
    df = build_canonical_market_context_df(
        [
            {
                "player": "Player A",
                "team": "Team A",
                "league": "LaLiga",
                "season": 2024,
                "age": 24,
                "market_value_eur": 1500000,
                "contract_end_date": "2027-06-30",
                "source": "manual_review",
                "source_url": "https://example.test/player-a",
                "confidence": "medium",
                "notes": "Synthetic test row.",
            }
        ]
    )

    assert df.columns.tolist() == CANONICAL_MARKET_CONTEXT_COLUMNS
    assert df.loc[0, "player"] == "Player A"
    assert df.loc[0, "age"] == 24
    assert df.loc[0, "market_value_eur"] == 1500000


def test_canonicalize_provider_record_ignores_extra_fields():
    row = canonicalize_provider_record(
        {
            "player": "Player A",
            "team": "Team A",
            "league": "LaLiga",
            "season": 2024,
            "provider_secret": "ignored",
        }
    )

    assert "provider_secret" not in row
    assert list(row) == CANONICAL_MARKET_CONTEXT_COLUMNS


def test_canonicalize_provider_record_fills_missing_fields_with_empty_string():
    row = canonicalize_provider_record({"player": "Player A"})

    assert row["player"] == "Player A"
    assert row["team"] == ""
    assert row["confidence"] == ""


def test_include_optional_fields_adds_provider_columns_in_order():
    df = build_canonical_market_context_df(
        [
            {
                "player": "Player A",
                "provider_player_id": "provider-player-1",
                "provider_team_id": "provider-team-1",
                "provider_name": "Synthetic Provider",
                "fetched_at": "2026-01-01T00:00:00Z",
                "value_date": "2026-01-01",
                "contract_option_notes": "Synthetic option note.",
                "license_scope": "local_test",
            }
        ],
        include_optional_fields=True,
    )

    assert df.columns.tolist() == [
        *CANONICAL_MARKET_CONTEXT_COLUMNS,
        *OPTIONAL_PROVIDER_CONTEXT_COLUMNS,
    ]
    assert df.loc[0, "provider_player_id"] == "provider-player-1"


def test_optional_fields_are_excluded_by_default():
    row = canonicalize_provider_record(
        {
            "player": "Player A",
            "provider_player_id": "provider-player-1",
        }
    )

    assert "provider_player_id" not in row


def test_does_not_invent_source_or_confidence():
    df = build_canonical_market_context_df(
        [{"player": "Player A", "team": "Team A", "league": "LaLiga", "season": 2024}]
    )

    assert df.loc[0, "source"] == ""
    assert df.loc[0, "confidence"] == ""


def test_does_not_convert_unknowns_to_zero():
    df = build_canonical_market_context_df(
        [
            {
                "player": "Player A",
                "team": "Team A",
                "league": "LaLiga",
                "season": 2024,
                "age": None,
                "market_value_eur": pd.NA,
            }
        ]
    )

    assert df.loc[0, "age"] == ""
    assert df.loc[0, "market_value_eur"] == ""


def test_validate_canonical_market_context_df_accepts_identity_only_row():
    df = build_canonical_market_context_df(
        [{"player": "Player A", "team": "Team A", "league": "LaLiga", "season": 2024}]
    )

    assert validate_canonical_market_context_df(df) == []


def test_validate_canonical_market_context_df_rejects_enrichment_without_source_confidence():
    df = build_canonical_market_context_df(
        [
            {
                "player": "Player A",
                "team": "Team A",
                "league": "LaLiga",
                "season": 2024,
                "age": 24,
            }
        ]
    )

    errors = validate_canonical_market_context_df(df)

    assert any("source is required" in error for error in errors)
    assert any("confidence is required" in error for error in errors)


def test_validate_canonical_market_context_df_rejects_non_iso_contract_date():
    df = build_canonical_market_context_df(
        [
            {
                "player": "Player A",
                "team": "Team A",
                "league": "LaLiga",
                "season": 2024,
                "contract_end_date": "30/06/2027",
                "source": "manual_review",
                "confidence": "medium",
            }
        ]
    )

    errors = validate_canonical_market_context_df(df)

    assert any("contract_end_date" in error and "ISO" in error for error in errors)


def test_validate_canonical_market_context_df_accepts_valid_enrichment_row():
    df = build_canonical_market_context_df(
        [
            {
                "player": "Player A",
                "team": "Team A",
                "league": "LaLiga",
                "season": 2024,
                "age": 24,
                "market_value_eur": 1500000,
                "contract_end_date": "2027-06-30",
                "source": "manual_review",
                "confidence": "medium",
            }
        ]
    )

    assert validate_canonical_market_context_df(df) == []
