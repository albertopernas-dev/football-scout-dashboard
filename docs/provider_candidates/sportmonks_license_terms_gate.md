# Sportmonks License And Terms Gate

## Status

- Candidate: Sportmonks
- Related intake pack: [Sportmonks Candidate Review Pack](sportmonks_candidate_review_pack.md)
- Review stage: Stage 1 - License And Terms Gate
- Public review notes: [Sportmonks Public Terms Review Notes](sportmonks_public_terms_review_notes.md)
- Permission request sent log: [Sportmonks Permission Request Sent Log](sportmonks_permission_request_sent_log.md)
- Gate status: partial public-source review
- Gate decision: defer
- Payload inspection: not allowed
- Credentials setup: not allowed
- Local trial: not allowed
- Decision record: not created
- Reviewer:
- Date:
- Notes: This gate document is a review scaffold only. It does not approve Sportmonks, authorize payload inspection or replace a payload decision record.

## Purpose

This document records a partial public-source review for Sportmonks. It asserts no project-specific permissions and accepts no terms. It does not authorize downloading, caching, transformation, redistribution, screenshots or demos, credential setup or integration.

The decision remains `defer` until applicable license or subscription terms, or explicit permission, establish the required project permissions.

## Review Inputs Required

- Current public terms or user-provided permitted terms.
- Current license or subscription terms, if applicable.
- Current API or data-usage documentation, if applicable.
- Any explicit permission for local development.
- Any explicit permission for payload inspection.
- Any explicit permission for local caching.
- Any explicit permission for derived outputs.
- Any restrictions on redistribution, screenshots, demos or sharing.
- Credential and account restrictions.
- Source and date of each reviewed item.

Do not copy restricted legal text into this repository. Record short references, dates and non-sensitive summaries only.

## Gate Questions

| Area | Question | Current Answer | Evidence Reference | Status |
|---|---|---|---|---|
| Terms source | What terms govern the intended use? | partial public-source review | [Public review notes](sportmonks_public_terms_review_notes.md) | partial |
| License source | What license or subscription applies? | not reviewed | [Public review notes](sportmonks_public_terms_review_notes.md) | unknown |
| Local development | Is local development or evaluation permitted? | unknown | pending | unknown |
| Payload inspection | Is payload inspection permitted before integration? | unknown | pending | unknown |
| Local caching | Is local caching permitted? | unknown | pending | unknown |
| Derived outputs | Are normalized or canonical derived outputs permitted? | unknown | pending | unknown |
| Redistribution | Can raw or derived data be shared? | unknown | pending | unknown |
| Screenshots/demo | Are screenshots or demos permitted? | unknown | pending | unknown |
| Credentials | Are there restrictions on account or API key handling? | unknown | pending | unknown |
| Retention | Are there limits on data retention? | unknown | pending | unknown |
| Attribution | Is attribution required? | unknown | pending | unknown |
| Commercial/internal use | Is the intended project use compatible? | unknown | pending | unknown |

## Current Gate Assessment

- Terms reviewed: partial public-source review
- License source: pending; subscription-specific license not reviewed
- Local development permitted: unknown
- Payload inspection permitted: unknown
- Caching permitted: unknown
- Derived outputs permitted: unknown
- Screenshots/demo permitted: unknown
- Redistribution permitted: unknown
- Retention limits: unknown
- Attribution requirements: unknown
- Credential restrictions: partially informed by public authentication documentation; project-specific restrictions unknown
- Blocking restrictions: unknown
- Gate decision: defer
- Reason: public sources were reviewed, but required project permissions remain unknown

## Allowed Actions Before Gate Completion

- Maintain documentation scaffolds.
- Record non-sensitive references to terms once reviewed.
- The [Sportmonks Permission Request Sent Log](sportmonks_permission_request_sent_log.md) records that the clarification request was sent; no response has been received and the gate remains `defer`.
- Keep Sportmonks in Stage 1 pending status.
- Decide to continue, defer or reject only after review inputs are available.

