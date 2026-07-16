# Sportmonks License And Terms Gate

## Status

- Candidate: Sportmonks
- Related intake pack: [Sportmonks Candidate Review Pack](sportmonks_candidate_review_pack.md)
- Review stage: Stage 1 - License And Terms Gate
- Public review notes: [Sportmonks Public Terms Review Notes](sportmonks_public_terms_review_notes.md)
- Permission request sent log: [Sportmonks Permission Request Sent Log](sportmonks_permission_request_sent_log.md)
- Permission response summary: [Sportmonks Permission Response Summary](sportmonks_permission_response_summary.md)
- Gate status: substantive permission response reviewed
- Gate decision: `continue`
- Detailed permission response: received
- Payload inspection: permitted for schema/field assessment after checklist and decision-record preparation
- Credentials setup: permitted only securely and after checklist and decision-record preparation
- Local trial: permitted to plan; not yet performed
- Decision record: not created
- Provider approval: no
- Review date: 2026-07-16
- Reviewer:
- Notes: `continue` permits the next governance step only. It does not approve Sportmonks, authorize production integration or replace the payload checklist and decision record.

## Purpose

This document records the Stage 1 review for Sportmonks using public references and a non-sensitive summary of the substantive permission response. The response supports moving the gate from `defer` to `continue` under explicit conditions.

The gate decision allows preparation of the provider payload checklist, payload-specific decision record and an ignored local trial plan. No payload has been inspected, no credentials have been created and no local trial has been performed.

## Reviewed Evidence

- [Sportmonks Public Terms Review Notes](sportmonks_public_terms_review_notes.md)
- [Sportmonks Permission Request Draft](sportmonks_permission_request_draft.md)
- [Sportmonks Permission Request Sent Log](sportmonks_permission_request_sent_log.md)
- [Sportmonks Ticket Acknowledgement Log](sportmonks_ticket_acknowledgement_log.md)
- [Sportmonks Permission Response Summary](sportmonks_permission_response_summary.md)

Do not copy restricted legal text, ticket identifiers or confidential correspondence into this repository. Record short references, dates and non-sensitive summaries only.

## Gate Questions

| Area | Current Answer | Evidence Reference | Status |
|---|---|---|---|
| Terms/license scope | Governed by an available plan and Sportmonks Terms of Service; selected plan scope remains plan-dependent. | [Response summary](sportmonks_permission_response_summary.md) | permitted with conditions |
| Local development | Permitted using an available plan before production integration. | [Response summary](sportmonks_permission_response_summary.md) | permitted |
| Payload inspection | Permitted for schema, field and suitability assessment after governance preparation. | [Response summary](sportmonks_permission_response_summary.md) | permitted with conditions |
| Local caching | Permitted for development/debugging while subscription is active and Terms of Service are followed. | [Response summary](sportmonks_permission_response_summary.md) | permitted with conditions |
| Derived outputs | Internal normalized/canonical datasets and analytical artifacts are permitted. | [Response summary](sportmonks_permission_response_summary.md) | permitted |
| Redistribution | Raw data must not be exposed or redistributed; internal derived use is permitted. | [Response summary](sportmonks_permission_response_summary.md) | restricted |
| Screenshots/demo | Internal derived-output documentation and demos are permitted if raw data is not exposed or redistributed. | [Response summary](sportmonks_permission_response_summary.md) | permitted with conditions |
| Credentials | Secure local environment/configuration storage is permitted; keys must never be public or committed. | [Response summary](sportmonks_permission_response_summary.md) | permitted with conditions |
| Retention | Local caching is tied to an active subscription and Terms of Service; exact plan/terms details remain applicable. | [Response summary](sportmonks_permission_response_summary.md) | conditional |
| Attribution | Not mandatory; acknowledgement is appreciated. | [Response summary](sportmonks_permission_response_summary.md) | optional |
| Endpoint/field scope | Availability depends on the subscription and selected competitions. | [Response summary](sportmonks_permission_response_summary.md) | plan-dependent |
| Production use | Not assessed or approved by this gate. | [Response summary](sportmonks_permission_response_summary.md) | out of scope |

## Current Gate Assessment

- Terms reviewed: public-source review plus non-sensitive substantive response summary
- License source: available plan and Terms of Service; exact selected plan remains pending
- Local development permitted: yes, plan-dependent
- Payload inspection permitted: yes, for schema/field/suitability assessment after checklist and decision-record preparation
- Caching permitted: yes, for development/debugging while subscription is active and Terms of Service are followed
- Derived outputs permitted: yes, for internal normalized/canonical outputs and analytical artifacts
- Screenshots/demo permitted: yes, for derived outputs if raw data is not exposed or redistributed
- Redistribution permitted: raw data no; internal derived use permitted
- Retention limits: tied to active subscription and Terms of Service; exact plan/terms details remain applicable
- Attribution requirements: optional and appreciated, not mandatory
- Credential restrictions: secure local environment/configuration storage allowed; never expose publicly or commit
- Endpoint/field scope: plan-dependent
- Gate decision: `continue`
- Reason: the substantive permission response supports moving to the next governance step under recorded conditions

