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

A row MAY retain valid field observations when another one of the seven Stage B Market Context observations is rejected. Structural or identity errors reject the complete row. `partially-accepted` applies only when one or more of the seven observations have field outcome `rejected`, at least one other provided observation survives with field outcome `accepted` or `accepted-with-warning`, and no row rule requires `review-required` or `rejected`. Rejection of metadata or provenance alone never produces `partially-accepted`.

Outcome precedence is:

1. `rejected`
2. `review-required`
3. `partially-accepted`
4. `accepted-with-warnings`
5. `accepted`

No silent fallback is allowed. `review-required` MUST NOT be converted automatically to an accepted outcome.

### Missing Optional Observation Precedence

The only Stage B optional observation fields are:

- `market_value_eur`
- `contract_end_date`
- `salary_value`
- `age`
- `date_of_birth`
- `jersey_number`
- `position`

For each of these seven fields, an absent optional column, null, empty or whitespace-only token:

- emits exactly one `MCV503_OPTIONAL_VALUE_MISSING`;
- has field outcome `not-provided`;
- creates no row in `accepted_observations`;
- creates no row in `review_required_observations`;
- does not reject the row by itself; and
- suppresses every later field-specific validation for that absent token.
- uses the absent observation field as `field_name`, preserves the safe empty token in `raw_value` and uses null `normalized_value`.

`MCV503_OPTIONAL_VALUE_MISSING` MUST NOT be emitted for `confidence`, `review_status`, `source_url`, `source_reference`, `salary_currency`, `salary_period`, `is_estimated`, auxiliary dates or other metadata.

Age is the sole sequencing exception: an absent `age` token is held pending the approved explicit-date derivation attempt. Successful derivation creates the age observation and suppresses `MCV503`; unsuccessful or unavailable derivation produces the normal single `MCV503`.

An optional column absent from the header is equivalent to an absent token for that observation or metadata field. For metadata:

- absent `review_status` is equivalent to null and follows `MCV408_MISSING_REVIEW_STATUS`;
- absent `source_url` and `source_reference` participate in `MCV400_MISSING_PROVENANCE_REFERENCE`;
- absent `confidence` follows the conditional confidence rules below; and
- absent metadata never emits `MCV503`.

Under Stage B, the unchanged Stage A fixture `valid_minimal.csv` therefore has this exact cumulative result:

- file outcome `accepted`;
- seven `MCV503_OPTIONAL_VALUE_MISSING` diagnostics;
- one `MCV408_MISSING_REVIEW_STATUS`;
- one `MCV400_MISSING_PROVENANCE_REFERENCE`;
- no `MCV303_MISSING_CONDITIONAL_METADATA`;
- no `MCV305_INVALID_CONFIDENCE`;
- no observation rows;
- final row outcome `review-required`;
- `review_required_rows = 1`;
- `accepted_rows = 0`; and
- `rejected_rows = 0`.

This changes only the Stage B expectations for the existing fixture. The Stage A fixture remains unchanged.

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
- A populated invalid field-specific value date emits one `MCV300_INVALID_DATE` with `field_name` set to that date column, preserves the safe original token in `raw_value`, uses null `normalized_value`, rejects every observation that depends on it and MUST NOT fall back to `value_date`.
- A populated invalid general `value_date`, when it is the selected fallback, emits one `MCV300_INVALID_DATE` with `field_name=value_date`, preserves the safe original token in `raw_value`, uses null `normalized_value`, rejects every observation that depends on it and MUST NOT become `unknown`.
- An invalid selected date suppresses `MCV401_UNKNOWN_VALUE_DATE` for every affected observation and produces no freshness count for those rejected observations.
- A future selected date emits one `MCV309_FUTURE_VALUE_DATE` per affected observation, with `field_name` set to the observation field and the ISO date in `raw_value` and `normalized_value`.
- A future selected date uses `future-invalid`, rejects the affected observation and suppresses `MCV401_UNKNOWN_VALUE_DATE` and `MCV402_STALE_VALUE`.

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

