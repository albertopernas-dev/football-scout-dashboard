import pandas as pd

from src.reports import render_scouting_report


def _player(**overrides):
    base = {
        "player": "Ana",
        "age": 20,
        "position": "LW",
        "team": "Madrid",
        "league": "Liga F",
        "season": "2025/26",
        "minutes": 1850,
        "market_value": 3_500_000,
        "contract_end": "2028-06-30",
        "overall_score": 81.2,
        "market_opportunity_score": 88.5,
        "attacking_impact_score": 76,
        "chance_creation_score": 82,
        "ball_progression_score": 71,
        "defensive_impact_score": 44,
        "dribbling_threat_score": 86,
        "goals_per90": 0.42,
        "assists_per90": 0.31,
        "xg_per90": 0.39,
        "xa_per90": 0.28,
    }
    base.update(overrides)
    return pd.Series(base)


def _similar():
    return pd.DataFrame(
        {
            "player": ["Bea"],
            "team": ["Barcelona"],
            "position": ["LW"],
            "league": ["Liga F"],
            "age": [22],
            "similarity": [0.9123],
            "overall_score": [74.4],
            "market_opportunity_score": [69.2],
        }
    )


def test_render_scouting_report_includes_profile_summary():
    html = render_scouting_report(_player(), _similar(), as_of_date="2026-06-30")

    assert "Resumen del perfil" in html
    assert "sub-23" in html
    assert "La muestra disponible es amplia y aporta fiabilidad al análisis." in html
    assert "2025/26" in html
    assert "Liga F" in html


def test_render_scouting_report_includes_strengths_from_high_scores():
    html = render_scouting_report(_player(), _similar(), as_of_date="2026-06-30")

    assert "Fortalezas principales" in html
    assert "generación de ocasiones" in html
    assert "amenaza en conducción y regate" in html
    assert "No aparece una fortaleza estadística dominante" not in html


def test_render_scouting_report_includes_risks_for_limited_or_unknown_context():
    player = _player(minutes=500, market_value=0, contract_end="not-a-date", overall_score=45, market_opportunity_score=42)

    html = render_scouting_report(player, _similar(), as_of_date="2026-06-30")

    assert "Riesgos o señales a revisar" in html
    assert "muestra de minutos limitada" in html
    assert "valor de mercado desconocido" in html
    assert "situación contractual no verificada" in html
    assert "rendimiento global por debajo" in html


def test_render_scouting_report_recommendation_changes_by_scores():
    high = render_scouting_report(_player(overall_score=75, market_opportunity_score=76), _similar(), as_of_date="2026-06-30")
    sport_only = render_scouting_report(_player(overall_score=65, market_opportunity_score=52), _similar(), as_of_date="2026-06-30")
    market_only = render_scouting_report(_player(overall_score=55, market_opportunity_score=75), _similar(), as_of_date="2026-06-30")

    assert "Prioridad alta para seguimiento" in high
    assert "Buen perfil deportivo, pero oportunidad de mercado menos clara" in sport_only
    assert "Oportunidad de mercado interesante, pero requiere validación deportiva" in market_only


def test_render_scouting_report_similar_table_includes_additional_fields():
    html = render_scouting_report(_player(), _similar(), as_of_date="2026-06-30")

    assert "Barcelona" in html
    assert "22" in html
    assert "74.40" in html
    assert "69.20" in html


def test_render_scouting_report_includes_market_context():
    html = render_scouting_report(_player(), _similar(), as_of_date="2026-06-30")

    assert "Contexto de mercado" in html
    assert "3.500.000 €" in html
    assert "oportunidad fuerte" in html
    assert "Market Opportunity Score" in html


def test_render_scouting_report_similar_table_uses_spanish_headers():
    html = render_scouting_report(_player(), _similar(), as_of_date="2026-06-30")

    assert "<th>Jugador</th>" in html
    assert "<th>Equipo</th>" in html
    assert "<th>Posición</th>" in html
    assert "<th>Similitud</th>" in html
