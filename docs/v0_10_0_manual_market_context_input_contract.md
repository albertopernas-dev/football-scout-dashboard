# v0.10.0 Reviewed Local Market Context Input Contract

## Status

- Milestone: v0.10.0
- Contract status: `reviewed-local-input-contract-defined`
- Contract version: `manual-market-context-input-v1`
- Related scope plan: [v0.10.0 Manual Market Context Workflow Hardening Scope Plan](v0_10_0_manual_market_context_scope_plan.md)
- Related scope decision: [v0.10.0 Manual Market Context Workflow Scope Decision](provider_decisions/v0_10_0_manual_market_context_scope_decision.md)
- Related contract decision: [v0.10.0 Reviewed Local Market Context Input Contract Decision](provider_decisions/v0_10_0_manual_market_context_input_contract_decision.md)
- Implementation approved: no
- Real local data access approved: no
- Parser approved: no
- Preview approved: no
- SQLite writes approved: no
- Streamlit changes approved: no
- Provider approval: none

## Purpose

This contract defines the accepted structure and semantics of future reviewed local Market Context CSV inputs.

It does not implement parsing, validation, conflict resolution, persistence or UI integration.

The contract:

- aligns input concepts with the existing canonical Market Context layer;
- avoids provider-dependent names;
- preserves value dates, provenance and human-review metadata;
- establishes deterministic structural expectations for future validation;
- keeps real inputs outside Git; and
- allows later committed fixtures only when they are synthetic.

## Normative Language

- **MUST** means required for a record or file to be acceptable.
- **MUST NOT** means expressly prohibited.
- **SHOULD** means expected unless a documented reason justifies an exception.
- **MAY** means optional.

## Contract Version

- The initial and only accepted v1 value is `manual-market-context-input-v1`.
- Every file MUST declare this value in `schema_version` on every row.
- A future implementation MUST report an unknown version as an error.
- An incompatible contract change requires a new version.
- A compatible optional-column extension MUST NOT silently redefine v1 semantics.
- The version MUST NOT be inferred from the filename.

## Row Grain

Each row represents **a reviewed Market Context snapshot for one canonical project player identity, from one declared source or reviewed reference**.

- A row MAY contain multiple Market Context values for the same identity and source.
- Every value in the row MUST refer to the same `player`, `team`, `league` and `season` context.
- `value_date` is the general date of the snapshot when a field-specific value date is absent.
- A field MAY carry its own value date where this contract defines one.
- A row is an observation, not a consolidated effective record.
- Multiple observations for the same player identity MAY coexist.
- A separate future policy MUST define conflict detection, precedence and consolidation.
- A future parser MUST NOT silently overwrite one observation with another.

## Canonical Identity Alignment

The current Market Context layer does not define a standalone canonical player ID. It joins context to players through the existing compound key `player`, `team`, `league` and `season`. The implementation normalizes the three text fields into internal match keys and normalizes `season` to a stable string for comparison.

This v1 contract retains that compound identity because inventing a new ID would break alignment with the repository. Retention does not approve new automatic text-only matching: input identity must be reviewed, all four components must be present, and a future parser must diagnose ambiguity rather than attach data silently.

| Input Column | Canonical Target | Required | Type | Nullable | Meaning |
|---|---|---:|---|---:|---|
| `player` | `player` / internal `player_match_key` | yes | string | no | Existing reviewed player identity component. It is not a standalone stable player ID. |
| `team` | `team` / internal `team_match_key` | yes | string | no | Existing team context required by the current compound join. |
| `league` | `league` / internal `league_match_key` | yes | string | no | Existing competition context required by the current compound join. |
| `season` | `season` / internal `_season_match_key` | yes | four-digit decimal season token | no | Canonical CSV string matching `^\d{4}$`; example: `2024`. |

The logical canonical type of `season` is a four-digit decimal season token. Decimal forms such as `2024.0`, ranges such as `2024/25` or `2024-25`, and labels such as `season-2024` are not canonical v1 values. A future parser MAY normalize an integer value read from CSV to the same four-digit string, but MUST reject ambiguous or non-canonical forms.

Rules:

- The complete compound identity MUST be present for an accepted record.
- No one component, including `player`, substitutes for the full compound identity.
- Human-readable identity labels are review evidence, not permission for fuzzy matching.
- Team, competition and season do not independently establish player identity.
- `player_name`, `team_name` and `competition_name` are not v1 aliases for `player`, `team` and `league`.
- A future provider-independent local key or reviewed crosswalk, if approved, MUST remain distinct from this current compound identity.
- No new player identity is created by this contract.

## Canonical Field Alignment

| Input Column | Existing Canonical Field | Contract Role | Required | Type | Nullable | Notes |
|---|---|---|---:|---|---:|---|
| `player` | `player` | aligned identity | yes | string | no | Part of the current compound join. |
| `team` | `team` | aligned identity | yes | string | no | Part of the current compound join. |
| `league` | `league` | aligned identity | yes | string | no | Part of the current compound join. |
| `season` | `season` | aligned identity | yes | four-digit decimal season token | no | Canonical CSV string matching `^\d{4}$`; part of the current compound join. |
| `age` | `age` | aligned value | no | integer from 15 through 45 | yes | Current layer accepts age; `age_reference_date` is conditionally required by v1. |
| `date_of_birth` | none | `contract-only-future-mapping` | no | ISO date | yes | Preferred source value for future explicit age derivation. |
| `age_reference_date` | none | `contract-only-future-mapping` | conditional | ISO date | yes | Required whenever `age` is present so its reference date is explicit. |
| `market_value_eur` | `market_value_eur` | aligned value | no | decimal | yes | Fixed-currency EUR field; not a transfer fee. |
| `market_value_currency` | none | deferred | no | ISO 4217 code | yes | Not a v1 input column because `market_value_eur` is explicitly fixed to EUR. |
| `contract_end_date` | `contract_end_date` | aligned value | no | ISO date | yes | Current Market Context contract field. |
| `salary_value` | none | `contract-only-future-mapping` | no | decimal | yes | No current canonical salary field. |
| `salary_currency` | none | `contract-only-future-mapping` | conditional | ISO 4217 code | yes | Required when `salary_value` is present. |
| `salary_period` | none | `contract-only-future-mapping` | conditional | enum | yes | Required when `salary_value` is present. |
| `jersey_number` | none in Market Context input | `contract-only-future-mapping` | no | integer | yes | Existing player data may contain a jersey concept, but the current Market Context schema does not map it. |
| `position` | none in Market Context input | `contract-only-future-mapping` | no | string | yes | Must use the project taxonomy after a future explicit mapping decision. |
| `source_name` | `source` | mapping-required provenance | yes | string | no | Future parser would map the more explicit input name to the current canonical field. |
| `source_url` | `source_url` | aligned provenance | no | string URL | yes | Optional reviewed public reference. |
| `confidence` | `confidence` | aligned review metadata | conditional | enum | yes | Required when `age`, `date_of_birth`, `market_value_eur`, `contract_end_date`, `salary_value`, `jersey_number` or `position` is present; `low`, `medium` or `high`. |
| `notes` | `notes` | aligned review metadata | no | string | yes | Must not contain secrets, credentials or payloads. |
| `value_date` | optional provider context `value_date` | mapping-required freshness | no | ISO date | yes | Defined here for manual observations; the current Market Context merge does not consume it. |
| `market_value_value_date` | none | `contract-only-future-mapping` | no | ISO date | yes | Field-specific freshness. |
| `salary_value_date` | none | `contract-only-future-mapping` | no | ISO date | yes | Field-specific freshness. |
| `contract_value_date` | none | `contract-only-future-mapping` | no | ISO date | yes | Date on which contract information was observed. |
| `market_context_*` output fields | `market_context_*` | pipeline-generated | no | derived | yes | MUST NOT be supplied by the manual CSV. |
| `effective_*` fields | `effective_*` | pipeline-generated | no | derived | yes | MUST NOT be supplied by the manual CSV. |

No Sportmonks, Capology or Transfermarkt-specific field is part of this contract.

## v1 Column Set

Strict-mode v1 recognizes only the following input columns.

### Required

- `schema_version`
- `local_record_id`
- `player`
- `team`
- `league`
- `season`
- `source_name`
- `source_type`
- `reviewed_at`
- `reviewer`

### Optional Or Conditionally Required

