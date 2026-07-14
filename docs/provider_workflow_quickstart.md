# Provider Workflow Quickstart

## Objective

This guide summarizes the safe workflow for moving from a candidate provider or source to a local canonical Market Context output. The app should never depend on live provider calls at runtime; provider data must pass through local review, canonical transformation, validation and diagnostics before explicit activation.

## Workflow Summary

1. Review or create provider decision record.
2. Check provider cache policy.
3. Build or obtain normalized records.
4. Apply reviewed identity mapping to provider records.
5. Build canonical Market Context rows.
6. Preview canonical CSV.
7. Validate canonical CSV.
8. Run Market Context diagnostics.
9. Activate explicitly with env var.
10. Review app Fuente de datos and Opportunity Finder.
11. Keep real provider data local and ignored.

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

## Step 4 - Apply Reviewed Identity Mapping

Apply only reviewed `matched` identities to normalized provider records:

```powershell
.venv\Scripts\python.exe scripts\apply_provider_identity_mapping.py --records docs\examples\provider_fixture_records_sample.csv --mapping docs\examples\provider_identity_mapping_sample.csv --output data\enrichment\provider_fixture_records_mapped.generated.local.csv --force
```

The mapped `.local.csv` is an intermediate artifact. It is not canonical Market Context and should
remain local and ignored.

## Step 5 - Synthetic Example

Use the synthetic example at [`docs/examples/provider_market_context_canonical_sample.csv`](examples/provider_market_context_canonical_sample.csv) to understand the expected format.

```powershell
.venv\Scripts\python.exe scripts\preview_provider_market_context.py --input docs\examples\provider_market_context_canonical_sample.csv --show-columns
```

## Step 6 - Preview Provider Canonical Output

Build a canonical CSV from already-normalized local records:

```powershell
.venv\Scripts\python.exe scripts\build_provider_market_context_canonical.py --input docs\examples\provider_market_context_normalized_records_sample.csv --output data\enrichment\provider_market_context_canonical.generated.local.csv --include-optional-fields --force
```

The generated `.local.csv` output should stay local and ignored. It is a review artifact, not a provider integration.

Then preview the generated output:

```powershell
.venv\Scripts\python.exe scripts\preview_provider_market_context.py --input data\enrichment\provider_market_context_canonical.generated.local.csv --show-columns
```

Preview a candidate canonical CSV before diagnostics or app activation:

```powershell
.venv\Scripts\python.exe scripts\preview_provider_market_context.py --input path\to\canonical_market_context.csv --show-columns --fail-on-validation-errors
```

Expected checks:

- `Missing canonical columns: None`
- `Validation error count: 0`
- `Extra columns` only lists non-recognized columns.

## Step 7 - Diagnostics Against Active Dataset

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

## Step 8 - Explicit App Activation

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

Apply reviewed identity mapping to provider records:

```powershell
.venv\Scripts\python.exe scripts\apply_provider_identity_mapping.py --records docs\examples\provider_fixture_records_sample.csv --mapping docs\examples\provider_identity_mapping_sample.csv --output data\enrichment\provider_fixture_records_mapped.generated.local.csv --force
```

Build canonical CSV from normalized records:

```powershell
.venv\Scripts\python.exe scripts\build_provider_market_context_canonical.py --input docs\examples\provider_market_context_normalized_records_sample.csv --output data\enrichment\provider_market_context_canonical.generated.local.csv --include-optional-fields --force
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
