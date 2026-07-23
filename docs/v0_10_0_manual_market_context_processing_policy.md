# v0.10.0 Reviewed Local Market Context Processing Policy

## Status

- Milestone: v0.10.0
- Policy status: `manual-market-context-processing-policy-defined`
- Policy version: `manual-market-context-policy-v1`
- Input contract: [v0.10.0 Reviewed Local Market Context Input Contract](v0_10_0_manual_market_context_input_contract.md)
- Input contract version: `manual-market-context-input-v1`
- Related scope plan: [v0.10.0 Manual Market Context Workflow Hardening Scope Plan](v0_10_0_manual_market_context_scope_plan.md)
- Related scope decision: [v0.10.0 Manual Market Context Workflow Scope Decision](provider_decisions/v0_10_0_manual_market_context_scope_decision.md)
- Related policy decision: [v0.10.0 Reviewed Local Market Context Processing Policy Decision](provider_decisions/v0_10_0_manual_market_context_processing_policy_decision.md)
- Implementation plan: [v0.10.0 Reviewed Local Market Context Implementation Plan](v0_10_0_manual_market_context_implementation_plan.md)
- Implementation plan decision: [v0.10.0 Reviewed Local Market Context Implementation Plan Decision](provider_decisions/v0_10_0_manual_market_context_implementation_plan_decision.md)
- Implementation approved: no
- Parser approved: no
- Synthetic fixtures approved: no
- Preview approved: no
- Real local data access approved: no
- SQLite writes approved: no
- Streamlit changes approved: no
- Provider approval: none

## Purpose

This policy defines how a future parser and validation pipeline must interpret, diagnose and classify reviewed local Market Context observations.

The policy:

- complements `manual-market-context-input-v1`;
- does not modify or access real data;
- does not consolidate observations into effective records;
- defines no commercial precedence between sources;
- authorizes no persistence, UI integration or provider integration; and
- requires deterministic, reconcilable and diagnosable results.

## Processing Units

### File

A file is the complete reviewed local CSV input.

Allowed outcomes:

- `accepted`
- `rejected`

A structural file error rejects the file and blocks normal row processing.

### Row

A row is one observation identified by `local_record_id`.

Allowed outcomes:

- `accepted`
- `accepted-with-warnings`
- `partially-accepted`
- `review-required`
- `rejected`

### Field Observation

A field observation is one Market Context field within a row, including:

- `market_value_eur`
- `contract_end_date`
- `salary_value`
- `age`
- `date_of_birth`
- `jersey_number`
- `position`

Allowed outcomes:

- `accepted`
- `accepted-with-warning`
- `review-required`
- `rejected`
- `not-provided`

A row MAY retain valid field observations when another field observation is rejected. Structural or identity errors reject the complete row. `partially-accepted` applies when at least one field is accepted and at least one field is rejected, unless a row-level rule requires `review-required` or `rejected`.

Outcome precedence is:

1. `rejected`
2. `review-required`
3. `partially-accepted`
4. `accepted-with-warnings`
5. `accepted`

No silent fallback is allowed. `review-required` MUST NOT be converted automatically to an accepted outcome.

## Date Resolution Policy

The effective value date for freshness is resolved per field:

| Field Observation | First Choice | Fallback | Final State |
|---|---|---|---|
| `market_value_eur` | `market_value_value_date` | `value_date` | unknown |
| `salary_value` | `salary_value_date` | `value_date` | unknown |
| `contract_end_date` information | `contract_value_date` | `value_date` | unknown |
| `age` | `age_reference_date` | none | unknown |
| `date_of_birth` | not applicable | not applicable | not applicable |
| `jersey_number` | `value_date` | none | unknown |
| `position` | `value_date` | none | unknown |

Rules:

- `reviewed_at` MUST NOT substitute for a value date.
- `ingested_at` MUST NOT substitute for a value date.
- Filesystem modification time MUST NOT be used.
- `contract_end_date` is a business value, not the observation date.
- An unknown effective value date emits `MCV401_UNKNOWN_VALUE_DATE` when the field value is populated.
- A field-specific date later than the UTC calendar date represented by future pipeline-generated `ingested_at` emits `MCV309_FUTURE_VALUE_DATE` and rejects that field.
- The same future-date rule applies to general `value_date` when it supplies the effective field date.

## Freshness Classification

Allowed freshness states:

- `current`
- `stale`
- `unknown`
- `not-applicable`
- `future-invalid`

