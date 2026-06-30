from __future__ import annotations

import pandas as pd

from src.schema import NUMERIC_COLUMNS, STAT_COLUMNS, normalize_columns, validate_required_columns


def clean_player_data(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize, validate, type-coerce, and lightly clean player data."""
    cleaned = normalize_columns(df)
    validate_required_columns(cleaned)

    for column in STAT_COLUMNS:
        if column not in cleaned.columns:
            cleaned[column] = 0

    for column in NUMERIC_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    cleaned["age"] = cleaned["age"].fillna(0).astype(int)
    cleaned["minutes"] = cleaned["minutes"].fillna(0).clip(lower=0)
    for column in STAT_COLUMNS:
        cleaned[column] = cleaned[column].fillna(0).clip(lower=0)

    for column in ["player", "position", "team", "league"]:
        cleaned[column] = cleaned[column].fillna("Unknown").astype(str).str.strip()
    for column in ["season", "contract_end"]:
        if column not in cleaned.columns:
            cleaned[column] = ""
        cleaned[column] = cleaned[column].fillna("").astype(str).str.strip()
    if "market_value" not in cleaned.columns:
        cleaned["market_value"] = 0
    cleaned["market_value"] = cleaned["market_value"].fillna(0).clip(lower=0)

    cleaned = cleaned[cleaned["player"].ne("")]
    return cleaned.reset_index(drop=True)
