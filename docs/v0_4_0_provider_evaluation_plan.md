# v0.4.0 Provider Evaluation / Licensed Data Integration Plan

## Objective

v0.4.0 should evaluate data providers for market context fields such as real age, market value, contract end date and potentially additional provenance context.

The goal is to move beyond manual local enrichment while preserving traceability, licensing discipline and a no-scraping policy. Any provider integration should feed the existing Market Context Layer rather than bypassing validation, diagnostics or local reproducibility.

## Scope

Included:

- evaluation of official, licensed or explicitly permitted API data sources;
- coverage by league, season and player;
- quality of age, market value and contract-end fields;
- cost, plan limits and usage restrictions;
- usage rights and redistribution constraints;
- local raw cache and reproducible pipeline design;
- opt-in integration with the existing Market Context Layer;
- diagnostics and validation before data is activated in the app.

## Out of Scope

- unauthorized scraping;
- copying protected data without permission;
- replacing the general sporting scoring model;
- automatic transfer recommendations without sufficient coverage;
- versioning real provider data when licensing does not allow redistribution;
- connecting a real provider before reviewing contract, license and usage terms.

## Provider Evaluation Criteria

Use the shared [Provider Evaluation Matrix](provider_decisions/provider_evaluation_matrix.md) to compare candidate sources at a high level. The matrix does not replace provider decision records; each accepted, rejected or deferred source still needs its own record in [`docs/provider_decisions/`](provider_decisions/).

| Criterion | Why it matters | How to evaluate | Minimum acceptable standard |
|---|---|---|---|
| Coverage | Opportunity Finder needs enough players to avoid biased shortlists. | Measure covered players by league, team and season against the local SQLite dataset. | Coverage is explicit, measurable and adequate for the target shortlist. |
| Field availability | v0.4.0 targets age, market value and contract context. | Inspect sample responses and map fields to the canonical schema. | At least one target market-context field is available with clear semantics. |
| Historical data | The app works with season-specific datasets. | Check whether historical seasons can be queried or exported. | Historical access is documented or limitations are explicit. |
| Update frequency | Market values and contracts become stale. | Review provider update cadence and timestamps. | Data freshness is known and can be shown or documented. |
| Licensing / redistribution rights | Real provider data may not be publishable in the repo. | Read terms, plan documentation and redistribution clauses. | Local/private use is permitted; redistribution limits are understood. |
| API reliability | Refreshes and diagnostics should be repeatable. | Test sample calls, errors, uptime information and response consistency. | Failures can be handled without breaking the app. |
| Cost | Paid data can affect project sustainability. | Compare free tier, paid tier and expected request volume. | Cost is acceptable for the intended usage or kept out of scope. |
| Rate limits | Batch refreshes must respect provider limits. | Review limits per minute/day/month and test conservative runs. | Limits allow a safe cached workflow. |
| Data provenance | The app should show where market context came from. | Check provider metadata, source labels and timestamps. | Provider/source can be recorded in `source`, `source_url` or future provenance fields. |
| Player identity matching | Bad matches can attach market data to the wrong player. | Compare provider IDs and names against local player/team/league/season keys. | Stable IDs or a reviewable matching strategy exist. |
| Contract data quality | Contract dates are high-impact and often uncertain. | Validate sample contract fields against known examples. | Contract semantics and date format are clear enough to validate. |
| Market value methodology | Market values can be estimates, model outputs or published values. | Review methodology notes and value date availability. | Methodology and value date are documented or confidence is marked accordingly. |
| Ease of local caching | The app should not depend on live provider calls at runtime. | Prototype raw payload storage and replay. | Raw or canonical responses can be cached locally when license permits. |
| GDPR / compliance considerations if applicable | Personal data and licensing obligations may apply. | Review terms and avoid storing unnecessary personal data. | Stored data is limited to necessary scouting context and follows provider terms. |

## Candidate Provider Types

### Official League Or Club Sources

Official sources can provide strong provenance for player identity, squad information and sometimes contract announcements. Coverage may be fragmented across clubs and competitions, and structured API access is not guaranteed.

Best use: high-confidence verification for specific fields, especially when a source URL can be recorded.

### Licensed Sports Data Providers

Licensed providers may offer structured player, team, contract or market datasets with stable IDs and documented usage terms. Cost, redistribution rights and plan limits must be reviewed before integration.

