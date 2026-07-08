import pandas as pd

from app import (
    goalkeeper_comparability_warning_message,
    market_context_status_from_metadata,
    market_context_warning_message,
    minutes_sample_warning_message,
    should_show_market_context_status,
)


def test_market_context_warning_message_returns_warning_without_market_context():
    message = market_context_warning_message({"has_market_context": False})

    assert message == (
        "Ranking basado principalmente en rendimiento deportivo. Faltan edad, valor de mercado "
        "y contrato para evaluar oportunidad real de mercado."
    )


def test_market_context_warning_message_returns_none_when_market_context_exists():
    assert market_context_warning_message({"has_market_context": True}) is None


def test_should_show_market_context_status_returns_false_without_metadata():
    assert should_show_market_context_status({"source": "sqlite", "row_count": 10}) is False


def test_market_context_status_from_metadata_returns_enabled_values():
    status = market_context_status_from_metadata(
        {
            "row_count": 10,
            "market_context_enabled": True,
            "market_context_csv_path": "data/enrichment/context.csv",
            "market_context_matched_count": 2,
            "market_context_matched_pct": 20.0,
            "market_context_age_known_pct": 10.0,
            "market_context_market_value_known_pct": 5.0,
            "market_context_contract_known_pct": 0.0,
            "market_context_validation_error_count": 0,
            "market_context_duplicate_count": 0,
        }
    )

    assert status["show"] is True
    assert status["enabled"] is True
    assert status["status"] == "Enabled"
    assert status["csv_path"] == "data/enrichment/context.csv"
    assert status["matched_count"] == 2
    assert status["row_count"] == 10
    assert status["matched_pct"] == 20.0
    assert status["age_known_pct"] == 10.0
    assert status["market_value_known_pct"] == 5.0
    assert status["contract_known_pct"] == 0.0
    assert status["warnings"] == []


def test_market_context_status_from_metadata_reports_load_error():
    status = market_context_status_from_metadata(
        {
            "market_context_enabled": False,
            "market_context_csv_path": "missing.csv",
            "market_context_load_error": "Market context CSV not found: missing.csv",
        }
    )

    assert status["show"] is True
    assert status["enabled"] is False
    assert status["status"] == "Error"
    assert status["csv_path"] == "missing.csv"
    assert status["load_error"] == "Market context CSV not found: missing.csv"
    assert status["warnings"] == ["Market context CSV could not be loaded."]


def test_market_context_status_from_metadata_warns_about_validation_errors():
    status = market_context_status_from_metadata(
        {
            "market_context_enabled": True,
            "market_context_validation_error_count": 3,
            "market_context_duplicate_count": 0,
        }
    )

    assert "Validation errors: 3" in status["warnings"]


def test_market_context_status_from_metadata_warns_about_duplicate_keys():
    status = market_context_status_from_metadata(
        {
            "market_context_enabled": True,
            "market_context_validation_error_count": 0,
            "market_context_duplicate_count": 2,
        }
    )

    assert "Duplicate keys: 2" in status["warnings"]


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
