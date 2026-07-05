from pathlib import Path


def test_build_parser_parses_basic_arguments():
    from scripts.refresh_local_dataset import build_parser

    args = build_parser().parse_args(
        [
            "--fixtures",
            "fixtures.json",
            "--fixture-players-dir",
            "cache",
            "--league",
            "LaLiga",
            "--season",
            "2024",
            "--limit",
            "5",
            "--delay-seconds",
            "2",
            "--dry-run",
        ]
    )

    assert args.fixtures == Path("fixtures.json")
    assert args.fixture_players_dir == Path("cache")
    assert args.league == "LaLiga"
    assert args.season == "2024"
    assert args.limit == 5
    assert args.delay_seconds == 2.0
    assert args.dry_run is True


def test_refresh_with_limit_zero_skips_fetch_and_builds_then_prints_status(tmp_path, monkeypatch, capsys):
    import scripts.refresh_local_dataset as refresh

    calls = []
    cached_file = tmp_path / "cache" / "api_football_fixture_players_1.json"
    cached_file.parent.mkdir()
    cached_file.write_text("{}", encoding="utf-8")

    monkeypatch.setattr(refresh, "resolve_input_paths", lambda inputs, pattern: [cached_file])
    monkeypatch.setattr(
        refresh,
        "build_sqlite_from_fixture_players",
        lambda input_paths, database_path, table_name, league, season: calls.append(
            ("build", input_paths, database_path, table_name, league, season)
        )
        or {
            "input_files": len(input_paths),
            "aggregated_players": 1,
            "canonical_records": 1,
            "database_path": database_path,
            "table": table_name,
            "rows_loaded": 1,
        },
    )
    monkeypatch.setattr(
        refresh,
        "calculate_local_dataset_status",
        lambda **kwargs: calls.append(("status", kwargs)) or {"sqlite_rows": 1},
    )
    monkeypatch.setattr(refresh, "print_status", lambda status: calls.append(("print_status", status)))

    summary = refresh.refresh_local_dataset(
        fixtures_path=tmp_path / "fixtures.json",
        fixture_players_dir=tmp_path / "cache",
        database_path=tmp_path / "db.sqlite",
        table_name="players",
        league="LaLiga",
        season="2024",
        limit=0,
    )

    assert summary["fetch_executed"] is False
    assert summary["build_executed"] is True
    assert calls[0][0] == "build"
    assert calls[1][0] == "status"
    assert calls[2] == ("print_status", {"sqlite_rows": 1})
    assert "Fetch skipped." in capsys.readouterr().out


def test_refresh_dry_run_does_not_build(tmp_path, monkeypatch, capsys):
    import scripts.refresh_local_dataset as refresh

    calls = []
    monkeypatch.setattr(refresh, "load_fixtures_payload", lambda path: {"response": []})
    monkeypatch.setattr(refresh, "extract_fixture_ids", lambda payload: [1, 2])
    monkeypatch.setattr(
        refresh,
        "fetch_fixture_players_batch",
        lambda **kwargs: calls.append(("fetch", kwargs))
        or {"stopped_early": False, "errors": [], "dry_run": True},
    )
    monkeypatch.setattr(refresh, "_print_fetch_summary", lambda summary: calls.append(("print_fetch", summary)))
    monkeypatch.setattr(
        refresh,
        "build_sqlite_from_fixture_players",
        lambda **kwargs: calls.append(("build", kwargs)),
    )
    monkeypatch.setattr(
        refresh,
        "calculate_local_dataset_status",
        lambda **kwargs: calls.append(("status", kwargs)) or {"sqlite_rows": 0},
    )
    monkeypatch.setattr(refresh, "print_status", lambda status: calls.append(("print_status", status)))

    summary = refresh.refresh_local_dataset(
        fixtures_path=tmp_path / "fixtures.json",
        fixture_players_dir=tmp_path / "cache",
        database_path=tmp_path / "db.sqlite",
        table_name="players",
        limit=5,
        dry_run=True,
    )

    assert summary["fetch_executed"] is True
    assert summary["build_executed"] is False
    assert not any(call[0] == "build" for call in calls)
    output = capsys.readouterr().out
    assert "Dry run: true" in output
    assert "No SQLite build performed." in output


def test_refresh_stopped_early_fetch_skips_build(tmp_path, monkeypatch, capsys):
    import scripts.refresh_local_dataset as refresh

    calls = []
    monkeypatch.setattr(refresh, "load_fixtures_payload", lambda path: {"response": []})
    monkeypatch.setattr(refresh, "extract_fixture_ids", lambda payload: [1, 2])
    monkeypatch.setattr(refresh, "_build_fetch_client", lambda dry_run: object())
    monkeypatch.setattr(
        refresh,
        "fetch_fixture_players_batch",
        lambda **kwargs: calls.append(("fetch", kwargs))
        or {"stopped_early": True, "errors": [{"fixture_id": 2, "error": "429"}]},
    )
    monkeypatch.setattr(refresh, "_print_fetch_summary", lambda summary: calls.append(("print_fetch", summary)))
    monkeypatch.setattr(refresh, "build_sqlite_from_fixture_players", lambda **kwargs: calls.append(("build", kwargs)))
    monkeypatch.setattr(refresh, "calculate_local_dataset_status", lambda **kwargs: {"sqlite_rows": 0})
    monkeypatch.setattr(refresh, "print_status", lambda status: calls.append(("print_status", status)))

    summary = refresh.refresh_local_dataset(
        fixtures_path=tmp_path / "fixtures.json",
        fixture_players_dir=tmp_path / "cache",
        database_path=tmp_path / "db.sqlite",
        table_name="players",
        limit=2,
    )

    assert summary["build_executed"] is False
    assert not any(call[0] == "build" for call in calls)
    assert "Fetch stopped early; SQLite build skipped." in capsys.readouterr().out


def test_refresh_build_uses_cached_fixture_player_jsons(tmp_path, monkeypatch):
    import scripts.refresh_local_dataset as refresh

    captured = {}
    first = tmp_path / "cache" / "api_football_fixture_players_2.json"
    second = tmp_path / "cache" / "api_football_fixture_players_1.json"
    first.parent.mkdir()
    first.write_text("{}", encoding="utf-8")
    second.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(refresh, "resolve_input_paths", lambda inputs, pattern: [second, first])
    monkeypatch.setattr(
        refresh,
        "build_sqlite_from_fixture_players",
        lambda input_paths, **kwargs: captured.setdefault("input_paths", input_paths)
        and {
            "input_files": len(input_paths),
            "aggregated_players": 2,
            "canonical_records": 2,
            "database_path": kwargs["database_path"],
            "table": kwargs["table_name"],
            "rows_loaded": 2,
        },
    )
    monkeypatch.setattr(refresh, "calculate_local_dataset_status", lambda **kwargs: {"sqlite_rows": 2})
    monkeypatch.setattr(refresh, "print_status", lambda status: None)

    refresh.refresh_local_dataset(
        fixtures_path=tmp_path / "fixtures.json",
        fixture_players_dir=tmp_path / "cache",
        database_path=tmp_path / "db.sqlite",
        table_name="players",
        limit=0,
    )

    assert captured["input_paths"] == [second, first]
