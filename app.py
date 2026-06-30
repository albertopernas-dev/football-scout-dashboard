from __future__ import annotations

import pandas as pd
import streamlit as st

from src.config import RADAR_METRICS, SAMPLE_DATA_PATH
from src.data_cleaning import clean_player_data
from src.features import add_per90_metrics, add_position_percentiles
from src.reports import render_scouting_report, save_scouting_report
from src.scoring import add_profile_scores
from src.similarity import find_similar_players
from src.visualizations import create_radar_chart


st.set_page_config(page_title="Football Scout Dashboard", page_icon=":soccer:", layout="wide")


@st.cache_data(show_spinner=False)
def load_default_data() -> pd.DataFrame:
    return pd.read_csv(SAMPLE_DATA_PATH)


@st.cache_data(show_spinner=False)
def prepare_data(raw: pd.DataFrame) -> pd.DataFrame:
    cleaned = clean_player_data(raw)
    featured = add_per90_metrics(cleaned)
    percentiles = add_position_percentiles(featured)
    return add_profile_scores(percentiles)


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    with st.sidebar:
        st.header("Filtros")
        leagues = st.multiselect("Liga", sorted(df["league"].unique()), default=sorted(df["league"].unique()))
        positions = st.multiselect(
            "Posicion",
            sorted(df["position"].unique()),
            default=sorted(df["position"].unique()),
        )
        teams = st.multiselect("Equipo", sorted(df["team"].unique()))
        age_range = st.slider("Rango de edad", int(df["age"].min()), int(df["age"].max()), (int(df["age"].min()), int(df["age"].max())))
        min_minutes = st.slider("Minutos minimos", 0, int(df["minutes"].max()), min(900, int(df["minutes"].max())))
        search = st.text_input("Buscar jugador")

    filtered = df[
        df["league"].isin(leagues)
        & df["position"].isin(positions)
        & df["age"].between(age_range[0], age_range[1])
        & (df["minutes"] >= min_minutes)
    ]
    if teams:
        filtered = filtered[filtered["team"].isin(teams)]
    if search:
        filtered = filtered[filtered["player"].str.contains(search, case=False, na=False)]
    return filtered


def player_table(df: pd.DataFrame) -> None:
    display_columns = [
        "player",
        "age",
        "position",
        "team",
        "league",
        "minutes",
        "market_value",
        "contract_end",
        "overall_score",
        "market_opportunity_score",
        "attacking_impact_score",
        "chance_creation_score",
        "ball_progression_score",
        "defensive_impact_score",
        "dribbling_threat_score",
        "goals_per90",
        "assists_per90",
        "xg_per90",
        "xa_per90",
    ]
    st.dataframe(
        df[[column for column in display_columns if column in df.columns]].sort_values("overall_score", ascending=False),
        width="stretch",
        hide_index=True,
    )


def comparison_view(df: pd.DataFrame) -> None:
    players = sorted(df["player"].unique())
    if len(players) < 2:
        st.info("Necesitas al menos dos jugadores para comparar.")
        return

    col_a, col_b = st.columns(2)
    player_a = col_a.selectbox("Jugador A", players, index=0)
    player_b = col_b.selectbox("Jugador B", players, index=1)

    selected_metrics = st.multiselect(
        "Metricas del radar",
        RADAR_METRICS,
        default=[metric for metric in RADAR_METRICS[:8] if metric in df.columns],
    )
    if selected_metrics:
        st.plotly_chart(create_radar_chart(df, [player_a, player_b], selected_metrics), width="stretch")

    rows = df[df["player"].isin([player_a, player_b])]
    comparison_columns = ["player", "overall_score", "market_opportunity_score"] + selected_metrics
    st.dataframe(rows[[column for column in comparison_columns if column in rows.columns]], width="stretch", hide_index=True)


def similarity_and_report_view(df: pd.DataFrame) -> None:
    st.subheader("Jugadores similares e informe")
    players = sorted(df["player"].unique())
    selected_player = st.selectbox("Jugador para scouting", players)
    top_n = st.slider("Numero de similares", 3, 10, 5)

    similar = find_similar_players(df, selected_player, top_n=top_n)
    st.dataframe(
        similar[["player", "age", "position", "team", "league", "market_value", "similarity", "overall_score", "market_opportunity_score"]],
        width="stretch",
        hide_index=True,
    )

    player_row = df[df["player"] == selected_player].iloc[0]
    html = render_scouting_report(player_row, similar)
    report_path = save_scouting_report(html, selected_player)
    st.download_button(
        "Descargar informe HTML",
        data=html,
        file_name=report_path.name,
        mime="text/html",
    )
    st.caption(f"Informe generado en: {report_path}")


def main() -> None:
    st.title("Football Scout Dashboard")

    uploaded = st.sidebar.file_uploader("Cargar CSV", type=["csv"])
    raw = pd.read_csv(uploaded) if uploaded else load_default_data()

    try:
        df = prepare_data(raw)
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    filtered = filter_data(df)
    kpi_a, kpi_b, kpi_c, kpi_d = st.columns(4)
    kpi_a.metric("Jugadores", len(filtered))
    kpi_b.metric("Equipos", filtered["team"].nunique())
    kpi_c.metric("Ligas", filtered["league"].nunique())
    kpi_d.metric("U23", int((filtered["age"] <= 23).sum()))

    tab_table, tab_compare, tab_similarity = st.tabs(["Tabla", "Comparador", "Similitud + informe"])
    with tab_table:
        player_table(filtered)
    with tab_compare:
        comparison_view(filtered)
    with tab_similarity:
        if filtered.empty:
            st.info("Ajusta los filtros para seleccionar jugadores.")
        else:
            similarity_and_report_view(filtered)


if __name__ == "__main__":
    main()
