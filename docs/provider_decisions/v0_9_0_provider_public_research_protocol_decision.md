# v0.9.0 Provider Public Research Protocol Decision

## Status

- Milestone: v0.9.0
- Decision status: `public-source-research-protocol-fulfilled`
- Related research protocol: [v0.9.0 Provider Public Research Protocol](../v0_9_0_provider_public_research_protocol.md)
- Related comparison plan: [v0.9.0 Provider Comparison Plan](../v0_9_0_provider_comparison_plan.md)
- Related comparison scope decision: [v0.9.0 Provider Comparison Scope Decision](v0_9_0_provider_comparison_scope_decision.md)
- Candidate set: locked
- Future public web research approved: no, the approved block has been completed
- Research executed: yes
- Evidence completeness review completed: yes
- Existing protocol fulfilled: yes
- Numeric scoring approved: no
- Ranking approved: no
- Recommendation approved: no
- Login or dashboard access approved: no
- API calls approved: no
- Provider cache reading approved: no
- Automated scraping approved: no
- Implementation approved: no
- Provider approval: none

## Decision

- The approved public-source research block was executed under the protocol.
- Research remained restricted to the four locked candidates.
- Official public sources were prioritized.
- Current facts were verified during the completed research block.
- Evidence used the approved classifications.
- The completed block created only the six approved evidence, matrix and summary files.
- The completed block did not score, rank, recommend or approve a provider.

## Locked Candidate Set

1. Sportmonks.
2. API-Football / API-Sports.
3. Capology.
4. Transfermarkt as a manual reference only.

## Approved Future Files

- `docs/provider_comparison/evidence/sportmonks_public_evidence.md`
- `docs/provider_comparison/evidence/api_football_public_evidence.md`
- `docs/provider_comparison/evidence/capology_public_evidence.md`
- `docs/provider_comparison/evidence/transfermarkt_manual_public_evidence.md`
- `docs/provider_comparison/v0_9_0_provider_comparison_matrix.md`
- `docs/provider_comparison/v0_9_0_public_research_summary.md`

Any additional file requires another decision.

## Approved Research Access

Allowed:

- Public official documentation.
- Public official pricing and plans.
- Public official coverage pages.
- Public terms and licensing pages.
- Public help centres and FAQs.
- Limited secondary context, clearly marked.

Forbidden:

- Login.
- Account creation.
- Private dashboards.
- API calls.
- SDKs.
- Cache reading.
- Raw JSON.
- Automated scraping.
- Downloaded payloads.
- Credentials.

## Evidence And Comparison Policy

- Evidence classifications only.
- No numeric score.
- No weights.
- No ranking.
- No winner.
- Unknown remains unknown.
- Marketing claims remain `advertised` unless supported technically.
- Conflicts must be recorded.
- A candidate cannot be described as approved.

## Still Forbidden

- API calls.
- Provider login.
- Account creation.
- Private dashboard access.
- Provider cache reading.
- Manual raw JSON review.
- Automated scraping.
- Payload downloads.
- `.local.csv`.
- SQLite writes.
- Streamlit integration.
- Local trial.
- App integration.
- Numeric scoring.
- Ranking.
- Recommendation.
- Provider approval.
- Release/tag.

## Next Required Action

A separate docs-only decision may define a qualitative recommendation protocol.

No further research is automatically approved. Numeric scoring, ranking, recommendation execution, implementation and provider approval remain blocked.
