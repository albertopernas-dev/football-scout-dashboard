# Football Scout Dashboard

MVP de scouting futbolistico construido con Python, Streamlit, pandas, scikit-learn, Plotly y una arquitectura modular preparada para evolucionar a FastAPI + Next.js.

## Funcionalidades

- Carga de CSV y uso de `data/sample_players.csv` por defecto.
- Normalizacion de columnas en espanol/ingles.
- Limpieza automatica y validacion de columnas obligatorias.
- Metricas por 90 minutos.
- Percentiles por posicion.
- Scores propios: finalizacion, creacion, progresion, defensa y overall.
- Market Opportunity Score para detectar jugadores infravalorados.
- Metricas de similitud especificas por posicion.
- Tabla filtrable.
- Comparador entre jugadores.
- Radar charts con Plotly.
- Jugadores similares mediante cosine similarity.
- Informes automaticos de scouting en HTML.

## Estructura

```text
football-scout-dashboard/
  app.py
  requirements.txt
  README.md
  data/
    sample_players.csv
  reports/
    generated/
  templates/
    scouting_report.html
  assets/
  notebooks/
  src/
    __init__.py
    config.py
    schema.py
    data_cleaning.py
    features.py
    scoring.py
    similarity.py
    visualizations.py
    reports.py
  tests/
    test_data_cleaning.py
    test_features.py
    test_similarity.py
    test_scoring.py
    test_reports.py
```

## Instalacion

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar

```bash
streamlit run app.py
```

## CSV esperado

Columnas canonicas recomendadas:

```text
player, age, position, team, league, minutes, goals, assists, xg, xa,
shots, key_passes, progressive_passes, progressive_carries,
completed_dribbles, duels_won, recoveries, interceptions,
season, market_value, contract_end
```

Tambien se aceptan aliases comunes en espanol, por ejemplo `Jugador`, `Edad`, `Posicion`, `Equipo`, `Liga`, `Minutos`, `Goles`, `Asistencias`, `Tiros`, `Pases clave`, `Pases progresivos`, `Conducciones progresivas`, `Regates completados`, `Duelos ganados`, `Recuperaciones` e `Intercepciones`.

## Demo use case

This MVP helps identify undervalued football players through statistical filters, position-based percentiles, similarity modelling and automated scouting reports.

Example:
Find U23 wingers with high dribbling volume, strong chance creation, good ball progression metrics and accessible market value.

The app returns:

- filtered player rankings;
- Market Opportunity Score;
- radar charts;
- similar players;
- automated scouting reports.

Suggested demo flow:

1. Open the app and use the default sample dataset.
2. Filter positions to `LW` and `RW`.
3. Set the age range to U23.
4. Sort by `market_opportunity_score`.
5. Compare the best candidate against a more established player.
6. Review the radar chart and similar players.
7. Generate the HTML scouting report.

## Tests

```bash
pytest
```

Los tests cubren la parte reusable del dominio. `app.py` se mantiene como una capa fina de UI para facilitar una futura migracion a FastAPI + Next.js.
