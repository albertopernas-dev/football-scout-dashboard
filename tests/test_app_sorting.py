import pandas as pd

from app import sort_players_for_display


def test_sort_players_for_display_prefers_sample_adjusted_overall_score():
    df = pd.DataFrame(
        {
            "player": ["Original Leader", "Adjusted Leader"],
            "overall_score": [95.0, 80.0],
            "sample_adjusted_overall_score": [55.0, 80.0],
        }
    )

    result = sort_players_for_display(df)

    assert result["player"].tolist() == ["Adjusted Leader", "Original Leader"]


def test_sort_players_for_display_falls_back_to_overall_score():
    df = pd.DataFrame(
        {
            "player": ["A", "B"],
            "overall_score": [60.0, 90.0],
        }
    )

    result = sort_players_for_display(df)

    assert result["player"].tolist() == ["B", "A"]
