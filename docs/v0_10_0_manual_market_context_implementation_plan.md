# v0.10.0 Reviewed Local Market Context Implementation Plan

## Status

- Milestone: v0.10.0
- Plan status: `manual-market-context-implementation-plan-defined`
- Related scope plan: [v0.10.0 Manual Market Context Workflow Hardening Scope Plan](v0_10_0_manual_market_context_scope_plan.md)
- Related scope decision: [v0.10.0 Manual Market Context Workflow Scope Decision](provider_decisions/v0_10_0_manual_market_context_scope_decision.md)
- Related input contract: [v0.10.0 Reviewed Local Market Context Input Contract](v0_10_0_manual_market_context_input_contract.md)
- Input contract version: `manual-market-context-input-v1`
- Related processing policy: [v0.10.0 Reviewed Local Market Context Processing Policy](v0_10_0_manual_market_context_processing_policy.md)
- Policy version: `manual-market-context-policy-v1`
- Related implementation decision: [v0.10.0 Reviewed Local Market Context Implementation Plan Decision](provider_decisions/v0_10_0_manual_market_context_implementation_plan_decision.md)
- Related Stage A plan: [v0.10.0 Reviewed Local Market Context Stage A Plan](v0_10_0_manual_market_context_stage_a_plan.md)
- Related Stage A decision: [v0.10.0 Reviewed Local Market Context Stage A Decision](provider_decisions/v0_10_0_manual_market_context_stage_a_decision.md)
- Related Stage A closeout: [v0.10.0 Reviewed Local Market Context Stage A Closeout](v0_10_0_manual_market_context_stage_a_closeout.md)
- Related Stage A closeout decision: [v0.10.0 Reviewed Local Market Context Stage A Closeout Decision](provider_decisions/v0_10_0_manual_market_context_stage_a_closeout_decision.md)
- Related Stage B plan: [v0.10.0 Reviewed Local Market Context Stage B Plan](v0_10_0_manual_market_context_stage_b_plan.md)
- Related Stage B decision: [v0.10.0 Reviewed Local Market Context Stage B Decision](provider_decisions/v0_10_0_manual_market_context_stage_b_decision.md)
- Plan approved: yes, documentation only
- Full implementation approved: no
- Stage A implementation approved: yes
- Stage A implemented: yes
- Stage A verified: yes
- Stage A completed: yes
- Stage A synthetic fixtures approved: yes, only the three specified Stage A fixture paths
- Stage B approved: yes, for a separate code block
- Stage B implemented: no
- Stage C approved: no
- Stage D approved: no
- Preview execution approved: no
- Real local data access approved: no
- SQLite approved: no
- Streamlit approved: no
- Provider approval: none
- New dependencies approved: no

## Purpose

This plan defines a bounded future implementation for parsing and diagnosing reviewed local Market Context observations under the approved input contract and processing policy.

It translates the contract and policy into concrete components while requiring that:

- implementation and tests use only synthetic data;
- accepted observations remain separate from effective values;
- the existing canonical loader and merge path remain unchanged;
- SQLite and Streamlit remain outside the implementation;
- no local input path is discovered automatically; and
- processing results are deterministic and reconcilable.

This document approves the complete plan as documentation. Stage A is completed and closed. The separate Stage B decision authorizes only its bounded future code block; Stages C-D remain unauthorized.

## Repository Alignment Review

The review was limited to versioned source, scripts, tests and documentation. No local data, ignored file, provider cache or SQLite database was read.