### Source URL Validation

A populated `source_url` is valid only when standard-library parsing confirms all of the following:

- scheme is exactly `http` or `https`;
- the URL is absolute;
- hostname is non-empty;
- username and password are absent;
- whitespace and control characters are absent;
- leading and trailing whitespace are absent; and
- no network request or meaning-changing URL normalization is required.

Reserved `.test` hostnames are valid for synthetic fixtures.

An invalid populated URL:

- emits exactly one `MCV310_INVALID_SOURCE_URL` for the row;
- uses `field_name=source_url`;
- preserves the bounded safe original token in `raw_value`;
- uses null `normalized_value`;
- has diagnostic field outcome `rejected`;
- rejects only the provenance field and does not reject any of the seven Market Context observations;
- does not independently change observation `effective_eligible`;
- does not increment `rejected_field_observations`;
- does not independently change the row outcome; and
- does not convert an otherwise `accepted` row to `partially-accepted`.

When the invalid URL is accompanied by no valid `source_reference`, emit the independent row warning `MCV400_MISSING_PROVENANCE_REFERENCE`, whose minimum row outcome remains `accepted-with-warnings`. A valid `source_reference` suppresses `MCV400` but not `MCV310`.

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

## Confidence Precedence

- When none of the seven Stage B observation fields is populated, empty `confidence` is valid and emits none of `MCV303`, `MCV305` or `MCV503`.
- When one or more observation fields are populated and `confidence` is absent, emit exactly one `MCV303_MISSING_CONDITIONAL_METADATA` for the row with `field_name=confidence`, the safe empty token in `raw_value` and null `normalized_value`.
- Missing confidence rejects every populated observation field. It does not emit one diagnostic per affected observation, and it MUST NOT also emit `MCV305` for the same token.
- When `confidence` is populated outside `low`, `medium` or `high`, emit exactly one `MCV305_INVALID_CONFIDENCE` for the row with `field_name=confidence`, the bounded safe original token in `raw_value` and null `normalized_value`.
- Invalid populated confidence rejects every populated observation field and MUST NOT also emit `MCV303` for the same token.
- If invalid populated confidence exists without any populated observation, the confidence metadata field is rejected and the row outcome is `rejected`.
- When missing or invalid confidence rejects all populated observations, the row outcome is `rejected`, subject to any independent higher-precedence row rejection already present.
- Each affected observation contributes at most once to `rejected_field_observations`, regardless of the single confidence diagnostic.

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
| `MCV303_MISSING_CONDITIONAL_METADATA` | error | field | field rejected | Required conditional metadata such as currency, period, estimate flag, age reference date or confidence is missing or is not validly supplied under its exact Stage B lexical contract. |
| `MCV304_INVALID_CURRENCY` | error | field | field rejected | Currency is not an approved uppercase ISO 4217 code. |
| `MCV305_INVALID_CONFIDENCE` | error | field | field rejected | Populated confidence is outside `low`, `medium`, `high`. |
| `MCV306_AGE_DATE_CONTRADICTION` | error | field | age and date-of-birth observations rejected | `age`, reference date and date of birth contradict one another. |
| `MCV307_INVALID_POSITION` | error | field | field rejected | A non-empty position token is one of the exact prohibited literal sentinels defined by the Stage B policy. |
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
- `salary_currency`, `salary_period` and `is_estimated` must be validly supplied when a salary value is present.
- `salary_period` allows exactly `annual`, `monthly` or `weekly`.
- `is_estimated` allows exactly lowercase `true` or `false`.
- Missing `salary_currency`, `salary_period` or `is_estimated` emits one `MCV303_MISSING_CONDITIONAL_METADATA` for each distinct defective metadata field.
- A populated `salary_period` outside its enum or a populated `is_estimated` outside its canonical boolean tokens emits `MCV303_MISSING_CONDITIONAL_METADATA` for that metadata field.
- Each `MCV303` uses the defective metadata column as `field_name`, preserves the bounded safe original token in `raw_value` and uses null `normalized_value`.
- An invalid populated `salary_currency` emits `MCV304_INVALID_CURRENCY` with `field_name=salary_currency` and MUST NOT also emit `MCV303` for that token.
- Multiple independent metadata defects may emit one diagnostic each, but the `salary_value` observation is rejected and counted only once in `rejected_field_observations`.
- One defective token MUST NOT emit multiple diagnostics for the same root cause.
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
- When `age`, `date_of_birth` and `age_reference_date` are valid but contradictory, emit exactly two `MCV306` diagnostics: one with `field_name=age` and one with `field_name=date_of_birth`.
- Each contradiction diagnostic preserves that field's bounded safe original token in `raw_value` and its parsed value in `normalized_value`.
- Both contradictory observations are rejected and contribute two rejected field observations; the pipeline MUST NOT choose one silently.
- Independent observations remain processable and row outcome follows the approved precedence.
- Age derivation is permitted only when `age` is absent and both `date_of_birth` and an explicitly populated `age_reference_date` are valid.
- Completed years are calculated exactly as `reference.year - birth.year - ((reference.month, reference.day) < (birth.month, birth.day))`.
- Derivation MUST NOT use `ingested_at`, `reviewed_at`, filesystem time or the current date.
- A derived age must be from 15 through 45 inclusive.
- A valid derived age creates an `age` observation with null `raw_value`, Python `int` `normalized_value`, `age_reference_date` as `effective_value_date`, normal age freshness and `MCV502_DERIVED_AGE`; it suppresses `MCV503` for `age`.
- When absent age cannot be derived, emit `MCV503` for `age` and invent no value.
- A populated age with absent `age_reference_date` emits `MCV303` for `age_reference_date`.
- A populated age with an invalid `age_reference_date` emits `MCV300` for `age_reference_date`.
- A populated age with invalid integer syntax or outside the approved range emits `MCV301` for `age`.

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

Position is evaluated verbatim after null, empty and whitespace-only detection. The general text-normalization algorithm is not applied to this field.

- Null, empty or whitespace-only emits only `MCV503_OPTIONAL_VALUE_MISSING`, has field outcome `not-provided` and emits neither `MCV307` nor `MCV409`.
- An exact canonical value may be accepted.
- The exact prohibited literal sentinel tokens are `N/A`, `unknown`, `-` and `null`. These emit `MCV307_INVALID_POSITION` and are rejected.
- No broader malformed-position predicate is approved in v1.
- Any other non-empty string outside the canonical taxonomy emits `MCV409_UNMAPPED_POSITION`, remains preserved for diagnostics and has field outcome `review-required`.
- Case differences, aliases and provider taxonomies are not converted to canonical values.
- No heuristic, fuzzy matching or transliteration is allowed.

## Exact Stage B Normalization Contract

| Input | Accepted lexical form | Normalized public value | Invalid behavior |
|---|---|---|---|
| `market_value_eur`, `salary_value` | `-?[0-9]+(?:\.[0-9]+)?`, where leading `-` is recognized only to classify a negative value | `decimal.Decimal`; numeric zero remains Decimal zero | negative emits `MCV302`; any other invalid token emits `MCV301`; never emit both for one token |
| `age` | `[0-9]+`, with no sign, decimal, exponent or whitespace; value 15-45 | Python `int` | invalid lexical form or range emits `MCV301` |
| `jersey_number` | `[0-9]+`, with no sign, decimal, exponent or whitespace; value 1-99 | Python `int` | invalid lexical form or range emits `MCV308` |
| Business dates and value dates | exact calendar-valid `YYYY-MM-DD` | ISO string `YYYY-MM-DD` | populated invalid token emits `MCV300` |
| `reviewed_at` | Stage A-valid timezone-aware ISO-8601 timestamp | `datetime.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")` | Stage A retains `MCV203`; Stage B does not reinterpret invalid timestamps |
| Safe text fields | any Stage A-valid non-missing string | NFKC, exterior trim and internal whitespace runs collapsed to one ASCII space | no aliases, case folding, accent removal, punctuation removal, transliteration or fuzzy matching |
| `position` | exact canonical values or other non-empty tokens under the finite position rules | unchanged string | exact sentinels emit `MCV307`; other non-canonical values emit `MCV409` |

