# Sportmonks Public Terms Review Notes

## Status

- Candidate: Sportmonks
- Related gate: [Sportmonks License And Terms Gate](sportmonks_license_terms_gate.md)
- Review type: public-source initial review
- Review date: 2026-07-16
- Reviewer:
- Gate impact: defer
- Payload inspection: not allowed
- Credentials setup: not allowed
- Local trial: not allowed
- Decision record: not created
- Notes: This document records non-sensitive public-source review notes only. It does not approve Sportmonks, authorize payload inspection or replace a payload decision record.

## Purpose

This document records an initial, non-sensitive review of the official public references supplied for this block. It separates technical documentation from legal permission, identifies remaining unknowns and keeps payload inspection, credentials, local caching and derived outputs blocked until the gate explicitly passes.

## Reviewed Public Sources

| Source | Source Type | Reference | Review Date | Non-sensitive Summary | Gate Relevance | Remaining Questions |
|---|---|---|---|---|---|---|
| Sportmonks Terms of Service | Public terms page | https://www.sportmonks.com/terms-of-service/ | 2026-07-16 | A public Terms of Service page exists and covers the Sportmonks service and subscription context. This review did not identify enough project-specific permission to approve payload inspection, local caching, derived outputs or redistribution. | Required legal reference, but not sufficient by itself for this project decision. | Local development; payload inspection; caching; derived outputs; retention; redistribution; subscription-specific scope. |
| Sportmonks Football API 3.0 docs page | Public technical documentation page | https://www.sportmonks.com/football-api-3-0-docs/ | 2026-07-16 | The public page points to technical API documentation, including endpoints, authentication, rate limits and related areas. It is useful for later field review only if the license gate permits inspection. | Technical reference, not a permission grant. | Current plan or license compatibility; permitted endpoints; Market Context fields; payload inspection permission. |
| Sportmonks FAQ | Public FAQ | https://www.sportmonks.com/faq/ | 2026-07-16 | The FAQ references commercial usage in relation to compliance with Terms of Service and licensing agreements. Compatibility cannot be assumed without reviewing the applicable terms or license. | Supports keeping the gate decision as defer. | Applicable license; project-use compatibility; redistribution restrictions. |
| Sportmonks Caching glossary | Public glossary and technical content | https://www.sportmonks.com/glossary/caching/ | 2026-07-16 | Public content explains caching as a technical concept. It is not contractual permission for this project. | Technical background only. | Whether local caching of actual provider payloads is permitted under applicable terms. |
| Sportmonks caching and optimisation blog | Public technical and blog content | https://www.sportmonks.com/blogs/caching-and-optimisation-strategies-for-high-volume-football-api-usage/ | 2026-07-16 | The public article discusses caching and optimisation strategies for API usage. It is not sufficient to approve local cache storage for this project. | Technical background only. | Cache retention; allowed storage; derived local outputs; whether terms or subscription rules supersede blog guidance. |
| Sportmonks API Authentication and Authorisation | Public technical and authentication content | https://www.sportmonks.com/glossary/api-authentication-and-authorisation/ | 2026-07-16 | Public content describes token and authentication concepts plus plan or subscription-based access. No credentials were created or used. | Supports keeping credentials blocked until terms and license review is complete. | Account and API key restrictions; credential storage; plan scope; permitted endpoints. |

## Public Review Findings

- Current public references identify sources for Stage 1 evidence.
- They are not sufficient to approve payload inspection.
- They are not sufficient to approve local caching.
- They are not sufficient to approve derived Market Context outputs.
- They are not sufficient to approve redistribution, screenshots or demos.
- Technical docs, blog posts and glossary pages are not license grants.
- Applicable license or subscription terms, or explicit permission, are still required.

## Gate Decision

- Decision: defer
- Reason:
  - Applicable project-specific terms or license are not confirmed.
  - Payload inspection permission remains unknown.
  - Local caching permission remains unknown.
  - Derived-output permission remains unknown.
  - Redistribution and demo restrictions remain unknown.
  - Subscription-specific scope remains unknown.
- Payload inspection: not allowed
- Credential setup: not allowed
- Local trial: not allowed
- Decision record: not created

## Missing Evidence

- Applicable license or subscription agreement.
- Explicit permission for local development or evaluation.
- Explicit permission for inspecting payloads.
- Explicit permission for local caching.
- Explicit permission for derived normalized or canonical outputs.
- Retention limits.
- Redistribution restrictions.
- Screenshot and demo restrictions.
- Attribution requirements.
- Endpoint and feature access by plan.
- Market Context field availability.
- Contact or support clarification if public documentation remains ambiguous.

## Allowed Next Actions

- Ask the user to provide permitted subscription or license terms if available.
- Review additional public documentation without copying legal text.
- Contact provider support outside the repository if clarification is needed.
- Record only non-sensitive references and summaries.
- Keep the gate decision as defer until required permissions are clear.

## Forbidden Next Actions

- Do not inspect payloads.
- Do not create provider credentials.
- Do not call Sportmonks APIs.
- Do not scrape.
- Do not cache provider data.
- Do not create `.local.csv` outputs from provider data.
- Do not write to SQLite.
- Do not activate provider data in the app.
- Do not create parser or transform code for real provider payloads.
- Do not commit raw terms, restricted content, credentials, payloads or dumps.