Freshness age is the whole-calendar-day difference between the UTC date of future pipeline-generated `ingested_at` and the resolved effective value date.

| Field | Current | Stale |
|---|---|---|
| `market_value_eur` | age <= 180 days | age > 180 days |
| `salary_value` | age <= 180 days | age > 180 days |
| `contract_end_date` information | age <= 365 days | age > 365 days |
| `age` | age <= 365 days | age > 365 days |
| `jersey_number` | age <= 180 days | age > 180 days |
| `position` | age <= 180 days | age > 180 days |
| `date_of_birth` | not applicable | not applicable |

Rules:

- `stale` does not reject a field automatically.
- `stale` emits `MCV402_STALE_VALUE`.
- `unknown` emits `MCV401_UNKNOWN_VALUE_DATE` when a value is present.
- A negative freshness age is `future-invalid`, emits `MCV309_FUTURE_VALUE_DATE` and rejects the field.
- These thresholds are v1 policy choices, not provider facts.
- Changing a threshold requires a separate documentation decision.
- A newer `reviewed_at` MUST NOT make an older observation appear current.

## Provenance Policy

- `source_name`, `source_type`, `reviewed_at` and `reviewer` are required.
- At least one of `source_url` or `source_reference` SHOULD be present.
- Absence of both emits `MCV400_MISSING_PROVENANCE_REFERENCE`.
- An invalid populated `source_url` emits `MCV310_INVALID_SOURCE_URL` for that provenance field.
- `source_type` establishes neither confidence nor precedence.
- `reviewer` establishes neither source authority nor value precedence.
- `confidence` describes confidence in the observation, not legal permission.
- Declared provenance grants no permission to access, reuse or redistribute data.
- `notes`, references and diagnostics MUST NOT contain payloads, credentials or secrets.
- When normalized references are identical, a changed `source_name` label does not create a different source identity for duplicate/conflict detection.
- Identical references do not authorize automatic row merging.
- No precedence exists between source types.

For deterministic grouping, source identity uses normalized `source_url` when present, otherwise normalized `source_reference`, otherwise normalized `source_name` with `source_type`. This identity is diagnostic metadata only and does not merge observations.

## Review Status Policy

### `reviewed`

- The row may qualify for acceptance.
- Validation, duplicate and conflict rules still apply.

### `needs-review`

- Minimum row outcome: `review-required`.
- Emit `MCV404_NEEDS_REVIEW_STATUS`.
- The row MUST NOT enter a future effective output.
- The row MUST remain visible in diagnostics and a future review preview.

### `rejected`

- Row outcome: `rejected`.
- Emit `MCV206_REJECTED_REVIEW_STATUS`.
- Its values MUST NOT become effective candidates.
- The row remains represented in diagnostics.

### Null

- In strict v1, null emits `MCV408_MISSING_REVIEW_STATUS`.
- Minimum row outcome: `review-required`.
- A future implementation MUST NOT infer review status from the filename.
- Treating null as `reviewed` requires a separate explicit decision.

## Validation Severity Model

Severities:

- `error`
- `warning`
- `info`

Scopes:

- `file`
- `row`
- `field`
- `conflict-group`

Rules:

- A file-scoped error rejects the file.
- A row-scoped error rejects the row.
- A field-scoped error rejects that field; the row may remain partially accepted.
- A warning preserves the affected element unless its diagnostic default outcome is `review-required`.
- An info diagnostic does not alter acceptance.
- Every diagnostic MUST identify `severity`, `scope`, `diagnostic_code`, `message`, and the applicable row, field or conflict group.

## Diagnostic Record Contract

| Column | Meaning |
|---|---|
| `diagnostic_code` | Stable machine-readable code. |
| `severity` | `error`, `warning` or `info`. |
| `scope` | `file`, `row`, `field` or `conflict-group`. |
| `message` | Human-readable explanation. |
| `local_record_id` | Affected row, when applicable. |
| `field_name` | Affected field, when applicable. |
| `conflict_group_id` | Deterministic conflict group, when applicable. |
| `raw_value` | Original safe value; never secrets or payload content. |
| `normalized_value` | Normalized value, when one exists. |
| `row_outcome` | Resulting row outcome. |
| `field_outcome` | Resulting field outcome. |

Diagnostic codes MUST remain stable. Messages MAY improve without changing code meaning. Diagnostic ordering MUST be deterministic, and one issue MUST NOT emit unnecessary duplicates.

## Diagnostic Catalog v1

### File Errors

