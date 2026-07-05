import pandas as pd

from src.scoring import (
    _contract_opportunity_score,
    add_minutes_reliability,
    add_profile_scores,
    adjust_score_by_minutes_reliability,
)


def test_add_profile_scores_creates_role_scores():
    df = pd.DataFrame(
        {
            "player": ["A", "B"],
            "goals_per90": [1.0, 0.0],
            "xg_per90": [0.8, 0.1],
            "assists_per90": [0.2, 1.0],
            "xa_per90": [0.1, 0.8],
            "key_passes_per90": [1.0, 3.0],
            "progressive_passes_per90": [1.0, 5.0],
            "progressive_carries_per90": [3.0, 1.0],
            "completed_dribbles_per90": [2.0, 0.5],
            "duels_won_per90": [1.0, 4.0],
            "recoveries_per90": [2.0, 7.0],
            "interceptions_per90": [0.5, 3.0],
        }
    )

    result = add_profile_scores(df)

    assert {
        "attacking_impact_score",
        "chance_creation_score",
        "ball_progression_score",
        "defensive_impact_score",
        "dribbling_threat_score",
        "overall_score",
        "market_opportunity_score",
        "scoring_score",
        "creation_score",
        "progression_score",
        "defensive_score",
    }.issubset(result.columns)
    assert result["overall_score"].between(0, 100).all()


def test_add_profile_scores_prefers_position_percentiles_when_available():
    df = pd.DataFrame(
        {
            "player": ["A", "B"],
            "position": ["FW", "FW"],
            "goals_per90": [99.0, 1.0],
            "goals_per90_pct": [10.0, 90.0],
            "xg_per90_pct": [10.0, 90.0],
            "shots_per90_pct": [10.0, 90.0],
            "completed_dribbles_per90_pct": [10.0, 90.0],
        }
    )

    result = add_profile_scores(df)

    score_a = result.loc[result["player"] == "A", "attacking_impact_score"].iloc[0]
    score_b = result.loc[result["player"] == "B", "attacking_impact_score"].iloc[0]
    assert score_b > score_a


def test_overall_score_uses_position_specific_weights():
    df = pd.DataFrame(
        {
            "player": ["Striker", "Center Back"],
            "position": ["ST", "CB"],
            "goals_per90_pct": [100, 100],
            "xg_per90_pct": [100, 100],
            "shots_per90_pct": [100, 100],
            "completed_dribbles_per90_pct": [0, 0],
            "assists_per90_pct": [0, 0],
            "xa_per90_pct": [0, 0],
            "key_passes_per90_pct": [0, 0],
            "progressive_passes_per90_pct": [0, 0],
            "progressive_carries_per90_pct": [0, 0],
            "duels_won_per90_pct": [0, 0],
            "recoveries_per90_pct": [0, 0],
            "interceptions_per90_pct": [0, 0],
        }
    )

    result = add_profile_scores(df)

    striker = result.loc[result["player"] == "Striker", "overall_score"].iloc[0]
    center_back = result.loc[result["player"] == "Center Back", "overall_score"].iloc[0]
    assert striker > center_back


def test_market_opportunity_rewards_young_cheap_high_performers():
    df = pd.DataFrame(
        {
            "player": ["Prospect", "Star"],
            "age": [20, 29],
            "minutes": [1600, 2400],
            "market_value": [2_000_000, 80_000_000],
            "goals_per90": [0.5, 0.6],
            "xg_per90": [0.45, 0.55],
            "assists_per90": [0.3, 0.4],
            "xa_per90": [0.25, 0.35],
            "key_passes_per90": [2.0, 2.2],
            "progressive_passes_per90": [4.0, 4.5],
            "progressive_carries_per90": [5.5, 5.7],
            "completed_dribbles_per90": [3.0, 3.1],
            "duels_won_per90": [4.0, 4.0],
            "recoveries_per90": [6.0, 6.0],
            "interceptions_per90": [1.0, 1.0],
        }
    )

    df["contract_end"] = ["2027-05-30", "2030-06-30"]

    result = add_profile_scores(df, as_of_date="2026-06-30")

    prospect = result.loc[result["player"] == "Prospect", "market_opportunity_score"].iloc[0]
    star = result.loc[result["player"] == "Star", "market_opportunity_score"].iloc[0]
    assert prospect > star


