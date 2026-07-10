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


def calculate_effective_market_context_coverage(df: pd.DataFrame) -> dict[str, float | int]:
    row_count = int(len(df))
    if row_count == 0:
        return _effective_market_context_zero_coverage(0)

    effective_age_known_count = _count_valid_effective_age(df)
    effective_market_value_known_count = _count_positive_numeric(df, "effective_market_value_eur")
    effective_contract_known_count = _count_non_empty(df, "effective_contract_end_date")
    effective_source_market_context_count = _count_matching_text(
        df,
        "effective_market_context_source",
        "market_context",
    )
    effective_source_original_count = _count_matching_text(
        df,
        "effective_market_context_source",
        "original",
    )
    effective_source_unknown_count = _count_matching_text(
        df,
        "effective_market_context_source",
        "unknown",
    )

    return {
        "row_count": row_count,
        "effective_age_known_count": effective_age_known_count,
        "effective_age_known_pct": _pct(effective_age_known_count, row_count),
        "effective_market_value_known_count": effective_market_value_known_count,
        "effective_market_value_known_pct": _pct(effective_market_value_known_count, row_count),
        "effective_contract_known_count": effective_contract_known_count,
        "effective_contract_known_pct": _pct(effective_contract_known_count, row_count),
        "effective_source_market_context_count": effective_source_market_context_count,
        "effective_source_market_context_pct": _pct(effective_source_market_context_count, row_count),
        "effective_source_original_count": effective_source_original_count,
        "effective_source_original_pct": _pct(effective_source_original_count, row_count),
        "effective_source_unknown_count": effective_source_unknown_count,
        "effective_source_unknown_pct": _pct(effective_source_unknown_count, row_count),
    }


def add_effective_market_context_fields(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    effective_rows = [
        _resolve_effective_market_context_row(row)
        for _, row in result.iterrows()
    ]
    effective = pd.DataFrame(
        effective_rows,
        columns=[
            "effective_age",
            "effective_market_value_eur",
            "effective_contract_end_date",
            "effective_market_context_source",
        ],
        index=result.index,
    )
    for column in effective.columns:
        result[column] = effective[column]
    return result


def summarize_market_context_diagnostics(
    players_df: pd.DataFrame,
    market_context_df: pd.DataFrame,
    validation_errors: list[str] | None = None,
    example_limit: int = 5,
) -> dict[str, object]:
    merged = merge_market_context(players_df, market_context_df)
    merged = add_effective_market_context_fields(merged)
    duplicates = find_duplicate_market_context_keys(market_context_df)
    coverage = calculate_market_context_enrichment_coverage(merged)
    effective_coverage = calculate_effective_market_context_coverage(merged)
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
        "effective_coverage": effective_coverage,
        "duplicate_count": int(len(duplicates)),
        "duplicate_rows": duplicates,
        "matched_examples": matched_examples,
        "unmatched_enrichment_examples": unmatched_examples,
        "merged": merged,
    }


def _resolve_effective_market_context_row(row: pd.Series) -> dict[str, object]:
    used_market_context = False
    used_original = False

    market_context_age = _valid_age_or_none(row.get("market_context_age"))
    if market_context_age is not None:
        effective_age = market_context_age
        used_market_context = True
    else:
        effective_age = _original_age_or_none(row)
        used_original = used_original or effective_age is not None

    market_context_value = _positive_number_or_none(row.get("market_context_market_value_eur"))
    if market_context_value is not None:
        effective_market_value = market_context_value
        used_market_context = True
    else:
        effective_market_value = _first_positive_number_or_none(
            row,
            ["market_value_eur", "market_value"],
        )
        used_original = used_original or effective_market_value is not None

    market_context_contract = _non_empty_or_none(row.get("market_context_contract_end_date"))
    if market_context_contract is not None:
        effective_contract = market_context_contract
        used_market_context = True
    else:
        effective_contract = _first_non_empty_or_none(
            row,
            ["contract_end_date", "contract_end"],
        )
        used_original = used_original or effective_contract is not None

    if used_market_context:
        source = "market_context"
    elif used_original:
        source = "original"
    else:
        source = "unknown"

    return {
        "effective_age": effective_age if effective_age is not None else pd.NA,
        "effective_market_value_eur": effective_market_value if effective_market_value is not None else pd.NA,
        "effective_contract_end_date": effective_contract if effective_contract is not None else pd.NA,
        "effective_market_context_source": source,
    }


