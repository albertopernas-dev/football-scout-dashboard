# v0.10.0 Reviewed Local Market Context Stage A Plan

## Status

- Milestone: v0.10.0
- Stage: A
- Stage name: Core Contract And File Validation
- Plan status: `manual-market-context-stage-a-plan-defined`
- Related implementation plan: [v0.10.0 Reviewed Local Market Context Implementation Plan](v0_10_0_manual_market_context_implementation_plan.md)
- Related implementation decision: [v0.10.0 Reviewed Local Market Context Implementation Plan Decision](provider_decisions/v0_10_0_manual_market_context_implementation_plan_decision.md)
- Related input contract: [v0.10.0 Reviewed Local Market Context Input Contract](v0_10_0_manual_market_context_input_contract.md)
- Input contract version: `manual-market-context-input-v1`
- Related processing policy: [v0.10.0 Reviewed Local Market Context Processing Policy](v0_10_0_manual_market_context_processing_policy.md)
- Policy version: `manual-market-context-policy-v1`
- Related Stage A decision: [v0.10.0 Reviewed Local Market Context Stage A Decision](provider_decisions/v0_10_0_manual_market_context_stage_a_decision.md)
- Related Stage A closeout: [v0.10.0 Reviewed Local Market Context Stage A Closeout](v0_10_0_manual_market_context_stage_a_closeout.md)
- Related Stage A closeout decision: [v0.10.0 Reviewed Local Market Context Stage A Closeout Decision](provider_decisions/v0_10_0_manual_market_context_stage_a_closeout_decision.md)
- Stage A implementation approved: yes
- Stage A implemented: yes
- Stage A verified: yes
- Stage A completed: yes
- Stage B approved: no
- Stage C approved: no
- Stage D approved: no
- Real local data approved: no
- SQLite approved: no
- Streamlit approved: no
- Provider approval: none
- New dependencies approved: no

## Purpose

Stage A implements only the deterministic structural boundary needed to identify whether a reviewed local CSV file and its rows are safe to process further.

Stage A:

- does not interpret Market Context field values;
- does not produce effective consolidation;
- does not calculate freshness;
- does not analyze duplicate observations or conflicts;
- does not execute a preview;
- does not access real data; and
- prepares the structured result contract for later, separately approved stages.

This document defined and authorized the bounded Stage A code block. The linked closeout records that block as implemented and verified.

## Approved Stage A Files

Only these five paths were authorized and implemented for Stage A:

| Path | Stage A Purpose |
|---|---|
| `src/manual_market_context_processing.py` | Define the v1 structural constants, public API, frozen result contract, strict CSV/file parsing, Stage A validation, diagnostics and summary. |
| `tests/test_manual_market_context_processing.py` | Test the public API, file/row structural validation, diagnostics, deterministic outputs and result contract. |
| `tests/fixtures/manual_market_context/valid_minimal.csv` | Provide one structurally valid, entirely synthetic row. |
| `tests/fixtures/manual_market_context/structural_row_errors.csv` | Provide independent synthetic rows for approved Stage A row failures. |
| `tests/fixtures/manual_market_context/duplicate_local_record_ids.csv` | Provide synthetic exact duplicate local record IDs for deterministic rejection tests. |

Malformed file cases that are difficult or misleading to represent as conventional versioned CSV fixtures, including BOM, invalid encoding, invalid delimiters and duplicate headers, MUST be created inside tests with `tmp_path`.

Stage A does not authorize:

- `scripts/preview_manual_market_context.py`;
- any Stage B, Stage C or Stage D fixture;
- modifications to `src/market_context.py`; or
- modifications to any existing source module.

## Public API Approved For Stage A

Stage A approves this public entry point:

```python
def process_reviewed_market_context(
    input_path: Path,
    *,
    ingested_at: datetime,
    strict: bool = True,
) -> ManualMarketContextProcessingResult:
    ...
```

Rules:

- `input_path` is required.
- `ingested_at` is required and MUST be timezone-aware.
- The implementation MUST NOT call `datetime.now()` internally.
- `strict=True` is the only approved Stage A mode.
- Passing `strict=False` MUST raise `ValueError` with the stable message `strict=False is not approved for Stage A`.
- A naive `ingested_at` MUST raise `ValueError` with the stable message `ingested_at must be timezone-aware`.
- `FileNotFoundError`, `PermissionError` and narrow filesystem errors MUST NOT become contract diagnostics.
- The implementation MUST NOT catch `Exception` indiscriminately.
- The API MUST NOT print or persist.
- The API MUST NOT call the current Market Context loader.
- The API has no default path and MUST NOT discover files automatically.

