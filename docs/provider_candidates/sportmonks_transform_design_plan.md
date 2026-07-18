# Sportmonks Transform Design Plan

## Status

- Candidate: Sportmonks
- Plan status: `draft/docs-only`
- Related suitability decision: [Sportmonks Transform Design Suitability Decision](../provider_decisions/sportmonks_transform_design_suitability_decision.md)
- Related minimal payload field review summary: [Sportmonks Minimal Payload Field Review Summary](sportmonks_minimal_payload_field_review_summary.md)
- Related payload decision record: [Sportmonks Payload Decision Record](../provider_decisions/sportmonks_payload_decision_record.md)
- Provider approval: no
- Transform implementation approved: no
- Transform code created: no
- API calls performed in this block: no
- Raw responses reviewed in this block: no
- `.local.csv` outputs created: no
- SQLite writes performed: no
- Streamlit activation performed: no
- Local trial performed: no

## Purpose

This document plans a future transform design based only on the non-sensitive field and category summary.

It does not read raw Sportmonks payloads, implement parser or normalizer code, or approve Sportmonks. It defines candidate mappings, gaps, validation needs and future decisions that must be resolved before any implementation.

## Scope And Non-Goals

### In Scope

- One endpoint shape: `/football/squads/seasons/{season_id}/teams/{team_id}`.
- Confirmed IDs:
  - `league_id 271`;
  - `season_id 27897`; and
  - `team_id 85`.
- Documentation-only transform design.
- Candidate canonical field mapping.
- Provenance and freshness strategy.
- Label-resolution strategy.
- Validation rules.
- Stop conditions.
- Open decisions before implementation.

### Out Of Scope

- Code implementation.
- API calls.
- Raw JSON review.
- Provider cache changes.
- `.local.csv` creation.
- SQLite loading.
- Streamlit integration.
- Player-detail endpoints.
- Broad Sportmonks payload inspection.
- Provider approval.
- Local trial.

## Input Endpoint And Confirmed IDs

| Item | Value | Status |
|---|---|---|
| Provider | Sportmonks | candidate only |
| Endpoint | Team Squad by Team and Season ID | confirmed access |
| Endpoint pattern | `/football/squads/seasons/{season_id}/teams/{team_id}` | confirmed |
| League | Denmark Superliga | confirmed |
| League ID | `271` | confirmed |
| Season | 2026/2027 | confirmed |
| Season ID | `27897` | confirmed |
| Team | FC København | confirmed |
| Team ID | `85` | confirmed |
| Sample count | `6` records | observed in minimal review |

## Observed Field Categories

| Category | Status | Source |
|---|---|---|
| Player identity/reference | present | minimal field review |
| Team/squad context | present | minimal field review |
| Season context | present | minimal field review |
| Position/role | present by ID | minimal field review |
| Jersey number | present | minimal field review |
| Record-level dates | unclear/missing | minimal field review |
| Freshness | unclear | minimal field review |
| Record-level provenance | unclear | minimal field review |
| Human-readable player labels | unclear/missing | minimal field review |
| Human-readable position labels | unclear/missing | minimal field review |
| Age/value/contract Market Context | not demonstrated | out of this endpoint scope |

## Candidate Canonical Fields

| Candidate Canonical Field | Source Field Category | Status | Notes |
|---|---|---|---|
| `provider` | static value | proposed | Example value: `sportmonks`; do not implement now. |
| `provider_league_id` | confirmed ID | proposed | `271`; ID known from discovery summary. |
| `provider_season_id` | observed `season_id` | proposed | `27897`; confirmed scope. |
| `provider_team_id` | observed `team_id` | proposed | `85`; confirmed scope. |
| `provider_player_id` | observed `player_id` | proposed | Useful for identity mapping, but the label is missing. |
| `provider_position_id` | observed `position_id` | proposed | Needs a label strategy before UI use. |
| `squad_record_id` | observed `id` | proposed | Provider record identifier, if stable. |
| `jersey_number` | observed `jersey_number` | optional | Squad detail; may be nullable. |
| `has_values` | observed `has_values` | optional/unclear | Needs a meaning review before use. |
| `source_endpoint` | endpoint pattern | proposed | Store the pattern, not a token URL. |
| `source_observed_at` | local review timestamp or future run timestamp | proposed | Needed because record-level dates are unclear. |
| `source_freshness_basis` | cache timestamp or response metadata | proposed/pending | Must be defined before implementation. |

