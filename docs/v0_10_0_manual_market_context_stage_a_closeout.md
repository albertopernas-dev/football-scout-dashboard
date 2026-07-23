# v0.10.0 Reviewed Local Market Context Stage A Closeout

## Status

- Milestone: v0.10.0
- Stage: A
- Stage name: Core Contract And File Validation
- Closeout status: `manual-market-context-stage-a-completed`
- Related Stage A plan: [v0.10.0 Reviewed Local Market Context Stage A Plan](v0_10_0_manual_market_context_stage_a_plan.md)
- Related Stage A decision: [v0.10.0 Reviewed Local Market Context Stage A Decision](provider_decisions/v0_10_0_manual_market_context_stage_a_decision.md)
- Related implementation plan: [v0.10.0 Reviewed Local Market Context Implementation Plan](v0_10_0_manual_market_context_implementation_plan.md)
- Related input contract: [v0.10.0 Reviewed Local Market Context Input Contract](v0_10_0_manual_market_context_input_contract.md)
- Related processing policy: [v0.10.0 Reviewed Local Market Context Processing Policy](v0_10_0_manual_market_context_processing_policy.md)
- Closeout decision: [v0.10.0 Reviewed Local Market Context Stage A Closeout Decision](provider_decisions/v0_10_0_manual_market_context_stage_a_closeout_decision.md)
- Stage A approved: yes
- Stage A implemented: yes
- Stage A verified: yes
- Stage A committed: yes
- Stage A pushed: yes
- Stage B approved: no
- Stage C approved: no
- Stage D approved: no
- Real-data access approved: no
- SQLite integration approved: no
- Streamlit integration approved: no
- Provider approved: none
- New dependencies approved or added: no

## Implemented Commit

- Commit SHA: `0c3348ea5824450960e7edfd8d8b8a2596a46dda`
- Short SHA: `0c3348e`
- Subject: `Implement v0.10.0 Market Context Stage A`
- Pushed: yes

This closeout does not claim that a v0.10.0 tag or release exists.

## Implemented Files

| Path | Implemented Stage A responsibility |
|---|---|
| `src/manual_market_context_processing.py` | Public Stage A API, strict structural parsing, validation, deterministic diagnostics and summary. |
| `tests/test_manual_market_context_processing.py` | Stage A contract, validation, result, traceability and determinism tests. |
| `tests/fixtures/manual_market_context/valid_minimal.csv` | Minimal valid synthetic reviewed-local input. |
| `tests/fixtures/manual_market_context/structural_row_errors.csv` | Synthetic structural row failures. |
| `tests/fixtures/manual_market_context/duplicate_local_record_ids.csv` | Synthetic duplicate local-record identity failures. |

No existing product module was modified. No preview was executed. `src/market_context.py` was not changed. All committed fixture data is synthetic.

## Implemented API

```python
process_reviewed_market_context(
    input_path: Path,
    *,
    ingested_at: datetime,
    strict: bool = True,
) -> ManualMarketContextProcessingResult
```

The API is implemented without a default for `ingested_at`. The timestamp must be explicit and timezone-aware. `strict=False` remains blocked with the approved stable error. The function does not use the current clock, print output, persist data, discover files or call an existing loader.

`input_path` is required, has no default value and uses the approved `Path` type. There is no public API named `process_reviewed_market_context_csv`, and no nonexistent alias is documented.

## Processing Result Contract

```python
@dataclass(frozen=True)
class ManualMarketContextProcessingResult:
    file_outcome: str
    accepted_observations: pd.DataFrame
    review_required_observations: pd.DataFrame
    rejected_rows: pd.DataFrame
    diagnostics: pd.DataFrame
    file_summary: dict[str, object]
```

- Stage A returns empty observation DataFrames with deterministic planned schemas.
- `rejected_rows` contains only rows whose final Stage A outcome is `rejected`.
- Diagnostics use deterministic public columns and zero-based `diagnostic_order`.
- Private sorting keys do not appear in public result DataFrames.
- `duplicate_groups` is always `0` in Stage A because duplicate observation analysis belongs to Stage C.

## Implemented Diagnostics

Stage A implements exactly these eleven diagnostics. Every diagnostic has severity `error`.

