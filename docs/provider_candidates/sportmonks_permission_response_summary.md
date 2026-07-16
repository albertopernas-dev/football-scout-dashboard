# Sportmonks Permission Response Summary

## Status

- Candidate: Sportmonks
- Related gate: [Sportmonks License And Terms Gate](sportmonks_license_terms_gate.md)
- Related sent log: [Sportmonks Permission Request Sent Log](sportmonks_permission_request_sent_log.md)
- Related acknowledgement log: [Sportmonks Ticket Acknowledgement Log](sportmonks_ticket_acknowledgement_log.md)
- Response status: substantive response received
- Ticket status: closed outside repository
- Response date: 2026-07-16
- Raw response stored in Git: no
- Exact ticket reference stored in Git: no
- Gate recommendation: `continue`
- Gate impact: Stage 1 can move from `defer` to `continue`
- Provider approval: no
- Payload inspection performed: no
- Credentials created: no
- Local trial performed: no
- Decision record created: no
- Notes: This file records only a non-sensitive summary. It does not include full provider correspondence, ticket identifiers, credentials, payloads or legal text.

## Non-sensitive Response Summary

- Sportmonks support responded to the permission clarification request.
- Local development and evaluation are permitted using an available plan before production integration.
- Inspecting API responses or payloads for schema, field and suitability assessment is permitted.
- Local caching for development and debugging is permitted while the subscription remains active and the Terms of Service are followed.
- Normalized datasets, canonical derived outputs and internal analytical artifacts are permitted.
- Internal documentation and demos using derived outputs are permitted if they do not expose or redistribute raw Sportmonks data.
- Attribution is not mandatory, though acknowledgement is appreciated.
- Available data depends on the subscription and selected competitions.
- Secure local API key storage in environment variables or configuration files is acceptable if the key is not exposed publicly or committed to source control.
- Standard plans are intended for evaluation and development; no separate evaluation license is required.
- Complete licensing details remain governed by the Sportmonks Terms of Service.

## Explicit Permissions Recorded

| Area | Summary | Status |
|---|---|---|
| Local development/evaluation | Permitted using an available plan before production integration. | permitted |
| Payload/schema inspection | API responses may be inspected for schema, fields and suitability. | permitted |
| Local caching | Permitted for development/debugging while subscription is active and Terms of Service are followed. | permitted with conditions |
| Derived outputs | Normalized/canonical datasets and internal analytical artifacts are permitted. | permitted |
| Internal docs/demos | Permitted for derived outputs if raw Sportmonks data is not exposed or redistributed. | permitted with conditions |
| Attribution | Not mandatory; acknowledgement appreciated. | optional |
| API key storage | Secure local environment/configuration storage permitted if not exposed or committed. | permitted with conditions |
| Plan/field scope | Data availability depends on subscription and selected competitions. | plan-dependent |
| Evaluation license | Standard plans are intended for evaluation/development; no separate evaluation license required. | no separate evaluation license indicated |

## Conditions And Restrictions

- Must comply with the Sportmonks Terms of Service.
- Subscription must remain active for local caching.
- Raw Sportmonks data must not be exposed or redistributed.
- API keys must not be exposed publicly or committed to source control.
- Available fields and endpoints depend on the selected plan and competitions.
- Raw correspondence, ticket identifiers and any restricted terms remain outside Git.

## Gate Decision

- Previous decision: `defer`
- New decision: `continue`
- Reason:
  - Sportmonks provided explicit permission for local evaluation.
  - Sportmonks allowed payload and schema inspection.
  - Sportmonks allowed local caching for development and debugging under an active subscription and Terms of Service compliance.
  - Sportmonks allowed normalized or canonical internal derived outputs.
  - Sportmonks allowed internal documentation and demos using derived outputs if raw data is not exposed or redistributed.
- Scope of `continue`:
  - may prepare the provider payload checklist;
  - may prepare a payload-specific decision record; and
  - may plan a local ignored trial.
- Not included:
  - does not approve the provider for production;
  - does not allow raw data in Git;
  - does not allow credentials in Git;
  - does not skip the checklist or decision record; and
  - does not activate provider data in the app.

## Next Allowed Actions

- Prepare the provider payload checklist.
- Prepare a payload-specific decision record.
- Define an ignored local trial plan.
- Only after the checklist and decision record, create credentials securely if required and permitted.
- Only after the checklist and decision record, inspect a minimal permitted payload if needed.
- Keep all raw payloads under ignored local paths.

## Still Forbidden

- Do not commit raw payloads.
- Do not commit API keys.
- Do not commit provider cache.
- Do not commit `.local.csv` provider outputs.
- Do not expose raw Sportmonks data in documentation or demos.
- Do not activate provider data in Streamlit.
- Do not write provider data to SQLite.
- Do not create parser or transform code until a later explicit block.
- Do not treat `continue` as provider approval.
