# v0.10.0 Manual Market Context Workflow Hardening Scope Plan

## Status

- Milestone: v0.10.0
- Plan status: `manual-market-context-scope-opened`
- Related v0.9.0 closeout decision: [v0.9.0 Provider Suitability Closeout Decision](provider_decisions/v0_9_0_provider_suitability_closeout_decision.md)
- Related v0.9.0 release notes: [Release Notes v0.9.0](release_notes_v0_9_0.md)
- Canonical input contract: [v0.10.0 Reviewed Local Market Context Input Contract](v0_10_0_manual_market_context_input_contract.md)
- Contract decision: [v0.10.0 Reviewed Local Market Context Input Contract Decision](provider_decisions/v0_10_0_manual_market_context_input_contract_decision.md)
- Contract version: `manual-market-context-input-v1`
- Contract status: approved docs-only
- Processing policy: [v0.10.0 Reviewed Local Market Context Processing Policy](v0_10_0_manual_market_context_processing_policy.md)
- Policy decision: [v0.10.0 Reviewed Local Market Context Processing Policy Decision](provider_decisions/v0_10_0_manual_market_context_processing_policy_decision.md)
- Policy version: `manual-market-context-policy-v1`
- Policy status: approved docs-only
- Implementation plan: [v0.10.0 Reviewed Local Market Context Implementation Plan](v0_10_0_manual_market_context_implementation_plan.md)
- Implementation plan decision: [v0.10.0 Reviewed Local Market Context Implementation Plan Decision](provider_decisions/v0_10_0_manual_market_context_implementation_plan_decision.md)
- Implementation plan status: approved docs-only
- Stage A plan: [v0.10.0 Reviewed Local Market Context Stage A Plan](v0_10_0_manual_market_context_stage_a_plan.md)
- Stage A decision: [v0.10.0 Reviewed Local Market Context Stage A Decision](provider_decisions/v0_10_0_manual_market_context_stage_a_decision.md)
- Stage A implementation approved: yes, for a separate code block
- Stage A implemented: no
- Stage B approved: no
- Stage C approved: no
- Stage D approved: no
- Selected path: Manual Market Context workflow improvements
- Full implementation approved: no
- Real local data access approved: no
- Provider integration approved: no
- Provider approval: none
- API calls approved: no
- SQLite writes approved: no
- Streamlit changes approved: no
- New dependencies approved: no

## Background

- v0.9.0 completed provider comparison without approving any provider.
- API-Football remains the statistics baseline.
- Transfermarkt remains manual-reference-only.
- Sportmonks and Capology require separate clarification decisions.
- The currently usable Market Context path remains reviewed local CSV enrichment.
- v0.10.0 focuses on making that local workflow safer, clearer and more reproducible.

## Goal

Create a governed, deterministic and diagnosable workflow for reviewed local Market Context inputs before any further UI or provider integration.

The future workflow must:

- Preserve canonical Market Context fields.
- Validate schema and values.
- Distinguish source date from ingestion date.
- Retain provenance.
- Detect duplicates and conflicts.
- Produce actionable diagnostics.
- Keep real inputs and generated local outputs outside Git.
- Support synthetic fixtures for committed tests.
- Avoid provider-specific assumptions.

## In Scope

- Canonical local input contract.
- Required and optional column definitions.
- Source and provenance fields.
- Value-date and freshness model.
- Duplicate and conflict policy.
- Validation severity model.
- Deterministic normalization rules.
- Diagnostics and rejection reporting.
- Safe local filename and ignore conventions.
- Synthetic fixture strategy.
- Test plan.
- Future integration boundary with the existing Market Context layer.

## Out Of Scope

- Provider research.
- Provider contact.
- Provider APIs.
- Scraping.
- Automated Transfermarkt ingestion.
- Sportmonks or Capology trials.
- New statistics ingestion.
- UI redesign.
- Streamlit integration.
- SQLite loading.
- Real player datasets committed to Git.
- Automatic conflict resolution using external sources.
- Numeric provider scoring.
- Multi-provider architecture.
- Production deployment.

## Proposed Canonical Input Areas

### Identity

- Player ID.
- Provider-independent local identity or mapping key.
- Player name.
- Team.
- Competition.
- Season.

### Market Context

- Market value.
- Market value currency.
- Contract end.
- Salary or compensation context.
- Salary currency.
- Age or date of birth.
- Jersey number.
- Position.

### Provenance

- Source name.
- Source URL or reviewed reference.
- Source classification.
- Value date.
- Reviewed at.
- Reviewer.
- Notes.

### Workflow Metadata

- Local record identifier.
- Ingestion timestamp.
- Validation status.
- Conflict status.
- Effective-field indicators.

These are design areas, not a final contract. Not every field will be required, and the definitive schema requires a separate block.

## Freshness And Date Model

The milestone must distinguish:

- `value_date`: date to which the data applies.
- `reviewed_at`: date of manual review.
- `ingested_at`: date of local ingestion.
- `contract_end`: business data, not a technical date.
- File modification time: must not act as a value date.

Future rules must:

- Not infer freshness only from a filename.
- Not replace a known value date with ingestion time.
- Record unknown dates explicitly.
- Allow field-level policies when market value, salary and contract end have different dates.