def test_missing_or_zero_market_value_is_neutral_not_best_score():
    df = pd.DataFrame(
        {
            "player": ["Unknown Value", "Cheap Player", "Expensive Player"],
            "position": ["FW", "FW", "FW"],
            "age": [22, 22, 22],
            "minutes": [1800, 1800, 1800],
            "market_value": [0, 1_000_000, 10_000_000],
            "contract_end": ["2027-06-30", "2027-06-30", "2027-06-30"],
            "goals_per90_pct": [80, 80, 80],
            "xg_per90_pct": [80, 80, 80],
            "shots_per90_pct": [80, 80, 80],
            "completed_dribbles_per90_pct": [80, 80, 80],
        }
    )

    result = add_profile_scores(df, as_of_date="2026-06-30")

    unknown = result.loc[result["player"] == "Unknown Value", "market_opportunity_score"].iloc[0]
    cheap = result.loc[result["player"] == "Cheap Player", "market_opportunity_score"].iloc[0]
    expensive = result.loc[result["player"] == "Expensive Player", "market_opportunity_score"].iloc[0]
    assert cheap > unknown > expensive


def test_equal_positive_market_values_are_neutral_not_boosted():
    df = pd.DataFrame(
        {
            "player": ["A", "B", "Unknown Value"],
            "position": ["FW", "FW", "FW"],
            "age": [22, 22, 22],
            "minutes": [1800, 1800, 1800],
            "market_value": [5_000_000, 5_000_000, 0],
            "contract_end": ["2027-06-30", "2027-06-30", "2027-06-30"],
            "goals_per90_pct": [80, 80, 80],
            "xg_per90_pct": [80, 80, 80],
            "shots_per90_pct": [80, 80, 80],
            "completed_dribbles_per90_pct": [80, 80, 80],
        }
    )

    result = add_profile_scores(df, as_of_date="2026-06-30")

    scores = result.set_index("player")["market_opportunity_score"]
    assert scores["A"] == scores["B"] == scores["Unknown Value"]


def test_single_positive_market_value_is_neutral_not_extreme_boost():
    df = pd.DataFrame(
        {
            "player": ["Known Value", "Unknown Value"],
            "position": ["FW", "FW"],
            "age": [22, 22],
            "minutes": [1800, 1800],
            "market_value": [5_000_000, 0],
            "contract_end": ["2027-06-30", "2027-06-30"],
            "goals_per90_pct": [80, 80],
            "xg_per90_pct": [80, 80],
            "shots_per90_pct": [80, 80],
            "completed_dribbles_per90_pct": [80, 80],
        }
    )

    result = add_profile_scores(df, as_of_date="2026-06-30")

    scores = result.set_index("player")["market_opportunity_score"]
    assert scores["Known Value"] == scores["Unknown Value"]


def test_unknown_or_zero_age_is_neutral_not_extreme_young_bonus():
    df = pd.DataFrame(
        {
            "player": ["Unknown Age", "Zero Age", "Neutral Age", "Young Player"],
            "position": ["FW", "FW", "FW", "FW"],
            "age": [None, 0, 25, 20],
            "age_known": [False, False, True, True],
            "minutes": [1800, 1800, 1800, 1800],
            "market_value": [0, 0, 0, 0],
            "contract_end": [None, None, None, None],
            "goals_per90_pct": [80, 80, 80, 80],
            "xg_per90_pct": [80, 80, 80, 80],
            "shots_per90_pct": [80, 80, 80, 80],
            "completed_dribbles_per90_pct": [80, 80, 80, 80],
        }
    )

    result = add_profile_scores(df, as_of_date="2026-06-30")

    scores = result.set_index("player")["market_opportunity_score"]
    assert scores["Unknown Age"] == scores["Zero Age"] == scores["Neutral Age"]
    assert scores["Young Player"] > scores["Neutral Age"]


