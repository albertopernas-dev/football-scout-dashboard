# Sportmonks Payload Decision Record

## Status

- Candidate: Sportmonks
- Decision record status: draft/pre-trial
- Related gate: [Sportmonks License And Terms Gate](../provider_candidates/sportmonks_license_terms_gate.md)
- Related response summary: [Sportmonks Permission Response Summary](../provider_candidates/sportmonks_permission_response_summary.md)
- Related checklist: [Sportmonks Provider Payload Checklist](../provider_candidates/sportmonks_provider_payload_checklist.md)
- Related trial scope plan: [Sportmonks Ignored Local Trial Scope Plan](../provider_candidates/sportmonks_ignored_local_trial_scope_plan.md)
- Related ID discovery plan: [Sportmonks ID Discovery Plan](../provider_candidates/sportmonks_id_discovery_plan.md)
- Related credential setup: [Sportmonks Secure Credential Setup](../provider_candidates/sportmonks_secure_credential_setup.md)
- Related credential verification: [Sportmonks Local Credential Setup Verification](../provider_candidates/sportmonks_local_credential_setup_verification.md)
- Discovery summary: [Sportmonks Minimal ID Discovery Summary](../provider_candidates/sportmonks_minimal_id_discovery_summary.md)
- Confirmed ID scope review: [passed](../provider_candidates/sportmonks_confirmed_id_scope_review.md)
- Minimal payload field review decision: [approved under strict scope](sportmonks_minimal_payload_field_review_decision.md)
- Minimal payload field review summary: [passed](../provider_candidates/sportmonks_minimal_payload_field_review_summary.md)
- Transform design suitability decision: [approved for docs-only planning](sportmonks_transform_design_suitability_decision.md)
- Transform design plan: [created docs-only](../provider_candidates/sportmonks_transform_design_plan.md)
- Implementation plan readiness decision: [approved for docs-only planning](sportmonks_implementation_plan_readiness_decision.md)
- Implementation plan: [created docs-only](../provider_candidates/sportmonks_implementation_plan.md)
- First code implementation approval: [approved under strict local-only scope](sportmonks_first_code_implementation_approval_decision.md)
- Implementation summary: [first local-only scaffold created](../provider_candidates/sportmonks_implementation_summary.md)
- Local preview run approval: [approved / executed](sportmonks_local_preview_run_approval_decision.md)
- Local preview run summary: [completed](../provider_candidates/sportmonks_local_preview_run_summary.md)
- Stage 1 gate decision: `continue`
- Provider approval: no
- Production approval: no
- Broad payload inspection performed: no
- Credentials created locally: yes, outside Git
- Credentials stored in Git: no
- API calls performed: yes, 3 minimal discovery calls
- Local provider cache created: yes, ignored
- Provider cache committed: no
- Local trial performed: no
- SQLite writes performed: no
- Streamlit activation performed: no
- Parser/transform code created: no
- Notes: This record defines decision boundaries before a possible minimal local trial. It does not approve Sportmonks as a provider or authorize production use.

## Purpose

This decision record defines the required scope and constraints before any Sportmonks payload inspection or local trial. It converts the Stage 1 `continue` gate into a controlled pre-trial decision framework.

It does not inspect payloads, select a final provider, expose credentials or start integration. All raw provider data and credentials must remain outside Git.

## Evidence Basis

- The [Stage 1 gate](../provider_candidates/sportmonks_license_terms_gate.md) moved to `continue` for the next governance step only.
- A [non-sensitive permission response summary](../provider_candidates/sportmonks_permission_response_summary.md) exists.
- The [provider payload checklist](../provider_candidates/sportmonks_provider_payload_checklist.md) exists as a draft/pre-trial artifact.
- The permission response summary records local evaluation, payload and schema inspection, and local caching for development or debugging under an active subscription and applicable Terms of Service.
- It also records internal normalized or canonical outputs and internal derived-output documentation and demos under the stated restrictions.
- Raw data must not be exposed or redistributed.
- API keys must not be committed or exposed.
- Data availability depends on the selected plan and competitions.

## Decision Scope

