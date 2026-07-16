# Sportmonks Permission Request Draft

## Status

- Candidate: Sportmonks
- Related gate: [Sportmonks License And Terms Gate](sportmonks_license_terms_gate.md)
- Related public review notes: [Sportmonks Public Terms Review Notes](sportmonks_public_terms_review_notes.md)
- Purpose: permission clarification draft
- Draft status: not sent
- Gate impact: none until response is reviewed
- Payload inspection: not allowed
- Credentials setup: not allowed
- Local trial: not allowed
- Decision record: not created
- Notes: This draft does not approve Sportmonks, does not authorize payload inspection and does not replace license review.

## Purpose

This document prepares a message requesting clarification from Sportmonks before any use of real provider data. It contains no provider response and grants no permission. Any response must be reviewed and summarized in a non-sensitive form before the gate decision can change.

## Draft Email

**Subject:** Permission clarification for local evaluation and derived football data outputs

Hello Sportmonks team,

We are evaluating whether Sportmonks could be a suitable data provider for a football scouting dashboard project.

The project is currently in a pre-integration review phase. No payloads have been inspected, no credentials have been created, and no provider data has been cached or integrated.

If permitted under the applicable terms and license, our intended evaluation would be limited to:

- evaluating football player identity fields;
- evaluating possible player metadata or Market Context fields;
- running a small local and offline trial;
- producing normalized or canonical derived outputs for internal review; and
- keeping raw payloads out of public repositories.

Before proceeding, could you please clarify the following?

1. Which terms, subscription plan or license would govern this intended evaluation?
2. Is local development or evaluation permitted before production integration?
3. Are we allowed to inspect small sample payloads for schema and field assessment?
4. Are we allowed to cache payloads locally for development or debugging? If yes, are there retention limits?
5. Are we allowed to create normalized or canonical derived outputs for internal review?
6. Are derived outputs allowed to include player identifiers, team identifiers, market or context metadata, source references and confidence notes?
7. Are screenshots or demo materials allowed if they do not expose raw restricted payloads?
8. Are there restrictions on redistributing derived data, including internally or in documentation?
9. Are there attribution requirements?
10. Are there endpoint, feature or field restrictions by plan that would affect player identity, squads, contracts, market values, dates or metadata?
11. Are there restrictions on API key storage, local environment files or developer access?
12. Who should we contact for written permission or a suitable evaluation license?

We will not inspect payloads, create credentials or cache data until we have confirmed the applicable permissions.

Thanks for clarifying the appropriate license path.

Kind regards,

[Name / project contact]

## Questions Checklist

- [ ] Applicable terms/license/plan
- [ ] Local development permission
- [ ] Sample payload inspection
- [ ] Local caching and retention
- [ ] Derived outputs
- [ ] Allowed derived fields
- [ ] Screenshots/demo
- [ ] Redistribution limits
- [ ] Attribution
- [ ] Endpoint/field restrictions
- [ ] Credential/API key restrictions
- [ ] Contact for written permission/evaluation license

## How To Record A Response

Do not paste restricted legal text into the repository. Record only:

- response date;
- sender or contact role, if shareable;
- non-sensitive summary;
- explicit permissions;
- explicit restrictions;
- unresolved questions; and
- whether written permission exists.

If the response contains confidential terms, keep it outside Git.

## Response Summary Template

```text
Response date:
Responder / source:
Can reference in repo: yes / no
Applicable terms/license:
Local development: yes / no / unknown
Payload inspection: yes / no / unknown
Local caching: yes / no / unknown
Retention limits:
Derived outputs: yes / no / unknown
Redistribution/screenshots/demo:
Credential restrictions:
Attribution:
Endpoint/field restrictions:
Written permission attached or available: yes / no
Gate recommendation: continue / defer / reject
Open questions:
```

## Gate Impact Rules

- A reply does not automatically approve Sportmonks.
- The gate can move to `continue` only if required permissions are explicit enough.
- If permissions remain unclear, the gate stays `defer`.
- If terms block the intended use, the gate becomes `reject`.
- Payload inspection remains forbidden until the gate explicitly moves to `continue`.

## Forbidden Actions

- Do not inspect payloads.
- Do not create credentials.
- Do not call Sportmonks APIs.
- Do not scrape.
- Do not cache provider data.
- Do not create `.local.csv` outputs from provider data.
- Do not write to SQLite.
- Do not activate provider data in the app.
- Do not create parser or transform code for real provider payloads.
- Do not commit raw legal terms, confidential replies, credentials, payloads or dumps.
