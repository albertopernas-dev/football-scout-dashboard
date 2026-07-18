# Sportmonks Local Preview Run Approval Decision

## Status

- Candidate: Sportmonks
- Decision status: `approved-for-one-local-preview-run`
- Related implementation summary: [Sportmonks Implementation Summary](../provider_candidates/sportmonks_implementation_summary.md)
- Related first-code approval decision: [Sportmonks First Code Implementation Approval Decision](sportmonks_first_code_implementation_approval_decision.md)
- Related payload decision record: [Sportmonks Payload Decision Record](sportmonks_payload_decision_record.md)
- Provider approval: no
- Local preview run approved: yes, strict one-run local-only scope
- Preview executed in this block: no
- API calls performed in this block: no
- Raw JSON manually reviewed in this block: no
- Provider cache modified in this block: no
- `.local.csv` outputs created: no
- SQLite writes performed: no
- Streamlit activation performed: no
- Local trial performed: no

## Decision

- The created local-only scaffold is sufficient to approve one future local preview run against an existing ignored local cache file.
- The future preview must use only the default-off script: `scripts/preview_sportmonks_squad_transform.py`.
- The preview may read exactly one explicitly supplied local JSON file under the ignored Sportmonks provider cache.
- The preview may print only the script's non-sensitive aggregate summary.
- This does not approve manual raw JSON inspection.
- This does not approve API calls.
- This does not approve `.local.csv` output creation.
- This does not approve SQLite writes.
- This does not approve Streamlit activation.
- This does not approve a local trial.
- This does not approve Sportmonks as a provider.

## Approved Future Preview Scope

| Item | Approved Scope |
|---|---|
| Script | `scripts/preview_sportmonks_squad_transform.py` |
| Input | one explicit local JSON path under `data/provider_cache/sportmonks/` |
| Path requirement | must be ignored by Git before use |
| Arguments | `--input`, `--league-id`, `--team-id`, `--season-id`, optional `--observed-at` |
| League ID | `271` |
| Team ID | `85` |
| Season ID | `27897` |
| Output | stdout aggregate summary only |
| Writes | none |
| Network | none |
| App integration | none |
| SQLite | none |
| `.local.csv` | none |

## Required Future Pre-Run Checks

The future preview block must run these checks before the preview:

- `git status --short`
- `git check-ignore -v .env`
- `git check-ignore -v <LOCAL_PREVIEW_INPUT_PATH>`
- `git status --ignored --short data/provider_cache/sportmonks`

It must confirm:

- `.env` remains ignored.
- The input path is under `data/provider_cache/sportmonks/`.
- The input path is ignored by Git.
- The input file does not appear in `git status --short`.
- SQLite has no changes.
- Streamlit has no changes.
- No `.local.csv` exists.

## Required Future Preview Command

The approved command template is documentation only and is not executed in this block:

```powershell
python scripts/preview_sportmonks_squad_transform.py `
  --input <LOCAL_PREVIEW_INPUT_PATH> `
  --league-id 271 `
  --team-id 85 `
  --season-id 27897
```

`<LOCAL_PREVIEW_INPUT_PATH>` must be the existing ignored cached file. Do not open or paste the raw file content. Do not use `cat`, `type`, `Get-Content` or an editor to inspect the JSON. Only the script may read it during the approved future preview.

## Required Future Post-Run Checks

After the future preview, run:

- `git status --short`
- `git status --ignored --short data/provider_cache/sportmonks`
- `git diff --check`
- `git check-ignore -v .env`
- Confirm no `.local.csv` was created.
- Confirm `data/football_scout.db` did not change.
- Confirm `app.py` did not change.

## Allowed Future Preview Output

Only these values may be reported:

- `row_count`
- `columns`
- `provider`
- `source_endpoint`
- `has_position_ids`
- `has_jersey_numbers`
- exit code
- a safe error message if the preview fails

Do not report:

- player IDs
- player names
- raw rows
- raw JSON snippets
- token
- file contents
- full provider payload
- cache filename if it contains sensitive information

## Still Forbidden

- API calls.
- Manual raw JSON review.
- Broad payload inspection.
- Reading more than the one approved local cache input.
- Pasting raw JSON into docs or chat.
- Creating `.local.csv`.
- Writing SQLite.
- Streamlit integration.
- Local trial.
- Player-detail endpoint.
- Includes/label endpoint.
- Provider approval.
- GitHub release/tag.

## Stop Conditions For Future Preview Block

- Input path is not ignored by Git.
- Input path is outside `data/provider_cache/sportmonks/`.
- Preview requires API calls.
- Preview requires manual raw JSON inspection.
- Script prints player IDs, player names, raw rows or raw JSON.
- Script writes an output file.
- `.local.csv` appears.
- SQLite file changes.
- `app.py` changes.
- Provider cache appears tracked.
- `.env` appears in `git status --short`.
- Token appears outside `.env`.
- Any licensing or exposure uncertainty appears.

## Next Required Action

A later preview block may run exactly one local preview under this approval.

That future block must provide the exact command, stdout/stderr summary, exit code and post-run checks.

The future preview still does not approve API calls, broad inspection, `.local.csv`, SQLite, Streamlit, local trial or provider approval.
