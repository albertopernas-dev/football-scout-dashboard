# Football Scout Dashboard Design

## Goal

Build a Streamlit MVP for football scouting that loads player CSV data, normalizes it, compares players, finds similar profiles, visualizes radar charts, and generates HTML scouting reports.

## Architecture

The project uses Streamlit as a thin UI layer over reusable Python modules in `src/`. Data contracts and aliases live in `src/schema.py`, transformations live in `src/data_cleaning.py` and `src/features.py`, domain scoring lives in `src/scoring.py`, similarity search lives in `src/similarity.py`, Plotly figures live in `src/visualizations.py`, and HTML report rendering lives in `src/reports.py`.

## Data Flow

CSV input is normalized to canonical column names, required fields are validated, numeric fields are coerced, and missing stat values are filled with zero. Per-90 metrics are derived from raw counting stats, percentiles are calculated within position groups, custom profile scores are computed from normalized per-90 stats, and cosine similarity uses a selected feature matrix.

## UI

The first screen is the working dashboard. It defaults to `data/sample_players.csv`, accepts uploaded CSVs, exposes sidebar filters for league/team/position/minutes, displays a player table, compares two players, shows radar charts, lists similar players, and lets the user download an HTML report.

## Testing

Focused pytest coverage validates schema normalization, cleaning behavior, per-90 and percentile generation, scoring, and similarity ranking.
