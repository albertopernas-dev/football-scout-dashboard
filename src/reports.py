from __future__ import annotations

from datetime import date, datetime
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

METRIC_LABELS = {
    "goals_per90": "Goles/90",
    "assists_per90": "Asistencias/90",
    "xg_per90": "xG/90",
    "xa_per90": "xA/90",
    "key_passes_per90": "Pases clave/90",
    "progressive_passes_per90": "Pases progresivos/90",
    "progressive_carries_per90": "Conducciones progresivas/90",
    "duels_won_per90": "Duelos ganados/90",
    "recoveries_per90": "Recuperaciones/90",
    "interceptions_per90": "Intercepciones/90",
    "market_opportunity_score": "Market Opportunity Score",
}

STRENGTH_LABELS = {
    "attacking_impact_score": "impacto ofensivo y amenaza de finalización",
    "chance_creation_score": "generación de ocasiones",
    "ball_progression_score": "progresión de balón",
    "defensive_impact_score": "actividad defensiva",
    "dribbling_threat_score": "amenaza en conducción y regate",
}

SIMILAR_PLAYER_LABELS = {
    "player": "Jugador",
    "team": "Equipo",
    "position": "Posición",
    "league": "Liga",
    "age": "Edad",
    "similarity": "Similitud",
    "overall_score": "Overall Score",
    "market_opportunity_score": "Market Opportunity Score",
}


def _number(value: object, default: float = 0.0) -> float:
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    return default if pd.isna(numeric) else float(numeric)


def _format_value(value: object) -> str:
    if isinstance(value, Integral):
        return f"{value:,}"
    if isinstance(value, Real):
        return f"{value:.2f}"
    return escape(str(value))


def _format_market_value(value: object) -> str:
    amount = _number(value, default=0)
    if amount <= 0:
        return "Desconocido"
    return f"{int(amount):,}".replace(",", ".") + " €"


def _html_list(items: list[str]) -> str:
    return "".join(f"<li>{escape(item)}</li>" for item in items)


def _describe_player_profile(player_row: pd.Series) -> str:
    age = _number(player_row.get("age", 0), default=0)
    minutes = _number(player_row.get("minutes", 0), default=0)
    position = str(player_row.get("position", ""))
    team = str(player_row.get("team", ""))
    league = str(player_row.get("league", ""))
    season = str(player_row.get("season", ""))
    overall = _number(player_row.get("overall_score", 0), default=0)

    age_text = "Jugador sub-23" if age <= 23 and age > 0 else "Jugador"
    parts = [f"{age_text} que actúa principalmente como {position} en {team}."]
    season_text = f" en la temporada {season}" if season else ""
    league_text = f" dentro de {league}" if league else ""
    parts.append(f"Acumula {int(minutes):,} minutos{season_text}{league_text} y presenta un overall score de {overall:.1f}/100.")
    if minutes >= 1800:
        parts.append("La muestra disponible es amplia y aporta fiabilidad al análisis.")
    elif minutes < 900:
        parts.append("La muestra disponible es reducida y conviene validarla con más contexto.")
    return " ".join(parts)


def _describe_strengths(player_row: pd.Series) -> str:
    strengths = []
    for score, label in STRENGTH_LABELS.items():
        value = _number(player_row.get(score, 0), default=0)
        if value >= 70:
            strengths.append((value, label))
    if not strengths:
        return "<p>No aparece una fortaleza estadística dominante en los scores disponibles.</p>"
    selected = [label for _, label in sorted(strengths, reverse=True)[:3]]
    return f"<ul>{_html_list(selected)}</ul>"


def _describe_risks(player_row: pd.Series) -> str:
    risks = []
    if _number(player_row.get("minutes", 0), default=0) < 900:
        risks.append("muestra de minutos limitada")
    if _number(player_row.get("market_value", 0), default=0) <= 0:
        risks.append("valor de mercado desconocido")
    if pd.isna(pd.to_datetime(player_row.get("contract_end", ""), errors="coerce")):
        risks.append("situación contractual no verificada")
    if _number(player_row.get("overall_score", 0), default=0) < 50:
        risks.append("rendimiento global por debajo de perfiles comparables")
    if _number(player_row.get("market_opportunity_score", 0), default=0) < 50:
        risks.append("oportunidad de mercado limitada según el modelo actual")
    if not risks:
        return "<p>No se detectan riesgos estadísticos evidentes con la información disponible.</p>"
    return f"<ul>{_html_list(risks[:4])}</ul>"


