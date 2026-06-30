from __future__ import annotations

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


def _minmax_100(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce").fillna(0)
    spread = numeric.max() - numeric.min()
    if spread == 0:
        return pd.Series(50.0, index=series.index)
    return ((numeric - numeric.min()) / spread * 100).round(1)


def add_profile_scores(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    normalized = pd.DataFrame(index=result.index)
    weighted_scores = []

    for score_name, weights in PROFILE_WEIGHTS.items():
        score = pd.Series(0.0, index=result.index)
        total_weight = 0.0
        for metric, weight in weights.items():
            if metric not in result.columns:
                continue
            if metric not in normalized:
                normalized[metric] = _minmax_100(result[metric])
            score = score + normalized[metric] * weight
            total_weight += weight
        result[score_name] = (score / total_weight).round(1) if total_weight else 0
        weighted_scores.append(score_name)

    result["overall_score"] = result[weighted_scores].mean(axis=1).round(1)
    result["market_opportunity_score"] = _market_opportunity_score(result)

    result["scoring_score"] = result["attacking_impact_score"]
    result["creation_score"] = result["chance_creation_score"]
    result["progression_score"] = result["ball_progression_score"]
    result["defensive_score"] = result["defensive_impact_score"]
    return result


def _market_opportunity_score(df: pd.DataFrame) -> pd.Series:
    performance = df["overall_score"] if "overall_score" in df.columns else pd.Series(50.0, index=df.index)
    age = df["age"] if "age" in df.columns else pd.Series(25, index=df.index)
    minutes = df["minutes"] if "minutes" in df.columns else pd.Series(900, index=df.index)
    age_score = (100 - ((pd.to_numeric(age, errors="coerce").fillna(25) - 18) / 14 * 100)).clip(0, 100)
    minutes_score = (pd.to_numeric(minutes, errors="coerce").fillna(0).clip(0, 1800) / 1800 * 100).round(1)
    if "market_value" in df.columns:
        value_score = 100 - _minmax_100(df["market_value"])
    else:
        value_score = pd.Series(50.0, index=df.index)
    return (performance * 0.25 + age_score * 0.30 + minutes_score * 0.20 + value_score * 0.25).round(1)
