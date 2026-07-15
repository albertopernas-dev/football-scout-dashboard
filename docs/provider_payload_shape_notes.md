# Provider Payload Shape Notes

## Purpose

This document analyses an advanced synthetic payload and describes how its shape could fit the provider fixture -> identity mapping -> canonical Market Context contract.

The sample is entirely synthetic. It does not represent a real provider, contain real data or authorize use of any real payload. A synthetic-only helper supports this documented shape, but no real provider parser has been implemented.

## Synthetic Sample

- [Advanced synthetic provider payload](examples/provider_payload_advanced_sample.json)

## Payload Shape Summary

- `provider` contains provider-level metadata, payload type, terms scope and generation timestamp.
- `competition` contains league identity and season metadata shared by the payload.
- `teams` is an array of provider teams.
- Each team contains a nested `players` array.
- Each player contains an `identity` block for age, birthdate and nationality.
- Each player contains a `market` block for value, currency and value date.
- Each player contains a `contract` block for end date, loan status and option notes.
- Each player contains a `provenance` block for source, URL, confidence and notes.

## Candidate Flattening Strategy

A future transform could iterate through `teams[]` and each nested `players[]`, carrying provider and competition metadata into one normalized record per player.

Expected normalized fields:

- `provider_name` <- `provider.name`
- `provider_player_id` <- `teams[].players[].provider_player_id`
- `provider_team_id` <- `teams[].provider_team_id`
- `provider_league_id` <- `competition.provider_league_id`
- `provider_season` <- `competition.season`
- `provider_player_name` <- `teams[].players[].provider_player_name`
- `provider_team_name` <- `teams[].provider_team_name`
- `age` <- `teams[].players[].identity.age`
- `market_value_eur` <- `teams[].players[].market.market_value` only when currency is EUR
- `contract_end_date` <- `teams[].players[].contract.contract_end_date`
- `source` <- `teams[].players[].provenance.source`
- `source_url` <- `teams[].players[].provenance.source_url`
- `confidence` <- `teams[].players[].provenance.confidence`
- `notes` <- `teams[].players[].provenance.notes`
- `value_date` <- `teams[].players[].market.market_value_date`
- `fetched_at` <- `provider.generated_at`
- `contract_option_notes` <- `teams[].players[].contract.option_notes`
- `license_scope` <- `provider.terms_scope`

## Synthetic Flattening Helper

`src/provider_payload_shapes.py` contains a pure helper for this advanced synthetic shape.

- It only flattens the versioned synthetic example.
- It does not integrate or parse a real provider payload.
- It does not apply identity mapping.
- It does not activate data in the app.
- It performs no network calls.

## Local Synthetic Flattening CLI

`scripts/flatten_provider_payload_advanced_sample.py` writes the advanced synthetic JSON
payload as normalized provider records in a local CSV:

```powershell
.venv\Scripts\python.exe scripts\flatten_provider_payload_advanced_sample.py --input docs\examples\provider_payload_advanced_sample.json --output data\enrichment\provider_payload_advanced_flattened.generated.local.csv --force
```

The output must be a `.local.csv` file inside `data/enrichment/`; generated local files
remain ignored by git. This command performs no identity mapping, canonical Market Context
build, app activation, real provider integration or network access.

## Field Fit Table

| Canonical / Optional Field | Payload Path | Fit | Notes |
|---|---|---|---|
| `provider_name` | `provider.name` | yes | Synthetic provider label. |
| `provider_player_id` | `teams[].players[].provider_player_id` | yes | Required for reviewed identity mapping. |
| `provider_team_id` | `teams[].provider_team_id` | yes | Inherited by nested players. |
| `provider_league_id` | `competition.provider_league_id` | yes | Shared competition context. |
| `provider_season` | `competition.season` | yes | Shared season context. |
| `provider_player_name` | `teams[].players[].provider_player_name` | yes | Provider-facing display name. |
| `provider_team_name` | `teams[].provider_team_name` | yes | Inherited by nested players. |
| `age` | `teams[].players[].identity.age` | partial | Null is allowed and must stay missing. |
| `market_value_eur` | `teams[].players[].market.market_value` | partial | Valid only when currency equals EUR. |
| `contract_end_date` | `teams[].players[].contract.contract_end_date` | partial | Null is allowed; populated values must be ISO dates. |
| `source` | `teams[].players[].provenance.source` | partial | Empty for identity-only rows. |
| `source_url` | `teams[].players[].provenance.source_url` | partial | Uses synthetic `example.test` URLs. |
| `confidence` | `teams[].players[].provenance.confidence` | partial | Must be empty or low, medium or high. |
| `notes` | `teams[].players[].provenance.notes` | yes | Synthetic traceability note. |
| `value_date` | `teams[].players[].market.market_value_date` | partial | Available only when a dated value exists. |
| `fetched_at` | `provider.generated_at` | yes | Shared payload generation timestamp. |
| `contract_option_notes` | `teams[].players[].contract.option_notes` | partial | Optional contract context. |
| `license_scope` | `provider.terms_scope` | yes | Synthetic scope only; not a real license. |

## Validation Considerations

- Null values must remain missing and must not become zero.
- `market_value` maps to `market_value_eur` only when `market_value_currency == "EUR"`.
- Non-EUR values require an explicit currency conversion policy before mapping.
- Contract dates must use ISO `YYYY-MM-DD`.
- Confidence must be empty or one of `low`, `medium` or `high`.
- Source is required when age, value or contract enrichment is present.
- Player, team, league and season identity must pass through reviewed mapping before canonical activation.

## Identity Mapping Considerations

The provider IDs appear sufficient for strong matching in this synthetic shape, but they still require reviewed identity mappings. Matching must remain team- and season-aware, use no fuzzy matching, and reject duplicate provider identities before canonical activation.

## License And Storage Considerations

The synthetic sample can be versioned. Real payloads must remain local and ignored unless their license explicitly permits redistribution. Real experiments should use `data/provider_cache/` or `.local.csv` paths, raw dumps must not enter git, and credentials must never be stored in the repository.

## Decision For This Synthetic Shape

Accepted as a synthetic shape example only. It is not accepted as a real provider integration.

A possible later step is to add a synthetic flattening fixture or parser test. That work would still use no real provider data.