| Scope | Code | Meaning |
|---|---|---|
| file | `MCV100_UNSUPPORTED_SCHEMA_VERSION` | Schema version is unsupported. |
| file | `MCV101_MISSING_REQUIRED_COLUMN` | A required contract column is missing. |
| file | `MCV102_DUPLICATE_HEADER` | The CSV header contains a duplicate column. |
| file | `MCV103_UNKNOWN_COLUMN` | The CSV header contains an unknown column. |
| file | `MCV104_INVALID_ENCODING` | The file is not valid under the approved encoding. |
| file | `MCV105_INVALID_DELIMITER` | An alternate delimiter was observed. |
| row | `MCV200_MISSING_REQUIRED_VALUE` | A required row value is missing. |
| row | `MCV201_DUPLICATE_LOCAL_RECORD_ID` | A local record identifier is duplicated. |
| row | `MCV202_INVALID_SEASON` | A populated season token is structurally invalid. |
| row | `MCV203_INVALID_REVIEWED_AT` | A populated reviewed-at token is structurally invalid. |
| row | `MCV204_INVALID_SOURCE_TYPE` | A populated source-type token is structurally invalid. |

No Stage B, Stage C or Stage D diagnostic is implemented by Stage A.

## Structural Behavior

Stage A implements strict UTF-8 CSV and header validation, required and unknown column checks, empty-file handling, required structural row values, duplicate local-record identifiers, season validation, timezone-aware `reviewed_at` validation and the approved `source_type` vocabulary.

Missing-value validation precedes field-specific structural validation. An absent required token emits only `MCV200_MISSING_REQUIRED_VALUE` for that field, while populated invalid tokens emit their specific structural diagnostic.

File-level rejection does not invent row records. A zero-byte or whitespace-only file is treated as an empty header set, emits the required-column diagnostics in canonical order and reports zero rows.

## Determinism And Traceability

- Invalid schema-version tokens are grouped and sorted by their complete internal values before safe public rendering.
- Row diagnostics retain the complete public `local_record_id`, allowing exact correlation with rejected rows.
- Public `raw_value` and `safe_row_reference` representations remain bounded and safe.
- Diagnostic and rejected-row ordering use private deterministic signatures rather than physical CSV row order.
- Canonical field rank is preserved; unknown fields sort lexicographically after canonical fields.
- Private sorting keys are removed before results are returned.
- Reordered equivalent inputs produce equivalent diagnostics, rejected rows and summaries.
- Summary counts reconcile with the returned Stage A partitions.

## Synthetic Fixtures

The implementation uses only the three approved synthetic fixtures:

- `valid_minimal.csv`
- `structural_row_errors.csv`
- `duplicate_local_record_ids.csv`

They contain no real player, provider or market-context data.

## Verification Evidence

- Python: `3.12.13`
- Stage A test file: `92 passed`
- Full test suite: `654 passed`
- `python -m compileall src scripts`: passed
- `git diff --check`: passed
- Preview: not executed

## Environment Note

The repository launcher `.venv\Scripts\python.exe` pointed to a removed Python 3.12 installation during verification. The approved checks were run with the functional Python `3.12.13` interpreter and the existing installed packages. The environment was not modified.

This is separate environment debt. It does not invalidate the recorded Stage A evidence and does not authorize dependency changes, environment repair or broader implementation.

## Scope Compliance

- No real or ignored local data was accessed.
- No existing Market Context loader or runtime behavior was changed.
- No SQLite read or write was added.
- No Streamlit integration was added.
- No provider path was opened or approved.
- No preview was executed.
- No dependency was added.
- No Stage B, Stage C or Stage D behavior was implemented.

## Deferred Work

The following remain blocked:

- field normalization;
- `market_value_eur = 0` observation processing;
- confidence processing;
- salary and currency processing;
- age and date-of-birth processing;
- contract-date processing;
- jersey-number processing;
- position processing;
- freshness processing;
- duplicate-observation analysis;
- conflict analysis;
- effective-field eligibility;
- preview execution;
- real-data access;
- SQLite integration;
- Streamlit integration;
- provider access or approval.

## Stage A Completion Decision

Stage A is implemented, verified, committed and pushed. Its bounded implementation is closed.

This closeout does not approve Stage B or any later stage.

Next permitted action: `Define a separate Stage B approval decision docs-only.`
