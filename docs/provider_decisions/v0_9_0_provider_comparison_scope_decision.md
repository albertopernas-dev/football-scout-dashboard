# v0.9.0 Provider Comparison Scope Decision

## Status

- Milestone: v0.9.0
- Decision status: `compare-providers-path-selected`
- Related comparison plan: [v0.9.0 Provider Comparison Plan](../v0_9_0_provider_comparison_plan.md)
- Related suitability scope plan: [v0.9.0 Provider Suitability Scope Plan](../v0_9_0_provider_suitability_scope_plan.md)
- Related Sportmonks scope decision: [Sportmonks v0.9.0 Scope Decision](sportmonks_v0_9_0_scope_decision.md)
- Selected path: compare providers
- Candidate set selected: yes
- Comparison executed: no
- Public web research approved: no
- Provider access approved: no
- API calls approved: no
- Additional cache reading approved: no
- Implementation approved: no
- Provider approval: none

## Decision

- `Compare providers` is selected as the next v0.9.0 path.
- Deeper Sportmonks-specific work remains paused.
- The comparison is limited to candidates already documented in the repository.
- No evaluation, scoring or current-fact research is performed in this block.
- No provider gains approval from inclusion in the candidate set.

## Selected Candidates

1. Sportmonks.
2. API-Football / API-Sports.
3. Capology.
4. Transfermarkt as a manual reference only.

## Reason For Selection

- Sportmonks has limited technical validation but unresolved functional gaps.
- API-Football provides a known technical baseline but lacks demonstrated Market Context.
- Capology may be relevant for salary and contract context but remains unapproved.
- Transfermarkt may provide manual market-reference context but is not approved for scraping or automated integration.
- Comparing these candidates reduces the risk of overcommitting to Sportmonks.

## Comparison Boundary

The future comparison must focus on:

- identity;
- human-readable labels;
- position and jersey coverage;
- age;
- market value;
- contract end;
- salary context;
- relevant league coverage;
- freshness;
- licensing clarity;
- local workflow compatibility;
- integration complexity;
- current public plan or access limits.

## Explicitly Not Selected

- Label lookup implementation.
- Richer Sportmonks endpoint review.
- Local trial design.
- SQLite integration.
- Streamlit integration.
- Provider approval.
- New provider discovery.
- API integration.

## Still Forbidden

- Web research until separately approved.
- API calls.
- Login or account dashboard access.
- Provider cache reading.
- Manual raw JSON review.
- Broad payload inspection.
- `.local.csv`.
- SQLite writes.
- Streamlit integration.
- Local trial.
- App integration.
- Provider approval.
- Release/tag.

## Next Required Action

A later docs-only block may approve the public-source comparison research protocol.

No research or provider access is authorized by this decision.