def test_missing_contract_end_is_neutral_not_contract_bonus():
    contract_dates = pd.Series([None, "", "not-a-date"])

    scores = _contract_opportunity_score(contract_dates, as_of_date="2026-06-30")

    assert scores.tolist() == [50, 50, 50]


def test_contract_opportunity_score_uses_fixed_as_of_date():
    contract_dates = pd.Series(
        [
            "2026-06-30",
            "2026-12-30",
            "2027-06-30",
            "2028-06-30",
            "2029-06-30",
            "2030-07-01",
            "",
            "not-a-date",
        ]
    )

    scores = _contract_opportunity_score(contract_dates, as_of_date="2026-06-30")

    assert scores.tolist() == [100, 100, 90, 70, 50, 35, 50, 50]


def test_add_minutes_reliability_scores_boundary_values():
    df = pd.DataFrame(
        {
            "player": ["Zero", "Low", "Medium Start", "Medium End", "Qualified", "Over"],
            "minutes": [0, 299, 300, 899, 900, 1200],
        }
    )

    result = add_minutes_reliability(df)

    assert result["minutes_reliability_score"].tolist() == [0.0, 33.2, 33.3, 99.9, 100.0, 100.0]
    assert result["minutes_sample_label"].tolist() == [
        "Muestra baja",
        "Muestra baja",
        "Muestra media",
        "Muestra media",
        "Muestra fiable",
        "Muestra fiable",
    ]
    assert result["is_minutes_qualified"].tolist() == [False, False, False, False, True, True]


def test_add_profile_scores_includes_minutes_reliability_columns():
    df = pd.DataFrame(
        {
            "player": ["A"],
            "position": ["FW"],
            "minutes": [450],
            "goals_per90_pct": [80],
            "xg_per90_pct": [80],
            "shots_per90_pct": [80],
            "completed_dribbles_per90_pct": [80],
        }
    )

    result = add_profile_scores(df)

    assert result.loc[0, "minutes_reliability_score"] == 50.0
    assert result.loc[0, "minutes_sample_label"] == "Muestra media"
    assert not bool(result.loc[0, "is_minutes_qualified"])


def test_adjust_score_by_minutes_reliability_keeps_score_at_full_reliability():
    assert adjust_score_by_minutes_reliability(82, 100) == 82.0


def test_adjust_score_by_minutes_reliability_returns_baseline_at_zero_reliability():
    assert adjust_score_by_minutes_reliability(82, 0) == 50.0


def test_adjust_score_by_minutes_reliability_moves_score_halfway_to_baseline():
    assert adjust_score_by_minutes_reliability(80, 50) == 65.0


def test_adjust_score_by_minutes_reliability_uses_baseline_for_invalid_score():
    assert adjust_score_by_minutes_reliability(pd.NA, 100) == 50.0


def test_adjust_score_by_minutes_reliability_uses_zero_reliability_for_invalid_reliability():
    assert adjust_score_by_minutes_reliability(80, pd.NA) == 50.0


def test_adjust_score_by_minutes_reliability_clips_reliability_above_100():
    assert adjust_score_by_minutes_reliability(80, 150) == 80.0


def test_adjust_score_by_minutes_reliability_clips_reliability_below_0():
    assert adjust_score_by_minutes_reliability(80, -10) == 50.0


def test_add_profile_scores_includes_sample_adjusted_scores_without_changing_original_scores():
    df = pd.DataFrame(
        {
            "player": ["A"],
            "position": ["FW"],
            "minutes": [450],
            "goals_per90_pct": [95],
            "xg_per90_pct": [95],
            "shots_per90_pct": [95],
            "completed_dribbles_per90_pct": [95],
        }
    )

    result = add_profile_scores(df)

    assert "sample_adjusted_overall_score" in result.columns
    assert "sample_adjusted_market_opportunity_score" in result.columns
    assert result.loc[0, "overall_score"] > 50.0
    assert 50.0 < result.loc[0, "sample_adjusted_overall_score"] < result.loc[0, "overall_score"]