## Forbidden Actions Before Gate Completion

- Do not inspect payloads.
- Do not create provider credentials.
- Do not call APIs.
- Do not scrape.
- Do not cache provider data.
- Do not create `.local.csv` outputs from provider data.
- Do not write to SQLite.
- Do not activate provider data in the app.
- Do not commit raw dumps, credentials, restricted terms or provider data.
- Do not create parser or transform code for real provider payloads.

## Evidence Log

| Evidence Item | Source Type | Reference | Review Date | Reviewer | Non-sensitive Summary | Open Questions |
|---|---|---|---|---|---|---|
| Sportmonks Terms of Service | Public terms page | https://www.sportmonks.com/terms-of-service/ | 2026-07-16 | pending | Public terms reference identified; project-specific permissions remain unconfirmed. | Local development, payload inspection, caching, derived outputs, retention and redistribution. |
| Sportmonks Football API 3.0 docs | Public technical documentation | https://www.sportmonks.com/football-api-3-0-docs/ | 2026-07-16 | pending | Technical documentation reference only; not a permission grant. | Permitted endpoints, field availability, payload inspection and plan scope. |
| Sportmonks FAQ | Public FAQ | https://www.sportmonks.com/faq/ | 2026-07-16 | pending | Indicates that applicable terms and licensing agreements remain relevant. | Applicable license, project-use compatibility and redistribution. |
| Sportmonks Caching glossary | Public technical content | https://www.sportmonks.com/glossary/caching/ | 2026-07-16 | pending | Technical caching background only. | Contractual permission for local caching. |
| Sportmonks caching and optimisation blog | Public technical and blog content | https://www.sportmonks.com/blogs/caching-and-optimisation-strategies-for-high-volume-football-api-usage/ | 2026-07-16 | pending | Technical strategy reference only; does not approve storage. | Retention, allowed storage and derived outputs. |
| Sportmonks API Authentication and Authorisation | Public technical and authentication content | https://www.sportmonks.com/glossary/api-authentication-and-authorisation/ | 2026-07-16 | pending | Authentication and access background; no credentials created. | Account restrictions, credential storage, plan scope and permitted endpoints. |

## Gate Decision Options

- **continue:** only when required permissions are clear enough to prepare the checklist and decision record.
- **defer:** when permissions are unclear or information is missing.
- **reject:** when terms clearly block the intended use.
- **stop:** when restricted data, credentials or payloads were accessed improperly.

## Current Decision

- Decision: defer
- Rationale:
  - Public sources were reviewed but are insufficient for project-specific permission.
  - No applicable license or subscription terms reviewed.
  - Payload inspection permission unknown.
  - Cache permission unknown.
  - Derived-output permission unknown.
- Next allowed step: obtain and review applicable license or subscription terms, or explicit permission
- Next forbidden step: payload inspection or credential setup

## Impact On Sportmonks Candidate Review Pack

- The related Sportmonks candidate review pack remains Stage 0 / Stage 1 pending.
- Local Trial Plan remains blocked.
- Checklist and decision record remain not created.
- No final outcome is recorded.

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
- [x] No current legal terms copied into git.
- [ ] Final `git status --short` is clean.

## Stop Conditions

- Terms cannot be found or verified.
- Terms are ambiguous for local development.
- Payload inspection permission is absent or unclear.
- Caching permission is absent or unclear.
- Derived-output permission is absent or unclear.
- Redistribution restrictions conflict with intended documentation or demo needs.
- Credentials would be required before terms are reviewed.
- Restricted data appears in git status.

## Next Required Action

The permission request has been sent, but no response has been received. The gate remains `defer`. The next action is to wait for a response or follow up outside the repository if needed, recording only non-sensitive summaries and references. Payload inspection and credential setup remain forbidden unless the completed gate explicitly allows them.
