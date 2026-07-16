# v0.7.0 Candidate Review Workflow

## Purpose

This document provides the operational sequence for reviewing a permitted candidate. It does not select a provider, approve a payload or replace the payload evaluation checklist and decision record. Its purpose is to control the work that must happen before any ignored local experiment.

## When To Use This Workflow

Use this workflow when:

- A specific provider or source candidate exists.
- There is a reasonable basis for permission or licensing.
- The team needs to decide whether a payload may proceed to an ignored local trial.

Do not use it for:

- Scraping.
- Providers with unclear terms.
- Payloads obtained without permission.
- Real data that cannot be stored locally under the applicable terms.
- Direct app integration.

Before Stage 0, the [provider candidate shortlist matrix](v0_7_0_provider_candidate_shortlist_matrix.md) may be used to decide whether a candidate merits intake. The matrix does not approve a provider or payload.

## Review Stages

### Stage 0 - Candidate Intake

Current intake example: the [Sportmonks Candidate Review Pack](provider_candidates/sportmonks_candidate_review_pack.md) is at Stage 0 only. Stage 1 is not complete and no payload inspection is authorized.

Record:

- Candidate name.
- Source type: API, licensed export, manual reference, permitted public source or other.
- Intended use.
- Expected data fields.
- Owner or reviewer.
- Review date.
- Initial risk notes.

### Stage 1 - License And Terms Gate

- Review terms before downloading or inspecting a payload.
- Confirm whether local development is permitted.
- Confirm whether caching is permitted.
- Confirm whether derived outputs are permitted.
- Confirm whether screenshots or demos are permitted.
- Record redistribution restrictions.
- Decide: stop or continue.

If the license or terms are unclear, stop the review.

### Stage 2 - Payload Handling Plan

- Define where a permitted payload would be stored.
- Use only `data/provider_cache/` or ignored `.local.csv` paths.
- Document retention and cleanup.
- Store no credentials with payloads.
- Do not version raw dumps.
- Decide whether safe local handling is possible.

### Stage 3 - Checklist Completion

- Complete [`docs/provider_payload_evaluation_checklist.md`](provider_payload_evaluation_checklist.md).
- Record gaps and blockers.
- Link internal evidence without placing sensitive or restricted data in git.

### Stage 4 - Decision Record

- Create a record from [`docs/provider_decisions/provider_payload_evaluation_template.md`](provider_decisions/provider_payload_evaluation_template.md).
- Cover license, provenance, payload shape, identity fit, Market Context fit, cache and storage, and expected diagnostics.
- Record an initial decision: accept, defer or reject.

### Stage 5 - Local Ignored Trial

Proceed only when Stage 4 explicitly allows it.

- Run a local and offline experiment.
- Write outputs only as ignored `.local.csv` files.
- Do not activate data in the app.
- Do not write to SQLite.
- Keep demo scripts free of network calls.
- Remove generated outputs when they are no longer needed.
- Confirm git status remains clean.

### Stage 6 - Diagnostics And Decision

Review:

- Coverage.
- Matched and unmatched identities.
- Duplicate identities.
- Validation errors.
- Missing fields.
- Currency and date semantics.
- Source and provenance quality.

Record the final decision: accept, defer or reject.

### Stage 7 - Next Action

- **Accept:** propose a provider-specific transform helper in a later block.
- **Defer:** document blockers and requirements for reconsideration.
- **Reject:** document the rationale and close the candidate review.

## Required Files For A Candidate

- Candidate review pack copied from the [v0.7.0 template](v0_7_0_candidate_review_pack_template.md); this does not replace the decision record.
- Completed or copied payload evaluation checklist.
- Provider payload decision record.
- License and terms notes.
- Payload handling plan.
- Identity mapping plan.
- Diagnostics summary.
- Cleanup notes.

## Git Safety Rules

- Do not commit real payloads.
- Do not commit raw provider dumps.
- Do not commit credentials or secrets.
- Do not commit `.local.csv` files.
- Do not commit `data/provider_cache/` contents.
- Delete or ignore generated local outputs.
- Finish with a clean git status.

## Stop Conditions

- License or terms are unclear.
- Permission to inspect or cache the payload is absent.
- Required derived outputs are forbidden.
- Identity fields are too weak for reviewed matching.
- Provenance is missing.
- The payload cannot distinguish missing values from zero.
- Currency or date semantics are unclear.
- Real data appears in git status.

## Candidate Review Outcome Template

```text
Candidate:
Reviewer:
Date:
License gate: stop / continue
Payload handling: approved / not approved
Checklist status:
Decision record:
Trial allowed: yes / no
Final decision: accept / defer / reject
Follow-up:
```

## Relationship To v0.6.0

v0.6.0 established the synthetic workflow and safety tools. v0.7.0 applies that framework only after a permitted candidate is named and reviewed. Synthetic success does not imply approval of any real provider or payload.

## Relationship To Future Work

A provider-specific parser or transform helper may be considered only after an accept decision. App activation must wait until license, provenance and coverage are clear. UI provenance, scoring and Opportunity Finder changes remain out of scope until a separate decision is made.
