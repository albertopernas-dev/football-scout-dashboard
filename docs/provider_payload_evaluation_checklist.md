# Provider Payload Evaluation Checklist

## Purpose

Use this checklist to decide whether a candidate payload can safely enter the local provider fixture -> identity mapping -> canonical Market Context workflow.

## 1. Legal And License Review

- [ ] Terms reviewed.
- [ ] License permits local development use.
- [ ] License permits caching, or caching is explicitly avoided.
- [ ] License permits derived outputs, or outputs remain local.
- [ ] Redistribution rights are clear.
- [ ] Screenshot and demo restrictions reviewed.
- [ ] No credentials committed.
- [ ] No raw dumps committed.
- [ ] Reviewer and review date documented.

## 2. Payload Provenance

- Provider name:
- Endpoint, report or source name:
- Retrieval method:
- `fetched_at` or `value_date`:
- Sample origin:
- Sample type: synthetic / licensed / public / manual
- Can the sample be versioned?:

## 3. Identity Fields

- [ ] `provider_player_id` is present.
- [ ] `provider_team_id` is present.
- [ ] `provider_league_id` is present.
- [ ] `provider_season` is present.
- [ ] Provider player and team names are present.
- [ ] Season semantics are understood.
- [ ] Duplicate IDs are reviewed.
- [ ] Transfers and team changes are handled.
- [ ] The identity mapping strategy is documented.

## 4. Market Context Fields

- [ ] Age or birthdate is available.
- [ ] Market value is available.
- [ ] Market value currency is available.
- [ ] Market value date is available.
- [ ] Contract end date is available.
- [ ] Loan, option or extension notes are available when relevant.
- [ ] Salary or cost fields are not confused with market value.
- [ ] Missing values are distinguishable from zero.

## 5. Transform Fit

- [ ] The payload can map to the canonical Market Context schema.
- [ ] Optional provider columns can be preserved.
- [ ] The transform can produce `source`, `source_url`, `confidence` and `notes`.
- [ ] Validation errors are understood.
- [ ] Identity mapping confidence remains separate from Market Context confidence.
- [ ] No fuzzy matching is required without manual review.

## 6. Cache And Storage

- [ ] An allowed cache path is identified.
- [ ] `data/provider_cache/` or `.local.csv` is used.
- [ ] No raw provider data is stored in git.
- [ ] Generated outputs are ignored.
- [ ] Retention and refresh policy is documented.
- [ ] Deletion process is documented.

## 7. Diagnostics And Acceptance

- [ ] Canonical preview passes.
- [ ] Validation errors are zero or documented.
- [ ] Duplicate keys are zero or documented.
- [ ] `matched_count` is reasonable.
- [ ] Unmatched examples are reviewed.
- [ ] Effective coverage is reviewed.
- [ ] App activation remains opt-in.

## Decision

- Candidate provider:
- Payload reviewed:
- Reviewer:
- Date:
- Decision: accept / defer / reject
- Rationale:
- Follow-up actions:
