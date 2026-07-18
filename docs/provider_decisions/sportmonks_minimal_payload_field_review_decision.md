# Sportmonks Minimal Payload Field Review Decision

## Status

- Candidate: Sportmonks
- Decision status: `approved-for-minimal-field-review`
- Related confirmed ID scope review: [Sportmonks Confirmed ID Scope Review](../provider_candidates/sportmonks_confirmed_id_scope_review.md)
- Related minimal ID discovery summary: [Sportmonks Minimal ID Discovery Summary](../provider_candidates/sportmonks_minimal_id_discovery_summary.md)
- Related payload decision record: [Sportmonks Payload Decision Record](sportmonks_payload_decision_record.md)
- Field review summary: [Sportmonks Minimal Payload Field Review Summary](../provider_candidates/sportmonks_minimal_payload_field_review_summary.md)
- Provider approval: no
- Field review approved: yes, minimal only
- Field review executed in this block: yes
- Review result: `passed`
- API calls in review: 0
- Raw response shape reviewed from existing ignored cache: yes
- Provider cache committed: no
- SQLite writes performed: no
- Streamlit activation performed: no
- Parser/transform code created: no

## Decision

- Permit a future minimal payload field review.
- Scope is limited to the already confirmed Sportmonks squad endpoint for one team and one season.
- This does not approve Sportmonks as a provider.
- This does not authorize broad payload inspection, local trial, SQLite writes, Streamlit activation or integration code.

## Confirmed Input Scope

| Item | Value |
|---|---|
| League | Denmark Superliga |
| League ID | `271` |
| Season | 2026/2027 |
| Season ID | `27897` |
| Team | FC København |
| Team ID | `85` |
| Endpoint | Team Squad by Team and Season ID |
| Endpoint pattern | `/football/squads/seasons/{season_id}/teams/{team_id}` |
| Expected endpoint IDs | `/football/squads/seasons/27897/teams/85` |

## Allowed Field Review Scope

- Inspect field names and high-level field categories only.
- Confirm whether the response appears to contain useful categories for:
  - identity;
  - squad/team context;
  - season context;
  - player reference IDs;
  - position or role, if present;
  - jersey number, if present; and
  - dates, freshness or provenance, if present.
- Count top-level records only.
- Summarize whether the payload shape looks suitable for a later transform design.
- Use only non-sensitive summaries in Git.

## API Call Limit For Future Field Review

- Preferred: use the existing ignored local raw response from minimal ID discovery if it is sufficient.
- If the existing cached response is missing or insufficient, allow at most 1 additional API call to the same squad endpoint.
- Do not use includes unless explicitly justified in the field review block.
- Do not expand pagination.
- Do not call player-detail endpoints.
- Do not perform broad league, team or player pulls.
- Do not make repeated retries beyond basic error handling.
- If the endpoint returns 401, 403, 429, a schema surprise or no data, stop.

## Allowed Local Handling

- Raw response may remain only under ignored local provider cache.
- Do not place raw JSON in Git.
- Do not include payload snippets in docs.
- Do not include a player list in docs.
- Do not expose the token in URLs, logs, docs, screenshots or ChatGPT.
- Use the Authorization header, not a token query parameter.
- The summary document may record only field names, categories and high-level suitability.

## Required Summary Format For Future Field Review

The future review must create:

`docs/provider_candidates/sportmonks_minimal_payload_field_review_summary.md`

That summary may include:

- Review status: `passed`, `partial` or `blocked`.
- Endpoint pattern only, with no token URL.
- Call count.
- Whether the existing cache was used or one new call was made.
- Top-level response type.
- Top-level data count.
- Field/category table.
- Missing or unclear categories.
- Suitability assessment.
- Stop conditions triggered, if any.
- No raw JSON.
- No player names list.
- No token.
- No provider approval.

## Stop Conditions

- Token appears anywhere outside local `.env`.
- `.env` appears in `git status --short`.
- Provider cache appears as tracked.
- Raw JSON appears in the Git diff.
- Field review requires more than one endpoint.
- Field review requires player-detail endpoints.
- Endpoint response is forbidden, unauthorized, rate-limited or unexpectedly large.
- Response shape is too complex to summarize safely without raw snippets.
- There is any uncertainty about licensing or exposure.

## Still Forbidden

- Do not approve Sportmonks.
- Do not perform broad payload inspection.
- Do not perform a local trial.
- Do not create `.local.csv`.
- Do not write SQLite.
- Do not activate Streamlit.
- Do not create parser or transform code.
- Do not commit provider cache.
- Do not commit raw JSON.
- Do not commit `.env`.
- Do not expose the token.

## Next Required Action

The minimal payload field review was executed from the existing ignored cache with 0 API calls and recorded as `passed`.

A later docs-only block may decide whether the observed payload shape is sufficient to plan a transform design. Transform code, local trial, SQLite writes, Streamlit activation and provider approval remain blocked.
