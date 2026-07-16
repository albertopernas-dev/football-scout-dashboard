# v0.8.0 Provider Permission Response Handling Plan

## Objective

v0.8.0 defines how to handle a real provider response or applicable license or subscription terms. A substantive Sportmonks response has now been recorded only as a non-sensitive summary. This does not approve Sportmonks or authorize skipping the checklist and payload-specific decision record.

The recorded evidence supports moving the Stage 1 gate to `continue` for the next governance step only. No payload has been inspected, no credentials have been created and no integration has started.

## Starting Point

v0.7.0 was published as a documentation and governance milestone. Sportmonks has:

- a Stage 0 intake pack;
- a Stage 1 license and terms gate;
- partial public-source review notes; and
- a permission request sent log; a [ticket acknowledgement log](provider_candidates/sportmonks_ticket_acknowledgement_log.md); and a [non-sensitive substantive response summary](provider_candidates/sportmonks_permission_response_summary.md).

The current gate decision is `continue`. This permits preparation of the checklist, payload-specific decision record and ignored local trial plan; it does not approve the provider or permit bypassing those controls.

## Scope

In scope:

- Record non-sensitive provider response summaries.
- Record explicit permissions and explicit restrictions.
- Update the Sportmonks gate decision only if evidence supports it.
- Prepare a checklist only if the gate moves to `continue`.
- Prepare and review a payload-specific decision record before any concrete permitted payload is inspected.
- Keep confidential terms and raw responses out of Git.

Out of scope:

- Payload inspection before the checklist and payload-specific decision record are prepared.
- Credential creation before the checklist and payload-specific decision record are prepared.
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
- Do not create credentials until the checklist and payload-specific decision record are prepared and secure local handling is confirmed.
- Do not add parser or transform code until a later explicit decision.

## Acceptance Criteria

- [ ] v0.8.0 plan exists.
- [ ] README current milestone points to v0.8.0.
- [ ] ROADMAP marks v0.7.0 as completed and published.
- [ ] ROADMAP identifies v0.8.0 as the current milestone.
- [ ] No provider response is invented.
- [ ] No provider approval is claimed.
- [ ] No payload inspection has been performed.
- [ ] No code is changed.
- [ ] No data files are generated.
- [ ] `git diff --check` passes.
- [ ] Final `git status --short` is clean before commit.

## Next Steps

1. The [Sportmonks Provider Payload Checklist](provider_candidates/sportmonks_provider_payload_checklist.md) exists as draft/pre-trial.
2. The [Sportmonks Payload Decision Record](provider_decisions/sportmonks_payload_decision_record.md) exists as draft/pre-trial.
3. The [Sportmonks Ignored Local Trial Scope Plan](provider_candidates/sportmonks_ignored_local_trial_scope_plan.md) exists as draft/pre-credential.
4. The Football Free Plan is confirmed by user screenshot, which shows 4 leagues and 3000 API calls.
5. Confirm the exact included league, selected season, selected team and endpoint access.
6. After those details are documented and reviewed, a separate explicit block may prepare secure local credential setup.
7. Do not create credentials, inspect payloads, perform the trial or call APIs in this block.
8. Keep raw payloads, provider cache, `.local.csv` outputs, credentials and confidential correspondence outside Git.
9. Continue to treat Sportmonks as unapproved until a later explicit decision.
