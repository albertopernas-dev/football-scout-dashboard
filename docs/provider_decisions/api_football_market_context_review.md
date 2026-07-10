# Provider Decision Record - API-Football Market Context Review

## Status

Rejected for market context / Accepted for performance data

## Date Evaluated

2026-07-10

## Evaluator

Football Scout Dashboard maintainer

## Provider Type

Existing provider limitation review

## Use Case

Evaluate whether API-Football covers:

- age;
- market_value_eur;
- contract_end_date;
- stable player/team IDs;
- performance stats.

## Data Covered

| Field | Available? | Notes | Confidence |
|---|---|---|---|
| age | Not reliable / not available in current workflow | The current local workflow does not provide usable age coverage from API-Football fixture/player data. | Low |
| market_value_eur | Not available | No usable market value field is available in the current workflow. | High |
| contract_end_date | Not available | No usable contract-end field is available in the current workflow. | High |
| player/team IDs | Available / useful | API-Football provides IDs that are useful internally, though the current Market Context Layer matches by player/team/league/season. | Medium |
| performance stats | Available / useful via fixtures/players | The existing pipeline produces a local performance dataset for scoring and scouting workflows. | High |
| value_date/provenance | Not available for market context | No market-context value date or provenance is available because market-context values are not available in this workflow. | High |

## Coverage Assessment

- Current pipeline uses API-Football `fixtures/players` for LaLiga 2024.
- It provides a local performance dataset with 588 players, 20 teams and 380/380 fixtures cached.
- It does not provide sufficient market context for age, market value or contract end date in the current workflow.
- Market context coverage from API-Football should not be assumed.

## License And Usage Review

- Existing project usage relies on local cached API responses for development and demo workflows.
- Redistribution of raw provider payloads should remain avoided unless API-Football terms explicitly allow it.
- No credentials or API keys should be committed.
- Any future provider use must respect API-Football terms.

## Technical Assessment

- Existing fixture-player pipeline is useful and reproducible.
- Local cache plus canonical SQLite workflow works for performance data.
- API-Football is not suitable as the canonical source for market context without additional verified fields.
- The app has no direct runtime dependency on API-Football.

## Data Quality Assessment

- Performance stats: useful enough for current scoring/demo, with documented limitations.
- Age: unavailable/unknown in the current local dataset.
- Market value: unavailable/unknown.
- Contract date: unavailable/unknown.
- Identity matching: useful because API-Football IDs exist internally, but the current Market Context Layer matches by player/team/league/season.

## Cost Assessment

- Existing usage has already been prototyped.
- Any expansion must consider request limits and plan terms.
- No market-context expansion should happen without confirming fields and terms.

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Assuming API-Football has market context | Opportunity Finder false precision | Keep market warnings and use separate enrichment. |
| Relying on provider IDs only | Matching issues with manual CSV | Keep diagnostics and explicit player/team/league/season matching. |
| Raw payload redistribution | Licensing risk | Keep raw data local and ignored. |
| API limits | Refresh instability | Keep local cache and batch controls. |

## Decision

- Accept for performance data pipeline.
- Reject as primary market context source for v0.4.0 unless new evidence shows reliable age, market value and contract fields with permitted usage.

## Rationale

API-Football is already useful for sporting performance data via `fixtures/players`, but current project diagnostics show age, market value and contract remain unknown. Therefore market context should continue through manual reviewed CSVs or a separate evaluated provider.

## Next Actions

- Keep API-Football performance pipeline.
- Do not use API-Football as market value or contract source.
- Evaluate other provider types for market context.
- Keep Market Context Layer provider-agnostic.

## Links / References

- [Data Provider Decision](../data_provider_decision.md)
- [v0.4.0 Provider Evaluation / Licensed Data Integration Plan](../v0_4_0_provider_evaluation_plan.md)
- [Market Context Layer Plan](../market_context_plan.md)