## Stage A Result Contract

Stage A implements the planned frozen dataclass:

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

Stage A rules:

- `accepted_observations` is empty and uses the approved observation schema and column order.
- `review_required_observations` is empty and uses the approved observation schema and column order.
- Stage A creates no field observations.
- Empty observation DataFrames do not mean that the input has no structurally valid rows.
- Structurally valid rows are represented in `file_summary` counts.
- `rejected_rows` contains only rows whose final `row_outcome` is `rejected`.
- File rejection before safe row interpretation MAY return an empty `rejected_rows`.
- File-level rejection MUST NOT invent row records.
- Every DataFrame has deterministic columns and order, including when empty.
- The implementation uses no global state and returns no open file handles.
- Outputs MUST NOT share mutable state with internal parsing objects.

The Stage A observation schema is the full planned schema so that later stages do not change the result shape:

- `local_record_id`
- `player`
- `team`
- `league`
- `season`
- `field_name`
- `raw_value`
- `normalized_value`
- `effective_value_date`
- `freshness_status`
- `source_name`
- `source_type`
- `source_url`
- `source_reference`
- `reviewed_at`
- `reviewer`
- `confidence`
- `review_status`
- `field_outcome`
- `conflict_group_id`
- `effective_eligible`

All observation rows remain absent in Stage A.

## Approved Stage A Constants

The implemented module defines only the constants needed for Stage A:

- input contract version;
- processing policy version;
- required columns;
- optional columns;
- allowed columns;
- canonical column order;
- allowed source types;
- observation, rejected-row and diagnostic output columns;
- Stage A diagnostic codes;
- severity ordering;
- approved scope values;
- file outcomes; and
- Stage A row outcomes.

Constants for later semantics are not approved, except where a column name is required to construct an empty approved output schema.

Stage A does not approve:

- freshness thresholds;
- active canonical-position validation;
- currencies;
- confidence validation;
- salary metadata validation;
- field-outcome calculation;
- effective-eligibility logic; or
- conflict hashing.

## Approved Stage A Diagnostics

Stage A implements exactly these diagnostics:

### File Scope

| Code | Severity | Scope | Default Outcome |
|---|---|---|---|
| `MCV100_UNSUPPORTED_SCHEMA_VERSION` | error | file | file rejected |
| `MCV101_MISSING_REQUIRED_COLUMN` | error | file | file rejected |
| `MCV102_DUPLICATE_HEADER` | error | file | file rejected |
| `MCV103_UNKNOWN_COLUMN` | error | file | file rejected |
| `MCV104_INVALID_ENCODING` | error | file | file rejected |
| `MCV105_INVALID_DELIMITER` | error | file | file rejected |

### Row Scope

| Code | Severity | Scope | Default Outcome |
|---|---|---|---|
| `MCV200_MISSING_REQUIRED_VALUE` | error | row | row rejected |
| `MCV201_DUPLICATE_LOCAL_RECORD_ID` | error | row | all implicated rows rejected |
| `MCV202_INVALID_SEASON` | error | row | row rejected |
| `MCV203_INVALID_REVIEWED_AT` | error | row | row rejected |
| `MCV204_INVALID_SOURCE_TYPE` | error | row | row rejected |

Stage A MUST NOT implement:

- `MCV205` or any later row/field error;
- warnings `MCV400` or later; or
- info diagnostics `MCV500` or later.

No unapproved diagnostic code may be emitted. Stage A does not change the approved severity, scope, default outcome or meaning of any code. A file error blocks normal row processing. Row errors may coexist in a structurally processable file. The same underlying issue MUST NOT emit unnecessary duplicate diagnostics.

## File Validation Order

The implementation order is mandatory:

1. Establish existence and open the explicit path, allowing narrow filesystem exceptions to propagate.
2. Validate `strict` and `ingested_at` API arguments.
3. Read bytes safely.
4. Validate UTF-8 without BOM.
5. Validate delimiter structure.
6. Validate headers and duplicate headers.
7. Validate required and unknown columns.
8. Read tabular values while preserving strings.
9. Validate schema version.
10. Perform structural row validation.

Contract violations become diagnostics. Filesystem failures remain narrow exceptions. If one phase makes later interpretation unsafe, processing stops. No rejected row is invented when rows could not be read safely.

## Encoding Policy

Stage A MUST:

- accept UTF-8 without BOM;
- reject UTF-8 BOM with `MCV104_INVALID_ENCODING`;
- reject undecodable bytes with `MCV104_INVALID_ENCODING`;
- avoid Latin-1, Windows-1252 and all other fallback decoding; and
- leave the input file unchanged.

## Delimiter And Header Policy

- The only approved delimiter is comma.
- Permissive delimiter auto-detection MUST NOT replace contract validation.
- Semicolon and tab inputs produce `MCV105_INVALID_DELIMITER`.
- Duplicate headers MUST be detected before pandas can rename them.
- Each duplicate-header issue produces `MCV102_DUPLICATE_HEADER`.
- Each missing required header produces `MCV101_MISSING_REQUIRED_COLUMN`, ordered by canonical column order.
- Each unknown header in `strict=True` produces `MCV103_UNKNOWN_COLUMN`, ordered lexicographically.
- Any of these file diagnostics sets `file_outcome` to `rejected`.
- Row processing does not continue after these errors.
- The tabular read MUST preserve input tokens as strings and MUST NOT infer numeric values.

### Empty Or Whitespace-Only File

- A zero-byte file or a decoded file containing only whitespace has no header.
- Treat it as an empty header set.
- Emit one `MCV101_MISSING_REQUIRED_COLUMN` for every required column.
- Order those diagnostics by canonical required-column order.
- Do not emit `MCV105_INVALID_DELIMITER`, because no alternate delimiter was observed.
- Set `file_outcome = rejected`.
- Set `total_rows = 0`.
- Set `accepted_rows = 0`.
- Set `rejected_rows = 0`.
- Return an empty `rejected_rows` DataFrame.
- Emit no row diagnostics.
- Do not invent row records.

## Schema Version Policy

- The `schema_version` header is required; an absent header is handled by `MCV101_MISSING_REQUIRED_COLUMN`.
- Every row MUST contain exactly `manual-market-context-input-v1`.
- An empty, different or inconsistent version produces `MCV100_UNSUPPORTED_SCHEMA_VERSION`.
- Emit one deterministic diagnostic for each distinct invalid version token, not necessarily one per repeated row.
- An invalid schema version sets `file_outcome` to `rejected`.
- Structural row validation does not continue when schema-version validation fails.

## Structural Required Values

Stage A validates these values in every safely interpreted row:

- `local_record_id`
- `player`
- `team`
- `league`
- `season`
- `source_name`
- `source_type`
- `reviewed_at`
- `reviewer`

Null, empty and whitespace-only values produce `MCV200_MISSING_REQUIRED_VALUE`, one diagnostic per missing field in canonical column order. The row outcome is `rejected`; other rows continue processing.

Required-value precedence:

- Missing-value validation runs before field-specific structural validation.
- When a required value is null, empty or whitespace-only, emit only `MCV200_MISSING_REQUIRED_VALUE` for that field.
- Do not additionally emit `MCV202_INVALID_SEASON`, `MCV203_INVALID_REVIEWED_AT` or `MCV204_INVALID_SOURCE_TYPE` for the same missing token.
- Season, reviewed-at and source-type validation run only when the corresponding token is present.
- This suppression prevents multiple diagnostics for the same underlying missing-value issue.
- Other independent errors on the same row may still emit their own diagnostics.

`schema_version` remains a file-level concern under `MCV100_UNSUPPORTED_SCHEMA_VERSION`.

## Season Validation

- `season` MUST match `^\d{4}$` exactly.
- Stage A MUST NOT normalize decimal forms, ranges, whitespace padding or free-form labels.
- Invalid examples include `2024.0`, `2024/25`, `2024-25`, ` 2024 ` and named seasons.
- Invalid values produce `MCV202_INVALID_SEASON`.
- The row outcome is `rejected`.
- All columns are read as strings; pandas numeric inference MUST NOT rewrite season tokens.

## Reviewed At Validation

Stage A accepts only ISO-8601 timezone-aware datetimes:

- UTC with `Z`; or
- an explicit offset such as `+02:00`.

Stage A rejects:

- naive datetimes;
- dates without a time;
- malformed text; and
- timestamps without a timezone designator.

Rejected values produce `MCV203_INVALID_REVIEWED_AT` and a `rejected` row outcome.

Stage A may normalize the instant internally for validation, but it:

- does not emit `MCV501_NORMALIZED_TIMESTAMP`;
- does not create a field observation; and
- preserves only a safe, bounded representation for diagnostics.

## Source Type Validation

Allowed values are exact and case-sensitive:

- `official-public`
- `provider-public`
- `manual-reference`
- `internal-reviewed`
- `other-reviewed`

Stage A does not normalize case, whitespace or aliases. An invalid value produces `MCV204_INVALID_SOURCE_TYPE` and a `rejected` row outcome.

## Duplicate Local Record IDs

- Evaluate duplicates only after presence validation.
- Compare non-empty tokens exactly as they appear in the CSV.
- Do not apply Stage B normalization.
- Reject every row implicated in an exact duplicate.
- Emit `MCV201_DUPLICATE_LOCAL_RECORD_ID` for every implicated row.
- Do not select a winner based on row position.
- Results MUST be independent of input order.

## Row Outcome Rules

Stage A supports only:

- `accepted`: the row has no Stage A row diagnostic; and
- `rejected`: the row has at least one Stage A row error.

Stage A does not produce:

- `accepted-with-warnings`;
- `partially-accepted`; or
- `review-required`.

`file_outcome = accepted` means the file was structurally processable and may include rejected rows. `file_outcome = rejected` is reserved for file-level errors. A file is not rejected only because every safely interpreted row has row errors.

## Diagnostics Schema And Ordering

Stage A diagnostics use these columns in this exact order:

- `diagnostic_code`
- `severity`
- `scope`
- `message`
- `local_record_id`
- `field_name`
- `conflict_group_id`
- `raw_value`
- `normalized_value`
- `row_outcome`
- `field_outcome`
- `diagnostic_order`

Stage A rules:

- `conflict_group_id` is always null.
- `field_outcome` is always null.

The mandatory deterministic sort is:

1. File-scope diagnostics before row-scope diagnostics.
2. File diagnostics by validation-phase order, with missing required columns ordered by canonical contract-column rank, unknown columns ordered lexicographically, and `diagnostic_code` as the final tie-breaker.
3. Row diagnostics by `local_record_id`, canonical field rank, unknown or non-contract field names lexicographically after canonical fields, `diagnostic_code`, and a safe normalized raw-value representation as the final tie-breaker when needed.
4. Assign zero-based `diagnostic_order` after this final sort.

Additional ordering rules:

- The first diagnostic has `diagnostic_order = 0`.
- `field_sort_rank` MAY exist as an internal transient sorting key.
- `field_sort_rank` MUST NOT appear in the public diagnostics DataFrame.
- Sorting directly and exclusively by alphabetic `field_name` is not compliant.
- Canonical required-field order MUST survive the final sort.
- Input CSV row order MUST NOT act as a tie-breaker.
- Order MUST be independent of raw CSV row order for canonically equivalent inputs.
- `diagnostic_order` MUST be recalculated from the final sorted output.
- Absolute paths MUST NOT appear.
- `raw_value` MUST be safe and bounded.
- Full rows MUST NOT be serialized.

## Stage A File Summary

Stage A calculates these fields from actual structural processing:

- `input_contract_version`
- `policy_version`
- `stage`
- `file_outcome`
- `total_rows`
- `accepted_rows`
- `rejected_rows`
- `diagnostics_by_severity`
- `diagnostics_by_code`

The remaining planned summary fields may exist with zero values to preserve the stable result shape:

- `accepted_with_warning_rows`
- `partially_accepted_rows`
- `review_required_rows`
- `accepted_observations`
- `review_required_observations`
- `rejected_field_observations`
- `duplicate_groups`
- `conflict_groups`
- `current_observations`
- `stale_observations`
- `unknown_freshness_observations`
- `not_applicable_observations`
- `future_invalid_observations`
- `market_value_zero_observation_count`
- `effective_eligible_observation_count`

Counts MUST reconcile. For a processable file, `accepted_rows + rejected_rows = total_rows`. When file rejection happens before rows can be interpreted safely, `total_rows` MAY be zero. The summary MUST NOT expose a complete input path.

## Approved Synthetic Fixtures

All fixture identities are fictitious. Any URL uses a reserved `.test` domain.

### `valid_minimal.csv`

- Contains one structurally valid row.
- Uses only values needed for structural validity.
- May leave `review_status` empty because its policy belongs to Stage B.
- Produces `file_outcome = accepted`, one accepted row and zero diagnostics.

### `structural_row_errors.csv`

Contains independent synthetic rows for:

- one required value missing;
- invalid season;
- naive `reviewed_at`; and
- invalid source type.

It MUST avoid Stage B errors.

### `duplicate_local_record_ids.csv`

