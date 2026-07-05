from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src.config import DATABASE_PATH, RADAR_METRICS
from src.data_cleaning import clean_player_data
from src.data_quality import calculate_data_quality_metrics
from src.data_sources import load_players_data_with_metadata
from src.features import add_per90_metrics, add_position_percentiles
from src.opportunity import find_market_opportunities
from src.reports import render_scouting_report, save_scouting_report
from src.scoring import add_profile_scores
from src.similarity import find_similar_players
from src.visualizations import create_opportunity_bar_chart, create_radar_chart


st.set_page_config(page_title="Football Scout Dashboard", page_icon=":soccer:", layout="wide")


@st.cache_data(show_spinner=False)
def load_default_data_with_metadata(sqlite_version: tuple[float, int] | None = None) -> tuple[pd.DataFrame, dict]:
    return load_players_data_with_metadata()


@st.cache_data(show_spinner=False)
def prepare_data(raw: pd.DataFrame) -> pd.DataFrame:
    cleaned = clean_player_data(raw)
    featured = add_per90_metrics(cleaned)
    percentiles = add_position_percentiles(featured)
    return add_profile_scores(percentiles)


def get_sqlite_data_version(database_path: Path) -> tuple[float, int] | None:
    if not database_path.exists():
        return None
    stat = database_path.stat()
    return stat.st_mtime, stat.st_size


def is_false_flag(value: object) -> bool:
    if value is None:
        return False
    try:
        if pd.isna(value):
            return False
    except (TypeError, ValueError):
        pass
    if isinstance(value, str):
        return value.strip().lower() == "false"
    return bool(value) is False


def is_true_flag(value: object) -> bool:
    if value is None:
        return False
    try:
        if pd.isna(value):
            return False
    except (TypeError, ValueError):
        pass
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value) is True


def format_euros(value: object, value_known: object | None = None) -> str:
    if is_false_flag(value_known):
        return "Desconocido"
    amount = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(amount) or amount <= 0:
        return "Desconocido"
    return f"{int(amount):,}".replace(",", ".") + " €"


def format_age(value: object, age_known: object | None = None) -> str:
    if is_false_flag(age_known):
        return "Desconocida"
    age = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(age) or age <= 0:
        return "Desconocida"
    return str(int(age))


def format_score(value: object, decimals: int = 1) -> str:
    number = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(number):
        return ""
    return f"{number:.{decimals}f}"


def format_number(value: object, decimals: int = 2) -> str:
    number = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(number):
        return ""
    return f"{number:.{decimals}f}"


def format_display_columns(
    df: pd.DataFrame,
    currency_columns: list[str] | None = None,
    age_columns: list[str] | None = None,
    one_decimal_columns: list[str] | None = None,
    two_decimal_columns: list[str] | None = None,
    three_decimal_columns: list[str] | None = None,
) -> pd.DataFrame:
    display_df = df.copy()
    for column in currency_columns or []:
        if column in display_df.columns:
            known_column = f"{column}_known"
            if known_column in display_df.columns:
                display_df[column] = display_df.apply(
                    lambda row: format_euros(row[column], row[known_column]),
                    axis=1,
                )
            else:
                display_df[column] = display_df[column].apply(format_euros)
    for column in age_columns or []:
        if column in display_df.columns:
            if "age_known" in display_df.columns:
                display_df[column] = display_df.apply(
                    lambda row: format_age(row[column], row["age_known"]),
                    axis=1,
                )
            else:
                display_df[column] = display_df[column].apply(format_age)
    for column in one_decimal_columns or []:
        if column in display_df.columns:
            display_df[column] = display_df[column].apply(lambda value: format_score(value, 1))
    for column in two_decimal_columns or []:
        if column in display_df.columns:
            display_df[column] = display_df[column].apply(lambda value: format_number(value, 2))
    for column in three_decimal_columns or []:
        if column in display_df.columns:
            display_df[column] = display_df[column].apply(lambda value: format_number(value, 3))
    display_df = display_df.drop(
        columns=[column for column in ["age_known", "market_value_known"] if column in display_df.columns]
    )
    return display_df


