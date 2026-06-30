from __future__ import annotations

import pandas as pd
import streamlit as st

from src.config import RADAR_METRICS, SAMPLE_DATA_PATH
from src.data_cleaning import clean_player_data
from src.features import add_per90_metrics, add_position_percentiles
from src.opportunity import find_market_opportunities
from src.reports import render_scouting_report, save_scouting_report
from src.scoring import add_profile_scores
from src.similarity import find_similar_players
from src.visualizations import create_opportunity_bar_chart, create_radar_chart


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


def format_euros(value: object) -> str:
    amount = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(amount) or amount <= 0:
        return "Desconocido"
    return f"{int(amount):,}".replace(",", ".") + " €"


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    with st.sidebar:
        st.header("Filtros")
        leagues = st.multiselect("Liga", sorted(df["league"].unique()), default=sorted(df["league"].unique()))
        positions = st.multiselect(
            "Posición",
            sorted(df["position"].unique()),
            default=sorted(df["position"].unique()),
        )
        teams = st.multiselect("Equipo", sorted(df["team"].unique()))
        age_range = st.slider("Rango de edad", int(df["age"].min()), int(df["age"].max()), (int(df["age"].min()), int(df["age"].max())))
        min_minutes = st.slider("Minutos mínimos", 0, int(df["minutes"].max()), min(900, int(df["minutes"].max())))
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
        "Métricas del radar",
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
    top_n = st.slider("Número de similares", 3, 10, 5)

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


def opportunity_finder_view(df: pd.DataFrame) -> None:
    st.subheader("Opportunity Finder")
    if df.empty:
        st.info("Ajusta los filtros para seleccionar jugadores.")
        return

    available_positions = sorted(df["position"].dropna().unique()) if "position" in df.columns else []
    controls_a, controls_b, controls_c = st.columns(3)
    positions = controls_a.multiselect("Posiciones", available_positions, default=available_positions)
    max_age = controls_b.number_input("Edad máxima", min_value=15, max_value=45, value=23, step=1)
    min_minutes = controls_c.number_input("Minutos mínimos", min_value=0, value=900, step=100)

    controls_d, controls_e, controls_f = st.columns(3)
    max_market_value = controls_d.number_input("Valor de mercado máximo (€)", min_value=0, value=10_000_000, step=500_000)
    use_contract_filter = controls_e.checkbox("Filtrar por contrato próximo")
    contract_months = controls_f.slider("Meses hasta fin de contrato", 1, 60, 24, disabled=not use_contract_filter)
    top_n = st.slider("Número de resultados", 3, 25, 10)

    try:
        opportunities = find_market_opportunities(
            df,
            positions=positions or None,
            max_age=int(max_age),
            min_minutes=int(min_minutes),
            max_market_value=float(max_market_value) if max_market_value else None,
            contract_within_months=int(contract_months) if use_contract_filter else None,
            top_n=int(top_n),
        )
    except ValueError as exc:
        st.error(str(exc))
        return

    if opportunities.empty:
        st.info(
            "No hay jugadores que cumplan estos filtros. Prueba a ampliar edad, minutos mínimos, "
            "valor de mercado o desactivar el filtro de contrato."
        )
        return

    ranking_columns = [
        "player",
        "age",
        "position",
        "team",
        "league",
        "season",
        "minutes",
        "market_value",
        "contract_end",
        "overall_score",
        "attacking_impact_score",
        "chance_creation_score",
        "ball_progression_score",
        "defensive_impact_score",
        "dribbling_threat_score",
        "market_opportunity_score",
    ]
    st.dataframe(
        opportunities[[column for column in ranking_columns if column in opportunities.columns]],
        width="stretch",
        hide_index=True,
    )
    st.plotly_chart(create_opportunity_bar_chart(opportunities), width="stretch")

    selected_player = st.selectbox("Detalle del jugador", opportunities["player"].tolist())
    selected_row = opportunities[opportunities["player"] == selected_player].iloc[0]
    detail_metrics = [metric for metric in RADAR_METRICS if metric in opportunities.columns]
    if detail_metrics:
        st.plotly_chart(create_radar_chart(opportunities, [selected_player], detail_metrics), width="stretch")

    card_a, card_b, card_c, card_d = st.columns(4)
    card_a.metric("Overall", selected_row.get("overall_score", 0))
    card_b.metric("Opportunity", selected_row.get("market_opportunity_score", 0))
    card_c.metric("Edad", selected_row.get("age", ""))
    card_d.metric("Valor de mercado", format_euros(selected_row.get("market_value", 0)))

    detail_a, detail_b, detail_c = st.columns(3)
    detail_a.markdown(f"**Posición:** {selected_row.get('position', '')}")
    detail_a.markdown(f"**Equipo:** {selected_row.get('team', '')}")
    detail_b.markdown(f"**Liga:** {selected_row.get('league', '')}")
    detail_b.markdown(f"**Temporada:** {selected_row.get('season', '')}")
    detail_c.markdown(f"**Fin de contrato:** {selected_row.get('contract_end', '')}")
    detail_c.markdown(f"**Valor de mercado:** {format_euros(selected_row.get('market_value', 0))}")


def render_intro() -> None:
    st.markdown(
        "Aplicación de scouting basada en datos para buscar jugadores, comparar perfiles, "
        "encontrar similares y detectar oportunidades de mercado."
    )
    with st.expander("Flujo recomendado", expanded=True):
        st.markdown(
            """
1. Filtra jugadores por liga, posición, edad y minutos.
2. Revisa la tabla y los scores.
3. Compara perfiles.
4. Busca jugadores similares.
5. Usa Opportunity Finder para detectar candidatos infravalorados.
6. Genera informes desde la pestaña de similitud.
            """.strip()
        )


def main() -> None:
    st.title("Football Scout Dashboard")
    render_intro()

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

    tab_table, tab_compare, tab_similarity, tab_opportunity = st.tabs(
        ["Tabla", "Comparador", "Similitud + informe", "Opportunity Finder"]
    )
    with tab_table:
        player_table(filtered)
    with tab_compare:
        comparison_view(filtered)
    with tab_similarity:
        if filtered.empty:
            st.info("Ajusta los filtros para seleccionar jugadores.")
        else:
            similarity_and_report_view(filtered)
    with tab_opportunity:
        opportunity_finder_view(filtered)


if __name__ == "__main__":
    main()
