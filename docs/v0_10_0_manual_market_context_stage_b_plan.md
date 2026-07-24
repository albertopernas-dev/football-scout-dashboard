# v0.10.0 Reviewed Local Market Context Stage B Plan

## Status

- Milestone: v0.10.0
- Stage: B
- Stage name: Row And Field Normalization
- Plan status: `manual-market-context-stage-b-plan-defined`
- Input contract: [v0.10.0 Reviewed Local Market Context Input Contract](v0_10_0_manual_market_context_input_contract.md)
- Input contract version: `manual-market-context-input-v1`
- Processing policy: [v0.10.0 Reviewed Local Market Context Processing Policy](v0_10_0_manual_market_context_processing_policy.md)
- Processing policy version: `manual-market-context-policy-v1`
- Implementation plan: [v0.10.0 Reviewed Local Market Context Implementation Plan](v0_10_0_manual_market_context_implementation_plan.md)
- Implementation-plan decision: [v0.10.0 Reviewed Local Market Context Implementation Plan Decision](provider_decisions/v0_10_0_manual_market_context_implementation_plan_decision.md)
- Stage A closeout: [v0.10.0 Reviewed Local Market Context Stage A Closeout](v0_10_0_manual_market_context_stage_a_closeout.md)
- Stage A closeout decision: [v0.10.0 Reviewed Local Market Context Stage A Closeout Decision](provider_decisions/v0_10_0_manual_market_context_stage_a_closeout_decision.md)
- Stage B decision: [v0.10.0 Reviewed Local Market Context Stage B Decision](provider_decisions/v0_10_0_manual_market_context_stage_b_decision.md)
- Stage A completed: yes
- Stage B implementation approved: yes, for a separate code block
- Stage B implemented: no
- Stage C approved: no
- Stage D approved: no
- Real data approved: no
- Preview approved: no
- SQLite approved: no
- Streamlit approved: no
- Provider approval: none
- New dependencies approved: no

## Purpose

Stage B implements only the approved row and field normalization layer on top of the closed Stage A structural boundary.

Stage A already owns:

- strict UTF-8, delimiter and header validation;
- contract-version validation;
- required-column and unknown-column handling;
- required structural values;
- canonical season structure;
- timezone-aware `reviewed_at` validation;
- approved `source_type` validation;
- duplicate `local_record_id` rejection;
- deterministic Stage A diagnostics, rejected rows and summary structure; and
- empty-file semantics.

Stage B adds:

- compound identity normalization without fuzzy matching;
- null and empty semantics for optional values;
- canonical numeric, date, timestamp and boolean parsing;
- confidence and review-status validation;
- provenance-reference and source-URL validation;
- salary metadata validation without currency conversion;
- canonical position and jersey-number validation;
- market-value-zero observation behavior;
- value-date resolution and freshness classification;
- field and row outcomes;
- observation output population;
- observation-level effective eligibility; and
- the Stage B diagnostics approved below.

Stage C retains duplicate-observation grouping, historical grouping, conflicts, conflict-group identifiers, source identity construction for grouping, output disposition after conflicts and conflict-order reconciliation.

Stage D retains the synthetic preview CLI and all preview execution.

Stage B MUST preserve the Stage A contract and MUST NOT redesign, weaken or reinterpret Stage A behavior.

## Approved Future Files

The future Stage B implementation may modify or create only these exact paths:

| Path | Stage B responsibility |
|---|---|
| `src/manual_market_context_processing.py` | Extend the existing processor with approved Stage B normalization, validation, freshness, outcomes, observations, diagnostics and summary counts. |
| `tests/test_manual_market_context_processing.py` | Add Stage B unit, contract, regression and determinism coverage while retaining every Stage A regression case under the limited expectation migration below. |
| `tests/fixtures/manual_market_context/valid_full.csv` | Fully populated valid synthetic v1 values and observation outputs. |
| `tests/fixtures/manual_market_context/market_value_zero.csv` | Exact zero preservation, warning, outcome and effective-ineligibility behavior. |
| `tests/fixtures/manual_market_context/row_errors.csv` | Stage B review-status row outcomes; Stage A structural cases continue to use existing fixtures. |
| `tests/fixtures/manual_market_context/field_errors.csv` | Date, numeric, conditional metadata, currency, confidence, URL, jersey, prohibited position sentinel and unmapped position cases. |
| `tests/fixtures/manual_market_context/freshness_cases.csv` | Exact current, stale, unknown, `not-applicable` and `future-invalid` boundaries. |
| `tests/fixtures/manual_market_context/positions.csv` | Four canonical position values plus invalid and unmapped synthetic values. |
| `tests/fixtures/manual_market_context/partial_acceptance.csv` | Accepted and rejected field observations within the same structurally valid row. |

The future code block MUST NOT:

- modify the three closed Stage A fixtures;
- create `file_schema_errors.csv`, `duplicates.csv` or `conflicts.csv`;
- create a preview script or preview test;
- modify `src/market_context.py`;
- modify README or documentation;
- use wildcard or generic path approval; or
- add files for speculative future use.

Malformed byte, header or ad hoc edge cases that do not justify a fixture remain generated through `tmp_path` in the existing test module.

## Public API Boundary

Stage B preserves the implemented public API exactly:

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

