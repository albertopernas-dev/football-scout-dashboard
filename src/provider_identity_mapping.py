from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pandas as pd


PROVIDER_IDENTITY_MAPPING_COLUMNS = [
    "provider_name",
    "provider_player_id",
    "provider_team_id",
    "provider_league_id",
    "provider_season",
    "local_player",
    "local_team",
    "local_league",
    "local_season",
    "match_status",
    "confidence",
    "reviewed_by",
    "reviewed_at",
    "notes",
]

MATCH_STATUS_VALUES = {"matched", "unmatched", "ambiguous", "rejected"}
CONFIDENCE_VALUES = {"low", "medium", "high"}
PROVIDER_IDENTITY_COLUMNS = [
    "provider_name",
    "provider_player_id",
    "provider_team_id",
    "provider_league_id",
    "provider_season",
]
PROVIDER_RECORD_IDENTITY_COLUMNS = list(PROVIDER_IDENTITY_COLUMNS)
CANONICAL_IDENTITY_COLUMNS = ["player", "team", "league", "season"]
IDENTITY_MAPPING_METADATA_RENAMES = {
    "confidence": "identity_mapping_confidence",
    "reviewed_by": "identity_mapping_reviewed_by",
    "reviewed_at": "identity_mapping_reviewed_at",
    "notes": "identity_mapping_notes",
}

LOCAL_MATCH_COLUMNS = ["local_player", "local_team", "local_league", "local_season"]


def required_provider_identity_mapping_columns() -> list[str]:
    return list(PROVIDER_IDENTITY_MAPPING_COLUMNS)


def validate_provider_identity_mapping_schema(df: pd.DataFrame) -> list[str]:
    return [
        f"Missing required provider identity mapping column: {column}"
        for column in PROVIDER_IDENTITY_MAPPING_COLUMNS
        if column not in df.columns
    ]


def validate_provider_identity_mapping_values(df: pd.DataFrame) -> list[str]:
    schema_errors = validate_provider_identity_mapping_schema(df)
    if schema_errors:
        return schema_errors

    errors: list[str] = []
    for row_index, row in df.iterrows():
        row_number = int(row_index) + 2
        _validate_required_provider_fields(row, row_number, errors)
        match_status = _normalized_text(row.get("match_status"))
        confidence = _normalized_text(row.get("confidence"))

        if _is_empty(match_status):
            errors.append(f"Row {row_number}: match_status is required.")
        elif match_status not in MATCH_STATUS_VALUES:
            errors.append(
                f"Row {row_number}: match_status must be one of {', '.join(sorted(MATCH_STATUS_VALUES))}."
            )

        if _is_empty(confidence):
            errors.append(f"Row {row_number}: confidence is required.")
        elif confidence not in CONFIDENCE_VALUES:
            errors.append(
                f"Row {row_number}: confidence must be one of {', '.join(sorted(CONFIDENCE_VALUES))}."
            )

        reviewed_at = row.get("reviewed_at")
        if not _is_empty(reviewed_at) and not _is_iso_date(reviewed_at):
            errors.append(f"Row {row_number}: reviewed_at must be empty or ISO YYYY-MM-DD.")

        if match_status == "matched":
            _validate_matched_local_fields(row, row_number, errors)

        if match_status == "ambiguous" and confidence == "high":
            errors.append(f"Row {row_number}: ambiguous mappings cannot have high confidence.")

    return errors


def validate_provider_identity_mapping_df(df: pd.DataFrame) -> list[str]:
    schema_errors = validate_provider_identity_mapping_schema(df)
    if schema_errors:
        return schema_errors
    return validate_provider_identity_mapping_values(df)


