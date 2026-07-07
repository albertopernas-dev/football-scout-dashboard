from pathlib import Path

import pandas as pd
import pytest

from src.market_context import (
    load_market_context_csv,
    normalize_market_context_key,
    required_market_context_columns,
    validate_market_context_df,
    validate_market_context_schema,
    validate_market_context_values,
)


EXPECTED_COLUMNS = [
    "player",
    "team",
    "league",
    "season",
    "age",
    "market_value_eur",
    "contract_end_date",
    "source",
    "source_url",
    "confidence",
    "notes",
]


def base_market_context_df(**overrides):
    row = {
        "player": "Test Player",
        "team": "Test FC",
        "league": "Test League",
        "season": 2024,
        "age": 24,
        "market_value_eur": 1_500_000,
        "contract_end_date": "2026-06-30",
        "source": "manual_review",
        "source_url": "https://example.com/player",
        "confidence": "medium",
        "notes": "synthetic row",
    }
    row.update(overrides)
    return pd.DataFrame([row])


def test_required_market_context_columns_returns_expected_list():
    assert required_market_context_columns() == EXPECTED_COLUMNS


def test_validate_market_context_schema_accepts_valid_schema():
    errors = validate_market_context_schema(base_market_context_df())

    assert errors == []


def test_validate_market_context_schema_reports_missing_columns():
    df = base_market_context_df().drop(columns=["source", "confidence"])

    errors = validate_market_context_schema(df)

    assert any("source" in error for error in errors)
    assert any("confidence" in error for error in errors)


def test_validate_market_context_schema_allows_extra_columns():
    df = base_market_context_df(extra_column="allowed")

    errors = validate_market_context_schema(df)

    assert errors == []


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, ""),
        (pd.NA, ""),
        ("  Test   Player  ", "test player"),
        ("Vinícius Júnior", "vinicius junior"),
        ("Álvaro   Núñez", "alvaro nunez"),
    ],
)
def test_normalize_market_context_key(value, expected):
    assert normalize_market_context_key(value) == expected


@pytest.mark.parametrize("age", ["", None, pd.NA, 15, 45, "24"])
def test_validate_market_context_values_accepts_valid_age(age):
    df = base_market_context_df(age=age)

    assert validate_market_context_values(df) == []


@pytest.mark.parametrize("age", [14, 46, "young"])
def test_validate_market_context_values_rejects_invalid_age(age):
    df = base_market_context_df(age=age)

    errors = validate_market_context_values(df)

    assert any("age" in error for error in errors)


@pytest.mark.parametrize("market_value", ["", None, pd.NA, 1, 1_500_000, "2500000"])
def test_validate_market_context_values_accepts_valid_market_value(market_value):
    df = base_market_context_df(market_value_eur=market_value)

    assert validate_market_context_values(df) == []


@pytest.mark.parametrize("market_value", [0, -1, "expensive"])
def test_validate_market_context_values_rejects_invalid_market_value(market_value):
    df = base_market_context_df(market_value_eur=market_value)

    errors = validate_market_context_values(df)

    assert any("market_value_eur" in error for error in errors)


@pytest.mark.parametrize("contract_end_date", ["", None, pd.NA, "2026-06-30", "30/06/2026"])
def test_validate_market_context_values_accepts_valid_contract_date(contract_end_date):
    df = base_market_context_df(contract_end_date=contract_end_date)

    assert validate_market_context_values(df) == []


def test_validate_market_context_values_rejects_invalid_contract_date():
    df = base_market_context_df(contract_end_date="not a date")

    errors = validate_market_context_values(df)

    assert any("contract_end_date" in error for error in errors)


@pytest.mark.parametrize("confidence", ["", None, pd.NA, "low", "medium", "high", " HIGH "])
def test_validate_market_context_values_accepts_valid_confidence(confidence):
    df = base_market_context_df(confidence=confidence)

    assert validate_market_context_values(df) == []


def test_validate_market_context_values_rejects_invalid_confidence():
    df = base_market_context_df(confidence="certain")

    errors = validate_market_context_values(df)

    assert any("confidence" in error for error in errors)


@pytest.mark.parametrize(
    "enrichment_column",
    ["age", "market_value_eur", "contract_end_date"],
)
def test_validate_market_context_values_requires_source_when_enriched(enrichment_column):
    values = {"age": "", "market_value_eur": "", "contract_end_date": "", "source": ""}
    values[enrichment_column] = {
        "age": 24,
        "market_value_eur": 1_500_000,
        "contract_end_date": "2026-06-30",
    }[enrichment_column]
    df = base_market_context_df(**values)

    errors = validate_market_context_values(df)

    assert any("source" in error for error in errors)


@pytest.mark.parametrize("required_key", ["player", "team", "league", "season"])
def test_validate_market_context_values_requires_match_keys_for_non_empty_rows(required_key):
    df = base_market_context_df(**{required_key: ""})

    errors = validate_market_context_values(df)

    assert any(required_key in error for error in errors)


def test_validate_market_context_values_allows_fully_empty_rows():
    df = pd.DataFrame([{column: "" for column in EXPECTED_COLUMNS}])

    assert validate_market_context_values(df) == []


def test_validate_market_context_df_combines_schema_and_value_errors():
    df = base_market_context_df(age=14).drop(columns=["notes"])

    errors = validate_market_context_df(df)

    assert any("notes" in error for error in errors)
    assert any("age" in error for error in errors)


def test_load_market_context_csv_adds_match_keys_and_preserves_display_values():
    path = Path("tests/fixtures/market_context_valid.csv")

    df, errors = load_market_context_csv(path)

    assert errors == []
    assert "player_match_key" in df.columns
    assert "team_match_key" in df.columns
    assert "league_match_key" in df.columns
    assert df.loc[0, "player"] == "Test Player One"
    assert df.loc[1, "player"] == "  Test   Player Two  "
    assert df.loc[1, "player_match_key"] == "test player two"
    assert df.loc[0, "team_match_key"] == "test fc"
    assert df.loc[0, "league_match_key"] == "test league"


def test_load_market_context_csv_returns_validation_errors_for_invalid_csv():
    path = Path("tests/fixtures/market_context_invalid.csv")

    _, errors = load_market_context_csv(path)

    assert any("age" in error for error in errors)
    assert any("market_value_eur" in error for error in errors)
    assert any("confidence" in error for error in errors)


def test_load_market_context_csv_raises_for_missing_file(tmp_path):
    missing_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_market_context_csv(missing_path)
