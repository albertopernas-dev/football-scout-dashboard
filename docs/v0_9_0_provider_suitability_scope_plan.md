# v0.9.0 Provider Suitability Scope Plan

## Status

- Milestone: v0.9.0
- Status: completed / closed docs-only
- Related v0.8.0 closeout decision: [Sportmonks v0.8.0 Closeout Decision](provider_decisions/sportmonks_v0_8_0_closeout_decision.md)
- Related v0.8.0 release notes: [Release Notes v0.8.0](release_notes_v0_8_0.md)
- Related provider comparison plan: [v0.9.0 Provider Comparison Plan](v0_9_0_provider_comparison_plan.md)
- Related comparison scope decision: [v0.9.0 Provider Comparison Scope Decision](provider_decisions/v0_9_0_provider_comparison_scope_decision.md)
- Related public research protocol: [v0.9.0 Provider Public Research Protocol](v0_9_0_provider_public_research_protocol.md)
- Sportmonks provider approval: no
- Selected evaluation path: `Compare providers`
- Selected evaluation path status: completed
- Public research protocol: fulfilled
- Final outcomes: Sportmonks `continue-targeted-clarification`; API-Football / API-Sports `technical-baseline-only`; Capology `separate-role-candidate`; Transfermarkt manual reference `manual-reference-only`
- Selected implementation path: none
- API calls approved: no
- Raw JSON review approved: no
- Additional cache reading approved: no
- `.local.csv` approved: no
- SQLite approved: no
- Streamlit approved: no
- Local trial approved: no

## Context From v0.8.0

- v0.8.0 completed permission handling and governance.
- A local-only Sportmonks scaffold was implemented.
- One aggregate local preview completed.
- Preview result:
  - `row_count 6`
  - `has_position_ids 0`
  - `has_jersey_numbers 0`
- The preview validated technical transformation only.
- Sportmonks remains unapproved.
- Labels, positions, jersey coverage and Market Context remain unresolved.

## v0.9.0 Goal

v0.9.0 is intended to decide whether Sportmonks exploration should continue and, if so, under which controlled path.

No implementation is selected by this plan.

## Candidate Paths

| Path | Description | Risk | Potential Value | Approval Status |
|---|---|---|---|---|
| Stop Sportmonks exploration | Archive candidate as explored but insufficient for now | low | avoids wasting work | not selected |
| Label lookup strategy | Investigate how to resolve player and position labels safely | medium | improves human usability | not approved |
| Richer endpoint review | Evaluate whether another Sportmonks endpoint can provide better fields | medium/high | may unlock Market Context or richer identity | not approved |
| Local trial design | Design an ignored local trial with derived output only | high | closer to provider suitability evidence | not approved |
| Compare providers | Compare Sportmonks against another candidate before continuing | medium | avoids provider lock-in | completed docs-only |

## Recommended Evaluation Questions

- Can Sportmonks provide human-readable player labels without unsafe broad payload exposure?
- Can Sportmonks provide position labels or reliable position IDs?
- Can Sportmonks provide jersey coverage reliably?
- Can Sportmonks provide Market Context fields needed by Opportunity Finder?
- Would another provider solve these gaps with less governance risk?
- Is the free plan scope sufficient for meaningful evaluation?
- What would be the minimum safe next action?

## Out Of Scope

- API calls.
- Manual raw JSON review.
- Additional cache reading.
- Broad payload inspection.
- `.local.csv` creation.
- SQLite writes.
- Streamlit integration.
- Local trial.
- App integration.
- Provider approval.
- Production usage.
- Release/tag.

## Public Research Protocol Status

The public-source comparison research protocol was fulfilled. The evidence review, qualitative recommendation and v0.9.0 closeout are completed docs-only.

The final role outcomes are recorded without scoring, ranking, a universal winner, implementation or provider approval.

Implementation path remains none, and no future provider path is selected.

## Recommended Next Action

Commit the docs-only closeout, then use a separate release/tag block for v0.9.0.

`Compare providers` is completed. No login, private dashboard access, API calls, cache reading, raw JSON review, automated scraping, scoring, implementation or provider approval is authorized.
