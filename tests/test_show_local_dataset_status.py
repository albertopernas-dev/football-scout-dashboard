import json

from scripts.show_local_dataset_status import calculate_local_dataset_status
from src.ingestion import load_records_to_sqlite


def _fixtures_payload() -> dict:
    return {
        "response": [
            {"fixture": {"id": 1001}},
            {"fixture": {"id": "1002"}},
            {"fixture": {"id": 1001}},
        ]
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_calculate_local_dataset_status_counts_cached_and_missing(tmp_path):
    fixtures_path = tmp_path / "fixtures.json"
    fixture_players_dir = tmp_path / "fixture_players"
    fixture_players_dir.mkdir()
    _write_json(fixtures_path, _fixtures_payload())
    _write_json(fixture_players_dir / "api_football_fixture_players_1001.json", {"response": []})

    status = calculate_local_dataset_status(
        fixtures_path=fixtures_path,
        fixture_players_dir=fixture_players_dir,
        database_path=tmp_path / "missing.db",
        table_name="players",
    )

    assert status["fixtures_in_fixtures_file"] == 2
    assert status["cached_fixture_player_files"] == 1
    assert status["missing_fixture_player_files"] == 1
    assert status["cached_pct"] == 50.0
    assert status["sqlite_rows"] == 0


def test_calculate_local_dataset_status_handles_missing_sqlite(tmp_path):
    fixtures_path = tmp_path / "fixtures.json"
    _write_json(fixtures_path, {"response": []})

    status = calculate_local_dataset_status(
        fixtures_path=fixtures_path,
        fixture_players_dir=tmp_path / "fixture_players",
        database_path=tmp_path / "missing.db",
        table_name="players",
    )

    assert status["sqlite_source"] == "missing"
    assert status["sqlite_rows"] == 0
    assert status["teams_count"] == 0
    assert status["age_known_pct"] == 0.0


def test_calculate_local_dataset_status_reads_sqlite_quality_metrics(tmp_path):
    fixtures_path = tmp_path / "fixtures.json"
    fixture_players_dir = tmp_path / "fixture_players"
    database_path = tmp_path / "football_scout.db"
    fixture_players_dir.mkdir()
    _write_json(fixtures_path, _fixtures_payload())
    _write_json(fixture_players_dir / "api_football_fixture_players_1001.json", {"response": []})
    _write_json(fixture_players_dir / "api_football_fixture_players_1002.json", {"response": []})
    load_records_to_sqlite(
        [
            {
                "player": "A",
                "team": "T1",
                "league": "LaLiga",
                "position": "Forward",
                "minutes": 90,
                "age": 25,
                "age_known": False,
                "market_value": None,
                "market_value_known": False,
                "contract_end": "",
            },
            {
                "player": "B",
                "team": "T2",
                "league": "LaLiga",
                "position": "Defender",
                "minutes": 45,
                "age": 21,
                "age_known": True,
                "market_value": 1_000_000,
                "market_value_known": True,
                "contract_end": "2026-06-30",
            },
        ],
        database_path,
        "players",
    )

    status = calculate_local_dataset_status(
        fixtures_path=fixtures_path,
        fixture_players_dir=fixture_players_dir,
        database_path=database_path,
        table_name="players",
        league="LaLiga",
        season=2024,
    )

    assert status["league"] == "LaLiga"
    assert status["season"] == 2024
    assert status["sqlite_source"] == "sqlite"
    assert status["sqlite_rows"] == 2
    assert status["teams_count"] == 2
    assert status["leagues_count"] == 1
    assert status["total_minutes"] == 135
    assert status["age_known_pct"] == 50.0
    assert status["market_value_known_pct"] == 50.0
    assert status["contract_known_pct"] == 50.0