| Code | Severity | Scope | Default Outcome | Meaning |
|---|---|---|---|---|
| `MCV100_UNSUPPORTED_SCHEMA_VERSION` | error | file | file rejected | `schema_version` is absent, inconsistent or unsupported. |
| `MCV101_MISSING_REQUIRED_COLUMN` | error | file | file rejected | A required header is missing. |
| `MCV102_DUPLICATE_HEADER` | error | file | file rejected | A header occurs more than once. |
| `MCV103_UNKNOWN_COLUMN` | error | file | file rejected | Strict mode found a column outside the approved contract. |
| `MCV104_INVALID_ENCODING` | error | file | file rejected | Encoding is not accepted by the input contract. |
| `MCV105_INVALID_DELIMITER` | error | file | file rejected | The file does not use the canonical delimiter. |

### Row Errors

| Code | Severity | Scope | Default Outcome | Meaning |
|---|---|---|---|---|
| `MCV200_MISSING_REQUIRED_VALUE` | error | row | row rejected | A required structural or identity value is missing. |
| `MCV201_DUPLICATE_LOCAL_RECORD_ID` | error | row | all implicated rows rejected | `local_record_id` occurs more than once. |
| `MCV202_INVALID_SEASON` | error | row | row rejected | `season` is not the canonical four-digit token. |
| `MCV203_INVALID_REVIEWED_AT` | error | row | row rejected | `reviewed_at` is invalid, naive or lacks a timezone designator. |
| `MCV204_INVALID_SOURCE_TYPE` | error | row | row rejected | `source_type` is outside the approved enum. |
| `MCV205_INVALID_REVIEW_STATUS` | error | row | row rejected | Populated `review_status` is outside the approved enum. |
| `MCV206_REJECTED_REVIEW_STATUS` | error | row | row rejected | Human review explicitly rejected the row. |

### Field Errors

| Code | Severity | Scope | Default Outcome | Meaning |
|---|---|---|---|---|
| `MCV300_INVALID_DATE` | error | field | field rejected | A field date is invalid or non-ISO. |
| `MCV301_INVALID_NUMBER` | error | field | field rejected | A numeric field cannot be parsed canonically. |
| `MCV302_NEGATIVE_VALUE` | error | field | field rejected | A non-negative value field contains a negative number. |
| `MCV303_MISSING_CONDITIONAL_METADATA` | error | field | field rejected | Required metadata such as currency, period, estimate flag, age reference date or confidence is missing. |
| `MCV304_INVALID_CURRENCY` | error | field | field rejected | Currency is not an approved uppercase ISO 4217 code. |
| `MCV305_INVALID_CONFIDENCE` | error | field | field rejected | Confidence is required or outside `low`, `medium`, `high`. |
| `MCV306_AGE_DATE_CONTRADICTION` | error | field | age and date-of-birth observations rejected | `age`, reference date and date of birth contradict one another. |
| `MCV307_INVALID_POSITION` | error | field | field rejected | Position is empty, malformed or structurally invalid. |
| `MCV308_INVALID_JERSEY_NUMBER` | error | field | field rejected | Jersey number is outside 1 through 99 or is not an integer. |
| `MCV309_FUTURE_VALUE_DATE` | error | field | field rejected | Effective value date is later than `ingested_at`. |
| `MCV310_INVALID_SOURCE_URL` | error | field | provenance field rejected | A populated source URL is invalid. |

### Warnings

| Code | Severity | Scope | Default Outcome | Meaning |
|---|---|---|---|---|
| `MCV400_MISSING_PROVENANCE_REFERENCE` | warning | row | accepted-with-warnings | Both source URL and source reference are absent. |
| `MCV401_UNKNOWN_VALUE_DATE` | warning | field | accepted-with-warning | A populated value has no effective value date. |
| `MCV402_STALE_VALUE` | warning | field | accepted-with-warning | A value exceeds its v1 freshness threshold. |
| `MCV403_ESTIMATED_VALUE` | warning | field | accepted-with-warning | A value, currently salary, is declared estimated. |
| `MCV404_NEEDS_REVIEW_STATUS` | warning | row | review-required | Human review status is `needs-review`. |
| `MCV405_DUPLICATE_OBSERVATION` | warning | conflict-group | accepted-with-warnings | Equivalent observations have distinct local record IDs. |
| `MCV406_CONFLICTING_OBSERVATION` | warning | conflict-group | review-required | Observations conflict under the v1 grouping rules. |
| `MCV407_MARKET_VALUE_ZERO_NOT_EFFECTIVE` | warning | field | accepted-with-warning | Zero market value is preserved as an observation but is not currently effective-eligible. |
| `MCV408_MISSING_REVIEW_STATUS` | warning | row | review-required | Strict v1 found null review status. |
| `MCV409_UNMAPPED_POSITION` | warning | field | review-required | Non-empty position is outside the canonical taxonomy. |