- The function name and signature MUST NOT change.
- `input_path` remains required and has no default.
- `ingested_at` remains required, keyword-only and timezone-aware.
- `strict=True` remains the only approved mode.
- The stable `strict=False is not approved for Stage A` behavior remains unchanged.
- The processor MUST NOT discover files or define a default path.
- It MUST NOT call an internal clock.
- It MUST NOT print, preview, persist or call the existing Market Context loader.
- It MUST NOT read SQLite, provider cache or ignored local CSVs.

Private helpers may be added inside `src/manual_market_context_processing.py` for deterministic Stage B transformations. They do not create a second public processing API.

## Stage A Compatibility Boundary

Stage B MUST preserve:

- all eleven Stage A diagnostic codes, severities, scopes and meanings;
- stable Stage A messages where tests make them contractual;
- file-validation phase ordering;
- required-value validation before field-specific structural validation;
- empty and whitespace-only file behavior;
- duplicate `local_record_id` rejection for every implicated row;
- deterministic result, observation, rejected-row and diagnostic schemas;
- complete public `local_record_id` traceability;
- bounded safe public `raw_value` and `safe_row_reference` values;
- zero-based consecutive `diagnostic_order`;
- private deterministic sorting keys;
- no pandas index or physical CSV row order as semantic identity; and
- `duplicate_groups == 0` until Stage C.

Stage B may add diagnostics to structurally processable rows. It MUST NOT turn a Stage A file error into recoverable row processing or suppress an independent Stage A diagnostic.

Every Stage A case remains as regression coverage. Expectations may change only where Stage B expressly changes:

- the stage marker;
- the total implemented diagnostic catalog;
- later diagnostics applicable to structurally valid rows;
- observation outputs; or
- Stage B summary counts.

The eleven Stage A diagnostics retain their exact triggers, scopes, severities, ordering and precedence. A Stage A file error emits no Stage B diagnostic, and a row rejected by Stage A structural validation does not continue into Stage B processing. Stage A tests MUST NOT be deleted to make Stage B pass. Tests may be renamed or split only to distinguish the frozen Stage A contract from the cumulative Stage B contract.

The future Stage B block is expressly authorized to:

- change `STAGE_NAME` from `"A"` to `"B"`;
- expect `file_summary["stage"] == "B"` for every Stage B implementation result, including results that stop during Stage A validation; and
- update the test that currently requires only eleven `MCV*` constants.

After Stage B, the implemented diagnostic catalog is exactly the eleven Stage A codes plus the 25 Stage B codes. It contains neither `MCV405_DUPLICATE_OBSERVATION` nor `MCV406_CONFLICTING_OBSERVATION`, and no other code. None of the eleven Stage A codes may be removed or reinterpreted.

## Stage B Fields And Rules

Stage B creates field observations only for the seven approved Market Context fields:

- `market_value_eur`
- `contract_end_date`
- `salary_value`
- `age`
- `date_of_birth`
- `jersey_number`
- `position`

