# Capology Public Evidence

## Status

- Candidate: Capology
- Research status: `public-evidence-pass-completed`
- Consultation date range: 2026-07-20
- Researcher: Codex
- Official sources reviewed: 7
- Secondary sources reviewed: 0
- Login used: no
- API calls: no
- Cache reading: no
- Raw JSON review: no
- Automated scraping: no
- Provider approval: no

## Candidate Boundary

- Intended role: Salary and contract context candidate.
- Automation boundary: Public pages and public documentation only; no login, API call, bulk extraction or player-data copying.
- Known repository context: Review-only candidate with no approved integration.
- Explicit exclusions: No assumption that an API subscription or market-value field exists beyond public evidence.

## Evidence Table

| Candidate | Criterion | Claim | Classification | Finding Type | Source Title | Source Publisher | Public URL | Source Tier | Consulted | Freshness Risk | Limitations | Conflict Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Capology | Stable player IDs | Public API documentation defines unique and persistent player IDs. | confirmed | fact | Players API Documentation | Capology | https://www.capology.com/documentation/api/v2/players/ | Tier 1 | 2026-07-20 | medium | Persistence outside the documented API contract was not assessed. |  |
| Capology | Human-readable player labels | Public schemas include player names and player identifiers. | confirmed | fact | Players API Documentation | Capology | https://www.capology.com/documentation/api/v2/players/ | Tier 1 | 2026-07-20 | medium | Population and spelling consistency were not tested. |  |
| Capology | Team and competition labels | Salary and contract schemas document league and club IDs and names. | confirmed | fact | Contracts API Documentation | Capology | https://www.capology.com/documentation/api/v2/contracts/ | Tier 1 | 2026-07-20 | medium | Coverage depends on subscription and league availability. |  |
| Capology | Position IDs and labels | Public salary schema documents broad player groups and group codes. | partial | fact | Salaries API Documentation | Capology | https://www.capology.com/documentation/api/v2/salaries/ | Tier 1 | 2026-07-20 | medium | Detailed positions and stable position IDs were not confirmed. |  |
| Capology | Jersey coverage | No jersey-number field was confirmed in the reviewed public schemas. | unknown | open-question | Players API Documentation | Capology | https://www.capology.com/documentation/api/v2/players/ | Tier 1 | 2026-07-20 | high | Unreviewed schemas may differ. |  |
| Capology | Player age | Public contract and salary schemas document player age and date of birth. | confirmed | fact | Contracts API Documentation | Capology | https://www.capology.com/documentation/api/v2/contracts/ | Tier 1 | 2026-07-20 | medium | Coverage by league and season was not tested. |  |
| Capology | Market value | No player market-value field was confirmed in public product, pricing or reviewed API documentation. | unknown | open-question | Capology Features | Capology | https://www.capology.com/features/ | Tier 2 | 2026-07-20 | high | Salary and transfer-finance context are not market value. |  |
| Capology | Contract end date | Public contract schema documents `contract_expiration` in ISO date format. | confirmed | fact | Contracts API Documentation<br>Capology Assistance | Capology | https://www.capology.com/documentation/api/v2/contracts/<br>https://www.capology.com/assistance/ | Tier 1 | 2026-07-20 | high | Capology states it lacks official access to player contracts; field accuracy is not independently verified. | Contract field exists while source certainty is qualified. |
| Capology | Salary context | Public schemas document gross/net salary estimates, bonuses and verification indicators. | confirmed | fact | Contracts API Documentation | Capology | https://www.capology.com/documentation/api/v2/contracts/ | Tier 1 | 2026-07-20 | high | Figures are estimates and may omit incentives, image rights or commercial deals. |  |
| Capology | Salary methodology | Capology states salaries are estimates sourced from public information, industry contacts and a source network; some values are algorithmic estimates. | confirmed | fact | Capology Assistance | Capology | https://www.capology.com/assistance/ | Tier 1 | 2026-07-20 | high | Even verified salaries are not official contract confirmation. |  |
| Capology | League coverage | Public pricing lists six leagues for API Basic and more than 30 for API Plus, subject to coverage limitations. | confirmed | fact | Capology Pricing | Capology | https://www.capology.com/pricing/ | Tier 1 | 2026-07-20 | high | Exact current league rows and field depth are time-sensitive. |  |
| Capology | Freshness | Public help states three major updates per year plus smaller updates and corrections. | confirmed | fact | Capology Assistance | Capology | https://www.capology.com/assistance/ | Tier 1 | 2026-07-20 | high | This cadence is not real-time and may vary by league. |  |
| Capology | Provenance | Public methodology describes source categories and verification marks but not source-level lineage for each record. | partial | fact | Capology Features | Capology | https://www.capology.com/features/ | Tier 2 | 2026-07-20 | medium | Individual source provenance is not publicly exposed in reviewed pages. |  |
| Capology | Licensing clarity | API plans require a standard service agreement; public help says API data may not be published without a publishing license. | restricted | fact | Capology Pricing<br>Capology Assistance | Capology | https://www.capology.com/pricing/<br>https://www.capology.com/assistance/ | Tier 1 | 2026-07-20 | high | Internal derived-use and caching would depend on an unreviewed agreement. |  |
| Capology | Attribution requirements | No public general attribution rule for API data was confirmed. | unknown | open-question | Capology Assistance | Capology | https://www.capology.com/assistance/ | Tier 1 | 2026-07-20 | high | Publishing requires a separate license, whose attribution terms were not reviewed. |  |
| Capology | Redistribution restrictions | Public help explicitly says API data cannot be published without an additional publishing license. | restricted | fact | Capology Assistance | Capology | https://www.capology.com/assistance/ | Tier 1 | 2026-07-20 | high | Exact private/internal redistribution boundaries require the service agreement. |  |
| Capology | Local/cache-first workflow fit | Public documentation supports structured APIs, but no public cache or retention right was confirmed. | unknown | open-question | API Get Started | Capology | https://www.capology.com/documentation/api/v2/get-started/ | Tier 1 | 2026-07-20 | high | Requires paid access and an API key; no account was used. |  |
| Capology | Identity mapping complexity | Persistent IDs, names and an advertised ID-mapping add-on support structured matching. | partial | inference | Capology Pricing | Capology | https://www.capology.com/pricing/ | Tier 1 | 2026-07-20 | high | Mapping availability requires a standard agreement and was not tested. |  |
| Capology | Integration complexity | Public schemas are structured, but paid plans, agreement requirements, estimate semantics and restricted publication add governance overhead. | partial | inference | Capology Pricing | Capology | https://www.capology.com/pricing/ | Tier 1 | 2026-07-20 | high | No implementation or payload inspection occurred. |  |
| Capology | Public pricing and plan limits | Public pricing lists paid website/API tiers, league coverage and standard-agreement requirements. | confirmed | fact | Capology Pricing | Capology | https://www.capology.com/pricing/ | Tier 1 | 2026-07-20 | high | Prices and included coverage are time-sensitive. |  |

