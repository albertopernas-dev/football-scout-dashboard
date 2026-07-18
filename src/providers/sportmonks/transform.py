from __future__ import annotations

from datetime import datetime, timezone

from src.providers.sportmonks.schema import (
    CANONICAL_OUTPUT_FIELDS,
    DEFAULT_FRESHNESS_BASIS,
    PROVIDER,
    SQUAD_ENDPOINT_PATTERN,
)
from src.providers.sportmonks.validation import (
    validate_no_token_text,
    validate_payload_shape,
    validate_scope,
)


def transform_squad_payload(
    payload: dict,
    *,
    league_id: int,
    expected_team_id: int,
    expected_season_id: int,
    observed_at: str | None = None,
    freshness_basis: str = DEFAULT_FRESHNESS_BASIS,
) -> list[dict]:
    """Transform an already-loaded squad payload into canonical ID-only rows."""
    validated_payload = validate_payload_shape(payload)
    observation_timestamp = observed_at or _utc_timestamp()
    validate_no_token_text(observation_timestamp)
    validate_no_token_text(freshness_basis)
    source_endpoint = SQUAD_ENDPOINT_PATTERN.format(
        season_id=expected_season_id,
        team_id=expected_team_id,
    )

    rows = []
    for record in validated_payload["data"]:
        validate_scope(
            record,
            expected_team_id=expected_team_id,
            expected_season_id=expected_season_id,
        )
        rows.append(
            {
                "provider": PROVIDER,
                "provider_league_id": league_id,
                "provider_season_id": record["season_id"],
                "provider_team_id": record["team_id"],
                "provider_player_id": record["player_id"],
                "provider_position_id": record.get("position_id"),
                "squad_record_id": record.get("id"),
                "jersey_number": record.get("jersey_number"),
                "has_values": record.get("has_values"),
                "source_endpoint": source_endpoint,
                "source_observed_at": observation_timestamp,
                "source_freshness_basis": freshness_basis,
                "source_scope_league_id": league_id,
                "source_scope_season_id": expected_season_id,
                "source_scope_team_id": expected_team_id,
            }
        )
    return rows


def summarize_transformed_rows(rows: list[dict]) -> dict:
    """Return a non-sensitive aggregate summary of transformed rows."""
    first_row = rows[0] if rows else {}
    return {
        "row_count": len(rows),
        "columns": list(first_row) if first_row else list(CANONICAL_OUTPUT_FIELDS),
        "provider": first_row.get("provider"),
        "source_endpoint": first_row.get("source_endpoint"),
        "has_position_ids": sum(
            row.get("provider_position_id") is not None for row in rows
        ),
        "has_jersey_numbers": sum(row.get("jersey_number") is not None for row in rows),
    }


def _utc_timestamp() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
