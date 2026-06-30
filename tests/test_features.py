import pandas as pd

from src.features import add_per90_metrics, add_position_percentiles


def test_add_per90_metrics_uses_minutes_denominator():
    df = pd.DataFrame(
        {
            "player": ["Ana"],
            "position": ["FW"],
            "minutes": [900],
            "goals": [10],
            "assists": [5],
            "xg": [8],
            "xa": [4],
        }
    )

    result = add_per90_metrics(df)

    assert result.loc[0, "goals_per90"] == 1.0
    assert result.loc[0, "assists_per90"] == 0.5


def test_add_position_percentiles_groups_by_position():
    df = pd.DataFrame(
        {
            "player": ["A", "B", "C"],
            "position": ["FW", "FW", "MF"],
            "goals_per90": [1.0, 0.0, 5.0],
            "assists_per90": [0.2, 0.4, 0.1],
        }
    )

    result = add_position_percentiles(df, metrics=["goals_per90"])

    assert result.loc[result["player"] == "A", "goals_per90_pct"].iloc[0] > result.loc[
        result["player"] == "B", "goals_per90_pct"
    ].iloc[0]
    assert result.loc[result["player"] == "C", "goals_per90_pct"].iloc[0] == 100