## Governance And Licensing

Public pages describe paid API products that require a standard service agreement. Publication is explicitly restricted unless a publishing license is acquired. Caching, internal derived use and attribution remain unresolved without reviewing a concrete agreement.

## Identity And Labels

Persistent player IDs and named league, club and player entities are publicly documented. Position information is broad rather than detailed in the reviewed schemas.

## Position And Jersey Coverage

Broad position groups and codes are documented. Jersey-number coverage remains unknown.

## Market Context

Age, contract expiration and salary context are documented. Salary figures are estimates, including values marked verified, because Capology states it lacks official access to player contracts. Market value remains unknown.

## Coverage And Freshness

Public pricing differentiates six-league and broader plans. Public help describes periodic major updates and smaller corrections rather than continuous updates.

## Pricing And Public Plan Limits

Public prices, plan names, league counts and standard-agreement requirements are visible and time-sensitive. No purchase, login or trial was used.

## Technical And Local Workflow Fit

The public API schemas are structured and identity-oriented. Local caching rights and permitted internal derived outputs remain unknown pending a concrete agreement.

## Conflicts

- Contract-expiry fields are documented, while Capology also states that it lacks official access to players' contracts for confirmation.

## Unknowns

- Market value.
- Jersey numbers.
- Detailed position identifiers.
- Cache and retention rights.
- Internal derived-use rights.
- Attribution terms.

## Research Stop Conditions Encountered

- Agreement-specific rights were not available on the reviewed public pages.
- No API sample was requested or downloaded.
- No account-only coverage or product details were inspected.

## Candidate-Level Summary

Public evidence is sufficiently complete for descriptive assessment of salary, contract, age, identity, pricing and publication restrictions. Market value, jersey coverage and local-workflow permissions remain incomplete. This summary does not recommend, rank, score or approve Capology.
