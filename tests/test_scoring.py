import pandas as pd

from src.scoring import add_profile_scores


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
    }.issubset(result.columns)
    assert result["overall_score"].between(0, 100).all()


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

    result = add_profile_scores(df)

    prospect = result.loc[result["player"] == "Prospect", "market_opportunity_score"].iloc[0]
    star = result.loc[result["player"] == "Star", "market_opportunity_score"].iloc[0]
    assert prospect > star