def _describe_market_context(
    player_row: pd.Series,
    as_of_date: str | date | pd.Timestamp | None = None,
) -> str:
    score = _number(player_row.get("market_opportunity_score", 0), default=0)
    if score >= 75:
        opportunity = "El modelo señala una oportunidad fuerte de mercado."
    elif score >= 60:
        opportunity = "El modelo señala una oportunidad interesante de mercado."
    elif score >= 50:
        opportunity = "El modelo señala una oportunidad moderada de mercado."
    else:
        opportunity = "El modelo señala una oportunidad limitada de mercado."

    notes = [opportunity]
    if _number(player_row.get("market_value", 0), default=0) <= 0:
        notes.append("El valor de mercado es desconocido, por lo que el modelo no puede valorar completamente la oportunidad económica.")

    contract_end = pd.to_datetime(player_row.get("contract_end", ""), errors="coerce")
    if not pd.isna(contract_end):
        base_date = pd.Timestamp(as_of_date) if as_of_date is not None else pd.Timestamp.today().normalize()
        if contract_end <= base_date + pd.DateOffset(months=24):
            notes.append("La situación contractual puede aumentar el atractivo al finalizar dentro de los próximos 24 meses.")
    return " ".join(notes)


def _recommendation_text(player_row: pd.Series) -> str:
    overall = _number(player_row.get("overall_score", 0), default=0)
    opportunity = _number(player_row.get("market_opportunity_score", 0), default=0)
    if overall >= 70 and opportunity >= 70:
        return "Prioridad alta para seguimiento."
    if overall >= 60 and opportunity >= 60:
        return "Perfil recomendable para seguimiento."
    if overall >= 60 and opportunity < 60:
        return "Buen perfil deportivo, pero oportunidad de mercado menos clara."
    if overall < 60 and opportunity >= 70:
        return "Oportunidad de mercado interesante, pero requiere validación deportiva."
    return "Seguimiento secundario o condicionado a más información."


def render_scouting_report(
    player_row: pd.Series,
    similar_players: pd.DataFrame,
    template_path: Path = REPORT_TEMPLATE_PATH,
    as_of_date: str | date | pd.Timestamp | None = None,
) -> str:
    template = template_path.read_text(encoding="utf-8")
    metrics_rows = []
    for metric in REPORT_METRICS:
        if metric in player_row.index:
            metrics_rows.append(
                f"<tr><td>{escape(METRIC_LABELS.get(metric, metric))}</td><td>{_format_value(player_row[metric])}</td></tr>"
            )

    similar_columns = ["player", "team", "position", "league", "age", "similarity", "overall_score", "market_opportunity_score"]
    similar_rows = []
    for _, row in similar_players.iterrows():
        cells = []
        for column in similar_columns:
            if column in similar_players.columns:
                cells.append(f"<td>{_format_value(row.get(column, ''))}</td>")
        similar_rows.append("<tr>" + "".join(cells) + "</tr>")
    similar_headers = "".join(
        f"<th>{escape(SIMILAR_PLAYER_LABELS.get(column, column.replace('_', ' ').title()))}</th>"
        for column in similar_columns
        if column in similar_players.columns
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
        "{{ market_value }}": _format_market_value(player_row.get("market_value", 0)),
        "{{ contract_end }}": escape(str(player_row.get("contract_end", ""))),
        "{{ overall_score }}": _format_value(player_row.get("overall_score", 0)),
        "{{ market_opportunity_score }}": _format_value(player_row.get("market_opportunity_score", 0)),
        "{{ profile_summary }}": escape(_describe_player_profile(player_row)),
        "{{ strengths }}": _describe_strengths(player_row),
        "{{ risks }}": _describe_risks(player_row),
        "{{ market_context }}": escape(_describe_market_context(player_row, as_of_date=as_of_date)),
        "{{ recommendation }}": escape(_recommendation_text(player_row)),
        "{{ metrics_rows }}": "\n".join(metrics_rows),
        "{{ similar_headers }}": similar_headers,
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