| Concern | Existing Repository Pattern | Planned Alignment |
|---|---|---|
| Module layout | Domain helpers are flat modules under `src/`. | Add one focused future module at `src/manual_market_context_processing.py`; do not introduce a package hierarchy or refactor existing modules. |
| Imports | Source modules use absolute imports such as `from src.market_context import ...`. Scripts add the project root to `sys.path` before importing `src` modules. | Use absolute `src` imports and follow the existing script bootstrap only in the future CLI. |
| Tabular processing | Market Context and provider helpers use pandas DataFrames and return copies rather than mutating callers. | Use DataFrames for observation, rejection and diagnostic collections; keep the processor pure after file loading. |
| Structured results | Frozen dataclasses already group immutable contracts in `src/schema.py` and batch-fetch scripts. | Use a standard-library frozen dataclass to group the processing outputs without adding a dependency. |
| Tests | Tests are pytest modules named `tests/test_*.py`; temporary files and synthetic versioned fixtures are already used. | Add focused processor and CLI tests under `tests/`, with small CSV fixtures under a dedicated synthetic fixture directory. |
| CLI scripts | Existing scripts under `scripts/` use `argparse`, explicit required paths and thin `main()` functions. Preview scripts print text summaries and return exit codes. | Add a thin `argparse` preview with required `--input` and `--ingested-at`; keep all processing in the source module. |
| Synthetic fixtures | Versioned test fixtures live under `tests/fixtures/`; synthetic public examples live under `docs/examples/`. | Put parser test inputs under `tests/fixtures/manual_market_context/`; do not create documentation examples or real-data fixtures in this plan. |
| Position normalization | The canonical API-Football taxonomy is `Goalkeeper`, `Defender`, `Midfielder`, `Forward`. | Validate these four canonical values in Stage B and diagnose any unmapped value under policy v1. |
| Current Market Context | `src/market_context.py` loads CSV with pandas, validates the legacy schema, creates normalized compound match keys and merges by `player + team + league + season`. | Keep the current loader and merge unchanged. The new processor produces observation outputs only and does not replace or call the existing effective merge path. |
| Preview/report pattern | `scripts/preview_provider_market_context.py` separates a reusable preview function from CLI parsing and prints deterministic console tables. | Follow the text/console pattern in Stage D, without HTML, persistence, Streamlit or personal paths. |

## Proposed Files

These paths are proposed for later, separately approved stages. None is created by this plan.

| Proposed Path | Purpose | Future Approval Required |
|---|---|---|
| `src/manual_market_context_processing.py` | Contract constants, strict CSV parsing, normalization, validation, freshness, diagnostics, duplicate/conflict analysis and output partitioning. | Stage A first; later Stage B and Stage C changes each require separate approval. |
| `scripts/preview_manual_market_context.py` | Read one explicit synthetic fixture through the public processor and print a deterministic, non-persistent summary. | Stage D approval. |
| `tests/test_manual_market_context_processing.py` | Unit and contract tests for Stages A-C. | Approved only with the corresponding implementation stage. |
| `tests/test_manual_market_context_preview.py` | CLI argument, output and exit-code tests for the synthetic preview. | Stage D approval. |
| `tests/fixtures/manual_market_context/` | Small, fictitious, deterministic CSV fixtures for approved stages. | Fixture creation requires the stage that first uses each fixture. |

The source module is intentionally separate from `src/market_context.py`: the new contract has field-observation semantics and stricter diagnostics, while the existing module remains the stable runtime loader and merge path.

## Public Python API

The future public entry point is:

```python
def process_reviewed_market_context(
    input_path: Path,
    *,
    ingested_at: datetime,
    strict: bool = True,
) -> ManualMarketContextProcessingResult:
    ...
```

Contract:

- `input_path` is required and has no default.
- `ingested_at` is required and MUST be timezone-aware.
- The core MUST NOT call `datetime.now()` or infer a hidden processing time.
- `strict` defaults to `True`.
- Expected contract failures are returned as diagnostics inside a structured, inspectable result, including file rejection when the file can be identified safely.
- Unreadable paths and programming errors remain exceptions at the documented error boundary.
- The function reads one explicit file, delegates to one processing path and returns the structured result.
- It does not preview, print, persist, merge effective fields or open external resources.

The implementation MAY use a private helper such as:

```python
def _process_reviewed_market_context_dataframe(
    df: pd.DataFrame,
    *,
    ingested_at: datetime,
    strict: bool,
) -> ManualMarketContextProcessingResult:
    ...
```

