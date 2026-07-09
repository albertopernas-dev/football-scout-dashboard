from __future__ import annotations

from datetime import date

import pandas as pd


def find_market_opportunities(
    df: pd.DataFrame,
    positions: list[str] | tuple[str, ...] | None = None,
    max_age: int | None = None,
    min_minutes: int | None = 900,
    max_market_value: int | float | None = None,
    contract_within_months: int | None = None,
    top_n: int = 10,
    as_of_date: str | date | pd.Timestamp | None = None,
) -> pd.DataFrame:
    """Filter and rank players by market opportunity score."""
    if "market_opportunity_score" not in df.columns:
        raise ValueError("market_opportunity_score is required to find market opportunities.")

    result = df.copy()

    if positions and "position" in result.columns:
        result = result[result["position"].isin(positions)]

    ages = _effective_age(result)
    if max_age is not None and ages is not None:
        age_known = ages.notna() & ages.gt(0)
        result = result[(~age_known) | (ages <= max_age)]

    if min_minutes is not None and "minutes" in result.columns:
        minutes = pd.to_numeric(result["minutes"], errors="coerce").fillna(0)
        result = result[minutes >= min_minutes]

    values = _effective_market_value(result)
    if max_market_value is not None and values is not None:
        result = result[(values > 0) & (values <= max_market_value)]

    contract_values = _effective_contract_end(result)
    if contract_within_months is not None and contract_values is not None:
        base_date = pd.Timestamp(as_of_date) if as_of_date is not None else pd.Timestamp.today().normalize()
        max_contract_date = base_date + pd.DateOffset(months=contract_within_months)
        contract_dates = pd.to_datetime(contract_values, errors="coerce")
        result = result[contract_dates.notna() & (contract_dates <= max_contract_date)]

    return sort_opportunities(result).head(top_n).reset_index(drop=True)


def sort_opportunities(df: pd.DataFrame) -> pd.DataFrame:
    sort_column = (
        "sample_adjusted_market_opportunity_score"
        if "sample_adjusted_market_opportunity_score" in df.columns
        else "market_opportunity_score"
    )
    return df.sort_values(sort_column, ascending=False)


def _effective_age(df: pd.DataFrame) -> pd.Series | None:
    if "effective_age" in df.columns:
        return pd.to_numeric(df["effective_age"], errors="coerce")
    if "age" not in df.columns:
        return None
    ages = pd.to_numeric(df["age"], errors="coerce")
    if "age_known" in df.columns:
        age_known = df["age_known"].fillna(False).astype(bool)
    else:
        age_known = ages.notna() & ages.gt(0)
    return ages.where(age_known)


def _effective_market_value(df: pd.DataFrame) -> pd.Series | None:
    value_columns = [
        "effective_market_value_eur",
        "market_value_eur",
        "market_value",
    ]
    available_columns = [column for column in value_columns if column in df.columns]
    if not available_columns:
        return None
    values = pd.Series(pd.NA, index=df.index, dtype="Float64")
    for column in available_columns:
        candidate = pd.to_numeric(df[column], errors="coerce")
        candidate = candidate.where(candidate.gt(0))
        values = values.where(values.notna(), candidate)
    return values


def _effective_contract_end(df: pd.DataFrame) -> pd.Series | None:
    value_columns = [
        "effective_contract_end_date",
        "contract_end_date",
        "contract_end",
    ]
    available_columns = [column for column in value_columns if column in df.columns]
    if not available_columns:
        return None
    values = pd.Series(pd.NA, index=df.index, dtype=object)
    for column in available_columns:
        candidate = df[column]
        non_empty = candidate.notna() & candidate.astype(str).str.strip().ne("")
        values = values.where(values.notna(), candidate.where(non_empty))
    return values
