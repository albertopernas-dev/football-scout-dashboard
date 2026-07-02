import json

import pytest

from src.data_sources import load_players_from_sqlite


def _fixture_payload(player_id: int, player: str, team: str, fixture_id: int = 1001) -> dict:
    return {
        "parameters": {"fixture": str(fixture_id)},
        "response": [
            {
                "team": {"id": 10, "name": team},
                "players": [
                    {
                        "player": {"id": player_id, "name": player, "photo": None},
                        "statistics": [
                            {
                                "games": {
                                    "minutes": 90,
                                    "position": "F",
                                    "rating": "7.5",
                                    "substitute": False,
                                },
                                "goals": {"total": 1, "assists": 0},
                                "shots": {"total": 3},
                                "passes": {"total": 22, "key": 2},
                                "duels": {"won": 5},
                                "tackles": {"interceptions": 1},
                            }
                        ],
                    }
                ],
            }
        ],
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_resolve_input_paths_accepts_repeated_inputs(tmp_path):
    from scripts.build_api_football_sqlite_from_fixture_players import resolve_input_paths

    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    first.write_text("{}", encoding="utf-8")
    second.write_text("{}", encoding="utf-8")

    assert resolve_input_paths([first, second], None) == [first, second]


def test_resolve_input_paths_accepts_input_glob(tmp_path):
    from scripts.build_api_football_sqlite_from_fixture_players import resolve_input_paths

    first = tmp_path / "fixture_a.json"
    second = tmp_path / "fixture_b.json"
    first.write_text("{}", encoding="utf-8")
    second.write_text("{}", encoding="utf-8")

    assert resolve_input_paths(None, str(tmp_path / "fixture_*.json")) == [first, second]


def test_resolve_input_paths_fails_when_no_inputs_resolved(tmp_path):
    from scripts.build_api_football_sqlite_from_fixture_players import resolve_input_paths

    with pytest.raises(SystemExit, match="No input files resolved"):
        resolve_input_paths(None, str(tmp_path / "missing_*.json"))


def test_resolve_input_paths_fails_when_input_does_not_exist(tmp_path):
    from scripts.build_api_football_sqlite_from_fixture_players import resolve_input_paths

    with pytest.raises(SystemExit, match="Input file not found"):
        resolve_input_paths([tmp_path / "missing.json"], None)


def test_load_payloads_reads_valid_json_files(tmp_path):
    from scripts.build_api_football_sqlite_from_fixture_players import load_payloads

    input_path = tmp_path / "fixture.json"
    payload = _fixture_payload(1, "Player One", "Team A")
    _write_json(input_path, payload)

    assert load_payloads([input_path]) == [payload]


def test_build_parser_parses_numeric_season_as_int():
    from scripts.build_api_football_sqlite_from_fixture_players import build_parser

    args = build_parser().parse_args(["--input", "fixture.json", "--season", "2024"])

    assert args.season == 2024


def test_build_end_to_end_with_two_payloads_loads_sqlite(tmp_path):
    from scripts.build_api_football_sqlite_from_fixture_players import build_sqlite_from_fixture_players

    first = tmp_path / "fixture_a.json"
    second = tmp_path / "fixture_b.json"
    database_path = tmp_path / "football_scout.db"
    _write_json(first, _fixture_payload(1, "Player One", "Team A", fixture_id=1001))
    _write_json(second, _fixture_payload(2, "Player Two", "Team B", fixture_id=1002))

    summary = build_sqlite_from_fixture_players(
        input_paths=[first, second],
        database_path=database_path,
        table_name="players",
        league="LaLiga",
        season=2024,
    )

    loaded = load_players_from_sqlite(database_path, "players")
    assert summary["input_files"] == 2
    assert summary["aggregated_players"] == 2
    assert summary["canonical_records"] == 2
    assert summary["rows_loaded"] == 2
    assert loaded[["player", "team", "position", "minutes"]].to_dict("records") == [
        {"player": "Player One", "team": "Team A", "position": "Forward", "minutes": 90.0},
        {"player": "Player Two", "team": "Team B", "position": "Forward", "minutes": 90.0},
    ]


def test_apply_context_defaults_fills_missing_league_and_season_only():
    from scripts.build_api_football_sqlite_from_fixture_players import apply_context_defaults

    records = [
        {"player": "A", "league": None, "season": ""},
        {"player": "B", "league": "Existing League", "season": 2023},
    ]

    enriched = apply_context_defaults(records, league="LaLiga", season=2024)

    assert enriched[0]["league"] == "LaLiga"
    assert enriched[0]["season"] == 2024
    assert enriched[1]["league"] == "Existing League"
    assert enriched[1]["season"] == 2023


def test_optional_outputs_are_written(tmp_path):
    from scripts.build_api_football_sqlite_from_fixture_players import build_sqlite_from_fixture_players

    input_path = tmp_path / "fixture.json"
    database_path = tmp_path / "football_scout.db"
    aggregated_output = tmp_path / "out" / "aggregated.json"
    canonical_output = tmp_path / "out" / "canonical.json"
    _write_json(input_path, _fixture_payload(1, "Player One", "Team A"))

    build_sqlite_from_fixture_players(
        input_paths=[input_path],
        database_path=database_path,
        table_name="players",
        aggregated_output=aggregated_output,
        canonical_output=canonical_output,
    )

    assert json.loads(aggregated_output.read_text(encoding="utf-8"))[0]["player"] == "Player One"
    assert json.loads(canonical_output.read_text(encoding="utf-8"))[0]["player"] == "Player One"