The DataFrame helper remains private. A second public processing API is not approved because it would create two supported entry paths and weaken file-contract coverage. Tests may exercise the private helper only where isolating deterministic transformations materially improves coverage; end-to-end contract tests must use the public file API.

## Processing Result Contract

The future result is a standard-library frozen dataclass:

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

| Member | Logical Type | Meaning |
|---|---|---|
| `file_outcome` | `str` | Deterministic file-level disposition defined by policy v1. |
| `accepted_observations` | `pd.DataFrame` | Field observations accepted normally or with warnings; acceptance does not imply effective promotion. |
| `review_required_observations` | `pd.DataFrame` | Structurally processable observations that require human review before later use. |
| `rejected_rows` | `pd.DataFrame` | Rows whose final `row_outcome` is `rejected`, represented safely and deterministically. |
| `diagnostics` | `pd.DataFrame` | Ordered diagnostic records using the approved catalog and severities. |
| `file_summary` | `dict[str, object]` | Reconciled counts, versions and aggregate outcomes without full personal paths. |

The dataclass groups results but does not make the contained DataFrames immutable. The processor MUST create owned output DataFrames and MUST NOT mutate caller-owned inputs. The result contains no open file handles, database connections or global state.

`rejected_rows` contains only rows whose final `row_outcome` is `rejected`. Field-level rejection does not move an otherwise `partially-accepted` row into `rejected_rows`; those rejected field observations remain inspectable through diagnostics and the `rejected_field_observations` summary count.

## Observation Output Schema

Both `accepted_observations` and `review_required_observations` use one row per field observation and contain at least:

| Column | Meaning |
|---|---|
| `local_record_id` | Stable input record identity from the contract. |
| `player` | Local player identity component. |
| `team` | Local team identity component. |
| `league` | Local league identity component. |
| `season` | Local season identity component. |
| `field_name` | Canonical Market Context field represented by the observation. |
| `raw_value` | Safe field value as received from the CSV parser. |
| `normalized_value` | Deterministically normalized value; zero remains numeric zero. |
| `effective_value_date` | Date selected by policy for freshness and conflict analysis. |
| `freshness_status` | `current`, `stale`, `unknown`, `not-applicable` or `future-invalid`. |
| `source_name` | Reviewed source name. |
| `source_type` | Approved source classification. |
| `source_url` | Optional reviewed source URL. |
| `source_reference` | Optional non-secret source reference. |
| `reviewed_at` | Normalized timezone-aware review timestamp. |
| `reviewer` | Reviewer identifier from the input. |
| `confidence` | Normalized confidence classification. |
| `review_status` | Normalized review status. |
| `field_outcome` | Field-level disposition. |
| `conflict_group_id` | Deterministic conflict identifier when applicable, otherwise null. |
| `effective_eligible` | Whether the observation may be considered by a future consolidation decision. |

Freshness semantics:

- `date_of_birth` uses `not-applicable`.
- A populated field without an effective date uses `unknown`.
- An effective date later than `ingested_at` uses `future-invalid`.

Concrete pandas dtypes are deferred to implementation review. `effective_eligible` does not mean that a value has been consolidated into current runtime fields.

For a structurally valid `market_value_eur = 0` observation:

- `normalized_value` MUST be numeric `0`, not null;
- `field_outcome` MUST be `accepted-with-warning`;
- `effective_eligible` MUST be `false`;
- diagnostic `MCV407_MARKET_VALUE_ZERO_NOT_EFFECTIVE` MUST be emitted;
- the minimum row outcome MUST be `accepted-with-warnings`; and
- the observation remains in `accepted_observations` unless another independent rule rejects it or places it under review.

## Rejected Rows Schema

`rejected_rows` contains only rows whose final `row_outcome` is `rejected` and contains at least:

- A field-level rejection does not place an otherwise `partially-accepted` row in `rejected_rows`.
- Rejected field observations within partially accepted rows remain represented through diagnostics and `rejected_field_observations` summary counts.
- A row MUST NOT appear simultaneously as partially accepted and rejected.
- When a file is rejected before rows can be interpreted safely, `rejected_rows` MAY be empty while file diagnostics explain the rejection.
- File-level rejection does not invent row records.

