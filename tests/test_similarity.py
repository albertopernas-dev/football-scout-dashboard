import pandas as pd

from src.similarity import features_for_position, find_similar_players


def test_find_similar_players_excludes_target_and_orders_by_similarity():
    df = pd.DataFrame(
        {
            "player": ["A", "B", "C"],
            "position": ["FW", "FW", "FW"],
            "goals_per90": [1.0, 0.9, 0.0],
            "assists_per90": [0.2, 0.25, 1.0],
            "xg_per90": [0.8, 0.75, 0.1],
        }
    )

    result = find_similar_players(df, "A", top_n=2, features=["goals_per90", "assists_per90", "xg_per90"])

    assert result.iloc[0]["player"] == "B"
    assert "similarity" in result.columns
    assert "A" not in result["player"].tolist()


def test_features_for_position_uses_role_specific_metrics():
    winger_metrics = features_for_position("LW")
    defender_metrics = features_for_position("CB")

    assert "completed_dribbles_per90" in winger_metrics
    assert "interceptions_per90" in defender_metrics
    assert winger_metrics != defender_metrics
