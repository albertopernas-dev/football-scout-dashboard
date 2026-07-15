from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pandas as pd


_ADVANCED_PAYLOAD_COLUMNS = [
    "provider_name",
    "provider_payload_type",
    "provider_terms_scope",
    "fetched_at",
    "provider_league_id",
    "provider_league_name",
    "provider_season",
    "provider_team_id",
    "provider_team_name",
    "provider_player_id",
    "provider_player_name",
    "age",
    "birthdate",
    "nationality",
    "market_value_eur",
    "market_value_currency",
    "market_value_date",
    "contract_end_date",
    "loan_status",
    "contract_option_notes",
    "source",
    "source_url",
    "confidence",
    "notes",
    "license_scope",
]


def expected_advanced_payload_columns() -> list[str]:
    return list(_ADVANCED_PAYLOAD_COLUMNS)


def load_json_payload(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as payload_file:
        payload = json.load(payload_file)

    if not isinstance(payload, dict):
        raise ValueError("JSON payload root must be an object.")

    return payload


def flatten_advanced_synthetic_provider_payload(
    payload: Mapping[str, Any],
) -> pd.DataFrame:
    if not isinstance(payload, Mapping):
        raise ValueError("Payload must be an object.")

    provider = _required_mapping(payload, "provider")
    competition = _required_mapping(payload, "competition")

    teams = payload.get("teams")
    if teams is None:
        raise ValueError("Payload is missing required section: teams.")
    if not isinstance(teams, list):
        raise ValueError("Payload teams must be a list.")

    provider_league_id = _required_identity_value(
        competition,
        "provider_league_id",
        "competition",
    )
    provider_season = _required_identity_value(
        competition,
        "season",
        "competition",
    )

    records: list[dict[str, Any]] = []
    for team_index, team in enumerate(teams):
        if not isinstance(team, Mapping):
            raise ValueError(f"Team at index {team_index} must be an object.")

        provider_team_id = _required_identity_value(
            team,
            "provider_team_id",
            f"team at index {team_index}",
        )
        players = team.get("players")
        if not isinstance(players, list):
            raise ValueError(f"Team at index {team_index} players must be a list.")

        for player_index, player in enumerate(players):
            if not isinstance(player, Mapping):
                raise ValueError(
                    f"Player at team index {team_index}, player index "
                    f"{player_index} must be an object."
                )

            provider_player_id = _required_identity_value(
                player,
                "provider_player_id",
                f"player at team index {team_index}, player index {player_index}",
            )
            identity = _optional_mapping(player, "identity", player_index)
            market = _optional_mapping(player, "market", player_index)
            contract = _optional_mapping(player, "contract", player_index)
            provenance = _optional_mapping(player, "provenance", player_index)

            market_currency = market.get("market_value_currency")
            market_value_eur = (
                market.get("market_value") if market_currency == "EUR" else None
            )

            records.append(
                {
                    "provider_name": provider.get("name"),
                    "provider_payload_type": provider.get("payload_type"),
                    "provider_terms_scope": provider.get("terms_scope"),
                    "fetched_at": provider.get("generated_at"),
                    "provider_league_id": provider_league_id,
                    "provider_league_name": competition.get("provider_league_name"),
                    "provider_season": provider_season,
                    "provider_team_id": provider_team_id,
                    "provider_team_name": team.get("provider_team_name"),
                    "provider_player_id": provider_player_id,
                    "provider_player_name": player.get("provider_player_name"),
                    "age": identity.get("age"),
                    "birthdate": identity.get("birthdate"),
                    "nationality": identity.get("nationality"),
                    "market_value_eur": market_value_eur,
                    "market_value_currency": market_currency,
                    "market_value_date": market.get("market_value_date"),
                    "contract_end_date": contract.get("contract_end_date"),
                    "loan_status": contract.get("loan_status"),
                    "contract_option_notes": contract.get("option_notes"),
                    "source": provenance.get("source"),
                    "source_url": provenance.get("source_url"),
                    "confidence": provenance.get("confidence"),
                    "notes": provenance.get("notes"),
                    "license_scope": provider.get("terms_scope"),
                }
            )

    return pd.DataFrame(records, columns=_ADVANCED_PAYLOAD_COLUMNS)


def _required_mapping(payload: Mapping[str, Any], section: str) -> Mapping[str, Any]:
    value = payload.get(section)
    if value is None:
        raise ValueError(f"Payload is missing required section: {section}.")
    if not isinstance(value, Mapping):
        raise ValueError(f"Payload section {section} must be an object.")
    return value


def _required_identity_value(
    container: Mapping[str, Any],
    field: str,
    context: str,
) -> Any:
    value = container.get(field)
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValueError(f"Missing required identity field {field} in {context}.")
    return value


def _optional_mapping(
    player: Mapping[str, Any],
    section: str,
    player_index: int,
) -> Mapping[str, Any]:
    value = player.get(section)
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ValueError(
            f"Player at index {player_index} section {section} must be an object."
        )
    return value