| Column | Meaning |
|---|---|
| `local_record_id` | Contract record ID when structurally available. |
| `player` | Compound identity component when available. |
| `team` | Compound identity component when available. |
| `league` | Compound identity component when available. |
| `season` | Compound identity component when available. |
| `row_outcome` | Deterministic rejected disposition. |
| `primary_diagnostic_code` | First diagnostic by approved severity and deterministic ordering. |
| `diagnostic_count` | Number of diagnostics associated with the row. |
| `safe_row_reference` | Deterministic non-secret reference derived from safe identity fields, never the physical CSV index. |

`safe_row_reference` MUST NOT contain a full serialized row, credentials, provider payloads or a personal absolute path. The physical CSV row index is diagnostic location metadata only and MUST NOT become record identity.

## Diagnostics Schema

The implementation must use exactly the approved diagnostic contract:

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

One additional field is approved as part of the plan:

- `diagnostic_order`: zero-based integer assigned after applying the approved deterministic diagnostic sorting.
- The first emitted diagnostic has value `0`.
- The value MUST be recalculated from final sorted output and MUST NOT depend on raw CSV row order.
- Repeated execution with equivalent canonical input MUST produce the same order values.

`source_file_name` is not approved because it is unnecessary for single-file processing and could expose a local filename. The implementation MUST NOT alter the 38 approved diagnostic codes or their severities.

## File Summary Schema

`file_summary` contains at least:

- `input_contract_version`
- `policy_version`
- `file_outcome`
- `total_rows`
- `accepted_rows`
- `accepted_with_warning_rows`
- `partially_accepted_rows`
- `review_required_rows`
- `rejected_rows`
- `accepted_observations`
- `review_required_observations`
- `rejected_field_observations`
- `diagnostics_by_severity`
- `diagnostics_by_code`
- `duplicate_groups`
- `conflict_groups`
- `current_observations`
- `stale_observations`
- `unknown_freshness_observations`
- `not_applicable_observations`
- `future_invalid_observations`
- `market_value_zero_observation_count`
- `effective_eligible_observation_count`

All counts MUST reconcile with the tabular outputs and remain stable under input reordering where policy semantics are order-independent. A zero market-value observation MUST NOT increase `effective_eligible_observation_count`. The summary MUST NOT expose a personal absolute path.

## Implementation Stages

Each stage requires a separate approval, focused diff review and tests before commit. Approval or completion of one stage does not authorize the next.

### Stage A - Core Contract And File Validation

Include:

- v1 contract and policy constants;
- strict UTF-8 input handling that rejects a BOM under the v1 contract;
- CSV delimiter and header validation;
- schema-version validation;
- strict unknown-column and required-column checks;
- structural type checks required to identify rows safely;
- timezone-aware `reviewed_at` validation;
- season validation;
- duplicate `local_record_id` detection;
- inspectable file-rejected results and deterministic file diagnostics; and
- synthetic structural fixtures and tests.

Exclude:

- field-level Market Context normalization beyond structural parsing;
- freshness;
- duplicate observation and conflict analysis;
- preview CLI;
- real local data;
- SQLite; and
- Streamlit.

### Stage B - Row And Field Normalization

Include:

- compound identity normalization;
- null and empty semantics;
- numeric value normalization;
- ISO date and timezone normalization;
- confidence and review-status validation;
- currency and salary metadata;
- canonical position taxonomy;
- jersey-number validation;
- market-value-zero semantics;
- row and field outcome calculation;
- freshness classification; and
- applicable diagnostics from `MCV200` through `MCV503`.

Exclude duplicate/conflict grouping and preview execution.

### Stage C - Duplicate And Conflict Analysis

Include:

- source identity construction;
- exact duplicate observation handling;
- historical observation handling;
- same-source and cross-source conflicts;
- deterministic conflict-group IDs;
- output disposition;
- deterministic output ordering; and
- reconciliation and input-order-independence tests.

### Stage D - Synthetic Preview

