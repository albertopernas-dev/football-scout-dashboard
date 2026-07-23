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
- Known contract/runtime compatibility blockers remain unresolved.
- No parser implementation may be approved until those blockers are addressed by a separate decision.

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

## Next Required Decision

A separate docs-only block may define freshness, provenance, validation and duplicate/conflict policy for the approved contract.

That block must not implement parsing, fixtures, previews, persistence or UI integration.