## Duplicate And Conflict Design

The future design must cover:

- Exact duplicate rows.
- The same player and field with different values.
- The same player with different source dates.
- The same player mapped to multiple identities.
- Undefined source precedence.
- Stale versus newer values.
- Null versus populated values.
- Conflicting manual references.

Silent resolution is not approved. Conflicts must be preserved, diagnosed, rejected or marked for review under an explicit and tested policy.

## Validation Severity Model

Proposed levels:

### Error

- Missing required identity.
- Invalid date.
- Invalid currency.
- Duplicate local record identifier.
- Impossible numeric value.
- Unsupported schema version.

### Warning

- Missing optional Market Context field.
- Unknown value date.
- Stale data.
- Unresolved mapping.
- Conflicting source value.

### Info

- Normalized label.
- Derived age.
- Optional field omitted.
- Record unchanged.

Definitive diagnostic codes will be decided in another block.

## Governance And Local Safety

- Real inputs remain ignored by Git.
- Provider cache remains ignored.
- `.env` remains ignored.
- No credentials in files.
- No raw provider payloads committed.
- Only synthetic fixtures may be committed.
- Derived local outputs must use ignored paths.
- Local filenames should clearly identify reviewed/manual status.
- No silent fallback from malformed real data to demo data.

## Candidate Future Architecture

```text
reviewed local CSV
        |
        v
schema validation
        |
        v
normalization
        |
        v
identity mapping
        |
        v
conflict detection
        |
        v
canonical Market Context preview
        |
        v
future approved persistence or UI integration
```

- Full implementation is not approved; Stage A alone is separately approved and remains unimplemented.
- SQLite and Streamlit remain outside this milestone for now.
- Every transition must be observable and diagnosable.

## Canonical Input Contract

The initial reviewed local input contract is defined in [v0.10.0 Reviewed Local Market Context Input Contract](v0_10_0_manual_market_context_input_contract.md) and approved as documentation by the [contract decision](provider_decisions/v0_10_0_manual_market_context_input_contract_decision.md).

- Contract version: `manual-market-context-input-v1`.
- Status: approved docs-only.
- The existing `player`, `team`, `league`, `season` compound identity is retained.
- Stage A structural parser/validation and its three synthetic fixtures are separately approved; broader validation, Stages B-D, preview and real-data processing remain blocked.
- Freshness, provenance, validation and duplicate/conflict policy are completed docs-only.
- The market-value-zero parser blocker is resolved through observation/effective separation.

## Processing Policy

The [v0.10.0 Reviewed Local Market Context Processing Policy](v0_10_0_manual_market_context_processing_policy.md) and its [decision record](provider_decisions/v0_10_0_manual_market_context_processing_policy_decision.md) are approved docs-only.

- Policy version: `manual-market-context-policy-v1`.
- Date resolution and freshness thresholds are defined.
- Provenance, validation severity and the diagnostic catalog are defined.
- Duplicate and conflict outcomes are defined without source precedence or automatic consolidation.
- Stage A structural parser and its three synthetic fixtures are approved but unimplemented; broader parser work and preview remain unapproved.
- The next action is Stage A implementation only.

## Proposed Workstreams

| Workstream | Purpose | Current Approval |
|---|---|---|
| Input contract design | Define canonical reviewed local input | not approved for implementation |
| Freshness and provenance design | Preserve source dates and lineage | not approved for implementation |
| Validation design | Define errors, warnings and diagnostics | not approved for implementation |
| Conflict policy design | Prevent silent overwrites | not approved for implementation |
| Synthetic fixture design | Enable committed testing safely | three Stage A fixtures approved only |
| Parser/normalizer implementation | Build deterministic local processing | Stage A structural parser approved only; normalization blocked |
| Preview/report implementation | Review normalized output and failures | not approved |
| SQLite integration | Persist effective Market Context | not approved |
| Streamlit integration | Surface diagnostics and context | not approved |

## Risks

- Unreliable manual identity matching.
- Stale market values.
- Currencies without normalization.
- Mixing source dates and ingestion dates.
- Silently replacing valid data with newer but less reliable values.
- Treating estimated salaries as official.
- Committing real data accidentally.
- Duplicated logic between preview and application paths.
- Provider-specific fields leaking into the canonical schema.
- Excessive governance without usable implementation.

## Success Criteria For v0.10.0

The milestone may be considered complete when later blocks establish that:

- A canonical input contract is approved.
- Validation and conflict policies are approved.
- A deterministic parser/normalizer is implemented.
- Committed synthetic fixtures cover valid and invalid cases.
- Real data remains ignored.
- Diagnostics are actionable.
- Full tests pass.
- An approved preview demonstrates the workflow.
- SQLite and Streamlit remain separate decisions unless later authorized.

This block does not meet those criteria. It only opens the scope.

## Decision Options After Scope Opening

1. Define the canonical input contract.
2. Define freshness and provenance rules first.
3. Define duplicate and conflict rules first.
4. Stop v0.10.0 before implementation.
5. Rescope the milestone.

## Recommended Next Action

The bounded implementation plan is approved docs-only. Stage A implementation is separately approved and remains unimplemented.

Next action: implement Stage A only. Stages B-D, real-data processing, SQLite and Streamlit remain unauthorized.
