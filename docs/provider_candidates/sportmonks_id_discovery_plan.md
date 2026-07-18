# Sportmonks ID Discovery Plan

## Status

- Candidate: Sportmonks
- ID discovery status: passed
- Related trial scope plan: [Sportmonks Ignored Local Trial Scope Plan](sportmonks_ignored_local_trial_scope_plan.md)
- Related checklist: [Sportmonks Provider Payload Checklist](sportmonks_provider_payload_checklist.md)
- Related decision record: [Sportmonks Payload Decision Record](../provider_decisions/sportmonks_payload_decision_record.md)
- Related credential setup: [Sportmonks Secure Credential Setup](sportmonks_secure_credential_setup.md)
- Related credential verification: [Sportmonks Local Credential Setup Verification](sportmonks_local_credential_setup_verification.md)
- Discovery summary: [Sportmonks Minimal ID Discovery Summary](sportmonks_minimal_id_discovery_summary.md)
- Confirmed ID scope review: [passed](sportmonks_confirmed_id_scope_review.md)
- Provider approval: no
- Credentials created locally: yes, outside Git
- Credentials stored in Git: no
- API calls performed: yes, 3 minimal discovery calls
- Broad payload inspection performed: no
- Local provider cache created: yes, ignored
- Provider cache committed: no
- Local trial performed: no
- Season ID confirmed: yes, `27897`
- Team ID confirmed: yes, `85`
- Endpoint access confirmed: yes, HTTP 200

## Purpose

The user could not find the Denmark Superliga `season_id` or FC Copenhagen `team_id` in the Sportmonks UI. This plan defined the minimal discovery path used to confirm those IDs and endpoint access without inventing values.

It does not expose credentials or authorize broad payload inspection. All raw API responses and credentials remain outside Git.

## Manual UI Lookup Result

| Item | Target | Result | Status |
|---|---|---|---|
| League list | Free Plan leagues | Found in UI screenshot. | confirmed |
| Selected league | Denmark Superliga, league_id 271 | Found in UI screenshot. | confirmed |
| Season ID | Denmark Superliga 2026/2027 | `27897` | confirmed |
| Team ID | FC København | `85` | confirmed |
| Endpoint access | Team Squad by Team and Season ID | HTTP 200; data present | confirmed |

## Proposed Minimal ID Discovery Sequence

1. Confirm the API key can be stored securely in ignored local environment or configuration only.
2. Use the smallest possible metadata request to confirm the Denmark Superliga current or latest season ID.
3. Use the smallest possible metadata request to identify the FC Copenhagen team ID for that season.
4. Confirm Team Squad by Team and Season ID endpoint access for those IDs.
5. Store any raw responses only under ignored local paths.
6. Record only a non-sensitive ID summary in Git.
7. Stop immediately if any credential, raw payload or provider cache appears in Git status.

## Candidate Discovery Endpoints

| Purpose | Candidate Endpoint / Method | Status | Notes |
|---|---|---|---|
| Confirm accessible leagues | League by ID with `currentSeason;seasons`. | completed | `league_id 271` accessible; `season_id 27897` confirmed. |
| Confirm latest/current season | League by ID with `currentSeason;seasons`. | completed | Denmark Superliga 2026/2027 confirmed. |
| Confirm teams | Teams by Season ID. | completed | FC København, `team_id 85`, confirmed without search fallback. |
| Confirm final squad endpoint | Team Squad by Team and Season ID. | completed | HTTP 200; data present; no broad field inspection. |

Do not record complete URLs containing a real `api_token`. Do not include credentials or raw responses.

## Required Before ID Discovery

- Secure credential setup document exists and has been reviewed.
- Local credential setup verification passed.
- `.env` ignore coverage verified.
- Token stored locally only.

- Football Free Plan confirmed.
- Denmark Superliga `league_id 271` selected.
- Credential storage path confirmed ignored.
- User explicitly confirms API key setup outside Git.
- `.env` or local configuration confirmed not tracked.
- `git status --short` clean.
- No credentials in docs, diffs or tracked files.
- Raw response path confirmed ignored.
- Cache path confirmed ignored.
- Stop conditions reviewed.
- Minimal ID discovery completed with 3 calls; no broad payload inspection performed.

## Allowed Outputs After ID Discovery

- A non-sensitive summary only:
  - confirmed `league_id`;
  - confirmed `season_id`;
  - confirmed `team_id`;
  - endpoint access result; and
  - whether fields appear suitable at a high level.
- No raw JSON.
- No full payload snippets.
- No credentials.
- No provider cache.
- No `.local.csv`.

## Still Forbidden In This Block

- Do not expose or commit credentials.
- Do not make additional API calls in this docs-only update.
- Do not inspect payloads.
- Do not commit provider cache.
- Do not create additional provider folders or outputs in this docs-only update.
- Do not write to SQLite.
- Do not activate Streamlit.
- Do not create parser or transform code.
- Do not approve Sportmonks.

## Next Required Action

ID discovery and the [confirmed ID scope review](sportmonks_confirmed_id_scope_review.md) have passed. The next later block may prepare the explicit minimal payload field review decision.
