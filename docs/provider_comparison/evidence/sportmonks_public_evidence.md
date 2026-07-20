# Sportmonks Public Evidence

## Status

- Candidate: Sportmonks
- Research status: `public-evidence-pass-completed`
- Consultation date range: 2026-07-20
- Researcher: Codex
- Official sources reviewed: 9
- Secondary sources reviewed: 0
- Login used: no
- API calls: no
- Cache reading: no
- Raw JSON review: no
- Automated scraping: no
- Provider approval: no

## Candidate Boundary

- Intended role: Main evaluated candidate carried over from v0.8.0.
- Automation boundary: Public pages only; no account, dashboard, API, SDK, payload or cache access.
- Known repository context: Existing local scaffold is excluded as evidence of current public capabilities.
- Explicit exclusions: No scoring, recommendation, implementation or provider approval.

## Evidence Table

| Candidate | Criterion | Claim | Classification | Finding Type | Source Title | Source Publisher | Public URL | Source Tier | Consulted | Freshness Risk | Limitations | Conflict Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Sportmonks | Stable player IDs | Public player documentation describes player retrieval by `player_id` and exposes an `id` field. | confirmed | fact | Players | Sportmonks | https://docs.sportmonks.com/v3/tutorials-and-guides/tutorials/teams-players-coaches-and-referees/players | Tier 1 | 2026-07-20 | medium | Persistence guarantees across major versions are not stated. |  |
| Sportmonks | Human-readable player labels | Public player documentation exposes name, display name, first name and last name fields. | confirmed | fact | Players | Sportmonks | https://docs.sportmonks.com/v3/tutorials-and-guides/tutorials/teams-players-coaches-and-referees/players | Tier 1 | 2026-07-20 | medium | Field population by league was not verified. |  |
| Sportmonks | Team and competition labels | The public product and coverage pages advertise team, league and competition data across selected leagues. | advertised | fact | Football API for Developers | Sportmonks | https://www.sportmonks.com/football-api/ | Tier 2 | 2026-07-20 | high | Marketing page does not prove population for every competition. |  |
| Sportmonks | Position IDs and labels | Player docs describe position and detailed-position includes; Team Squad docs list position IDs and detailed position IDs. | confirmed | fact | Players<br>Team, Player, Squad, Coach and Referee | Sportmonks | https://docs.sportmonks.com/v3/tutorials-and-guides/tutorials/teams-players-coaches-and-referees/players<br>https://docs.sportmonks.com/v3/endpoints-and-entities/entities/team-player-squad-coach-and-referee | Tier 1 | 2026-07-20 | medium | Reliable population across leagues remains unverified. |  |
| Sportmonks | Jersey coverage | Public Team Squad entity documentation defines `jersey_number`, and lineup documentation also exposes jersey numbers, but population and completeness across leagues and squad endpoints were not tested. | partial | fact | Team, Player, Squad, Coach and Referee<br>Lineups | Sportmonks | https://docs.sportmonks.com/v3/endpoints-and-entities/entities/team-player-squad-coach-and-referee<br>https://docs.sportmonks.com/v3/tutorials-and-guides/tutorials/includes/lineups | Tier 1 | 2026-07-20 | high | Population and completeness across leagues and squad endpoints were not tested. |  |
| Sportmonks | Player age | Player documentation exposes date of birth, from which age can be derived. | partial | inference | Players | Sportmonks | https://docs.sportmonks.com/v3/tutorials-and-guides/tutorials/teams-players-coaches-and-referees/players | Tier 1 | 2026-07-20 | medium | No direct age field or completeness guarantee was confirmed. |  |
| Sportmonks | Market value | No authoritative public source reviewed documents a player market-value field. | unknown | open-question | Football API for Developers | Sportmonks | https://www.sportmonks.com/football-api/ | Tier 2 | 2026-07-20 | high | Absence from reviewed pages does not prove non-availability. |  |
| Sportmonks | Contract end date | Public Team Squad entity documentation defines an `end` field as the player's contract end date. | confirmed | fact | Team, Player, Squad, Coach and Referee | Sportmonks | https://docs.sportmonks.com/v3/endpoints-and-entities/entities/team-player-squad-coach-and-referee | Tier 1 | 2026-07-20 | high | Field population, accuracy and availability across leagues, plans and squad endpoints were not tested. |  |
| Sportmonks | Salary context | No authoritative public source reviewed documents player salary or compensation fields. | unknown | open-question | Football API for Developers | Sportmonks | https://www.sportmonks.com/football-api/ | Tier 2 | 2026-07-20 | high | No conclusion about unreviewed products or private plans. |  |
| Sportmonks | League coverage | Official public pages state more than 2,200 leagues in one place and more than 2,500 in another. | conflicting | fact | Football Coverage<br>Football API for Developers | Sportmonks | https://www.sportmonks.com/football-api/coverage/<br>https://www.sportmonks.com/football-api/ | Tier 1 | 2026-07-20 | high | Exact current count and per-league field depth require reconciliation. | Official public pages use different totals. |
| Sportmonks | Freshness | Player docs expose a last-updated endpoint for recent changes; squad history notes variable and incomplete competition coverage. | partial | fact | Players<br>Squads | Sportmonks | https://docs.sportmonks.com/v3/tutorials-and-guides/tutorials/teams-players-coaches-and-referees/players<br>https://www.sportmonks.com/glossary/squads/ | Tier 1 | 2026-07-20 | high | No single freshness guarantee covers all required criteria. |  |
| Sportmonks | Provenance | Official FAQ and product pages state that scouts and data partners collect and validate data. | advertised | fact | Sportmonks FAQ | Sportmonks | https://www.sportmonks.com/faq/ | Tier 2 | 2026-07-20 | medium | Source-level provenance per field or record was not documented. |  |
| Sportmonks | Licensing clarity | Public terms distinguish service materials from supplied data, prohibit unauthorized resale and describe allowed product-building use. | partial | fact | Sportmonks Terms of Service | Sportmonks | https://www.sportmonks.com/terms-of-service/ | Tier 1 | 2026-07-20 | high | Internal derived-use boundaries and multi-source redistribution remain materially ambiguous. | Terms contain nuanced storage/distribution language. |
| Sportmonks | Attribution requirements | Terms discuss rights and attribution concerns for logos and profile photos but do not state a general data-attribution rule. | partial | fact | Sportmonks Terms of Service | Sportmonks | https://www.sportmonks.com/terms-of-service/ | Tier 1 | 2026-07-20 | high | Asset rights are separate from general data attribution. |  |
| Sportmonks | Redistribution restrictions | Direct resale is prohibited; public terms say supplied data may be stored or distributed while the service itself remains protected. | restricted | fact | Sportmonks Terms of Service | Sportmonks | https://www.sportmonks.com/terms-of-service/ | Tier 1 | 2026-07-20 | high | A concrete use case would need clarification before integration. |  |
| Sportmonks | Local/cache-first workflow fit | Official guidance encourages caching static data and gives example retention intervals. | partial | fact | API Throughput | Sportmonks | https://www.sportmonks.com/blogs/api-throughput/ | Tier 1 | 2026-07-20 | medium | Guidance is operational, not a complete license grant for this project. |  |
| Sportmonks | Identity mapping complexity | Stable IDs, labels and positions are documented, but field population and Market Context identity remain unresolved. | partial | inference | Players<br>Squads | Sportmonks | https://docs.sportmonks.com/v3/tutorials-and-guides/tutorials/teams-players-coaches-and-referees/players<br>https://www.sportmonks.com/glossary/squads/ | Tier 1 | 2026-07-20 | medium | No payload or cross-provider mapping was inspected. |  |
| Sportmonks | Integration complexity | Public docs describe REST, includes, filters and uniform selected-league access. | partial | inference | Football API for Developers | Sportmonks | https://www.sportmonks.com/football-api/ | Tier 2 | 2026-07-20 | high | Technical ease does not establish field completeness or permitted use. |  |
| Sportmonks | Public pricing and plan limits | Public pricing lists league-count tiers, hourly entity limits and starting monthly prices. | confirmed | fact | Football API for Developers | Sportmonks | https://www.sportmonks.com/football-api/ | Tier 1 | 2026-07-20 | high | Pricing and plan contents are time-sensitive; free access requires an account. |  |

