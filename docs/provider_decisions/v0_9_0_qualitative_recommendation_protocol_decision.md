# v0.9.0 Qualitative Provider Recommendation Protocol Decision

## Status

- Milestone: v0.9.0
- Decision status: `qualitative-recommendation-protocol-approved`
- Related protocol: [v0.9.0 Qualitative Provider Recommendation Protocol](../provider_comparison/v0_9_0_qualitative_recommendation_protocol.md)
- Related completeness review: [v0.9.0 Provider Evidence Completeness Review](../provider_comparison/v0_9_0_evidence_completeness_review.md)
- Related completeness decision: [v0.9.0 Provider Evidence Completeness Review Decision](v0_9_0_provider_evidence_completeness_review_decision.md)
- Candidate set: locked
- Qualitative recommendation protocol approved: yes
- Recommendation execution approved: no
- New research approved: no
- Numeric scoring approved: no
- Ranking approved: no
- Universal winner approved: no
- Provider approval: none
- Implementation approved: no

## Decision

- The qualitative recommendation protocol is approved.
- The protocol uses only existing committed evidence.
- Recommendation execution remains a separate future block.
- Recommendation must remain role-based.
- No candidate may be ranked or declared a universal winner.
- Transfermarkt remains manual-reference-only.
- API-Football remains a technical/statistics baseline unless separately clarified.
- Capology remains a separate-role candidate subject to agreement clarification.
- Sportmonks remains an automated-provider candidate under clarification.
- No provider is recommended or approved in this block.

## Approved Outcome Vocabulary

- `continue-targeted-clarification`
- `technical-baseline-only`
- `manual-reference-only`
- `defer`
- `stop-exploration`
- `separate-role-candidate`

No additional outcome is allowed without another decision.

## Approved Future Files

- `docs/provider_comparison/v0_9_0_qualitative_recommendation.md`
- `docs/provider_decisions/v0_9_0_qualitative_recommendation_decision.md`

Any additional file requires another decision.

## Still Forbidden

- New web research.
- New sources.
- Login.
- Account creation.
- Private dashboards.
- API calls.
- Provider cache reading.
- Raw JSON review.
- Automated scraping.
- Payload downloads.
- `.local.csv`.
- SQLite writes.
- Streamlit integration.
- Local trial.
- App integration.
- Numeric scoring.
- Weights.
- Ranking.
- Universal winner.
- Recommendation execution until separately approved.
- Provider approval.
- Implementation.
- Release/tag.

## Next Required Action

A later docs-only block may approve execution of the qualitative recommendation protocol.

No recommendation is made by this decision.
