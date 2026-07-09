# Football Scout Dashboard v0.2.0

## Summary

v0.2.0 focuses on the Market Context Layer: an opt-in workflow for enriching the local player dataset with manually reviewed market context without changing the general performance scoring.

The release keeps the v0.1.0 SQLite-first scouting dashboard stable while adding validation, diagnostics, app visibility and effective market fields for Opportunity Finder.

## Focus

Market Context Layer:

- optional enrichment CSV configured through `FOOTBALL_SCOUT_MARKET_CONTEXT_CSV`;
- schema validation for manual market context files;
- merge helpers for player/team/league/season matching;
- diagnostics CLI for validation, duplicates, match coverage and effective coverage;
- app status and coverage display;
- `market_context_*` display columns in the main table and Opportunity Finder;
- `effective_*` fields prepared in the data layer;
- Opportunity Finder uses effective age, market value and contract date;
- general scoring remains unchanged.

## Highlights

- Manual market context enrichment template in `data/enrichment/`.
- Identity-only sample CSV for diagnostics and UI testing.
- Validation rules for age, market value, contract date, source and confidence.
- Duplicate-key detection for enrichment rows.
- Effective market fields:
  - `effective_age`;
  - `effective_market_value_eur`;
  - `effective_contract_end_date`;
  - `effective_market_context_source`.
- Effective coverage shown in both CLI diagnostics and app UI.
- Opportunity Finder can use enriched values when valid context exists.
- Existing performance scoring, sample-adjusted rankings and goalkeeper handling remain intact.
- 408 passing tests.

## Verification

Commands used for validation:

```powershell
.venv\Scripts\python.exe -m pytest -p no:cacheprovider tests -q
```

Expected result:

```text
408 passed
```

Market context diagnostic sample:

```powershell
.venv\Scripts\python.exe scripts/diagnose_market_context.py --market-context-csv data/enrichment/player_market_context_sample.csv
```

Streamlit smoke:

```powershell
.venv\Scripts\streamlit.exe run app.py --server.headless true --server.port 8501
```

Expected result:

```text
http://localhost:8501 -> 200
```

## Demo Steps

1. Open the app without `FOOTBALL_SCOUT_MARKET_CONTEXT_CSV` and show limited market context.
2. Run the diagnostic command against `data/enrichment/player_market_context_sample.csv`.
3. Enable the sample CSV:

   ```powershell
   $env:FOOTBALL_SCOUT_MARKET_CONTEXT_CSV="data/enrichment/player_market_context_sample.csv"
   ```

4. Restart the app and open `Fuente de datos`.
5. Show market context match coverage and effective coverage.
6. Explain that the sample is identity-only, so effective age/value/contract coverage remains 0%.
7. Open Opportunity Finder and show the market/effective context columns.
8. Explain that Opportunity Finder will use effective values when real enrichment data exists.

## Known Limitations

- No real enrichment data is included.
- The sample CSV is identity-only and does not contain real age, market value or contract values.
- No automated market-data provider is connected yet.
- No scraping is included.
- General scoring remains performance-based and unchanged.
- Opportunity Finder depends on enrichment quality when evaluating true market context.
- Partial enrichment coverage can bias interpretation if not reviewed carefully.

## Suggested GitHub Release Text

```markdown
## Football Scout Dashboard v0.2.0

This release adds the Market Context Layer.

Highlights:
- Optional market context CSV via `FOOTBALL_SCOUT_MARKET_CONTEXT_CSV`.
- Schema validation, duplicate detection and diagnostics CLI.
- Market context and effective coverage visible in the app.
- Effective age, market value and contract fields prepared in the data layer.
- Opportunity Finder now uses effective age/value/contract when available.
- General performance scoring remains unchanged.
- 408 passing tests.

Limitations:
- No real enrichment data is included.
- The sample CSV is identity-only.
- No automated market-data provider is connected yet.
- General scoring remains performance-based.
```
