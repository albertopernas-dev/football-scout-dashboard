# Sportmonks Implementation Plan

## Status

- Candidate: Sportmonks
- Plan status: draft/docs-only
- Related readiness decision: [Sportmonks Implementation Plan Readiness Decision](../provider_decisions/sportmonks_implementation_plan_readiness_decision.md)
- Related transform design plan: [Sportmonks Transform Design Plan](sportmonks_transform_design_plan.md)
- Related payload decision record: [Sportmonks Payload Decision Record](../provider_decisions/sportmonks_payload_decision_record.md)
- Related first-code approval decision: [Sportmonks First Code Implementation Approval Decision](../provider_decisions/sportmonks_first_code_implementation_approval_decision.md)
- Related implementation summary: [Sportmonks Implementation Summary](sportmonks_implementation_summary.md)
- Provider approval: no
- First code implementation approved: yes, strict local-only future block
- Implementation created: yes, strict local-only scaffold
- Code created in this block: yes, approved scaffold only
- API calls performed in this block: no
- Raw JSON reviewed in this block: no
- `.local.csv` outputs created: no
- SQLite writes performed: no
- Streamlit activation performed: no
- Local trial performed: no

## Purpose

This document plans how a future implementation could be structured if implementation is later approved. It does not implement the transform or approve Sportmonks as a provider. It does not authorize API calls, raw payload review, a local trial, SQLite writes or Streamlit activation.

The plan converts the [transform design plan](sportmonks_transform_design_plan.md) into a future implementation checklist covering files, tests, safety controls and stop conditions.

## Scope And Non-Goals

### In Scope

- Documentation-only implementation planning.
- Future module boundaries.
- Future test strategy.
- Future ignored local input/output paths.
- No-network/default-off behavior.
- Secret handling.
- Schema and validation requirements.
- Provenance and freshness fields.
- Label-resolution decision.
- Cleanup and retention policy.
- Rollback and stop conditions.
- Acceptance criteria before future implementation.

### Out Of Scope

- Actual code.
- API calls.
- Raw JSON review.
- Provider cache reads.
- `.local.csv` creation.
- SQLite writes.
- Streamlit activation.
- Local trial.
- Provider approval.
- GitHub release/tag.

## Proposed Future Files And Modules

| Future File/Module | Purpose | Status |
|---|---|---|
| `src/providers/sportmonks/__init__.py` | Future provider namespace | proposed only |
| `src/providers/sportmonks/schema.py` | Future schema constants and expected columns | proposed only |
| `src/providers/sportmonks/transform.py` | Future pure transform from local raw/cache input to canonical draft rows | proposed only |
| `src/providers/sportmonks/validation.py` | Future validation and stop conditions | proposed only |
| `scripts/preview_sportmonks_squad_transform.py` | Future local-only preview script, default-off | proposed only |
| `tests/test_sportmonks_transform.py` | Future unit tests with synthetic fixtures only | proposed only |
| `tests/fixtures/sportmonks_squad_shape_minimal.json` | Future synthetic fixture, no real provider data | proposed only |
| `docs/provider_candidates/sportmonks_implementation_summary.md` | Future non-sensitive implementation summary if code is later approved | proposed only |

These files are proposed only. Do not create them in this block. Future synthetic fixtures must not contain real Sportmonks payloads, player names, a token, raw snippets or provider data.

## Future Data Flow

1. Load local ignored raw/cache input only when explicitly invoked.
2. Validate the expected top-level shape and `data` list.
3. Extract allowed ID-first fields:
   - `id`
   - `player_id`
   - `team_id`
   - `season_id`
   - `position_id`
   - `jersey_number`
   - `has_values`
4. Add static provenance:
   - `provider`
   - `source_endpoint`
   - `source_observed_at`
   - `source_freshness_basis`
5. Produce an in-memory preview dataframe or ignored local output only if later explicitly approved.
6. Never write SQLite in the first implementation.
7. Never activate Streamlit in the first implementation.

## Future Canonical Output Candidate

| Output Field | Source | Required? | Notes |
|---|---|---|---|
| `provider` | static `sportmonks` | yes | Static marker |
| `provider_league_id` | configured/confirmed ID | yes | Scope guard |
| `provider_season_id` | `season_id` | yes | Scope guard |
| `provider_team_id` | `team_id` | yes | Scope guard |
| `provider_player_id` | `player_id` | yes | Identity mapping |
| `provider_position_id` | `position_id` | conditional | Label unresolved |
| `squad_record_id` | `id` | conditional | Provider squad record |
| `jersey_number` | `jersey_number` | optional | Nullable |
| `has_values` | `has_values` | optional/pending | Meaning unclear |
| `source_endpoint` | endpoint pattern | yes | No token URL |
| `source_observed_at` | future execution timestamp | yes | Observation timestamp |
| `source_freshness_basis` | future chosen basis | yes | Required before implementation |

## Future Validation Requirements