| Field or group | Validation | Normalization | Observation behavior | Diagnostic codes |
|---|---|---|---|---|
| Optional field presence | For exactly the seven observation fields, an absent optional column, null, empty or whitespace-only token means absent. Metadata fields do not use `MCV503`. | Preserve absence as `None`; suppress field-specific validation for that absent token. | Exactly one `MCV503` per absent observation field, outcome `not-provided`, no observation row and no row rejection by itself. | `MCV503_OPTIONAL_VALUE_MISSING` |
| Compound identity | Stage A guarantees populated identity and canonical season structure. | Build only deterministic canonical comparison values; no fuzzy matching, aliases, provider mapping or silent identity replacement. | Local identity columns remain traceable in every emitted observation. | `MCV500_NORMALIZED_TEXT` only when an approved safe text normalization changes a value |
| `reviewed_at` and other timestamps | Stage A preserves timezone-aware `reviewed_at`; naive timestamps remain rejected. | A timezone-aware instant may be normalized while preserving the instant. | Normalized provenance timestamp is copied to observations. | `MCV501_NORMALIZED_TIMESTAMP` |
| `review_status` | Allowed populated values are `reviewed`, `needs-review`, `rejected`; null remains a distinct strict-v1 case. | Preserve the approved enum without aliases or inferred defaults. | `reviewed` may qualify; `needs-review` and null require review; `rejected` rejects the row. | `MCV205_INVALID_REVIEW_STATUS`, `MCV206_REJECTED_REVIEW_STATUS`, `MCV404_NEEDS_REVIEW_STATUS`, `MCV408_MISSING_REVIEW_STATUS` |
| `confidence` | Empty is valid only when no observation field is populated. Missing conditional confidence and invalid populated confidence are distinct. | Preserve `low`, `medium` or `high`; infer nothing. Emit one metadata diagnostic per row, not one per affected observation. | Missing uses `MCV303`; invalid populated uses `MCV305`; each rejects all populated observations, and the codes suppress one another for the same token. | `MCV303_MISSING_CONDITIONAL_METADATA`, `MCV305_INVALID_CONFIDENCE` |
| Provenance references | `source_name`, `source_type`, `reviewed_at` and `reviewer` remain required. A populated `source_url` must be valid. | Preserve safe reviewed references; no provider permission is inferred. | Missing both URL and reference warns at row scope; an invalid populated URL rejects that provenance field. | `MCV310_INVALID_SOURCE_URL`, `MCV400_MISSING_PROVENANCE_REFERENCE` |
| Value dates | Field-specific date first, then `value_date`, otherwise unknown. Dates must be ISO `YYYY-MM-DD`. | Normalize valid dates deterministically; never use `reviewed_at`, `ingested_at` or filesystem time as a substitute. | Populate `effective_value_date` and the approved freshness status. | `MCV300_INVALID_DATE`, `MCV309_FUTURE_VALUE_DATE`, `MCV401_UNKNOWN_VALUE_DATE`, `MCV402_STALE_VALUE` |
| `market_value_eur` | Nullable non-negative decimal in EUR; period decimal, no thousands separators; no conversion. | Preserve canonical decimal value, including numeric zero. | Positive valid values may be accepted. Zero is accepted with warning but is not effective-eligible. | `MCV301_INVALID_NUMBER`, `MCV302_NEGATIVE_VALUE`, `MCV401_UNKNOWN_VALUE_DATE`, `MCV402_STALE_VALUE`, `MCV407_MARKET_VALUE_ZERO_NOT_EFFECTIVE`, `MCV503_OPTIONAL_VALUE_MISSING` |
| `salary_value` and metadata | Decimal salary requires valid currency, period and estimate flag. Invalid period/boolean uses `MCV303`; invalid populated currency uses only `MCV304` for that token. | Preserve Decimal zero. Period is `annual`, `monthly` or `weekly`; boolean is lowercase `true` or `false`; currency uses the static uppercase ISO 4217 set. | Any defective conditional metadata rejects the salary observation once; independent metadata defects emit one diagnostic each. Salary remains non-effective. | `MCV301_INVALID_NUMBER`, `MCV302_NEGATIVE_VALUE`, `MCV303_MISSING_CONDITIONAL_METADATA`, `MCV304_INVALID_CURRENCY`, `MCV403_ESTIMATED_VALUE`, `MCV401_UNKNOWN_VALUE_DATE`, `MCV402_STALE_VALUE`, `MCV503_OPTIONAL_VALUE_MISSING` |
| `contract_end_date` | Nullable valid ISO `YYYY-MM-DD`; no inferred active/expired state. | Preserve the business date separately from its observation date. | Valid contract date becomes an observation; future observation date rejects the field, not the business contract date itself. | `MCV300_INVALID_DATE`, `MCV309_FUTURE_VALUE_DATE`, `MCV401_UNKNOWN_VALUE_DATE`, `MCV402_STALE_VALUE`, `MCV503_OPTIONAL_VALUE_MISSING` |
| `age`, `date_of_birth`, `age_reference_date` | Age uses integer lexical form and range 15-45. Reference date is required with populated age. Contradictions produce exactly two `MCV306` diagnostics. | Derive only from valid explicit birth/reference dates using completed years; never use runtime clocks. | Valid derivation emits `MCV502` and suppresses age `MCV503`; contradictions reject age and date-of-birth observations while independent fields survive. | `MCV300_INVALID_DATE`, `MCV301_INVALID_NUMBER`, `MCV303_MISSING_CONDITIONAL_METADATA`, `MCV306_AGE_DATE_CONTRADICTION`, `MCV309_FUTURE_VALUE_DATE`, `MCV401_UNKNOWN_VALUE_DATE`, `MCV402_STALE_VALUE`, `MCV502_DERIVED_AGE`, `MCV503_OPTIONAL_VALUE_MISSING` |
| `jersey_number` | Nullable integer 1-99; zero and non-integers are invalid. | Preserve a valid integer without using zero as unknown. | Valid populated value becomes an observation and uses `value_date`. | `MCV308_INVALID_JERSEY_NUMBER`, `MCV309_FUTURE_VALUE_DATE`, `MCV401_UNKNOWN_VALUE_DATE`, `MCV402_STALE_VALUE`, `MCV503_OPTIONAL_VALUE_MISSING` |
| `position` | Empty uses `MCV503`. Canonical values are exact. Exact sentinels `N/A`, `unknown`, `-`, `null` use `MCV307`; every other non-empty non-canonical token uses `MCV409`. | Position remains verbatim; no general text normalization, aliases, case conversion, heuristics or fuzzy matching. | Canonical may be accepted; sentinels reject; other non-canonical values are preserved and require review. | `MCV307_INVALID_POSITION`, `MCV309_FUTURE_VALUE_DATE`, `MCV401_UNKNOWN_VALUE_DATE`, `MCV402_STALE_VALUE`, `MCV409_UNMAPPED_POSITION`, `MCV503_OPTIONAL_VALUE_MISSING` |

Text normalization MUST NOT introduce undocumented aliases, case mappings or fuzzy identity behavior. `MCV500_NORMALIZED_TEXT` is limited to the exact algorithm below; any broader rule requires another decision.

## Frozen Stage B Normalization And Precedence

The detailed normative source is policy v1. The future Stage B implementation MUST follow these exact operational rules.

### Missing observations and position

