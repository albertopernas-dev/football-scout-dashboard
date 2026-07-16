# v0.7.0 Release Readiness

## Purpose

This document evaluates whether v0.7.0 is ready to close as a documentation and governance milestone. v0.7.0 does not deliver a real provider integration, approve Sportmonks, or authorize payload inspection, credentials, caching, derived outputs, SQLite writes or app activation.

The expected outcome is a project that stops correctly at the permission boundary until applicable license or subscription terms, or explicit written permission, are available.

## Release Position

- Candidate selected for intake: Sportmonks
- Current gate: Stage 1 License And Terms Gate
- Gate decision: `defer`
- Reason: public-source review is insufficient for project-specific permission
- External dependency: applicable license or subscription terms, or explicit written permission
- Release type: documentation/governance milestone
- Integration status: not started
- Data status: no real provider payloads
- Code status: no provider integration code

## Included v0.7.0 Artifacts

- [v0.7.0 candidate review plan](v0_7_0_permitted_provider_candidate_review_plan.md)
- [Candidate review workflow](v0_7_0_candidate_review_workflow.md)
- [Candidate review pack template](v0_7_0_candidate_review_pack_template.md)
- [Provider candidate shortlist matrix](v0_7_0_provider_candidate_shortlist_matrix.md)
- [Provider candidates README](provider_candidates/README.md)
- [Initial provider shortlist](provider_candidates/v0_7_0_initial_shortlist.md)
- [Sportmonks candidate review pack](provider_candidates/sportmonks_candidate_review_pack.md)
- [Sportmonks license and terms gate](provider_candidates/sportmonks_license_terms_gate.md)
- [Sportmonks public terms review notes](provider_candidates/sportmonks_public_terms_review_notes.md)
- [Sportmonks permission request draft](provider_candidates/sportmonks_permission_request_draft.md)

## What v0.7.0 Completed

- Created the formal candidate review workflow.
- Created a copyable candidate review pack template.
- Created a neutral shortlist matrix.
- Created a preliminary provider and source shortlist.
- Selected Sportmonks for Candidate Intake only.
- Created the Sportmonks Stage 0 intake pack.
- Created the Sportmonks Stage 1 license and terms gate.
- Recorded partial public-source review notes.
- Created a permission request draft.
- Updated current next steps to reflect that permission is the blocker.

## What v0.7.0 Does Not Do

- Does not approve Sportmonks.
- Does not pass the license gate.
- Does not inspect real payloads.
- Does not create credentials.
- Does not call provider APIs.
- Does not scrape.
- Does not cache provider data.
- Does not create provider `.local.csv` outputs.
- Does not write provider data to SQLite.
- Does not add parser or transform code for a real provider.
- Does not activate provider data in Streamlit.
- Does not create a payload-specific decision record.

## Release Blockers

No technical blocker prevents releasing v0.7.0 as a documentation and governance milestone.

Any advance toward provider integration remains blocked because:

- applicable license or subscription terms have not been reviewed;
- explicit permission has not been obtained;
- payload inspection permission is unknown;
- local caching permission is unknown;
- derived-output permission is unknown;
- redistribution and demo restrictions are unknown;
- endpoint, field and plan scope are unknown; and
- credential and account restrictions are unknown.

## Release Acceptance Criteria

- [ ] v0.7.0 plan exists.
- [ ] Candidate review workflow exists.
- [ ] Candidate review pack template exists.
- [ ] Neutral shortlist matrix exists.
- [ ] Initial shortlist exists.
- [ ] Sportmonks intake pack exists.
- [ ] Sportmonks license gate exists.
- [ ] Public-source review notes exist.
- [ ] Permission request draft exists.
- [ ] Gate decision remains correctly recorded as `defer`.
- [ ] No provider is approved.
- [ ] No real payload is committed.
- [ ] No credentials are committed.
- [ ] No `.local.csv` outputs are committed.
- [ ] No `data/provider_cache/` contents are committed.
- [ ] No code changes are included in v0.7.0.
- [ ] `git diff --check` passes.
- [ ] Final `git status --short` is clean before tagging.

## Required Verification Before Tagging

- Run `git diff --check`.
- Run `git status --short`.
- Confirm no tracked changes exist under `data/provider_cache/`.
- Confirm no tracked `.local.csv` files exist.
- Confirm no credentials or secrets changed.
- Because this milestone is docs-only, pytest is optional and is not required unless code changed.

## Suggested Release Summary

Draft release notes: [Release Notes - v0.7.0](release_notes_v0_7_0.md).

```text
v0.7.0 formalizes the permitted-provider candidate review process. It adds a shortlist matrix, candidate review workflow, reusable review pack, and a Sportmonks Stage 0/Stage 1 intake path. The Sportmonks gate remains deferred pending applicable license/subscription terms or explicit permission. No provider is approved, no payload is inspected, and no integration code is added.
```

## Post-Release Next Actions

- Send or adapt the Sportmonks permission request outside the repository.
- Record only non-sensitive response summaries.
- Keep the gate as `defer` unless explicit permissions are clear.
- If permission is clear, prepare the checklist and a payload-specific decision record.
- If permission is unclear, keep the candidate deferred.
- If terms block the intended use, reject the candidate.
- Do not inspect payloads or create credentials until the gate explicitly moves to `continue`.

## Safety Statement

v0.7.0 is intentionally conservative. The milestone ends at the permission boundary and does not cross into provider data handling.
