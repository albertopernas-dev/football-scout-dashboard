# v0.4.0 - Provider Evaluation Workflow

## Summary

v0.4.0 does not integrate a real provider yet. It prepares a safe, offline and validated workflow to evaluate data providers, transform already-normalized records into canonical Market Context, preview outputs, validate them, run diagnostics and activate them explicitly.

The goal is to make future provider work auditable without adding scraping, runtime provider calls or unreviewed data paths.

## Highlights

- Provider evaluation plan.
- Provider decision records and evaluation matrix.
- Provider cache policy.
- Provider-to-Market Context transform plan.
- Provider workflow quickstart.
- Canonical helper module:
  - `src/provider_market_context.py`
- Preview CLI:
  - `scripts/preview_provider_market_context.py`
- Canonical builder CLI:
  - `scripts/build_provider_market_context_canonical.py`
- Synthetic examples:
  - `docs/examples/provider_market_context_canonical_sample.csv`
  - `docs/examples/provider_market_context_normalized_records_sample.csv`
- Tests isolated from `FOOTBALL_SCOUT_MARKET_CONTEXT_CSV`.

## Safety Model

- No scraping.
- No live provider calls from the app.
- No raw provider dumps in git.
- No credentials in repo or docs.
- Real provider data stays local and ignored.
- Real canonical outputs are not versioned unless license explicitly allows it.
- Validation happens before writing or app activation.
- Diagnostics happen before app activation.

## Workflow

```text
provider decision record
  -> cache and license review
  -> normalized records
  -> canonical builder
  -> preview CLI
  -> diagnostics
  -> explicit env var activation
  -> app review
```

## Commands

Tests:

```powershell
.venv\Scripts\python.exe -m pytest -p no:cacheprovider tests -q
```

Build synthetic canonical output:

```powershell
.venv\Scripts\python.exe scripts\build_provider_market_context_canonical.py --input docs\examples\provider_market_context_normalized_records_sample.csv --output data\enrichment\provider_market_context_canonical.generated.local.csv --include-optional-fields --force
```

Preview generated output:

```powershell
.venv\Scripts\python.exe scripts\preview_provider_market_context.py --input data\enrichment\provider_market_context_canonical.generated.local.csv --show-columns
```

Diagnose synthetic canonical sample:

```powershell
.venv\Scripts\python.exe scripts\diagnose_market_context.py --market-context-csv docs\examples\provider_market_context_canonical_sample.csv
```

Clear generated local output:

```powershell
Remove-Item data\enrichment\provider_market_context_canonical.generated.local.csv -ErrorAction SilentlyContinue
```

## Verification

- Tests: `475 passed`.
- Builder sample:
  - Row count: 3
  - Column count: 18
  - Validation error count: 0
  - Written: yes
- Preview generated output:
  - Missing canonical columns: None
  - Extra columns: None
  - Validation error count: 0
- Diagnostics synthetic sample:
  - Validation errors: None
  - Duplicate market context keys: None
  - `matched_count`: 0 expected because sample is synthetic
- `git diff --check`: OK

## Limitations

- No real provider integration yet.
- No automated provider fetching.
- No app runtime provider calls.
- No market value provider selected as final.
- Synthetic examples only demonstrate the contract.
- Real provider licensing is still required before using any actual provider output.

## Upgrade Notes

- Existing app behavior is unchanged.
- Existing market context env var workflow remains opt-in.
- Provider cache data remains ignored.
- Generated `.local.csv` outputs should remain local.
- Tests now remain stable whether `FOOTBALL_SCOUT_MARKET_CONTEXT_CSV` is set or not.