Best use: candidate source for repeatable market context enrichment if licensing allows local usage.

### Public APIs With Explicit Terms

Public APIs can be suitable when terms clearly allow the intended use. They still require validation for coverage, field definitions, rate limits and redistribution rights.

Best use: prototyping provider-to-canonical transforms and testing cache/diagnostic flows.

### Manually Reviewed Public References

Manual references remain useful for spot checks, confidence assignment and small reviewed batches. They should not become hidden scraping or untraceable copying.

Best use: fallback or validation layer for small shortlists.

### Existing API-Football Limitations

The current API-Football pipeline works for sporting performance using `fixtures/players` payloads and local SQLite refreshes. It has not provided reliable coverage for age, market value or contract-end context in the current workflow.

Best use: continue using API-Football for performance data while evaluating separate market-context sources.

Decision record: [`docs/provider_decisions/api_football_market_context_review.md`](provider_decisions/api_football_market_context_review.md).

## Integration Architecture

Future provider integration should follow a local, auditable path:

```text
provider raw fetch
  -> local raw cache
  -> canonical market context transform
  -> validation
  -> diagnostics
  -> optional activation
  -> Streamlit app reads validated local data
```

Design principles:

- no direct app-to-provider calls;
- no hidden provider dependency at Streamlit runtime;
- app consumes validated local CSV or canonical local artifacts;
- keep explicit configuration through environment variable or config;
- keep fallback mode without market context;
- keep validation and diagnostics mandatory before activation.

Supporting documents:

- [Provider Cache Policy](provider_cache_policy.md)
- [Provider To Market Context Transform Plan](provider_to_market_context_transform_plan.md)

## Proposed Canonical Schema

Current schema:

```text
player,team,league,season,age,market_value_eur,contract_end_date,source,source_url,confidence,notes
```

Possible future fields:

```text
provider_player_id
provider_team_id
provider_name
fetched_at
value_date
contract_option_notes
license_scope
```

These fields are proposals only. They should not be implemented until a provider decision requires them.

## Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| License does not allow redistribution | Real data cannot be committed or shared publicly. | Keep provider data local, document license scope and avoid versioning restricted data. |
| Incomplete coverage | Opportunity Finder can become biased toward covered players. | Report coverage, keep warnings and avoid weighting changes until coverage is sufficient. |
| Incorrect player matching | Market context can attach to the wrong player. | Prefer provider IDs, diagnostic examples and manual review for ambiguous matches. |
| Opaque market values | Users may overtrust estimates. | Store source, confidence, value date and methodology notes where possible. |
| Outdated contracts | Contract opportunity signals can become misleading. | Track fetched/value dates and rerun diagnostics before use. |
| API limits or cost | Refresh workflow may become expensive or unreliable. | Use local cache, conservative batching and explicit refresh commands. |
| Provider dependency | Product quality may depend on one vendor. | Keep canonical schema and fallback CSV workflow provider-agnostic. |
| Mixed data dates | Combining values from different dates can distort comparisons. | Store value dates and document mixed-date coverage. |
| False precision in Opportunity Finder | Rankings may look more authoritative than the data supports. | Keep warnings, coverage panels and confidence/source display. |

## Decision Record Template

Decision records live in [`docs/provider_decisions/`](provider_decisions/). Use [`docs/provider_decisions/provider_decision_template.md`](provider_decisions/provider_decision_template.md) for each evaluated provider or source type.

```text
Provider:
Date evaluated:
Data covered:
License summary:
Cost:
Pros:
Cons:
Decision:
Next action:
```

## v0.4.0 Acceptance Criteria

- At least 2-3 provider types are evaluated or explicitly ruled out.
- Provider decision is documented.
- No scraping is introduced.
- License and redistribution constraints are reviewed before integration.
- A sample or canonical local artifact is validated if provider data is prototyped.
- Diagnostics work against any prototype canonical output.
- The app keeps working without market context.
- Tests are added if code is implemented after the planning phase.

## Recommended Next Issues

- [DATA] Evaluate licensed market data providers.
- [DATA] Define provider decision record.
- [DATA] Maintain provider evaluation matrix.
- [DATA] Define provider cache policy.
- [DATA] Define provider-to-market-context transform contract.
- [DATA] Prototype provider-to-market-context canonical transform.
- [APP] Show provider provenance in market context UI.
- [QA] Add fixture tests for provider canonical transform.
