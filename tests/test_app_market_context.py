import pandas as pd

from app import (
    goalkeeper_comparability_warning_message,
    market_context_warning_message,
    minutes_sample_warning_message,
)


def test_market_context_warning_message_returns_warning_without_market_context():
    message = market_context_warning_message({"has_market_context": False})

    assert message == (
        "Ranking basado principalmente en rendimiento deportivo. Faltan edad, valor de mercado "
        "y contrato para evaluar oportunidad real de mercado."
    )


def test_market_context_warning_message_returns_none_when_market_context_exists():
    assert market_context_warning_message({"has_market_context": True}) is None


def test_minutes_sample_warning_message_returns_warning_with_unqualified_players():
    df = pd.DataFrame({"is_minutes_qualified": [True, False]})

    assert minutes_sample_warning_message(df) == (
        "Algunos jugadores tienen pocos minutos; interpreta su ranking como señal exploratoria."
    )


def test_minutes_sample_warning_message_returns_none_when_all_players_are_qualified():
    df = pd.DataFrame({"is_minutes_qualified": [True, True]})

    assert minutes_sample_warning_message(df) is None


def test_goalkeeper_comparability_warning_message_returns_warning_for_limited_goalkeeper():
    df = pd.DataFrame(
        {
            "position": ["Goalkeeper", "Forward"],
            "is_general_ranking_comparable": [False, True],
        }
    )

    assert goalkeeper_comparability_warning_message(df) == (
        "Los porteros no son plenamente comparables con el scoring general."
    )


def test_goalkeeper_comparability_warning_message_returns_none_without_limited_goalkeepers():
    df = pd.DataFrame(
        {
            "position": ["Forward", "Defender"],
            "is_general_ranking_comparable": [True, True],
        }
    )

    assert goalkeeper_comparability_warning_message(df) is None
