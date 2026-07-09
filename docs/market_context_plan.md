# Market Context Layer Plan

## Objective

The v0.2.0 goal is to enrich the current football scouting dataset with real market context:

- real player age;
- market value;
- contract end date;
- data source;
- confidence and coverage indicators.

This layer should make market-related analysis explicit, traceable and measurable without changing the stable v0.1.0 scoring pipeline prematurely.

## Why this matters

Opportunity Finder currently works mostly as a performance plus minutes-reliability shortlist. That is useful for scouting exploration, but it is not yet a true market opportunity ranking.

Without real age, market value and contract data, the dashboard cannot reliably answer whether a player is young, undervalued, approaching contract expiry or genuinely attractive from a recruitment-market perspective.

Adding a Market Context Layer would let Opportunity Finder evolve from a performance signal into a more useful scouting workflow, while still showing warnings whenever context is missing or partial.

## Implementation Status

- CSV schema and validation module complete in `src/market_context.py`.
- Merge helpers for prepared player data complete.
- Diagnostics script complete in `scripts/diagnose_market_context.py`.
- CSV template/sample added in `data/enrichment/`.
- Optional config-based enrichment loading complete.
- App status display complete.
- Market context table display complete.
- Opportunity Finder display complete.
- Effective market context fields complete.
- Real enrichment data pending.
- App analytical integration pending.
- Scoring integration pending; rankings are unchanged.
- Opportunity Finder analytical integration pending.

## Diagnostic Command

Validate and diagnose a market context CSV against the active local player dataset with:

```powershell
.venv\Scripts\python.exe scripts/diagnose_market_context.py --market-context-csv data/enrichment/player_market_context_sample.csv
```

The command reads the active dataset and the provided CSV, reports validation errors, duplicate keys, merge coverage and examples. It does not modify SQLite or the app.

CSV templates and identity-only sample rows live in `data/enrichment/`.

## Optional Enrichment Loading

Market context enrichment is opt-in. No CSV is loaded by default, and `data/enrichment/player_market_context_sample.csv` is only a diagnostic/sample file.

To enable enrichment explicitly:

```powershell
$env:FOOTBALL_SCOUT_MARKET_CONTEXT_CSV="data/enrichment/player_market_context_sample.csv"
```

For production-like usage, point this variable to a manually reviewed CSV with real `age`, `market_value_eur`, `contract_end_date`, `source`, `confidence` and `notes`.

The data layer now prepares `effective_*` market context fields. These fields prefer valid enrichment values and fall back to original values when available, but current scoring, rankings and Opportunity Finder calculations remain unchanged.

## Recommended Approach

### Phase 1

- Add a manual enrichment CSV.
- Start with a small number of players.
- Validate the enrichment schema.
- Merge enrichment data into the prepared player dataset.

### Phase 2

- Integrate enrichment into the existing prepared dataset workflow.
- Calculate market context coverage.
- Show coverage in the data quality panel.

### Phase 3

- Adjust Opportunity Finder to use real age, market value and contract data when available.
- Keep clear warnings when market context is missing or incomplete.

### Phase 4

- Explore automated data sources.
- Avoid scraping.
- Keep source, confidence and coverage visible.

## Proposed CSV Schema

```text
player, team, league, season, age, market_value_eur, contract_end_date, source, source_url, confidence, notes
```

Column notes:

- `player`: player name used for matching.
- `team`: team name used for matching.
- `league`: league name used for matching.
- `season`: season used for matching.
- `age`: real player age.
- `market_value_eur`: market value in euros.
- `contract_end_date`: contract end date.
- `source`: source name for the enrichment data.
- `source_url`: optional source URL for review.
- `confidence`: confidence level for the enriched row.
- `notes`: optional manual notes about ambiguity, source quality or matching decisions.

## Matching Strategy

The initial match should use:

- `player`;
- `team`;
- `league`;
- `season`.

Before matching, names should be normalized conservatively:

- trim whitespace;
- normalize case;
- handle accents where possible;
- keep original display names unchanged.

Expected matching problems:

- accents and diacritics;
- abbreviated player names;
- duplicated names;
- loan moves;
- mid-season transfers;
- team naming differences;
- players appearing in multiple competitions or squads.

The first version should prefer explicit review and confidence labels over aggressive fuzzy matching.

## Data Quality Rules

- `age` is valid when it is numeric and between 15 and 45.
- `market_value_eur` is valid when it is numeric and greater than 0.
- `contract_end_date` is valid when it is parseable as a date.
- `confidence` must be one of `low`, `medium` or `high`.
- `source` is required if any enrichment value is present.
- Unknown values should remain unknown, not be converted into misleading defaults.

## App Impact

Once the layer is implemented:

- age would stop showing as `Desconocida` for enriched players;
- market value would stop showing as `Desconocido` for enriched players;
- Opportunity Finder could use real age, value and contract context;
- the dataset summary and data quality panel would show real market-context coverage;
- warnings would remain visible when coverage is partial or missing.

## Risks

- Poor matching quality can attach market data to the wrong player.
- Market data can become outdated quickly.
- Sources may be inconsistent across players, teams or leagues.
- Partial coverage can bias rankings toward enriched players.
- Numeric market values can create a false sense of precision.
- Contract data may be incomplete, stale or unavailable from standard football statistics providers.

## Definition of Done for v0.2.0

- A sample enrichment CSV is versioned.
- A loader validates and merges enrichment data.
- Tests cover schema validation, matching and unknown-value behavior.
- Market context coverage is visible in the app.
- Opportunity Finder uses real market context when it exists.
- Warnings remain clear when age, market value or contract data are missing.
