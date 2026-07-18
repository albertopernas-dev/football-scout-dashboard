# v0.8.0 Provider Permission Response Handling Plan

## Objective

v0.8.0 defines how to handle a real provider response or applicable license or subscription terms. A substantive Sportmonks response has now been recorded only as a non-sensitive summary. This does not approve Sportmonks or authorize skipping the checklist and payload-specific decision record.

The recorded evidence supports moving the Stage 1 gate to `continue` for the next governance step only. No broad payload inspection has been performed, minimal ID discovery has passed, local credential setup remains outside Git and no integration has started.

## Starting Point

v0.7.0 was published as a documentation and governance milestone. Sportmonks has:

- a Stage 0 intake pack;
- a Stage 1 license and terms gate;
- partial public-source review notes; and
- a permission request sent log; a [ticket acknowledgement log](provider_candidates/sportmonks_ticket_acknowledgement_log.md); and a [non-sensitive substantive response summary](provider_candidates/sportmonks_permission_response_summary.md).

The current gate decision is `continue`. The checklist, decision records and minimal field review are complete; only a docs-only transform design plan is now permitted. This does not approve the provider or local trial.

## Scope

In scope:

- Record non-sensitive provider response summaries.
- Record explicit permissions and explicit restrictions.
- Update the Sportmonks gate decision only if evidence supports it.
- Prepare a checklist only if the gate moves to `continue`.
- Prepare and review a payload-specific decision record before any concrete permitted payload is inspected.
- Keep confidential terms and raw responses out of Git.
- Record minimal ID discovery results only as non-sensitive summaries.
- Record a docs-only confirmed ID scope review before any payload field review decision.
- Record a strict minimal payload field review decision before any field review is executed.
- Record the completed minimal payload field review as a non-sensitive field/category summary.
- Record a docs-only suitability decision before any transform design is created.
- Record the documentation-only transform design plan before any implementation-plan decision.
- Record a docs-only readiness decision before any implementation plan is created.
- Record the [Sportmonks Implementation Plan](provider_candidates/sportmonks_implementation_plan.md) as documentation only before any first-code-implementation approval decision.
- Record the [Sportmonks First Code Implementation Approval Decision](provider_decisions/sportmonks_first_code_implementation_approval_decision.md) before any implementation begins.
- Record the [Sportmonks Implementation Summary](provider_candidates/sportmonks_implementation_summary.md) before any local preview run decision.

Out of scope:

- Payload inspection before the checklist and payload-specific decision record are prepared.
- Credential creation before the checklist and payload-specific decision record are prepared.
- Additional API calls after the completed minimal field review without a new explicit decision.
- Scraping.
- Provider caching beyond the existing ignored ID discovery response used by the completed minimal field review.
- `.local.csv` outputs from provider data.
- SQLite writes.
- Streamlit activation.
- Parser or transform code for real provider payloads.
- Publishing confidential legal text.

## Response Handling Workflow

1. Receive a response or applicable license or subscription terms.
2. Classify sensitivity as public, shareable summary, or confidential/do not commit.
3. Extract only a non-sensitive summary.
4. Record explicit permissions and restrictions.
5. Identify unresolved questions.
6. Recommend a gate decision: `continue`, `defer` or `reject`.
7. Update the Sportmonks license gate only if evidence is clear.
8. If the gate moves to `continue`, prepare the checklist.
9. Prepare and review a payload-specific decision record before any concrete permitted payload is inspected.
10. Keep all raw or confidential materials outside Git.

## Response Summary Document

The substantive response is recorded in [Sportmonks Permission Response Summary](provider_candidates/sportmonks_permission_response_summary.md).

The summary contains no confidential text, ticket identifiers, payloads or credentials. The raw response remains outside Git.

## Gate Decision Rules

- **continue:** only when local evaluation, payload inspection and required handling permissions are explicit enough. This does not approve the provider; it permits only the next governance step, the checklist and decision record.
- **defer:** when permissions remain unclear or incomplete.
- **reject:** when terms block the intended use.
- **stop:** when restricted data, credentials or payloads were accessed improperly.

## Evidence Basis For Continue

- Applicable terms, license or subscription scope identified.
- Payload inspection permission clear.
- Local development or evaluation permission clear.
- Local caching and retention rules clear.
- Derived-output permission clear.
- Redistribution, demo and screenshot restrictions clear.
- Credential and account handling rules clear.
- Endpoint, field and plan scope clear enough for the intended review.
- Confidential materials kept outside Git.

