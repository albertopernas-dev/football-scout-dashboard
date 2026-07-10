# Release Notes v0.3.0 - Real Enrichment Workflow

## Overview

v0.3.0 turns the Market Context Layer into a practical manual enrichment workflow.

The release supports moving from identity-only sample rows to locally reviewed market context data while keeping the dashboard transparent, reproducible and conservative.

This release does not add scraping, does not version real reviewed CSVs and does not change the general performance scoring model.

## What Changed

- Added a local seed export workflow for market context review.
- Added safeguards to avoid overwriting reviewed enrichment files.
- Hardened market context CSV validation.
- Fixed diagnostics so explicit `--market-context-csv` runs against a base dataset, avoiding double merges from environment configuration.
- Improved Opportunity Finder display so effective market context values are visible as the primary market fields.
- Kept original market fields visible as reference when effective values exist.
- Kept general sporting scoring unchanged.

## Real Enrichment Workflow

Generate a local seed CSV from the current Opportunity Finder candidates:

```powershell
.venv\Scripts\python.exe scripts\export_enrichment_seed.py --top-n 25
```

The seed fills only identity columns:

```text
player,team,league,season
```

It leaves enrichment fields empty for manual review:

```text
age,market_value_eur,contract_end_date,source,source_url,confidence,notes
```

Real reviewed files should remain local by default and use `.local.csv`, for example:

```text
data/enrichment/player_market_context_laliga_2024_reviewed.local.csv
```

## Validation And Safeguards

Validation rules:

- `age` must be an integer between 15 and 45.
- `market_value_eur` must be a positive number.
- `contract_end_date` must use strict ISO format: `YYYY-MM-DD`.
- `source` is required if `age`, `market_value_eur` or `contract_end_date` is filled.
- `confidence` is required if `age`, `market_value_eur` or `contract_end_date` is filled.
- `confidence` must be `low`, `medium` or `high`.
- Identity-only rows are valid.
- Unknown values must stay empty, not `0`.

Overwrite protection:

- If an output CSV exists, normal execution refuses to overwrite it.
- `--force` can regenerate empty seed files.
- If the existing CSV contains reviewed enrichment values, `--force` refuses to overwrite it.
- The dangerous escape hatch is:

```powershell
.venv\Scripts\python.exe scripts\export_enrichment_seed.py --top-n 25 --force-dangerously-overwrite-reviewed-data
```

That flag can delete reviewed values and should normally not be used.

## Opportunity Finder Display Improvements

Opportunity Finder now uses and displays effective market context clearly:

- `effective_age`
- `effective_market_value_eur`
- `effective_contract_end_date`
- `effective_market_context_source`

In the table and player detail, effective age, value and contract are shown as the primary market fields when available.

Original values remain visible as reference, but they no longer visually override reviewed effective values.

The general performance scoring remains unchanged.

## Local Data Policy

- Real reviewed enrichment CSVs are not versioned by default.
- Local reviewed CSVs should use `.local.csv`.
- `data/enrichment/*.local.csv` is ignored by git.
- `data/enrichment/*_reviewed.csv` is ignored by git.
- The versioned `player_market_context_sample.csv` remains identity-only and does not contain real market values, ages or contract dates.
- No scraping is included or recommended.

## Commands

Generate a seed:

```powershell
.venv\Scripts\python.exe scripts\export_enrichment_seed.py --top-n 25
```

Diagnose a reviewed local CSV:

```powershell
.venv\Scripts\python.exe scripts\diagnose_market_context.py --market-context-csv data\enrichment\player_market_context_laliga_2024_reviewed.local.csv
```

Activate reviewed enrichment in the app:

```powershell
$env:FOOTBALL_SCOUT_MARKET_CONTEXT_CSV="data/enrichment/player_market_context_laliga_2024_reviewed.local.csv"
.venv\Scripts\streamlit.exe run app.py
```

Clear the environment variable:

```powershell
Remove-Item Env:\FOOTBALL_SCOUT_MARKET_CONTEXT_CSV -ErrorAction SilentlyContinue
```

## Known Limitations

- Coverage depends on manual review.
- API-Football `fixtures/players` does not provide reliable age, market value or contract-end context for this workflow.
- Real reviewed local CSVs are not part of the release.
- There is no automatic market data provider integration yet.
- There is no scraping.
- General sporting scoring remains performance-based and unchanged.
- Opportunity Finder uses effective market fields, but coverage and source quality still determine how much market interpretation is justified.

## Recommended Verification

Run the full test suite:

```powershell
.venv\Scripts\python.exe -m pytest -p no:cacheprovider tests -q
```

Run diagnostics against the reviewed local CSV:

```powershell
.venv\Scripts\python.exe scripts\diagnose_market_context.py --market-context-csv data\enrichment\player_market_context_laliga_2024_reviewed.local.csv
```

Start Streamlit and confirm HTTP 200:

```powershell
$env:FOOTBALL_SCOUT_MARKET_CONTEXT_CSV="data/enrichment/player_market_context_laliga_2024_reviewed.local.csv"
.venv\Scripts\streamlit.exe run app.py
```

Manual checks:

- `Fuente de datos` shows market context enabled.
- Validation errors are `0`.
- Duplicate keys are `0`.
- Effective age/value/contract coverage is visible.
- Opportunity Finder shows effective market values in the table.
- Opportunity Finder player detail uses effective age, value and contract when available.
