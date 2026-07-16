# Sportmonks Payload Decision Record

## Status

- Candidate: Sportmonks
- Decision record status: draft/pre-trial
- Related gate: [Sportmonks License And Terms Gate](../provider_candidates/sportmonks_license_terms_gate.md)
- Related response summary: [Sportmonks Permission Response Summary](../provider_candidates/sportmonks_permission_response_summary.md)
- Related checklist: [Sportmonks Provider Payload Checklist](../provider_candidates/sportmonks_provider_payload_checklist.md)
- Related trial scope plan: [Sportmonks Ignored Local Trial Scope Plan](../provider_candidates/sportmonks_ignored_local_trial_scope_plan.md)
- Stage 1 gate decision: `continue`
- Provider approval: no
- Production approval: no
- Payload inspection performed: no
- Credentials created: no
- API calls performed: no
- Provider cache created: no
- Local trial performed: no
- SQLite writes performed: no
- Streamlit activation performed: no
- Parser/transform code created: no
- Notes: This record defines decision boundaries before a possible minimal local trial. It does not approve Sportmonks as a provider or authorize production use.

## Purpose

This decision record defines the required scope and constraints before any Sportmonks payload inspection or local trial. It converts the Stage 1 `continue` gate into a controlled pre-trial decision framework.

It does not inspect payloads, select a final provider, create credentials or start integration. All raw provider data and credentials must remain outside Git.

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
| Credentials | May be prepared later. | allowed with conditions | Only in ignored local environment or configuration after user confirmation. |
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
| Selected competition(s) | One league included in the Free Plan; Danish Superliga preferred if available. | pending exact league confirmation |
| Selected season | Latest available season for the selected free-plan league. | pending confirmation |
| Selected team | One team from the selected free-plan league; FC Copenhagen preferred only if Danish Superliga is available. | proposed/pending confirmation |
| Endpoint(s) | Proposed Team Squad by Team and Season ID; Players endpoint only if needed for schema/include validation. | proposed/pending documentation and account confirmation |
| Field categories | Must be mapped to Market Context needs. | pending |
| Sample size | One team, one season, minimal payload. | proposed; not executed |
| Raw payload path | Must be an ignored local path. | proposed in trial scope plan; not created |
| Cache path | Must be an ignored local path. | proposed in trial scope plan; not created |
| Retention/cleanup | Must be documented before trial. | pending |
| Credential storage | Must use ignored local environment or configuration. | proposed in trial scope plan; not created |
| Expected derived output | Must avoid raw data exposure. | pending |
| Stop conditions | Must be reviewed before trial. | pending |

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

## Required Before Credentials

- Selected plan documented.
- Competition scope documented.
- Credential storage path defined and ignored.
- `.env` or local configuration confirmed not tracked.
- User explicitly confirms credential creation outside Git.
- `git status --short` clean before credential creation.
- No credentials appear in `git diff`, tracked files or docs.

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
| `accept_for_local_transform_design` | Payload shape is suitable enough to design local transform code later. | Create an explicit implementation plan. |
| `defer` | Payload, plan or field coverage remains unclear. | Record blockers and avoid implementation. |
| `reject` | Payload, plan, coverage or restrictions do not fit project needs. | Close the Sportmonks candidate path or revisit alternatives. |
| `stop` | A safety issue occurred. | Remove local data, document the issue and do not proceed. |

## Current Decision

- Current decision: `prepare_trial_only`
- Meaning:
  - the checklist exists;
  - this decision record exists;
  - a local trial may be planned; and
  - credentials and payload inspection have not been performed.
- Next allowed step:
  - confirm the exact Free Plan league list;
  - confirm the selected league;
  - confirm the selected season;
  - confirm the selected team; and
  - confirm endpoint availability.
- Still forbidden:
  - credentials;
  - payload inspection;
  - API calls;
  - SQLite writes;
  - Streamlit activation; and
  - parser or transform code.

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
- [ ] Selected plan documented.
- [ ] Competition scope documented.
- [ ] Endpoint scope documented.
- [ ] Field scope documented.
- [ ] Ignored local paths documented.
- [ ] Cleanup process documented.
- [ ] Final `git status --short` clean.

## Next Required Action

Review the [ignored local trial scope plan](../provider_candidates/sportmonks_ignored_local_trial_scope_plan.md), then complete the checklist and this decision record after the user confirms the exact Free Plan league list, selected league, latest available season, selected team and endpoint access.

Do not create credentials, call APIs or inspect payloads until those details are documented and reviewed. After that review, a separate explicit block may prepare the ignored local trial setup.