def _valid_age_or_none(value: object) -> int | None:
    numeric_value = _to_number(value)
    if numeric_value is None or numeric_value < 15 or numeric_value > 45:
        return None
    return int(numeric_value)


def _original_age_or_none(row: pd.Series) -> int | None:
    if "age" not in row.index:
        return None
    if _is_false_flag(row.get("age_known")):
        return None
    return _valid_age_or_none(row.get("age"))


def _positive_number_or_none(value: object) -> float | None:
    numeric_value = _to_number(value)
    if numeric_value is None or numeric_value <= 0:
        return None
    return numeric_value


def _first_positive_number_or_none(row: pd.Series, columns: list[str]) -> float | None:
    for column in columns:
        if column not in row.index:
            continue
        numeric_value = _positive_number_or_none(row.get(column))
        if numeric_value is not None:
            return numeric_value
    return None


def _non_empty_or_none(value: object) -> object | None:
    if _is_empty(value):
        return None
    return value


def _first_non_empty_or_none(row: pd.Series, columns: list[str]) -> object | None:
    for column in columns:
        if column not in row.index:
            continue
        value = _non_empty_or_none(row.get(column))
        if value is not None:
            return value
    return None


def _is_false_flag(value: object) -> bool:
    if _is_empty(value):
        return False
    if isinstance(value, str):
        return value.strip().lower() == "false"
    return bool(value) is False


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


def _effective_market_context_zero_coverage(row_count: int) -> dict[str, float | int]:
    return {
        "row_count": row_count,
        "effective_age_known_count": 0,
        "effective_age_known_pct": 0.0,
        "effective_market_value_known_count": 0,
        "effective_market_value_known_pct": 0.0,
        "effective_contract_known_count": 0,
        "effective_contract_known_pct": 0.0,
        "effective_source_market_context_count": 0,
        "effective_source_market_context_pct": 0.0,
        "effective_source_original_count": 0,
        "effective_source_original_pct": 0.0,
        "effective_source_unknown_count": 0,
        "effective_source_unknown_pct": 0.0,
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


def _count_valid_effective_age(df: pd.DataFrame) -> int:
    if "effective_age" not in df.columns:
        return 0
    values = pd.to_numeric(df["effective_age"], errors="coerce")
    return int(values.between(15, 45).fillna(False).sum())


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
    if (
        numeric_value is None
        or numeric_value < 15
        or numeric_value > 45
        or not float(numeric_value).is_integer()
    ):
        errors.append(f"Row {row_number}: age must be empty or an integer between 15 and 45.")


def _validate_market_value(value: object, row_number: int, errors: list[str]) -> None:
    if _is_empty(value):
        return
    numeric_value = _to_number(value)
    if numeric_value is None or numeric_value <= 0:
        errors.append(f"Row {row_number}: market_value_eur must be empty or greater than 0.")


def _validate_contract_end_date(value: object, row_number: int, errors: list[str]) -> None:
    if _is_empty(value):
        return
    if not _is_iso_date(value):
        errors.append(f"Row {row_number}: contract_end_date must be empty or ISO YYYY-MM-DD.")


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
    if has_enrichment and _is_empty(row.get("confidence")):
        errors.append(f"Row {row_number}: confidence is required when enrichment values are present.")


def _is_iso_date(value: object) -> bool:
    text = str(value).strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return False
    parsed = pd.to_datetime(text, format="%Y-%m-%d", errors="coerce")
    return not pd.isna(parsed)


def _to_number(value: Any) -> float | None:
    try:
        numeric_value = pd.to_numeric(value, errors="coerce")
    except (TypeError, ValueError):
        return None
    if pd.isna(numeric_value):
        return None
    return float(numeric_value)
