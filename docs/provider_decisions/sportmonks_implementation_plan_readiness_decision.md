# Sportmonks Implementation Plan Readiness Decision

## Status

- Candidate: Sportmonks
- Decision status: `approved-to-create-implementation-plan`
- Related transform design plan: [Sportmonks Transform Design Plan](../provider_candidates/sportmonks_transform_design_plan.md)
- Related transform design suitability decision: [Sportmonks Transform Design Suitability Decision](sportmonks_transform_design_suitability_decision.md)
- Related payload decision record: [Sportmonks Payload Decision Record](sportmonks_payload_decision_record.md)
- Related implementation plan: [Sportmonks Implementation Plan](../provider_candidates/sportmonks_implementation_plan.md)
- Related first-code approval decision: [Sportmonks First Code Implementation Approval Decision](sportmonks_first_code_implementation_approval_decision.md)
- Provider approval: no
- Implementation plan approved: yes, docs-only
- Implementation plan created: yes, docs-only
- First code implementation approval: approved under strict scope
- Transform code approved: yes, only for the approved local-only scaffold; broader transform implementation remains blocked
- API calls performed in this block: no
- Raw responses reviewed in this block: no
- `.local.csv` outputs created: no
- SQLite writes performed: no
- Streamlit activation performed: no
- Local trial performed: no

## Decision

- The transform design plan is sufficient to approve creating a future implementation plan.
- The approval is for an implementation plan document only.
- This does not approve implementation.
- This does not approve Sportmonks as a provider.
- This does not authorize API calls, raw payload review, local trial, SQLite writes, Streamlit activation or parser/transform code.

## Evidence Reviewed

| Artifact | Result | Interpretation |
|---|---|---|
| Minimal ID discovery | passed | IDs and endpoint access confirmed |
| Confirmed ID scope review | passed | Scoped IDs formally reviewed |
| Minimal payload field review | passed | Field shape reviewed from cache with 0 API calls |
| Suitability assessment | partially suitable | Enough for planning, not enough for direct implementation |
| Transform design plan | created docs-only | Candidate mappings and gaps documented |

## Readiness Assessment

| Area | Status | Implementation-Plan Implication |
|---|---|---|
| Input endpoint | ready for planning | One endpoint shape confirmed |
| Confirmed IDs | ready for planning | League, season and team IDs known |
| Candidate mappings | ready for planning | Mapping candidates exist |
| Validation rules | ready for planning | Rules can be converted into implementation requirements |
| Provenance strategy | partial | Implementation plan must define exact fields |
| Freshness strategy | partial | Implementation plan must decide cache timestamp versus metadata |
| Label strategy | partial | Implementation plan must choose ID-only or separate label review |
| Market Context coverage | not demonstrated | Implementation plan must keep Market Context separate |
| Cleanup/retention | pending | Implementation plan must include an ignored local retention policy |

## Conditions For Future Implementation Plan

The future implementation plan must:

- Stay documentation-only.
- Define exact files or modules that might be created later, without creating them.
- Define the test strategy before code.
- Define ignored local input and output paths.
- Define no-network and default-off behavior.
- Define secret handling.
- Define schema and validation requirements.
- Define provenance and freshness fields.
- Define the label-resolution decision.
- Define cleanup and retention policy.
- Define rollback and stop conditions.
- Define acceptance criteria before any implementation.

## Implementation Plan Must Not

- Create code.
- Modify `src/`.
- Modify `app.py`.
- Modify `scripts/`.
- Modify tests.
- Call APIs.
- Read raw JSON.
- Create `.local.csv`.
- Write SQLite.
- Activate Streamlit.
- Approve Sportmonks.
- Commit provider cache.
- Commit credentials.

## Open Issues The Implementation Plan Must Resolve

| Issue | Required Handling |
|---|---|
| Human-readable player labels missing | Choose ID-only, local join or future approved lookup review |
| Position labels missing | Choose ID-only mapping or future approved lookup/include review |
| Freshness unclear | Define `source_observed_at` and freshness basis |
| Provenance unclear | Define required provenance fields before code |
| Market Context not demonstrated | Keep age, value and contract enrichment separate |
| Cleanup pending | Define cache and output retention and deletion rules |
| Trial output path not approved | Define an ignored local output path only if later permitted |
| Provider approval absent | Ensure the implementation plan cannot imply approval |

## Still Forbidden

- Implementation.
- Parser code.
- Normalizer code.
- SQLite loading.
- Streamlit integration.
- Local trial.
- API calls.
- Raw JSON review.
- `.local.csv` outputs.
- Broad payload inspection.
- Provider approval.

## Next Required Action

A future local-only code implementation block may create only the files approved by the [first-code implementation approval decision](sportmonks_first_code_implementation_approval_decision.md).

No API calls, raw JSON review, `.local.csv`, SQLite writes, Streamlit activation, local trial or provider approval are allowed by this decision.
