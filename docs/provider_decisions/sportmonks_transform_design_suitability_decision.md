# Sportmonks Transform Design Suitability Decision

## Status

- Candidate: Sportmonks
- Decision status: `approved-to-plan-transform-design`
- Related minimal payload field review summary: [Sportmonks Minimal Payload Field Review Summary](../provider_candidates/sportmonks_minimal_payload_field_review_summary.md)
- Related minimal payload field review decision: [Sportmonks Minimal Payload Field Review Decision](sportmonks_minimal_payload_field_review_decision.md)
- Related payload decision record: [Sportmonks Payload Decision Record](sportmonks_payload_decision_record.md)
- Transform design plan: [Sportmonks Transform Design Plan](../provider_candidates/sportmonks_transform_design_plan.md)
- Implementation plan readiness decision: [approved for docs-only planning](sportmonks_implementation_plan_readiness_decision.md)
- Provider approval: no
- Transform design planning approved: yes, docs-only
- Transform design created in this block: yes, docs-only
- Transform implementation approved: no
- Implementation-plan readiness: `approved-to-create-implementation-plan`
- API calls performed in this block: no
- Raw responses reviewed in this block: no
- SQLite writes performed: no
- Streamlit activation performed: no
- Parser/transform code created: no
- Local trial performed: no

## Decision

- The observed Sportmonks squad payload shape is sufficient to plan a future docs-only transform design.
- The suitability is partial, not complete.
- Transform design planning may proceed only as documentation.
- This does not approve implementation.
- This does not approve Sportmonks as a provider.
- This does not authorize additional API calls, local trial, SQLite writes, Streamlit activation or parser/transform code.

## Evidence Summary

| Area | Result | Interpretation |
|---|---|---|
| Review status | passed | Minimal field review completed safely |
| Suitability | partially suitable | Enough for transform planning, not enough for implementation |
| Source | existing ignored cache | No new API call required |
| API calls in review | 0 | No new provider call during field review |
| Data count | 6 | Small scoped sample |
| Raw JSON committed | no | Safe |
| Provider cache committed | no | Safe |

## Useful Observed Categories

| Category | Status | Design Implication |
|---|---|---|
| Player identity/reference | present | Can plan ID mapping around player references |
| Team/squad context | present | Can plan team- and season-scoped squad context |
| Season context | present | Can plan season-scoped records |
| Position/role | present by ID | May require label resolution later |
| Jersey number | present | Can plan an optional squad detail field |

## Gaps And Risks

| Gap | Risk | Required Future Decision |
|---|---|---|
| No clear record-level dates | Freshness may be weak | Decide whether external freshness or provenance metadata is needed |
| Freshness unclear | Hard to judge update age | Decide whether response metadata or cache timestamp is enough |
| Record-level provenance unclear | Traceability may be incomplete | Define provenance fields in the transform design |
| Player labels unclear | UI and report readability may be limited | Decide whether label enrichment is needed |
| Position labels unclear | Position mapping may require lookup | Decide whether a position lookup or include is needed |
| Market Context coverage not demonstrated | Not enough for age, value or contract enrichment | Keep the Market Context transform separate |

## Approved Future Transform Design Scope

A later docs-only block may create a transform design plan.

That plan may define:

- input endpoint shape assumptions;
- field mapping candidates;
- canonical output candidate fields;
- provenance and freshness strategy;
- validation rules;
- stop conditions; and
- future decisions needed for labels or includes.

That plan must not:

- implement code;
- read raw JSON;
- make API calls;
- write SQLite;
- create `.local.csv`;
- activate Streamlit; or
- approve Sportmonks.

## Explicitly Not Approved

- Transform implementation.
- Parser code.
- Normalizer code.
- SQLite loading.
- Streamlit integration.
- Local trial execution.
- Broad payload inspection.
- Additional API calls.
- Player-detail endpoint calls.
- Includes for labels.
- Provider approval.

## Required Future Transform Design Plan Sections

The future design document must include:

- Scope and non-goals.
- Input endpoint and confirmed IDs.
- Observed field categories.
- Candidate canonical fields.
- Fields explicitly not available from this endpoint.
- Provenance and freshness strategy.
- Label-resolution strategy.
- Validation rules.
- Local file and cache handling.
- Stop conditions.
- Open decisions before implementation.

## Next Required Action

The [Sportmonks Transform Design Plan](../provider_candidates/sportmonks_transform_design_plan.md) has been created as documentation only. The [readiness decision](sportmonks_implementation_plan_readiness_decision.md) approves only a future docs-only implementation plan.

That future implementation plan is still not implementation.

No transform code, API calls, raw JSON review, SQLite writes, Streamlit activation, `.local.csv` outputs, local trial or provider approval are allowed.
