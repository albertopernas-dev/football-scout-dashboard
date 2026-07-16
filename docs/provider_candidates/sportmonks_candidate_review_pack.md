# Sportmonks Candidate Review Pack

## Status

- Candidate: Sportmonks
- Review stage: Stage 0 - Candidate Intake
- License gate status: not started
- Payload inspection status: not started
- Trial status: not allowed
- Decision status: no decision
- Reviewer:
- Date:
- Notes: This pack does not approve Sportmonks, does not authorize payload inspection and does not replace a payload decision record.

## Purpose

This document starts Candidate Intake for Sportmonks as the candidate chosen from the preliminary shortlist. It does not review current terms, approve a license or authorize downloading, caching, transforming or integrating provider data.

The next mandatory step is Stage 1 - License And Terms Gate. No payload may be inspected unless that gate explicitly permits the intended activity.

## Source Context

- Candidate name: Sportmonks
- Source type: structured football data provider candidate
- Intended use: evaluate whether permitted payloads could support identity and Market Context review
- Existing project context: appears in historical provider evaluation material and the v0.7.0 initial shortlist as an `investigate` hypothesis, not as approval
- Documentation/source reference: pending current review
- Expected fields: unknown until permitted documentation and payload review
- Initial label from shortlist: investigate
- Current review outcome: pending

## Stage 0 - Candidate Intake

- Candidate name: Sportmonks
- Source type: API / licensed export / other: structured football data provider candidate
- Intended use: assess whether permitted Sportmonks data can support local Market Context candidate review
- Data fields expected: unknown; identity and Market Context fields require review
- Owner/reviewer:
- Review date:
- Initial risk notes:
  - License permissions unknown.
  - Cache permissions unknown.
  - Derived-output permissions unknown.
  - Field availability unknown.
  - No payload inspected.
- Stage 0 status: draft
- Stage 0 outcome: ready for license gate / defer

## Stage 1 - License And Terms Gate

Review scaffold: [Sportmonks License And Terms Gate](sportmonks_license_terms_gate.md). It remains `not reviewed` with decision `defer`.

- Terms reviewed: no
- License source: pending
- Local development permitted: unknown
- Payload inspection permitted: unknown
- Caching permitted: unknown
- Derived outputs permitted: unknown
- Screenshots/demo permitted: unknown
- Redistribution permitted: unknown
- Credential restrictions: unknown
- Blocking restrictions: unknown
- Gate decision: stop until reviewed
- Notes:
  - Do not inspect payloads before this gate is completed.
  - Do not create credentials before terms are reviewed.
  - Do not store provider data in git.

## Payload Handling Plan

- Permitted payload location: not approved
- Ignored storage path: pending; would need `data/provider_cache/` or `data/enrichment/*.local.csv`
- Raw payload retention: not approved
- Derived output path: not approved
- Cleanup command: pending
- Secrets handling: no credentials created
- Git safety command: `git status --short`
- Handling approved: no

## Checklist And Decision Record

- Completed checklist path: not created
- Decision record path: not created
- Decision record type: payload-specific, if a concrete permitted payload is reviewed later
- Evidence references: pending
- Open blockers:
  - Terms and license not reviewed.
  - Payload inspection not permitted yet.
  - Cache and derived-output permissions unknown.
  - Payload shape unknown.
- Reviewer sign-off: pending

## Payload Shape Review

- Payload type: unknown
- Format: unknown
- Provider identity fields: unknown
- Team identity fields: unknown
- League/season fields: unknown
- Player display fields: unknown
- Market value fields: unknown
- Contract fields: unknown
- Age/birthdate fields: unknown
- Source/provenance fields: unknown
- Value date / `fetched_at` fields: unknown
- Missing value semantics: unknown
- Currency semantics: unknown
- Date format: unknown
- Notes: no payload inspected

## Identity Mapping Plan

- Strong provider IDs available: unknown
- Team-aware mapping possible: unknown
- Season-aware mapping possible: unknown
- Name-only/fuzzy matching required: unknown
- Duplicate risk: unknown
- Mapping output path: not approved
- Manual review required: yes, if a trial is later allowed
- Expected matched coverage: unknown
- Notes: mapping cannot be planned until permitted fields are known

## Market Context Fit

- Can produce canonical age: unknown
- Can produce canonical `market_value_eur`: unknown
- Can produce canonical `contract_end_date`: unknown
- Can produce source: unknown
- Can produce `source_url`: unknown
- Can produce confidence: unknown
- Can produce notes: unknown
- Optional fields: unknown
- Known gaps: no permitted payload reviewed
- Notes: no Market Context claims are made

## Local Trial Plan

- Trial allowed: no
- Reason: license and terms gate not completed
- Input path: not approved
- Mapping path: not approved
- Flattened output path: not approved
- Mapped output path: not approved
- Canonical output path: not approved
- Preview command: not approved
- Diagnostics command: not approved
- Cleanup command: pending
- App activation allowed: no
- SQLite writes allowed: no
- Network calls allowed: no

## Diagnostics Summary

- Payload rows: not available
- Flattened rows: not available
- Mapped rows: not available
- Unmatched rows: not available
- Duplicate identities: not available
- Canonical rows: not available
- Validation errors: not available
- Effective age coverage: not available
- Effective market value coverage: not available
- Effective contract coverage: not available
- Missing critical fields: not available
- Currency/date issues: not available
- Provenance quality: not available
- Notes: diagnostics require a permitted local trial

## Final Outcome

- Final decision: pending
- Rationale: Stage 0 only; Stage 1 not completed
- Accepted scope, if any: none
- Deferred blockers:
  - License and terms review.
  - Permission for payload inspection.
  - Cache and derived-output permission.
  - Payload shape evidence.
- Rejection reason: none
- Follow-up actions:
  - Complete Stage 1 - License And Terms Gate.
  - Create a checklist only if terms permit review.
  - Create a payload decision record only if a concrete permitted payload exists.
- Re-review trigger: completion of license gate
- Reviewer:
- Date:

## Safety Checklist

- [x] No real payload committed.
- [x] No raw provider dump committed.
- [x] No credentials committed.
- [x] No `.local.csv` committed.
- [x] No `data/provider_cache/` contents committed.
- [x] No app activation performed.
- [x] No SQLite writes performed.
- [x] No scraping performed.
- [x] No live provider calls from Streamlit.
- [ ] Final `git status --short` is clean.

## Stop Conditions

- License unclear.
- Payload inspection not permitted.
- Caching forbidden or unknown.
- Derived outputs forbidden or unknown.
- Provider fields unavailable or unclear.
- Restricted data appears in git status.
- Credentials required before terms are reviewed.

## Next Required Action

The next block must perform only a terms and license review using publicly accessible documentation or user-provided permitted terms. No payload inspection or credential setup is allowed unless the gate explicitly permits it.
