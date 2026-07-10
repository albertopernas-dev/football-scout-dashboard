# Demo Walkthrough

This walkthrough is designed for a 5-10 minute portfolio or stakeholder demo. It shows the current local workflow without claiming complete market coverage or a finished professional scouting model.

## Start app

Run the Streamlit app from the project root:

```powershell
.venv\Scripts\streamlit.exe run app.py
```

Open the local URL shown by Streamlit. The app should load the active data source, prepare features, calculate scores and show the dashboard.

## Refresh dataset

If the local raw payloads are already cached, rebuild the SQLite dataset with:

```powershell
.venv\Scripts\python.exe scripts/refresh_local_dataset.py --fixtures data/raw/api_football_laliga_2024_finished_fixtures.json --fixture-players-dir data/raw/fixture_players --league LaLiga --season 2024
```

This rebuilds the local SQLite database from cached API-Football `fixtures/players` payloads. It does not require a new API call when the raw files are already present.

## Check dataset summary

Start at the top of the app and review:

- active data source;
- player count;
- team count;
- total minutes;
- reliable sample count;
- market context status.

For the current LaLiga 2024 dataset, age, market value and contract coverage are limited. The app surfaces that context so the rankings are not presented as complete market intelligence.

## v0.2.0 Market Context Demo

First, run the app without market context enrichment. `Fuente de datos` should show the active SQLite source and limited market context.

Then run the diagnostic command against the identity-only sample:

```powershell
.venv\Scripts\python.exe scripts/diagnose_market_context.py --market-context-csv data/enrichment/player_market_context_sample.csv
```

The sample validates matching and UI behavior, but intentionally does not include real age, market value or contract values.

Enable the sample explicitly:

```powershell
$env:FOOTBALL_SCOUT_MARKET_CONTEXT_CSV="data/enrichment/player_market_context_sample.csv"
.venv\Scripts\streamlit.exe run app.py
```

Open `Fuente de datos` again and show:

- market context status;
- matched rows;
- validation and duplicate counts;
- effective market context coverage;
- source breakdown: enrichment, original and unknown.

With the identity-only sample, effective age, market value and contract coverage should remain 0%. That is expected and useful for explaining that the layer is ready, but real market enrichment data is still pending.

## v0.3.0 Real Enrichment Demo

For a reviewed local CSV, first generate a seed from Opportunity Finder candidates:

```powershell
.venv\Scripts\python.exe scripts\export_enrichment_seed.py --top-n 25
```

After manual review, validate the local file:

```powershell
.venv\Scripts\python.exe scripts\diagnose_market_context.py --market-context-csv data/enrichment/player_market_context_laliga_2024_reviewed.local.csv
```

Then activate it explicitly and reopen the app:

```powershell
$env:FOOTBALL_SCOUT_MARKET_CONTEXT_CSV="data/enrichment/player_market_context_laliga_2024_reviewed.local.csv"
.venv\Scripts\streamlit.exe run app.py
```

Opportunity Finder should show effective age, market value and contract as the primary market fields when reviewed values exist.

## Review recommended ranking

Open the main player table and focus on `Score recomendado`. This is the recommended score because it adjusts the raw score by minutes reliability.

Use `Score bruto` as an exploratory signal. A player with a high raw score but a low-minute sample can still be interesting, but should not be treated as equally reliable as a player with a larger sample.

## Filter reliable/comparable players

Use the table controls:

- `Ambito ranking`: start with comparable general-ranking players.
- `Fiabilidad muestra`: use `Media o fiable` or `Solo fiable` for a cleaner shortlist.

Goalkeepers are marked separately because the general scoring model is not fully comparable for them.

## Use Opportunity Finder

Open Opportunity Finder and apply the same mindset:

- use comparability filters;
- use sample reliability filters;
- adjust position, minutes and result count;
- read the market-context warning before interpreting the ranking.

In the current dataset, Opportunity Finder is closer to a performance-and-reliability shortlist than a full market opportunity model, because age, market value and contract fields are not available.

Opportunity Finder uses `effective_age`, `effective_market_value_eur` and `effective_contract_end_date` when real values exist. In the table and player detail, those effective values are shown as the primary market context, with original values kept as reference. With the bundled sample, they remain unknown because the sample is identity-only.

## Export CSV

Use the CSV download buttons to export:

- the visible player table;
- the visible Opportunity Finder results.

The exports preserve the visible columns and current filters, making them useful for shortlists, review notes or external analysis.

## Generate scouting report

Use the similarity/reporting flow to generate an HTML scouting report for a selected player. The report is useful for a quick profile summary, comparable players and visual context.

Reports should be treated as draft scouting material, not final recruitment recommendations.

## Explain current limitations

Be explicit about what the dashboard can and cannot claim today:

- no real age source is connected yet;
- no real market value source is connected yet;
- no contract-end source is connected yet;
- advanced metrics such as xG, xA, progressions and recoveries may have no signal in the current API-Football payloads;
- goalkeeper scoring is intentionally conservative and depends on limited available goalkeeper signals;
- rankings support scouting work, but do not replace video review, live scouting or domain judgement.
