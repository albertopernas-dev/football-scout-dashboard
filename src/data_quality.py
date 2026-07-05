from __future__ import annotations

import pandas as pd


def calculate_data_quality_metrics(df: pd.DataFrame) -> dict[str, object]:
    players_count = len(df)

    age_known = _known_flag_or_numeric_positive(df, flag_column="age_known", value_column="age")
    market_value_known = _known_flag_or_numeric_positive(
        df,
        flag_column="market_value_known",
        value_column="market_value",
    )
    contract_known = _contract_known_mask(df)
    minutes = pd.to_numeric(df.get("minutes", pd.Series(dtype="float64")), errors="coerce").fillna(0)

    return {
        "players_count": players_count,
        "teams_count": _nunique_if_exists(df, "team"),
        "leagues_count": _nunique_if_exists(df, "league"),
        "total_minutes": int(minutes.sum()) if not minutes.empty else 0,
        "age_known_count": int(age_known.sum()),
        "age_known_pct": _pct(age_known.sum(), players_count),
        "market_value_known_count": int(market_value_known.sum()),
        "market_value_known_pct": _pct(market_value_known.sum(), players_count),
        "contract_known_count": int(contract_known.sum()),
        "contract_known_pct": _pct(contract_known.sum(), players_count),
        "positions_count": _nunique_if_exists(df, "position"),
    }


def calculate_market_context_availability(df: pd.DataFrame) -> dict[str, object]:
    metrics = calculate_data_quality_metrics(df)
    age_known_pct = float(metrics["age_known_pct"])
    market_value_known_pct = float(metrics["market_value_known_pct"])
    contract_known_pct = float(metrics["contract_known_pct"])
    return {
        "age_known_pct": age_known_pct,
        "market_value_known_pct": market_value_known_pct,
        "contract_known_pct": contract_known_pct,
        "has_market_context": any(
            pct > 0 for pct in [age_known_pct, market_value_known_pct, contract_known_pct]
        ),
    }


def _known_flag_or_numeric_positive(df: pd.DataFrame, flag_column: str, value_column: str) -> pd.Series:
    if df.empty:
        return pd.Series(dtype=bool)
    if flag_column in df.columns:
        return df[flag_column].apply(_is_true_flag)
    if value_column not in df.columns:
        return pd.Series([False] * len(df), index=df.index)
    values = pd.to_numeric(df[value_column], errors="coerce")
    return values.notna() & (values > 0)


def _contract_known_mask(df: pd.DataFrame) -> pd.Series:
    if df.empty:
        return pd.Series(dtype=bool)
    if "contract_end" not in df.columns:
        return pd.Series([False] * len(df), index=df.index)
    return df["contract_end"].apply(lambda value: value is not None and not pd.isna(value) and str(value).strip() != "")


def _nunique_if_exists(df: pd.DataFrame, column: str) -> int:
    if column not in df.columns:
        return 0
    return int(df[column].dropna().nunique())


def _pct(count: int | float, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((float(count) / total) * 100, 1)


def _is_true_flag(value: object) -> bool:
    if value is None:
        return False
    try:
        if pd.isna(value):
            return False
    except (TypeError, ValueError):
        pass
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value) is True
