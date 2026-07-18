# Sportmonks Provider Payload Checklist

## Status

- Candidate: Sportmonks
- Related gate: [Sportmonks License And Terms Gate](sportmonks_license_terms_gate.md)
- Related response summary: [Sportmonks Permission Response Summary](sportmonks_permission_response_summary.md)
- Related decision record: [Sportmonks Payload Decision Record](../provider_decisions/sportmonks_payload_decision_record.md)
- Related trial scope plan: [Sportmonks Ignored Local Trial Scope Plan](sportmonks_ignored_local_trial_scope_plan.md)
- Related ID discovery plan: [Sportmonks ID Discovery Plan](sportmonks_id_discovery_plan.md)
- Related credential setup: [Sportmonks Secure Credential Setup](sportmonks_secure_credential_setup.md)
- Related credential verification: [Sportmonks Local Credential Setup Verification](sportmonks_local_credential_setup_verification.md)
- Discovery summary: [Sportmonks Minimal ID Discovery Summary](sportmonks_minimal_id_discovery_summary.md)
- Confirmed ID scope review: [passed](sportmonks_confirmed_id_scope_review.md)
- Minimal payload field review decision: [executed under strict scope](../provider_decisions/sportmonks_minimal_payload_field_review_decision.md)
- Minimal payload field review summary: [passed](sportmonks_minimal_payload_field_review_summary.md)
- Checklist status: draft/pre-trial
- Gate decision: `continue`
- Provider approval: no
- Broad payload inspection performed: no
- Credentials created locally: yes, outside Git
- Credentials stored in Git: no
- API calls performed: yes, 3 minimal discovery calls
- Local provider cache created: yes, ignored
- Provider cache committed: no
- Local trial performed: no
- Decision record created: yes, draft/pre-trial
- Notes: This checklist and the draft decision record prepare the next governance step only. They do not approve Sportmonks or authorize production use.

## Purpose

This checklist defines the minimum conditions before any Sportmonks payload inspection or ignored local trial. It applies the permission response safely while keeping raw payloads, credentials, cache, `.local.csv` outputs and confidential correspondence outside Git.

It does not activate Sportmonks data in the app or write provider data to SQLite.

## Permission Basis

- The [Stage 1 gate](sportmonks_license_terms_gate.md) is `continue` for the next governance step only.
- The [response summary](sportmonks_permission_response_summary.md) records permission for local evaluation, schema and payload inspection, local caching for development/debugging under an active subscription and Terms of Service compliance, internal normalized/canonical outputs, and internal derived-output documentation and demos.
- Conditions:
  - comply with the Sportmonks Terms of Service;
  - keep the subscription active for local caching;
  - do not expose or redistribute raw Sportmonks data;
  - do not expose or commit API keys; and
  - confirm that required fields and endpoints are available under the selected plan and competitions.

## Pre-Trial Checklist

| Area | Requirement | Status | Notes |
|---|---|---|---|
| Selected plan | Football Free Plan confirmed by user screenshot. | confirmed | 4 leagues and 3000 API calls shown; no paid plan selected. |
| Competition scope | Denmark Superliga, league_id 271. | confirmed | Confirmed included in the Free Plan by user screenshot. |
| Season scope | Denmark Superliga 2026/2027, `season_id 27897`. | confirmed | Confirmed by [minimal ID discovery](sportmonks_minimal_id_discovery_summary.md). |
| Team scope | FC København, `team_id 85`. | confirmed | Confirmed by [minimal ID discovery](sportmonks_minimal_id_discovery_summary.md). |
| Endpoint scope | Team Squad by Team and Season ID only. | access confirmed | The confirmed squad endpoint is the sole endpoint allowed by the minimal field review decision. |
| Field scope | Review only field names and high-level categories for the confirmed squad endpoint. | reviewed minimal / passed | [Summary](sportmonks_minimal_payload_field_review_summary.md) records identity, team, season, position and jersey categories; dates/freshness/provenance remain unclear. |
| Payload minimization | One FC København squad, one Denmark Superliga season, minimal payload. | proposed | Avoid broad pulls; season and team IDs are confirmed. |
| Raw data handling | Confirm raw payloads stay outside Git. | verified for ID discovery | Raw ID discovery responses remain only under the ignored local provider cache path. |
| Cache handling | Confirm cache path, retention and cleanup. | partial | ID discovery cache is ignored and uncommitted; future trial retention and cleanup remain pending. |
| Credential handling | Store API token only in local ignored `.env` or equivalent configuration. | local setup verified/outside Git | [Verification record](sportmonks_local_credential_setup_verification.md) exists; only 3 minimal discovery calls have occurred. |
| Derived output handling | Confirm derived outputs do not expose raw data. | pending | Internal review only. |
| Documentation handling | Confirm documentation uses non-sensitive summaries only. | pending | No raw payload excerpts. |
| Demo handling | Confirm demos use derived, non-raw content only. | pending | No raw redistribution. |
| SQLite handling | Confirm no provider data writes to SQLite in the trial. | pending | Keep trial isolated. |
| App handling | Confirm no Streamlit activation in the trial. | pending | No app integration. |
| Decision record | Prepare a payload-specific decision record before the trial. | draft/pre-trial | [Record created](../provider_decisions/sportmonks_payload_decision_record.md); concrete trial scope remains pending. |
| Cleanup | Define cleanup procedure for local payload/cache. | pending | Required before trial. |