Numeric rules:

- Monetary parsing MUST use `decimal.Decimal`, never binary float.
- Accepted monetary tokens MUST be converted with `Decimal(token)`.
- The parser MUST NOT call `.normalize()`, quantize or round accepted monetary values.
- Lexical scale is preserved: `1` becomes `Decimal("1")`, `1.0` becomes `Decimal("1.0")` and `1.00` becomes `Decimal("1.00")`.
- Numeric equality does not require representational equality, and the original raw token remains available for audit.
- At least one digit is required before an optional decimal point.
- Exponents, thousands separators, leading `+` and surrounding whitespace are invalid.
- Every token beginning with `-`, including `-0` and `-0.00`, is parsed only far enough to emit `MCV302_NEGATIVE_VALUE`.
- A negative-zero token creates no zero observation. Only non-negative lexical zero forms use the approved market-value-zero semantics.
- Syntactically valid monetary zero remains Decimal zero and MUST NOT become null.

Date and timestamp rules:

- Datetimes are not accepted as business dates or value dates.
- Local date formats and surrounding whitespace are invalid.
- UTC timestamp normalization preserves the instant.
- Fractional seconds are preserved only as produced by `datetime.isoformat()`.
- Emit `MCV501_NORMALIZED_TIMESTAMP` only when the canonical UTC representation differs from the valid original token.

The text algorithm runs in this exact order: (1) `unicodedata.normalize("NFKC", token)`, (2) remove leading and trailing Unicode whitespace, and (3) replace every maximal internal Unicode-whitespace run with one ASCII space (`U+0020`).

Safe text normalization applies exactly to:

- `player`
- `team`
- `league`
- `source_name`
- `source_reference`
- `reviewer`

It does not apply automatically to `season`, URLs, enum fields, numeric fields, dates, `position`, `notes` or `review_notes`.

- Public identity and provenance output values use the normalized text.
- Diagnostic `raw_value` retains the bounded safe original token.
- Emit one `MCV500_NORMALIZED_TEXT` per changed field, using that field as `field_name`.
- Preserve case, accents and punctuation.
- Private complete sorting keys remain internal and MUST NOT appear in public outputs.

Public logical types are frozen for Stage B:

| Output value | Logical type |
|---|---|
| Monetary normalized values | `decimal.Decimal` |
| `age`, `jersey_number` | Python `int` |
| Business dates and effective dates | ISO `YYYY-MM-DD` strings |
| `position` | Python `str` |
| `reviewed_at` | canonical UTC string |
| Missing normalized values | `None` |
| `effective_eligible` | Python `bool` |
| `conflict_group_id` | `None` throughout Stage B |

## Static Currency Validation

Stage B may validate salary currency with one explicit static immutable set of accepted alphabetic ISO 4217 codes in `src/manual_market_context_processing.py`.

- Tokens must be exactly three ASCII uppercase letters.
- Membership validation is case-sensitive.
- Lowercase tokens, symbols and free-form names are invalid.
- No case normalization, currency conversion, network access or runtime lookup is allowed.
- The future code diff MUST expose the complete set for review and tests.
- No new dependency, including pycountry, Babel, Pydantic or Pandera, is approved.

## Stage B Diagnostic And Outcome Reconciliation

