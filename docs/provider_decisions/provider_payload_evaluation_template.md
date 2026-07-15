# Provider Payload Evaluation Template

## Status

- Status: Draft / Accepted / Deferred / Rejected
- Date:
- Reviewer:
- Provider candidate:
- Payload reviewed:
- Related decision record:
- Related checklist:

## Summary

Describe in two to four lines which payload is being evaluated, which Market Context fields it may cover and whether its terms permit local use.

## Payload Source

- Provider/source name:
- Endpoint/report/file/source:
- Retrieval method:
- Sample type: synthetic / licensed / public / manual
- Sample location:
- Can sample be versioned?: yes / no / unknown
- Can derived outputs be versioned?: yes / no / unknown
- Notes:

## License And Terms Review

- Terms reviewed: yes / no
- License permits local development use: yes / no / unknown
- License permits caching: yes / no / unknown
- License permits derived outputs: yes / no / unknown
- Redistribution permitted: yes / no / unknown
- Screenshot/demo restrictions:
- Credential handling:
- Raw dumps allowed in git?: no unless explicitly allowed
- Reviewer notes:

## Payload Shape

| Field | Available: yes / no / partial / unknown | Notes |
|---|---|---|
| `provider_player_id` |  |  |
| `provider_team_id` |  |  |
| `provider_league_id` |  |  |
| `provider_season` |  |  |
| `provider_player_name` |  |  |
| `provider_team_name` |  |  |
| age or birthdate |  |  |
| market value |  |  |
| market value currency |  |  |
| market value date |  |  |
| contract end date |  |  |
| `source` / `source_url` |  |  |
| `fetched_at` / `value_date` |  |  |
| confidence / provenance |  |  |

## Identity Mapping Fit

- Strong provider IDs available?: yes / no / partial
- Season-aware mapping possible?: yes / no / partial
- Transfers/team changes handled?: yes / no / partial
- Duplicate IDs risk:
- Name-only/fuzzy matching required?: yes / no
- Mapping storage plan:
- Mapping review process:

## Market Context Fit

- Can produce canonical `age`:
- Can produce canonical `market_value_eur`:
- Can produce canonical `contract_end_date`:
- Can produce `source`, `source_url`, `confidence`, `notes`:
- Missing values distinguishable from zero:
- Salary/cost fields confused with market value?: yes / no
- Currency conversion needed?: yes / no
- Value date available?: yes / no

## Cache And Storage Plan

- Raw payload storage:
- Canonical output storage:
- `.local.csv` or ignored path:
- Refresh policy:
- Retention policy:
- Deletion process:
- Git safety check:

## Transform Experiment Plan

- Transform experiment allowed?: yes / no / unknown
- Input path:
- Mapping path:
- Expected canonical output path:
- Preview command:
- Diagnostics command:
- Cleanup command:
- No network/app runtime calls confirmation:

## Diagnostics Expectations

- Expected `matched_count`:
- Expected unmatched review:
- Expected effective coverage:
- Expected validation errors:
- Duplicate key expectation:
- App activation allowed?: yes / no, normally no until accepted

## Decision

- Decision: accept / defer / reject
- Rationale:
- Blocking issues:
- Follow-up actions:
- Re-review trigger:

## Safety Notes

- No scraping.
- No live provider calls from the app.
- No credentials in the repository.
- No raw dumps in git unless explicitly allowed.
- Real outputs remain local and ignored unless redistribution is explicitly permitted.
- No scoring changes until real coverage is sufficient.
