# Sportmonks Local Preview Run Summary

## Status

- Candidate: Sportmonks
- Preview status: `completed`
- Related local preview approval decision: [Sportmonks Local Preview Run Approval Decision](../provider_decisions/sportmonks_local_preview_run_approval_decision.md)
- Related implementation summary: [Sportmonks Implementation Summary](sportmonks_implementation_summary.md)
- Provider approval: no
- Preview executed: yes
- Preview count: one approved local preview run
- API calls performed: no
- Manual raw JSON review performed: no
- Raw JSON included in docs: no
- Provider cache modified: no
- `.local.csv` outputs created: no
- SQLite writes performed: no
- Streamlit activation performed: no
- Local trial performed: no

## Approved Input Scope

| Item | Value |
|---|---|
| Input path | `data/provider_cache/sportmonks/id_discovery/04_squad_season_27897_team_85.json` |
| Input status | ignored local cache |
| League ID | `271` |
| Team ID | `85` |
| Season ID | `27897` |
| Script | `scripts/preview_sportmonks_squad_transform.py` |
| Output type | aggregate stdout summary only |

The input path is recorded because it contains only endpoint/scope IDs and no player-identifying values.

No raw JSON content, player IDs, raw rows or player names are included.

## Runtime Note

- `python` and `.venv\Scripts\python.exe` could not start a process in this local environment.
- Those failed attempts did not read the input file.
- The effective preview was run using Codex local Python.
- The runtime substitution did not change the approved script, input, arguments or output scope.

## Preview Command

```powershell
<Codex bundled Python> scripts/preview_sportmonks_squad_transform.py `
  --input <ignored cache JSON> `
  --league-id 271 `
  --team-id 85 `
  --season-id 27897
```

This command does not open or manually inspect raw JSON.

## Preview Result

| Field | Value |
|---|---|
| Exit code | `0` |
| Stderr | `none` |
| `row_count` | `6` |
| `provider` | `sportmonks` |
| `source_endpoint` | `/football/squads/seasons/27897/teams/85` |
| `has_position_ids` | `0` |
| `has_jersey_numbers` | `0` |

Columns:

```text
provider
provider_league_id
provider_season_id
provider_team_id
provider_player_id
provider_position_id
squad_record_id
jersey_number
has_values
source_endpoint
source_observed_at
source_freshness_basis
source_scope_league_id
source_scope_season_id
source_scope_team_id
```

No player IDs, raw rows or player names are included.

## Interpretation

The local-only scaffold executed successfully against the approved ignored cache input.

The result confirms the transform can produce canonical rows from the scoped cache input.

`row_count = 6` matches the previously recorded minimal review count.

`has_position_ids = 0` and `has_jersey_numbers = 0` indicate those fields were not populated in the transformed rows for this preview input.

This reinforces that labels, position labels, jersey coverage and richer Market Context remain unresolved.

This does not make Sportmonks a provider-approved source.

This does not approve app integration, SQLite loading, local trial or `.local.csv` generation.

## Checks Summary

- Git clean before and after: yes.
- `.env` ignored: yes.
- Provider cache ignored: yes.
- `.local.csv` baseline: 2 before / 2 after.
- Existing `.local.csv` files remained ignored: yes.
- JSON metadata unchanged: yes.
- `app.py` unchanged: yes.
- `data/football_scout.db` unchanged: yes.
- `git diff --check`: passed.
- API calls: no.
- Manual raw JSON review: no.
- Commit performed: no.

## Still Forbidden

- API calls.
- Manual raw JSON review.
- Additional cache inputs.
- Broad payload inspection.
- `.local.csv` creation.
- SQLite writes.
- Streamlit integration.
- Local trial.
- Provider approval.
- GitHub release/tag.

## Next Required Action

A later docs-only block may decide whether the completed preview is sufficient to approve a non-sensitive preview result decision or close the v0.8.0 milestone.

No further preview, additional cache reading, `.local.csv`, SQLite, Streamlit, local trial or provider approval is approved by this summary.
