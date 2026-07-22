# v0.9.0 Provider Comparison Plan

## Status

- Milestone: v0.9.0
- Plan status: `provider-comparison-completed-docs-only`
- Related suitability scope plan: [v0.9.0 Provider Suitability Scope Plan](v0_9_0_provider_suitability_scope_plan.md)
- Related scope decision: [Sportmonks v0.9.0 Scope Decision](provider_decisions/sportmonks_v0_9_0_scope_decision.md)
- Related comparison scope decision: [v0.9.0 Provider Comparison Scope Decision](provider_decisions/v0_9_0_provider_comparison_scope_decision.md)
- Related public research protocol: [v0.9.0 Provider Public Research Protocol](v0_9_0_provider_public_research_protocol.md)
- Related protocol decision: [v0.9.0 Provider Public Research Protocol Decision](provider_decisions/v0_9_0_provider_public_research_protocol_decision.md)
- Selected path: compare providers
- Research protocol: approved / executed
- No-scoring policy: selected
- Comparison performed: yes, descriptive only
- Public web research performed: yes, in the completed approved research block
- Public evidence pass: completed
- Evidence completeness review: completed
- Descriptive comparison: sufficient
- Qualitative recommendation protocol design: permitted with limitations
- Qualitative recommendation protocol: fulfilled
- Qualitative outcomes: completed
- v0.9.0 closeout: completed docs-only
- Numeric scoring: blocked
- Provider access performed: no
- API calls performed: no
- Cache reading performed: no
- Provider approval: none
- No future provider path selected: yes
- Next: separate release/tag block

## Goal

v0.9.0 will compare the suitability of already documented provider candidates before allowing deeper Sportmonks work.

The comparison must help decide:

- whether Sportmonks deserves further investigation;
- whether another candidate covers the unresolved gaps better;
- whether a combined solution is appropriate;
- or whether provider exploration should stop.

This plan does not evaluate or score the candidates.

## Candidate Set

| Candidate | Intended Comparison Role | Current Status |
|---|---|---|
| Sportmonks | Main candidate carried over from v0.8.0 | explored / unapproved |
| API-Football / API-Sports | Existing football statistics source and comparison baseline | existing offline integration, not approved for Market Context |
| Capology | Salary and contract context candidate | review-only / unapproved |
| Transfermarkt manual reference | Manual market value and contract reference candidate | manual-reference-only / unapproved |

- No new candidate is added in this block.
- Transfermarkt is evaluated only as a manual reference, not as an API or scraping target.
- The existing API-Football statistics integration does not imply approval for Market Context.
- Sportmonks receives no preference because a local scaffold already exists.

## Comparison Questions

### Identity and usability

- Can the candidate provide stable player IDs?
- Can it provide human-readable player labels?
- Can it provide team and competition labels?
- Can it provide reliable position IDs or position labels?
- Can it provide jersey numbers with useful coverage?

### Market Context

- Can it provide player age?
- Can it provide market value?
- Can it provide contract end date?
- Can it provide salary or compensation context?
- Are those fields suitable for Opportunity Finder?

### Technical suitability

- Can data be normalized into the current canonical model?
- Can it work in a local-first or cache-first workflow?
- Does it support reproducible identity mapping?
- Is provenance available?
- Is freshness clear?
- Can it be evaluated without app or SQLite integration?

### Governance and licensing

- Is public documentation sufficient to understand permitted use?
- Are local evaluation and derived internal outputs permitted?
- Is attribution required?
- Is redistribution restricted?
- Are raw payloads allowed to remain local?
- Is provider approval still required before integration?

### Practical suitability

- Is relevant league coverage available?
- Is the available plan sufficient for meaningful evaluation?
- Are essential fields bundled or split across endpoints?
- Would combining providers create unacceptable mapping complexity?
- Does the candidate solve enough gaps to justify further work?

## Comparison Criteria

| Criterion | Description | Weight Status |
|---|---|---|
| Identity stability | Stable player/team/competition identifiers | weight pending |
| Human-readable labels | Player, team and position labels | weight pending |
| Position and jersey coverage | Populated and reliable squad fields | weight pending |
| Market value | Availability and provenance | weight pending |
| Contract context | Contract end and related context | weight pending |
| Salary context | Availability, reliability and permitted use | weight pending |
| League coverage | Relevant competition coverage | weight pending |
| Freshness | Update cadence and observable dates | weight pending |
| Licensing clarity | Permitted evaluation and internal derived use | weight pending |
| Local workflow fit | Cache-first and offline evaluation suitability | weight pending |
| Integration complexity | Mapping and normalization effort | weight pending |
| Cost and plan limits | Current public plan suitability | weight pending |

- No weights are selected in this block.
- No scores are assigned in this block.
- Cost, plans and licensing facts must be verified from current public sources in a later approved research block.

## Future Research Source Rules

Future research, if separately approved, must:

- prioritize official provider documentation;
- use public pages;
- record the consultation date;
- summarize terms instead of copying extensive legal text;
- distinguish confirmed facts from inferences;
- record unknown fields as `unknown`;
- avoid affiliate blogs as primary sources;
- not sign in;
- not use private dashboards;
- not create accounts;
- not make API calls;
- not download payloads;
- not use credentials;
- not read provider cache;
- not perform automated scraping.

Secondary sources may be used only for context and must be clearly identified.

## Completed Research Artifacts And Next Decision

The approved research block created:

- Public evidence notes for each candidate.
- A descriptive comparison matrix.
- A public research summary.
- An evidence completeness review and decision record.

The qualitative role recommendation and closeout are completed. No scoring, ranking, universal winner, implementation or provider approval was produced.

## Approved Qualitative Outcome Vocabulary

- `continue-targeted-clarification`
- `technical-baseline-only`
- `manual-reference-only`
- `defer`
- `stop-exploration`
- `separate-role-candidate`

The vocabulary defines the completed role-based outcomes only. It does not authorize scoring, ranking, implementation or provider approval.

## Stop Conditions

- The comparison requires API calls.
- Current facts cannot be verified from public sources.
- A source requires login or account access.
- Legal or licensing text is ambiguous.
- Raw payload inspection becomes necessary.
- Provider cache reading becomes necessary.
- A new provider is proposed without a separate scope decision.
- Scoring begins before weights and evidence rules are approved.
- Any candidate is described as approved.

## Next Required Action

Commit the docs-only closeout. After commit and clean status, a separate release/tag block may create the v0.9.0 tag and GitHub release.

No future provider path is selected. Numeric scoring, ranking, implementation and provider approval remain blocked.