- The observation fields are exactly `market_value_eur`, `contract_end_date`, `salary_value`, `age`, `date_of_birth`, `jersey_number` and `position`.
- An absent optional column, null, empty or whitespace-only token emits exactly one `MCV503` for that absent observation, yields `not-provided`, creates no observation row and suppresses later validation for the token, except that absent age first receives the approved explicit-date derivation attempt.
- The diagnostic uses the absent observation field as `field_name`, the safe empty token as `raw_value` and null `normalized_value`.
- `MCV503` never applies to confidence, review status, provenance, salary metadata, auxiliary dates or other metadata.
- An absent `review_status` column is equivalent to null and uses `MCV408`.
- Absent `source_url` and `source_reference` columns participate in `MCV400`.
- An absent `confidence` column follows the conditional confidence rules below.
- Empty position emits only `MCV503`.
- Exact position values `Goalkeeper`, `Defender`, `Midfielder`, `Forward` are canonical.
- Exact sentinels `N/A`, `unknown`, `-`, `null` emit `MCV307`.
- Every other non-empty non-canonical position emits `MCV409` and requires review.

The existing Stage A fixture `valid_minimal.csv` is not modified. Under the cumulative Stage B contract it produces file outcome `accepted`; seven `MCV503` diagnostics; one `MCV408`; one `MCV400`; no `MCV303` or `MCV305`; no observation rows; final row outcome `review-required`; `review_required_rows = 1`; `accepted_rows = 0`; and `rejected_rows = 0`.

### Conditional metadata suppression

- Missing confidence with any populated observation emits one `MCV303` with `field_name=confidence`; invalid populated confidence emits one `MCV305` with the same field name.
- Confidence diagnostics are emitted once per row token, not once per affected observation. Either diagnostic rejects every populated observation; the two codes are mutually exclusive for one token.
- Empty confidence with no populated observation emits no `MCV303`, `MCV305` or `MCV503`.
- Populated salary requires valid `salary_currency`, `salary_period` and `is_estimated`.
- Missing metadata, invalid period or invalid boolean emits one `MCV303` for each defective metadata field.
- Invalid populated currency emits only `MCV304` for that token, not `MCV303`.
- Multiple metadata diagnostics reject and count the salary observation only once.

### Exact lexical normalization

| Input | Accepted lexical form | Public normalized type/value | Invalid behavior |
|---|---|---|---|
| Monetary values | `-?[0-9]+(?:\.[0-9]+)?`; minus is recognized only for negative classification | `decimal.Decimal`, including Decimal zero | negative `MCV302`; otherwise invalid `MCV301` |
| `age` | `[0-9]+`, range 15-45, no sign/decimal/exponent/whitespace | Python `int` | `MCV301` |
| `jersey_number` | `[0-9]+`, range 1-99, no sign/decimal/exponent/whitespace | Python `int` | `MCV308` |
| Business and value dates | exact valid `YYYY-MM-DD` | ISO string | `MCV300` |
| `reviewed_at` | Stage A-valid timezone-aware ISO-8601 | canonical UTC string using `astimezone(timezone.utc).isoformat().replace("+00:00", "Z")` | Stage A retains `MCV203` |
| Safe text fields | Stage A-valid strings | NFKC, exterior trim, internal whitespace collapsed to one ASCII space | no aliases or semantic conversion |

Monetary parsing uses `Decimal(token)`, never binary float. It does not call `.normalize()`, quantize or round. It preserves lexical scale: `1` becomes `Decimal("1")`, `1.0` becomes `Decimal("1.0")` and `1.00` becomes `Decimal("1.00")`. Numeric equality does not require representational equality, and the original raw token remains available for audit. Exponents, thousands separators, leading `+`, surrounding whitespace, local dates and datetime tokens used as dates are invalid. Every token beginning with `-`, including `-0` and `-0.00`, emits `MCV302`, produces no zero observation and never uses market-value-zero semantics. Only non-negative lexical zero forms are preserved as numeric zero.

Safe text normalization runs in this exact order: NFKC, removal of leading/trailing Unicode whitespace, then replacement of every maximal internal Unicode-whitespace run with one ASCII space (`U+0020`). It applies exactly to `player`, `team`, `league`, `source_name`, `source_reference` and `reviewer`. It preserves case, accents and punctuation. It does not apply to season, URLs, enums, numeric values, dates, position, notes or review notes. Public identity/provenance values use normalized text; diagnostic `raw_value` preserves the bounded safe original. Emit one `MCV500` per changed field.

Public logical types are exactly:

- monetary normalized values: `decimal.Decimal`;
- age and jersey number: Python `int`;
- business and effective dates: ISO strings;
- position: Python `str`;
- reviewed timestamp: canonical UTC string;
- missing normalized value: `None`;
- effective eligibility: Python `bool`; and
- conflict group ID: `None` throughout Stage B.

### Age derivation and contradiction

- Derive age only when age is absent and valid explicit `date_of_birth` and `age_reference_date` are populated.
- Completed years equal `reference.year - birth.year - ((reference.month, reference.day) < (birth.month, birth.day))`.
- No pipeline, review, filesystem or current clock may substitute.
- Valid derived age is 15-45, uses null `raw_value`, Python `int` normalized value, the reference date as effective date, emits `MCV502` and suppresses age `MCV503`.
- If derivation is unavailable or invalid, age remains absent and emits `MCV503`.
- Populated age with absent reference date uses `MCV303`; invalid reference date uses `MCV300`; invalid age/range uses `MCV301`.
- A contradiction emits exactly two `MCV306` diagnostics, one for `age` and one for `date_of_birth`, and rejects both observations without choosing a winner.

