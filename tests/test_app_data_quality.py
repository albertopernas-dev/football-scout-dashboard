import pandas as pd

from app import calculate_data_quality_metrics


def test_calculate_data_quality_metrics_uses_known_flags():
    df = pd.DataFrame(
        {
            "player": ["A", "B", "C"],
            "team": ["T1", "T1", "T2"],
            "league": ["L1", "L1", "L2"],
            "position": ["Forward", "Forward", "Defender"],
            "minutes": [90, 45, 0],
            "age": [25, 21, 25],
            "age_known": [False, True, False],
            "market_value": [None, 1_000_000, None],
            "market_value_known": [False, True, False],
            "contract_end": ["", "2026-06-30", None],
        }
    )

    metrics = calculate_data_quality_metrics(df)

    assert metrics["players_count"] == 3
    assert metrics["teams_count"] == 2
    assert metrics["leagues_count"] == 2
    assert metrics["positions_count"] == 2
    assert metrics["total_minutes"] == 135
    assert metrics["age_known_count"] == 1
    assert metrics["age_known_pct"] == 33.3
    assert metrics["market_value_known_count"] == 1
    assert metrics["market_value_known_pct"] == 33.3
    assert metrics["contract_known_count"] == 1
    assert metrics["contract_known_pct"] == 33.3


def test_calculate_data_quality_metrics_falls_back_without_known_flags():
    df = pd.DataFrame(
        {
            "player": ["A", "B"],
            "team": ["T1", "T2"],
            "league": ["L1", "L1"],
            "position": ["Forward", "Midfielder"],
            "minutes": [100, None],
            "age": [22, 0],
            "market_value": [0, 2_000_000],
            "contract_end": ["unknown text", ""],
        }
    )

    metrics = calculate_data_quality_metrics(df)

    assert metrics["players_count"] == 2
    assert metrics["total_minutes"] == 100
    assert metrics["age_known_count"] == 1
    assert metrics["age_known_pct"] == 50.0
    assert metrics["market_value_known_count"] == 1
    assert metrics["market_value_known_pct"] == 50.0
    assert metrics["contract_known_count"] == 1
    assert metrics["contract_known_pct"] == 50.0


def test_calculate_data_quality_metrics_empty_dataframe_does_not_break():
    metrics = calculate_data_quality_metrics(pd.DataFrame())

    assert metrics["players_count"] == 0
    assert metrics["teams_count"] == 0
    assert metrics["leagues_count"] == 0
    assert metrics["positions_count"] == 0
    assert metrics["total_minutes"] == 0
    assert metrics["age_known_count"] == 0
    assert metrics["age_known_pct"] == 0.0
    assert metrics["market_value_known_count"] == 0
    assert metrics["market_value_known_pct"] == 0.0
    assert metrics["contract_known_count"] == 0
    assert metrics["contract_known_pct"] == 0.0