## Allowed Actions After Gate Continue

- Prepare the provider payload checklist.
- Prepare a payload-specific decision record.
- Define an ignored local trial plan.
- Select the applicable plan and competitions before any trial.
- After the checklist and decision record are prepared, create credentials securely if required and permitted.
- After the checklist and decision record are prepared, inspect a minimal permitted payload if needed.
- Keep all provider payloads and caches under ignored local paths.

## Required Before Any Trial

- Complete the provider payload checklist.
- Create the payload-specific decision record.
- Record the selected plan, competition scope and applicable conditions.
- Define ignored local paths and cleanup handling.
- Confirm credentials will remain outside Git.
- Confirm raw payloads will not appear in documentation, demos or source control.

## Still Forbidden

- Do not inspect payloads before the checklist and decision record are prepared.
- Do not create credentials before the checklist and decision record are prepared.
- Do not commit raw payloads, provider cache or dumps.
- Do not commit API keys or credentials.
- Do not commit `.local.csv` provider outputs.
- Do not expose or redistribute raw Sportmonks data.
- Do not write provider data to SQLite.
- Do not activate provider data in the app.
- Do not create parser or transform code until a later explicit block.
- Do not treat `continue` as provider or production approval.

## Evidence Log

| Evidence Item | Source Type | Reference | Review Date | Non-sensitive Summary |
|---|---|---|---|---|
| Sportmonks Terms of Service | Public terms page | https://www.sportmonks.com/terms-of-service/ | 2026-07-16 | Public terms remain applicable to the permitted activities. |
| Sportmonks Football API 3.0 docs | Public technical documentation | https://www.sportmonks.com/football-api-3-0-docs/ | 2026-07-16 | Technical reference only; plan and field availability remain subscription-dependent. |
| Sportmonks FAQ | Public FAQ | https://www.sportmonks.com/faq/ | 2026-07-16 | Public reference that points usage back to applicable terms and licensing. |
| Sportmonks caching references | Public technical content | [Public review notes](sportmonks_public_terms_review_notes.md) | 2026-07-16 | Technical background; permission conditions are recorded from the substantive response. |
| Sportmonks authentication reference | Public technical content | https://www.sportmonks.com/glossary/api-authentication-and-authorisation/ | 2026-07-16 | Technical background for secure credentials; no credentials have been created. |
| Sportmonks substantive permission response | Provider support response summarized outside raw correspondence | [Response summary](sportmonks_permission_response_summary.md) | 2026-07-16 | Explicit permissions and conditions recorded without ticket identifiers or confidential text. |

## Gate Decision Options

- **continue:** required permissions are clear enough to prepare the checklist and decision record.
- **defer:** permissions are unclear or incomplete.
- **reject:** terms block the intended use.
- **stop:** restricted data, credentials or payloads were accessed improperly.

## Current Decision

- Previous decision: `defer`
- Decision: `continue`
- Rationale:
  - Local evaluation is permitted using an available plan.
  - Payload/schema inspection is permitted for assessment.
  - Local caching is permitted under an active subscription and Terms of Service compliance.
  - Internal normalized/canonical derived outputs are permitted.
  - Internal derived-output documentation and demos are permitted if raw data is not exposed or redistributed.
- Next allowed step: prepare the provider payload checklist and payload-specific decision record
- Next forbidden step: any payload inspection, credential creation or local trial before that governance preparation is complete

## Impact On Sportmonks Candidate Review Pack

- Sportmonks remains unapproved as a provider.
- The Stage 1 gate now permits the next governance step only.
- The provider payload checklist and payload-specific decision record remain not created.
- A local ignored trial may be planned but has not been performed.
- No final provider outcome is recorded.

## Safety Checklist

- [x] No real payload committed.
- [x] No raw provider dump committed.
- [x] No credentials committed.
- [x] No `.local.csv` committed.
- [x] No `data/provider_cache/` contents committed.
- [x] No app activation performed.
- [x] No SQLite writes performed.
- [x] No scraping performed.
- [x] No live provider calls performed.
- [x] No confidential response or ticket identifier copied into Git.
- [ ] Provider payload checklist prepared.
- [ ] Payload-specific decision record prepared.
- [ ] Final `git status --short` is clean.

## Stop Conditions

- The selected plan or competition scope does not cover the intended review.
- Terms or plan conditions conflict with the intended local handling.
- Raw data, credentials, confidential correspondence or ticket identifiers appear in Git.
- Checklist or decision-record preparation identifies unresolved permission risks.
- Local caching cannot comply with active-subscription or Terms of Service conditions.
- Raw data would be exposed or redistributed through documentation or demos.

## Next Required Action

Prepare the provider payload checklist and payload-specific decision record using only non-sensitive references. Define an ignored local trial plan, but do not inspect payloads, create credentials or perform the trial until those governance artifacts are prepared and reviewed.
