# v0.10.0 Reviewed Local Market Context Processing Policy Decision

## Status

- Milestone: v0.10.0
- Decision status: `manual-market-context-processing-policy-approved`
- Policy version: `manual-market-context-policy-v1`
- Related policy: [v0.10.0 Reviewed Local Market Context Processing Policy](../v0_10_0_manual_market_context_processing_policy.md)
- Related input contract: [v0.10.0 Reviewed Local Market Context Input Contract](../v0_10_0_manual_market_context_input_contract.md)
- Related implementation plan: [v0.10.0 Reviewed Local Market Context Implementation Plan](../v0_10_0_manual_market_context_implementation_plan.md)
- Related implementation plan decision: [v0.10.0 Reviewed Local Market Context Implementation Plan Decision](v0_10_0_manual_market_context_implementation_plan_decision.md)
- Input contract version: `manual-market-context-input-v1`
- Policy approved: yes, docs-only
- Market-value zero parser blocker: resolved
- Implementation approved: no
- Parser approved: no
- Fixtures approved: no
- Preview approved: no
- Real data access approved: no
- SQLite approved: no
- Streamlit approved: no
- Provider approval: none

## Decision

- Policy v1 is approved as documentation.
- It defines date resolution, freshness, provenance, validation, diagnostics, duplicate handling and conflict handling.
- It does not consolidate observations or select provider/source precedence.
- It resolves the zero-value parser blocker by separating observation acceptance from effective eligibility.
- Current runtime behavior is unchanged.
- No implementation is authorized.

## Approved Policy Outcomes

| Area | Outcome |
|---|---|
| Date resolution | approved docs-only |
| Freshness statuses and thresholds | approved docs-only |
| Provenance requirements | approved docs-only |
| Validation severity model | approved docs-only |
| Diagnostic catalog | approved docs-only |
| Duplicate policy | approved docs-only |
| Conflict policy | approved docs-only |
| Market-value zero observation semantics | approved docs-only |
| Market-value zero effective eligibility | remains excluded under current behavior |
| Parser implementation | not approved |
| Synthetic fixtures | not approved |
| Preview/report | not approved |
| Effective consolidation | deferred |
| Source precedence | deferred |
| SQLite | not approved |
| Streamlit | not approved |

## Market Value Zero Decision

- Zero remains a declared value distinct from null.
- A conforming future parser MUST accept and preserve a structurally valid zero as a normalized observation.
- It MUST preserve the numeric value as zero and MUST NOT convert it to null.
- It MUST emit `MCV407_MARKET_VALUE_ZERO_NOT_EFFECTIVE`.
- Field outcome: `accepted-with-warning`.
- Minimum row outcome: `accepted-with-warnings`.
- The observation remains in `accepted_observations` unless another independent rule rejects or places the row or field under review.
- It MUST NOT promote zero to `effective_market_value_eur` under current effective behavior.
- It MUST NOT increase effective market-value coverage.
- Parser implementation is no longer blocked by this issue.
- Effective integration remains a separate decision.

## Existing System Boundary

- No canonical field is renamed.
- No current loader is modified.
- No effective logic is modified.
- Provider outcomes remain unchanged.
- No provider integration is introduced.
- No data is accessed.

## Next Required Decision

The bounded implementation plan is approved docs-only. Implementation remains blocked.

A separate decision may approve Stage A core contract and file-validation implementation only. Stages B-D, real local data, SQLite, Streamlit, provider access and production integration remain excluded.
