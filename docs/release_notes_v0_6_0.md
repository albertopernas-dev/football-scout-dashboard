# v0.6.0 - Licensed Provider Payload Evaluation

## Summary

v0.6.0 prepares the project to evaluate permitted or licensed provider payloads before any real integration is implemented. It adds a fully synthetic workflow for examining payload shape, flattening nested records, applying reviewed identity mappings and producing validated canonical Market Context.

Real provider data, live integrations and app activation remain deliberately separate from this release.

## What Changed

### Payload Evaluation Governance

- Added a provider payload evaluation checklist.
- Added a payload-specific decision record template and a completed synthetic example.
- Documented payload shape, licensing, caching, redistribution and credential criteria.
- Kept license and terms review as a prerequisite for any real payload experiment.

### Advanced Synthetic Payload Shape

- Added an advanced synthetic JSON payload and a compatible reviewed synthetic identity mapping.
- Modelled nested provider, competition, team, player, identity, market, contract and provenance sections.
- Used fictional entities and `example.test` references only; the sample does not represent a real provider.

### Synthetic Flattening Helper

`src/provider_payload_shapes.py` loads local JSON and flattens provider, competition, teams and players into normalized records. It preserves missing values and populates `market_value_eur` only when the payload currency is EUR. It performs no identity mapping, app activation or network access.

### Local Synthetic CLI

`scripts/flatten_provider_payload_advanced_sample.py` writes normalized synthetic provider records to an ignored `.local.csv` inside `data/enrichment/`. It reads no `.env` configuration and performs no network calls.

### Advanced Synthetic End-to-End Demo

`scripts/run_advanced_provider_payload_demo.py` runs this offline pipeline:

```text
advanced synthetic JSON
  -> flattened normalized records
  -> reviewed synthetic identity mapping
  -> validated canonical Market Context CSV
```

The demo validates inputs and canonical output before writing, prevents partial outputs when preflight fails, and restricts every generated artifact to ignored `.local.csv` paths under `data/enrichment/`.

### Tests

- Latest known full-suite verification: `545 passed`.

## Example Commands

Validate the synthetic JSON:

```powershell
.venv\Scripts\python.exe -m json.tool docs\examples\provider_payload_advanced_sample.json > $null
```

Flatten the payload locally:

```powershell
.venv\Scripts\python.exe scripts\flatten_provider_payload_advanced_sample.py --input docs\examples\provider_payload_advanced_sample.json --output data\enrichment\provider_payload_advanced_flattened.generated.local.csv --force
```

Run the end-to-end synthetic demo:

```powershell
.venv\Scripts\python.exe scripts\run_advanced_provider_payload_demo.py --input docs\examples\provider_payload_advanced_sample.json --mapping docs\examples\provider_advanced_identity_mapping_sample.csv --flattened-output data\enrichment\provider_payload_advanced_flattened.generated.local.csv --mapped-output data\enrichment\provider_payload_advanced_mapped.generated.local.csv --canonical-output data\enrichment\provider_market_context_from_advanced_payload.generated.local.csv --include-optional-fields --force
```

Preview the canonical output:

```powershell
.venv\Scripts\python.exe scripts\preview_provider_market_context.py --input data\enrichment\provider_market_context_from_advanced_payload.generated.local.csv --show-columns
```

Remove generated local artifacts:

```powershell
Remove-Item data\enrichment\provider_payload_advanced_flattened.generated.local.csv -ErrorAction SilentlyContinue
Remove-Item data\enrichment\provider_payload_advanced_mapped.generated.local.csv -ErrorAction SilentlyContinue
Remove-Item data\enrichment\provider_market_context_from_advanced_payload.generated.local.csv -ErrorAction SilentlyContinue
```

## What This Release Does Not Do

- Does not integrate a real provider.
- Does not evaluate or approve a real provider payload.
- Does not scrape or make live provider calls.
- Does not activate provider data in Streamlit.
- Does not write provider data to SQLite.
- Does not version real payloads or generated `.local.csv` outputs.
- Does not change scoring or Opportunity Finder logic.

## Safety Notes

- Real provider payloads must remain local and ignored unless their license explicitly permits redistribution.
- Credentials and API keys must never enter the repository or documentation.
- Raw dumps must not enter git without explicit permission.
- Every real candidate must complete the payload checklist and a decision record before transformation work begins.

## Verification

Expected final pre-tag verification:

- `json.tool`: OK for `docs/examples/provider_payload_advanced_sample.json`.
- Pytest: `545 passed`.
- `git diff --check`: OK.

Tagging should occur only after these checks are rerun successfully on the final release commit.

## Next Steps

- Use the checklist and decision record template for an actual permitted provider candidate.
- Review license and terms before inspecting or transforming any real payload.
- Keep permitted local experiments in `data/provider_cache/` or ignored `.local.csv` paths.
- Consider provider-specific transform helpers only after the candidate is approved.
