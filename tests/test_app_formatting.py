import pandas as pd

from app import (
    apply_display_column_labels,
    dataframe_to_csv_bytes,
    format_age,
    format_boolean_columns,
    format_display_columns,
    format_euros,
    prepare_table_display,
    sort_players_for_display,
)


def test_format_age_shows_unknown_when_age_known_is_false():
    assert format_age(25, age_known=False) == "Desconocida"


def test_format_age_handles_pandas_boolean_false():
    df = pd.DataFrame({"age": [25], "age_known": pd.Series([False], dtype="boolean")})

    display = format_display_columns(df, age_columns=["age"])

    assert display.loc[0, "age"] == "Desconocida"


def test_format_age_handles_numpy_boolean_false():
    assert format_age(25, age_known=pd.Series([False]).iloc[0]) == "Desconocida"


def test_format_age_shows_integer_when_age_is_known():
    assert format_age(22, age_known=True) == "22"


def test_format_euros_shows_unknown_when_market_value_known_is_false_or_missing():
    assert format_euros(0, value_known=False) == "Desconocido"
    assert format_euros(float("nan"), value_known=True) == "Desconocido"


def test_format_euros_formats_known_value():
    assert format_euros(3_000_000, value_known=True) == "3.000.000 €"


def test_format_display_columns_uses_known_flags_without_mutating_original_values():
    df = pd.DataFrame(
        {
            "player": ["A", "B"],
            "age": [25, 22],
            "age_known": [False, True],
            "market_value": [pd.NA, 3_000_000],
            "market_value_known": [False, True],
        }
    )

    display = format_display_columns(df, currency_columns=["market_value"], age_columns=["age"])

    assert display["age"].tolist() == ["Desconocida", "22"]
    assert display["market_value"].tolist() == ["Desconocido", "3.000.000 €"]
    assert df["age"].tolist() == [25, 22]


def test_apply_display_column_labels_keeps_unmapped_columns():
    df = pd.DataFrame({"player": ["A"], "custom_metric": [1]})

    display = apply_display_column_labels(df)

    assert display.columns.tolist() == ["Jugador", "custom_metric"]


def test_format_boolean_columns_shows_yes_no_without_mutating_original():
    df = pd.DataFrame(
        {
            "is_minutes_qualified": [True, False, pd.NA],
            "is_general_ranking_comparable": [False, True, pd.NA],
        }
    )

    display = format_boolean_columns(df, ["is_minutes_qualified", "is_general_ranking_comparable"])

    assert display["is_minutes_qualified"].tolist() == ["Sí", "No", ""]
    assert display["is_general_ranking_comparable"].tolist() == ["No", "Sí", ""]
    assert df["is_minutes_qualified"].tolist() == [True, False, pd.NA]


def test_prepare_table_display_formats_and_labels_score_columns():
    df = pd.DataFrame(
        {
            "player": ["A"],
            "overall_score": [65.432],
            "sample_adjusted_overall_score": [61.234],
            "is_minutes_qualified": [True],
        }
    )

    display = prepare_table_display(
        df,
        one_decimal_columns=["overall_score", "sample_adjusted_overall_score"],
        boolean_columns=["is_minutes_qualified"],
    )

    assert display.columns.tolist() == ["Jugador", "Score bruto", "Score recomendado", "Muestra fiable"]
    assert display.loc[0, "Score bruto"] == "65.4"
    assert display.loc[0, "Score recomendado"] == "61.2"
    assert display.loc[0, "Muestra fiable"] == "Sí"


def test_sort_players_for_display_uses_internal_columns_before_visual_labels():
    df = pd.DataFrame(
        {
            "player": ["A", "B"],
            "overall_score": [90.0, 50.0],
            "sample_adjusted_overall_score": [40.0, 80.0],
        }
    )

    sorted_df = sort_players_for_display(df)
    display = prepare_table_display(sorted_df, one_decimal_columns=["sample_adjusted_overall_score"])

    assert sorted_df["player"].tolist() == ["B", "A"]
    assert display["Jugador"].tolist() == ["B", "A"]


def test_dataframe_to_csv_bytes_returns_bytes_without_index():
    df = pd.DataFrame({"Jugador": ["A"], "Score recomendado": ["71.0"]}, index=[42])

    csv_bytes = dataframe_to_csv_bytes(df)
    csv_text = csv_bytes.decode("utf-8-sig")

    assert isinstance(csv_bytes, bytes)
    assert "42" not in csv_text
    assert csv_text.splitlines()[0] == "Jugador,Score recomendado"


def test_dataframe_to_csv_bytes_preserves_visual_columns_and_can_be_read_back():
    df = pd.DataFrame(
        {
            "Jugador": ["Portero"],
            "Muestra": ["Muestra fiable"],
            "Muestra fiable": ["S\u00ed"],
        }
    )

    csv_bytes = dataframe_to_csv_bytes(df)
    restored = pd.read_csv(pd.io.common.BytesIO(csv_bytes), encoding="utf-8-sig")

    assert restored.columns.tolist() == ["Jugador", "Muestra", "Muestra fiable"]
    assert restored.loc[0, "Jugador"] == "Portero"
    assert restored.loc[0, "Muestra"] == "Muestra fiable"
    assert restored.loc[0, "Muestra fiable"] == "S\u00ed"
