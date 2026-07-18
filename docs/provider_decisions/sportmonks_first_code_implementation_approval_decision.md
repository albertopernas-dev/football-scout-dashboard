# Sportmonks First Code Implementation Approval Decision

## Status

- Candidate: Sportmonks
- Decision status: `approved-for-first-local-only-code-implementation`
- Related implementation plan: [Sportmonks Implementation Plan](../provider_candidates/sportmonks_implementation_plan.md)
- Related implementation-plan readiness decision: [Sportmonks Implementation Plan Readiness Decision](sportmonks_implementation_plan_readiness_decision.md)
- Related payload decision record: [Sportmonks Payload Decision Record](sportmonks_payload_decision_record.md)
- Provider approval: no
- First code implementation approved: yes, strict local-only scope
- Code implemented in this block: no
- API calls performed in this block: no
- Raw JSON reviewed in this block: no
- `.local.csv` outputs created: no
- SQLite writes performed: no
- Streamlit activation performed: no
- Local trial performed: no

## Decision

- The Sportmonks implementation plan is sufficient to approve a future first code implementation.
- The future implementation must be local-only, default-off, synthetic-test-first and no-network.
- This decision approves only the first code implementation scope defined below.
- This does not approve Sportmonks as a provider.
- This does not approve API calls, raw payload review, `.local.csv` output creation, SQLite writes, Streamlit activation, a local trial or provider approval.

## Evidence Reviewed

| Artifact | Result | Interpretation |
|---|---|---|
| Minimal ID discovery | passed | IDs and endpoint access confirmed |
| Minimal payload field review | passed | Shape reviewed from ignored cache with 0 API calls |
| Transform design plan | created docs-only | Candidate mapping, validation and gaps documented |
| Implementation plan | created docs-only | Future modules, tests and safety controls documented |

## Approved Future Code Scope

The future implementation, in a separate block, may create only:

| Future File/Module | Approval | Constraint |
|---|---|---|
| `src/providers/sportmonks/__init__.py` | approved | namespace only |
| `src/providers/sportmonks/schema.py` | approved | constants/schema only, no network |
| `src/providers/sportmonks/validation.py` | approved | pure validation only |
| `src/providers/sportmonks/transform.py` | approved | pure transform only |
| `scripts/preview_sportmonks_squad_transform.py` | approved | explicit local path, default-off, no network |
| `tests/test_sportmonks_transform.py` | approved | synthetic fixtures only |
| `tests/fixtures/sportmonks_squad_shape_minimal.json` | approved | synthetic fixture only, no real provider data |
| `docs/provider_candidates/sportmonks_implementation_summary.md` | approved | non-sensitive implementation summary |

These are the only files approved for the first implementation block. Any additional file requires a separate decision.

The future code must not read `.env` or use `SPORTMONKS_API_TOKEN`. It must not import or use `requests`, `httpx`, `aiohttp`, provider SDKs or network clients.

## Required Future Implementation Behavior

- Local-only.
- Default-off.
- No automatic execution.
- No Streamlit wiring.
- No SQLite writes.
- No app integration.
- No API client.
- No token handling.
- No provider cache access unless an explicit local path is passed to the preview script.
- Pure transform functions must accept already-loaded data structures or an explicit local input path in the script only.
- Synthetic tests must not require real provider data.
- The preview script must fail closed if the path is missing, not ignored or unsafe.
- The preview script must produce stdout/non-sensitive preview only unless a future ignored output path is explicitly approved.

## Required Future Test Scope

The approved future tests are:

- `test_transform_rejects_non_object_payload`
- `test_transform_requires_data_list`
- `test_transform_maps_required_ids`
- `test_transform_rejects_wrong_team_scope`
- `test_transform_rejects_wrong_season_scope`
- `test_transform_adds_provenance_fields`
- `test_transform_allows_missing_labels_in_id_only_mode`
- `test_transform_does_not_require_token`
- `test_preview_script_requires_explicit_input_path`
- `test_no_real_provider_payload_in_fixtures`

Tests must use synthetic fixtures only. No real Sportmonks payload, player names, token, network access or provider cache is allowed or required for tests.

## Future Code Acceptance Criteria

The future implementation is acceptable only if:

- All new tests pass.
- The existing full pytest suite passes.
- `python -m compileall src scripts tests` passes, or the project's standard compile check passes.
- `git diff --check` passes.
- `git status --short` shows only expected tracked files.
- `.env` remains ignored.
- `data/provider_cache/` remains ignored.
- No raw JSON is tracked.
- No `.local.csv` is created.
- No SQLite file is modified.
- No Streamlit file is modified.
- No network library or API client is added.
- No provider approval is implied.

## Explicitly Still Forbidden

- API calls.
- Raw JSON review in a docs or code block.
- Reading real provider cache during tests.
- Committing real provider payloads.
- Committing a token or `.env`.
- Creating `.local.csv`.
- Writing SQLite.
- Streamlit integration.
- Local trial.
- Broad payload inspection.
- Player-detail endpoint.
- Includes/label endpoint.
- Provider approval.
- GitHub release/tag.

## Stop Conditions For Future Code Block

- Any need for API calls.
- Any need to read raw JSON to design tests.
- Any real provider payload appears in tests or fixtures.
- Any token appears outside `.env`.
- `.env` appears in `git status --short`.
- Provider cache appears tracked.
- SQLite file changes.
- Streamlit file changes.
- Code needs labels from an API.
- Code needs a player-detail endpoint.
- Code requires non-local execution.
- Code implies Sportmonks is approved.
- Licensing or exposure uncertainty appears.

## Next Required Action

A later implementation block may create only the approved local-only code, synthetic fixture, tests, preview script and implementation summary.

That future block must not make API calls, read raw provider JSON for test fixtures, write SQLite, activate Streamlit, create `.local.csv`, perform a trial or approve Sportmonks.

The future block must provide full diffs and test results before commit.