- Missing-value checks run before field-specific validation.
- A missing optional observation emits only its single `MCV503`.
- Missing confidence uses `MCV303`; invalid populated confidence uses `MCV305`; the two are mutually exclusive for one token.
- Missing or invalid salary metadata uses the exact one-root-cause rules above.
- Diagnostics affecting multiple observations may reject each affected observation while emitting only the approved metadata diagnostic cardinality.
- `MCV306` emits exactly twice for one age/date-of-birth contradiction.
- `MCV503` emits at most once for each absent one of the seven observation fields.
- Row-scope diagnostics follow their approved minimum row outcomes.
- Field-observation diagnostics determine the affected observation outcome; independent valid observations survive.
- `rejected_field_observations` counts only rejected observations among the seven Stage B Market Context fields, once per observation.
- Rejected metadata or provenance fields do not increment `rejected_field_observations`.
- `MCV405_DUPLICATE_OBSERVATION` and `MCV406_CONFLICTING_OBSERVATION` MUST NOT be emitted in Stage B.
- Every summary count MUST reconcile with final public outputs and diagnostics.
- Final deterministic sorting precedes assignment of zero-based consecutive `diagnostic_order`.
- Pandas indexes and physical CSV row order MUST NOT be used as identity or tie-breakers.

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
- This policy does not independently approve code; the separate Stage B decision authorizes the bounded future Stage B behavior, which is not implemented.
- A future integration decision MAY preserve this separation or change effective semantics with an explicit decision and tests.

The contract version remains `manual-market-context-input-v1`: the field name and representation are unchanged, the effective destination is clarified, Stage A remains intact and Stage B behavior is not yet implemented.

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

Final observation partitioning occurs only after all field outcomes and the final row outcome are known:

- A `not-provided` field appears in neither observation DataFrame, may be represented by `MCV503` and increments no accepted, review-required or rejected observation count.
- A `rejected` field appears in neither observation DataFrame. It increments `rejected_field_observations` exactly once only when it is one of the seven observation fields; rejected metadata or provenance does not increment that count.
- For final row outcome `accepted`, every observation with field outcome `accepted` goes to `accepted_observations`.
- For final row outcome `accepted-with-warnings`, every observation with field outcome `accepted` or `accepted-with-warning` goes to `accepted_observations` and preserves its exact field outcome.
- Final row outcome `partially-accepted` is available only when one or more of the seven observations are rejected, at least one other provided observation survives as `accepted` or `accepted-with-warning`, and no row rule requires `review-required` or `rejected`. Every surviving observation goes to `accepted_observations`; rejected observations remain outside both observation DataFrames, and the row does not appear in `rejected_rows`. Isolated metadata or provenance rejection never selects this outcome.
- For final row outcome `review-required`, every provided, non-rejected observation goes to `review_required_observations`; its existing field outcome is preserved when a row rule caused review, while an observation that caused review, including `MCV409`, uses field outcome `review-required`. No observation from that row appears in `accepted_observations`, and the row does not appear in `rejected_rows`.
- For final row outcome `rejected`, no observation appears in either observation DataFrame and the row appears exactly once in `rejected_rows`. Row rejection does not automatically convert otherwise valid observations into rejected field observations.

The five row counters are mutually exclusive and sum to `total_rows` for a processable file. Summary observation counts equal the row counts of their corresponding DataFrames. `rejected_field_observations` follows the seven-field rule above. Info diagnostics do not change row outcome by themselves. All partitions are complete before final summary construction.

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

- Stage B code and fixtures except through the separate Stage B decision.
- Stage C duplicate/conflict implementation.
- Stage D preview implementation and execution.
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
- Stage A is completed and closed.
- Stage B code and its seven fixtures are authorized only by the separate Stage B decision and are not implemented.
- Stages C-D remain blocked.
- Real-data access is not authorized.
- Preview is not authorized.
- SQLite and Streamlit are not authorized.
- No provider is approved.

The bounded [implementation plan](v0_10_0_manual_market_context_implementation_plan.md) and its [decision](provider_decisions/v0_10_0_manual_market_context_implementation_plan_decision.md) remain approved. Stage A is closed. The separate Stage B decision approves only its bounded future implementation, which has not started. Stages C-D remain blocked.