### Value dates, URL and currency

- A valid populated field-specific date wins over `value_date`; absent field-specific date allows fallback; both absent yields `unknown`.
- An invalid populated field-specific date emits `MCV300`, rejects every dependent observation and forbids fallback.
- An invalid populated fallback `value_date` emits `MCV300`, rejects every dependent observation and does not become unknown.
- Invalid selected dates suppress `MCV401`; future selected dates emit one `MCV309` per affected observation, use `future-invalid`, reject that observation and suppress `MCV401` and `MCV402`.
- URL validation uses only standard-library parsing: absolute `http`/`https`, non-empty hostname, no credentials, whitespace or controls, with `.test` allowed and no network request or semantic normalization.
- Invalid URL emits one field-scope `MCV310` at `field_name=source_url`, rejects only that provenance field, leaves all seven observation outcomes and effective eligibility unchanged, does not increment `rejected_field_observations`, does not independently change row outcome and does not convert an otherwise accepted row to `partially-accepted`.
- If invalid URL also lacks a valid source reference, emit independent `MCV400`, whose minimum row outcome remains `accepted-with-warnings`.
- Currency uses one explicit static immutable set of accepted three-letter ASCII uppercase ISO 4217 codes, with case-sensitive membership, no normalization/conversion/network/dependency, and the complete set visible in the future diff.

### Reconciliation

- One root cause emits only its selected diagnostic; documented suppression rules apply before diagnostic construction.
- `MCV306` has cardinality two per contradiction; `MCV503` has cardinality one per absent observation field.
- `rejected_field_observations` counts only rejected observations among the seven fields, once each; metadata/provenance rejections do not increment it.
- `MCV405` and `MCV406` remain absent in Stage B.
- All summaries reconcile with final outputs.
- Assign zero-based consecutive `diagnostic_order` after deterministic final sorting, never from pandas index or physical CSV order.

## Freshness Rules

Freshness is the whole-calendar-day difference between the UTC date of explicit `ingested_at` and the resolved effective value date.

| Field | `current` | `stale` |
|---|---|---|
| `market_value_eur` | age <= 180 days | age > 180 days |
| `salary_value` | age <= 180 days | age > 180 days |
| `contract_end_date` | age <= 365 days | age > 365 days |
| `age` | age <= 365 days | age > 365 days |
| `jersey_number` | age <= 180 days | age > 180 days |
| `position` | age <= 180 days | age > 180 days |
| `date_of_birth` | `not-applicable` | `not-applicable` |

The exact allowed statuses are:

- `current`
- `stale`
- `unknown`
- `not-applicable`
- `future-invalid`

`stale` warns and does not reject automatically. `unknown` warns for a populated value. A future effective value date produces `future-invalid`, emits `MCV309_FUTURE_VALUE_DATE` and rejects the field.

## Diagnostic Boundary

Stage B authorizes exactly these new diagnostics:

| Code | Severity | Scope | Trigger | Outcome |
|---|---|---|---|---|
| `MCV205_INVALID_REVIEW_STATUS` | error | row | Populated `review_status` is outside the approved enum. | row rejected |
| `MCV206_REJECTED_REVIEW_STATUS` | error | row | Human review explicitly rejected the row. | row rejected |
| `MCV300_INVALID_DATE` | error | field | A field date is invalid or non-ISO. | field rejected |
| `MCV301_INVALID_NUMBER` | error | field | A numeric field cannot be parsed canonically. | field rejected |
| `MCV302_NEGATIVE_VALUE` | error | field | A non-negative value field contains a negative number. | field rejected |
| `MCV303_MISSING_CONDITIONAL_METADATA` | error | field | Conditional metadata is missing or not validly supplied under the exact lexical contract. | field rejected |
| `MCV304_INVALID_CURRENCY` | error | field | Currency is not an approved uppercase ISO 4217 code. | field rejected |
| `MCV305_INVALID_CONFIDENCE` | error | field | Populated confidence is outside `low`, `medium`, `high`. | field rejected |
| `MCV306_AGE_DATE_CONTRADICTION` | error | field | Age, reference date and date of birth contradict one another. | age and date-of-birth observations rejected |
| `MCV307_INVALID_POSITION` | error | field | Non-empty position is one of the exact prohibited literal sentinels. | field rejected |
| `MCV308_INVALID_JERSEY_NUMBER` | error | field | Jersey number is outside 1-99 or is not an integer. | field rejected |
| `MCV309_FUTURE_VALUE_DATE` | error | field | Effective value date is later than `ingested_at`. | field rejected |
| `MCV310_INVALID_SOURCE_URL` | error | field | Populated URL fails the exact standard-library validation predicate. | provenance field rejected |
| `MCV400_MISSING_PROVENANCE_REFERENCE` | warning | row | Both source URL and source reference are absent. | accepted-with-warnings |
| `MCV401_UNKNOWN_VALUE_DATE` | warning | field | A populated value has no effective value date. | accepted-with-warning |
| `MCV402_STALE_VALUE` | warning | field | A value exceeds its v1 freshness threshold. | accepted-with-warning |
| `MCV403_ESTIMATED_VALUE` | warning | field | Salary is declared estimated. | accepted-with-warning |
| `MCV404_NEEDS_REVIEW_STATUS` | warning | row | Human review status is `needs-review`. | review-required |
| `MCV407_MARKET_VALUE_ZERO_NOT_EFFECTIVE` | warning | field | Zero market value is preserved but not currently effective-eligible. | accepted-with-warning |
| `MCV408_MISSING_REVIEW_STATUS` | warning | row | Strict v1 found null review status. | review-required |
| `MCV409_UNMAPPED_POSITION` | warning | field | Non-empty position is outside the canonical taxonomy. | review-required |
| `MCV500_NORMALIZED_TEXT` | info | field | Approved text normalization changed a safe value. | accepted |
| `MCV501_NORMALIZED_TIMESTAMP` | info | field | A timezone-aware timestamp was normalized while preserving its instant. | accepted |
| `MCV502_DERIVED_AGE` | info | field | Age was derived deterministically using an explicit date. | accepted |
| `MCV503_OPTIONAL_VALUE_MISSING` | info | field | An optional value is absent. | not-provided |

