# Provider Workflow Quickstart

## Objective

This guide summarizes the safe workflow for moving from a candidate provider or source to a local canonical Market Context output. The app should never depend on live provider calls at runtime; provider data must pass through local review, canonical transformation, validation and diagnostics before explicit activation.

## Workflow Summary

1. Review or create provider decision record.
2. Check provider cache policy.
3. Build or obtain normalized records.
4. Build canonical Market Context rows.
5. Preview canonical CSV.
6. Validate canonical CSV.
7. Run Market Context diagnostics.
8. Activate explicitly with env var.
9. Review app Fuente de datos and Opportunity Finder.
10. Keep real provider data local and ignored.

## Step 1 - Provider Decision Record

Use [`docs/provider_decisions/`](provider_decisions/) for provider decision records.

Start from [`docs/provider_decisions/provider_decision_template.md`](provider_decisions/provider_decision_template.md). No provider should move to implementation without a decision record that covers fields, license, usage, caching, cost, risks and the final decision.

## Step 2 - Cache And License

Review [`docs/provider_cache_policy.md`](provider_cache_policy.md) before storing any provider output.

Key reminders:

- no credentials in repo;
- no raw dumps versioned;
- `data/provider_cache/` is ignored;
- provider terms must permit the intended caching and use.

## Step 3 - Canonical Transform Contract

Review [`docs/provider_to_market_context_transform_plan.md`](provider_to_market_context_transform_plan.md).

The reusable helper module is `src/provider_market_context.py`. It builds canonical rows from already-normalized records and does not implement real providers.

Minimum canonical schema:

```text
player,team,league,season,age,market_value_eur,contract_end_date,source,source_url,confidence,notes
```

## Step 4 - Synthetic Example

Use the synthetic example at [`docs/examples/provider_market_context_canonical_sample.csv`](examples/provider_market_context_canonical_sample.csv) to understand the expected format.

```powershell
.venv\Scripts\python.exe scripts\preview_provider_market_context.py --input docs\examples\provider_market_context_canonical_sample.csv --show-columns
```

## Step 5 - Preview Provider Canonical Output

Preview a candidate canonical CSV before diagnostics or app activation:

```powershell
.venv\Scripts\python.exe scripts\preview_provider_market_context.py --input path\to\canonical_market_context.csv --show-columns --fail-on-validation-errors
```

Expected checks:

- `Missing canonical columns: None`
- `Validation error count: 0`
- `Extra columns` only lists non-recognized columns.

## Step 6 - Diagnostics Against Active Dataset

Run Market Context diagnostics against the active dataset:

```powershell
.venv\Scripts\python.exe scripts\diagnose_market_context.py --market-context-csv path\to\canonical_market_context.csv
```

Review:

- validation errors are 0;
- duplicate keys are 0;
- matched count is reasonable;
- effective coverage is reviewed;
- unmatched examples are reviewed.

## Step 7 - Explicit App Activation

Activate a reviewed canonical CSV explicitly:

```powershell
$env:FOOTBALL_SCOUT_MARKET_CONTEXT_CSV="path/to/canonical_market_context.csv"
.venv\Scripts\streamlit.exe run app.py
```

Checks:

- Fuente de datos shows market context enabled;
- validation errors are 0;
- duplicate keys are 0;
- Opportunity Finder shows effective values when they exist.

## Safety Rules

- No scraping.
- No live provider calls from app.
- No raw provider dumps in git.
- No credentials in docs or code.
- No real canonical outputs versioned unless license explicitly allows it.
- No invented values to pass validation.
- No scoring changes until coverage is sufficient.

## Quick Commands

Preview synthetic sample:

```powershell
.venv\Scripts\python.exe scripts\preview_provider_market_context.py --input docs\examples\provider_market_context_canonical_sample.csv --show-columns
```

Preview candidate canonical CSV:

```powershell
.venv\Scripts\python.exe scripts\preview_provider_market_context.py --input path\to\canonical_market_context.csv --show-columns --fail-on-validation-errors
```

Diagnose candidate CSV:

```powershell
.venv\Scripts\python.exe scripts\diagnose_market_context.py --market-context-csv path\to\canonical_market_context.csv
```

Activate env var:

```powershell
$env:FOOTBALL_SCOUT_MARKET_CONTEXT_CSV="path/to/canonical_market_context.csv"
```

Clear env var:

```powershell
Remove-Item Env:\FOOTBALL_SCOUT_MARKET_CONTEXT_CSV -ErrorAction SilentlyContinue
```

## Related Docs

- [`docs/v0_4_0_provider_evaluation_plan.md`](v0_4_0_provider_evaluation_plan.md)
- [`docs/provider_cache_policy.md`](provider_cache_policy.md)
- [`docs/provider_to_market_context_transform_plan.md`](provider_to_market_context_transform_plan.md)
- [`docs/provider_decisions/provider_evaluation_matrix.md`](provider_decisions/provider_evaluation_matrix.md)
- [`docs/provider_decisions/provider_decision_template.md`](provider_decisions/provider_decision_template.md)
