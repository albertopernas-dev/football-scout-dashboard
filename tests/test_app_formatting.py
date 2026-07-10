import pandas as pd

from app import (
    apply_display_column_labels,
    dataframe_to_csv_bytes,
    clarify_opportunity_original_market_labels,
    format_age,
    format_boolean_columns,
    format_display_columns,
    format_euros,
    format_integer_or_blank,
    get_display_age,
    get_display_contract_end,
    get_display_market_source,
    get_display_market_value,
    opportunity_display_columns,
    prepare_table_display,
    player_table_display_columns,
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
    assert format_euros(3_000_000, value_known=True) == "3.000.000 \u20ac"


def test_format_integer_or_blank_formats_values_without_decimals():
    assert format_integer_or_blank(24.0) == "24"
    assert format_integer_or_blank(pd.NA) == ""
    assert format_integer_or_blank("bad") == ""


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
    assert display["market_value"].tolist() == ["Desconocido", "3.000.000 \u20ac"]
    assert df["age"].tolist() == [25, 22]


def test_apply_display_column_labels_keeps_unmapped_columns():
    df = pd.DataFrame(
        {
            "player": ["A"],
            "market_context_matched": [True],
            "market_context_market_value_eur": [1_500_000],
            "custom_metric": [1],
        }
    )

    display = apply_display_column_labels(df)

    assert display.columns.tolist() == [
        "Jugador",
        "Contexto mercado match",
        "Valor contexto mercado",
        "custom_metric",
    ]


def test_format_boolean_columns_shows_yes_no_without_mutating_original():
    df = pd.DataFrame(
        {
            "is_minutes_qualified": [True, False, pd.NA],
            "is_general_ranking_comparable": [False, True, pd.NA],
        }
    )

    display = format_boolean_columns(df, ["is_minutes_qualified", "is_general_ranking_comparable"])

    assert display["is_minutes_qualified"].tolist() == ["S\u00ed", "No", ""]
    assert display["is_general_ranking_comparable"].tolist() == ["No", "S\u00ed", ""]
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
    assert display.loc[0, "Muestra fiable"] == "S\u00ed"


def test_prepare_table_display_formats_market_context_columns():
    df = pd.DataFrame(
        {
            "player": ["A", "B"],
            "market_context_matched": [True, False],
            "market_context_age": [24.0, pd.NA],
            "market_context_market_value_eur": [1_500_000, pd.NA],
            "market_context_duplicate_key": [False, True],
        }
    )

    display = prepare_table_display(
        df,
        currency_columns=["market_context_market_value_eur"],
        integer_columns=["market_context_age"],
        boolean_columns=["market_context_matched", "market_context_duplicate_key"],
    )

    assert display["Contexto mercado match"].tolist() == ["S\u00ed", "No"]
    assert display["Edad contexto mercado"].tolist() == ["24", ""]
    assert display["Valor contexto mercado"].tolist() == [format_euros(1_500_000), "Desconocido"]
    assert display["Clave duplicada contexto"].tolist() == ["No", "S\u00ed"]


def test_player_table_display_columns_includes_market_context_but_not_matching_keys():
    df = pd.DataFrame(
        {
            "player": ["A"],
            "market_context_matched": [True],
            "market_context_age": [24],
            "market_context_market_value_eur": [1_500_000],
            "market_context_contract_end_date": ["2027-06-30"],
            "market_context_confidence": ["high"],
            "market_context_source": ["manual_review"],
            "market_context_duplicate_key": [False],
            "effective_age": [24],
            "effective_market_value_eur": [1_500_000],
            "effective_contract_end_date": ["2027-06-30"],
            "effective_market_context_source": ["market_context"],
            "player_match_key": ["a"],
            "team_match_key": ["team"],
            "league_match_key": ["league"],
        }
    )

    columns = player_table_display_columns(df)

    assert "market_context_matched" in columns
    assert "market_context_age" in columns
    assert "market_context_market_value_eur" in columns
    assert "market_context_contract_end_date" in columns
    assert "market_context_confidence" in columns
    assert "market_context_source" in columns
    assert "market_context_duplicate_key" in columns
    assert "effective_age" not in columns
    assert "effective_market_value_eur" not in columns
    assert "effective_contract_end_date" not in columns
    assert "effective_market_context_source" not in columns
    assert "player_match_key" not in columns
    assert "team_match_key" not in columns
    assert "league_match_key" not in columns


def test_player_table_display_columns_ignores_missing_market_context_columns():
    df = pd.DataFrame({"player": ["A"], "overall_score": [60.0]})

    columns = player_table_display_columns(df)

    assert columns == ["player", "overall_score"]


def test_opportunity_display_columns_includes_market_context_but_not_matching_keys():
    df = pd.DataFrame(
        {
            "player": ["A"],
            "sample_adjusted_market_opportunity_score": [80.0],
            "market_context_matched": [True],
            "market_context_age": [24],
            "market_context_market_value_eur": [1_500_000],
            "market_context_contract_end_date": ["2027-06-30"],
            "market_context_confidence": ["high"],
            "market_context_source": ["manual_review"],
            "market_context_duplicate_key": [False],
            "effective_age": [24],
            "effective_market_value_eur": [1_500_000],
            "effective_contract_end_date": ["2027-06-30"],
            "effective_market_context_source": ["market_context"],
            "player_match_key": ["a"],
            "team_match_key": ["team"],
            "league_match_key": ["league"],
        }
    )

    columns = opportunity_display_columns(df)

    assert "market_context_matched" in columns
    assert "market_context_age" in columns
    assert "market_context_market_value_eur" in columns
    assert "market_context_contract_end_date" in columns
    assert "market_context_confidence" in columns
    assert "market_context_source" in columns
    assert "market_context_duplicate_key" in columns
    assert "effective_age" in columns
    assert "effective_market_value_eur" in columns
    assert "effective_contract_end_date" in columns
    assert "effective_market_context_source" in columns
    assert "player_match_key" not in columns
    assert "team_match_key" not in columns
    assert "league_match_key" not in columns


def test_opportunity_display_columns_prioritizes_effective_market_fields_before_originals():
    df = pd.DataFrame(
        {
            "player": ["A"],
            "age": [25],
            "effective_age": [23],
            "position": ["Defender"],
            "team": ["Team"],
            "league": ["League"],
            "market_value": [0],
            "effective_market_value_eur": [8_000_000],
            "contract_end": [""],
            "effective_contract_end_date": ["2029-06-30"],
            "effective_market_context_source": ["market_context"],
            "market_context_confidence": ["medium"],
        }
    )

    columns = opportunity_display_columns(df)

    assert columns.index("effective_age") < columns.index("age")
    assert columns.index("effective_market_value_eur") < columns.index("market_value")
    assert columns.index("effective_contract_end_date") < columns.index("contract_end")
    assert columns.index("effective_market_context_source") < columns.index("market_context_confidence")


def test_opportunity_display_columns_ignores_missing_market_context_columns():
    df = pd.DataFrame({"player": ["A"], "market_opportunity_score": [60.0]})

    columns = opportunity_display_columns(df)

    assert columns == ["player", "market_opportunity_score"]


def test_opportunity_display_market_context_columns_are_export_ready():
    df = pd.DataFrame(
        {
            "player": ["A"],
            "market_context_matched": [True],
            "market_context_age": [24.0],
            "market_context_market_value_eur": [1_500_000],
            "market_context_duplicate_key": [False],
        }
    )
    display = prepare_table_display(
        df[opportunity_display_columns(df)],
        currency_columns=["market_context_market_value_eur"],
        integer_columns=["market_context_age"],
        boolean_columns=["market_context_matched", "market_context_duplicate_key"],
    )

    assert display["Contexto mercado match"].tolist() == ["S\u00ed"]
    assert display["Edad contexto mercado"].tolist() == ["24"]
    assert display["Valor contexto mercado"].tolist() == [format_euros(1_500_000)]
    assert display["Clave duplicada contexto"].tolist() == ["No"]


def test_opportunity_display_effective_market_context_columns_are_export_ready():
    df = pd.DataFrame(
        {
            "player": ["A"],
            "effective_age": [24.0],
            "effective_market_value_eur": [1_500_000],
            "effective_contract_end_date": ["2027-06-30"],
            "effective_market_context_source": ["market_context"],
        }
    )
    display = prepare_table_display(
        df[opportunity_display_columns(df)],
        currency_columns=["effective_market_value_eur"],
        integer_columns=["effective_age"],
    )

    assert display["Edad efectiva"].tolist() == ["24"]
    assert display["Valor efectivo"].tolist() == [format_euros(1_500_000)]
    assert display["Contrato efectivo"].tolist() == ["2027-06-30"]
    assert display["Fuente mercado efectiva"].tolist() == ["market_context"]


def test_get_display_age_prefers_effective_age():
    row = pd.Series({"age": 25, "age_known": False, "effective_age": 23})

    assert get_display_age(row) == "23"


def test_get_display_age_falls_back_to_original_age():
    row = pd.Series({"age": 22, "age_known": True})

    assert get_display_age(row) == "22"


def test_get_display_age_returns_unknown_without_effective_or_known_original():
    row = pd.Series({"age": 25, "age_known": False, "effective_age": pd.NA})

    assert get_display_age(row) == "Desconocida"


def test_get_display_market_value_prefers_effective_value():
    row = pd.Series(
        {
            "market_value": 0,
            "market_value_known": False,
            "effective_market_value_eur": 8_000_000,
        }
    )

    assert get_display_market_value(row) == "8.000.000 \u20ac"


def test_get_display_contract_end_prefers_effective_contract():
    row = pd.Series({"contract_end": "", "effective_contract_end_date": "2029-06-30"})

    assert get_display_contract_end(row) == "2029-06-30"


def test_get_display_market_source_includes_source_and_confidence():
    row = pd.Series(
        {
            "effective_market_context_source": "market_context",
            "market_context_confidence": "medium",
        }
    )

    assert get_display_market_source(row) == "market_context · medium"


def test_clarify_opportunity_original_market_labels_only_when_effective_columns_exist():
    display = pd.DataFrame(
        {
            "Edad efectiva": ["23"],
            "Edad": ["Desconocida"],
            "Valor efectivo": ["8.000.000 \u20ac"],
            "Valor de mercado": ["Desconocido"],
            "Contrato efectivo": ["2029-06-30"],
            "Fin de contrato": [""],
        }
    )

    clarified = clarify_opportunity_original_market_labels(
        display,
        [
            "effective_age",
            "age",
            "effective_market_value_eur",
            "market_value",
            "effective_contract_end_date",
            "contract_end",
        ],
    )

    assert "Edad original" in clarified.columns
    assert "Valor original mercado" in clarified.columns
    assert "Contrato original" in clarified.columns


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
