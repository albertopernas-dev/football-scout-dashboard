from __future__ import annotations

import re
import unicodedata
import warnings
from pathlib import Path
from typing import Any

import pandas as pd


MARKET_CONTEXT_COLUMNS = [
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

CONFIDENCE_VALUES = {"low", "medium", "high"}
MATCH_KEY_COLUMNS = {
    "player": "player_match_key",
    "team": "team_match_key",
    "league": "league_match_key",
}


def required_market_context_columns() -> list[str]:
    return list(MARKET_CONTEXT_COLUMNS)


def normalize_market_context_key(value: object) -> str:
    if _is_empty(value):
        return ""
    text = str(value).strip().lower()
    normalized = unicodedata.normalize("NFKD", text)
    without_diacritics = "".join(
        character for character in normalized if not unicodedata.combining(character)
    )
    return re.sub(r"\s+", " ", without_diacritics).strip()


def validate_market_context_schema(df: pd.DataFrame) -> list[str]:
    errors: list[str] = []
    missing_columns = [column for column in MARKET_CONTEXT_COLUMNS if column not in df.columns]
    for column in missing_columns:
        errors.append(f"Missing required market context column: {column}")
    return errors


def validate_market_context_values(df: pd.DataFrame) -> list[str]:
    errors: list[str] = []
    for row_number, row in df.iterrows():
        if _is_empty_row(row):
            continue

        display_row_number = int(row_number) + 2
        _validate_required_match_keys(row, display_row_number, errors)
        _validate_age(row.get("age"), display_row_number, errors)
        _validate_market_value(row.get("market_value_eur"), display_row_number, errors)
        _validate_contract_end_date(row.get("contract_end_date"), display_row_number, errors)
        _validate_confidence(row.get("confidence"), display_row_number, errors)
        _validate_source_for_enrichment(row, display_row_number, errors)

    return errors


def validate_market_context_df(df: pd.DataFrame) -> list[str]:
    return validate_market_context_schema(df) + validate_market_context_values(df)


def load_market_context_csv(path: str | Path) -> tuple[pd.DataFrame, list[str]]:
    csv_path = Path(path)
    df = pd.read_csv(csv_path, keep_default_na=False)
    errors = validate_market_context_df(df)

    for source_column, match_column in MATCH_KEY_COLUMNS.items():
        if source_column in df.columns:
            df[match_column] = df[source_column].apply(normalize_market_context_key)

    return df, errors


def _is_empty(value: object) -> bool:
    if value is None:
        return True
    try:
        if pd.isna(value):
            return True
    except (TypeError, ValueError):
        pass
    return isinstance(value, str) and value.strip() == ""


def _is_empty_row(row: pd.Series) -> bool:
    return all(_is_empty(row.get(column)) for column in MARKET_CONTEXT_COLUMNS)


def _validate_required_match_keys(row: pd.Series, row_number: int, errors: list[str]) -> None:
    for column in ["player", "team", "league", "season"]:
        if _is_empty(row.get(column)):
            errors.append(f"Row {row_number}: {column} is required for non-empty market context rows.")


def _validate_age(value: object, row_number: int, errors: list[str]) -> None:
    if _is_empty(value):
        return
    numeric_value = _to_number(value)
    if numeric_value is None or numeric_value < 15 or numeric_value > 45:
        errors.append(f"Row {row_number}: age must be empty or a number between 15 and 45.")


def _validate_market_value(value: object, row_number: int, errors: list[str]) -> None:
    if _is_empty(value):
        return
    numeric_value = _to_number(value)
    if numeric_value is None or numeric_value <= 0:
        errors.append(f"Row {row_number}: market_value_eur must be empty or greater than 0.")


def _validate_contract_end_date(value: object, row_number: int, errors: list[str]) -> None:
    if _is_empty(value):
        return
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        parsed = pd.to_datetime(value, errors="coerce", dayfirst=True)
    if pd.isna(parsed):
        errors.append(f"Row {row_number}: contract_end_date must be empty or parseable as a date.")


def _validate_confidence(value: object, row_number: int, errors: list[str]) -> None:
    if _is_empty(value):
        return
    normalized = str(value).strip().lower()
    if normalized not in CONFIDENCE_VALUES:
        errors.append(f"Row {row_number}: confidence must be empty, low, medium or high.")


def _validate_source_for_enrichment(row: pd.Series, row_number: int, errors: list[str]) -> None:
    has_enrichment = any(
        not _is_empty(row.get(column))
        for column in ["age", "market_value_eur", "contract_end_date"]
    )
    if has_enrichment and _is_empty(row.get("source")):
        errors.append(f"Row {row_number}: source is required when enrichment values are present.")


def _to_number(value: Any) -> float | None:
    try:
        numeric_value = pd.to_numeric(value, errors="coerce")
    except (TypeError, ValueError):
        return None
    if pd.isna(numeric_value):
        return None
    return float(numeric_value)
