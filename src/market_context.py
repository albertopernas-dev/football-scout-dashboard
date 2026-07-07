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
MARKET_CONTEXT_OUTPUT_COLUMNS = {
    "age": "market_context_age",
    "market_value_eur": "market_context_market_value_eur",
    "contract_end_date": "market_context_contract_end_date",
    "source": "market_context_source",
    "source_url": "market_context_source_url",
    "confidence": "market_context_confidence",
    "notes": "market_context_notes",
}
MERGE_KEY_COLUMNS = ["player_match_key", "team_match_key", "league_match_key", "_season_match_key"]
MERGE_SOURCE_COLUMNS = ["player", "team", "league", "season"]


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

    df = prepare_players_market_context_keys(df)

    return df, errors


def prepare_players_market_context_keys(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    for source_column, match_column in MATCH_KEY_COLUMNS.items():
        if source_column in result.columns:
            result[match_column] = result[source_column].apply(normalize_market_context_key)
        else:
            result[match_column] = ""
    return result


def find_duplicate_market_context_keys(df: pd.DataFrame) -> pd.DataFrame:
    prepared = _prepare_for_market_context_merge(df)
    duplicate_mask = prepared.duplicated(MERGE_KEY_COLUMNS, keep=False)
    return prepared.loc[duplicate_mask].drop(columns=["_season_match_key"], errors="ignore").copy()


def merge_market_context(
    players_df: pd.DataFrame,
    market_context_df: pd.DataFrame,
) -> pd.DataFrame:
    players = _prepare_for_market_context_merge(players_df)
    context = _prepare_context_for_merge(market_context_df)
    duplicates = find_duplicate_market_context_keys(context)

    duplicate_keys = set()
    if not duplicates.empty:
        duplicate_key_frame = _prepare_for_market_context_merge(duplicates)
        duplicate_keys = {
            tuple(row[column] for column in MERGE_KEY_COLUMNS)
            for _, row in duplicate_key_frame.iterrows()
        }

    if context.empty:
        merged = players.copy()
        for output_column in MARKET_CONTEXT_OUTPUT_COLUMNS.values():
            merged[output_column] = pd.NA
        merged["market_context_matched"] = pd.Series([False] * len(merged), dtype=object)
        merged["market_context_duplicate_key"] = pd.Series([False] * len(merged), dtype=object)
        return _finalize_market_context_merge(merged)

    context = context.drop_duplicates(MERGE_KEY_COLUMNS, keep="first").copy()
    context["_market_context_matched"] = True
    context["_market_context_duplicate_key"] = context.apply(
        lambda row: tuple(row[column] for column in MERGE_KEY_COLUMNS) in duplicate_keys,
        axis=1,
    )

    right_columns = MERGE_KEY_COLUMNS + [
        *MARKET_CONTEXT_OUTPUT_COLUMNS.values(),
        "_market_context_matched",
        "_market_context_duplicate_key",
    ]
    merged = players.merge(
        context[right_columns],
        how="left",
        on=MERGE_KEY_COLUMNS,
        sort=False,
    )
    merged["market_context_matched"] = (
        merged["_market_context_matched"].fillna(False).astype(bool)
        .map(lambda value: bool(value))
        .astype(object)
    )
    merged["market_context_duplicate_key"] = (
        merged["_market_context_duplicate_key"].fillna(False).astype(bool)
        .map(lambda value: bool(value))
        .astype(object)
    )
    merged = merged.drop(
        columns=["_market_context_matched", "_market_context_duplicate_key"],
        errors="ignore",
    )
    return _finalize_market_context_merge(merged)


def calculate_market_context_enrichment_coverage(df: pd.DataFrame) -> dict[str, float | int]:
    row_count = int(len(df))
    if row_count == 0:
        return _market_context_zero_coverage(0)

    matched_count = _count_truthy(df, "market_context_matched")
    age_known_count = _count_non_empty(df, "market_context_age")
    market_value_known_count = _count_positive_numeric(df, "market_context_market_value_eur")
    contract_known_count = _count_parseable_dates(df, "market_context_contract_end_date")
    high_confidence_count = _count_matching_text(df, "market_context_confidence", "high")

    return {
        "row_count": row_count,
        "matched_count": matched_count,
        "matched_pct": _pct(matched_count, row_count),
        "age_known_count": age_known_count,
        "age_known_pct": _pct(age_known_count, row_count),
        "market_value_known_count": market_value_known_count,
        "market_value_known_pct": _pct(market_value_known_count, row_count),
        "contract_known_count": contract_known_count,
        "contract_known_pct": _pct(contract_known_count, row_count),
        "high_confidence_count": high_confidence_count,
        "high_confidence_pct": _pct(high_confidence_count, row_count),
    }


def summarize_market_context_diagnostics(
    players_df: pd.DataFrame,
    market_context_df: pd.DataFrame,
    validation_errors: list[str] | None = None,
    example_limit: int = 5,
) -> dict[str, object]:
    merged = merge_market_context(players_df, market_context_df)
    duplicates = find_duplicate_market_context_keys(market_context_df)
    coverage = calculate_market_context_enrichment_coverage(merged)
    matched_examples = _market_context_example_rows(
        merged[merged["market_context_matched"].fillna(False).astype(bool)],
        limit=example_limit,
    )
    unmatched_examples = _find_unmatched_market_context_rows(
        players_df,
        market_context_df,
        limit=example_limit,
    )
    return {
        "validation_errors": list(validation_errors or []),
        "coverage": coverage,
        "duplicate_count": int(len(duplicates)),
        "duplicate_rows": duplicates,
        "matched_examples": matched_examples,
        "unmatched_enrichment_examples": unmatched_examples,
        "merged": merged,
    }


def _is_empty(value: object) -> bool:
    if value is None:
        return True
    try:
        if pd.isna(value):
            return True
    except (TypeError, ValueError):
        pass
    return isinstance(value, str) and value.strip() == ""


def _prepare_for_market_context_merge(df: pd.DataFrame) -> pd.DataFrame:
    result = prepare_players_market_context_keys(df)
    if "season" in result.columns:
        result["_season_match_key"] = result["season"].apply(_normalize_season_for_match)
    else:
        result["_season_match_key"] = ""
    return result


def _prepare_context_for_merge(df: pd.DataFrame) -> pd.DataFrame:
    context = _prepare_for_market_context_merge(df)
    for source_column, output_column in MARKET_CONTEXT_OUTPUT_COLUMNS.items():
        if source_column in context.columns:
            context[output_column] = context[source_column]
        else:
            context[output_column] = pd.NA
    return context


def _finalize_market_context_merge(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=["_season_match_key"], errors="ignore")


def _normalize_season_for_match(value: object) -> str:
    if _is_empty(value):
        return ""
    try:
        numeric_value = pd.to_numeric(value, errors="coerce")
    except (TypeError, ValueError):
        numeric_value = pd.NA
    if not pd.isna(numeric_value):
        return str(int(float(numeric_value)))
    return normalize_market_context_key(value)


def _market_context_zero_coverage(row_count: int) -> dict[str, float | int]:
    return {
        "row_count": row_count,
        "matched_count": 0,
        "matched_pct": 0.0,
        "age_known_count": 0,
        "age_known_pct": 0.0,
        "market_value_known_count": 0,
        "market_value_known_pct": 0.0,
        "contract_known_count": 0,
        "contract_known_pct": 0.0,
        "high_confidence_count": 0,
        "high_confidence_pct": 0.0,
    }


def _count_truthy(df: pd.DataFrame, column: str) -> int:
    if column not in df.columns:
        return 0
    return int(df[column].fillna(False).astype(bool).sum())


def _count_non_empty(df: pd.DataFrame, column: str) -> int:
    if column not in df.columns:
        return 0
    return int(df[column].apply(lambda value: not _is_empty(value)).sum())


def _count_positive_numeric(df: pd.DataFrame, column: str) -> int:
    if column not in df.columns:
        return 0
    values = pd.to_numeric(df[column], errors="coerce")
    return int(values.gt(0).fillna(False).sum())


def _count_parseable_dates(df: pd.DataFrame, column: str) -> int:
    if column not in df.columns:
        return 0
    values = df[column]
    non_empty = values.apply(lambda value: not _is_empty(value))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        parsed = pd.to_datetime(values, errors="coerce", dayfirst=True)
    return int((non_empty & parsed.notna()).sum())


def _count_matching_text(df: pd.DataFrame, column: str, expected: str) -> int:
    if column not in df.columns:
        return 0
    values = df[column].apply(
        lambda value: "" if _is_empty(value) else str(value).strip().lower()
    )
    return int(values.eq(expected).sum())


def _pct(count: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round((count / total) * 100, 1)


def _market_context_example_rows(df: pd.DataFrame, limit: int) -> pd.DataFrame:
    columns = [
        "player",
        "team",
        "league",
        "season",
        "market_context_age",
        "market_context_market_value_eur",
        "market_context_contract_end_date",
        "market_context_confidence",
    ]
    display_columns = [column for column in columns if column in df.columns]
    return df.loc[:, display_columns].head(limit).copy()


def _find_unmatched_market_context_rows(
    players_df: pd.DataFrame,
    market_context_df: pd.DataFrame,
    limit: int,
) -> pd.DataFrame:
    players = _prepare_for_market_context_merge(players_df)
    context = _prepare_for_market_context_merge(market_context_df)
    player_keys = {
        tuple(row[column] for column in MERGE_KEY_COLUMNS)
        for _, row in players.iterrows()
    }
    unmatched_mask = context.apply(
        lambda row: tuple(row[column] for column in MERGE_KEY_COLUMNS) not in player_keys,
        axis=1,
    )
    columns = [
        "player",
        "team",
        "league",
        "season",
        "age",
        "market_value_eur",
        "contract_end_date",
        "confidence",
    ]
    display_columns = [column for column in columns if column in context.columns]
    return context.loc[unmatched_mask, display_columns].head(limit).copy()


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
