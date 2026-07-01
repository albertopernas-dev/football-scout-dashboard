from __future__ import annotations

import json
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from src.config import API_FOOTBALL_BASE_URL, API_FOOTBALL_TIMEOUT_SECONDS


Requester = Callable[[str, dict[str, str], dict | None, int], dict]


class ApiFootballClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = API_FOOTBALL_BASE_URL,
        timeout_seconds: int = API_FOOTBALL_TIMEOUT_SECONDS,
        requester: Requester | None = None,
    ):
        if not api_key:
            raise ValueError("API_FOOTBALL_KEY is required to use ApiFootballClient.")

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.requester = requester or _default_requester

    def get(self, endpoint: str, params: dict | None = None) -> dict:
        clean_endpoint = endpoint.strip("/")
        url = f"{self.base_url}/{clean_endpoint}"
        headers = {"x-apisports-key": self.api_key}
        return self.requester(url, headers, params, self.timeout_seconds)

    def fetch_players(self, league_id: int, season: int, page: int = 1) -> dict:
        return self.get(
            "players",
            params={
                "league": league_id,
                "season": season,
                "page": page,
            },
        )


def _default_requester(url: str, headers: dict[str, str], params: dict | None, timeout_seconds: int) -> dict:
    query = urlencode(params or {})
    request_url = f"{url}?{query}" if query else url
    request = Request(request_url, headers=headers, method="GET")

    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8")
    except HTTPError as exc:
        raise RuntimeError(f"API-Football HTTP error {exc.code}: {exc.reason}") from exc
    except URLError as exc:
        raise RuntimeError(f"API-Football request failed: {exc.reason}") from exc

    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError("API-Football response is not valid JSON.") from exc

    if not isinstance(payload, dict):
        raise ValueError("API-Football response must be a JSON object.")

    return payload