Include:

- a small `argparse` CLI;
- one explicit input path;
- verification only with versioned synthetic fixtures;
- readable file, row, observation, freshness and diagnostic summaries;
- duplicate/conflict and zero-value counts; and
- deterministic exit codes and output.

Exclude persistence, HTML, SQLite, Streamlit, effective-field merging, real data and path discovery. HTML is not planned because the current relevant preview pattern is a console report and no additional presentation layer is justified.

## Synthetic Fixture Matrix

Future fixtures must be small, deterministic and entirely fictitious.

| Fixture | Purpose |
|---|---|
| `valid_minimal.csv` | One minimally valid v1 row. |
| `valid_full.csv` | All supported fields populated with valid synthetic values. |
| `market_value_zero.csv` | Zero preserved with warning `MCV407` and no effective eligibility. |
| `file_schema_errors.csv` | Unsupported version, malformed header and column cases isolated as far as one file can safely represent them. |
| `row_errors.csv` | Identity, season, `reviewed_at` and review-status failures. |
| `field_errors.csv` | Date, numeric, currency and confidence failures. |
| `freshness_cases.csv` | Current, stale, unknown, not-applicable and future-invalid boundaries. |
| `duplicates.csv` | Duplicate record IDs and exact observation duplicates. |
| `conflicts.csv` | Source/date/value/null conflict combinations. |
| `positions.csv` | Canonical position values and unmapped values. |
| `partial_acceptance.csv` | Accepted and rejected field observations in the same row. |

Rules:

- identities and organizations are fictitious;
- URLs use reserved `.test` domains;
- no figures are copied from real players, clubs or providers;
- no real provider is used as an individual source;
- no fixture embeds a provider payload;
- files remain small enough for direct review;
- expected output is deterministic; and
- all fixtures are safe to version.

The completed Stage A implementation created only the three specified synthetic fixture paths. No later-stage fixture is approved.

## Test Plan

### Contract Tests

- supported and unsupported contract versions;
- exact required and allowed columns;
- strict unknown columns;
- valid UTF-8 acceptance and UTF-8 BOM rejection with `MCV104_INVALID_ENCODING`;
- delimiter rejection;
- season structure;
- timezone-aware `reviewed_at`;
- missing and duplicate `local_record_id`; and
- inspectable file rejection.

### Field Validation Tests

- null versus zero;
- negative numeric values;
- salary value, period and currency dependencies;
- confidence requirements and triggers;
- age and date-of-birth ranges and contradiction;
- jersey-number range;
- canonical and unmapped positions; and
- URL validation.

### Freshness Tests

- exact market-value boundaries at 180 and 181 days;
- exact contract and other approved boundaries at 365 and 366 days;
- unknown effective date;
- `date_of_birth` classified as `not-applicable`;
- future-invalid date; and
- timezone-safe comparison against explicit `ingested_at`.

### Outcome Tests

- `accepted`;
- `accepted-with-warnings`;
- `partially-accepted`;
- `review-required`;
- `rejected`;
- `rejected_rows` membership based only on final `row_outcome` and disjoint from partially accepted rows;
- empty `rejected_rows` when a file is rejected before safe row interpretation; and
- file, row and field outcome precedence.

### Duplicate And Conflict Tests

- duplicate local record IDs;
- exact duplicate observations;
- repeated historical values;
- same-source conflicts;
- cross-source conflicts;
- unknown dates;
- null versus populated values;
- deterministic group IDs; and
- input-order independence.

### Market Value Zero Tests

Tests MUST verify exactly that:

- the normalized value is numeric `0`;
- the value is not null;
- `MCV407_MARKET_VALUE_ZERO_NOT_EFFECTIVE` is emitted;
- the field outcome is `accepted-with-warning`;
- the row outcome is at least `accepted-with-warnings`;
- the observation appears in `accepted_observations`;
- `effective_eligible` is `false`; and
- effective market-value coverage is not increased.

### Determinism Tests

