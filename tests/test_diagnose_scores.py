from __future__ import annotations

import pandas as pd

from scripts.diagnose_scores import (
    calculate_score_distribution,
    find_low_minutes_in_top_rankings,
    summarize_scoring_columns,
    top_rankings,
)


def test_summarize_scoring_columns_marks_missing_and_zero_only_columns():
    df = pd.DataFrame(
        {
            "goals_per90": [0.4, 0.2],
            "goals_per90_pct": [90.0, 40.0],
            "xg_per90": [0, 0],
        }
    )

    summary = summarize_scoring_columns(df, scoring_columns=["goals_per90", "xg_per90", "xa_per90"])

    assert summary["available"] == ["goals_per90", "xg_per90"]
    assert summary["missing"] == ["xa_per90"]
    assert summary["percentile_available"] == ["goals_per90_pct"]
    assert summary["zero_only"] == ["xg_per90"]


def test_calculate_score_distribution_returns_basic_percentiles():
    df = pd.DataFrame({"overall_score": [10, 20, 30, 40]})

    distribution = calculate_score_distribution(df, ["overall_score"])

    assert distribution["overall_score"]["count"] == 4
    assert distribution["overall_score"]["min"] == 10.0
    assert distribution["overall_score"]["median"] == 25.0
    assert distribution["overall_score"]["max"] == 40.0


def test_top_rankings_orders_by_score_descending():
    df = pd.DataFrame(
        {
            "player": ["A", "B", "C"],
            "overall_score": [60.0, 90.0, 70.0],
            "minutes": [900, 800, 700],
        }
    )

    result = top_rankings(df, "overall_score", n=2)

    assert result["player"].tolist() == ["B", "C"]


def test_find_low_minutes_in_top_rankings_flags_top_score_outliers():
    df = pd.DataFrame(
        {
            "player": ["Low", "Regular", "Other"],
            "overall_score": [95.0, 90.0, 10.0],
            "market_opportunity_score": [88.0, 92.0, 5.0],
            "minutes": [45, 1200, 20],
        }
    )

    result = find_low_minutes_in_top_rankings(
        df,
        score_columns=["overall_score", "market_opportunity_score"],
        top_n=2,
        minutes_threshold=300,
    )

    assert result["overall_score"]["player"].tolist() == ["Low"]
    assert result["market_opportunity_score"]["player"].tolist() == ["Low"]