- `age`
- `date_of_birth`
- `age_reference_date`
- `market_value_eur`
- `contract_end_date`
- `salary_value`
- `salary_currency`
- `salary_period`
- `jersey_number`
- `position`
- `value_date`
- `market_value_value_date`
- `salary_value_date`
- `contract_value_date`
- `source_url`
- `source_reference`
- `confidence`
- `notes`
- `is_estimated`
- `review_status`
- `review_notes`

`confidence` MUST be populated when at least one of `age`, `date_of_birth`, `market_value_eur`, `contract_end_date`, `salary_value`, `jersey_number` or `position` is populated. Allowed values remain `low`, `medium` and `high`. `value_date`, field-specific value dates, `notes` and provenance metadata do not trigger `confidence` by themselves. Empty `confidence` is allowed only when none of those Market Context value columns is populated. Final diagnostic codes remain deferred.

## Required Structural Columns

| Column | Required | Type | Nullable | Rule |
|---|---:|---|---:|---|
| `schema_version` | yes | string | no | Exact value `manual-market-context-input-v1`. |
| `local_record_id` | yes | string | no | Unique within the file; not derived only from row number; no secrets or sensitive data. |
| `player` | yes | string | no | Reviewed component of the current canonical compound identity. |
| `team` | yes | string | no | Reviewed component of the current canonical compound identity. |
| `league` | yes | string | no | Reviewed component of the current canonical compound identity. |
| `season` | yes | four-digit decimal season token | no | Canonical CSV string matching `^\d{4}$`; reviewed component of the current canonical compound identity. |
| `source_name` | yes | string | no | Identifies the source or reviewed reference; does not imply provider approval. |
| `source_type` | yes | enum string | no | One of the source types defined below. |
| `reviewed_at` | yes | timezone-aware ISO-8601 datetime | no | Time of human review; must include `Z` or an explicit UTC offset and remains distinct from value dates and ingestion time. |
| `reviewer` | yes | string | no | Non-sensitive internal reviewer identifier; no credentials or unnecessary private email. |

`reviewed_at` MUST include either `Z` or an explicit UTC offset such as `+02:00`. Naive datetimes without a timezone are invalid. A future pipeline MAY normalize the timestamp to UTC while preserving its instant. `reviewed_at` remains distinct from value dates and ingestion time.

The definitive format constraints for `local_record_id` are deferred, but uniqueness and non-nullability are not.

## Recommended Identity Context Columns

The repository already uses `player`, `team`, `league` and `season` as the reviewed compound identity. Therefore:

- `player_name` is not a separate v1 column; use `player`.
- `team_name` is not a separate v1 column; use `team`.
- `competition_name` is not a separate v1 column; use `league`.
- `season` is required because it participates in the current join.

These fields support human inspection and diagnostics. Their presence does not authorize fuzzy matching or silent normalization decisions.

## Market Context Value Columns

### Market Value

- `market_value_eur` is a nullable decimal amount in EUR.
- It MUST be numeric and non-negative when present.
- Zero is a real declared value and MUST NOT be converted to unknown.
- Unknown MUST be represented as null.
- The value MUST NOT be described as a transfer fee.
- Because the field name fixes EUR, `market_value_currency` is not accepted in v1.
- Monetary conversion is not approved.

The current validator and effective-field logic treat only positive values as known. That difference is an explicit compatibility issue for future implementation; this documentation does not change it.

### Salary Or Compensation

- `salary_value` is a nullable non-negative decimal source value and has no current canonical Market Context target.
- Zero is a real declared amount and MUST NOT be converted to unknown.
- `salary_currency` MUST be present when `salary_value` is present.
- `salary_period` MUST be present when `salary_value` is present and MUST be `annual`, `monthly` or `weekly`.
- `is_estimated` MUST be present when `salary_value` is present and MUST be `true` or `false`.
- An estimate MUST NOT be presented as an official contractual amount.
- Null means unknown; it does not mean zero salary.

The canonical salary mapping remains deferred.

### Contract End

- `contract_end_date` is a nullable ISO `YYYY-MM-DD` business date.
- It MUST NOT be replaced by `reviewed_at`, `value_date` or a future ingestion timestamp.
- Null means unknown or not provided.

### Date Of Birth And Age