| Area | Decision | Status | Notes |
|---|---|---|---|
| Provider approval | Not approved. | fixed | This record does not approve Sportmonks as final provider. |
| Production use | Not approved. | fixed | Production use is out of scope. |
| Local evaluation | May be planned. | allowed with conditions | Requires selected plan, checklist completion and secure credentials. |
| Payload inspection | May be planned. | allowed with conditions | Only minimal schema, field and suitability inspection after checklist review. |
| Credentials | Prepared locally outside Git. | verified/local-only | Token remains ignored, untracked and undisclosed. |
| Local caching | May be planned. | allowed with conditions | Only under ignored local paths, active subscription and Terms of Service compliance. |
| Derived outputs | May be planned. | allowed with conditions | Internal normalized or canonical outputs only, with no raw redistribution. |
| Documentation/demo | May use derived non-raw summaries. | allowed with conditions | No raw payload excerpts. |
| SQLite | Not allowed in trial. | forbidden | Keep trial isolated. |
| Streamlit app | Not allowed in trial. | forbidden | No app activation. |
| Parser/transform code | Not allowed in this block. | forbidden | Later explicit block only. |

## Trial Scope To Define Before Execution

| Area | Required Decision | Current Status |
|---|---|---|
| Selected Sportmonks plan | Football Free Plan confirmed by user screenshot. | confirmed |
| Selected competition(s) | Denmark Superliga, league_id 271. | confirmed |
| Selected season | Denmark Superliga 2026/2027, `season_id 27897`. | confirmed |
| Selected team | FC København, `team_id 85`. | confirmed |
| Endpoint(s) | Team Squad by Team and Season ID primary; Players auxiliary only if needed for schema/include validation. | primary access confirmed; field review pending |
| Field categories | Must be mapped to Market Context needs. | pending |
| Sample size | One FC København squad, one Denmark Superliga season, minimal payload. | proposed; field review not executed |
| Raw payload path | Must be an ignored local path. | ID discovery responses stored locally under ignored provider cache; trial path pending |
| Cache path | Must be an ignored local path. | ignored ID discovery cache verified; trial retention pending |
| Retention/cleanup | Must be documented before trial. | pending |
| Credential storage | Must use ignored local environment or configuration. | verified outside Git |
| Expected derived output | Must avoid raw data exposure. | pending |
| Stop conditions | Must be reviewed before trial. | pending |

## Free Plan League Selection Rationale

- Denmark Superliga is included in the confirmed Free Plan league list.
- It is a regular league rather than a play-off competition.
- The trial needs only one stable league, one team and one season.
- Scotland Premiership remains a fallback if the Denmark scope cannot be resolved.
- No Sportmonks provider approval is implied.

## Candidate Field Fit

| Market Context Need | Sportmonks Fit To Check | Status |
|---|---|---|
| Player identity | Player IDs, names and team or squad relationship. | to verify |
| Team/competition context | Team, league, season and competition metadata. | to verify |
| Dates/season context | Season dates, squad dates or metadata timestamps if available. | to verify |
| Contract context | Availability depends on plan and data coverage. | to verify |
| Market value context | Availability depends on plan and data coverage. | to verify |
| Position metadata | Player position or role fields if available. | to verify |
| Provenance/freshness | Source timestamps or update metadata if available. | to verify |

## Local Trial Boundaries

- Trial must be minimal and manually reviewed.
- Trial must use ignored local paths only.
- Trial must not write to SQLite.
- Trial must not activate Streamlit.
- Trial must not create tracked examples from raw data.
- Trial must not commit payloads, provider cache or `.local.csv` outputs.
- Trial must not expose raw Sportmonks data in docs or demos.
- Trial must stop immediately if data appears in Git status.
- Trial must stop if the selected plan or competition scope does not clearly support the intended fields.
- Trial must stop if Terms of Service or subscription conditions conflict with the intended handling.

## Credential Setup Verification

- [x] Review the [Sportmonks Secure Credential Setup](../provider_candidates/sportmonks_secure_credential_setup.md).
- [x] Local credential setup verified outside Git in the [verification record](../provider_candidates/sportmonks_local_credential_setup_verification.md).

