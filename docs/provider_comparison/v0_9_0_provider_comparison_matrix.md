# v0.9.0 Provider Comparison Matrix

## Status

- Milestone: v0.9.0
- Matrix status: `public-evidence-pass-completed`
- Evidence pass complete: yes, subject to recorded unknowns
- Numeric scoring: not approved
- Ranking: not approved
- Recommendation: not approved
- Provider approval: none

## Classification Legend

- `confirmed`
- `advertised`
- `partial`
- `unknown`
- `not-available`
- `not-applicable`
- `restricted`
- `conflicting`

## Comparison Matrix

| Criterion | Sportmonks | API-Football / API-Sports | Capology | Transfermarkt manual reference | Evidence Notes |
|---|---|---|---|---|---|
| Stable player IDs | confirmed — Sportmonks evidence: Identity And Labels | confirmed — API-Football evidence: Identity And Labels | confirmed — Capology evidence: Identity And Labels | partial — Transfermarkt evidence: Identity And Labels | Persistence guarantees differ or remain unstated. |
| Human-readable player labels | confirmed — Sportmonks evidence: Identity And Labels | confirmed — API-Football evidence: Identity And Labels | confirmed — Capology evidence: Identity And Labels | confirmed — Transfermarkt evidence: Identity And Labels | Population and spelling consistency were not tested. |
| Team and competition labels | advertised — Sportmonks evidence: Identity And Labels | confirmed — API-Football evidence: Identity And Labels | confirmed — Capology evidence: Identity And Labels | confirmed — Transfermarkt evidence: Identity And Labels | Sportmonks support is publicly advertised but not verified across leagues. |
| Position IDs | confirmed — Sportmonks evidence: Position And Jersey Coverage | partial — API-Football evidence: Position And Jersey Coverage | partial — Capology evidence: Position And Jersey Coverage | partial — Transfermarkt evidence: Position And Jersey Coverage | Detailed, stable taxonomies are not equally documented. |
| Position labels | confirmed — Sportmonks evidence: Position And Jersey Coverage | confirmed — API-Football evidence: Position And Jersey Coverage | partial — Capology evidence: Position And Jersey Coverage | confirmed — Transfermarkt evidence: Position And Jersey Coverage | Capology documents broad groups rather than detailed roles. |
| Jersey coverage | partial — Sportmonks evidence: Position And Jersey Coverage | partial — API-Football evidence: Position And Jersey Coverage | unknown — Capology evidence: Position And Jersey Coverage | confirmed — Transfermarkt evidence: Position And Jersey Coverage | Completeness was not measured for any candidate. |
| Age | partial — Sportmonks evidence: Market Context | confirmed — API-Football evidence: Market Context | confirmed — Capology evidence: Market Context | confirmed — Transfermarkt evidence: Market Context | Sportmonks documents birth date rather than a direct age guarantee. |
| Market value | unknown — Sportmonks evidence: Market Context | unknown — API-Football evidence: Market Context | unknown — Capology evidence: Market Context | confirmed — Transfermarkt evidence: Market Context | Transfermarkt values are expected values, not transfer fees. |
| Contract end date | confirmed — Sportmonks evidence: Market Context | unknown — API-Football evidence: Market Context | confirmed — Capology evidence: Market Context | confirmed — Transfermarkt evidence: Market Context | Sportmonks and Capology document contract-end fields, but population and accuracy were not verified. |
| Salary context | unknown — Sportmonks evidence: Market Context | unknown — API-Football evidence: Market Context | confirmed — Capology evidence: Market Context | unknown — Transfermarkt evidence: Market Context | Capology salaries are estimates, including verified entries. |
| Relevant league coverage | conflicting — Sportmonks evidence: Coverage And Freshness | partial — API-Football evidence: Coverage And Freshness | confirmed — Capology evidence: Coverage And Freshness | partial — Transfermarkt evidence: Coverage And Freshness | Exact field depth and current coverage remain time-sensitive. |
| Freshness | partial — Sportmonks evidence: Coverage And Freshness | partial — API-Football evidence: Coverage And Freshness | confirmed — Capology evidence: Coverage And Freshness | partial — Transfermarkt evidence: Coverage And Freshness | Published cadences differ and do not guarantee field completeness. |
| Provenance | advertised — Sportmonks evidence: Governance And Licensing | unknown — API-Football evidence: Governance And Licensing | partial — Capology evidence: Governance And Licensing | partial — Transfermarkt evidence: Governance And Licensing | None exposes complete field-level lineage publicly. |
| Licensing clarity | partial — Sportmonks evidence: Governance And Licensing | partial — API-Football evidence: Governance And Licensing | restricted — Capology evidence: Governance And Licensing | restricted — Transfermarkt evidence: Governance And Licensing | Concrete downstream use still needs provider-specific review. |
| Internal derived-use clarity | partial — Sportmonks evidence: Governance And Licensing | unknown — API-Football evidence: Governance And Licensing | unknown — Capology evidence: Governance And Licensing | restricted — Transfermarkt evidence: Governance And Licensing | Technical availability is separate from permitted use. |
| Attribution requirements | partial — Sportmonks evidence: Governance And Licensing | unknown — API-Football evidence: Governance And Licensing | unknown — Capology evidence: Governance And Licensing | unknown — Transfermarkt evidence: Governance And Licensing | Asset attribution and data attribution must not be conflated. |
| Redistribution restrictions | restricted — Sportmonks evidence: Governance And Licensing | unknown — API-Football evidence: Governance And Licensing | restricted — Capology evidence: Governance And Licensing | restricted — Transfermarkt evidence: Governance And Licensing | No candidate has a confirmed unrestricted redistribution grant. |
| Local workflow fit | partial — Sportmonks evidence: Technical And Local Workflow Fit | partial — API-Football evidence: Technical And Local Workflow Fit | unknown — Capology evidence: Technical And Local Workflow Fit | partial — Transfermarkt evidence: Technical And Local Workflow Fit | Transfermarkt fit is manual only; cache rights remain unresolved elsewhere. |
| Identity mapping complexity | partial — Sportmonks evidence: Technical And Local Workflow Fit | partial — API-Football evidence: Technical And Local Workflow Fit | partial — Capology evidence: Technical And Local Workflow Fit | partial — Transfermarkt evidence: Technical And Local Workflow Fit | Cross-provider matching remains a reviewed process. |
| Integration complexity | partial — Sportmonks evidence: Technical And Local Workflow Fit | partial — API-Football evidence: Technical And Local Workflow Fit | partial — Capology evidence: Technical And Local Workflow Fit | restricted — Transfermarkt evidence: Technical And Local Workflow Fit | Manual and automated boundaries materially differ. |
| Public pricing / plan limits | confirmed — Sportmonks evidence: Pricing And Public Plan Limits | confirmed — API-Football evidence: Pricing And Public Plan Limits | confirmed — Capology evidence: Pricing And Public Plan Limits | unknown — Transfermarkt evidence: Pricing And Public Plan Limits | Pricing and plan content require revalidation when used. |

