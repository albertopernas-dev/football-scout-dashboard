# Football Scout Dashboard v0.1.0

## Summary

First stable MVP of a local football scouting dashboard.

This release includes a SQLite-first local workflow, an API-Football `fixtures/players` pipeline, a LaLiga 2024 dataset rebuilt from cached raw payloads, sample-adjusted player rankings, Opportunity Finder, CSV exports, HTML scouting reports, documentation and automated tests.

## Dataset Snapshot

- League: LaLiga
- Season: 2024
- Fixtures cached: 380 / 380
- Players: 588
- Teams: 20
- Total minutes: 649284
- Age known pct: 0.0%
- Market value known pct: 0.0%
- Contract known pct: 0.0%

## Highlights

- Local SQLite-first data source.
- Reproducible refresh from cached API-Football fixture/player payloads.
- Ranking adjusted by minutes reliability.
- Raw score kept visible for exploratory signals.
- Metrics without signal are ignored automatically.
- Goalkeepers treated separately for comparability.
- Opportunity Finder includes reliability/comparability filters.
- CSV exports preserve visible filters and columns.
- HTML scouting reports.
- User guide, scoring methodology and demo walkthrough.
- 290 passing tests.

## Validation

Commands used to validate the milestone:

```powershell
.venv\Scripts\python.exe -m pytest -p no:cacheprovider tests -q
```

```powershell
.venv\Scripts\python.exe scripts/refresh_local_dataset.py --fixtures data/raw/api_football_laliga_2024_finished_fixtures.json --fixture-players-dir data/raw/fixture_players --league LaLiga --season 2024
```

```powershell
.venv\Scripts\python.exe scripts/diagnose_scores.py
```

## Known Limitations

- No real age source is connected yet.
- No real market value source is connected yet.
- No contract-end source is connected yet.
- Some advanced metrics have no signal in current API-Football payloads.
- The goalkeeper model is conservative and limited by available goalkeeper metrics.
- The dashboard supports scouting work, but does not replace video review or human judgement.

## Suggested GitHub Release Text

```markdown
## Football Scout Dashboard v0.1.0

First stable MVP of a local football scouting dashboard.

### What is included

- SQLite-first local data workflow.
- API-Football fixtures/players pipeline using cached raw payloads.
- LaLiga 2024 local dataset: 380 / 380 fixtures cached, 588 players, 20 teams and 649284 total minutes.
- Sample-adjusted player rankings based on minutes reliability.
- Adaptive scoring that ignores metrics without real signal.
- Separate goalkeeper comparability handling.
- Opportunity Finder with reliability and comparability filters.
- CSV exports for visible table results.
- HTML scouting reports.
- User guide, scoring methodology and demo walkthrough.
- 290 passing tests.

### Current limitations

- Age, market value and contract-end data are not connected yet.
- Some advanced metrics have no signal in the current API-Football payloads.
- Goalkeeper scoring is intentionally conservative.
- Rankings support scouting work, but do not replace video review or human judgement.
```
