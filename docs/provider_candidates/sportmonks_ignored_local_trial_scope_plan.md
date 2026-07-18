# Sportmonks Ignored Local Trial Scope Plan

## Status

- Candidate: Sportmonks
- Trial scope status: draft/pre-trial
- Related gate: [Sportmonks License And Terms Gate](sportmonks_license_terms_gate.md)
- Related checklist: [Sportmonks Provider Payload Checklist](sportmonks_provider_payload_checklist.md)
- Related decision record: [Sportmonks Payload Decision Record](../provider_decisions/sportmonks_payload_decision_record.md)
- Related ID discovery plan: [Sportmonks ID Discovery Plan](sportmonks_id_discovery_plan.md)
- Related credential setup: [Sportmonks Secure Credential Setup](sportmonks_secure_credential_setup.md)
- Related credential verification: [Sportmonks Local Credential Setup Verification](sportmonks_local_credential_setup_verification.md)
- Discovery summary: [Sportmonks Minimal ID Discovery Summary](sportmonks_minimal_id_discovery_summary.md)
- Confirmed ID scope review: [passed](sportmonks_confirmed_id_scope_review.md)
- Minimal payload field review decision: [executed under strict scope](../provider_decisions/sportmonks_minimal_payload_field_review_decision.md)
- Minimal payload field review summary: [passed](sportmonks_minimal_payload_field_review_summary.md)
- Transform design suitability decision: [approved for docs-only planning](../provider_decisions/sportmonks_transform_design_suitability_decision.md)
- Transform design plan: [created docs-only](sportmonks_transform_design_plan.md)
- Implementation plan readiness decision: [approved for docs-only planning](../provider_decisions/sportmonks_implementation_plan_readiness_decision.md)
- Implementation plan: [created docs-only](sportmonks_implementation_plan.md)
- First code implementation approval: [approved under strict local-only scope](../provider_decisions/sportmonks_first_code_implementation_approval_decision.md)
- Implementation summary: [first local-only scaffold created](sportmonks_implementation_summary.md)
- Local preview run approval: [approved / not executed](../provider_decisions/sportmonks_local_preview_run_approval_decision.md)
- Provider approval: no
- Production approval: no
- Credentials created locally: yes, outside Git
- Credentials stored in Git: no
- Broad payload inspection performed: no
- API calls performed: yes, 3 minimal discovery calls
- Local provider cache created: yes, ignored
- Provider cache committed: no
- Local trial performed: no
- SQLite writes performed: no
- Streamlit activation performed: no
- Parser/transform code created: no

## Purpose

This plan defines the intended boundaries for a future ignored local Sportmonks trial. It prepares the local handling model before any trial, but it does not expose credentials, inspect payloads or approve Sportmonks.

All provider data, credentials, cache and outputs must remain outside Git.

## Trial Scope

| Area | Planned Scope | Status | Notes |
|---|---|---|---|
| Selected plan | Football Free Plan confirmed by user screenshot. | confirmed | Included leagues are listed below; IDs and endpoint access are now confirmed, while payload field review remains pending. |
| Competition scope | Denmark Superliga, league_id 271. | confirmed | Confirmed in user screenshot as included in Football Free Plan. Regular league selected over play-off competitions. |
| Season scope | Denmark Superliga 2026/2027, `season_id 27897`. | confirmed | Confirmed by minimal ID discovery. |
| Team scope | FC København, `team_id 85`. | confirmed | Confirmed by minimal ID discovery. |
| Endpoint scope | Team Squad by Team and Season ID only. | reviewed minimal / passed | Existing ignored cache was sufficient; no additional API call was made. |
| Field scope | Identity/reference, team/squad, season, position, jersey and dates/freshness/provenance categories. | reviewed minimal / passed | Identity, team, season, position and jersey are present by key names; dates/freshness/provenance remain unclear. |
| Sample size | One FC København squad, one Denmark Superliga season, minimal payload. | proposed | Avoid broad pulls. |
| Raw payload path | `data/provider_cache/sportmonks/raw/` or another ignored local path. | proposed | Must remain ignored. |
| Cache path | `data/provider_cache/sportmonks/cache/` or another ignored local path. | proposed | Must remain ignored. |
| Derived output path | `data/enrichment/sportmonks_trial.local.csv` only if later explicitly allowed. | proposed | Must remain ignored; do not create now. |
| Credential path | Local `.env` or ignored local configuration only. | proposed | Never commit. |
| Cleanup | Remove local raw, cache and output artifacts after review if not needed. | draft | Must be documented before trial. |

## Confirmed Free Plan League List

| Country | League | League ID | Use In Trial |
|---|---|---:|---|
| Denmark | Superliga | 271 | selected |
| Denmark | Superliga Play-offs | 1659 | excluded for first trial |
| Scotland | Premiership | 501 | fallback only |
| Scotland | Premiership Play-Offs | 513 | excluded for first trial |

- Play-off competitions are excluded from the first trial to keep the sample stable and simple.
- Scotland Premiership is kept as fallback only.
- No season ID, team ID or endpoint response has been confirmed yet.

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

- Sportmonks subscription UI reviewed by user screenshot: Football Free Plan, 4 leagues and 3000 API calls.
- Sportmonks Team Squads documentation reviewed.
- Sportmonks Team Squad by Team and Season endpoint documentation reviewed.
- Sportmonks Players endpoint documentation reviewed.
- Sportmonks pricing and plans page reviewed only as context for paid alternatives.

These non-sensitive references confirm the plan limits and four league IDs shown in the user screenshot. They do not confirm season IDs, team IDs, endpoint access or field availability.

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

- Do not expose or commit credentials.
- Do not inspect payloads.
- Do not make additional API calls in this docs-only update.
- Do not commit provider cache.
- Do not create additional provider folders or local outputs in this docs-only update.
- Do not write to SQLite.
- Do not activate Streamlit.
- Do not create parser or transform code.
- Do not approve Sportmonks.

## Next Required Action

Minimal ID discovery, the [confirmed ID scope review](sportmonks_confirmed_id_scope_review.md) and the [minimal payload field review](sportmonks_minimal_payload_field_review_summary.md) have passed.

The [first local-only scaffold](sportmonks_implementation_summary.md) is created with synthetic tests only. The next allowed step is one approved local preview run under the [strict decision](../provider_decisions/sportmonks_local_preview_run_approval_decision.md). The local trial, any additional cache reading, manual raw JSON review, broad inspection and app integration remain blocked.
