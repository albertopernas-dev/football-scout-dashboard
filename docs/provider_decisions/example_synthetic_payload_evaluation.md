# Example Synthetic Payload Evaluation

This is a synthetic example. It does not evaluate a real provider, use real payloads or grant permission to use any real provider data. It only demonstrates how to complete the payload evaluation template.

## Status

- Status: Accepted as synthetic example
- Date: 2026-07-15
- Reviewer: Synthetic reviewer
- Provider candidate: Synthetic Provider
- Payload reviewed: `docs/examples/provider_fixture_records_sample.csv`
- Related decision record: none, synthetic example only
- Related checklist: `docs/provider_payload_evaluation_checklist.md`

## Summary

This synthetic payload demonstrates the offline provider fixture records -> reviewed identity mapping -> canonical Market Context workflow. It contains no real players, teams, provider data or provider authorization and cannot be used as evidence for a real provider decision.

## Payload Source

- Provider/source name: Synthetic Provider
- Endpoint/report/file/source: `docs/examples/provider_fixture_records_sample.csv`
- Retrieval method: versioned synthetic fixture
- Sample type: synthetic
- Sample location: `docs/examples/provider_fixture_records_sample.csv`
- Can sample be versioned?: yes, because it is synthetic
- Can derived outputs be versioned?: no need; generated outputs stay local as `.local.csv`
- Notes: generated for contract testing and documentation only

## License And Terms Review

- Terms reviewed: not applicable, synthetic data
- License permits local development use: yes, project-owned synthetic example
- License permits caching: yes, synthetic example
- License permits derived outputs: yes for local generated outputs, but outputs should stay ignored
- Redistribution permitted: yes for the synthetic sample in the repository
- Screenshot/demo restrictions: none for the synthetic sample
- Credential handling: no credentials involved
- Raw dumps allowed in git?: synthetic sample only
- Reviewer notes: this record is not reusable as approval for real provider payloads

## Payload Shape

| Field | Available | Notes |
|---|---|---|
| `provider_player_id` | yes | Synthetic stable IDs are present. |
| `provider_team_id` | yes | Synthetic stable IDs are present. |
| `provider_league_id` | yes | A synthetic league ID is present. |
| `provider_season` | yes | Season 2024 is present. |
| `provider_player_name` | yes | Synthetic provider-facing names are present. |
| `provider_team_name` | yes | Synthetic provider-facing names are present. |
| age or birthdate | partial | Age is populated for some records; birthdate is absent. |
| market value | partial | One synthetic record contains `market_value_eur`. |
| market value currency | no | EUR is implied only by the synthetic canonical field name. |
| market value date | no | No value date is present. |
| contract end date | partial | One synthetic record contains a contract end date. |
| `source` / `source_url` | partial | Populated only on enriched synthetic rows. |
| `fetched_at` / `value_date` | no | Neither field is present. |
| confidence / provenance | partial | Market Context confidence is present only on enriched rows. |

## Identity Mapping Fit

- Strong provider IDs available?: yes
- Season-aware mapping possible?: yes
- Transfers/team changes handled?: not applicable in the synthetic sample
- Duplicate IDs risk: low in the sample
- Name-only/fuzzy matching required?: no
- Mapping storage plan: `docs/examples/provider_identity_mapping_sample.csv`
- Mapping review process: synthetic reviewed mapping with `match_status` and identity mapping confidence

## Market Context Fit

- Can produce canonical `age`: partial
- Can produce canonical `market_value_eur`: partial
- Can produce canonical `contract_end_date`: partial
- Can produce `source`, `source_url`, `confidence`, `notes`: partial
- Missing values distinguishable from zero: yes, empty fields represent missing values
- Salary/cost fields confused with market value?: no
- Currency conversion needed?: no
- Value date available?: no

## Cache And Storage Plan

- Raw payload storage: versioned synthetic CSV under `docs/examples/`
- Canonical output storage: generated `.local.csv` under `data/enrichment/`
- `.local.csv` or ignored path: yes
- Refresh policy: manual synthetic update only
- Retention policy: generated outputs removed after the demo
- Deletion process: remove generated `.local.csv` outputs with the cleanup commands below
- Git safety check: only synthetic input samples are versioned

## Transform Experiment Plan

- Transform experiment allowed?: yes, synthetic only
- Input path: `docs/examples/provider_fixture_records_sample.csv`
- Mapping path: `docs/examples/provider_identity_mapping_sample.csv`
- Expected canonical output path: `data/enrichment/provider_market_context_from_fixture_demo.generated.local.csv`
- No network/app runtime calls confirmation: yes

Run the synthetic demo:

```powershell
.venv\Scripts\python.exe scripts\run_provider_fixture_prototype_demo.py --records docs\examples\provider_fixture_records_sample.csv --mapping docs\examples\provider_identity_mapping_sample.csv --mapped-output data\enrichment\provider_fixture_records_mapped.generated.local.csv --canonical-output data\enrichment\provider_market_context_from_fixture_demo.generated.local.csv --include-optional-fields --force
```

Preview the canonical output:

```powershell
.venv\Scripts\python.exe scripts\preview_provider_market_context.py --input data\enrichment\provider_market_context_from_fixture_demo.generated.local.csv --show-columns
```

Run diagnostics:

```powershell
.venv\Scripts\python.exe scripts\diagnose_market_context.py --market-context-csv data\enrichment\provider_market_context_from_fixture_demo.generated.local.csv
```

Clean up generated outputs:

```powershell
Remove-Item data\enrichment\provider_fixture_records_mapped.generated.local.csv -ErrorAction SilentlyContinue
Remove-Item data\enrichment\provider_market_context_from_fixture_demo.generated.local.csv -ErrorAction SilentlyContinue
```

## Diagnostics Expectations

- Expected `matched_count`: 0 against the real LaLiga dataset because the sample identities are synthetic; the synthetic identity mapping demo itself maps 2 records.
- Expected unmatched review: synthetic `unmatched`, `ambiguous` and `rejected` records are excluded.
- Expected effective coverage: 0 against the real dataset.
- Expected validation errors: 0 for the generated canonical CSV.
- Duplicate key expectation: 0.
- App activation allowed?: no, synthetic demo only.

## Decision

- Decision: accept
- Rationale: accepted only as a synthetic contract and demo example
- Blocking issues: not usable for real provider evaluation
- Follow-up actions: review terms and license before any real provider payload review; keep real payloads local and ignored; complete the checklist before a transform experiment
- Advanced synthetic shape notes: [`docs/provider_payload_shape_notes.md`](../provider_payload_shape_notes.md)
- Re-review trigger: introduction of a real provider candidate or permitted payload

## Safety Notes

- No scraping.
- No live provider calls from the app.
- No real provider data.
- No credentials.
- No raw provider dumps.
- Generated outputs remain local and ignored.
- No scoring changes.
