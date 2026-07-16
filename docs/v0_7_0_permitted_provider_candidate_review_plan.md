# v0.7.0 - Permitted Provider Candidate Review

## Objective

v0.7.0 focuses on reviewing a real or otherwise permitted provider candidate only after its license and terms have been confirmed. The objective is not to integrate a provider, but to decide whether a candidate payload may proceed to an ignored local experiment.

The review must conclude with an explicit decision: accept, defer or reject.

## Starting Point

This milestone builds on the safeguards and synthetic workflow completed in v0.6.0:

- [v0.6.0 release notes](release_notes_v0_6_0.md)
- [Provider Payload Evaluation Checklist](provider_payload_evaluation_checklist.md)
- [Provider Payload Evaluation Template](provider_decisions/provider_payload_evaluation_template.md)
- [Advanced Synthetic Payload Shape Notes](provider_payload_shape_notes.md)
- Advanced synthetic flattening and end-to-end demo
- [v0.7.0 Candidate Review Workflow](v0_7_0_candidate_review_workflow.md)
- [v0.7.0 Provider Candidate Shortlist Matrix](v0_7_0_provider_candidate_shortlist_matrix.md)
- [v0.7.0 Initial Provider Candidate Shortlist](provider_candidates/v0_7_0_initial_shortlist.md)

Synthetic success demonstrates the workflow only. It does not establish that any real payload is licensed, compatible or approved.

## Scope

- Identify a candidate provider or source.
- Review its license and terms before inspecting or storing payloads.
- Document any payload that is explicitly permitted for evaluation.
- Complete the provider payload evaluation checklist.
- Create a payload decision record.
- Review provider identity and Market Context fields.
- Estimate field coverage and matching feasibility.
- Define ignored local storage and cleanup rules.
- Decide whether a local experiment may proceed.

## Out Of Scope

- Real provider integration.
- App activation.
- Scraping.
- Live provider calls from Streamlit.
- Credentials in the repository.
- Real payloads in git.
- SQLite writes from provider payloads.
- Scoring changes.
- Opportunity Finder changes.
- UI provenance changes.

## Candidate Review Workflow

1. Select a candidate provider or source explicitly.
2. Confirm permission and licensing before inspecting or storing payloads.
3. Complete the provider payload evaluation checklist.
4. Create a provider payload decision record using the v0.6.0 template.
5. Store any permitted real payload only in ignored local paths.
6. Run local and offline experiments only.
7. Produce coverage and validation diagnostics.
8. Decide accept, defer or reject.
9. Consider a provider-specific transform helper only after an accept decision.

## Required Artifacts Before Any Experiment

- Completed payload evaluation checklist.
- Provider payload decision record.
- License and terms notes.
- Payload provenance notes.
- Cache and storage decision.
- Identity mapping plan.
- Cleanup plan.
- Git safety check.

## Local Experiment Rules

- Store payloads under `data/provider_cache/` or as ignored `.local.csv` files only.
- Do not commit raw dumps.
- Write generated outputs as `.local.csv`.
- Do not activate outputs in the app.
- Keep demo scripts offline and free of provider network calls.
- Store no secrets or credentials.
- Document cleanup commands.
- Finish with a clean git status.

## Acceptance Criteria

- README and ROADMAP identify v0.7.0 as the current milestone.
- This v0.7.0 plan exists.
- The operational candidate review workflow exists.
- A copyable candidate review pack template exists without naming a candidate.
- A neutral shortlist matrix exists without selecting or evaluating a real candidate.
- A preliminary shortlist exists without selecting a final candidate.
- No real provider is chosen in this initial block.
- No real payload is evaluated in this initial block.
- No code is added.
- No data is generated.
- The next block can create a blank candidate review issue or checklist copy, or wait for a named candidate.

## Risks

- Ambiguous licensing or terms.
- Payload redistribution restrictions.
- Weak identity matching.
- Low Market Context coverage.
- Unclear currency or date semantics.
- Accidental versioning of local data.
- Treating synthetic success as real-provider readiness.

## Next Steps

Follow the [v0.7.0 Candidate Review Workflow](v0_7_0_candidate_review_workflow.md) when a candidate is explicitly chosen.

1. Choose a candidate explicitly.
2. Complete the payload evaluation checklist.
3. Create a decision record.
4. Run an ignored local payload trial only if the license and decision allow it.