- `date_of_birth` SHOULD be preferred when a reviewed source provides it.
- `date_of_birth` and `age_reference_date` are contract-only future fields; current canonical input supports only `age`.
- `age` is a nullable integer from 15 through 45.
- `age_reference_date` MUST be present whenever `age` is present, whether the age was copied or derived, so its temporal meaning is explicit.
- A future validator MUST detect contradictions between `age`, `age_reference_date` and `date_of_birth`; it MUST NOT resolve them silently.

### Jersey Number

- `jersey_number` is a nullable positive integer.
- A reasonable accepted range is deferred to the validation policy.
- Zero MUST NOT represent unknown.

### Position

- `position` is a nullable string intended for the project's canonical position taxonomy.
- Provider-specific position labels MUST NOT acquire canonical meaning without an explicit mapping.
- A future pipeline SHOULD preserve unmapped source values for diagnostics rather than convert them silently.

## Date And Freshness Columns

| Column | Type | Nullable | Meaning |
|---|---|---:|---|
| `value_date` | ISO `YYYY-MM-DD` | yes | General date to which the row snapshot applies. |
| `market_value_value_date` | ISO `YYYY-MM-DD` | yes | Market-value-specific observation date. |
| `salary_value_date` | ISO `YYYY-MM-DD` | yes | Salary-specific observation date. |
| `contract_value_date` | ISO `YYYY-MM-DD` | yes | Date on which contract information was observed. |

Future date selection semantics are:

1. Use the field-specific value date.
2. Otherwise use `value_date`.
3. Otherwise treat the value date as unknown.

This order defines semantics only; it is not an implemented precedence or conflict policy. An unknown value date SHOULD produce a future diagnostic.

`contract_end_date` is not `contract_value_date`. `ingested_at` MUST NOT be a trusted manual input: a future pipeline generates it, and it does not replace a business value date. Filesystem modification time MUST NOT be used as a value date.

## Provenance Columns

| Column | Required | Type | Nullable | Rule |
|---|---:|---|---:|---|
| `source_name` | yes | string | no | Human-readable source or reference name. |
| `source_url` | no | string URL | yes | Public reviewed URL when available. |
| `source_type` | yes | enum string | no | Source classification independent of provider candidates. |
| `source_reference` | no | string | yes | Reviewed non-URL citation or reference. |
| `reviewed_at` | yes | timezone-aware ISO-8601 datetime | no | Human review timestamp containing `Z` or an explicit UTC offset. |
| `reviewer` | yes | string | no | Non-sensitive reviewer identifier. |
| `notes` | no | string | yes | Source/value context; never credentials or payload content. |

Initial `source_type` values:

- `official-public`
- `provider-public`
- `manual-reference`
- `internal-reviewed`
- `other-reviewed`

At least one of `source_url` or `source_reference` SHOULD be present. Declaring provenance does not grant permission to access, reuse or redistribute data.

## Review And Estimate Metadata

| Column | Required | Type | Nullable | Rule |
|---|---:|---|---:|---|
| `is_estimated` | conditional | boolean | yes | Required when `salary_value` is present; canonical values are `true` and `false`. |
| `review_status` | no | enum string | yes | `reviewed`, `needs-review` or `rejected`. Normal processing SHOULD contain `reviewed`. |
| `review_notes` | no | string | yes | Review workflow notes, separate from source/value `notes`. |

Future validation will decide whether `needs-review` and `rejected` rows are rejected or routed to a report. This contract does not approve normal processing of those statuses.

## Currency Rules

- Currency codes MUST use uppercase ISO 4217 codes.
- Symbols such as `EUR`'s euro sign, `$` or the pound sign MUST NOT be used as codes.
- Free-form names such as `euros` MUST NOT be used.
- Automatic currency conversion is not approved.
- EUR MUST NOT be assumed for a generic monetary field.
- `market_value_eur` is the exception because its existing canonical name explicitly fixes EUR.
- A monetary value without its required currency MUST be an error unless the canonical field explicitly fixes the currency.
- Future conversion requires separate exchange-rate provenance and date rules.

## Null And Empty Semantics

