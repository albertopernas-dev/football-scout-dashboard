# v0.5.0 - Provider Fixture Prototype

## Summary

v0.5.0 demonstrates a fully offline, synthetic workflow that transforms provider fixture records into canonical Market Context through a reviewed identity mapping.

This release does not integrate a real provider, scrape any source, make network calls or connect provider data to the app. It does not change scoring or Opportunity Finder. The prototype uses versioned synthetic samples and generated local artifacts that remain ignored by git.

## Highlights

- Provider Fixture Prototype plan:
  - `docs/v0_5_0_provider_fixture_prototype_plan.md`
- Provider Identity Mapping Plan:
  - `docs/provider_identity_mapping_plan.md`
- Synthetic identity mapping sample:
  - `docs/examples/provider_identity_mapping_sample.csv`
- Synthetic provider fixture records sample:
  - `docs/examples/provider_fixture_records_sample.csv`
- Provider identity mapping validator:
  - `src/provider_identity_mapping.py`
- Mapping application helper:
  - `apply_provider_identity_mapping_to_records(...)`
- Offline mapped records CLI:
  - `scripts/apply_provider_identity_mapping.py`
- Offline end-to-end demo:
  - `scripts/run_provider_fixture_prototype_demo.py`
- Canonical builder integration:
  - `scripts/build_provider_market_context_canonical.py`
- Preview compatibility:
  - `scripts/preview_provider_market_context.py`

## Workflow

```text
provider fixture records
  + reviewed identity mapping
  -> mapped provider records
  -> canonical Market Context
  -> preview validation
  -> diagnostics and app activation later
```

## Identity Mapping Rules

- Records are joined exactly by `provider_name`, `provider_player_id`, `provider_team_id`, `provider_league_id` and `provider_season`.
- Only mappings with `match_status == matched` are applied.
- `unmatched`, `ambiguous` and `rejected` mappings are excluded.
- No fuzzy matching or name-only matching is used.
- Identity mapping confidence remains separate from Market Context confidence.
- Duplicate matched provider identities are rejected.

## Commands

Run the full test suite:

```powershell
.venv\Scripts\python.exe -m pytest -p no:cacheprovider tests -q
```

Run the synthetic end-to-end demo:

```powershell
.venv\Scripts\python.exe scripts\run_provider_fixture_prototype_demo.py --records docs\examples\provider_fixture_records_sample.csv --mapping docs\examples\provider_identity_mapping_sample.csv --mapped-output data\enrichment\provider_fixture_records_mapped.generated.local.csv --canonical-output data\enrichment\provider_market_context_from_fixture_demo.generated.local.csv --include-optional-fields --force
```

Preview the canonical output:

```powershell
.venv\Scripts\python.exe scripts\preview_provider_market_context.py --input data\enrichment\provider_market_context_from_fixture_demo.generated.local.csv --show-columns
```

Clear generated local outputs:

```powershell
Remove-Item data\enrichment\provider_fixture_records_mapped.generated.local.csv -ErrorAction SilentlyContinue
Remove-Item data\enrichment\provider_market_context_from_fixture_demo.generated.local.csv -ErrorAction SilentlyContinue
```

## Verification

- Tests: `515 passed`.
- End-to-end demo:
  - Input record count: 5
  - Mapped record count: 2
  - Excluded record count: 3
  - Canonical row count: 2
  - Canonical column count: 18
  - Canonical validation error count: 0
  - Written mapped: yes
  - Written canonical: yes
- Canonical preview:
  - Row count: 2
  - Column count: 18
  - Missing canonical columns: None
  - Extra columns: None
  - Validation error count: 0
  - Players: Player Alpha, Player Beta
- `git diff --check`: OK.

## Safety Model

- No real provider data is versioned.
- No raw provider dumps are stored in git.
- No credentials are stored in the repository or documentation.
- Generated `.local.csv` outputs remain local and ignored.
- The app makes no live provider calls.
- No scraping is used.
- Synthetic coverage does not change scoring.

## Limitations

- The prototype uses synthetic samples only.
- No real provider is selected or integrated.
- There is no provider payload fetcher.
- There is no provider-to-local mapping for a real dataset.
- There are no app UI changes.
- The demo does not run diagnostics automatically; preview and diagnostics remain separate inspection steps.

## Upgrade Notes

- Existing app behavior is unchanged.
- The v0.4.0 provider evaluation workflow remains valid.
- v0.5.0 adds an offline fixture prototype before canonical Market Context.
- Any real provider work still requires a license and terms review, with outputs kept local and ignored unless redistribution is explicitly permitted.
