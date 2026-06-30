from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def create_radar_chart(
    df: pd.DataFrame,
    players: list[str],
    metrics: list[str],
    use_percentiles: bool = True,
) -> go.Figure:
    figure = go.Figure()
    labels = [metric.replace("_per90", "").replace("_", " ").title() for metric in metrics]
    radar_columns = [f"{metric}_pct" if use_percentiles and f"{metric}_pct" in df.columns else metric for metric in metrics]

    for player in players:
        row = df[df["player"] == player]
        if row.empty:
            continue
        values = [float(row[column].iloc[0]) if column in row.columns else 0 for column in radar_columns]
        figure.add_trace(
            go.Scatterpolar(
                r=values + values[:1],
                theta=labels + labels[:1],
                fill="toself",
                name=player,
            )
        )

    max_range = 100 if use_percentiles else None
    figure.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        polar=dict(radialaxis=dict(visible=True, range=[0, max_range] if max_range else None)),
        showlegend=True,
        template="plotly_white",
    )
    return figure


def create_opportunity_bar_chart(
    df: pd.DataFrame,
    player_col: str = "player",
    score_col: str = "market_opportunity_score",
) -> go.Figure:
    chart_data = df.copy()
    if player_col not in chart_data.columns or score_col not in chart_data.columns:
        return go.Figure()
    chart_data = chart_data.sort_values(score_col, ascending=True)
    figure = px.bar(
        chart_data,
        x=score_col,
        y=player_col,
        orientation="h",
        color=score_col,
        color_continuous_scale="Tealgrn",
        range_x=[0, 100],
        labels={
            player_col: "Player",
            score_col: "Market Opportunity Score",
        },
    )
    figure.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        template="plotly_white",
        coloraxis_showscale=False,
    )
    return figure
