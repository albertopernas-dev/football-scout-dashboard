# Transfermarkt Manual Reference Public Evidence

## Status

- Candidate: Transfermarkt manual reference
- Research status: `public-evidence-pass-completed`
- Consultation date range: 2026-07-20
- Researcher: Codex
- Official sources reviewed: 6
- Secondary sources reviewed: 0
- Login used: no
- API calls: no
- Cache reading: no
- Raw JSON review: no
- Automated scraping: no
- Provider approval: no

## Candidate Boundary

- Intended role: Manual market-value and contract reference only.
- Automation boundary: Public manual pages only; no scraping, bulk extraction, API assumptions or automated integration.
- Known repository context: Existing manual-reference workflow does not imply permission to automate or redistribute data.
- Explicit exclusions: No individual player data copied, no integration, scoring, recommendation or provider approval.

## Evidence Table

| Candidate | Criterion | Claim | Classification | Finding Type | Source Title | Source Publisher | Public URL | Source Tier | Consulted | Freshness Risk | Limitations | Conflict Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Transfermarkt manual reference | Stable player IDs | Public profile URLs use numeric player identifiers, but no official persistence guarantee was found. | partial | inference | Data Administration, Market Values and Watchlist | Transfermarkt | https://www.transfermarkt.com/data-administration-market-values-and-watchlist-become-a-part-of-the-transfermarkt-community/view/news/403373 | Tier 1 | 2026-07-20 | medium | URL structure is observable, not a published identifier contract. |  |
| Transfermarkt manual reference | Human-readable player labels | Public player and squad pages display player names. | confirmed | fact | Detailed Squad | Transfermarkt | https://www.transfermarkt.com/inter-milan/kader/verein/46 | Tier 1 | 2026-07-20 | medium | No bulk or automated use is authorized. |  |
| Transfermarkt manual reference | Team and competition labels | Public squad pages display club and competition labels. | confirmed | fact | Detailed Squad | Transfermarkt | https://www.transfermarkt.com/inter-milan/kader/verein/46 | Tier 1 | 2026-07-20 | medium | Coverage was not enumerated systematically. |  |
| Transfermarkt manual reference | Position IDs and labels | Public squad/profile presentation includes human-readable positions; no official stable position-ID scheme was found. | partial | fact | Detailed Squad | Transfermarkt | https://www.transfermarkt.com/inter-milan/kader/verein/46 | Tier 1 | 2026-07-20 | medium | Position labels are visible, position IDs remain unknown. |  |
| Transfermarkt manual reference | Jersey coverage | Public squad pages include shirt-number references. | confirmed | fact | Detailed Squad | Transfermarkt | https://www.transfermarkt.com/inter-milan/kader/verein/46 | Tier 1 | 2026-07-20 | high | Completeness and historical coverage were not verified. |  |
| Transfermarkt manual reference | Player age | Public squad pages describe age as part of player information. | confirmed | fact | Detailed Squad | Transfermarkt | https://www.transfermarkt.com/inter-milan/kader/verein/46 | Tier 1 | 2026-07-20 | medium | Manual reference only; no individual values copied. |  |
| Transfermarkt manual reference | Market value | Public pages display player market values and an official definition explains their community-based expected-value methodology. | confirmed | fact | Market Value Definition | Transfermarkt | https://www.transfermarkt.com/navigation/mwdefinition | Tier 1 | 2026-07-20 | high | Market value is not an actual transfer fee and is not algorithmic. |  |
| Transfermarkt manual reference | Contract end date | Public squad pages describe contract duration or expiry as part of player information. | confirmed | fact | Detailed Squad | Transfermarkt | https://www.transfermarkt.com/inter-milan/kader/verein/46 | Tier 1 | 2026-07-20 | high | Accuracy and update cadence are not guaranteed publicly. |  |
| Transfermarkt manual reference | Salary context | No salary or compensation dataset was established in the reviewed official pages. | unknown | open-question | Transfermarkt Community | Transfermarkt | https://www.transfermarkt.com/intern/community | Tier 1 | 2026-07-20 | high | Market value must not be treated as salary. |  |
| Transfermarkt manual reference | League coverage | Transfermarkt describes a broad football database and multiple international domains, but no structured current coverage contract was found. | partial | fact | 20 Years of Transfermarkt Market Values | Transfermarkt | https://www.transfermarkt.com/20-years-of-transfermarkt-market-values-from-a-hobby-project-to-a-key-player-in-world-football/view/news/445167 | Tier 2 | 2026-07-20 | high | No exhaustive league list or field-depth guarantee was reviewed. |  |
| Transfermarkt manual reference | Freshness | Public community material describes profile, contract and market-value updates, but no guaranteed cadence was found. | partial | fact | Data Administration, Market Values and Watchlist | Transfermarkt | https://www.transfermarkt.com/data-administration-market-values-and-watchlist-become-a-part-of-the-transfermarkt-community/view/news/403373 | Tier 1 | 2026-07-20 | high | Update timing depends on editorial/community processes. |  |
| Transfermarkt manual reference | Provenance | Official material describes community discussion, volunteer data administration and review by data scouts. | partial | fact | Data Administration, Market Values and Watchlist | Transfermarkt | https://www.transfermarkt.com/data-administration-market-values-and-watchlist-become-a-part-of-the-transfermarkt-community/view/news/403373 | Tier 1 | 2026-07-20 | medium | Source lineage is not exposed per displayed field. |  |
| Transfermarkt manual reference | Market-value methodology | Official definition states values reflect expected demand under multiple factors and are not actual transfer fees. | confirmed | fact | Market Value Definition | Transfermarkt | https://www.transfermarkt.com/navigation/mwdefinition | Tier 1 | 2026-07-20 | medium | Methodology includes editorial/community judgment rather than reproducible computation. |  |
| Transfermarkt manual reference | Licensing clarity | Public terms reserve database/material rights and prohibit bots, spiders, screen scraping and other automated copying. | restricted | fact | Terms of Use | Transfermarkt | https://www.transfermarkt.com/intern/anb | Tier 1 | 2026-07-20 | high | Terms do not create a general automated-integration right. |  |
| Transfermarkt manual reference | Internal derived-use clarity | Public terms expressly restrict automated copying and text/data mining; manual internal-reference rights are not fully specified. | restricted | fact | Terms of Use | Transfermarkt | https://www.transfermarkt.com/intern/anb | Tier 1 | 2026-07-20 | high | Concrete reuse would require legal clarification. |  |
| Transfermarkt manual reference | Attribution requirements | No standalone public attribution framework for reused data was confirmed. | unknown | open-question | Terms of Use | Transfermarkt | https://www.transfermarkt.com/intern/anb | Tier 1 | 2026-07-20 | high | Unknown must not be read as permission without attribution. |  |
| Transfermarkt manual reference | Redistribution restrictions | Public terms reserve rights in the database and content and prohibit automated copying. | restricted | fact | Terms of Use | Transfermarkt | https://www.transfermarkt.com/intern/anb | Tier 1 | 2026-07-20 | high | Redistribution rights were not granted in reviewed terms. |  |
| Transfermarkt manual reference | Local/cache-first workflow fit | Manual page review can support a reviewed local-reference process, but automated cache-first ingestion is restricted. | partial | inference | Terms of Use | Transfermarkt | https://www.transfermarkt.com/intern/anb | Tier 1 | 2026-07-20 | high | Manual reference and automated integration must remain separate. |  |
| Transfermarkt manual reference | Identity mapping complexity | Visible labels and profile URL identifiers may support manual matching, but no official export or ID-mapping contract exists. | partial | inference | Data Administration, Market Values and Watchlist | Transfermarkt | https://www.transfermarkt.com/data-administration-market-values-and-watchlist-become-a-part-of-the-transfermarkt-community/view/news/403373 | Tier 1 | 2026-07-20 | medium | Manual review remains necessary. |  |
| Transfermarkt manual reference | Integration complexity | Automated integration is outside the approved boundary and publicly restricted; manual review is operationally separate. | restricted | fact | Terms of Use | Transfermarkt | https://www.transfermarkt.com/intern/anb | Tier 1 | 2026-07-20 | high | No API or automated extraction assumption is permitted. |  |
| Transfermarkt manual reference | Public pricing and plan limits | No public structured data/API plan applicable to this manual-reference assessment was confirmed. | unknown | open-question | Terms of Use | Transfermarkt | https://www.transfermarkt.com/intern/anb | Tier 1 | 2026-07-20 | high | Consumer or agent products are not evidence of data-integration rights. |  |

