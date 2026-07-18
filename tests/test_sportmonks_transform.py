from __future__ import annotations

import ast
import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from src.providers.sportmonks.schema import CANONICAL_OUTPUT_FIELDS
from src.providers.sportmonks.transform import (
    summarize_transformed_rows,
    transform_squad_payload,
)
from src.providers.sportmonks.validation import (
    SportmonksValidationError,
    validate_no_token_text,
    validate_safe_input_path,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    PROJECT_ROOT / "tests" / "fixtures" / "sportmonks_squad_shape_minimal.json"
)
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "preview_sportmonks_squad_transform.py"


def _load_fixture() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _transform(payload: dict) -> list[dict]:
    return transform_squad_payload(
        payload,
        league_id=271,
        expected_team_id=85,
        expected_season_id=27897,
        observed_at="2026-07-18T12:00:00Z",
    )


def test_transform_rejects_non_object_payload():
    with pytest.raises(SportmonksValidationError, match="object"):
        transform_squad_payload(
            [],
            league_id=271,
            expected_team_id=85,
            expected_season_id=27897,
        )


def test_transform_requires_data_list():
    with pytest.raises(SportmonksValidationError, match="data.*list"):
        _transform({"data": {}})


def test_transform_maps_required_ids():
    rows = _transform(_load_fixture())

    assert len(rows) == 2
    assert list(rows[0]) == CANONICAL_OUTPUT_FIELDS
    assert rows[0]["provider_league_id"] == 271
    assert rows[0]["provider_season_id"] == 27897
    assert rows[0]["provider_team_id"] == 85
    assert rows[0]["provider_player_id"] == 10001
    assert rows[0]["squad_record_id"] == 1


def test_transform_rejects_wrong_team_scope():
    payload = copy.deepcopy(_load_fixture())
    payload["data"][0]["team_id"] = 999

    with pytest.raises(SportmonksValidationError, match="team_id"):
        _transform(payload)


def test_transform_rejects_wrong_season_scope():
    payload = copy.deepcopy(_load_fixture())
    payload["data"][0]["season_id"] = 999

    with pytest.raises(SportmonksValidationError, match="season_id"):
        _transform(payload)


def test_transform_adds_provenance_fields():
    row = _transform(_load_fixture())[0]

    assert row["provider"] == "sportmonks"
    assert row["source_endpoint"] == "/football/squads/seasons/27897/teams/85"
    assert row["source_observed_at"] == "2026-07-18T12:00:00Z"
    assert row["source_freshness_basis"] == "local_cache_observation_time"
    assert row["source_scope_league_id"] == 271
    assert row["source_scope_season_id"] == 27897
    assert row["source_scope_team_id"] == 85


def test_transform_allows_missing_labels_in_id_only_mode():
    row = _transform(_load_fixture())[1]

    assert "player" not in row
    assert row["provider_position_id"] is None
    assert row["jersey_number"] is None


def test_transform_does_not_require_token(monkeypatch):
    monkeypatch.delenv("SPORTMONKS_API_TOKEN", raising=False)

    rows = _transform(_load_fixture())

    assert len(rows) == 2


def test_preview_script_requires_explicit_input_path():
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--league-id",
            "271",
            "--team-id",
            "85",
            "--season-id",
            "27897",
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "--input" in result.stderr


def test_no_real_provider_payload_in_fixtures():
    fixture_text = FIXTURE_PATH.read_text(encoding="utf-8")
    payload = json.loads(fixture_text)

    assert "player_name" not in fixture_text.lower()
    assert "sportmonks_api_token" not in fixture_text.lower()
    assert "api_token" not in fixture_text.lower()
    assert [record["player_id"] for record in payload["data"]] == [10001, 10002]


def test_preview_prints_only_non_sensitive_summary():
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--input",
            str(FIXTURE_PATH),
            "--league-id",
            "271",
            "--team-id",
            "85",
            "--season-id",
            "27897",
            "--observed-at",
            "2026-07-18T12:00:00Z",
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "row_count: 2" in result.stdout
    assert "provider: sportmonks" in result.stdout
    assert "10001" not in result.stdout
    assert "10002" not in result.stdout


def test_summary_contains_aggregate_counts_only():
    summary = summarize_transformed_rows(_transform(_load_fixture()))

    assert summary == {
        "row_count": 2,
        "columns": CANONICAL_OUTPUT_FIELDS,
        "provider": "sportmonks",
        "source_endpoint": "/football/squads/seasons/27897/teams/85",
        "has_position_ids": 1,
        "has_jersey_numbers": 1,
    }


def test_safe_input_path_rejects_env_and_accepts_explicit_fixture():
    with pytest.raises(SportmonksValidationError):
        validate_safe_input_path(PROJECT_ROOT / ".env")

    assert validate_safe_input_path(FIXTURE_PATH) == FIXTURE_PATH


@pytest.mark.parametrize(
    "unsafe_text",
    [
        "SPORTMONKS_API_TOKEN=value",
        "api_token=value",
        "Authorization: Bearer secret",
    ],
)
def test_token_text_is_rejected(unsafe_text):
    with pytest.raises(SportmonksValidationError):
        validate_no_token_text(unsafe_text)


def test_scaffold_has_no_network_imports():
    paths = [
        PROJECT_ROOT / "src" / "providers" / "sportmonks" / "__init__.py",
        PROJECT_ROOT / "src" / "providers" / "sportmonks" / "schema.py",
        PROJECT_ROOT / "src" / "providers" / "sportmonks" / "validation.py",
        PROJECT_ROOT / "src" / "providers" / "sportmonks" / "transform.py",
        SCRIPT_PATH,
    ]
    forbidden_roots = {"requests", "httpx", "aiohttp", "urllib"}

    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported_roots = {
            node.names[0].name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
        }
        imported_roots.update(
            node.module.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        )
        assert imported_roots.isdisjoint(forbidden_roots)
