import pandas as pd

from src.similarity import _resolve_similarity_features, features_for_position, find_similar_players


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


def test_resolve_similarity_features_prefers_percentiles_when_available():
    df = pd.DataFrame(
        {
            "goals_per90": [0.1, 0.2],
            "goals_per90_pct": [10, 90],
            "xg_per90": [0.2, 0.3],
        }
    )

    resolved = _resolve_similarity_features(df, ["goals_per90", "xg_per90", "missing_per90"])

    assert resolved == ["goals_per90_pct", "xg_per90"]


def test_find_similar_players_uses_percentiles_for_similarity_when_available():
    df = pd.DataFrame(
        {
            "player": ["A", "B", "C"],
            "position": ["LW", "LW", "LW"],
            "completed_dribbles_per90": [1000, 0, 990],
            "completed_dribbles_per90_pct": [50, 49, 5],
            "progressive_carries_per90": [1, 1, 1000],
            "progressive_carries_per90_pct": [50, 51, 5],
        }
    )

    result = find_similar_players(
        df,
        "A",
        top_n=2,
        features=["completed_dribbles_per90", "progressive_carries_per90"],
    )

    assert result.iloc[0]["player"] == "B"


def test_similarity_normalization_prevents_large_scale_metric_from_dominating():
    df = pd.DataFrame(
        {
            "player": ["A", "B", "C"],
            "position": ["FW", "FW", "FW"],
            "goals_per90_pct": [50, 51, 99],
            "xg_per90_pct": [50, 51, 0],
            "market_value": [1_000_000, 1_000_100, 50_000_000],
        }
    )

    result = find_similar_players(df, "A", top_n=2, features=["goals_per90", "xg_per90", "market_value"])

    assert result.iloc[0]["player"] == "B"
