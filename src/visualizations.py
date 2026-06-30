from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


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
