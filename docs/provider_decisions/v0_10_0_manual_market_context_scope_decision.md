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
- v0.10.0 opened: yes
- Selected path: Manual Market Context workflow improvements
- Implementation approved: no
- Provider integration approved: no
- Real local data access approved: no
- SQLite writes approved: no
- Streamlit changes approved: no
- Numeric scoring approved: no
- Provider approval: none

## Decision

- v0.10.0 is opened as a local Market Context workflow-hardening milestone.
- The milestone builds on reviewed local CSV enrichment.
- It does not reopen v0.9.0 provider suitability work.
- No provider is selected or approved.
- No provider API or automated source is authorized.
- The first design block, the canonical reviewed local input contract, is completed docs-only.
- Implementation remains unapproved.
- That input contract is now approved as documentation only; no parser or data processing is approved.
- Freshness, provenance, validation, diagnostics and duplicate/conflict policy are completed docs-only.
- The market-value-zero parser blocker is resolved through observation/effective separation.
- Parser, fixtures and preview remain unapproved.

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
- It does not authorize implementation, fixtures, previews, real-data access, SQLite or Streamlit.

## Processing Policy

- `manual-market-context-policy-v1` is approved as a documentation policy.
- It defines freshness, provenance, validation, diagnostics, duplicates and conflicts.
- It does not approve source precedence, effective consolidation or runtime changes.
- The market-value-zero parser blocker is resolved, while effective integration remains limited.

## Next Required Decision

The bounded implementation plan is approved docs-only. Implementation remains blocked.

A separate decision may approve Stage A core contract and file-validation implementation only. Stages B-D, real local data, persistence, SQLite, Streamlit and provider access remain excluded.