No player values, raw JSON or player list are included.

## Fields Explicitly Not Available From This Endpoint

- Human-readable player name is not established from the reviewed shape.
- Human-readable position label is not established from the reviewed shape.
- Player age is not established.
- Market value is not established.
- Contract end date is not established.
- Transfer status is not established.
- Record-level updated date is not established.
- Rich provenance is not established.
- Fitness, injury or availability status is not established.
- Performance statistics are not established.

## Provenance And Freshness Strategy

- Always add the static provider marker `sportmonks`.
- Always add the source endpoint pattern without a token.
- Always add source league, season and team IDs.
- Add `source_observed_at` at future transform execution time.
- Add `source_cache_path_type` or an equivalent summary, not a raw path containing secrets.
- Treat freshness as limited unless:
  - response metadata provides a safe freshness signal; or
  - cache or write timestamp is accepted as observation freshness.
- Do not claim record-level update dates unless a future approved review confirms them.

## Label Resolution Strategy

The current squad endpoint shape is ID-first. Human-readable player and position labels are not confirmed.

Future choices:

1. Defer labels and use only IDs for internal mapping.
2. Use a separately approved minimal lookup or include review.
3. Join labels from an already permitted local canonical source, if available.

No label endpoint, include, player-detail call or additional API call is approved by this plan.

## Validation Rules

| Rule | Severity | Rationale |
|---|---|---|
| `provider_player_id` must be present | error | Identity mapping requires a player reference. |
| `provider_team_id` must equal the confirmed scope or selected future scope | error | Avoid cross-team contamination. |
| `provider_season_id` must equal the confirmed scope or selected future scope | error | Avoid cross-season contamination. |
| `provider_position_id` may be missing only if documented | warning/error pending | Position coverage needs review. |
| `jersey_number` may be nullable | warning | Some squad records may lack shirt numbers. |
| Duplicate provider player IDs in the same team and season require review | warning/error pending | Could reflect a data issue or player-role nuance. |
| Missing provenance fields must stop implementation | error | Traceability is required. |
| Unexpected fields should be logged in a future non-sensitive summary | warning | Supports schema drift detection. |

## Local File And Cache Handling

- Raw Sportmonks responses remain under ignored provider cache only.
- No raw JSON can be committed.
- No `.local.csv` can be created without a future explicit decision.
- Any future transform output path must be ignored first.
- Any future summary in Git must be non-sensitive and contain no raw snippets.
- `.env` must remain ignored and unmodified in Git.

## Stop Conditions

- A docs-only block needs to read raw JSON.
- Additional API calls are needed before a new explicit decision.
- The token appears outside local `.env`.
- Provider cache appears tracked.
- Raw JSON appears in the Git diff.
- The transform requires player-detail endpoints.
- The transform requires broad player, team or league pulls.
- A provenance or freshness strategy cannot be defined.
- Suitability remains only partial and blockers cannot be resolved safely.
- Any licensing or exposure uncertainty appears.

## Open Decisions Before Implementation

| Decision | Why It Matters | Required Before |
|---|---|---|
| Whether an ID-only transform is acceptable | Labels are unclear | Implementation |
| Whether position labels are required | Position IDs may not be readable | UI/report design |
| Whether player labels can come from local canonical data | Avoid extra provider calls | Transform implementation |
| Whether cache timestamp is acceptable freshness | Record-level dates are unclear | Transform implementation |
| Whether a minimal label lookup review is needed | Labels are missing | Any additional API calls |
| Whether `.local.csv` output is allowed | Trial output handling | Local trial |
| Cleanup and retention policy | Cache exists locally | Local trial |
| Whether Sportmonks should move from candidate to trial provider | Governance decision | Local trial |

## Acceptance Criteria For This Design Plan

- No code created.
- No API calls performed.
- No raw JSON reviewed.
- No raw payload snippets included.
- No player names listed.
- No provider cache committed.
- No `.env` committed.
- No `.local.csv` created.
- No SQLite writes.
- No Streamlit activation.
- Provider approval remains no.
- Next action is clearly documented.

## Next Required Action

A later docs-only block may decide whether this transform design plan is sufficient to approve an implementation plan.

An implementation plan is still not implementation.

No transform code, API calls, `.local.csv`, SQLite writes, Streamlit activation, local trial or provider approval are allowed by this document.
