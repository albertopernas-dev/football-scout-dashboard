# v0.10.0 Reviewed Local Market Context Stage B Decision

## Status

- Milestone: v0.10.0
- Stage: B
- Stage name: Row And Field Normalization
- Decision status: `manual-market-context-stage-b-approved`
- Stage B plan: [v0.10.0 Reviewed Local Market Context Stage B Plan](../v0_10_0_manual_market_context_stage_b_plan.md)
- Implementation plan: [v0.10.0 Reviewed Local Market Context Implementation Plan](../v0_10_0_manual_market_context_implementation_plan.md)
- Implementation-plan decision: [v0.10.0 Reviewed Local Market Context Implementation Plan Decision](v0_10_0_manual_market_context_implementation_plan_decision.md)
- Input contract: [v0.10.0 Reviewed Local Market Context Input Contract](../v0_10_0_manual_market_context_input_contract.md)
- Input contract version: `manual-market-context-input-v1`
- Processing policy: [v0.10.0 Reviewed Local Market Context Processing Policy](../v0_10_0_manual_market_context_processing_policy.md)
- Processing-policy decision: [v0.10.0 Reviewed Local Market Context Processing Policy Decision](v0_10_0_manual_market_context_processing_policy_decision.md)
- Processing policy version: `manual-market-context-policy-v1`
- Stage A closeout: [v0.10.0 Reviewed Local Market Context Stage A Closeout](../v0_10_0_manual_market_context_stage_a_closeout.md)
- Stage A closeout decision: [v0.10.0 Reviewed Local Market Context Stage A Closeout Decision](v0_10_0_manual_market_context_stage_a_closeout_decision.md)
- Stage A completed: yes
- Stage B approved: yes
- Stage B implemented: no
- Stage C approved: no
- Stage D approved: no
- Real data approved: no
- Preview approved: no
- SQLite approved: no
- Streamlit approved: no
- Provider approval: none
- New dependencies approved: no

## Decision

Approve only:

- the exact Stage B paths listed below;
- internal extension of the existing processor without changing its public signature;
- the 25 exact Stage B diagnostics listed below;
- the seven exact synthetic Stage B fixtures;
- the Stage B test matrix;
- limited migration of Stage A test expectations while retaining every Stage A regression case;
- `STAGE_NAME = "B"` and summary stage `B` for every returned Stage B result;
- the cumulative implemented catalog of exactly 36 diagnostics: eleven Stage A plus 25 Stage B, with neither `MCV405` nor `MCV406`;
- the frozen result, observation, rejected-row, diagnostic and summary schemas;
- the approved field outcomes, row outcomes and freshness statuses;
- observation-level effective eligibility without runtime consolidation;
- deterministic normalization, ordering and reconciliation under policy v1; and
- the exact suppression, cardinality and one-root-cause rules frozen by the clarified policy.

Do not approve:

- Stage C or Stage D;
- duplicate-observation or conflict processing;
- preview code or execution;
- real or ignored local data;
- SQLite or Streamlit;
- provider cache, providers or APIs;
- changes to `src/market_context.py`;
- new dependencies; or
- modifications outside the authorized paths.

## Frozen Stage B Rule Set

This decision expressly authorizes the future Stage B implementation to apply only the following clarified policy-v1 rules:

- every Stage A case remains as regression coverage; only the stage marker, cumulative diagnostic catalog, later Stage B diagnostics on structurally valid rows, observation outputs and Stage B summary-count expectations may migrate;
- the eleven Stage A diagnostics retain their triggers, scopes, severities, ordering and precedence; Stage A file errors and structurally rejected rows emit no Stage B diagnostics;
- tests may be renamed or split but not deleted, `STAGE_NAME` becomes `"B"`, every returned summary reports stage `B`, and exactly 36 diagnostic constants are implemented without `MCV405`, `MCV406` or any other code;
- exactly seven optional observation fields use one `MCV503` each when an optional column is absent or its token is null, empty or whitespace-only; metadata fields never use `MCV503`, and successful explicit-date age derivation is the sole suppression exception;
- absent `review_status`, provenance-reference and confidence columns follow their approved metadata rules;
- unchanged `valid_minimal.csv` yields file outcome `accepted`, seven `MCV503`, one `MCV408`, one `MCV400`, no `MCV303` or `MCV305`, no observations, final row outcome `review-required`, one review-required row and zero accepted or rejected rows;
- empty position is not provided, exact sentinels `N/A`, `unknown`, `-`, `null` use `MCV307`, and every other non-empty non-canonical position uses `MCV409` without semantic conversion;
- missing confidence uses one `MCV303`, invalid populated confidence uses one `MCV305`, and each rejects all populated observations without duplicate diagnostics for the same token;
- salary period and estimate metadata use exact enums and `MCV303` when missing or invalid, while an invalid populated currency uses only `MCV304` for that token;
- monetary normalization uses `Decimal(token)` without `.normalize()`, quantization or rounding and preserves lexical scale; every token beginning with `-`, including `-0` and `-0.00`, emits `MCV302`, creates no zero observation and does not use market-value-zero semantics;
- age and jersey number use Python `int`; dates use ISO strings; reviewed timestamps use canonical UTC strings; missing values use `None`; eligibility uses Python `bool`; conflict IDs remain `None`;
- safe text normalization is NFKC plus exterior trim and whitespace collapse for exactly `player`, `team`, `league`, `source_name`, `source_reference` and `reviewer`, preserving case, accents and punctuation;
- age derivation uses only explicit valid birth/reference dates and completed-year arithmetic, while contradictions emit exactly two `MCV306` diagnostics and reject both observations;
- an invalid populated field-specific value date forbids fallback, an invalid fallback date does not become unknown, and future dates suppress stale/unknown diagnostics;
- URL validation uses the exact standard-library-only predicate; field-scope `MCV310` uses `field_name=source_url`, rejects only that provenance field, preserves all seven observation outcomes, does not increment `rejected_field_observations`, does not independently change row outcome and never creates `partially-accepted`; independent `MCV400` retains minimum outcome `accepted-with-warnings` when no valid reference exists;
- currency validation uses a visible static immutable case-sensitive set of three-letter uppercase ISO 4217 codes, with no network or dependency;
- `partially-accepted` is authorized only when at least one of the seven observations is rejected, another provided observation survives as `accepted` or `accepted-with-warning`, and no row rule requires review or rejection; isolated metadata or provenance rejection never qualifies;
- final partitioning follows the exact `not-provided`, rejected-field and five-row-outcome algorithm, with mutually exclusive row counts and observation DataFrame counts reconciled before the summary; and
- rejected observation counts, diagnostic cardinality, summary reconciliation and zero-based final ordering follow the clarified policy exactly.

These rules do not add or rename diagnostics and do not change any approved severity, scope or default outcome.

## Evidence And Preconditions

- Stage A is implemented, verified, committed, pushed and closed.
- The Stage A implementation commit is `0c3348ea5824450960e7edfd8d8b8a2596a46dda`.
- Stage A tests previously recorded `92 passed`.
- The full suite previously recorded `654 passed`.
- Stage A compileall and diff checks previously passed.
- Stage B has no implementation evidence.
- This decision does not claim that Stage B code or fixtures exist.
- No real data, preview, persistence, UI or provider activity is authorized.

## Authorized Paths

| Path | Authorized purpose |
|---|---|
| `src/manual_market_context_processing.py` | Stage B normalization, field validation, freshness, outcomes, observations, diagnostics and summary counts. |
| `tests/test_manual_market_context_processing.py` | Stage B tests and complete Stage A regression coverage. |
| `tests/fixtures/manual_market_context/valid_full.csv` | Fully valid synthetic Stage B input. |
| `tests/fixtures/manual_market_context/market_value_zero.csv` | Approved zero-value observation behavior. |
| `tests/fixtures/manual_market_context/row_errors.csv` | Stage B review-status row outcomes. |
| `tests/fixtures/manual_market_context/field_errors.csv` | Stage B field validation failures. |
| `tests/fixtures/manual_market_context/freshness_cases.csv` | Approved freshness states and boundaries. |
| `tests/fixtures/manual_market_context/positions.csv` | Canonical, invalid and unmapped synthetic positions. |
| `tests/fixtures/manual_market_context/partial_acceptance.csv` | Mixed accepted/rejected field observations in one row. |

