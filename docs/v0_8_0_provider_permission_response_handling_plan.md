# v0.8.0 Provider Permission Response Handling Plan

## Objective

v0.8.0 defines how to handle a real provider response or applicable license or subscription terms. It does not assume that a response has been received, approve Sportmonks, or authorize payload inspection, credentials, caching, derived outputs or integration.

The milestone prepares a controlled process for moving the gate to `continue`, `defer` or `reject` based only on explicit evidence.

## Starting Point

v0.7.0 was published as a documentation and governance milestone. Sportmonks has:

- a Stage 0 intake pack;
- a Stage 1 license and terms gate;
- partial public-source review notes; and
- a permission request sent log; a [ticket acknowledgement log](provider_candidates/sportmonks_ticket_acknowledgement_log.md) exists, but the substantive permission response is still pending.

The current gate decision is `defer`. The external dependency is applicable license or subscription terms, or explicit written permission.

## Scope

In scope:

- Record non-sensitive provider response summaries.
- Record explicit permissions and explicit restrictions.
- Update the Sportmonks gate decision only if evidence supports it.
- Prepare a checklist only if the gate moves to `continue`.
- Prepare a payload-specific decision record only if a concrete permitted payload exists.
- Keep confidential terms and raw responses out of Git.

Out of scope:

- Payload inspection before the gate moves to `continue`.
- Credential creation before the gate moves to `continue`.
- API calls.
- Scraping.
- Provider caching.
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
9. If a concrete permitted payload exists, prepare a payload-specific decision record.
10. Keep all raw or confidential materials outside Git.

## Response Summary Document

A future response may be summarized in:

`docs/provider_candidates/sportmonks_permission_response_summary.md`

Create this file only when a real response or applicable reviewed terms exist. It must contain only a non-sensitive summary and must not include confidential text, payloads or credentials.

## Gate Decision Rules

- **continue:** only when local evaluation, payload inspection and required handling permissions are explicit enough. This does not approve the provider; it permits only the next governance step, the checklist and decision record.
- **defer:** when permissions remain unclear or incomplete.
- **reject:** when terms block the intended use.
- **stop:** when restricted data, credentials or payloads were accessed improperly.

## Required Evidence Before Continue

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
- Do not inspect payloads until the gate moves to `continue`.
- Do not create credentials until the gate permits it.
- Do not add parser or transform code until a later explicit decision.

## Acceptance Criteria

- [ ] v0.8.0 plan exists.
- [ ] README current milestone points to v0.8.0.
- [ ] ROADMAP marks v0.7.0 as completed and published.
- [ ] ROADMAP identifies v0.8.0 as the current milestone.
- [ ] No provider response is invented.
- [ ] No provider approval is claimed.
- [ ] No payload inspection is authorized.
- [ ] No code is changed.
- [ ] No data files are generated.
- [ ] `git diff --check` passes.
- [ ] Final `git status --short` is clean before commit.

## Next Steps

1. Wait for the substantive response or follow up outside the repository if needed.
2. If a substantive response arrives, create a non-sensitive response summary.
3. Update the gate decision only from explicit evidence.
4. If the gate moves to `continue`, prepare the checklist.
5. If the gate remains `defer`, keep the blocker documented.
6. If the gate moves to `reject`, close the candidate path.
7. Continue to keep all payloads, credentials and confidential material outside Git.
