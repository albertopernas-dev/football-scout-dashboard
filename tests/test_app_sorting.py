import pandas as pd

from app import (
    filter_by_ranking_scope,
    filter_by_sample_quality,
    prepare_opportunity_input,
    sort_players_for_display,
)


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


def test_filter_by_ranking_scope_all_keeps_all_rows():
    df = pd.DataFrame({"player": ["A", "B"], "is_general_ranking_comparable": [True, False]})

    result = filter_by_ranking_scope(df, "Todos")

    assert result["player"].tolist() == ["A", "B"]


def test_filter_by_ranking_scope_keeps_only_general_comparable_players():
    df = pd.DataFrame(
        {
            "player": ["Comparable", "Limited"],
            "is_general_ranking_comparable": [True, False],
        }
    )

    result = filter_by_ranking_scope(df, "Solo comparables ranking general")

    assert result["player"].tolist() == ["Comparable"]


def test_filter_by_ranking_scope_keeps_only_goalkeepers_from_flag():
    df = pd.DataFrame({"player": ["Keeper", "Forward"], "is_goalkeeper": [True, False]})

    result = filter_by_ranking_scope(df, "Solo porteros")

    assert result["player"].tolist() == ["Keeper"]


def test_filter_by_ranking_scope_goalkeeper_fallback_uses_position():
    df = pd.DataFrame(
        {
            "player": ["Keeper", "Short GK", "Letter G", "Defender"],
            "position": ["Goalkeeper", "GK", "G", "Defender"],
        }
    )

    result = filter_by_ranking_scope(df, "Solo porteros")

    assert result["player"].tolist() == ["Keeper", "Short GK", "Letter G"]


def test_filter_by_ranking_scope_missing_columns_does_not_break():
    df = pd.DataFrame({"player": ["A", "B"]})

    result = filter_by_ranking_scope(df, "Solo comparables ranking general")

    assert result["player"].tolist() == ["A", "B"]


def test_filter_by_sample_quality_all_keeps_all_rows():
    df = pd.DataFrame({"player": ["Low", "Reliable"], "minutes_sample_label": ["Muestra baja", "Muestra fiable"]})

    result = filter_by_sample_quality(df, "Todas")

    assert result["player"].tolist() == ["Low", "Reliable"]


def test_filter_by_sample_quality_medium_or_reliable_excludes_low_sample():
    df = pd.DataFrame(
        {
            "player": ["Low", "Medium", "Reliable"],
            "minutes_sample_label": ["Muestra baja", "Muestra media", "Muestra fiable"],
        }
    )

    result = filter_by_sample_quality(df, "Media o fiable")

    assert result["player"].tolist() == ["Medium", "Reliable"]


def test_filter_by_sample_quality_reliable_uses_minutes_qualified_flag():
    df = pd.DataFrame(
        {
            "player": ["Low", "Reliable"],
            "minutes_sample_label": ["Muestra fiable", "Muestra baja"],
            "is_minutes_qualified": [False, True],
        }
    )

    result = filter_by_sample_quality(df, "Solo fiable")

    assert result["player"].tolist() == ["Reliable"]


def test_filter_by_sample_quality_reliable_falls_back_to_label():
    df = pd.DataFrame(
        {
            "player": ["Low", "Reliable"],
            "minutes_sample_label": ["Muestra baja", "Muestra fiable"],
        }
    )

    result = filter_by_sample_quality(df, "Solo fiable")

    assert result["player"].tolist() == ["Reliable"]


def test_filter_by_sample_quality_missing_columns_does_not_break():
    df = pd.DataFrame({"player": ["A", "B"]})

    result = filter_by_sample_quality(df, "Solo fiable")

    assert result["player"].tolist() == ["A", "B"]


def test_prepare_opportunity_input_excludes_goalkeepers_when_general_comparable_scope_is_selected():
    df = pd.DataFrame(
        {
            "player": ["Forward", "Keeper"],
            "is_general_ranking_comparable": [True, False],
            "is_goalkeeper": [False, True],
        }
    )

    result = prepare_opportunity_input(df, "Solo comparables ranking general", "Todas")

    assert result["player"].tolist() == ["Forward"]


def test_prepare_opportunity_input_excludes_unreliable_samples_when_reliable_filter_is_selected():
    df = pd.DataFrame(
        {
            "player": ["Low", "Reliable"],
            "is_minutes_qualified": [False, True],
        }
    )

    result = prepare_opportunity_input(df, "Todos", "Solo fiable")

    assert result["player"].tolist() == ["Reliable"]


def test_prepare_opportunity_input_all_filters_keep_rows_unchanged():
    df = pd.DataFrame(
        {
            "player": ["A", "B"],
            "is_general_ranking_comparable": [True, False],
            "is_minutes_qualified": [False, True],
        }
    )

    result = prepare_opportunity_input(df, "Todos", "Todas")

    assert result["player"].tolist() == ["A", "B"]


def test_prepare_opportunity_input_missing_columns_does_not_remove_rows():
    df = pd.DataFrame({"player": ["A", "B"]})

    result = prepare_opportunity_input(df, "Solo comparables ranking general", "Solo fiable")

    assert result["player"].tolist() == ["A", "B"]
