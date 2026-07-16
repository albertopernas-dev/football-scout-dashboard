# Sportmonks License And Terms Gate

## Status

- Candidate: Sportmonks
- Related intake pack: [Sportmonks Candidate Review Pack](sportmonks_candidate_review_pack.md)
- Review stage: Stage 1 - License And Terms Gate
- Gate status: not reviewed
- Gate decision: defer
- Payload inspection: not allowed
- Credentials setup: not allowed
- Local trial: not allowed
- Decision record: not created
- Reviewer:
- Date:
- Notes: This gate document is a review scaffold only. It does not approve Sportmonks, authorize payload inspection or replace a payload decision record.

## Purpose

This document prepares the Stage 1 review for Sportmonks. It contains no current legal review, asserts no permissions and accepts no terms. It does not authorize downloading, caching, transformation, redistribution, screenshots or demos, credential setup or integration.

The default decision is `defer` until current public sources or permitted user-provided terms are reviewed.

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
| Terms source | What terms govern the intended use? | not reviewed | pending | unknown |
| License source | What license or subscription applies? | not reviewed | pending | unknown |
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

- Terms reviewed: no
- License source: pending
- Local development permitted: unknown
- Payload inspection permitted: unknown
- Caching permitted: unknown
- Derived outputs permitted: unknown
- Screenshots/demo permitted: unknown
- Redistribution permitted: unknown
- Retention limits: unknown
- Attribution requirements: unknown
- Credential restrictions: unknown
- Blocking restrictions: unknown
- Gate decision: defer
- Reason: current terms and permissions have not been reviewed

## Allowed Actions Before Gate Completion

- Maintain documentation scaffolds.
- Record non-sensitive references to terms once reviewed.
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

## Evidence Log Template

| Evidence Item | Source Type | Reference | Review Date | Reviewer | Non-sensitive Summary | Open Questions |
|---|---|---|---|---|---|---|
| Terms reference | pending | pending | pending | pending | pending | pending |
| License/subscription reference | pending | pending | pending | pending | pending | pending |
| API/data usage reference | pending | pending | pending | pending | pending | pending |

## Gate Decision Options

- **continue:** only when required permissions are clear enough to prepare the checklist and decision record.
- **defer:** when permissions are unclear or information is missing.
- **reject:** when terms clearly block the intended use.
- **stop:** when restricted data, credentials or payloads were accessed improperly.

## Current Decision

- Decision: defer
- Rationale:
  - No current terms reviewed.
  - No current license reviewed.
  - Payload inspection permission unknown.
  - Cache permission unknown.
  - Derived-output permission unknown.
- Next allowed step: perform a terms and license review from public documentation or user-provided permitted terms
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

The next block must review current public documentation or user-provided permitted terms. It must record only non-sensitive summaries and references. It must not inspect payloads or create credentials unless the completed gate explicitly allows it.
