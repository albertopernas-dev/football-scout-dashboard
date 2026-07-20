# v0.9.0 Public Provider Research Summary

## Status

- Milestone: v0.9.0
- Research status: `public-evidence-pass-completed`
- Consultation date range: 2026-07-20
- Candidate set: locked
- Evidence files created: 4
- Comparison matrix created: yes
- Numeric scoring performed: no
- Ranking performed: no
- Recommendation made: no
- Provider approval: none
- Login used: no
- API calls: no
- Cache reading: no
- Raw JSON: no
- Automated scraping: no

## Sources Reviewed

### Sportmonks

- Official sources: 9.
- Secondary sources: 0.
- Page types: public API documentation, squad/lineup documentation, product and coverage pages, pricing, FAQ, caching guidance and terms.

### API-Football / API-Sports

- Official sources: 3.
- Secondary sources: 0.
- Page types: public football API documentation, public pricing and public terms.

### Capology

- Official sources: 7.
- Secondary sources: 0.
- Page types: public player/contract/salary API documentation, pricing, methodology/features and help/FAQ.

### Transfermarkt Manual Reference

- Official sources: 6.
- Secondary sources: 0.
- Page types: public terms, market-value methodology, community/data-administration material and public squad-page structure.

All consulted URLs and consultation dates are recorded in the candidate evidence files.

## Research Coverage

| Candidate | Governance | Identity | Position/Jersey | Market Context | Coverage/Freshness | Pricing/Plans | Overall Evidence Completeness |
|---|---|---|---|---|---|---|---|
| Sportmonks | partial | complete | partial | materially incomplete | partial | complete | partial |
| API-Football / API-Sports | partial | complete | partial | materially incomplete | partial | complete | materially incomplete |
| Capology | partial | complete | partial | partial | complete | complete | complete |
| Transfermarkt manual reference | partial | partial | partial | partial | partial | materially incomplete | complete |

`Complete` means complete enough for descriptive comparison within the candidate's stated role. It does not mean implementation-ready or approved.

## Cross-Candidate Findings

- The candidates cover different categories rather than one uniform Market Context package.
- Stable identity and readable labels are better documented than downstream-use rights.
- Market value is publicly established only for the manual-reference candidate in this evidence pass.
- Salary and structured contract context are publicly documented for Capology, with explicit estimate and licensing limitations.
- Contract end is publicly documented for Sportmonks, Capology and Transfermarkt manual reference; Sportmonks field population and reliability were not tested.
- Age is documented more broadly than market value, contract end or salary.
- Combining sources would require reviewed identity mapping, value dates, provenance and conflict rules.
- Technical availability and permitted use remain separate questions.

## Material Unknowns

- No single candidate has confirmed coverage for every identity, jersey and Market Context criterion.
- Internal derived-use, cache, attribution and redistribution rights remain incomplete or restricted.
- Market value is not publicly established for Sportmonks, API-Football/API-Sports or Capology.
- Contract end is not publicly established for API-Football / API-Sports. Sportmonks publicly documents a contract-end field, but its population and reliability were not tested.
- Salary context is not publicly established for Sportmonks, API-Football/API-Sports or Transfermarkt.
- Exact per-league field completeness remains incomplete.

## Conflicts

- Sportmonks public pages show different league totals.
- API-Football plan breadth is qualified by competition-level availability warnings.
- Capology exposes contract-expiration fields while qualifying that contracts are not available for official confirmation.
- No material Transfermarkt conflict was found in the reviewed official sources.

## Stop Conditions Encountered

- Account-specific or private plan details were not reviewed.
- API field population was not tested.
- Provider-specific agreement terms unavailable publicly were recorded as unknown.
- Automated Transfermarkt use was not explored because public terms prohibit automated copying.
- No new candidate was added.

## Files Created

- `docs/provider_comparison/evidence/sportmonks_public_evidence.md`
- `docs/provider_comparison/evidence/api_football_public_evidence.md`
- `docs/provider_comparison/evidence/capology_public_evidence.md`
- `docs/provider_comparison/evidence/transfermarkt_manual_public_evidence.md`
- `docs/provider_comparison/v0_9_0_provider_comparison_matrix.md`
- `docs/provider_comparison/v0_9_0_public_research_summary.md`

## Safety Confirmation

- No login.
- No account creation.
- No private dashboard.
- No API calls.
- No provider cache.
- No raw JSON.
- No automated scraping.
- No payload downloads.
- No credentials or `.env`.
- No individual player data copied.
- No code or tests.
- No scoring or ranking.
- No recommendation.
- No provider approval.

## Next Required Action

A separate docs-only evidence-completeness review decision is required before any recommendation, scoring design, additional research, provider access or implementation.
