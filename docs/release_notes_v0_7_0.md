# Release Notes - v0.7.0

## Status

- Release status: published
- Release URL: https://github.com/albertopernas-dev/football-scout-dashboard/releases/tag/v0.7.0
- Release type: documentation/governance milestone
- Provider integration: not started
- Provider approval: none
- Current candidate: Sportmonks, Candidate Intake only
- Gate decision: `defer`
- Payload inspection: not allowed
- Credentials setup: not allowed
- Local trial: not allowed
- Code changes: none
- Real provider data: none

## Summary

v0.7.0 formalizes the permitted-provider candidate review process. It adds a neutral shortlist matrix, candidate review workflow, reusable review pack template, and a Sportmonks Stage 0/Stage 1 intake path. The Sportmonks gate remains deferred pending applicable license or subscription terms, or explicit permission. No provider is approved, no payload is inspected, and no integration code is added.

## Added

- v0.7.0 permitted provider candidate review plan.
- Candidate review workflow.
- Candidate review pack template.
- Provider candidate shortlist matrix.
- Provider candidates documentation folder.
- Initial provider and source shortlist.
- Sportmonks Stage 0 candidate review pack.
- Sportmonks Stage 1 license and terms gate.
- Sportmonks public terms review notes.
- Sportmonks permission request draft.
- v0.7.0 release readiness document.

## Changed

- README links updated for v0.7.0 governance documents.
- ROADMAP updated with the current v0.7.0 state.
- v0.7.0 plan updated with the current Sportmonks Stage 0/Stage 1 status and next steps.

## Not Included

- No real provider integration.
- No provider approval.
- No passed license gate.
- No real payload inspection.
- No credentials or API keys.
- No live API calls.
- No scraping.
- No provider data cache.
- No provider `.local.csv` outputs.
- No SQLite writes.
- No Streamlit app activation.
- No parser or transform code for real provider payloads.
- No payload-specific decision record.

## Current Decision

- Candidate: Sportmonks
- Stage: Stage 1 License And Terms Gate
- Decision: `defer`
- Reason:
  - Public-source review is insufficient for project-specific permission.
  - Applicable license or subscription terms are not reviewed.
  - Explicit permission is not obtained.
  - Payload inspection, caching, derived outputs and redistribution remain unknown.

## Safety And Governance

v0.7.0 intentionally stops at the permission boundary. Technical documentation is not treated as license permission, and blog, glossary or documentation references do not authorize caching or payload use. Any future provider work must pass through the gate, checklist and payload-specific decision record.

## Verification

- `git status --short`: clean
- `git diff --check`: passed
- Tracked `data/provider_cache/` files: none
- Tracked `*.local.csv` files: none
- Credential or secret pattern check: no matches
- pytest: not run because v0.7.0 is docs-only

## Post-Release Next Steps

1. Send or adapt the Sportmonks permission request outside the repository.
2. Record only non-sensitive response summaries.
3. Keep the gate as `defer` unless explicit permissions are clear.
4. If the gate moves to `continue`, prepare the provider payload checklist.
5. If a concrete permitted payload exists, prepare a payload-specific decision record.
6. If permission remains unclear, keep the candidate deferred.
7. If terms block the intended use, reject the candidate.
8. Do not inspect payloads or create credentials until the gate explicitly allows it.

## Tagging Notes

- The tag should only be created after these release notes are committed and `git status --short` is clean.
- Suggested tag: `v0.7.0`
- Suggested GitHub release title: `v0.7.0 - Permitted Provider Candidate Review`
- The suggested release body can reuse Summary, Added, Not Included and Current Decision.
