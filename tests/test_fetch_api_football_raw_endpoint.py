import json

import pytest

from scripts import fetch_api_football_raw_endpoint
from scripts.fetch_api_football_raw_endpoint import (
    count_response_records,
    main,
    parse_params,
    save_json,
)


def test_parse_params_converts_integer_values():
    assert parse_params(["league=140", "season=2024", "team=541"]) == {
        "league": 140,
        "season": 2024,
        "team": 541,
    }


def test_parse_params_keeps_string_values():
    assert parse_params(["name=Real Madrid", "endpoint=players"]) == {
        "name": "Real Madrid",
        "endpoint": "players",
    }


def test_parse_params_returns_empty_dict_for_none_or_empty_list():
    assert parse_params(None) == {}
    assert parse_params([]) == {}


def test_parse_params_rejects_values_without_equals():
    with pytest.raises(ValueError, match="key=value"):
        parse_params(["league"])


def test_parse_params_rejects_empty_key():
    with pytest.raises(ValueError, match="Parameter key cannot be empty"):
        parse_params(["=140"])


def test_save_json_creates_parent_directory_and_preserves_payload(tmp_path):
    output_path = tmp_path / "raw" / "payload.json"
    payload = {"response": [{"player": "José"}]}

    saved_path = save_json(payload, output_path)

    assert saved_path == output_path
    assert json.loads(output_path.read_text(encoding="utf-8")) == payload


def test_count_response_records_returns_length_only_for_response_list():
    assert count_response_records({"response": [1, 2]}) == 2
    assert count_response_records({"response": {"item": 1}}) is None
    assert count_response_records({}) is None


def test_main_exits_when_api_key_is_empty_and_does_not_create_output(tmp_path, monkeypatch):
    output_path = tmp_path / "payload.json"
    monkeypatch.setattr(fetch_api_football_raw_endpoint, "API_FOOTBALL_KEY", "")
    monkeypatch.setattr(
        "sys.argv",
        [
            "fetch_api_football_raw_endpoint.py",
            "--endpoint",
            "players",
            "--param",
            "league=140",
            "--output",
            str(output_path),
        ],
    )

    with pytest.raises(SystemExit, match="API_FOOTBALL_KEY"):
        main()

    assert not output_path.exists()


def test_main_calls_client_with_endpoint_and_params_without_real_network(tmp_path, monkeypatch):
    output_path = tmp_path / "payload.json"
    calls = []

    class FakeClient:
        def __init__(self, api_key, base_url, timeout_seconds):
            calls.append(
                {
                    "api_key": api_key,
                    "base_url": base_url,
                    "timeout_seconds": timeout_seconds,
                }
            )

        def get(self, endpoint, params=None):
            calls.append({"endpoint": endpoint, "params": params})
            return {"response": [{"id": 1}], "results": 1}

    monkeypatch.setattr(fetch_api_football_raw_endpoint, "API_FOOTBALL_KEY", "test-key")
    monkeypatch.setattr(fetch_api_football_raw_endpoint, "ApiFootballClient", FakeClient)
    monkeypatch.setattr(
        "sys.argv",
        [
            "fetch_api_football_raw_endpoint.py",
            "--endpoint",
            "players",
            "--param",
            "league=140",
            "--param",
            "name=Real Madrid",
            "--output",
            str(output_path),
        ],
    )

    main()

    assert calls[-1] == {"endpoint": "players", "params": {"league": 140, "name": "Real Madrid"}}
    assert json.loads(output_path.read_text(encoding="utf-8")) == {
        "response": [{"id": 1}],
        "results": 1,
    }
