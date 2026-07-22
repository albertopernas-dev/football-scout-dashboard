# v0.10.0 Manual Market Context Workflow Scope Decision

## Status

- Milestone: v0.10.0
- Decision status: `manual-market-context-workflow-selected`
- Related scope plan: [v0.10.0 Manual Market Context Workflow Hardening Scope Plan](../v0_10_0_manual_market_context_scope_plan.md)
- Related v0.9.0 closeout: [v0.9.0 Provider Suitability Closeout Decision](v0_9_0_provider_suitability_closeout_decision.md)
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
- The first planned design block is the canonical reviewed local input contract.
- Implementation remains unapproved.

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

## First Required Decision

A separate docs-only block may define the canonical reviewed local Market Context input contract.

That block must not implement parsing, access real local data or modify the application.
