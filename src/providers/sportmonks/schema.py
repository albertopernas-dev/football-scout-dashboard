from __future__ import annotations


PROVIDER = "sportmonks"
SQUAD_ENDPOINT_PATTERN = "/football/squads/seasons/{season_id}/teams/{team_id}"
DEFAULT_FRESHNESS_BASIS = "local_cache_observation_time"

REQUIRED_RECORD_FIELDS = [
    "player_id",
    "team_id",
    "season_id",
]

OPTIONAL_RECORD_FIELDS = [
    "id",
    "position_id",
    "jersey_number",
    "has_values",
]

EXPECTED_RECORD_FIELDS = [
    "id",
    "player_id",
    "team_id",
    "season_id",
    "position_id",
    "jersey_number",
    "has_values",
]

CANONICAL_OUTPUT_FIELDS = [
    "provider",
    "provider_league_id",
    "provider_season_id",
    "provider_team_id",
    "provider_player_id",
    "provider_position_id",
    "squad_record_id",
    "jersey_number",
    "has_values",
    "source_endpoint",
    "source_observed_at",
    "source_freshness_basis",
    "source_scope_league_id",
    "source_scope_season_id",
    "source_scope_team_id",
]
