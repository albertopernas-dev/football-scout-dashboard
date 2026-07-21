# v0.9.0 Qualitative Provider Recommendation Protocol

## Status

- Milestone: v0.9.0
- Protocol status: `qualitative-recommendation-protocol-defined`
- Related evidence completeness review: [v0.9.0 Provider Evidence Completeness Review](v0_9_0_evidence_completeness_review.md)
- Related completeness decision: [v0.9.0 Provider Evidence Completeness Review Decision](../provider_decisions/v0_9_0_provider_evidence_completeness_review_decision.md)
- Related recommendation protocol decision: [v0.9.0 Qualitative Provider Recommendation Protocol Decision](../provider_decisions/v0_9_0_qualitative_recommendation_protocol_decision.md)
- Candidate set locked: yes
- Recommendation execution approved: no
- Numeric scoring approved: no
- Weights approved: no
- Ranking approved: no
- Universal winner approved: no
- New research approved: no
- Provider approval: none
- Implementation approved: no

## Purpose

This protocol defines how a future docs-only block may produce a qualitative, role-based recommendation from the existing evidence.

It does not execute that recommendation.

The protocol must preserve:

- Candidate-specific roles.
- Unknowns.
- Conflicts.
- Licensing limits.
- Manual versus automated boundaries.
- Separation between technical capability and permitted use.

## Locked Inputs

Use only:

- `docs/provider_comparison/evidence/sportmonks_public_evidence.md`
- `docs/provider_comparison/evidence/api_football_public_evidence.md`
- `docs/provider_comparison/evidence/capology_public_evidence.md`
- `docs/provider_comparison/evidence/transfermarkt_manual_public_evidence.md`
- `docs/provider_comparison/v0_9_0_provider_comparison_matrix.md`
- `docs/provider_comparison/v0_9_0_public_research_summary.md`
- `docs/provider_comparison/v0_9_0_evidence_completeness_review.md`
- `docs/provider_decisions/v0_9_0_provider_evidence_completeness_review_decision.md`

No new sources or facts may be added.

## Evidence Hierarchy

Apply this order:

1. Confirmed Tier 1 facts.
2. Confirmed limitations and restrictions.
3. Partial findings.
4. Conflicting findings.
5. Advertised findings.
6. Unknowns.
7. Inferences.

Rules:

- `confirmed` does not imply approved.
- `advertised` cannot override `partial`, `restricted`, `conflicting` or `unknown`.
- `unknown` must remain unknown.
- `restricted` must be treated as a hard boundary unless separately clarified.
- `conflicting` must remain unresolved.
- An inference cannot override a confirmed fact or restriction.
- Existing technical work cannot substitute for current suitability evidence.

## Candidate Roles

| Candidate | Approved Comparison Role |
|---|---|
| Sportmonks | Automated-provider candidate under clarification |
| API-Football / API-Sports | Existing technical/statistics baseline and possible limited context candidate |
| Capology | Salary and contract context candidate under agreement clarification |
| Transfermarkt manual reference | Manual-reference-only candidate |

- Candidate roles are not rankings.
- Candidates do not compete for one universal role.
- A future recommendation may produce different outcomes for different roles.

## Allowed Recommendation Outcomes

### `continue-targeted-clarification`

Use when evidence suggests material potential, but provider-specific licensing, field population, plan availability or technical questions must be clarified before any next step.

### `technical-baseline-only`

Use when the candidate is useful as an existing technical/statistical baseline but does not currently demonstrate Market Context suitability.

### `manual-reference-only`

Use when the candidate is useful only within a reviewed manual workflow and automated access or integration is not permitted or supported.

### `defer`

Use when evidence is insufficient to justify either continuation or rejection, and no immediate follow-up is approved.

### `stop-exploration`

Use when the candidate does not fit the required role or its restrictions make further evaluation unjustified under the project boundary.

### `separate-role-candidate`

Use when the candidate may suit a narrow role such as salary/contract context but cannot be treated as a complete provider solution.

- No outcome means provider approval.
- No outcome authorizes API calls, implementation, trial or provider access.
- A candidate may receive more than one compatible role-specific outcome only when clearly separated.
- `manual-reference-only` and automated-provider outcomes cannot be conflated.

## Decision Questions

For each candidate, the future execution must answer:

1. What role is actually supported by the evidence?
2. Which required criteria are confirmed?
3. Which material criteria remain unknown, restricted or conflicting?
4. Does the candidate solve a meaningful project gap?
5. What governance boundary prevents immediate use?
6. Is a narrow clarification step justified?
7. Should exploration continue, defer or stop?
8. What remains explicitly unapproved?

## Candidate-Specific Rules

### Sportmonks

The future recommendation must consider:

- Documented identity, labels, positions and contract-end field.
- Unknown market value and salary.
- Untested field population.
- Incomplete derived-use and licensing clarity.
- Existing local scaffold without treating it as approval.

Allowed outcomes:

- `continue-targeted-clarification`
- `defer`
- `stop-exploration`

Not allowed:

- Provider approval.
- Implementation recommendation.
- Universal winner.

### API-Football / API-Sports

The future recommendation must consider:

- Existing statistics baseline.
- Documented identity, labels and age.
- Unknown market value, contract end and salary.
- Unresolved cache, redistribution and derived-use rights.
- Separation between statistics integration and Market Context.

Allowed outcomes:

- `technical-baseline-only`
- `continue-targeted-clarification`
- `defer`
- `stop-exploration`

### Capology

The future recommendation must consider:

- Documented salary and contract role.
- Estimate and source-certainty limitations.
- Unknown market value and jersey coverage.
- Agreement-specific cache, derived-use and publication rights.

Allowed outcomes:

- `separate-role-candidate`
- `continue-targeted-clarification`
- `defer`
- `stop-exploration`

### Transfermarkt manual reference

The future recommendation must consider:

- Visible labels, positions, age, market value and contract references.
- Automated-use restrictions.
- No approved automated integration role.

Allowed outcomes:

- `manual-reference-only`
- `defer`
- `stop-exploration`

Not allowed:

- Automated-provider recommendation.
- API assumption.
- Scraping or integration recommendation.

## Cross-Candidate Rules

- Do not select a universal winner.
- Do not rank candidates.
- Do not convert unknowns into disadvantages numerically.
- Do not treat broader coverage as automatically superior.
- Do not compare manual and automated roles as equivalent.
- Do not recommend a multi-provider architecture.
- Do not recommend implementation.
- Do not use existing sunk work as a reason to favor Sportmonks.
- Do not use existing API-Football integration as Market Context approval.
- Do not treat Capology estimates as official contracts.
- Do not treat Transfermarkt market values as objective transfer fees.

## Qualitative Decision Structure

The future recommendation must include these exact second-level sections:

- `## Status`
- `## Evidence Boundary`
- `## Candidate Outcomes`
- `## Cross-Candidate Interpretation`
- `## Clarification Candidates`
- `## Deferred Or Stopped Paths`
- `## Manual-Reference Boundary`
- `## Safety And Governance Boundary`
- `## Final Qualitative Conclusion`
- `## Next Decision Boundary`

The `## Candidate Outcomes` section must use this table:

| Candidate | Supported Role | Qualitative Outcome | Evidence Basis | Blocking Unknowns | Explicitly Not Approved |
|---|---|---|---|---|---|

## Prohibited Language

Do not use:

- best provider;
- winner;
- top-ranked;
- score;
- weighted;
- approved;
- production-ready;
- integration-ready;
- complete solution;
- objectively better.

These terms may appear only to explicitly deny those states.

## Future Approved Files

A future execution block, if separately approved, may create only:

- `docs/provider_comparison/v0_9_0_qualitative_recommendation.md`
- `docs/provider_decisions/v0_9_0_qualitative_recommendation_decision.md`

Do not create those files in this block.

## Stop Conditions

Stop the future execution if:

- New research appears necessary.
- A fact appears that is not contained in the locked inputs.
- A score is proposed.
- Candidates are ordered.
- A winner is selected.
- Provider approval is proposed.
- Implementation is recommended.
- A multi-provider architecture is recommended.
- A conclusion requires interpretation of ambiguous legal terms.
- A candidate requires access, API, cache or trial to support the conclusion.

In those cases, record one of the following according to the existing evidence:

- `continue-targeted-clarification`
- `defer`
- `stop-exploration`

## Next Required Action

A separate docs-only decision may approve execution of this qualitative recommendation protocol.

That future execution may create only the two approved recommendation files and must not perform new research, scoring, ranking, implementation design or provider approval.
