# Sportmonks ID Discovery Plan

## Status

- Candidate: Sportmonks
- ID discovery status: draft/pre-credential
- Related trial scope plan: [Sportmonks Ignored Local Trial Scope Plan](sportmonks_ignored_local_trial_scope_plan.md)
- Related checklist: [Sportmonks Provider Payload Checklist](sportmonks_provider_payload_checklist.md)
- Related decision record: [Sportmonks Payload Decision Record](../provider_decisions/sportmonks_payload_decision_record.md)
- Provider approval: no
- Credentials created: no
- API calls performed: no
- Payload inspection performed: no
- Provider cache created: no
- Local trial performed: no
- Season ID confirmed: no
- Team ID confirmed: no
- Endpoint access confirmed: no

## Purpose

The user could not find the Denmark Superliga `season_id` or FC Copenhagen `team_id` in the Sportmonks UI. This plan defines a minimal future ID discovery path without inventing IDs or endpoint access.

It does not create credentials, call APIs or inspect payloads. All raw API responses and credentials must remain outside Git.

## Manual UI Lookup Result

| Item | Target | Result | Status |
|---|---|---|---|
| League list | Free Plan leagues | Found in UI screenshot. | confirmed |
| Selected league | Denmark Superliga, league_id 271 | Found in UI screenshot. | confirmed |
| Season ID | Latest Denmark Superliga season | Not found in UI. | pending |
| Team ID | FC Copenhagen | Not found in UI. | pending |
| Endpoint access | Team Squad by Team and Season ID | Not tested. | pending |

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
| Confirm accessible leagues | GET All Leagues with `currentSeason` or `seasons` include if needed. | planned | `league_id 271` is already known; useful for `season_id`. |
| Confirm latest/current season | League by ID or All Leagues with `currentSeason` or `seasons` include. | planned | Must minimize response. |
| Confirm teams | Teams by Season ID or minimal team lookup or search if available. | planned | Used only to identify FC Copenhagen `team_id`. |
| Confirm final squad endpoint | Team Squad by Team and Season ID. | planned | Only after `season_id` and `team_id` are known. |

Do not record complete URLs containing a real `api_token`. Do not include credentials or raw responses.

## Required Before ID Discovery

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

## Allowed Outputs After Future ID Discovery

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

- Do not create credentials.
- Do not call APIs.
- Do not inspect payloads.
- Do not create provider cache.
- Do not create provider folders or outputs.
- Do not write to SQLite.
- Do not activate Streamlit.
- Do not create parser or transform code.
- Do not approve Sportmonks.

## Next Required Action

Prepare secure local credential setup in a separate explicit block. That block must only configure ignored credential storage and safety checks.

ID discovery API calls must remain a later, separate explicit block after credential setup is reviewed.
