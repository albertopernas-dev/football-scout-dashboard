from copy import deepcopy
from pathlib import Path

import pandas as pd
import pytest

from src.provider_payload_shapes import (
    expected_advanced_payload_columns,
    flatten_advanced_synthetic_provider_payload,
    load_json_payload,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ADVANCED_PAYLOAD_SAMPLE = (
    PROJECT_ROOT / "docs" / "examples" / "provider_payload_advanced_sample.json"
)


def test_load_json_payload_reads_object():
    payload = load_json_payload(ADVANCED_PAYLOAD_SAMPLE)

    assert isinstance(payload, dict)
    assert payload["provider"]["name"] == "Synthetic Advanced Provider"


def _minimal_payload() -> dict:
    return {
        "provider": {
            "name": "Synthetic Provider",
            "payload_type": "player_market_context_snapshot",
            "terms_scope": "synthetic_example_only",
            "generated_at": "2026-01-01T00:00:00Z",
        },
        "competition": {
            "provider_league_id": "synthetic-league",
            "provider_league_name": "Synthetic League",
            "season": 2024,
        },
        "teams": [
            {
                "provider_team_id": "synthetic-team",
                "provider_team_name": "Synthetic Team",
                "players": [
                    {
                        "provider_player_id": "synthetic-player",
                        "provider_player_name": "Synthetic Player",
                        "identity": {
                            "birthdate": None,
                            "age": None,
                            "nationality": "Synthetic Country",
                        },
                        "market": {
                            "market_value": None,
                            "market_value_currency": "EUR",
                            "market_value_date": None,
                        },
                        "contract": {
                            "contract_end_date": None,
                            "loan_status": None,
                            "option_notes": None,
                        },
                        "provenance": {
                            "source": "",
                            "source_url": "",
                            "confidence": "",
                            "notes": "",
                        },
                    }
                ],
            }
        ],
    }


def test_load_json_payload_rejects_non_object_root(tmp_path):
    input_path = tmp_path / "payload.json"
    input_path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="root must be an object"):
        load_json_payload(input_path)


def test_flatten_advanced_synthetic_provider_payload_returns_expected_rows_and_columns():
    payload = load_json_payload(ADVANCED_PAYLOAD_SAMPLE)

    result = flatten_advanced_synthetic_provider_payload(payload)

    assert len(result) == 3
    assert result.columns.tolist() == expected_advanced_payload_columns()
    assert result["provider_player_id"].tolist() == [
        "synthetic-player-alpha",
        "synthetic-player-beta",
        "synthetic-player-gamma",
    ]


def test_flatten_maps_enriched_eur_market_value():
    payload = load_json_payload(ADVANCED_PAYLOAD_SAMPLE)

    result = flatten_advanced_synthetic_provider_payload(payload)
    beta = result.loc[result["provider_player_id"] == "synthetic-player-beta"].iloc[0]

    assert beta["market_value_eur"] == 1500000
    assert beta["contract_end_date"] == "2027-06-30"
    assert beta["confidence"] == "medium"


def test_flatten_keeps_missing_values_missing():
    payload = load_json_payload(ADVANCED_PAYLOAD_SAMPLE)

    result = flatten_advanced_synthetic_provider_payload(payload)
    alpha = result.loc[result["provider_player_id"] == "synthetic-player-alpha"].iloc[0]

    assert pd.isna(alpha["market_value_eur"])
    assert pd.isna(alpha["age"])
    assert alpha["source"] == ""


def test_flatten_non_eur_market_value_does_not_populate_market_value_eur():
    payload = _minimal_payload()
    market = payload["teams"][0]["players"][0]["market"]
    market["market_value"] = 999
    market["market_value_currency"] = "GBP"

    result = flatten_advanced_synthetic_provider_payload(payload)

    assert pd.isna(result.loc[0, "market_value_eur"])
    assert result.loc[0, "market_value_currency"] == "GBP"


def test_flatten_empty_teams_returns_empty_dataframe_with_columns():
    payload = _minimal_payload()
    payload["teams"] = []

    result = flatten_advanced_synthetic_provider_payload(payload)

    assert result.empty
    assert result.columns.tolist() == expected_advanced_payload_columns()


def test_flatten_empty_players_list_is_allowed():
    payload = _minimal_payload()
    payload["teams"][0]["players"] = []

    result = flatten_advanced_synthetic_provider_payload(payload)

    assert result.empty
    assert result.columns.tolist() == expected_advanced_payload_columns()


def test_flatten_does_not_mutate_payload():
    payload = load_json_payload(ADVANCED_PAYLOAD_SAMPLE)
    original = deepcopy(payload)

    flatten_advanced_synthetic_provider_payload(payload)

    assert payload == original


def test_flatten_rejects_missing_provider_section():
    payload = _minimal_payload()
    del payload["provider"]

    with pytest.raises(ValueError, match="provider"):
        flatten_advanced_synthetic_provider_payload(payload)


def test_flatten_rejects_missing_competition_section():
    payload = _minimal_payload()
    del payload["competition"]

    with pytest.raises(ValueError, match="competition"):
        flatten_advanced_synthetic_provider_payload(payload)


def test_flatten_rejects_non_list_teams():
    payload = _minimal_payload()
    payload["teams"] = {}

    with pytest.raises(ValueError, match="teams must be a list"):
        flatten_advanced_synthetic_provider_payload(payload)


def test_flatten_rejects_non_list_players():
    payload = _minimal_payload()
    payload["teams"][0]["players"] = {}

    with pytest.raises(ValueError, match="players must be a list"):
        flatten_advanced_synthetic_provider_payload(payload)


@pytest.mark.parametrize(
    ("section", "field"),
    [
        ("competition", "provider_league_id"),
        ("competition", "season"),
        ("team", "provider_team_id"),
        ("player", "provider_player_id"),
    ],
)
def test_flatten_rejects_missing_required_identity_field(section, field):
    payload = _minimal_payload()
    target = {
        "competition": payload["competition"],
        "team": payload["teams"][0],
        "player": payload["teams"][0]["players"][0],
    }[section]
    del target[field]

    with pytest.raises(ValueError, match=field):
        flatten_advanced_synthetic_provider_payload(payload)
