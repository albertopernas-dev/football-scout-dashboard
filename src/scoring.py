from __future__ import annotations

from datetime import date

import pandas as pd


PROFILE_WEIGHTS = {
    "attacking_impact_score": {
        "goals_per90": 0.35,
        "xg_per90": 0.30,
        "shots_per90": 0.20,
        "completed_dribbles_per90": 0.15,
    },
    "chance_creation_score": {
        "assists_per90": 0.25,
        "xa_per90": 0.30,
        "key_passes_per90": 0.30,
        "progressive_passes_per90": 0.15,
    },
    "ball_progression_score": {
        "progressive_passes_per90": 0.35,
        "progressive_carries_per90": 0.35,
        "completed_dribbles_per90": 0.30,
    },
    "defensive_impact_score": {
        "duels_won_per90": 0.30,
        "recoveries_per90": 0.40,
        "interceptions_per90": 0.30,
    },
    "dribbling_threat_score": {
        "completed_dribbles_per90": 0.55,
        "progressive_carries_per90": 0.30,
        "xa_per90": 0.15,
    },
}

POSITION_SCORE_WEIGHTS = {
    "ST": {
        "attacking_impact_score": 0.35,
        "chance_creation_score": 0.20,
        "ball_progression_score": 0.15,
        "dribbling_threat_score": 0.20,
        "defensive_impact_score": 0.10,
    },
    "FW": {
        "attacking_impact_score": 0.35,
        "chance_creation_score": 0.20,
        "ball_progression_score": 0.15,
        "dribbling_threat_score": 0.20,
        "defensive_impact_score": 0.10,
    },
    "LW": {
        "attacking_impact_score": 0.25,
        "chance_creation_score": 0.25,
        "ball_progression_score": 0.20,
        "dribbling_threat_score": 0.25,
        "defensive_impact_score": 0.05,
    },
    "RW": {
        "attacking_impact_score": 0.25,
        "chance_creation_score": 0.25,
        "ball_progression_score": 0.20,
        "dribbling_threat_score": 0.25,
        "defensive_impact_score": 0.05,
    },
    "CM": {
        "attacking_impact_score": 0.10,
        "chance_creation_score": 0.25,
        "ball_progression_score": 0.30,
        "dribbling_threat_score": 0.10,
        "defensive_impact_score": 0.25,
    },
    "MF": {
        "attacking_impact_score": 0.10,
        "chance_creation_score": 0.25,
        "ball_progression_score": 0.30,
        "dribbling_threat_score": 0.10,
        "defensive_impact_score": 0.25,
    },
    "DM": {
        "attacking_impact_score": 0.05,
        "chance_creation_score": 0.10,
        "ball_progression_score": 0.25,
        "dribbling_threat_score": 0.10,
        "defensive_impact_score": 0.50,
    },
    "CB": {
        "attacking_impact_score": 0.05,
        "chance_creation_score": 0.05,
        "ball_progression_score": 0.15,
        "dribbling_threat_score": 0.05,
        "defensive_impact_score": 0.70,
    },
    "DF": {
        "attacking_impact_score": 0.05,
        "chance_creation_score": 0.05,
        "ball_progression_score": 0.15,
        "dribbling_threat_score": 0.05,
        "defensive_impact_score": 0.70,
    },
    "FB": {
        "attacking_impact_score": 0.10,
        "chance_creation_score": 0.20,
        "ball_progression_score": 0.30,
        "dribbling_threat_score": 0.10,
        "defensive_impact_score": 0.30,
    },
}

PROFILE_SCORE_COLUMNS = list(PROFILE_WEIGHTS)


