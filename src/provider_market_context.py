from __future__ import annotations

from typing import Any

import pandas as pd

from src.market_context import validate_market_context_df


CANONICAL_MARKET_CONTEXT_COLUMNS = [
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

OPTIONAL_PROVIDER_CONTEXT_COLUMNS = [
    "provider_player_id",
    "provider_team_id",
    "provider_name",
    "fetched_at",
    "value_date",
    "contract_option_notes",
    "license_scope",
]


def build_canonical_market_context_df(
    records: list[dict],
    include_optional_fields: bool = False,
) -> pd.DataFrame:
    columns = _output_columns(include_optional_fields)
    canonical_records = [
        canonicalize_provider_record(
            record,
            include_optional_fields=include_optional_fields,
        )
        for record in records
    ]
    return pd.DataFrame(canonical_records, columns=columns)


def canonicalize_provider_record(
    record: dict,
    include_optional_fields: bool = False,
) -> dict[str, Any]:
    return {
        column: _empty_string_if_missing(record.get(column, ""))
        for column in _output_columns(include_optional_fields)
    }


def validate_canonical_market_context_df(df: pd.DataFrame) -> list[str]:
    return validate_market_context_df(df)


def _output_columns(include_optional_fields: bool) -> list[str]:
    if include_optional_fields:
        return [*CANONICAL_MARKET_CONTEXT_COLUMNS, *OPTIONAL_PROVIDER_CONTEXT_COLUMNS]
    return list(CANONICAL_MARKET_CONTEXT_COLUMNS)


def _empty_string_if_missing(value: Any) -> Any:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return value
