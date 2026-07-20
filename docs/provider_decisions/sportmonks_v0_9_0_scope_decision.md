# Sportmonks v0.9.0 Scope Decision

## Status

- Candidate: Sportmonks
- Milestone: v0.9.0
- Decision status: `scope-opened-provider-suitability`
- Related v0.9.0 scope plan: [v0.9.0 Provider Suitability Scope Plan](../v0_9_0_provider_suitability_scope_plan.md)
- Related v0.8.0 closeout decision: [Sportmonks v0.8.0 Closeout Decision](sportmonks_v0_8_0_closeout_decision.md)
- Related comparison scope decision: [v0.9.0 Provider Comparison Scope Decision](v0_9_0_provider_comparison_scope_decision.md)
- Sportmonks provider approval: no
- v0.9.0 opened: yes, docs-only
- Selected evaluation path: compare providers
- Selected implementation path: none
- Deeper Sportmonks work: paused
- API calls performed in this block: no
- Manual raw JSON review performed in this block: no
- Additional cache reading performed in this block: no
- `.local.csv` outputs created: no
- SQLite writes performed: no
- Streamlit activation performed: no
- Local trial performed: no
- GitHub release/tag created in this block: no

## Decision

- v0.9.0 is opened as a provider suitability scope milestone.
- This decision does not select an implementation path.
- This decision does not approve Sportmonks as a provider.
- This decision does not approve API calls, additional cache reading, `.local.csv`, SQLite, Streamlit, local trial or app integration.
- `Compare providers` is selected as the evaluation path.
- Deeper Sportmonks-specific work remains paused.
- The next decision must define a docs-only public-source comparison research protocol.

## Evidence From v0.8.0

| Evidence | Result |
|---|---|
| v0.8.0 closeout | closed with limitations |
| Local scaffold | completed |
| Approved local preview | completed |
| `row_count` | `6` |
| `has_position_ids` | `0` |
| `has_jersey_numbers` | `0` |
| Labels | unresolved |
| Market Context | unresolved |
| Provider approval | no |

## Scope Options

1. Stop Sportmonks exploration.
2. Compare providers before deeper Sportmonks work. Selected.
3. Investigate Sportmonks label lookup strategy.
4. Review richer Sportmonks endpoint suitability.
5. Design a separate local trial.

## Recommendation

Selected evaluation path: compare providers before deeper Sportmonks work.

- v0.8.0 validated the scaffold but exposed major unresolved gaps.
- Continuing deeper into Sportmonks without comparison risks overfitting the project to a weak or incomplete source.
- Provider comparison can be docs-only first and may avoid unnecessary API or cache work.

This is only a recommendation. It does not authorize provider access, web research, API calls or implementation.

## Still Forbidden

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
- GitHub release/tag.

## Next Required Action

A later docs-only block may create a public-source provider comparison research protocol decision for v0.9.0.

No web research, provider access, API calls, cache reading, implementation or approval is authorized by this decision.