## Governance And Licensing

Public terms permit building products from supplied data and prohibit direct resale. They also distinguish data from copyrighted website materials and call out separate rights for logos and profile photos. The exact boundary for internal derived datasets, redistribution and multi-provider combination remains partial rather than fully confirmed.

## Identity And Labels

Player IDs and human-readable names are documented. General and detailed positions are also documented, but population and persistence guarantees across all selected leagues remain unverified.

## Position And Jersey Coverage

Position identifiers and labels are documented. Jersey numbers are documented in the Team Squad entity and fixture lineups, but population and completeness across leagues and squad endpoints were not tested.

## Market Context

Date of birth supports derived age. Contract end is publicly documented in the Team Squad entity. Market value and salary remain `unknown`. Population and reliability of contract dates were not tested.

## Coverage And Freshness

Official pages conflict on the headline league count. Public docs expose recent-update patterns and acknowledge variable historical coverage; criterion-level completeness remains partial.

## Pricing And Public Plan Limits

Current public pricing is visible and organized by selected league count and request capacity. Prices, free-plan content and plan limits are time-sensitive.

## Technical And Local Workflow Fit

REST endpoints, IDs, includes and caching guidance support a plausible cache-first architecture. This is a technical observation only; it does not resolve licensing or Market Context gaps.

## Conflicts

- Official pages use different current league totals.
- Public terms contain nuanced wording around protected services, supplied-data storage/distribution and resale.

## Unknowns

- Market value availability.
- Salary context.
- General data-attribution requirement.
- Exact internal derived-use permission for this project.
- Per-league completeness of labels, positions and jersey numbers.

## Research Stop Conditions Encountered

- Account-specific free-plan scope was not reviewed because it requires account access.
- Any field claim requiring API responses was left unknown or partial.
- Ambiguous licensing points were not interpreted beyond the public wording.

## Candidate-Level Summary

Public evidence is sufficient for a partial descriptive assessment of identity, labels, positions, documented contract end, pricing and API workflow. Market Context remains incomplete because market value and salary are unknown, contract-date population and reliability were not tested, and several licensing boundaries remain unresolved. This summary does not recommend, rank, score or approve Sportmonks.