## Cross-Provider Combination Risks

- Identity mapping: candidate-specific IDs require reviewed crosswalks; visible names alone are insufficient.
- Freshness mismatch: provider cadences range from near-live or weekly API updates to periodic editorial updates.
- Licensing incompatibility: publishing, redistribution, storage and automated-use rules differ and may prevent a combined automated dataset.
- Provenance mismatch: provider-level source descriptions do not provide a uniform field-level lineage model.
- Duplicate or conflicting fields: age, position, contract and value fields can disagree without a shared value date or source hierarchy.
- Operational maintenance: multiple providers increase schema, monitoring, refresh and conflict-resolution work.
- Manual versus automated boundaries: Transfermarkt is assessed only as a manual reference, while API candidates expose structured interfaces under separate restrictions.

## Material Unknowns

- Sportmonks market value, salary and exact internal derived-use boundaries.
- API-Football/API-Sports market value, contract end, salary, cache rights and redistribution.
- Capology market value, jersey coverage, cache rights and agreement-specific derived use.
- Transfermarkt salary, formal ID persistence, attribution and any reusable structured-data license.
- Cross-provider field precedence, value dates and conflict-resolution policy.

## Conflicts

- Sportmonks official pages use different headline league totals.
- API-Football pricing breadth is qualified by terms stating that actual data availability varies by competition.
- Capology documents contract-expiry fields while stating that it lacks official access to player contracts for confirmation.
- No material conflict was recorded for Transfermarkt within the reviewed public sources.

## Evidence Completeness

- Sportmonks: partial.
- API-Football / API-Sports: materially incomplete for Market Context and downstream-use rights.
- Capology: complete enough for descriptive comparison of its salary/contract role, subject to agreement-specific unknowns.
- Transfermarkt manual reference: complete enough for descriptive comparison of its manual-reference role, subject to automated-use restrictions.

These completeness labels describe evidence coverage only. They are not scores or rankings.

## Next Decision Boundary

No winner is selected. No provider is recommended. No provider is approved.

Evidence completeness must be reviewed in a separate docs-only decision before recommendation, scoring design, additional research, provider access or implementation.
