import pandas as pd
import pytest

from src.opportunity import find_market_opportunities, sort_opportunities


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


def test_find_market_opportunities_sorts_by_sample_adjusted_market_opportunity_when_available():
    df = _players()
    df["sample_adjusted_market_opportunity_score"] = [70.0, 95.0, 80.0, 65.0]

    result = find_market_opportunities(df, min_minutes=0)

    assert result["player"].tolist() == ["B", "C", "A", "D"]


def test_sort_opportunities_falls_back_to_market_opportunity_score():
    result = sort_opportunities(_players())

    assert result["player"].tolist() == ["C", "A", "B", "D"]


def test_sort_opportunities_keeps_unqualified_players():
    df = _players()
    df["sample_adjusted_market_opportunity_score"] = [70.0, 95.0, 80.0, 65.0]
    df["is_minutes_qualified"] = [True, False, True, True]

    result = sort_opportunities(df)

    assert "B" in result["player"].tolist()


def test_find_market_opportunities_filters_by_max_age():
    result = find_market_opportunities(_players(), max_age=21, min_minutes=0)

    assert result["player"].tolist() == ["C", "A"]


def test_find_market_opportunities_uses_effective_age_before_original_age():
    df = _players()
    df["age"] = [30, 30, 30, 30]
    df["effective_age"] = [20, pd.NA, 24, 25]

    result = find_market_opportunities(df, max_age=21, min_minutes=0)

    assert result["player"].tolist() == ["A", "B"]


def test_find_market_opportunities_falls_back_to_age_when_effective_age_is_missing():
    result = find_market_opportunities(_players(), max_age=21, min_minutes=0)

    assert result["player"].tolist() == ["C", "A"]


def test_find_market_opportunities_filters_by_min_minutes():
    result = find_market_opportunities(_players(), min_minutes=1000)

    assert result["player"].tolist() == ["A", "B", "D"]


def test_find_market_opportunities_filters_max_market_value_without_treating_zero_as_cheap():
    result = find_market_opportunities(_players(), min_minutes=0, max_market_value=3_500_000)

    assert result["player"].tolist() == ["C", "A"]
    assert "B" not in result["player"].tolist()


def test_find_market_opportunities_uses_effective_market_value_before_original_value():
    df = _players()
    df["market_value"] = [12_000_000, 12_000_000, 12_000_000, 12_000_000]
    df["effective_market_value_eur"] = [3_000_000, pd.NA, 2_000_000, 12_000_000]

    result = find_market_opportunities(df, min_minutes=0, max_market_value=3_500_000)

    assert result["player"].tolist() == ["C", "A"]


def test_find_market_opportunities_falls_back_to_market_value_eur_when_effective_value_is_missing():
    df = _players().drop(columns=["market_value"])
    df["market_value_eur"] = [3_000_000, 0, 2_000_000, 12_000_000]

    result = find_market_opportunities(df, min_minutes=0, max_market_value=3_500_000)

    assert result["player"].tolist() == ["C", "A"]


def test_find_market_opportunities_falls_back_when_effective_market_value_is_invalid():
    df = _players().drop(columns=["market_value"])
    df["effective_market_value_eur"] = [0, -1, "unknown", pd.NA]
    df["market_value_eur"] = [3_000_000, 1_000_000, 2_000_000, 12_000_000]

    result = find_market_opportunities(df, min_minutes=0, max_market_value=3_500_000)

    assert result["player"].tolist() == ["C", "A", "B"]


def test_find_market_opportunities_does_not_treat_missing_effective_market_value_as_cheap():
    df = _players()
    df["market_value"] = [pd.NA, pd.NA, pd.NA, pd.NA]
    df["effective_market_value_eur"] = [pd.NA, pd.NA, pd.NA, pd.NA]

    result = find_market_opportunities(df, min_minutes=0, max_market_value=3_500_000)

    assert result.empty


def test_find_market_opportunities_filters_contract_within_months_with_fixed_date():
    result = find_market_opportunities(
        _players(),
        min_minutes=0,
        contract_within_months=12,
        as_of_date="2026-06-30",
    )

    assert result["player"].tolist() == ["C", "A"]


def test_find_market_opportunities_uses_effective_contract_before_original_contract():
    df = _players()
    df["contract_end"] = ["2029-06-30", "2029-06-30", "2029-06-30", "2029-06-30"]
    df["effective_contract_end_date"] = ["2026-12-31", pd.NA, "2027-06-30", "2029-06-30"]

    result = find_market_opportunities(
        df,
        min_minutes=0,
        contract_within_months=12,
        as_of_date="2026-06-30",
    )

    assert result["player"].tolist() == ["C", "A"]


def test_find_market_opportunities_falls_back_to_contract_end_date_when_effective_contract_is_missing():
    df = _players().drop(columns=["contract_end"])
    df["contract_end_date"] = ["2027-06-30", "2029-06-30", "2026-12-31", "2028-06-30"]

    result = find_market_opportunities(
        df,
        min_minutes=0,
        contract_within_months=12,
        as_of_date="2026-06-30",
    )

    assert result["player"].tolist() == ["C", "A"]


def test_find_market_opportunities_keeps_unknown_age_when_age_filter_is_applied():
    df = pd.DataFrame(
        {
            "player": ["Unknown Age", "Old Player"],
            "position": ["LW", "LW"],
            "age": [25, 30],
            "age_known": [False, True],
            "minutes": [1200, 1200],
            "market_value": [None, None],
            "contract_end": [None, None],
            "market_opportunity_score": [80.0, 70.0],
        }
    )

    result = find_market_opportunities(df, max_age=23, min_minutes=0)

    assert result["player"].tolist() == ["Unknown Age"]


def test_find_market_opportunities_does_not_treat_unknown_contract_as_contract_upcoming():
    df = pd.DataFrame(
        {
            "player": ["Unknown Contract", "Upcoming Contract"],
            "position": ["LW", "LW"],
            "age": [22, 22],
            "minutes": [1200, 1200],
            "market_value": [1_000_000, 1_000_000],
            "contract_end": [None, "2026-12-31"],
            "market_opportunity_score": [90.0, 80.0],
        }
    )

    result = find_market_opportunities(
        df,
        min_minutes=0,
        contract_within_months=12,
        as_of_date="2026-06-30",
    )

    assert result["player"].tolist() == ["Upcoming Contract"]


def test_find_market_opportunities_requires_market_opportunity_score():
    df = _players().drop(columns=["market_opportunity_score"])

    with pytest.raises(ValueError, match="market_opportunity_score"):
        find_market_opportunities(df)


def test_find_market_opportunities_does_not_change_existing_scores_when_using_effective_context():
    df = _players()
    df["effective_age"] = [20, 24, 20, 22]
    df["effective_market_value_eur"] = [3_000_000, 1_000_000, 2_000_000, 12_000_000]
    original_scores = df["market_opportunity_score"].copy()

    result = find_market_opportunities(df, min_minutes=0, max_market_value=3_500_000)

    assert df["market_opportunity_score"].equals(original_scores)
    assert result["market_opportunity_score"].tolist() == [90.0, 88.0, 71.0]
