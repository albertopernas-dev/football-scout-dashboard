import pytest

from src.providers.api_football import ApiFootballClient


def test_api_football_client_rejects_empty_api_key():
    with pytest.raises(ValueError, match="API_FOOTBALL_KEY"):
        ApiFootballClient(api_key="")


def test_get_uses_expected_url_headers_params_and_timeout():
    calls = []

    def requester(url, headers, params, timeout_seconds):
        calls.append(
            {
                "url": url,
                "headers": headers,
                "params": params,
                "timeout_seconds": timeout_seconds,
            }
        )
        return {"response": []}

    client = ApiFootballClient(
        api_key="test-key",
        base_url="https://api.example.test",
        timeout_seconds=7,
        requester=requester,
    )

    payload = client.get("players", params={"league": 39, "season": 2025})

    assert payload == {"response": []}
    assert calls == [
        {
            "url": "https://api.example.test/players",
            "headers": {"x-apisports-key": "test-key"},
            "params": {"league": 39, "season": 2025},
            "timeout_seconds": 7,
        }
    ]


def test_fetch_players_calls_players_endpoint_with_expected_params():
    calls = []

    def requester(url, headers, params, timeout_seconds):
        calls.append({"url": url, "headers": headers, "params": params})
        return {"response": [{"player": {"name": "Player Name"}}]}

    client = ApiFootballClient(
        api_key="test-key",
        base_url="https://api.example.test",
        requester=requester,
    )

    payload = client.fetch_players(league_id=140, season=2024, page=2)

    assert payload == {"response": [{"player": {"name": "Player Name"}}]}
    assert calls == [
        {
            "url": "https://api.example.test/players",
            "headers": {"x-apisports-key": "test-key"},
            "params": {"league": 140, "season": 2024, "page": 2},
        }
    ]


def test_fetch_players_adds_team_param_when_team_id_is_provided():
    calls = []

    def requester(url, headers, params, timeout_seconds):
        calls.append(params)
        return {"response": []}

    client = ApiFootballClient(
        api_key="test-key",
        base_url="https://api.example.test",
        requester=requester,
    )

    client.fetch_players(league_id=140, season=2024, page=1, team_id=541)

    assert calls == [{"league": 140, "season": 2024, "page": 1, "team": 541}]


def test_base_url_trailing_slash_does_not_generate_double_slash():
    calls = []

    def requester(url, headers, params, timeout_seconds):
        calls.append(url)
        return {"response": []}

    client = ApiFootballClient(
        api_key="test-key",
        base_url="https://api.example.test/",
        requester=requester,
    )

    client.get("/players")

    assert calls == ["https://api.example.test/players"]


def test_requester_fake_returns_raw_payload_without_network():
    def requester(url, headers, params, timeout_seconds):
        return {"response": [{"id": 1}], "paging": {"current": 1}}

    client = ApiFootballClient(api_key="test-key", requester=requester)

    assert client.get("players") == {"response": [{"id": 1}], "paging": {"current": 1}}
