import pandas as pd

from src.reports import render_scouting_report


def test_render_scouting_report_includes_market_context():
    player = pd.Series(
        {
            "player": "Ana",
            "age": 20,
            "position": "LW",
            "team": "Madrid",
            "league": "Liga F",
            "season": "2025/26",
            "minutes": 1200,
            "market_value": 3_500_000,
            "contract_end": "2028-06-30",
            "overall_score": 81.2,
            "market_opportunity_score": 88.5,
        }
    )
    similar = pd.DataFrame(
        {
            "player": ["Bea"],
            "team": ["Barcelona"],
            "position": ["LW"],
            "similarity": [0.91],
        }
    )

    html = render_scouting_report(player, similar)

    assert "2025/26" in html
    assert "3,500,000" in html
    assert "Market Opportunity" in html