def split_provider_identity_mapping_by_status(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    result: dict[str, pd.DataFrame] = {}
    if "match_status" not in df.columns:
        for status in sorted(MATCH_STATUS_VALUES):
            result[status] = df.iloc[0:0].copy().reset_index(drop=True)
        return result

    status_values = df["match_status"].apply(_normalized_text)
    for status in sorted(MATCH_STATUS_VALUES):
        result[status] = df.loc[status_values == status].copy().reset_index(drop=True)
    return result


def find_duplicate_provider_identity_mappings(df: pd.DataFrame) -> pd.DataFrame:
    required_columns = [*PROVIDER_IDENTITY_COLUMNS, "match_status"]
    if any(column not in df.columns for column in required_columns):
        return df.iloc[0:0].copy().reset_index(drop=True)

    matched = df.loc[df["match_status"].apply(_normalized_text) == "matched"].copy()
    if matched.empty:
        return df.iloc[0:0].copy().reset_index(drop=True)

    duplicate_mask = matched.duplicated(PROVIDER_IDENTITY_COLUMNS, keep=False)
    return matched.loc[duplicate_mask].copy().reset_index(drop=True)


def load_provider_identity_mapping_csv(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(Path(path), keep_default_na=False)


def apply_provider_identity_mapping_to_records(
    records_df: pd.DataFrame,
    mapping_df: pd.DataFrame,
) -> pd.DataFrame:
    mapping_errors = validate_provider_identity_mapping_df(mapping_df)
    if mapping_errors:
        formatted_errors = "\n".join(f"- {error}" for error in mapping_errors)
        raise ValueError(f"Invalid provider identity mapping:\n{formatted_errors}")

    duplicates = find_duplicate_provider_identity_mappings(mapping_df)
    if not duplicates.empty:
        raise ValueError(
            "Provider identity mapping contains duplicate matched provider identities."
        )

    missing_record_columns = [
        column
        for column in PROVIDER_RECORD_IDENTITY_COLUMNS
        if column not in records_df.columns
    ]
    if missing_record_columns:
        raise ValueError(
            "Provider records are missing required identity columns: "
            + ", ".join(missing_record_columns)
        )

    existing_canonical_columns = [
        column for column in CANONICAL_IDENTITY_COLUMNS if column in records_df.columns
    ]
    if existing_canonical_columns:
        raise ValueError(
            "Provider records already contain canonical identity columns: "
            + ", ".join(existing_canonical_columns)
        )

    matched_mapping = mapping_df.loc[
        mapping_df["match_status"].apply(_normalized_text) == "matched",
        [
            *PROVIDER_RECORD_IDENTITY_COLUMNS,
            *LOCAL_MATCH_COLUMNS,
            *IDENTITY_MAPPING_METADATA_RENAMES,
        ],
    ].copy()
    matched_mapping = matched_mapping.rename(columns=IDENTITY_MAPPING_METADATA_RENAMES)

    result = records_df.merge(
        matched_mapping,
        how="inner",
        on=PROVIDER_RECORD_IDENTITY_COLUMNS,
        sort=False,
        validate="many_to_one",
    )
    result = result.rename(columns=dict(zip(LOCAL_MATCH_COLUMNS, CANONICAL_IDENTITY_COLUMNS)))
    return result.reset_index(drop=True)


def _validate_required_provider_fields(
    row: pd.Series,
    row_number: int,
    errors: list[str],
) -> None:
    for column in PROVIDER_IDENTITY_COLUMNS:
        if _is_empty(row.get(column)):
            errors.append(f"Row {row_number}: {column} is required.")


def _validate_matched_local_fields(
    row: pd.Series,
    row_number: int,
    errors: list[str],
) -> None:
    for column in LOCAL_MATCH_COLUMNS:
        if _is_empty(row.get(column)):
            errors.append(f"Row {row_number}: {column} is required when match_status is matched.")


def _normalized_text(value: Any) -> str:
    if _is_empty(value):
        return ""
    return str(value).strip().lower()


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    try:
        if pd.isna(value):
            return True
    except (TypeError, ValueError):
        pass
    return isinstance(value, str) and value.strip() == ""


def _is_iso_date(value: Any) -> bool:
    text = str(value).strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return False
    parsed = pd.to_datetime(text, format="%Y-%m-%d", errors="coerce")
    return not pd.isna(parsed)
