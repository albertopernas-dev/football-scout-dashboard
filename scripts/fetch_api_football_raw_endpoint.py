from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import API_FOOTBALL_BASE_URL, API_FOOTBALL_KEY, API_FOOTBALL_TIMEOUT_SECONDS
from src.providers.api_football import ApiFootballClient


DEFAULT_OUTPUT_PATH = Path("data/raw/api_football_raw_endpoint.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch a raw API-Football payload from any endpoint for local inspection."
    )
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--param", action="append", default=None, help="Query parameter in key=value format.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    return parser


def parse_params(param_values: list[str] | None) -> dict[str, object]:
    if not param_values:
        return {}

    params = {}
    for value in param_values:
        if "=" not in value:
            raise ValueError(f"Invalid parameter '{value}'. Use key=value format.")
        key, raw_value = value.split("=", 1)
        if not key:
            raise ValueError("Parameter key cannot be empty.")
        params[key] = _parse_param_value(raw_value)
    return params


def save_json(payload: dict, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return output_path


def count_response_records(payload: dict) -> int | None:
    response = payload.get("response")
    if isinstance(response, list):
        return len(response)
    return None


def _parse_param_value(value: str) -> object:
    try:
        return int(value)
    except ValueError:
        return value


def main() -> None:
    args = build_parser().parse_args()

    if not API_FOOTBALL_KEY:
        raise SystemExit("API_FOOTBALL_KEY is not defined. Set it before fetching API-Football data.")

    try:
        params = parse_params(args.param)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    client = ApiFootballClient(
        api_key=API_FOOTBALL_KEY,
        base_url=API_FOOTBALL_BASE_URL,
        timeout_seconds=API_FOOTBALL_TIMEOUT_SECONDS,
    )
    payload = client.get(args.endpoint, params=params)
    output_path = save_json(payload, args.output)

    print(f"Endpoint: {args.endpoint}")
    print(f"Params: {params}")
    print(f"Output path: {output_path}")
    response_count = count_response_records(payload)
    if response_count is not None:
        print(f"Response records: {response_count}")
    else:
        print("Response records: unknown")
    if isinstance(payload, dict):
        print(f"Top-level keys: {sorted(str(key) for key in payload.keys())}")


if __name__ == "__main__":
    main()