- Selected plan documented.
- Competition scope documented.
- Credential storage path defined and ignored.
- `.env` or local configuration confirmed not tracked.
- User explicitly confirms credential creation outside Git.
- `git status --short` clean before credential creation.
- No credentials appear in `git diff`, tracked files or docs.
- No additional API calls without a new explicit decision.

## Required Before Payload Inspection

- Checklist reviewed and completed enough for trial.
- This decision record reviewed.
- Endpoint scope documented.
- Field scope documented.
- Minimal sample size documented.
- Ignored raw payload path documented.
- Ignored cache path documented.
- Cleanup process documented.
- Stop conditions reviewed.
- No SQLite, app or parser work planned.

## Decision Options After Trial

| Outcome | Meaning | Follow-up |
|---|---|---|
| `accept_for_local_transform_design` | Payload shape is suitable enough to plan a transform design. | Create a docs-only design plan; implementation requires a separate decision. |
| `defer` | Payload, plan or field coverage remains unclear. | Record blockers and avoid implementation. |
| `reject` | Payload, plan, coverage or restrictions do not fit project needs. | Close the Sportmonks candidate path or revisit alternatives. |
| `stop` | A safety issue occurred. | Remove local data, document the issue and do not proceed. |

## Current Decision

- Current decision: `local-preview-completed`
- Transform design decision: `transform-design-plan-created-docs-only`
- Implementation plan decision: `implementation-plan-created-docs-only`
- First code implementation decision: `approved-local-only-strict-scope`
- Meaning:
  - the checklist and decision records exist;
  - local credential setup remains outside Git;
  - minimal ID discovery and confirmed ID scope review passed;
  - minimal payload field review passed using existing ignored cache with 0 API calls;
  - the transform design plan is created as documentation only;
  - the implementation plan is created as documentation only;
  - the first code implementation is approved only for the listed local-only files;
  - one approved local preview is completed with non-sensitive aggregate output only;
  - broad payload inspection remains no; and
  - Sportmonks provider approval remains no.
- Next allowed step:
  - make a docs-only preview result decision or close the v0.8.0 milestone.

- Still forbidden:
  - credential exposure or commitment;
  - broad payload inspection;
  - manual raw JSON review;
  - additional cache reading;
  - `.local.csv` outputs;
  - code outside the approved first implementation file scope;
  - local trial;
  - API calls;
  - SQLite writes;
  - Streamlit activation;
  - provider approval.

## Safety Checklist

- [x] Non-sensitive response summary exists.
- [x] Stage 1 gate is `continue`.
- [x] Provider payload checklist exists.
- [x] Payload decision record created as draft/pre-trial.
- [x] No raw provider correspondence committed.
- [x] No ticket identifiers committed.
- [x] No payloads committed.
- [x] No credentials committed.
- [x] No provider cache committed.
- [x] No `.local.csv` provider outputs committed.
- [x] No SQLite writes performed.
- [x] No Streamlit activation performed.
- [x] No parser/transform code created.
- [x] Selected plan documented.
- [x] Competition scope documented.
- [x] Endpoint access and minimal field scope reviewed.
- [x] Confirmed ID scope review passed.
- [x] Minimal payload field review passed with 0 API calls.
- [x] Field scope documented in the minimal payload field review summary.
- [x] Ignored ID discovery path documented; future trial paths remain pending.
- [ ] Cleanup process documented.
- [ ] Final `git status --short` clean.

## Next Required Action

Minimal ID discovery, the [confirmed ID scope review](../provider_candidates/sportmonks_confirmed_id_scope_review.md) and the [minimal payload field review](../provider_candidates/sportmonks_minimal_payload_field_review_summary.md) have passed.

The [local preview summary](../provider_candidates/sportmonks_local_preview_run_summary.md) records the completed aggregate preview. The next allowed step is a docs-only preview result decision or v0.8.0 closeout. API calls, manual raw JSON review, additional cache reading, broad payload inspection, `.local.csv`, local trial, SQLite, Streamlit and provider approval remain forbidden.
