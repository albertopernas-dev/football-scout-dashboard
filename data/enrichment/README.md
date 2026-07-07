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
