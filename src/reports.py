from __future__ import annotations

from datetime import datetime
from html import escape
from numbers import Integral, Real
from pathlib import Path

import pandas as pd

from src.config import REPORT_TEMPLATE_PATH, REPORTS_DIR


REPORT_METRICS = [
    "goals_per90",
    "assists_per90",
    "xg_per90",
    "xa_per90",
    "key_passes_per90",
    "progressive_passes_per90",
    "progressive_carries_per90",
    "duels_won_per90",
    "recoveries_per90",
    "interceptions_per90",
    "market_opportunity_score",
]


def _format_value(value: object) -> str:
    if isinstance(value, Integral):
        return f"{value:,}"
    if isinstance(value, Real):
        return f"{value:.2f}"
    return escape(str(value))


def render_scouting_report(
    player_row: pd.Series,
    similar_players: pd.DataFrame,
    template_path: Path = REPORT_TEMPLATE_PATH,
) -> str:
    template = template_path.read_text(encoding="utf-8")
    metrics_rows = []
    for metric in REPORT_METRICS:
        if metric in player_row.index:
            metrics_rows.append(
                f"<tr><td>{escape(metric.replace('_', ' ').title())}</td><td>{_format_value(player_row[metric])}</td></tr>"
            )

    similar_rows = []
    for _, row in similar_players.iterrows():
        similar_rows.append(
            "<tr>"
            f"<td>{escape(str(row.get('player', '')))}</td>"
            f"<td>{escape(str(row.get('team', '')))}</td>"
            f"<td>{escape(str(row.get('position', '')))}</td>"
            f"<td>{_format_value(row.get('similarity', 0))}</td>"
            "</tr>"
        )

    replacements = {
        "{{ generated_at }}": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "{{ player }}": escape(str(player_row.get("player", ""))),
        "{{ age }}": escape(str(player_row.get("age", ""))),
        "{{ position }}": escape(str(player_row.get("position", ""))),
        "{{ team }}": escape(str(player_row.get("team", ""))),
        "{{ league }}": escape(str(player_row.get("league", ""))),
        "{{ season }}": escape(str(player_row.get("season", ""))),
        "{{ minutes }}": escape(str(player_row.get("minutes", ""))),
        "{{ market_value }}": _format_value(player_row.get("market_value", 0)),
        "{{ contract_end }}": escape(str(player_row.get("contract_end", ""))),
        "{{ overall_score }}": _format_value(player_row.get("overall_score", 0)),
        "{{ market_opportunity_score }}": _format_value(player_row.get("market_opportunity_score", 0)),
        "{{ metrics_rows }}": "\n".join(metrics_rows),
        "{{ similar_rows }}": "\n".join(similar_rows),
    }
    html = template
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)
    return html


def save_scouting_report(html: str, player_name: str, output_dir: Path = REPORTS_DIR) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = "".join(char.lower() if char.isalnum() else "-" for char in player_name).strip("-")
    path = output_dir / f"{slug or 'player'}-scouting-report.html"
    path.write_text(html, encoding="utf-8")
    return path