def get_known_age_values(df: pd.DataFrame) -> pd.Series:
    if "age" not in df.columns:
        return pd.Series(dtype="int64")

    ages = pd.to_numeric(df["age"], errors="coerce")
    valid_mask = ages.notna() & (ages > 0)
    if "age_known" in df.columns:
        valid_mask = valid_mask & df["age_known"].apply(is_true_flag)

    return ages[valid_mask].astype(int).drop_duplicates().sort_values()


def get_known_age_bounds(df: pd.DataFrame) -> tuple[int, int] | None:
    ages = get_known_age_values(df)
    if ages.empty:
        return None
    min_age = int(ages.min())
    max_age = int(ages.max())
    if min_age == max_age:
        return None
    return min_age, max_age


def apply_age_filter(df: pd.DataFrame, selected_range: tuple[int, int] | None) -> pd.DataFrame:
    if selected_range is None or "age" not in df.columns:
        return df

    ages = pd.to_numeric(df["age"], errors="coerce")
    mask = ages.between(selected_range[0], selected_range[1])
    if "age_known" in df.columns:
        mask = mask & df["age_known"].apply(is_true_flag)
    return df[mask]


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
        age_values = get_known_age_values(df)
        age_bounds = get_known_age_bounds(df)
        age_range = None
        if age_bounds is None:
            if age_values.empty:
                st.info("Edad no disponible en la fuente actual.")
            else:
                st.caption(f"Todas las edades conocidas son {int(age_values.iloc[0])}.")
        else:
            age_range = st.slider("Rango de edad", age_bounds[0], age_bounds[1], age_bounds)
            if age_range == age_bounds:
                age_range = None
        min_minutes = st.slider("Minutos mínimos", 0, int(df["minutes"].max()), min(900, int(df["minutes"].max())))
        search = st.text_input("Buscar jugador")

    filtered = df[
        df["league"].isin(leagues)
        & df["position"].isin(positions)
        & (df["minutes"] >= min_minutes)
    ]
    filtered = apply_age_filter(filtered, age_range)
    if teams:
        filtered = filtered[filtered["team"].isin(teams)]
    if search:
        filtered = filtered[filtered["player"].str.contains(search, case=False, na=False)]
    return filtered