## Governance And Licensing

Public terms prohibit automated access and copying, including bots and screen scraping, and reserve database/content rights. The candidate remains bounded to manual reference; no automated integration or redistribution right is established.

## Identity And Labels

Names, club/competition labels and positions are publicly visible. Numeric URL identifiers may help manual matching, but their stability is not contractually documented.

## Position And Jersey Coverage

Public squad pages display positions and shirt-number references. No systematic completeness assessment or reusable position-ID contract was found.

## Market Context

Age, market value and contract information are publicly displayed. Market values are community/editorial expected values, not actual transfer fees. Salary remains unknown.

## Coverage And Freshness

The public database is broad, and update workflows are described, but no exhaustive current coverage list or guaranteed update cadence was found.

## Pricing And Public Plan Limits

No public data-integration plan relevant to this manual-reference role was confirmed. Account or agent-service products were not treated as data licenses.

## Technical And Local Workflow Fit

Manual review can fit the existing reviewed-CSV process. Automated extraction, caching and integration remain outside scope and restricted by public terms.

## Conflicts

- No material conflict among the reviewed official sources was recorded.

## Unknowns

- Salary context.
- Stable position IDs.
- Formal persistence of profile identifiers.
- Exhaustive league/field coverage.
- General attribution rule.
- Manual derived-use and redistribution boundary.
- Applicable structured-data pricing.

## Research Stop Conditions Encountered

- Automated access was explicitly prohibited and not attempted.
- No login or account-specific product was reviewed.
- No player-level values were copied into this evidence file.
- Reuse rights beyond manual reference remain unresolved.

## Candidate-Level Summary

Public evidence is sufficient for descriptive assessment as a manual source of labels, positions, age, market value and contract references. Evidence also clearly blocks an assumption of automated suitability. This summary does not recommend, rank, score or approve Transfermarkt.