- repeated execution produces equal normalized outputs;
- row reordering does not change order-independent semantics;
- diagnostics use a stable sort and consecutive `diagnostic_order` values starting at `0`;
- conflict IDs are stable; and
- summaries reconcile with all result tables.

### Regression And Full Tests

Each approved stage must run:

```powershell
.venv\Scripts\python.exe -m pytest -p no:cacheprovider tests/test_manual_market_context_processing.py -q
.venv\Scripts\python.exe -m pytest -p no:cacheprovider tests -q
.venv\Scripts\python.exe -m compileall src scripts
```

Stage D must additionally run the approved synthetic preview smoke command.

## Preview Contract

The future synthetic preview command is:

```powershell
.venv\Scripts\python.exe scripts\preview_manual_market_context.py `
  --input tests\fixtures\manual_market_context\valid_full.csv `
  --ingested-at 2026-07-23T10:00:00Z
```

It displays:

- file outcome;
- row outcomes;
- accepted, review-required and rejected observation counts;
- freshness counts;
- diagnostics by severity and code;
- duplicate and conflict group counts;
- zero market-value observation count; and
- effective-eligible observation count.

Rules:

- `--input` is required.
- `--ingested-at` is required and timezone-aware.
- No input auto-discovery or personal default path is allowed.
- No output file is written unless a later decision changes this boundary.
- No SQLite, Streamlit or effective-field merge is allowed.
- File rejection returns a non-zero exit code.
- Row or field warnings do not require a non-zero exit code when the file is processable.
- Output ordering and formatting are deterministic.

## Error Handling Boundary

- Expected contract violations become approved diagnostics.
- Programming errors are not hidden as diagnostics.
- File rejection remains inspectable through the structured result whenever the input can be parsed safely enough to construct one.
- The implementation MUST NOT catch `Exception` indiscriminately.
- No demo-data fallback is allowed.
- Processing stops when encoding, delimiter, header or schema failures prevent safe interpretation.
- Console output MUST NOT print credentials, full unsafe rows or personal absolute paths.
- File-not-found and operating-system read failures may raise narrow standard-library exceptions; the future CLI converts those exceptions into a safe message and non-zero exit code.

## Dependency Boundary

Approved future dependencies are limited to:

- Python standard library; and
- pandas, already present in the repository.

The plan does not approve Pydantic, Pandera, new date libraries, new CLI libraries or any other dependency. A dependency change requires a separate decision.

## Explicit Non-Goals

- Real-data migration.
- Reading any existing `.local.csv`.
- Provider-cache access.
- API calls or provider integration.
- Currency conversion.
- Automatic identity crosswalks.
- Source precedence.
- Effective consolidation.
- Replacement of the existing Market Context loader or merge.
- SQLite.
- Streamlit.
- HTML dashboard output.
- Production deployment.
- Background jobs.
- Automatic file discovery.

## Stage Approval Boundary

- The complete plan is approved as documentation.
- Full milestone implementation is not authorized.
- Stage A is implemented, verified and closed under its separate approval and closeout.
- Stage B is approved for a separate code block and is not implemented.
- Stages C-D remain unapproved.
- Each stage requires a separate decision, focused diff, stage-specific tests, full pytest, compileall and a clean status after any later approved commit.
- Only synthetic fixtures may be used.

## Success Criteria

This plan is considered fully executed only when:

- Stages A-D are separately implemented and approved;
- all 38 diagnostic codes are covered or explicitly justified;
- synthetic fixtures cover valid and invalid contract behavior;
- outputs and conflict IDs are deterministic;
- summaries reconcile with result tables;
- market-value-zero semantics are verified;
- the full test suite passes;
- the synthetic preview works under its approved contract;
- real data remains untouched; and
- SQLite and Streamlit remain outside scope unless separately approved.

## Implementation Plan Decision Boundary

The bounded implementation plan is approved docs-only.

Stage A was separately authorized, implemented and closed under its Stage A decision and closeout. Stage B is approved but not implemented. Preview execution remains unauthorized.

Next permitted action: implement Stage B only under its approved file, diagnostic and test boundaries.

No other stage receives automatic approval.