def player_table(df: pd.DataFrame) -> None:
    display_columns = [
        "player",
        "age",
        "age_known",
        "position",
        "team",
        "league",
        "minutes",
        "market_value",
        "market_value_known",
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
    visible_columns = [column for column in display_columns if column in df.columns]
    sorted_df = df[visible_columns].sort_values("overall_score", ascending=False)
    display_df = format_display_columns(
        sorted_df,
        currency_columns=["market_value"],
        age_columns=["age"],
        one_decimal_columns=[
            "overall_score",
            "market_opportunity_score",
            "attacking_impact_score",
            "chance_creation_score",
            "ball_progression_score",
            "defensive_impact_score",
            "dribbling_threat_score",
        ],
        two_decimal_columns=["goals_per90", "assists_per90", "xg_per90", "xa_per90"],
    )
    st.dataframe(
        display_df,
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
    similar_columns = [
        "player",
        "age",
        "age_known",
        "position",
        "team",
        "league",
        "market_value",
        "market_value_known",
        "similarity",
        "overall_score",
        "market_opportunity_score",
    ]
    similar_display = format_display_columns(
        similar[[column for column in similar_columns if column in similar.columns]],
        currency_columns=["market_value"],
        age_columns=["age"],
        one_decimal_columns=["overall_score", "market_opportunity_score"],
        three_decimal_columns=["similarity"],
    )
    st.dataframe(
        similar_display,
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
        "age_known",
        "position",
        "team",
        "league",
        "season",
        "minutes",
        "market_value",
        "market_value_known",
        "contract_end",
        "overall_score",
        "attacking_impact_score",
        "chance_creation_score",
        "ball_progression_score",
        "defensive_impact_score",
        "dribbling_threat_score",
        "market_opportunity_score",
    ]
    opportunity_display = format_display_columns(
        opportunities[[column for column in ranking_columns if column in opportunities.columns]],
        currency_columns=["market_value"],
        age_columns=["age"],
        one_decimal_columns=[
            "overall_score",
            "attacking_impact_score",
            "chance_creation_score",
            "ball_progression_score",
            "defensive_impact_score",
            "dribbling_threat_score",
            "market_opportunity_score",
        ],
    )
    st.dataframe(
        opportunity_display,
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
    card_c.metric("Edad", format_age(selected_row.get("age", ""), selected_row.get("age_known", None)))
    card_d.metric(
        "Valor de mercado",
        format_euros(selected_row.get("market_value", 0), selected_row.get("market_value_known", None)),
    )

    detail_a, detail_b, detail_c = st.columns(3)
    detail_a.markdown(f"**Posición:** {selected_row.get('position', '')}")
    detail_a.markdown(f"**Equipo:** {selected_row.get('team', '')}")
    detail_b.markdown(f"**Liga:** {selected_row.get('league', '')}")
    detail_b.markdown(f"**Temporada:** {selected_row.get('season', '')}")
    detail_c.markdown(f"**Fin de contrato:** {selected_row.get('contract_end', '')}")
    detail_c.markdown(
        f"**Valor de mercado:** "
        f"{format_euros(selected_row.get('market_value', 0), selected_row.get('market_value_known', None))}"
    )


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


def render_data_source(metadata: dict) -> None:
    source_labels = {
        "sqlite": "SQLite",
        "external": "Proveedor externo",
        "csv": "CSV fallback",
        "upload": "Upload manual",
    }
    source = metadata.get("source", "unknown")
    with st.expander("Fuente de datos", expanded=False):
        st.markdown(f"**Fuente activa:** {source_labels.get(source, source)}")
        st.markdown(f"**Filas cargadas:** {metadata.get('row_count', 0)}")
        if source == "sqlite":
            st.markdown(f"**Base de datos:** `{metadata.get('path', '')}`")
            st.markdown(f"**Tabla:** `{metadata.get('table', '')}`")
        elif source == "external":
            st.markdown(f"**URL:** `{metadata.get('url', '')}`")
        elif source == "csv":
            st.markdown(f"**CSV:** `{metadata.get('path', '')}`")
        elif source == "upload":
            st.markdown(f"**Archivo:** `{metadata.get('path', '')}`")


def render_data_quality(metrics: dict[str, object]) -> None:
    with st.expander("Calidad de datos", expanded=False):
        row_a = st.columns(4)
        row_a[0].metric("Jugadores", metrics["players_count"])
        row_a[1].metric("Equipos", metrics["teams_count"])
        row_a[2].metric("Ligas", metrics["leagues_count"])
        row_a[3].metric("Minutos totales", metrics["total_minutes"])

        row_b = st.columns(4)
        row_b[0].metric("Posiciones", metrics["positions_count"])
        row_b[1].metric("Edad conocida", f"{metrics['age_known_pct']}%")
        row_b[2].metric("Valor mercado conocido", f"{metrics['market_value_known_pct']}%")
        row_b[3].metric("Contrato conocido", f"{metrics['contract_known_pct']}%")


def main() -> None:
    st.title("Football Scout Dashboard")
    render_intro()

    uploaded = st.sidebar.file_uploader("Cargar CSV", type=["csv"])
    if uploaded:
        raw = pd.read_csv(uploaded)
        data_source_metadata = {
            "source": "upload",
            "path": uploaded.name,
            "row_count": len(raw),
        }
    else:
        try:
            sqlite_version = get_sqlite_data_version(DATABASE_PATH)
            raw, data_source_metadata = load_default_data_with_metadata(sqlite_version=sqlite_version)
        except ValueError as exc:
            st.error(str(exc))
            st.stop()

    try:
        df = prepare_data(raw)
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    render_data_source(data_source_metadata)
    render_data_quality(calculate_data_quality_metrics(df))

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
