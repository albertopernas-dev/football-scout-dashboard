from app import market_context_warning_message


def test_market_context_warning_message_returns_warning_without_market_context():
    message = market_context_warning_message({"has_market_context": False})

    assert message == (
        "Ranking basado principalmente en rendimiento deportivo. Faltan edad, valor de mercado "
        "y contrato para evaluar oportunidad real de mercado."
    )


def test_market_context_warning_message_returns_none_when_market_context_exists():
    assert market_context_warning_message({"has_market_context": True}) is None
