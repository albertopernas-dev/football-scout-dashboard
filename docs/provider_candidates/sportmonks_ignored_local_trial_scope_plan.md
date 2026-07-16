# Sportmonks Ignored Local Trial Scope Plan

## Status

- Candidate: Sportmonks
- Trial scope status: draft/pre-credential
- Related gate: [Sportmonks License And Terms Gate](sportmonks_license_terms_gate.md)
- Related checklist: [Sportmonks Provider Payload Checklist](sportmonks_provider_payload_checklist.md)
- Related decision record: [Sportmonks Payload Decision Record](../provider_decisions/sportmonks_payload_decision_record.md)
- Provider approval: no
- Production approval: no
- Credentials created: no
- Payload inspection performed: no
- API calls performed: no
- Provider cache created: no
- Local trial performed: no
- SQLite writes performed: no
- Streamlit activation performed: no
- Parser/transform code created: no

## Purpose

This plan defines the intended boundaries for a future ignored local Sportmonks trial. It prepares the local handling model before any trial, but it does not create credentials, inspect payloads or approve Sportmonks.

All provider data, credentials, cache and outputs must remain outside Git.

## Trial Scope

| Area | Planned Scope | Status | Notes |
|---|---|---|---|
| Selected plan | Free trial or Starter plan, pending user/account confirmation. | proposed/pending confirmation | Must be selected before credentials. |
| Competition scope | LaLiga, pending account/coverage confirmation. | proposed/pending confirmation | Keep to one minimal competition if possible. |
| Season scope | One selected season, pending account/docs confirmation. | proposed/pending confirmation | Keep minimal. |
| Endpoint scope | Primary candidate: Team Squad by Team and Season ID. Auxiliary candidate: Players endpoint only if needed for schema/include validation. | proposed/pending docs/account confirmation | No endpoint is approved yet. |
| Field scope | Identity, team/squad context, season/date metadata, position, provenance/freshness, and Market Context candidates if available. | draft | Availability must be verified. |
| Sample size | One team, one season, minimal payload. | proposed | Avoid broad pulls. |
| Raw payload path | `data/provider_cache/sportmonks/raw/` or another ignored local path. | proposed | Must remain ignored. |
| Cache path | `data/provider_cache/sportmonks/cache/` or another ignored local path. | proposed | Must remain ignored. |
| Derived output path | `data/enrichment/sportmonks_trial.local.csv` only if later explicitly allowed. | proposed | Must remain ignored; do not create now. |
| Credential path | Local `.env` or ignored local configuration only. | proposed | Never commit. |
| Cleanup | Remove local raw, cache and output artifacts after review if not needed. | draft | Must be documented before trial. |

## Proposed Local Paths

These paths are proposed only. Do not create them in this block, and do not commit anything inside them:

- `data/provider_cache/sportmonks/raw/`
- `data/provider_cache/sportmonks/cache/`
- `data/enrichment/sportmonks_trial.local.csv`
- `.env` or an ignored local environment or configuration file for the API key

These paths must be confirmed as ignored before use. `git status --short` must remain clean before and after any future trial.

## Field Categories To Evaluate

| Category | Why It Matters | Status |
|---|---|---|
| Provider player ID | Identity matching. | to verify |
| Player name | Identity matching and manual review. | to verify |
| Team/squad relationship | Club context and disambiguation. | to verify |
| Competition/season | Scope and provenance. | to verify |
| Position/role | Filtering and similarity support. | to verify |
| Birth date/age | Market Context enrichment if available. | to verify |
| Contract/date fields | Market Context enrichment if available. | to verify |
| Market value fields | Market Context enrichment if available. | to verify |
| Update timestamps | Freshness and provenance. | to verify |

## External Documentation References

- Sportmonks plans and pricing page reviewed.
- Sportmonks Players endpoint documentation reviewed.
- Sportmonks team squads documentation reviewed.
- Sportmonks Team Squad by Team and Season endpoint documentation reviewed.

These are non-sensitive reference summaries only. They do not confirm account coverage, plan availability, endpoint access or field availability.

## Required Before Credential Creation

- Selected plan documented.
- Competition and season scope documented.
- Credential storage path confirmed ignored.
- `.env` or local configuration confirmed not tracked.
- User explicitly confirms creation of credentials outside Git.
- `git status --short` clean.
- No credentials in tracked files, docs or diffs.

## Required Before API Call Or Payload Inspection

- Checklist completed enough for trial.
- Decision record completed enough for trial.
- This trial scope plan reviewed.
- Endpoint scope documented.
- Minimal sample size documented.
- Ignored raw and cache paths confirmed.
- Cleanup process documented.
- Stop conditions reviewed.
- No SQLite, Streamlit or parser work planned.
- User explicitly confirms proceeding to the local ignored trial.

## Cleanup Plan

- Keep raw payloads only in ignored local paths.
- Delete raw payloads if the trial is rejected, stopped or no longer needed.
- Keep only non-sensitive summaries in Git.
- Do not copy raw JSON into docs, examples or tests.
- Do not commit derived `.local.csv` outputs.
- Verify `git status --short` before and after cleanup.

## Stop Conditions

- Credentials appear in Git.
- A raw payload appears in Git.
- Provider cache appears in Git.
- A `.local.csv` provider output appears in Git.
- Endpoint scope is broader than needed.
- Plan or competition scope does not support the intended fields.
- Raw data would be exposed in documentation or a demo.
- The trial requires SQLite writes, Streamlit activation or transform code.
- Terms of Service or subscription conditions become unclear.

## Still Forbidden In This Block

- Do not create credentials.
- Do not inspect payloads.
- Do not call APIs.
- Do not create provider cache.
- Do not create provider folders or local outputs.
- Do not write to SQLite.
- Do not activate Streamlit.
- Do not create parser or transform code.
- Do not approve Sportmonks.

## Next Required Action

The user must choose or confirm:

- the Sportmonks plan;
- competition and season scope; and
- endpoint scope after documentation and plan review.

Only after that confirmation may a separate explicit block prepare secure local credential setup. No credentials or payload inspection occur in this block.