- Contains at least two rows with the same exact non-empty ID.
- Rejects every implicated row.
- Produces results independent of input order.

BOM, undecodable bytes, invalid delimiters, duplicate headers, missing columns and other malformed file cases are generated only with `tmp_path`.

## Stage A Test Matrix

### API Boundary

- required path;
- file not found;
- `strict=False`;
- naive `ingested_at`;
- timezone-aware `ingested_at`;
- no printing or persistence; and
- no default-path or discovery behavior.

### File Validation

- valid UTF-8;
- UTF-8 BOM;
- invalid encoding;
- comma delimiter;
- semicolon delimiter;
- tab delimiter;
- duplicate headers;
- one missing required column;
- multiple missing required columns retaining canonical contract order;
- unknown columns retaining lexical order;
- unsupported schema version;
- mixed schema versions;
- a zero-byte file and a whitespace-only file;
- exactly one `MCV101_MISSING_REQUIRED_COLUMN` per required column for those files, in canonical order;
- no `MCV105_INVALID_DELIMITER` for those files;
- `file_outcome = rejected` with `total_rows = 0`, `accepted_rows = 0` and `rejected_rows = 0`;
- an empty `rejected_rows` DataFrame, no row diagnostics and no invented rows.

### Row Validation

- valid minimal row;
- each structural required value missing;
- whitespace-only required values;
- empty `season` emits only `MCV200_MISSING_REQUIRED_VALUE`;
- empty `reviewed_at` emits only `MCV200_MISSING_REQUIRED_VALUE`;
- empty `source_type` emits only `MCV200_MISSING_REQUIRED_VALUE`;
- populated invalid `season`, `reviewed_at` and `source_type` values emit `MCV202_INVALID_SEASON`, `MCV203_INVALID_REVIEWED_AT` and `MCV204_INVALID_SOURCE_TYPE`, respectively;
- valid season;
- every listed invalid season form;
- valid `reviewed_at` with `Z`;
- valid `reviewed_at` with an explicit offset;
- naive and malformed `reviewed_at`;
- every valid source type;
- invalid source type;
- duplicate local IDs;
- missing local IDs excluded from duplicate grouping;
- multiple diagnostics on one row; and
- valid and rejected rows in one file.

### Result Contract

- frozen dataclass;
- deterministic empty observation schemas;
- `rejected_rows` membership;
- no row invention on file rejection;
- summary reconciliation;
- exact diagnostics schema and ordering;
- row diagnostics for multiple fields retaining canonical field order;
- consecutive `diagnostic_order` from zero;
- repeated-execution equality;
- reordered canonically equivalent inputs producing identical diagnostics and `diagnostic_order` values; and
- no mutable output state shared with parsing internals.

## Verification Evidence

The completed Stage A implementation recorded:

- Python `3.12.13`;
- Stage A tests: `92 passed`;
- full test suite: `654 passed`;
- `python -m compileall src scripts`: passed;
- `git diff --check`: passed; and
- preview: not executed.

The repository `.venv\Scripts\python.exe` launcher pointed to a removed Python installation, so verification used the functional Python 3.12.13 interpreter without modifying the environment.

## Stage A Exclusions

The separate Stage A code block MUST NOT include:

- field observations;
- numeric Market Context parsing;
- market-value-zero behavior;
- confidence validation;
- salary or currency processing;
- contract-date processing;
- age or date-of-birth processing;
- jersey-number processing;
- position validation;
- freshness;
- warning or info diagnostics;
- duplicate observation analysis;
- conflicts or conflict-group IDs;
- effective-eligibility logic;
- preview CLI;
- SQLite;
- Streamlit;
- current loader changes;
- providers or API calls;
- real or ignored local data;
- automatic file discovery; or
- new dependencies.

## Stage A Completion Criteria

Stage A is implemented only when:

- all five authorized paths exist;
- the public API and frozen result contract are implemented;
- file diagnostics `MCV100` through `MCV105` work;
- row diagnostics `MCV200` through `MCV204` work;
- all three synthetic fixtures are versioned;
- Stage A tests pass;
- the full test suite passes;
- compileall passes;
- diff and status are reviewed;
- no change exists outside the approved paths; and
- no real data was used.

All Stage A completion criteria are met and recorded in the closeout.

## Stage A Decision Boundary

Stage A is implemented, verified and closed.

Stage A completion does not authorize Stage B or any later stage.

Stages B-D remain blocked. Stage A completion does not authorize preview, integration, effective processing or real data.

Next permitted action: define a separate Stage B approval decision docs-only.