No documentation, script, existing Stage A fixture or other path is authorized for the future Stage B code block.

## Authorized Diagnostics

| Code | Severity | Scope | Outcome |
|---|---|---|---|
| `MCV205_INVALID_REVIEW_STATUS` | error | row | row rejected |
| `MCV206_REJECTED_REVIEW_STATUS` | error | row | row rejected |
| `MCV300_INVALID_DATE` | error | field | field rejected |
| `MCV301_INVALID_NUMBER` | error | field | field rejected |
| `MCV302_NEGATIVE_VALUE` | error | field | field rejected |
| `MCV303_MISSING_CONDITIONAL_METADATA` | error | field | field rejected |
| `MCV304_INVALID_CURRENCY` | error | field | field rejected |
| `MCV305_INVALID_CONFIDENCE` | error | field | field rejected |
| `MCV306_AGE_DATE_CONTRADICTION` | error | field | age and date-of-birth observations rejected |
| `MCV307_INVALID_POSITION` | error | field | field rejected |
| `MCV308_INVALID_JERSEY_NUMBER` | error | field | field rejected |
| `MCV309_FUTURE_VALUE_DATE` | error | field | field rejected |
| `MCV310_INVALID_SOURCE_URL` | error | field | provenance field rejected |
| `MCV400_MISSING_PROVENANCE_REFERENCE` | warning | row | accepted-with-warnings |
| `MCV401_UNKNOWN_VALUE_DATE` | warning | field | accepted-with-warning |
| `MCV402_STALE_VALUE` | warning | field | accepted-with-warning |
| `MCV403_ESTIMATED_VALUE` | warning | field | accepted-with-warning |
| `MCV404_NEEDS_REVIEW_STATUS` | warning | row | review-required |
| `MCV407_MARKET_VALUE_ZERO_NOT_EFFECTIVE` | warning | field | accepted-with-warning |
| `MCV408_MISSING_REVIEW_STATUS` | warning | row | review-required |
| `MCV409_UNMAPPED_POSITION` | warning | field | review-required |
| `MCV500_NORMALIZED_TEXT` | info | field | accepted |
| `MCV501_NORMALIZED_TIMESTAMP` | info | field | accepted |
| `MCV502_DERIVED_AGE` | info | field | accepted |
| `MCV503_OPTIONAL_VALUE_MISSING` | info | field | not-provided |

The cumulative Stage B implementation catalog is exactly 36 diagnostics: the eleven Stage A diagnostics remain implemented and frozen, and the 25 Stage B diagnostics above are added. `MCV405_DUPLICATE_OBSERVATION` and `MCV406_CONFLICTING_OBSERVATION` remain reserved for Stage C and undeclared in Stage B. No other diagnostic code is authorized.

## Authorized Fixtures

- `tests/fixtures/manual_market_context/valid_full.csv`
- `tests/fixtures/manual_market_context/market_value_zero.csv`
- `tests/fixtures/manual_market_context/row_errors.csv`
- `tests/fixtures/manual_market_context/field_errors.csv`
- `tests/fixtures/manual_market_context/freshness_cases.csv`
- `tests/fixtures/manual_market_context/positions.csv`
- `tests/fixtures/manual_market_context/partial_acceptance.csv`

All must be synthetic, fictitious, deterministic, safe for Git and free of Stage C-D behavior.

## Frozen Boundaries

Public API:

```python
def process_reviewed_market_context(
    input_path: Path,
    *,
    ingested_at: datetime,
    strict: bool = True,
) -> ManualMarketContextProcessingResult:
    ...
```

The following are frozen:

- Stage A file and structural row behavior;
- `manual-market-context-input-v1`;
- `manual-market-context-policy-v1`;
- the frozen result dataclass members;
- the 21-column observation schema;
- the rejected-row schema;
- the 12-column diagnostic schema;
- the 24-field summary schema;
- approved field and row outcomes;
- approved freshness statuses;
- zero-based deterministic diagnostic ordering;
- no automatic source precedence;
- no fuzzy matching;
- no provider-specific assumption;
- no automatic effective consolidation; and
- no physical CSV order as semantic identity.

## Next Action

Implement Stage B only under the approved file, diagnostic and test boundaries.

Completing Stage B will not approve Stage C or Stage D.
