import pandas as pd
import pytest

from src.opportunity import find_market_opportunities


def _players() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "player": ["A", "B", "C", "D"],
            "position": ["LW", "RW", "CB", "LW"],
            "age": [21, 24, 20, 22],
            "minutes": [1200, 1500, 800, 2000],
            "market_value": [3_000_000, 0, 2_000_000, 12_000_000],
            "contract_end": ["2027-06-30", "2029-06-30", "2026-12-31", "2028-06-30"],
            "market_opportunity_score": [88.0, 71.0, 90.0, 65.0],
        }
    )


def test_find_market_opportunities_sorts_by_market_opportunity_descending():
    result = find_market_opportunities(_players(), min_minutes=0)

    assert result["player"].tolist() == ["C", "A", "B", "D"]


def test_find_market_opportunities_filters_by_max_age():
    result = find_market_opportunities(_players(), max_age=21, min_minutes=0)

    assert result["player"].tolist() == ["C", "A"]


def test_find_market_opportunities_filters_by_min_minutes():
    result = find_market_opportunities(_players(), min_minutes=1000)

    assert result["player"].tolist() == ["A", "B", "D"]


def test_find_market_opportunities_filters_max_market_value_without_treating_zero_as_cheap():
    result = find_market_opportunities(_players(), min_minutes=0, max_market_value=3_500_000)

    assert result["player"].tolist() == ["C", "A"]
    assert "B" not in result["player"].tolist()


def test_find_market_opportunities_filters_contract_within_months_with_fixed_date():
    result = find_market_opportunities(
        _players(),
        min_minutes=0,
        contract_within_months=12,
        as_of_date="2026-06-30",
    )

    assert result["player"].tolist() == ["C", "A"]


def test_find_market_opportunities_requires_market_opportunity_score():
    df = _players().drop(columns=["market_opportunity_score"])

    with pytest.raises(ValueError, match="market_opportunity_score"):
        find_market_opportunities(df)