## Credential Setup Verification

The requirements below are recorded as passed in the [local credential setup verification](sportmonks_local_credential_setup_verification.md).

- Selected plan is documented.
- Competition scope is documented.
- Credential storage path is defined and ignored by Git.
- `.env` or local configuration is confirmed not tracked.
- No credentials appear in `git status`, `git diff` or tracked files.
- Decision record exists or is being prepared before credentials are used.
- User explicitly confirms credential creation outside Git.

## Required Before Payload Inspection

- Payload-specific decision record exists.
- Endpoint and field scope are documented.
- Sample size is minimal.
- Local ignored raw payload path is defined.
- Local ignored cache path is defined.
- Cleanup process is documented.
- Raw payloads will not be pasted into documentation, tests or examples.
- No SQLite write is planned.
- No app integration is planned.
- No parser or transform code is planned in this block.

## Required Before Local Trial

- Checklist reviewed.
- Decision record reviewed.
- Selected plan and competitions documented.
- Credentials stored securely outside Git.
- Ignored local folders confirmed.
- Trial commands planned but not run in this docs-only block.
- Expected outputs defined as ignored local artifacts.
- Cleanup command or process defined.
- Stop conditions reviewed.

## Stop Conditions

- Any credential appears in Git.
- Any raw payload appears in Git.
- Any provider cache appears in Git.
- Any `.local.csv` provider output appears in Git.
- Endpoint or field scope is broader than needed.
- Selected plan does not clearly support intended data.
- Terms of Service or subscription conditions conflict with the planned trial.
- Trial would expose or redistribute raw Sportmonks data.
- Trial requires app activation or SQLite writes.
- Checklist or decision record remains incomplete.

## Still Forbidden In This Block

- Do not expose or commit credentials.
- Do not inspect payloads.
- Do not make additional Sportmonks API calls in this docs-only update.
- Do not commit provider cache.
- Do not create `.local.csv` provider outputs.
- Do not write provider data to SQLite.
- Do not activate provider data in Streamlit.
- Do not create parser or transform code.
- Do not commit raw correspondence, ticket identifiers, legal text excerpts, credentials or payloads.
- Do not treat this checklist as provider approval.

## Next Governance Artifact

The [payload-specific decision record](../provider_decisions/sportmonks_payload_decision_record.md) now exists as a draft/pre-trial artifact.

Minimal ID discovery, confirmed ID scope review and the [minimal field review](sportmonks_minimal_payload_field_review_summary.md) have passed. Cleanup remains pending, and no trial or broad payload inspection has been performed. The next gate is a docs-only transform design suitability decision.

## Acceptance Criteria

- [ ] Sportmonks provider payload checklist exists.
- [ ] It links the gate and response summary.
- [ ] It does not include raw provider correspondence.
- [ ] It does not include ticket identifiers.
- [ ] It does not include credentials.
- [ ] It does not include payloads.
- [ ] It does not approve Sportmonks.
- [ ] It requires a decision record before trial.
- [ ] It keeps local trial outputs ignored and outside Git.
- [ ] No code is changed.
- [ ] No data files are generated.
- [ ] `git diff --check` passes.
