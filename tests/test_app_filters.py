import pandas as pd

from app import apply_age_filter, get_known_age_bounds, get_known_age_values


def test_get_known_age_bounds_returns_none_when_all_ages_are_unknown():
    df = pd.DataFrame({"age": [25, 25], "age_known": [False, False]})

    assert get_known_age_bounds(df) is None


def test_get_known_age_bounds_uses_only_known_ages():
    df = pd.DataFrame({"age": [25, 20, 30], "age_known": [False, True, True]})

    assert get_known_age_bounds(df) == (20, 30)


def test_get_known_age_bounds_returns_none_for_single_known_age():
    df = pd.DataFrame({"age": [25], "age_known": [True]})

    assert get_known_age_bounds(df) is None
    assert get_known_age_values(df).tolist() == [25]


def test_apply_age_filter_keeps_unknowns_when_no_age_filter_exists():
    df = pd.DataFrame({"player": ["A", "B"], "age": [25, 25], "age_known": [False, False]})

    filtered = apply_age_filter(df, None)

    assert filtered["player"].tolist() == ["A", "B"]


def test_apply_age_filter_keeps_all_rows_when_selected_range_is_none_with_mixed_knownness():
    df = pd.DataFrame(
        {
            "player": ["Unknown", "Young", "Old"],
            "age": [25, 20, 30],
            "age_known": [False, True, True],
        }
    )

    filtered = apply_age_filter(df, None)

    assert filtered["player"].tolist() == ["Unknown", "Young", "Old"]


def test_apply_age_filter_excludes_unknowns_when_age_filter_is_explicit():
    df = pd.DataFrame(
        {
            "player": ["Unknown", "Young", "Old"],
            "age": [25, 20, 30],
            "age_known": [False, True, True],
        }
    )

    filtered = apply_age_filter(df, (18, 25))

    assert filtered["player"].tolist() == ["Young"]


def test_get_known_age_bounds_falls_back_when_age_known_is_missing():
    df = pd.DataFrame({"age": [19, 31, None]})

    assert get_known_age_bounds(df) == (19, 31)
