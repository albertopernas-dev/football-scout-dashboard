# v0.10.0 Manual Market Context Workflow Scope Decision

## Status

- Milestone: v0.10.0
- Decision status: `manual-market-context-workflow-selected`
- Related scope plan: [v0.10.0 Manual Market Context Workflow Hardening Scope Plan](../v0_10_0_manual_market_context_scope_plan.md)
- Related v0.9.0 closeout: [v0.9.0 Provider Suitability Closeout Decision](v0_9_0_provider_suitability_closeout_decision.md)
- Canonical input contract: [v0.10.0 Reviewed Local Market Context Input Contract](../v0_10_0_manual_market_context_input_contract.md)
- Contract decision: [v0.10.0 Reviewed Local Market Context Input Contract Decision](v0_10_0_manual_market_context_input_contract_decision.md)
- Contract version: `manual-market-context-input-v1`
- Contract status: approved docs-only
- Processing policy: [v0.10.0 Reviewed Local Market Context Processing Policy](../v0_10_0_manual_market_context_processing_policy.md)
- Policy decision: [v0.10.0 Reviewed Local Market Context Processing Policy Decision](v0_10_0_manual_market_context_processing_policy_decision.md)
- Policy version: `manual-market-context-policy-v1`
- Policy status: approved docs-only
- Implementation plan: [v0.10.0 Reviewed Local Market Context Implementation Plan](../v0_10_0_manual_market_context_implementation_plan.md)
- Implementation plan decision: [v0.10.0 Reviewed Local Market Context Implementation Plan Decision](v0_10_0_manual_market_context_implementation_plan_decision.md)
- Implementation plan status: approved docs-only
- Stage A plan: [v0.10.0 Reviewed Local Market Context Stage A Plan](../v0_10_0_manual_market_context_stage_a_plan.md)
- Stage A decision: [v0.10.0 Reviewed Local Market Context Stage A Decision](v0_10_0_manual_market_context_stage_a_decision.md)
- Stage A closeout: [v0.10.0 Reviewed Local Market Context Stage A Closeout](../v0_10_0_manual_market_context_stage_a_closeout.md)
- Stage A closeout decision: [v0.10.0 Reviewed Local Market Context Stage A Closeout Decision](v0_10_0_manual_market_context_stage_a_closeout_decision.md)
- Stage B plan: [v0.10.0 Reviewed Local Market Context Stage B Plan](../v0_10_0_manual_market_context_stage_b_plan.md)
- Stage B decision: [v0.10.0 Reviewed Local Market Context Stage B Decision](v0_10_0_manual_market_context_stage_b_decision.md)
- Stage A implementation approved: yes
- Stage A implemented: yes
- Stage A verified: yes
- Stage A completed: yes
- Stage B approved: yes
- Stage B implemented: no
- Stage C approved: no
- Stage D approved: no
- Preview approved: no
- v0.10.0 opened: yes
- Selected path: Manual Market Context workflow improvements
- Full implementation approved: no
- Provider integration approved: no
- Real local data access approved: no
- SQLite writes approved: no
- Streamlit changes approved: no
- Numeric scoring approved: no
- Provider approval: none

## Decision

- v0.10.0 is opened as a local Market Context workflow-hardening milestone.
- The separate Stage B decision authorizes only the bounded future Stage B code block defined in its plan.
- The milestone builds on reviewed local CSV enrichment.
- It does not reopen v0.9.0 provider suitability work.
- No provider is selected or approved.
- No provider API or automated source is authorized.
- The first design block, the canonical reviewed local input contract, is completed docs-only.
- Full milestone implementation remains unapproved; Stage A is closed and Stage B is approved but not implemented.
- The input contract remains approved as documentation; the separate Stage A decision authorized only bounded structural parser and validation work, now completed under the closeout.
- Freshness, provenance, validation, diagnostics and duplicate/conflict policy are completed docs-only.
- The market-value-zero parser blocker is resolved through observation/effective separation.
- Stage A structural work is closed. Stage B normalization is approved but not implemented. Stages C-D and preview remain unapproved.

## Selected Scope

Permitted for future separately approved blocks:

- Canonical input contract design.
- Freshness and provenance design.
- Validation and conflict-policy design.
- Synthetic fixture design.
- Local parser and preview implementation after explicit approval.
- Diagnostics.
- Tests.

Not yet permitted:

- Real data access.
- Provider access.
- API calls.
- Cache reading.
- Scraping.
- SQLite writes.
- Streamlit integration.
- Production usage.

## v0.9.0 Boundary

- Sportmonks remains `continue-targeted-clarification`.
- API-Football remains `technical-baseline-only`.
- Capology remains `separate-role-candidate`.
- Transfermarkt remains `manual-reference-only`.
- No role outcome changes.
- No provider clarification is initiated.

## Canonical Input Contract

- `manual-market-context-input-v1` is approved as a documentation contract.
- It retains the existing `player`, `team`, `league`, `season` compound identity.
- The contract decision itself does not authorize implementation or fixtures. The separate Stage A decision authorizes only its bounded structural implementation and three synthetic fixtures; previews, real-data access, SQLite and Streamlit remain blocked.

## Processing Policy

- `manual-market-context-policy-v1` is approved as a documentation policy.
- It defines freshness, provenance, validation, diagnostics, duplicates and conflicts.
- It does not approve source precedence, effective consolidation or runtime changes.
- The market-value-zero parser blocker is resolved, while effective integration remains limited.

## Next Required Decision

Stage A is implemented, verified and closed. Stage B is approved for a separate code block and is not implemented.

Next permitted action: implement Stage B only under its approved boundary. Stages C-D, real local data, preview, persistence, SQLite, Streamlit and provider access remain excluded.
