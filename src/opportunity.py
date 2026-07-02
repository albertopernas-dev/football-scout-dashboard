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

    if max_age is not None and "age" in result.columns:
        ages = pd.to_numeric(result["age"], errors="coerce")
        if "age_known" in result.columns:
            age_known = result["age_known"].fillna(False).astype(bool)
        else:
            age_known = ages.notna() & ages.gt(0)
        result = result[(~age_known) | (ages <= max_age)]

    if min_minutes is not None and "minutes" in result.columns:
        minutes = pd.to_numeric(result["minutes"], errors="coerce").fillna(0)
        result = result[minutes >= min_minutes]

    if max_market_value is not None and "market_value" in result.columns:
        values = pd.to_numeric(result["market_value"], errors="coerce").fillna(0)
        result = result[(values > 0) & (values <= max_market_value)]

    if contract_within_months is not None and "contract_end" in result.columns:
        base_date = pd.Timestamp(as_of_date) if as_of_date is not None else pd.Timestamp.today().normalize()
        max_contract_date = base_date + pd.DateOffset(months=contract_within_months)
        contract_dates = pd.to_datetime(result["contract_end"], errors="coerce")
        result = result[contract_dates.notna() & (contract_dates <= max_contract_date)]

    return result.sort_values("market_opportunity_score", ascending=False).head(top_n).reset_index(drop=True)
