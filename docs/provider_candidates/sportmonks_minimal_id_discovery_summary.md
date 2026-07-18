# Sportmonks Minimal ID Discovery Summary

## Status

- Candidate: Sportmonks
- Discovery status: passed
- Related ID discovery plan: [Sportmonks ID Discovery Plan](sportmonks_id_discovery_plan.md)
- Related credential verification: [Sportmonks Local Credential Setup Verification](sportmonks_local_credential_setup_verification.md)
- Confirmed ID scope review: [passed](sportmonks_confirmed_id_scope_review.md)
- Minimal payload field review decision: [approved for a future minimal review](../provider_decisions/sportmonks_minimal_payload_field_review_decision.md)
- Provider approval: no
- API calls performed: yes, minimal ID discovery only
- Broad payload inspection performed: no
- Provider cache committed: no
- Raw responses committed: no
- SQLite writes performed: no
- Streamlit activation performed: no
- Parser/transform code created: no

## Confirmed Scope

| Item | Value | Status |
|---|---|---|
| League | Denmark Superliga | confirmed |
| League ID | `271` | confirmed |
| Season | 2026/2027 | confirmed |
| Season ID | `27897` | confirmed |
| Team | FC København | confirmed |
| Team ID | `85` | confirmed |
| Squad endpoint access | HTTP 200; data present | confirmed |

## Calls Performed

| Step | Purpose | Endpoint Pattern | Result |
|---|---|---|---|
| 1 | Season discovery | `/football/leagues/271` with `currentSeason;seasons` | HTTP 200; season confirmed |
| 2 | Team discovery | `/football/teams/seasons/{season_id}` | HTTP 200; team confirmed |
| 3 | Optional team search fallback | `/football/teams/search/Copenhagen` | not used |
| 4 | Squad endpoint access | `/football/squads/seasons/{season_id}/teams/{team_id}` | HTTP 200; data present; 6 entries |

Three API calls were performed. No URL containing the token was recorded.

## Interpretation

Minimal ID discovery confirms the IDs needed for the later scoped trial. This does not approve Sportmonks as a provider and does not authorize broad payload pulls.

The [confirmed ID scope review](sportmonks_confirmed_id_scope_review.md) has passed. The completed discovery remains minimal, and a [strict decision](../provider_decisions/sportmonks_minimal_payload_field_review_decision.md) now governs any future minimal payload field review.

## Local Raw Response Handling

Raw responses were stored only under the ignored local provider cache path `data/provider_cache/sportmonks/id_discovery/`. Raw responses were not committed. This document contains only non-sensitive summary values and no payload snippets or player list.

## Still Forbidden

- Do not commit raw JSON.
- Do not commit provider cache.
- Do not commit `.env`.
- Do not commit the API token.
- Do not perform broad payload inspection.
- Do not write to SQLite.
- Do not activate Streamlit.
- Do not create parser or transform code.
- Do not approve Sportmonks.

## Next Required Action

The [confirmed ID scope review](sportmonks_confirmed_id_scope_review.md) has passed.

A later explicit block may execute the minimal payload field review under the [approved decision](../provider_decisions/sportmonks_minimal_payload_field_review_decision.md). This summary grants no additional API calls.