## Safety Rules

- Do not commit raw provider responses if confidential.
- Do not commit legal text excerpts beyond short non-sensitive summaries.
- Do not commit payloads.
- Do not commit credentials.
- Do not commit provider cache.
- Do not commit `.local.csv` outputs from provider data.
- Do not inspect payloads until the checklist and payload-specific decision record are prepared.
- Keep credentials local, ignored and absent from docs, diffs, logs and commits.
- Do not add parser or transform code; the current suitability decision permits documentation only.

## Acceptance Criteria

- [ ] v0.8.0 plan exists.
- [ ] README current milestone points to v0.8.0.
- [ ] ROADMAP marks v0.7.0 as completed and published.
- [ ] ROADMAP identifies v0.8.0 as the current milestone.
- [ ] No provider response is invented.
- [ ] No provider approval is claimed.
- [ ] No broad payload inspection has been performed.
- [ ] No tracked product code is changed.
- [ ] No provider data files are tracked or committed.
- [ ] `git diff --check` passes.
- [ ] Final `git status --short` is clean before commit.

## Next Steps

1. The [Sportmonks Provider Payload Checklist](provider_candidates/sportmonks_provider_payload_checklist.md) exists as draft/pre-trial.
2. The [Sportmonks Payload Decision Record](provider_decisions/sportmonks_payload_decision_record.md) exists as draft/pre-trial.
3. The [Sportmonks Ignored Local Trial Scope Plan](provider_candidates/sportmonks_ignored_local_trial_scope_plan.md) remains draft/pre-trial.
4. The Football Free Plan is confirmed by user screenshot, which shows 4 leagues and 3000 API calls.
5. The Free Plan league list is confirmed, and Denmark Superliga `league_id 271` is selected for the minimal trial scope.
6. Manual UI lookup did not expose the IDs; minimal API discovery later confirmed Denmark Superliga 2026/2027 `season_id 27897` and FC København `team_id 85`.
7. The [Sportmonks ID Discovery Plan](provider_candidates/sportmonks_id_discovery_plan.md) is completed for minimal discovery.
8. The [Sportmonks Secure Credential Setup](provider_candidates/sportmonks_secure_credential_setup.md) is verified/local-only.
9. The [Sportmonks Local Credential Setup Verification](provider_candidates/sportmonks_local_credential_setup_verification.md) records that local credential setup passed outside Git.
10. The [Sportmonks Minimal ID Discovery Summary](provider_candidates/sportmonks_minimal_id_discovery_summary.md) records 3 scoped calls and HTTP 200 squad endpoint access.
11. The [Sportmonks Confirmed ID Scope Review](provider_candidates/sportmonks_confirmed_id_scope_review.md) has passed.
12. The [Sportmonks Minimal Payload Field Review Decision](provider_decisions/sportmonks_minimal_payload_field_review_decision.md) defined the strict review scope.
13. The [Sportmonks Minimal Payload Field Review Summary](provider_candidates/sportmonks_minimal_payload_field_review_summary.md) records a `passed` review from existing ignored cache with 0 API calls.
14. The [Sportmonks Transform Design Suitability Decision](provider_decisions/sportmonks_transform_design_suitability_decision.md) approved documentation-only planning.
15. The [Sportmonks Transform Design Plan](provider_candidates/sportmonks_transform_design_plan.md) is created as documentation only.
16. The [Sportmonks Implementation Plan Readiness Decision](provider_decisions/sportmonks_implementation_plan_readiness_decision.md) approved only docs-only implementation planning.
17. The [Sportmonks Implementation Plan](provider_candidates/sportmonks_implementation_plan.md) is created as documentation only.
18. The [Sportmonks First Code Implementation Approval Decision](provider_decisions/sportmonks_first_code_implementation_approval_decision.md) approved only the listed local-only, default-off, synthetic-test-first and no-network files.
19. The [Sportmonks Implementation Summary](provider_candidates/sportmonks_implementation_summary.md) records that the first scaffold is created without API calls or real provider payloads.
20. The next action is a docs-only local preview run approval decision.
21. Keep raw payloads, provider cache, `.local.csv` outputs, credentials and confidential correspondence outside Git.
22. Continue to treat Sportmonks as unapproved; API calls, integration, local trial and provider approval remain blocked.