Codes, severities, scopes and default outcomes are frozen by policy v1.

### Stage B diagnostic codes not approved here

Already implemented by Stage A and preserved without reinterpretation:

- `MCV100_UNSUPPORTED_SCHEMA_VERSION`
- `MCV101_MISSING_REQUIRED_COLUMN`
- `MCV102_DUPLICATE_HEADER`
- `MCV103_UNKNOWN_COLUMN`
- `MCV104_INVALID_ENCODING`
- `MCV105_INVALID_DELIMITER`
- `MCV200_MISSING_REQUIRED_VALUE`
- `MCV201_DUPLICATE_LOCAL_RECORD_ID`
- `MCV202_INVALID_SEASON`
- `MCV203_INVALID_REVIEWED_AT`
- `MCV204_INVALID_SOURCE_TYPE`

Reserved for Stage C:

- `MCV405_DUPLICATE_OBSERVATION`
- `MCV406_CONFLICTING_OBSERVATION`

Stage D adds preview behavior, not new diagnostic codes. The full policy catalog contains 38 reserved codes, but the Stage B implementation declares exactly 36: eleven Stage A codes plus 25 Stage B codes. `MCV405` and `MCV406` remain undeclared until a separately approved Stage C implementation.

## Observation Outputs

Stage B retains the frozen result:

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

Both observation DataFrames use exactly:

1. `local_record_id`
2. `player`
3. `team`
4. `league`
5. `season`
6. `field_name`
7. `raw_value`
8. `normalized_value`
9. `effective_value_date`
10. `freshness_status`
11. `source_name`
12. `source_type`
13. `source_url`
14. `source_reference`
15. `reviewed_at`
16. `reviewer`
17. `confidence`
18. `review_status`
19. `field_outcome`
20. `conflict_group_id`
21. `effective_eligible`

Stage B leaves `conflict_group_id` null because grouping belongs to Stage C.

Final partitioning occurs after field outcomes and final row outcome are known:

- `not-provided` fields appear in neither observation DataFrame and increment no observation counter.
- Rejected fields appear in neither observation DataFrame. A rejected one of the seven observation fields increments `rejected_field_observations` exactly once; rejected metadata or provenance does not.
- An `accepted` row places every `accepted` observation in `accepted_observations`.
- An `accepted-with-warnings` row places every `accepted` or `accepted-with-warning` observation in `accepted_observations`, preserving the exact field outcome.
- A `partially-accepted` row exists only when one or more of the seven observations are rejected, at least one other provided observation survives as `accepted` or `accepted-with-warning`, and no row rule requires `review-required` or `rejected`. Surviving observations go to `accepted_observations`; rejected observations remain outside both DataFrames, and the row remains outside `rejected_rows`. Isolated metadata or provenance rejection never produces this outcome.
- A `review-required` row places every provided, non-rejected observation in `review_required_observations`. A row-level review rule preserves each observation's existing field outcome; an observation that caused review, including `MCV409`, uses `review-required`. No observation from the row appears in `accepted_observations`, and the row remains outside `rejected_rows`.
- A `rejected` row contributes no observation to either DataFrame and appears exactly once in `rejected_rows`. Row rejection does not automatically make every valid observation a rejected field observation.

`rejected_rows` retains its Stage A schema and contains only final `row_outcome == rejected` rows.

The five row counters are mutually exclusive and sum to `total_rows` for a processable file. `accepted_observations` and `review_required_observations` summary values equal their DataFrame row counts. Info diagnostics do not alter row outcome by themselves. All partitions precede final summary construction.

Diagnostics retain exactly:

1. `diagnostic_code`
2. `severity`
3. `scope`
4. `message`
5. `local_record_id`
6. `field_name`
7. `conflict_group_id`
8. `raw_value`
9. `normalized_value`
10. `row_outcome`
11. `field_outcome`
12. `diagnostic_order`

`file_summary` retains exactly:

1. `input_contract_version`
2. `policy_version`
3. `stage`
4. `file_outcome`
5. `total_rows`
6. `accepted_rows`
7. `accepted_with_warning_rows`
8. `partially_accepted_rows`
9. `review_required_rows`
10. `rejected_rows`
11. `accepted_observations`
12. `review_required_observations`
13. `rejected_field_observations`
14. `diagnostics_by_severity`
15. `diagnostics_by_code`
16. `duplicate_groups`
17. `conflict_groups`
18. `current_observations`
19. `stale_observations`
20. `unknown_freshness_observations`
21. `not_applicable_observations`
22. `future_invalid_observations`
23. `market_value_zero_observation_count`
24. `effective_eligible_observation_count`

