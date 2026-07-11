# Provider To Market Context Transform Plan

## Objective

Define the future contract for transforming provider data into the existing Market Context Layer.

The app should consume validated market context data, not provider payloads. Provider-specific data must be transformed into a canonical local artifact, validated, diagnosed and activated explicitly.

## Input Assumptions

- Provider data may arrive as API JSON, CSV export or another structured local file.
- Provider terms must allow the intended local use before any fetch/cache work.
- Raw provider data may have provider-specific IDs, names, dates and field semantics.
- Some providers may cover only partial market context.
- Some providers may be useful only for manual review or validation.

## Current Canonical Schema

The minimum output remains:

```text
player,team,league,season,age,market_value_eur,contract_end_date,source,source_url,confidence,notes
```

This schema feeds the existing Market Context Layer.

`src/provider_market_context.py` defines generic helpers to build canonical rows from already-normalized provider records. It does not implement any real provider. Future adapters should use synthetic test data, call these helpers, then pass output through validation and diagnostics before activation.

## Future Optional Fields

Future provider-specific fields may be added only if a decision record justifies them:

```text
provider_player_id
provider_team_id
provider_name
fetched_at
value_date
contract_option_notes
license_scope
```

These fields are optional proposals and should not be required for the current app workflow.

## Transform Stages

1. Load raw/cache.
2. Normalize provider entities.
3. Map IDs and names.
4. Build canonical rows.
5. Assign `source`, `confidence` and `notes`.
6. Run validation.
7. Run diagnostics.
8. Activate explicitly.

## Matching Strategy

Preferred matching order:

1. Provider IDs if mapped to local player/team identities.
2. Reviewed `player` / `team` / `league` / `season` keys.
3. Manual review for ambiguous cases.

Rules:

- ambiguous matches should be rejected or marked low confidence;
- fuzzy matching should not silently attach data;
- team changes and loan moves require explicit review;
- original provider names should be preserved in diagnostics when useful;
- matching decisions should be auditable.

## Validation Strategy

Use existing Market Context Layer validation rules:

- `age` is empty or an integer between 15 and 45;
- `market_value_eur` is empty or a positive number;
- `contract_end_date` is empty or strict ISO `YYYY-MM-DD`;
- `source` is required when any enrichment value is present;
- `confidence` is required when any enrichment value is present;
- `confidence` must be `low`, `medium` or `high`;
- identity-only rows remain valid.

Provider transforms should not invent values to pass validation.

## Diagnostics Strategy

Diagnostics should report:

- row count;
- validation errors;
- duplicate keys;
- matched and unmatched rows;
- age coverage;
- market value coverage;
- contract coverage;
- effective coverage;
- source breakdown;
- examples for manual review.

Diagnostics are required before any provider-derived file is activated in the app.

`scripts/preview_provider_market_context.py` can validate and preview local canonical CSV outputs before deeper diagnostics or app activation.

## Failure Handling

- Missing license confirmation blocks prototype work.
- Missing required source/provenance blocks canonical output.
- Missing target fields means the provider should be marked partial or rejected for that use case.
- Invalid dates or values fail validation.
- Ambiguous identity matches should be rejected or marked low confidence.
- Low coverage keeps Opportunity Finder warnings.
- Provider request failures should not break the app because the app consumes local validated data.

## Auditability

Every canonical row should make review possible through:

- source;
- source URL or provider reference;
- confidence;
- notes;
- value date when available;
- fetched date when available;
- provider ID when available and permitted.

The transform should leave enough evidence to understand where each field came from without committing restricted provider payloads.

## Testing Strategy

When transforms are implemented:

- use synthetic raw payload fixtures only;
- do not use real provider dumps in tests;
- unit test provider-specific field mapping;
- unit test invalid and missing values;
- unit test ambiguous matches;
- unit test canonical output validation;
- unit test diagnostics;
- verify that provider code does not require network calls in tests.

## Non-goals

- No scraping.
- No direct app-to-provider runtime calls.
- No committing raw provider payloads.
- No committing restricted real provider data.
- No replacing general sporting scoring.
- No automatic transfer recommendations.
- No silent fallback from missing market data to invented defaults.
