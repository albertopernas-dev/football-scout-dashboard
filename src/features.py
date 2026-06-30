from __future__ import annotations

import pandas as pd

from src.schema import STAT_COLUMNS


def add_per90_metrics(df: pd.DataFrame, metrics: list[str] | tuple[str, ...] = STAT_COLUMNS) -> pd.DataFrame:
    result = df.copy()
    minutes = result["minutes"].replace(0, pd.NA)
    for metric in metrics:
        if metric in result.columns:
            result[f"{metric}_per90"] = ((result[metric] / minutes) * 90).fillna(0).round(3)
    return result


def add_position_percentiles(df: pd.DataFrame, metrics: list[str] | tuple[str, ...] | None = None) -> pd.DataFrame:
    result = df.copy()
    selected_metrics = metrics or [column for column in result.columns if column.endswith("_per90")]
    for metric in selected_metrics:
        if metric not in result.columns:
            continue
        pct_column = f"{metric}_pct"
        result[pct_column] = (
            result.groupby("position", group_keys=False)[metric]
            .rank(pct=True, method="average")
            .mul(100)
            .fillna(0)
            .round(1)
        )
    return result
