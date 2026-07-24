# v0.10.0 Reviewed Local Market Context Processing Policy Decision

## Status

- Milestone: v0.10.0
- Decision status: `manual-market-context-processing-policy-approved`
- Policy version: `manual-market-context-policy-v1`
- Related policy: [v0.10.0 Reviewed Local Market Context Processing Policy](../v0_10_0_manual_market_context_processing_policy.md)
- Related input contract: [v0.10.0 Reviewed Local Market Context Input Contract](../v0_10_0_manual_market_context_input_contract.md)
- Related implementation plan: [v0.10.0 Reviewed Local Market Context Implementation Plan](../v0_10_0_manual_market_context_implementation_plan.md)
- Related implementation plan decision: [v0.10.0 Reviewed Local Market Context Implementation Plan Decision](v0_10_0_manual_market_context_implementation_plan_decision.md)
- Related Stage B plan: [v0.10.0 Reviewed Local Market Context Stage B Plan](../v0_10_0_manual_market_context_stage_b_plan.md)
- Related Stage B decision: [v0.10.0 Reviewed Local Market Context Stage B Decision](v0_10_0_manual_market_context_stage_b_decision.md)
- Input contract version: `manual-market-context-input-v1`
- Policy approved: yes, docs-only
- Market-value zero parser blocker: resolved
- Stage A completed: yes
- Stage B approved by separate decision: yes
- Stage B implemented: no
- Stage C approved: no
- Stage D approved: no
- Implementation approved by this policy decision: no
- Parser implementation approved by this policy decision: no
- Synthetic fixtures approved by this policy decision: no
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
- This policy decision does not independently authorize implementation; the separate Stage B decision controls the bounded future Stage B code block.

## Stage B Normative Clarifications

Policy v1 now freezes all of the following without changing any diagnostic code, severity, scope or default outcome:

- every Stage A regression case remains, while expectations may migrate only for the Stage B stage marker, cumulative diagnostic catalog, later diagnostics on structurally valid rows, observation outputs and Stage B summary counts;
- `STAGE_NAME` changes to `"B"`, every Stage B result reports summary stage `B` even when Stage A validation stops processing, and the implemented catalog is exactly eleven Stage A plus 25 Stage B diagnostics, excluding `MCV405`, `MCV406` and every other code;
- exactly seven optional observation fields use one `MCV503_OPTIONAL_VALUE_MISSING` each when an optional column is absent or its value is null, empty or whitespace-only; metadata fields never use `MCV503`, and successful explicit-date age derivation is the sole suppression exception;
- absent `review_status`, provenance-reference and confidence columns follow the same approved metadata rules as absent tokens;
- the unchanged `valid_minimal.csv` Stage B result is accepted at file level, review-required at row level, has seven `MCV503`, one `MCV408`, one `MCV400`, no `MCV303` or `MCV305`, no observations, one review-required row and zero accepted or rejected rows;
- empty position is not provided, exact prohibited sentinel tokens use `MCV307`, and every other non-empty non-canonical position uses `MCV409` without aliases or fuzzy matching;
- missing confidence uses one `MCV303`, invalid populated confidence uses one `MCV305`, and the two are suppressed against each other for one token;
- missing or invalid salary period and estimate metadata use `MCV303`, while invalid populated currency uses only `MCV304` for that token;
- monetary values use `Decimal(token)` without normalization, quantization or rounding and preserve lexical scale; tokens beginning with `-`, including negative zero, use `MCV302` and create no zero observation;
- age and jersey number use Python `int`, dates use ISO strings, reviewed timestamps use canonical UTC strings, booleans use Python `bool`, missing normalized values use `None` and Stage B conflict IDs remain `None`;
- safe text normalization is exactly NFKC, exterior trim and whitespace collapse for the six named identity/provenance fields, preserving case, accents and punctuation;
- age derivation uses only valid explicit date of birth and age reference date, with completed-year arithmetic and exactly two `MCV306` diagnostics for a contradiction;
- invalid field-specific value dates do not fall back, invalid fallback dates do not become unknown, and future dates suppress stale/unknown diagnostics;
- `source_url` validation is deterministic and standard-library-only; `MCV310` rejects only the provenance field, preserves all seven observation outcomes, does not increment rejected observations or independently change row outcome, and never creates `partially-accepted`, while independent `MCV400` retains minimum outcome `accepted-with-warnings`;
- salary currency uses a visible, static, immutable, case-sensitive ISO 4217 alphabetic-code set with no dependency or network lookup;
- `partially-accepted` requires at least one rejected Stage B observation, at least one other surviving provided observation, and no higher-precedence row rule; isolated metadata or provenance rejection never qualifies;
- final observation partitioning follows the exact field-outcome and row-outcome algorithm, with mutually exclusive row counters and DataFrame counts reconciled before summary construction; and
- diagnostic suppression, cardinality, summary reconciliation and zero-based final ordering follow the exact Stage B policy sections.

These clarifications do not approve Stage C, Stage D, preview, real data, SQLite, Streamlit, providers or new dependencies.

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
| Stage B normalization and suppression rules | approved docs-only |
| Stage B logical output types | approved docs-only |
| Stage B age, date, URL and currency rules | approved docs-only |
| Parser implementation | authorized only by the separate bounded Stage B decision |
| Synthetic fixtures | authorized only by the separate bounded Stage B decision |
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

Stage A is completed and closed. The separate Stage B decision approves a bounded future Stage B implementation block, which has not been implemented.

Next permitted action: implement Stage B only under its approved file, diagnostic and test boundaries. Stages C-D, preview, real local data, SQLite, Streamlit, provider access and production integration remain excluded.
