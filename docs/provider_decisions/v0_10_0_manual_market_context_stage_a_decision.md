# v0.10.0 Reviewed Local Market Context Stage A Decision

## Status

- Milestone: v0.10.0
- Stage: A
- Decision status: `manual-market-context-stage-a-approved`
- Related Stage A plan: [v0.10.0 Reviewed Local Market Context Stage A Plan](../v0_10_0_manual_market_context_stage_a_plan.md)
- Related implementation plan: [v0.10.0 Reviewed Local Market Context Implementation Plan](../v0_10_0_manual_market_context_implementation_plan.md)
- Related input contract: [v0.10.0 Reviewed Local Market Context Input Contract](../v0_10_0_manual_market_context_input_contract.md)
- Related processing policy: [v0.10.0 Reviewed Local Market Context Processing Policy](../v0_10_0_manual_market_context_processing_policy.md)
- Stage A approved: yes
- Stage A implemented: no
- Stage B approved: no
- Stage C approved: no
- Stage D approved: no
- Real data approved: no
- SQLite approved: no
- Streamlit approved: no
- Provider approval: none
- New dependencies approved: no

## Decision

- Stage A implementation is approved for a separate code block.
- Approval is limited to the five specified paths.
- Only structural contract and file/row validation are approved.
- Only diagnostics `MCV100` through `MCV105` and `MCV200` through `MCV204` may be implemented.
- Only synthetic fixtures may be used.
- No field-level Market Context semantics are approved.
- No current runtime path may change.

## Approved Files

| Path | Approved Function |
|---|---|
| `src/manual_market_context_processing.py` | Stage A constants, API, result contract, strict file parsing, structural validation, diagnostics and summary. |
| `tests/test_manual_market_context_processing.py` | Stage A API, parser, validation, result and determinism tests. |
| `tests/fixtures/manual_market_context/valid_minimal.csv` | One structurally valid synthetic input. |
| `tests/fixtures/manual_market_context/structural_row_errors.csv` | Synthetic structural row failures only. |
| `tests/fixtures/manual_market_context/duplicate_local_record_ids.csv` | Synthetic exact duplicate local IDs. |

No other path is approved for the Stage A implementation block.

## Approved Diagnostics

| Code | Scope | Default Outcome |
|---|---|---|
| `MCV100_UNSUPPORTED_SCHEMA_VERSION` | file | file rejected |
| `MCV101_MISSING_REQUIRED_COLUMN` | file | file rejected |
| `MCV102_DUPLICATE_HEADER` | file | file rejected |
| `MCV103_UNKNOWN_COLUMN` | file | file rejected |
| `MCV104_INVALID_ENCODING` | file | file rejected |
| `MCV105_INVALID_DELIMITER` | file | file rejected |
| `MCV200_MISSING_REQUIRED_VALUE` | row | row rejected |
| `MCV201_DUPLICATE_LOCAL_RECORD_ID` | row | all implicated rows rejected |
| `MCV202_INVALID_SEASON` | row | row rejected |
| `MCV203_INVALID_REVIEWED_AT` | row | row rejected |
| `MCV204_INVALID_SOURCE_TYPE` | row | row rejected |

The approved severity for all eleven diagnostics remains `error`. Stage A does not change any approved code, scope, severity, outcome or meaning.

## Explicitly Not Approved

- Stage B, Stage C or Stage D.
- Preview script or preview execution.
- Real data or existing local CSV files.
- Provider cache.
- SQLite.
- Streamlit.
- API calls or providers.
- Changes to the existing Market Context loader.
- Freshness.
- Market-value-zero semantics.
- Position, jersey, salary, currency, contract, age or date-of-birth parsing.
- Confidence or review-status semantics.
- Duplicate observations.
- Conflicts or conflict-group IDs.
- Source precedence.
- Effective consolidation or eligibility.
- New dependencies.

## Next Action

Implement Stage A only under the approved file, diagnostic and test boundaries.

Completion of Stage A does not approve Stage B.
