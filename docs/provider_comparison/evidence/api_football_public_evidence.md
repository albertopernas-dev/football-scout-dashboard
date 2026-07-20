# API-Football / API-Sports Public Evidence

## Status

- Candidate: API-Football / API-Sports
- Research status: `public-evidence-pass-completed`
- Consultation date range: 2026-07-20
- Researcher: Codex
- Official sources reviewed: 3
- Secondary sources reviewed: 0
- Login used: no
- API calls: no
- Cache reading: no
- Raw JSON review: no
- Automated scraping: no
- Provider approval: no

## Candidate Boundary

- Intended role: Existing football-statistics source and technical comparison baseline.
- Automation boundary: Public API-Football/API-Sports documentation only; no endpoint execution or dashboard access.
- Known repository context: Existing offline statistics integration does not establish Market Context suitability or approval.
- Explicit exclusions: No local data, cache, scoring, recommendation, implementation or provider approval.

## Evidence Table

| Candidate | Criterion | Claim | Classification | Finding Type | Source Title | Source Publisher | Public URL | Source Tier | Consulted | Freshness Risk | Limitations | Conflict Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| API-Football / API-Sports | Product boundary | API-Football is the football API product documented and served under the API-Sports platform. | confirmed | fact | API-Sports Documentation Football | API-Sports | https://api-sports.io/documentation/football/v3 | Tier 1 | 2026-07-20 | medium | Branding and commercial channels may change. |  |
| API-Football / API-Sports | Stable player IDs | Documentation states player IDs are unique and remain with players across teams. | confirmed | fact | API-Sports Documentation Football | API-Sports | https://api-sports.io/documentation/football/v3 | Tier 1 | 2026-07-20 | medium | Cross-version persistence is not expressly guaranteed. |  |
| API-Football / API-Sports | Human-readable player labels | Player profile documentation exposes name, first name and last name fields. | confirmed | fact | API-Sports Documentation Football | API-Sports | https://api-sports.io/documentation/football/v3 | Tier 1 | 2026-07-20 | medium | Population varies with available profiles. |  |
| API-Football / API-Sports | Team and competition labels | Player-statistics and squad schemas expose team and league identifiers and names. | confirmed | fact | API-Sports Documentation Football | API-Sports | https://api-sports.io/documentation/football/v3 | Tier 1 | 2026-07-20 | medium | Availability depends on competition coverage. |  |
| API-Football / API-Sports | Position IDs and labels | Profiles and squads expose broad position labels; no stable position identifier contract was confirmed. | partial | fact | API-Sports Documentation Football | API-Sports | https://api-sports.io/documentation/football/v3 | Tier 1 | 2026-07-20 | medium | Lineup grid coordinates are not canonical position IDs. |  |
| API-Football / API-Sports | Jersey coverage | Profiles and current squad responses document a player number field. | partial | fact | API-Sports Documentation Football | API-Sports | https://api-sports.io/documentation/football/v3 | Tier 1 | 2026-07-20 | high | Completeness across leagues, squads and seasons is not guaranteed. |  |
| API-Football / API-Sports | Player age | Profiles document age and date-of-birth fields. | confirmed | fact | API-Sports Documentation Football | API-Sports | https://api-sports.io/documentation/football/v3 | Tier 1 | 2026-07-20 | medium | Coverage may vary by available player profile. |  |
| API-Football / API-Sports | Market value | Reviewed official documentation and pricing do not establish a player market-value field. | unknown | open-question | API-Sports Documentation Football | API-Sports | https://api-sports.io/documentation/football/v3 | Tier 1 | 2026-07-20 | high | Transfer fee text is not player market value. |  |
| API-Football / API-Sports | Contract end date | Reviewed public schemas do not establish player contract-expiry data. | unknown | open-question | API-Sports Documentation Football | API-Sports | https://api-sports.io/documentation/football/v3 | Tier 1 | 2026-07-20 | high | Career team dates and transfer dates must not be treated as contract end. |  |
| API-Football / API-Sports | Salary context | Reviewed official documentation does not establish salary or compensation data. | unknown | open-question | API-Sports Documentation Football | API-Sports | https://api-sports.io/documentation/football/v3 | Tier 1 | 2026-07-20 | high | Absence from reviewed pages is not proof of permanent non-availability. |  |
| API-Football / API-Sports | League coverage | Pricing says plans include all competitions and endpoints, while terms warn that actual data availability varies by competition. | partial | fact | API-Football Pricing<br>API-Sports Terms | API-Sports | https://www.api-football.com/pricing<br>https://api-sports.io/terms | Tier 1 | 2026-07-20 | high | Free plans have season limits and field coverage may vary. | Marketing breadth is qualified by terms. |
| API-Football / API-Sports | Freshness | Documentation publishes indicative update frequencies for profiles, squads, lineups and statistics. | partial | fact | API-Sports Documentation Football | API-Sports | https://api-sports.io/documentation/football/v3 | Tier 1 | 2026-07-20 | high | Documentation says frequency can vary by competition. |  |
| API-Football / API-Sports | Provenance | No field-level source provenance model was found in the reviewed official pages. | unknown | open-question | API-Sports Terms | API-Sports | https://api-sports.io/terms | Tier 1 | 2026-07-20 | high | Provider identity is known, underlying source lineage is not. |  |
| API-Football / API-Sports | Licensing clarity | Public terms explain subscription, quotas and availability but do not clearly define redistribution or internal derived-use rights. | partial | fact | API-Sports Terms of Service | API-Sports | https://api-sports.io/terms | Tier 1 | 2026-07-20 | high | Concrete downstream usage would require separate clarification. |  |
| API-Football / API-Sports | Attribution requirements | No general attribution requirement was confirmed in the reviewed public terms. | unknown | open-question | API-Sports Terms of Service | API-Sports | https://api-sports.io/terms | Tier 1 | 2026-07-20 | high | Unknown must not be interpreted as no attribution requirement. |  |
| API-Football / API-Sports | Redistribution restrictions | Public terms reviewed do not provide a clear redistribution grant. | unknown | open-question | API-Sports Terms of Service | API-Sports | https://api-sports.io/terms | Tier 1 | 2026-07-20 | high | Subscription access does not itself imply redistribution permission. |  |
| API-Football / API-Sports | Local/cache-first workflow fit | Public documentation supports reproducible IDs and endpoint-specific refresh guidance, but public cache rights were not established. | partial | inference | API-Sports Documentation Football | API-Sports | https://api-sports.io/documentation/football/v3 | Tier 1 | 2026-07-20 | high | Technical fit and permitted storage are separate questions. |  |
| API-Football / API-Sports | Identity mapping complexity | Unique player IDs and named team/league entities reduce mapping ambiguity within the product. | partial | inference | API-Sports Documentation Football | API-Sports | https://api-sports.io/documentation/football/v3 | Tier 1 | 2026-07-20 | medium | Cross-provider mapping remains unverified. |  |
| API-Football / API-Sports | Integration complexity | Public REST documentation, pagination, coverage flags and schemas support technical integration. | partial | inference | API-Sports Documentation Football | API-Sports | https://api-sports.io/documentation/football/v3 | Tier 1 | 2026-07-20 | medium | Market Context gaps and licensing clarity remain unresolved. |  |
| API-Football / API-Sports | Public pricing and plan limits | Public pricing lists free and paid request quotas and states that all endpoints are included, with free-season limits. | confirmed | fact | API-Football Pricing | API-Sports | https://www.api-football.com/pricing | Tier 1 | 2026-07-20 | high | Pricing and quotas are time-sensitive. |  |