- Null means unknown, unavailable or not provided.
- Zero is a real value and MUST NOT substitute for null.
- In CSV representation, an unquoted empty optional field is the v1 null representation.
- Whitespace-only required fields are invalid; future normalization of optional whitespace is a separate implementation detail.
- Literal sentinels such as `N/A`, `unknown`, `-` or `null` MUST NOT be interpreted as canonical values.
- Values MUST NOT be invented through defaults.
- A malformed real input MUST NOT fall back silently to demo data.
- A missing optional value does not by itself invalidate the row.
- Compound identity and required structural fields MUST NOT be null.

## CSV Representation

- Encoding MUST be UTF-8 without BOM.
- The first row MUST contain exact headers.
- The canonical delimiter is comma, matching the repository's current CSV schema and `pandas.read_csv` default.
- A file MUST use only that delimiter.
- `season` MUST be represented as a four-digit string matching `^\d{4}$`; decimal forms, ranges and free-form labels are invalid canonical CSV values.
- Dates MUST use the ISO forms specified by this contract.
- Decimal values MUST use a period and MUST NOT use thousands separators.
- Boolean values MUST be lowercase `true` or `false`.
- Header names are lowercase snake_case and case-sensitive.
- Spreadsheet formulas MUST NOT be present.
- Comment rows MUST NOT be present.
- Duplicate headers MUST NOT be present.
- Line endings MUST be consistent within the file.

No CSV reader or parser is implemented or approved by this section.

## Unknown And Additional Columns

v1 uses a strict-by-default policy.

- Columns outside the v1 column set MUST NOT be ignored silently.
- A future implementation MUST reject unknown columns by default.
- A future explicitly approved compatibility mode MAY preserve unknown columns without assigning semantics to them.
- Unknown columns MUST NOT become canonical through incidental naming.

Reserved pipeline or workflow columns that are not manual v1 inputs include:

- `ingested_at`
- `player_match_key`
- `team_match_key`
- `league_match_key`
- `_season_match_key`
- `market_context_matched`
- `market_context_duplicate_key`
- all `market_context_*` output columns
- all `effective_*` fields
- provider-specific IDs, names, cache metadata and license fields

## File Naming And Location Boundary

- Real inputs MUST remain in Git-ignored local paths.
- Real inputs SHOULD use the existing `.local.csv` convention.
- A compatible generic filename is `market_context.reviewed.v1.local.csv`.
- The filename SHOULD identify manual/reviewed purpose and MAY contain a version hint.
- The filename MUST NOT be the authoritative schema version; `schema_version` is authoritative.
- A provider name MUST NOT define the canonical contract.
- Personal absolute paths MUST NOT be committed.
- Filesystem timestamps MUST NOT act as `value_date`.
- This contract creates no real file and authorizes no migration.

## Structural Acceptance Rules

Before value processing, a future implementation MUST verify:

- `schema_version` is supported and consistent;
- every required column is present;
- headers are unique and exact;
- all four canonical compound identity components are present;
- `season` uses the canonical four-digit decimal representation;
- `local_record_id` is present and unique within the file;
- required source and review metadata is present;
- `reviewed_at` includes a valid timezone designator;
- `confidence` is present when any of `age`, `date_of_birth`, `market_value_eur`, `contract_end_date`, `salary_value`, `jersey_number` or `position` is populated, and is empty only when none is populated;
- encoding and delimiter match this contract;
- unknown columns are absent in strict mode;
- duplicate `local_record_id` values are rejected; and
- no impossible structural combination is accepted, including a monetary value without required currency/period metadata.

These checks do not replace the future validation policy. This contract defines no final diagnostic codes, row-rejection format, conflict precedence or duplicate-observation resolution.

## Compatibility With Existing Market Context Layer

