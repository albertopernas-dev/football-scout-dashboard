import pandas as pd

from app import format_age, format_display_columns, format_euros


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