### Info

| Code | Severity | Scope | Default Outcome | Meaning |
|---|---|---|---|---|
| `MCV500_NORMALIZED_TEXT` | info | field | accepted | Text normalization changed a safe value. |
| `MCV501_NORMALIZED_TIMESTAMP` | info | field | accepted | A timezone-aware timestamp was normalized while preserving its instant. |
| `MCV502_DERIVED_AGE` | info | field | accepted | Age was derived deterministically using an explicit date. |
| `MCV503_OPTIONAL_VALUE_MISSING` | info | field | not-provided | An optional value is absent. |

No diagnostic code is provider-specific. Final implementation wording may improve, but code, severity, scope and default outcome changes require a policy decision.

## Value Validation Rules

### Market Value

- Null means `not-provided`.
- A negative value emits `MCV302_NEGATIVE_VALUE` and rejects the field.
- A positive value is accepted when its other metadata is valid.
- Zero follows [Market Value Zero Resolution](#market-value-zero-resolution).
- No currency conversion is approved.
- `market_value_eur` MUST NOT be interpreted as a transfer fee.

### Salary

- A negative value emits `MCV302_NEGATIVE_VALUE` and rejects the field.
- Currency, period and `is_estimated` are required when a salary value is present.
- Missing conditional metadata emits `MCV303_MISSING_CONDITIONAL_METADATA`.
- `is_estimated=true` emits `MCV403_ESTIMATED_VALUE`.
- A declared zero is preserved as zero.
- No canonical salary mapping or effective integration is approved.

### Contract End

- `contract_end_date` MUST be a valid ISO date.
- It MAY precede `reviewed_at` without being structurally impossible.
- The pipeline MUST NOT infer automatically that a contract is active or expired.
- A future observation date emits `MCV309_FUTURE_VALUE_DATE`.
- Derived contractual status remains out of scope.

### Age And Date Of Birth

- `age` MUST be an integer from 15 through 45.
- `age_reference_date` is required when `age` is present.
- A contradiction with `date_of_birth` emits `MCV306_AGE_DATE_CONTRADICTION`.
- Both contradictory age observations are rejected; the pipeline MUST NOT choose one silently.
- Future derivation MUST be deterministic and use an explicit reference date.

### Jersey Number

- Accepted range: integer 1 through 99.
- Null means `not-provided`.
- Zero is invalid.
- A non-integer or out-of-range value emits `MCV308_INVALID_JERSEY_NUMBER`.

### Position

The versioned canonical normalization in `src/api_football_canonical.py` defines these exact canonical values:

- `Goalkeeper`
- `Defender`
- `Midfielder`
- `Forward`

An exact canonical value may be accepted. A non-empty string outside this taxonomy emits `MCV409_UNMAPPED_POSITION`, remains preserved for diagnostics and receives `review-required`. Empty, malformed or structurally invalid values emit `MCV307_INVALID_POSITION` and are rejected. No provider taxonomy is converted silently.

## Duplicate Policy

### Duplicate Local Record Identifier

The same `local_record_id` more than once emits `MCV201_DUPLICATE_LOCAL_RECORD_ID`. Every implicated row is rejected. File order MUST NOT select a winner.

### Exact Duplicate Observation

An exact duplicate has the same:

- normalized compound identity;
- field name;
- normalized value;
- effective value date or explicit unknown marker; and
- normalized source identity/reference.

Distinct `local_record_id` values do not make the observations semantically different. Emit `MCV405_DUPLICATE_OBSERVATION`, preserve the observations, assign a deterministic conflict group, and select no effective winner.

### Repeated Historical Observation

The same identity and field at different effective dates is not a duplicate by itself. Both observations MAY coexist. The newest observation MUST NOT be selected automatically, and freshness is calculated independently.

## Conflict Policy

Conflict detection operates on field observations.

The base conflict group contains:

- normalized `player`;
- normalized `team`;
- normalized `league`;
- canonical `season`;
- `field_name`; and
- effective value date or an explicit unknown marker.

### Same Source And Date, Different Values

Emit `MCV406_CONFLICTING_OBSERVATION`. The conflict group and all implicated observations are `review-required`. The latest row MUST NOT win.

### Different Sources, Same Date, Different Values

Emit `MCV406_CONFLICTING_OBSERVATION`. All implicated observations are `review-required`. There is no source precedence and no automatic confidence derived from `source_type`.

### Different Dates, Different Values

These are historical observations, not an automatic conflict. Both MAY coexist. No value is selected automatically, and freshness is calculated separately.

### Unknown Dates, Different Values

The conflict group is `review-required`. Emit `MCV406_CONFLICTING_OBSERVATION` and `MCV401_UNKNOWN_VALUE_DATE`. The pipeline MUST NOT assume simultaneity or ordering.

### Null Versus Populated Value

For the same source, effective date and field, null versus populated is a conflict. Emit `MCV406_CONFLICTING_OBSERVATION`; do not prefer the populated value automatically. Null continues to mean unknown.

### Age Versus Date Of Birth Contradiction

Do not hide this contradiction through general source policy. Emit `MCV306_AGE_DATE_CONTRADICTION`; reject both affected field observations and allow unrelated valid fields to remain.

## Deterministic Conflict Group IDs

A future `conflict_group_id` MUST derive from a stable canonical representation of:

- compound identity;
- field name; and
- effective value date or an explicit unknown marker.

It MUST NOT depend on:

- row number;
- input order;
- filesystem timestamp; or
- a non-deterministic hash.

The cryptographic algorithm is deferred. Stability for identical canonical input is mandatory.

## Market Value Zero Resolution

### Observation Semantics

- `market_value_eur = 0` is a real declared value distinct from null.
- A conforming future parser MUST accept and preserve a structurally valid zero as a normalized observation.
- It MUST preserve the numeric value as zero and MUST NOT convert it to null.

### Effective Eligibility

- It MUST emit `MCV407_MARKET_VALUE_ZERO_NOT_EFFECTIVE`.
- Field outcome: `accepted-with-warning`.
- Minimum row outcome: `accepted-with-warnings`.
- The observation remains in `accepted_observations` unless another independent rule rejects or places the row or field under review.
- It MUST NOT promote zero to `effective_market_value_eur` under current effective behavior.
- It MUST NOT increase effective market-value coverage.

### Resolution Status

- Parser blocker: resolved.
- Effective integration behavior: explicitly limited.
- Current runtime behavior is unchanged.
- No code change is approved.
- A future integration decision MAY preserve this separation or change effective semantics with an explicit decision and tests.

The contract version remains `manual-market-context-input-v1`: the field name and representation are unchanged, the effective destination is clarified, and no approved implementation exists to break.

## Output Disposition Model

Future logical outputs are:

- `accepted_observations`
- `review_required_observations`
- `rejected_rows`
- `diagnostics`
- `file_summary`

No physical path, file format or persistence target is approved.

- An accepted observation is not automatically effective.
- A partially accepted row may contribute accepted and rejected field observations.
- `review-required` MUST NOT be promoted automatically.
- File, row, field and diagnostic counts MUST be deterministic and reconcilable.

## Deterministic Ordering

Diagnostics order:

1. severity: `error`, `warning`, `info`;
2. canonical `local_record_id` order, with file diagnostics first;
3. field name;
4. diagnostic code;
5. conflict group ID.

Observation order:

1. compound identity;
2. field name;
3. effective value date, with unknown last;
4. source name;
5. local record ID.

Original CSV order MUST NOT have semantic meaning.

## Explicitly Deferred

- Parser implementation.
- DataFrame schema.
- Python types.
- Fixture files.
- Preview/report layout.
- Physical output paths.
- Currency conversion.
- Identity crosswalks.
- Effective-field consolidation.
- Source precedence.
- Automatic conflict resolution.
- SQLite.
- Streamlit.
- Real-data migration.
- Production usage.

## Policy Decision Boundary

`manual-market-context-policy-v1` is defined docs-only, and `manual-market-context-input-v1` remains approved.

- The `market_value_eur = 0` parser blocker is resolved through observation/effective separation.
- Parser and fixture implementation are not authorized.
- Real-data access is not authorized.
- Preview is not authorized.
- SQLite and Streamlit are not authorized.
- No provider is approved.

The bounded [implementation plan](v0_10_0_manual_market_context_implementation_plan.md) and its [decision](provider_decisions/v0_10_0_manual_market_context_implementation_plan_decision.md) are approved docs-only. Implementation remains blocked. The next decision may approve Stage A core contract and file-validation implementation only; Stages B-D remain blocked.
