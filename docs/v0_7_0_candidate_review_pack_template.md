# v0.7.0 Candidate Review Pack Template

## Purpose

Copy this template when a concrete candidate is explicitly selected for review. This document is not a decision record, does not approve any provider and does not authorize payload inspection, caching, transformation or integration.

Use it together with:

- [v0.7.0 Candidate Review Workflow](v0_7_0_candidate_review_workflow.md)
- [Provider Payload Evaluation Checklist](provider_payload_evaluation_checklist.md)
- [Provider Payload Evaluation Template](provider_decisions/provider_payload_evaluation_template.md)

## How To Use

1. Copy this template to a candidate-specific local or documentation file only after a candidate is explicitly named.
2. Do not include restricted payload data.
3. Keep real payloads out of git.
4. Link to the completed checklist.
5. Link to the provider payload decision record.
6. Stop if the license or terms are unclear.

If the review contains restricted terms excerpts, credentials, raw payloads or non-redistributable details, keep it local and ignored. Do not commit it.

## Candidate Intake

- Candidate name:
- Source type: API / licensed export / manual reference / permitted public source / other
- Website / documentation reference:
- Intended use:
- Expected fields:
- Reviewer:
- Review date:
- Initial risk level: low / medium / high / unknown
- Initial notes:

## License And Terms Gate

- Terms reviewed: yes / no
- License source:
- Local development permitted: yes / no / unknown
- Payload inspection permitted: yes / no / unknown
- Caching permitted: yes / no / unknown
- Derived outputs permitted: yes / no / unknown
- Screenshots/demo permitted: yes / no / unknown
- Redistribution permitted: yes / no / unknown
- Credential restrictions:
- Blocking restrictions:
- Gate decision: stop / continue
- Notes:

If any required permission is unknown, stop or defer before inspecting payloads.

## Payload Handling Plan

- Permitted payload location:
- Ignored storage path:
- Raw payload retention:
- Derived output path:
- Cleanup command:
- Secrets handling:
- Git safety command:
- Handling approved: yes / no

Use `data/provider_cache/` or `data/enrichment/*.local.csv` only.

## Checklist And Decision Record

- Completed checklist path:
- Decision record path:
- Decision record type: general provider / payload-specific
- Evidence references:
- Open blockers:
- Reviewer sign-off:

## Payload Shape Review

- Payload type:
- Format: JSON / CSV / API response / export / other
- Provider identity fields:
- Team identity fields:
- League/season fields:
- Player display fields:
- Market value fields:
- Contract fields:
- Age/birthdate fields:
- Source/provenance fields:
- Value date / `fetched_at` fields:
- Missing value semantics:
- Currency semantics:
- Date format:
- Notes:

## Identity Mapping Plan

- Strong provider IDs available: yes / no / partial
- Team-aware mapping possible: yes / no / partial
- Season-aware mapping possible: yes / no / partial
- Name-only/fuzzy matching required: yes / no
- Duplicate risk:
- Mapping output path:
- Manual review required:
- Expected matched coverage:
- Notes:

## Market Context Fit

- Can produce canonical age:
- Can produce canonical `market_value_eur`:
- Can produce canonical `contract_end_date`:
- Can produce source:
- Can produce `source_url`:
- Can produce confidence:
- Can produce notes:
- Optional fields:
- Known gaps:
- Notes:

## Local Trial Plan

- Trial allowed: yes / no
- Reason:
- Input path:
- Mapping path:
- Flattened output path:
- Mapped output path:
- Canonical output path:
- Preview command:
- Diagnostics command:
- Cleanup command:
- App activation allowed: no
- SQLite writes allowed: no
- Network calls allowed: no

Trial paths must be ignored local paths. Do not write real outputs into `docs/examples/`.

## Diagnostics Summary

- Payload rows:
- Flattened rows:
- Mapped rows:
- Unmatched rows:
- Duplicate identities:
- Canonical rows:
- Validation errors:
- Effective age coverage:
- Effective market value coverage:
- Effective contract coverage:
- Missing critical fields:
- Currency/date issues:
- Provenance quality:
- Notes:

## Final Outcome

- Final decision: accept / defer / reject
- Rationale:
- Accepted scope, if any:
- Deferred blockers:
- Rejection reason:
- Follow-up actions:
- Re-review trigger:
- Reviewer:
- Date:

## Safety Checklist

- [ ] No real payload committed.
- [ ] No raw provider dump committed.
- [ ] No credentials committed.
- [ ] No `.local.csv` committed.
- [ ] No `data/provider_cache/` contents committed.
- [ ] No app activation performed.
- [ ] No SQLite writes performed.
- [ ] No scraping performed.
- [ ] No live provider calls from Streamlit.
- [ ] Final `git status --short` is clean.

## Stop Conditions

- License unclear.
- Payload inspection not permitted.
- Caching forbidden but required.
- Derived outputs forbidden but required.
- Identity fields too weak.
- Missing-value or provenance semantics unclear.
- Currency or date semantics ambiguous.
- Restricted data appears in git status.
- Candidate cannot meet Market Context minimum requirements.

## Relationship To Other Docs

- [v0.7.0 Candidate Review Workflow](v0_7_0_candidate_review_workflow.md)
- [v0.7.0 Permitted Provider Candidate Review Plan](v0_7_0_permitted_provider_candidate_review_plan.md)
- [Provider Payload Evaluation Checklist](provider_payload_evaluation_checklist.md)
- [Provider Payload Evaluation Template](provider_decisions/provider_payload_evaluation_template.md)
- [Provider Payload Shape Notes](provider_payload_shape_notes.md)