| Validation | Severity | Stop? |
|---|---|---|
| Input must not be a raw committed file | error | yes |
| Provider cache path is ignored | error | yes |
| Token not present in input path/output/logs | error | yes |
| Top-level response is object-like | error | yes |
| `data` is present and list-like | error | yes |
| `data` count is small and expected for scoped review | warning/error pending | maybe |
| `provider_player_id` present | error | yes |
| `provider_team_id` matches selected scope | error | yes |
| `provider_season_id` matches selected scope | error | yes |
| Missing provenance fields | error | yes |
| Unknown extra fields | warning | no, but log non-sensitive summary |
| Duplicate player/team/season combinations | warning/error pending | maybe |
| Label fields missing | warning | no, because ID-only mode may be allowed |

## No-Network And Default-Off Behavior

- Future implementation must be local-only by default.
- No API clients.
- No `requests`, `httpx` or `aiohttp` usage in the first implementation.
- No automatic reading from provider cache in Streamlit.
- The future script must require an explicit local path argument.
- Future app integration must remain disabled until a later approval.
- Any network behavior requires a separate explicit decision.

## Secret Handling

- Future implementation must not read `SPORTMONKS_API_TOKEN`.
- The future transform must not need credentials.
- No token in CLI arguments.
- No token in logs.
- No token in docs.
- No token in output paths.
- `.env` must remain ignored.
- Any secret-related change stops the implementation.

## Ignored Local Paths

Proposed paths only:

- Input raw/cache path: `data/provider_cache/sportmonks/id_discovery/`
- Future preview output path, if later approved: `data/provider_cache/sportmonks/transform_preview/`
- Future local CSV output, only if later approved: `data/enrichment/sportmonks_squad_transform.local.csv`

These paths must be ignored before use. A `.local.csv` must not be created until explicitly approved. Raw/cache paths must never be committed.

## Label Resolution Plan

- The first implementation plan should use ID-only mode.
- Human-readable player and position labels remain unresolved.
- No label API call, include or player details endpoint is approved.
- Future labels may come from:
  - local canonical data if already permitted;
  - a later approved lookup/include review;
  - a manual mapping artifact if separately approved.
- UI/report readable labels remain out of scope for the first implementation.

## Provenance And Freshness Plan

Required future output fields:

- `provider`
- `source_endpoint`
- `source_observed_at`
- `source_freshness_basis`
- `source_scope_league_id`
- `source_scope_season_id`
- `source_scope_team_id`

`source_observed_at` should be the future transform runtime timestamp. `source_freshness_basis` should initially be `local_cache_observation_time` unless a later approved review confirms provider metadata. No record-level updated date should be claimed.

## Test Strategy

| Future Test | Purpose |
|---|---|
| `test_transform_rejects_non_object_payload` | Shape safety |
| `test_transform_requires_data_list` | Required structure |
| `test_transform_maps_required_ids` | Canonical mapping |
| `test_transform_rejects_wrong_team_scope` | Scope guard |
| `test_transform_rejects_wrong_season_scope` | Scope guard |
| `test_transform_adds_provenance_fields` | Traceability |
| `test_transform_allows_missing_labels_in_id_only_mode` | Label gap handling |
| `test_transform_does_not_require_token` | Secret safety |
| `test_preview_script_requires_explicit_input_path` | Default-off behavior |
| `test_no_real_provider_payload_in_fixtures` | Licensing/data safety |

Tests must use synthetic fixtures only. No real Sportmonks raw payloads, player names, token or network access are allowed in tests.

## Rollback And Cleanup Plan

- Future implementation must be removable by deleting the future provider namespace, script and tests.
- No SQLite migrations.
- No app wiring in the first implementation.
- No persistent tracked generated data.
- Ignored preview outputs can be deleted safely.
- Any accidentally created raw or local output must be removed before commit.
- If credentials or raw payload appear in the Git diff, stop immediately.

## Stop Conditions

- Need to read raw JSON in a docs-only block.
- Need an API call.
- Need a player detail endpoint.
- Need includes.
- Need Streamlit integration.
- Need SQLite writes.
- Need a `.local.csv`.
- Need a real provider payload in tests.
- Token appears anywhere outside `.env`.
- Provider cache appears tracked.
- `.env` appears in `git status --short`.
- Licensing uncertainty.
- Transform would imply provider approval.

## Acceptance Criteria For This Implementation Plan

- No code created.
- No proposed future file actually created except this document.
- No API calls.
- No raw JSON review.
- No provider cache modification.
- No `.local.csv`.
- No SQLite writes.
- No Streamlit activation.
- No trial.
- No provider approval.
- Future files/modules clearly marked as proposed only.
- Test strategy uses synthetic fixtures only.
- Next action clearly documented.

## Next Required Action

A later docs-only block may decide whether the [created scaffold](sportmonks_implementation_summary.md) is sufficient to approve a local preview run using an ignored local cache path.

No local preview run against real provider cache is approved. API calls, `.local.csv`, SQLite writes, Streamlit activation, a local trial and provider approval remain forbidden.
