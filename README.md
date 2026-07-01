# Football Scout Dashboard

MVP de scouting futbolístico construido con Python, Streamlit, pandas, scikit-learn, Plotly y una arquitectura modular preparada para evolucionar a FastAPI + Next.js.

## Funcionalidades

- Carga de CSV y uso de `data/sample_players.csv` por defecto.
- Normalización de columnas en español/ingles.
- Limpieza automática y validación de columnas obligatorias.
- Métricas por 90 minutos.
- Percentiles por posicion.
- Scores propios: finalización, creación, progresión, defensa y overall.
- Market Opportunity Score para detectar jugadores infravalorados.
- Opportunity Finder para rankear candidatos según edad, minutos, mercado y contrato.
- Métricas de similitud especificas por posición.
- Tabla filtrable.
- Comparador entre jugadores.
- Radar charts con Plotly.
- Jugadores similares mediante cosine similarity.
- Informes automáticos de scouting en HTML.

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
    opportunity.py
    visualizations.py
    reports.py
  tests/
    test_data_cleaning.py
    test_features.py
    test_similarity.py
    test_scoring.py
    test_reports.py
    test_opportunity.py
```

## Instalación

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

Columnas canónicas recomendadas:

```text
player, age, position, team, league, minutes, goals, assists, xg, xa,
shots, key_passes, progressive_passes, progressive_carries,
completed_dribbles, duels_won, recoveries, interceptions,
season, market_value, contract_end
```

También se aceptan aliases comunes en español, por ejemplo `Jugador`, `Edad`, `Posicion`, `Equipo`, `Liga`, `Minutos`, `Goles`, `Asistencias`, `Tiros`, `Pases clave`, `Pases progresivos`, `Conducciones progresivas`, `Regates completados`, `Duelos ganados`, `Recuperaciones` e `Intercepciones`.

## Data sources

La fuente principal prevista es SQLite, usando por defecto `data/football_scout.db` y la tabla `players`.

El proveedor externo es opcional y se activa configurando `EXTERNAL_PROVIDER_URL`. Esta capa solo prepara el punto de integración: no incluye scraping, credenciales reales ni llamadas obligatorias a servicios externos.

El CSV `data/sample_players.csv` queda como fallback y dataset de demo si SQLite o el proveedor externo no devuelven datos.

El upload manual de CSV en Streamlit sigue disponible y tiene prioridad sobre la carga por defecto.

## SQLite local ingestion

Genera la base local SQLite desde el CSV de ejemplo con:

```bash
.venv\Scripts\python.exe scripts/load_sample_to_sqlite.py
```

El script carga `data/sample_players.csv` en `data/football_scout.db`, tabla `players`. Después de ejecutarlo, la app cargará SQLite como fuente principal por defecto. Si la base no existe, la capa de datos cae al CSV de demo.

## External provider ingestion

La app permite preparar una ingesta desde `EXTERNAL_PROVIDER_URL` hacia SQLite. El proveedor debe devolver JSON como lista de jugadores o como objeto con clave `players`.

`.env.example` es solo una plantilla. El proyecto actualmente no carga archivos `.env` automaticamente, asi que define `EXTERNAL_PROVIDER_URL` en la sesion antes de ejecutar la ingesta.

Ejemplo en PowerShell:

```powershell
$env:EXTERNAL_PROVIDER_URL="https://example.com/players.json"
.venv\Scripts\python.exe scripts/load_external_to_sqlite.py
```

El script carga los datos en `data/football_scout.db`, tabla `players`. Todavía no hay proveedor específico implementado, credenciales reales ni scraping.

## External normalization

Los datos externos se normalizan al esquema interno antes de guardarse en SQLite. Existe soporte genérico para registros planos con aliases comunes y un primer adaptador preparado para estructuras tipo API-Football.

Todavía no hay conexión real a un proveedor específico, credenciales ni scraping. Esta capa solo prepara la transformación de payloads externos hacia columnas canónicas como `player`, `team`, `league`, `minutes`, `goals`, `assists` y métricas relacionadas.

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

## Flujo recomendado

1. Filtra jugadores por liga, posición, edad y minutos.
2. Revisa la tabla y los scores.
3. Compara perfiles.
4. Busca jugadores similares.
5. Usa Opportunity Finder para detectar candidatos infravalorados.
6. Genera informes desde la pestaña de similitud.

## Opportunity Finder

Opportunity Finder ayuda a convertir el `market_opportunity_score` en un ranking accionable de scouting. Permite buscar jugadores jóvenes, con minutos suficientes, valor de mercado acotado y, opcionalmente, contrato próximo a finalizar.

Problema que resuelve: reduce una tabla amplia de estadísticas a una lista corta de candidatos potencialmente infravalorados.

Ejemplo:
Buscar extremos sub-23 con alto impacto ofensivo, buen regate, valor de mercado bajo y contrato próximo a finalizar.

## Tests

```bash
pytest
```

Los tests cubren la parte reusable del dominio. `app.py` se mantiene como una capa fina de UI para facilitar una futura migración a FastAPI + Next.js.