| Element | Classification | Finding |
|---|---|---|
| `player`, `team`, `league`, `season` | aligned | Exact current compound merge identity; no standalone player ID exists in this layer. |
| `age` | aligned | Existing canonical input and `market_context_age` output. |
| `market_value_eur` | aligned with semantic incompatibility | Existing input/output name; current validation/effective logic treats only positive values as known, while v1 preserves a declared zero as real. |
| `contract_end_date` | aligned | Existing canonical input and output. |
| `source_url`, `confidence`, `notes` | aligned | Existing canonical provenance/review fields. |
| `source_name` | mapping-required | Must map explicitly to existing `source`; v1 does not rename the current canonical field. |
| `source_type`, `source_reference`, review metadata | mapping-required | No current canonical destination. |
| `schema_version`, `local_record_id` | mapping-required | New workflow structure; no current Market Context input equivalent. |
| `value_date` | mapping-required | Exists as an optional provider context field, but current manual merge does not consume it. |
| Field-specific value dates | `contract-only-future-mapping` | No current canonical destination. |
| `date_of_birth`, `age_reference_date` | `contract-only-future-mapping` | Current layer accepts only `age`. |
| Salary fields | `contract-only-future-mapping` | No current canonical salary/compensation fields. |
| `jersey_number`, `position` | `contract-only-future-mapping` | Not current Market Context input fields. |
| `market_context_*`, match keys and duplicate/matched flags | pipeline-generated | Current merge outputs/internal columns; prohibited as manual inputs. |
| `effective_*` | pipeline-generated | Current data layer derives these fields; prohibited as manual inputs. |
| `ingested_at` | pipeline-generated | Future technical timestamp, never trusted from a manual CSV. |
| Provider optional fields such as provider IDs and `provider_name` | deferred | Not accepted by the provider-independent reviewed local v1 contract. |

The current loader accepts the smaller legacy schema and permits extra columns. The v1 contract is therefore documentation for a future explicit parser, not a claim that current code enforces it.

## Implementation-Blocking Compatibility Decisions

### `market_value_eur = 0`

- Contract v1 semantics: zero is a real declared value and is distinct from null.
- Current canonical behavior: zero is rejected or treated as unknown because current validation and effective coverage require a positive value.
- Status: unresolved semantic incompatibility.
- Parser implementation MUST NOT proceed until a separate decision chooses one of:
  1. adapt the canonical validation and effective logic to preserve zero;
  2. revise the v1 contract before implementation.
- This documentation block does not change current code or runtime behavior.

## Explicitly Deferred

- Parser implementation.
- Resolution of the `market_value_eur = 0` semantic incompatibility.
- Normalization functions.
- Final diagnostic codes.
- Row rejection format.
- Conflict precedence.
- Duplicate observation resolution.
- Stale-data thresholds.
- Currency conversion.
- Identity crosswalk generation.
- Synthetic fixtures.
- Preview or report implementation.
- SQLite loading.
- Streamlit integration.
- Real local data migration.
- Position taxonomy mapping.
- Jersey-number range validation.

## Contract Examples

The following are non-executable documentation examples. Every identity, source and value is synthetic.

### Example Header

```csv
schema_version,local_record_id,player,team,league,season,age,date_of_birth,age_reference_date,market_value_eur,contract_end_date,salary_value,salary_currency,salary_period,jersey_number,position,value_date,market_value_value_date,salary_value_date,contract_value_date,source_name,source_url,source_type,source_reference,reviewed_at,reviewer,confidence,notes,is_estimated,review_status,review_notes
```

### Conceptually Valid Row

```csv
manual-market-context-input-v1,synthetic-record-001,Player Example,Team Example,Synthetic League,2024,24,2000-06-15,2024-07-01,1500000,2027-06-30,,,,,Forward,2024-07-01,2024-07-01,,2024-07-01,Synthetic Reviewed Reference,https://example.test/player-example,internal-reviewed,,2024-07-02T10:30:00Z,reviewer-example,medium,Synthetic documentation only.,,reviewed,
```

### Conceptually Invalid Row

```csv
manual-market-context-input-v2,,Player Example,,Synthetic League,2024,unknown,,,1,30,2027,,,,,,,,,Unreviewed Source,,other-reviewed,,yesterday,,high,Synthetic invalid example.,yes,reviewed,
```

This row is invalid because it uses an unsupported schema version, lacks `local_record_id`, `team` and `reviewer`, uses non-canonical values, has a malformed contract date, and omits required review/value semantics.

## Contract Decision Boundary

`manual-market-context-input-v1` is defined as a documentation contract.

- Implementation is not authorized.
- Real local data access is not authorized.
- CSV creation or migration is not authorized.
- Parser, fixtures, preview, SQLite and Streamlit work are not authorized.
- Provider integration or approval is not authorized.

The recommended next decision is a separate docs-only definition of freshness, provenance, validation and duplicate/conflict policy for v1.
