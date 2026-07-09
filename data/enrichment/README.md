# Market Context Enrichment

This folder contains versioned CSV files for the v0.2.0 Market Context Layer.

## Files

- `player_market_context_template.csv`: empty template with the required schema.
- `player_market_context_sample.csv`: minimal sample for validating schema, matching and diagnostics.

The sample does not contain real market values, real contract dates or verified ages. Its rows are identity-only examples for testing the workflow safely.

## Diagnostic command

Run the diagnostic script from the project root:

```powershell
.venv\Scripts\python.exe scripts/diagnose_market_context.py --market-context-csv data/enrichment/player_market_context_sample.csv
```

The command reads the active player dataset and the selected enrichment CSV. It reports validation errors, duplicate keys, merge coverage and matched/unmatched examples.

It does not modify SQLite and does not change the Streamlit app.

## Real enrichment data

For real enrichment, fill `age`, `market_value_eur`, `contract_end_date`, `source`, `confidence` and `notes` after manual review.

Keep unknown values empty. Do not use `0` for unknown age, market value or contract date.

Review source quality before adding values. Use the checklist in [`docs/enrichment_source_quality_checklist.md`](../../docs/enrichment_source_quality_checklist.md).

## Generate a local seed CSV

Create a local reviewed-file seed from the current Opportunity Finder ranking:

```powershell
.venv\Scripts\python.exe scripts/export_enrichment_seed.py --top-n 25 --force
```

By default this writes:

```text
data/enrichment/player_market_context_laliga_2024_reviewed.local.csv
```

The generated CSV only fills `player`, `team`, `league` and `season`. It intentionally leaves `age`, `market_value_eur`, `contract_end_date`, `source`, `source_url`, `confidence` and `notes` empty for manual review.

After generating the seed:

1. Review the source quality checklist.
2. Fill only manually reviewed values.
3. Keep unknown values empty.
4. Run diagnostics before activating the CSV.

## Real CSV policy

The versioned files in this folder are:

- `player_market_context_template.csv`
- `player_market_context_sample.csv`

Real reviewed enrichment CSVs should stay local by default unless there is clear permission to redistribute the data and sources.

Suggested local naming:

```text
player_market_context_laliga_2024_reviewed.local.csv
```

Activate a local reviewed CSV explicitly:

```powershell
$env:FOOTBALL_SCOUT_MARKET_CONTEXT_CSV="data/enrichment/player_market_context_laliga_2024_reviewed.local.csv"
```

Run diagnostics before opening the app with a real reviewed file:

```powershell
.venv\Scripts\python.exe scripts/diagnose_market_context.py --market-context-csv data/enrichment/player_market_context_laliga_2024_reviewed.local.csv
```

The diagnostic command should be clean before the CSV is used for scouting review:

- validation errors = 0;
- duplicate keys = 0;
- matched coverage reviewed;
- effective coverage reviewed.
