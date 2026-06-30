# Football Scout Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a modular Streamlit MVP for football scouting.

**Architecture:** Streamlit orchestrates CSV upload, filtering, comparison, similarity, visualizations, and report generation. Reusable business logic lives under `src/` with tests covering the reusable modules.

**Tech Stack:** Python, Streamlit, pandas, scikit-learn, Plotly, DuckDB, pytest, HTML reports.

## Global Constraints

Use the exact project folder `C:\Users\alber\04_Desarrollo\football-scout-dashboard`.
Keep modules easy to migrate to FastAPI + Next.js by avoiding Streamlit dependencies inside `src/`.
Support Spanish and English column aliases.
Use `data/sample_players.csv` by default.

---

### Task 1: Data Contract And Cleaning

**Files:**
- Create: `src/schema.py`
- Create: `src/data_cleaning.py`
- Test: `tests/test_data_cleaning.py`

**Interfaces:**
- Produces: `normalize_columns(df: pd.DataFrame) -> pd.DataFrame`
- Produces: `validate_required_columns(df: pd.DataFrame) -> None`
- Produces: `clean_player_data(df: pd.DataFrame) -> pd.DataFrame`

- [x] Write failing tests for alias normalization, required validation, numeric coercion, and stat fill.
- [x] Run tests and confirm they fail because modules do not exist.
- [x] Implement schema and cleaning functions.
- [x] Run tests and confirm they pass.

### Task 2: Features, Scoring, And Similarity

**Files:**
- Create: `src/features.py`
- Create: `src/scoring.py`
- Create: `src/similarity.py`
- Test: `tests/test_features.py`
- Test: `tests/test_scoring.py`
- Test: `tests/test_similarity.py`

**Interfaces:**
- Produces: `add_per90_metrics(df: pd.DataFrame) -> pd.DataFrame`
- Produces: `add_position_percentiles(df: pd.DataFrame) -> pd.DataFrame`
- Produces: `add_profile_scores(df: pd.DataFrame) -> pd.DataFrame`
- Produces: `find_similar_players(df: pd.DataFrame, player_name: str, top_n: int = 5) -> pd.DataFrame`

- [x] Write failing tests for per-90 metrics, percentiles, scoring, and similarity.
- [x] Run tests and confirm they fail because modules do not exist.
- [x] Implement minimal reusable logic.
- [x] Run tests and confirm they pass.

### Task 3: UI, Visualizations, Reports, And Docs

**Files:**
- Create: `app.py`
- Create: `src/config.py`
- Create: `src/visualizations.py`
- Create: `src/reports.py`
- Create: `templates/scouting_report.html`
- Create: `data/sample_players.csv`
- Create: `requirements.txt`
- Create: `README.md`

**Interfaces:**
- Produces: `create_radar_chart(...) -> plotly.graph_objects.Figure`
- Produces: `render_scouting_report(...) -> str`
- Produces: a functional Streamlit app.

- [x] Build the app around tested modules.
- [x] Add sample data and HTML report template.
- [x] Add dependency and usage documentation.
- [x] Run module tests and import checks.