## Governance And Licensing

The public terms cover subscription channels, quotas, renewal and variable data availability. The reviewed pages do not clearly grant redistribution or define internal derived-use rights, so licensing suitability remains partial.

## Identity And Labels

Player IDs, player names, team names and league names are documented. Broad position labels are available; a stable canonical position-ID scheme was not confirmed.

## Position And Jersey Coverage

Squad/profile schemas include broad positions and shirt numbers. Coverage is partial because documentation warns that competition-level availability varies.

## Market Context

Age and date of birth are documented. Market value, contract end and salary remain `unknown`. Documented transfer fee strings are not equivalent to current player market value.

## Coverage And Freshness

Plans advertise all competitions and endpoints, but terms and documentation qualify actual field availability by competition. Update frequencies are documented as indicative rather than guaranteed.

## Pricing And Public Plan Limits

Current public pricing and daily request quotas are visible. Free access is season-limited; current plan facts require revalidation when used.

## Technical And Local Workflow Fit

The documented API structure is technically compatible with normalized local processing. Public evidence does not settle cache rights or Market Context completeness.

## Conflicts

- Broad pricing claims about all competitions/endpoints coexist with explicit warnings that data availability varies by competition.

## Unknowns

- Market value.
- Contract end.
- Salary context.
- Field-level provenance.
- Redistribution rights.
- General attribution requirements.
- Explicit cache and internal derived-use rights.

## Research Stop Conditions Encountered

- No dashboard or plan-specific authenticated coverage was reviewed.
- No endpoint was called to test field population.
- Licensing ambiguity was recorded instead of interpreted.

## Candidate-Level Summary

Public evidence is sufficient for a descriptive technical baseline covering identity, labels, age, statistics-oriented schemas and pricing. Market Context and downstream-use permissions remain materially incomplete. This summary does not recommend, rank, score or approve API-Football/API-Sports.