def _minmax_100(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce").fillna(0)
    spread = numeric.max() - numeric.min()
    if spread == 0:
        return pd.Series(50.0, index=series.index)
    return ((numeric - numeric.min()) / spread * 100).round(1)


def _neutral_score(index: pd.Index) -> pd.Series:
    return pd.Series(50.0, index=index)


def _metric_score(df: pd.DataFrame, metric: str) -> pd.Series:
    percentile_column = f"{metric}_pct"
    if percentile_column in df.columns:
        return pd.to_numeric(df[percentile_column], errors="coerce").fillna(50).clip(0, 100)
    if metric in df.columns:
        return _minmax_100(df[metric]).clip(0, 100)
    return _neutral_score(df.index)


def _weights_for_position(position: object) -> dict[str, float] | None:
    key = str(position).upper().strip()
    return POSITION_SCORE_WEIGHTS.get(key)


def _weighted_overall_score(row: pd.Series) -> float:
    weights = _weights_for_position(row.get("position", ""))
    if not weights:
        return round(float(row[PROFILE_SCORE_COLUMNS].mean()), 1)
    score = 0.0
    total_weight = 0.0
    for column, weight in weights.items():
        if column in row.index:
            score += float(row[column]) * weight
            total_weight += weight
    if total_weight == 0:
        return round(float(row[PROFILE_SCORE_COLUMNS].mean()), 1)
    return round(score / total_weight, 1)


def add_profile_scores(df: pd.DataFrame, as_of_date: str | date | pd.Timestamp | None = None) -> pd.DataFrame:
    result = df.copy()
    weighted_scores = []

    for score_name, weights in PROFILE_WEIGHTS.items():
        score = pd.Series(0.0, index=result.index)
        total_weight = 0.0
        for metric, weight in weights.items():
            score = score + _metric_score(result, metric) * weight
            total_weight += weight
        result[score_name] = (score / total_weight).round(1) if total_weight else 0
        weighted_scores.append(score_name)

    result["overall_score"] = result.apply(_weighted_overall_score, axis=1)
    result["market_opportunity_score"] = _market_opportunity_score(result, as_of_date=as_of_date)

    result["scoring_score"] = result["attacking_impact_score"]
    result["creation_score"] = result["chance_creation_score"]
    result["progression_score"] = result["ball_progression_score"]
    result["defensive_score"] = result["defensive_impact_score"]
    return result


def _market_value_score(series: pd.Series, index: pd.Index) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    score = pd.Series(50.0, index=index)
    positive = values[values > 0]
    if positive.empty:
        return score
    spread = positive.max() - positive.min()
    if spread == 0:
        score.loc[positive.index] = 50.0
    else:
        score.loc[positive.index] = (100 - ((positive - positive.min()) / spread * 100)).round(1)
    return score.clip(0, 100)


def _contract_opportunity_score(
    series: pd.Series,
    as_of_date: str | date | pd.Timestamp | None = None,
) -> pd.Series:
    base_date = pd.Timestamp(as_of_date) if as_of_date is not None else pd.Timestamp.today().normalize()
    dates = pd.to_datetime(series, errors="coerce")
    score = pd.Series(50.0, index=series.index)
    known = dates.notna()
    six_months = base_date + pd.DateOffset(months=6)
    twelve_months = base_date + pd.DateOffset(months=12)
    twenty_four_months = base_date + pd.DateOffset(months=24)
    thirty_six_months = base_date + pd.DateOffset(months=36)
    score.loc[known & (dates <= six_months)] = 100
    score.loc[known & (dates > six_months) & (dates <= twelve_months)] = 90
    score.loc[known & (dates > twelve_months) & (dates <= twenty_four_months)] = 70
    score.loc[known & (dates > twenty_four_months) & (dates <= thirty_six_months)] = 50
    score.loc[known & (dates > thirty_six_months)] = 35
    return score


def _age_opportunity_score(df: pd.DataFrame, index: pd.Index) -> pd.Series:
    age = pd.to_numeric(df["age"], errors="coerce") if "age" in df.columns else pd.Series(pd.NA, index=index)
    if "age_known" in df.columns:
        known = df["age_known"].fillna(False).astype(bool) & age.gt(0)
    else:
        known = age.gt(0)

    score = pd.Series(50.0, index=index)
    if known.any():
        score.loc[known] = (100 - ((age.loc[known] - 18) / 14 * 100)).clip(0, 100)
    return score


def _market_opportunity_score(
    df: pd.DataFrame,
    as_of_date: str | date | pd.Timestamp | None = None,
) -> pd.Series:
    performance = df["overall_score"] if "overall_score" in df.columns else pd.Series(50.0, index=df.index)
    minutes = df["minutes"] if "minutes" in df.columns else pd.Series(900, index=df.index)
    age_score = _age_opportunity_score(df, df.index)
    minutes_score = (pd.to_numeric(minutes, errors="coerce").fillna(0).clip(0, 1800) / 1800 * 100).round(1)
    if "market_value" in df.columns:
        value_score = _market_value_score(df["market_value"], df.index)
    else:
        value_score = pd.Series(50.0, index=df.index)
    if "contract_end" in df.columns:
        contract_score = _contract_opportunity_score(df["contract_end"], as_of_date=as_of_date)
    else:
        contract_score = pd.Series(50.0, index=df.index)
    return (
        performance * 0.35
        + age_score * 0.20
        + minutes_score * 0.15
        + value_score * 0.20
        + contract_score * 0.10
    ).round(1)