`duplicate_groups` and `conflict_groups` remain `0` in Stage B.

After Stage B implementation, `file_summary["stage"]` is `B`; the summary schema itself remains unchanged.

## Outcomes And Effective Eligibility

Allowed field outcomes:

- `accepted`
- `accepted-with-warning`
- `review-required`
- `rejected`
- `not-provided`

Allowed row outcomes:

- `accepted`
- `accepted-with-warnings`
- `partially-accepted`
- `review-required`
- `rejected`

Row outcome precedence is exactly:

1. `rejected`
2. `review-required`
3. `partially-accepted`
4. `accepted-with-warnings`
5. `accepted`

Structural and row errors reject the row. Only an error that rejects one or more of the seven Stage B Market Context observations may contribute to `partially-accepted`, and only when another provided observation survives as `accepted` or `accepted-with-warning` and no row rule requires `review-required` or `rejected`. Rejection of metadata or provenance alone, including `MCV310`, never produces `partially-accepted`. Warnings preserve the affected element unless their approved outcome is `review-required`. Info diagnostics do not alter acceptance.

`effective_eligible` is observation-level audit metadata only. It does not populate runtime `effective_*` fields and does not authorize consolidation. Stage B MUST set it to false where policy explicitly blocks eligibility, including zero market value, rejected fields and observations requiring review. Salary has no canonical effective integration. No unapproved source precedence or winner selection may influence the value.

## Outcome Precedence

Processing order is:

1. Stage A file validation.
2. Stage A row structural validation.
3. Stage B optional-value and field validation.
4. Stage B deterministic normalization.
5. Stage B field-specific value-date resolution.
6. Stage B freshness classification.
7. Stage B field outcome.
8. Stage B row outcome using the approved precedence.
9. Stage B observation partitioning and rejected-row construction.
10. Deterministic diagnostics sorting and zero-based `diagnostic_order`.
11. Reconciled summary construction.

Stage B MUST NOT continue normal row processing after a Stage A file rejection. It MUST NOT resolve duplicate observations, conflicts, source precedence or winners.

## Market Value Zero

A structurally valid `market_value_eur = 0`:

- is a real declared value distinct from null;
- MUST be accepted and preserved as normalized numeric `0`;
- MUST NOT be converted to null;
- emits `MCV407_MARKET_VALUE_ZERO_NOT_EFFECTIVE`;
- has field outcome `accepted-with-warning`;
- gives a minimum row outcome of `accepted-with-warnings`;
- remains in `accepted_observations` unless another independent rule rejects it or places it under review;
- has `effective_eligible == false`;
- MUST NOT populate `effective_market_value_eur`; and
- MUST NOT increase effective market-value coverage or `effective_eligible_observation_count`.

## Determinism

Stage B MUST:

- preserve the Stage A deterministic file and row diagnostic order;
- sort diagnostics by the approved severity, scope/identity, canonical field and code rules before assigning zero-based consecutive `diagnostic_order`;
- sort observations by compound identity, field name, effective value date with unknown last, source name and local record ID;
- sort rejected rows using complete structural identity and private deterministic diagnostic signatures;
- normalize timezone-aware timestamps while preserving instants;
- compare freshness using whole UTC calendar days and explicit `ingested_at`;
- reconcile every summary count with returned outputs;
- return independent owned DataFrames;
- remain independent of physical CSV order where policy semantics are order-independent; and
- remove all private sorting keys from public outputs.

Stage B MUST NOT use pandas indices as public identity or add Stage C conflict hashing.

## Synthetic Fixtures

Only these new Stage B fixtures are approved:

- `tests/fixtures/manual_market_context/valid_full.csv`
- `tests/fixtures/manual_market_context/market_value_zero.csv`
- `tests/fixtures/manual_market_context/row_errors.csv`
- `tests/fixtures/manual_market_context/field_errors.csv`
- `tests/fixtures/manual_market_context/freshness_cases.csv`
- `tests/fixtures/manual_market_context/positions.csv`
- `tests/fixtures/manual_market_context/partial_acceptance.csv`

Every fixture MUST:

- contain only fictitious identities, organizations and sources;
- use reserved `.test` URLs;
- contain no real player, club, league or provider;
- contain no credential or provider payload;
- avoid Stage C duplicate-observation or conflict cases;
- avoid Stage D preview behavior;
- remain small, deterministic, directly reviewable and safe for Git; and
- test one bounded responsibility.

Malformed inputs better represented by generated bytes, headers or one-off rows remain in `tmp_path`.

## Stage B Test Matrix

Future tests MUST cover:

- every Stage A case as regression coverage, with expectation changes limited to the approved stage marker, cumulative diagnostic catalog, later Stage B diagnostics on structurally valid rows, observation outputs and Stage B summary counts;
- unchanged triggers, scopes, severities, ordering and precedence for all eleven Stage A diagnostics;
- no Stage B diagnostics after a Stage A file error or structurally rejected row;
- no deletion of Stage A cases, while allowing tests to be renamed or split between the frozen Stage A contract and cumulative Stage B contract;
- `STAGE_NAME == "B"` and `file_summary["stage"] == "B"` for every Stage B result, including early Stage A validation stops;
- exactly 36 implemented diagnostic constants: eleven Stage A plus 25 Stage B, excluding `MCV405`, `MCV406` and every other code;
- exact public API and result schemas;
- all 25 Stage B diagnostic codes;
- no Stage C diagnostic emission;
- exactly one `MCV503` per absent observation field, no `MCV503` for metadata and the successful-age-derivation exception;
- identical missing-observation behavior for absent optional columns, null, empty and whitespace-only values;
- absent `review_status` using `MCV408`, absent provenance-reference columns participating in `MCV400` and absent confidence following conditional confidence rules;
- unchanged `valid_minimal.csv` producing file outcome `accepted`, seven `MCV503`, one `MCV408`, one `MCV400`, no `MCV303` or `MCV305`, no observation rows, final row outcome `review-required`, one review-required row and zero accepted or rejected rows;
- empty, canonical, exact-sentinel and other non-canonical position precedence;
- missing versus invalid confidence suppression and exact one-per-row diagnostic cardinality;
- missing/invalid salary period and estimate metadata, plus invalid-currency suppression;
- canonical optional-null handling;
- exact `Decimal(token)` and integer lexical behavior, public logical types, lexical scale preservation and no normalization, quantization or rounding;
- `-0` and `-0.00` rejected with `MCV302`, no zero observation and no market-value-zero semantics;
- NFKC/trim/whitespace text normalization on exactly the six approved fields;
- ISO date and canonical UTC timestamp handling;
- lowercase boolean handling;
- salary currency, period and estimate dependencies;
- confidence triggers and enum validation;
- every review-status outcome;
- exact standard-library URL validation, `MCV310` metadata effects and independent `MCV400` behavior;
- static immutable case-sensitive ISO 4217 membership validation without dependencies;
- age range, completed-year derivation, derivation suppression and two-diagnostic contradiction cardinality;
- contract-end date without inferred status;
- jersey number 1, 99, zero, non-integer and out-of-range cases;
- the four canonical positions plus invalid and unmapped values;
- value-date first-choice/fallback behavior, invalid-date no-fallback and suppression rules;
- freshness boundaries at 180/181 and 365/366 days;
- `unknown`, `not-applicable` and `future-invalid`, including future-date suppression of stale/unknown;
- market-value-zero preservation and effective ineligibility;
- field and row outcome precedence;
- exact final partitioning for `not-provided`, rejected, accepted, accepted-with-warnings, partially-accepted, review-required and rejected outcomes;
- accepted and review-required observation DataFrames matching their summary counts;
- partially accepted and review-required rows remaining outside `rejected_rows`;
- row rejection not inflating `rejected_field_observations`;
- exact summary reconciliation;
- deterministic observations, diagnostics and rejected rows;
- zero-based consecutive `diagnostic_order`;
- equivalent reordered input;
- independent result DataFrames;
- `duplicate_groups == 0` and `conflict_groups == 0`; and
- no preview, conflict grouping, persistence, loader or runtime behavior.

## Verification Required For Future Code Block

Use a functional Python interpreter and run:

```powershell
python -m pytest -p no:cacheprovider tests/test_manual_market_context_processing.py -q
python -m pytest -p no:cacheprovider tests -q
python -m compileall src scripts
git diff --check
git status --short
```

Stage B does not authorize environment repair, dependency changes or preview execution.

## Explicit Exclusions

Stage B does not authorize:

- duplicate-observation grouping;
- historical grouping;
- conflict detection or conflict-group hashing;
- winner selection;
- source precedence;
- automatic consolidation;
- runtime `effective_*` population;
- preview CLI or preview execution;
- real data or ignored local CSVs;
- provider cache;
- SQLite;
- Streamlit;
- provider or API access;
- automatic discovery;
- changes to the existing Market Context loader;
- currency conversion;
- identity crosswalks;
- new dependencies;
- Stage C; or
- Stage D.

## Completion Criteria

Stage B is implemented only when:

- every authorized path exists and no path outside the boundary changed;
- the public API signature remains unchanged;
- every Stage A regression case remains, with only the expressly authorized cumulative Stage B expectation migration;
- all eleven Stage A diagnostics retain their triggers, scopes, severities, ordering and precedence;
- `STAGE_NAME` and every returned summary use stage `B`;
- exactly 36 diagnostic constants are implemented, with no `MCV405`, `MCV406` or other code;
- all 25 Stage B diagnostics are implemented with exact code, severity, scope and outcome;
- all seven approved Stage B fixtures are synthetic and versioned;
- observation and summary schemas remain exact;
- freshness, outcomes and market-value-zero behavior match policy v1;
- duplicate and conflict groups remain zero;
- Stage B tests pass;
- the full suite passes;
- compileall passes;
- diff and status are reviewed;
- no preview runs; and
- no real or ignored local data is accessed.

## Decision Boundary

Stage B is authorized only for a future separate implementation block under this exact boundary.

Stage B is not implemented.

Stages C-D remain blocked. Real data, preview, persistence, SQLite, Streamlit and providers remain blocked.

Next action: `Implement Stage B only under the approved boundary.`
