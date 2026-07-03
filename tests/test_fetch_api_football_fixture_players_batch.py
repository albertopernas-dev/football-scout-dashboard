import json

import pytest


def _fixtures_payload() -> dict:
    return {
        "response": [
            {"fixture": {"id": 1001, "status": {"short": "FT"}}},
            {"fixture": {"id": "1002", "status": {"short": "AET"}}},
            {"fixture": {"id": 1001, "status": {"short": "FT"}}},
            {"fixture": {"id": 1003, "status": {"short": "NS"}}},
        ]
    }


def test_extract_fixture_ids_extracts_ids_in_order():
    from scripts.fetch_api_football_fixture_players_batch import extract_fixture_ids

    assert extract_fixture_ids({"response": [{"fixture": {"id": 3}}, {"fixture": {"id": "4"}}]}) == [3, 4]


def test_extract_fixture_ids_removes_duplicates():
    from scripts.fetch_api_football_fixture_players_batch import extract_fixture_ids

    assert extract_fixture_ids(_fixtures_payload()) == [1001, 1002, 1003]


def test_extract_fixture_ids_filters_by_status():
    from scripts.fetch_api_football_fixture_players_batch import extract_fixture_ids

    assert extract_fixture_ids(_fixtures_payload(), statuses={"FT", "AET"}) == [1001, 1002]


def test_load_fixtures_payload_fails_when_file_missing(tmp_path):
    from scripts.fetch_api_football_fixture_players_batch import load_fixtures_payload

    with pytest.raises(SystemExit, match="Fixtures file not found"):
        load_fixtures_payload(tmp_path / "missing.json")


def test_load_fixtures_payload_fails_when_json_invalid(tmp_path):
    from scripts.fetch_api_football_fixture_players_batch import load_fixtures_payload

    path = tmp_path / "fixtures.json"
    path.write_text("{bad", encoding="utf-8")

    with pytest.raises(SystemExit, match="Fixtures file is not valid JSON"):
        load_fixtures_payload(path)


def test_resolve_download_plan_skips_cached_without_force_and_applies_limit(tmp_path):
    from scripts.fetch_api_football_fixture_players_batch import resolve_download_plan

    output_dir = tmp_path / "fixture_players"
    output_dir.mkdir()
    (output_dir / "api_football_fixture_players_1001.json").write_text("{}", encoding="utf-8")

    plan = resolve_download_plan([1001, 1002, 1003, 1004], output_dir, limit=2, force=False)

    assert [item.fixture_id for item in plan.cached] == [1001]
    assert [item.fixture_id for item in plan.to_download] == [1002, 1003]
    assert plan.pending_before_limit == 3
    assert plan.remaining_after_plan == 1


def test_resolve_download_plan_includes_cached_with_force(tmp_path):
    from scripts.fetch_api_football_fixture_players_batch import resolve_download_plan

    output_dir = tmp_path / "fixture_players"
    output_dir.mkdir()
    (output_dir / "api_football_fixture_players_1001.json").write_text("{}", encoding="utf-8")

    plan = resolve_download_plan([1001, 1002], output_dir, limit=10, force=True)

    assert [item.fixture_id for item in plan.cached] == [1001]
    assert [item.fixture_id for item in plan.to_download] == [1001, 1002]


def test_resolve_download_plan_with_force_counts_all_fixtures_as_pending(tmp_path):
    from scripts.fetch_api_football_fixture_players_batch import resolve_download_plan

    output_dir = tmp_path / "fixture_players"
    output_dir.mkdir()
    (output_dir / "api_football_fixture_players_1001.json").write_text("{}", encoding="utf-8")

    plan = resolve_download_plan([1001, 1002], output_dir, limit=1, force=True)

    assert [item.fixture_id for item in plan.cached] == [1001]
    assert [item.fixture_id for item in plan.to_download] == [1001]
    assert plan.pending_before_limit == 2
    assert plan.remaining_after_plan == 1


def test_output_path_for_fixture_uses_expected_name(tmp_path):
    from scripts.fetch_api_football_fixture_players_batch import output_path_for_fixture

    assert output_path_for_fixture(tmp_path, 1208494) == tmp_path / "api_football_fixture_players_1208494.json"


def test_dry_run_does_not_call_client_or_create_files(tmp_path):
    from scripts.fetch_api_football_fixture_players_batch import fetch_fixture_players_batch

    class FakeClient:
        def get(self, endpoint, params=None):
            raise AssertionError("client should not be called in dry-run")

    summary = fetch_fixture_players_batch(
        fixture_ids=[1001, 1002],
        output_dir=tmp_path / "fixture_players",
        limit=1,
        client=FakeClient(),
        dry_run=True,
    )

    assert summary["planned_downloads"] == 1
    assert summary["pending_before_limit"] == 2
    assert summary["remaining_after_plan"] == 1
    assert summary["total_covered_after_run"] == 1
    assert summary["downloaded"] == 0
    assert summary["dry_run"] is True
    assert not (tmp_path / "fixture_players").exists()


def test_batch_fetch_with_fake_client_creates_expected_json_files(tmp_path):
    from scripts.fetch_api_football_fixture_players_batch import fetch_fixture_players_batch

    calls = []

    class FakeClient:
        def get(self, endpoint, params=None):
            calls.append({"endpoint": endpoint, "params": params})
            return {"response": [{"fixture": params["fixture"]}]}

    summary = fetch_fixture_players_batch(
        fixture_ids=[1001, 1002],
        output_dir=tmp_path / "fixture_players",
        limit=10,
        client=FakeClient(),
    )

    assert calls == [
        {"endpoint": "fixtures/players", "params": {"fixture": 1001}},
        {"endpoint": "fixtures/players", "params": {"fixture": 1002}},
    ]
    assert summary["pending_before_limit"] == 2
    assert summary["remaining_after_plan"] == 0
    assert summary["total_covered_after_run"] == 2
    assert summary["downloaded"] == 2
    first = tmp_path / "fixture_players" / "api_football_fixture_players_1001.json"
    second = tmp_path / "fixture_players" / "api_football_fixture_players_1002.json"
    assert json.loads(first.read_text(encoding="utf-8")) == {"response": [{"fixture": 1001}]}
    assert json.loads(second.read_text(encoding="utf-8")) == {"response": [{"fixture": 1002}]}
