# v0.10.0 Reviewed Local Market Context Input Contract Decision

## Status

- Milestone: v0.10.0
- Decision status: `reviewed-local-input-contract-approved`
- Related contract: [v0.10.0 Reviewed Local Market Context Input Contract](../v0_10_0_manual_market_context_input_contract.md)
- Related scope plan: [v0.10.0 Manual Market Context Workflow Hardening Scope Plan](../v0_10_0_manual_market_context_scope_plan.md)
- Related scope decision: [v0.10.0 Manual Market Context Workflow Scope Decision](v0_10_0_manual_market_context_scope_decision.md)
- Contract version approved: `manual-market-context-input-v1`
- Contract approved: yes, documentation only
- Implementation approved: no
- Parser approved: no
- Real local data access approved: no
- CSV creation or migration approved: no
- Synthetic fixtures approved: no
- SQLite writes approved: no
- Streamlit changes approved: no
- Provider approval: none

## Decision

- The reviewed local Market Context input contract v1 is approved as a documentation contract.
- The contract aligns with the existing compound identity and canonical field names where possible.
- Known semantic incompatibilities are explicitly recorded.
- `market_value_eur = 0` remains an implementation-blocking compatibility decision.
- It defines row grain, identity, field semantics, dates, currencies, provenance, review metadata and structural acceptance expectations.
- It does not authorize implementation or real-data processing.
- No provider-specific schema is approved.
- Unknown or additional columns must not be ignored silently.
- Conflict resolution remains deferred.

## Approved Contract Principles

- Existing canonical compound player identity retained.
- One reviewed snapshot per row.
- Explicit schema version.
- Unique local record identifier.
- Required source and review metadata.
- ISO dates.
- Explicit currencies for generic monetary values.
- Null remains distinct from zero.
- No provider-specific fields.
- Strict unknown-column policy by default.
- Real inputs remain ignored by Git.
- Pipeline-generated ingestion metadata remains outside manual control.
- No silent fallback, overwrite or conflict resolution.

## Approved And Deferred Table

| Area | Status |
|---|---|
| Contract structure | approved docs-only |
| Column semantics | approved docs-only |
| Row grain | approved docs-only |
| Schema version | approved docs-only |
| Structural acceptance rules | approved docs-only |
| Market-value zero semantics | unresolved; blocks parser implementation |
| Parser implementation | not approved |
| Validation implementation | not approved |
| Conflict resolution | deferred |
| Synthetic fixtures | not approved |
| Real local input access | not approved |
| Preview/report | not approved |
| SQLite | not approved |
| Streamlit | not approved |

## Existing System Boundary

- API-Football remains the technical and statistics baseline.
- This decision does not alter any provider outcome from v0.9.0.
- Transfermarkt remains manual-reference-only.
- No provider integration is introduced.
- No existing canonical field is renamed by this decision.
- The current `player`, `team`, `league`, `season` compound join remains documented as the existing identity boundary; no new player ID is created.

## Next Required Decision

A separate docs-only block may define the freshness, provenance, validation and duplicate/conflict policy for contract v1. Before implementation can be approved, that policy decision must resolve the `market_value_eur = 0` compatibility blocker or explicitly preserve it as blocking.

That block must not implement parsing, fixtures, previews, persistence or UI integration.
