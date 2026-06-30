import pandas as pd
import pytest

from src.data_cleaning import clean_player_data
from src.schema import normalize_columns, validate_required_columns


def test_normalize_columns_accepts_spanish_aliases():
    df = pd.DataFrame(
        {
            "Jugador": ["Ana"],
            "Edad": [22],
            "Posicion": ["FW"],
            "Equipo": ["Madrid"],
            "Liga": ["Liga F"],
            "Minutos": [900],
            "Goles": [10],
        }
    )

    normalized = normalize_columns(df)

    assert "player" in normalized.columns
    assert "position" in normalized.columns
    assert "minutes" in normalized.columns
    assert normalized.loc[0, "player"] == "Ana"


def test_validate_required_columns_reports_missing_fields():
    df = pd.DataFrame({"player": ["Ana"], "minutes": [900]})

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_required_columns(df)


def test_clean_player_data_coerces_numeric_and_fills_stats():
    df = pd.DataFrame(
        {
            "player": ["Ana"],
            "age": ["22"],
            "position": ["FW"],
            "team": ["Madrid"],
            "league": ["Liga F"],
            "minutes": ["900"],
            "goals": ["10"],
            "assists": [None],
            "xg": ["4.5"],
            "xa": [None],
        }
    )

    cleaned = clean_player_data(df)

    assert cleaned.loc[0, "age"] == 22
    assert cleaned.loc[0, "minutes"] == 900
    assert cleaned.loc[0, "assists"] == 0
    assert cleaned.loc[0, "xa"] == 0


def test_clean_player_data_supports_market_schema_aliases():
    df = pd.DataFrame(
        {
            "Jugador": ["Ana"],
            "Temporada": ["2025/26"],
            "Edad": [20],
            "Posicion": ["LW"],
            "Equipo": ["Madrid"],
            "Liga": ["Liga F"],
            "Minutos": [1200],
            "Valor de mercado": ["3500000"],
            "Fin contrato": ["2028-06-30"],
        }
    )

    cleaned = clean_player_data(df)

    assert cleaned.loc[0, "season"] == "2025/26"
    assert cleaned.loc[0, "market_value"] == 3500000
    assert cleaned.loc[0, "contract_end"] == "2028-06-30"
