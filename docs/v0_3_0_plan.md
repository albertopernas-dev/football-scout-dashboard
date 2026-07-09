# v0.3.0 Plan: Real Enrichment Workflow

## Objective

v0.3.0 should turn the Market Context Layer from an identity-only sample workflow into a usable manual enrichment workflow with real reviewed data.

The goal is to:

- create a reliable process for adding real age, market value and contract context;
- preserve source, confidence and notes for every enriched value;
- avoid scraping and unreviewed data collection;
- keep general performance scoring unchanged unless there is enough evidence and coverage to justify changes;
- make Opportunity Finder more useful without hiding uncertainty.

## Scope

Included:

- workflow for creating a real market context enrichment CSV;
- source and confidence criteria;
- mandatory validation before use;
- mandatory diagnostics before enabling the CSV in the app;
- checklist before activating enrichment in Streamlit;
- minimum coverage criteria before considering Opportunity Finder weighting changes.

Out of scope:

- scraping;
- automatic external provider integration;
- general scoring changes;
- goalkeeper model changes;
- automatic transfer recommendations.

## Expected Real CSV

Use the existing schema:

```text
player,team,league,season,age,market_value_eur,contract_end_date,source,source_url,confidence,notes
```

Rules:

- Do not use `0` for unknown values.
- Leave unknown fields empty.
- `source` is required when any enrichment value is filled.
- `confidence` must be `low`, `medium` or `high`.
- `notes` should include brief context for the row, especially ambiguity or manual assumptions.
- `source_url` is optional but recommended.
- Duplicate player/team/league/season keys must be reviewed before use.
- Real values should come from manually reviewed, traceable sources.

## Proposed Workflow

1. Copy the template:

   ```powershell
   Copy-Item data/enrichment/player_market_context_template.csv data/enrichment/player_market_context_laliga_2024_reviewed.csv
   ```

2. Start with a small first batch, for example the top 25 players from Opportunity Finder.
3. Fill only values that have been manually reviewed.
4. Keep unknown values empty.
5. Add `source`, optional `source_url`, `confidence` and `notes`.
6. Run diagnostics:

   ```powershell
   .venv\Scripts\python.exe scripts/diagnose_market_context.py --market-context-csv data/enrichment/player_market_context_laliga_2024_reviewed.csv
   ```

7. Review validation errors.
8. Review duplicate keys.
9. Review matched and unmatched examples.
10. Review effective age, value and contract coverage.
11. Enable the CSV explicitly:

    ```powershell
    $env:FOOTBALL_SCOUT_MARKET_CONTEXT_CSV="data/enrichment/player_market_context_laliga_2024_reviewed.csv"
    ```

12. Open the app and check `Fuente de datos`.
13. Confirm market context coverage and effective coverage.
14. Review Opportunity Finder with effective context columns visible.
15. Export a shortlist CSV.
16. Document coverage and known gaps.

## Quality Gates

Before using a real enrichment CSV for scouting decisions:

- validation errors = 0;
- duplicate keys = 0;
- matched_pct is reasonable for the selected batch;
- effective age coverage is reported;
- effective market value coverage is reported;
- effective contract coverage is reported;
- no doubtful sources are used without low confidence and clear notes;
- no values are invented to improve coverage;
- unknown values remain empty;
- sample identity-only rows are not treated as real market data.

Before considering Opportunity Finder weighting changes:

- enrichment coverage should be broad enough for the target shortlist;
- source quality should be consistent;
- market value and contract fields should not be sparse outliers;
- coverage bias should be reviewed;
- rankings should be compared before and after enrichment;
- changes should be backed by diagnostics and tests.

## Future Automation

Automation can be explored after the manual workflow is proven.

Future options:

- evaluate official/API-based market data providers;
- compare coverage, cost, update frequency and license constraints;
- keep raw provider responses cached locally when allowed;
- preserve `source`, `source_url`, `confidence` and `notes`;
- avoid mixing automated values with manual values unless provenance is explicit;
- keep validation and diagnostics mandatory before app use.

Scraping remains out of scope.

## Suggested GitHub Issues

- Build first real enrichment CSV for LaLiga 2024 top opportunities.
- Add enrichment source quality checklist.
- Add app filter for effective market context source.
- Add coverage threshold warning for Opportunity Finder.
- Evaluate market data providers.
- Add saved shortlists.

## Definition of Done

- A reviewed enrichment CSV exists for a small real batch.
- Diagnostics pass with validation errors = 0.
- Duplicate keys are resolved or explicitly documented.
- Effective coverage is visible and documented.
- The app can be run with the reviewed CSV via `FOOTBALL_SCOUT_MARKET_CONTEXT_CSV`.
- Opportunity Finder uses effective values without changing general scoring.
- Remaining market-context gaps are documented.
