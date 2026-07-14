# Provider Identity Mapping Plan

## Purpose

Provider identity mapping avoids silent fuzzy matching and makes each enriched row traceable. The mapping layer should explain how provider IDs and names connect to local `player`, `team`, `league` and `season` keys before any provider-derived row enters canonical Market Context.

## Mapping Levels

1. Strong match:
   - `provider_player_id` + `provider_team_id` + `provider_name` + season.
2. Reviewed identity match:
   - manually reviewed `player` + `team` + `league` + `season`.
3. Rejected or ambiguous:
   - duplicate names;
   - uncertain team or season;
   - missing provider ID when one should exist.

## Proposed Mapping Schema

| Column | Purpose |
|---|---|
| `provider_name` | Provider or source label. |
| `provider_player_id` | Provider player identifier. |
| `provider_team_id` | Provider team identifier. |
| `provider_league_id` | Provider league or competition identifier. |
| `provider_season` | Provider season key. |
| `local_player` | Local player display name. |
| `local_team` | Local team display name. |
| `local_league` | Local league display name. |
| `local_season` | Local season key. |
| `match_status` | Mapping status. |
| `confidence` | Review confidence. |
| `reviewed_by` | Reviewer label. |
| `reviewed_at` | Review date. |
| `notes` | Review notes. |

Suggested `match_status` values:

- `matched`
- `unmatched`
- `ambiguous`
- `rejected`

Suggested `confidence` values:

- `low`
- `medium`
- `high`

## Rules

- No automatic fuzzy matching without review.
- No silent name-only match.
- Mapping must be season-aware.
- The same `provider_player_id` can have multiple teams by season, but the same local player/team/season should not be duplicated without review.
- `ambiguous` and `rejected` rows must not enter the canonical builder.
- Any real mapping must remain local unless license explicitly allows versioning.

## Synthetic Example

See [`docs/examples/provider_identity_mapping_sample.csv`](examples/provider_identity_mapping_sample.csv).

## Implementation

`src/provider_identity_mapping.py` validates the mapping contract but does not apply mappings to provider fixtures yet.

Main functions:

- `required_provider_identity_mapping_columns()`
- `validate_provider_identity_mapping_schema(df)`
- `validate_provider_identity_mapping_values(df)`
- `validate_provider_identity_mapping_df(df)`
- `split_provider_identity_mapping_by_status(df)`
- `find_duplicate_provider_identity_mappings(df)`
- `load_provider_identity_mapping_csv(path)`

## Future Implementation Notes

Future helper ideas:

- apply reviewed mapping to normalized provider fixtures.

Future tests should use synthetic fixtures only.
