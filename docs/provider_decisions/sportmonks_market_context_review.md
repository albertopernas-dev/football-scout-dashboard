# Provider Decision Record - Sportmonks Market Context Review

## Status

Accept for prototype as partial market context provider

Not accepted as complete market value provider unless future evidence confirms `market_value_eur` availability and permitted usage.

## Date Evaluated

2026-07-10

## Evaluator

Football Scout Dashboard maintainer

## Provider Type

Public API with explicit terms / licensed sports data provider candidate

## Use Case

Evaluate whether Sportmonks can support:

- age;
- market_value_eur;
- contract_end_date;
- stable player/team IDs;
- squad and transfer context;
- provenance for canonical market context.

## Data Covered

| Field | Available? | Notes | Confidence |
|---|---|---|---|
| age | Likely available | Player metadata appears to include date of birth or equivalent player profile fields. Must be validated with sample responses. | Medium |
| market_value_eur | Not confirmed | No clear evidence yet that Sportmonks provides usable market value in euros with permitted usage. | Low |
| contract_end_date | Possible / needs validation | Squad/team-player documentation appears to include start/end contract fields. Must be validated in actual endpoints and plans. | Medium |
| player/team IDs | Likely available | Stable player/team IDs appear to be part of the API model. | Medium |
| squads/transfers | Likely available | Public documentation references squads, active squads and transfers. | Medium |
| provenance | Needs review | Source/provenance fields and terms must be reviewed before integration. | Low |

## Coverage Assessment

- Candidate for player metadata, date of birth, squads, transfers and stable IDs.
- Public LaLiga-facing documentation indicates players, active squads, transfers, date of birth, height and weight.
- Squad/team-player documentation indicates start/end contract fields.
- Market value coverage is not confirmed.
- Coverage by league, season and plan tier must be tested before any code integration.

## License And Usage Review

- Terms, plan limits, caching rights and redistribution constraints must be reviewed before any integration.
- No raw provider payloads should be committed.
- No credentials or API keys should be committed.
- Any prototype should use local raw cache only if terms permit it.

## Technical Assessment

- Appears technically promising for canonical market context enrichment.
- Likely supports stable IDs and structured API responses.
- Needs manual endpoint review and sample response mapping.
- Should feed the existing Market Context Layer through a local canonical transform.
- The app should not call Sportmonks directly at runtime.

## Data Quality Assessment

- Age quality: promising if date of birth is available and stable.
- Market value methodology: not confirmed.
- Contract date quality: promising but must validate contract field semantics.
- Identity matching quality: potentially good if stable IDs can be mapped.
- Provenance quality: unknown until provider metadata and terms are reviewed.
- Stale data risk: depends on update frequency and plan.

## Cost Assessment

- Pricing and plan limits must be reviewed.
- Prototype should not proceed until cost, quota and allowed usage are clear.
- Sustainability for a local/demo project must be checked before adopting.

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Assuming market values exist | False provider fit for Opportunity Finder | Do not accept as market value provider until sample responses confirm fields and usage rights. |
| Contract fields have unclear semantics | Misleading contract-expiry filters | Validate field definitions and examples before canonical mapping. |
| Plan tier lacks required fields | Prototype cannot reproduce expected coverage | Confirm plan requirements before code work. |
| Caching or redistribution restrictions | Data cannot be stored or shown safely | Review terms before fetching and keep raw data local if allowed. |
| Matching mismatch with existing SQLite dataset | Wrong enrichment attached to players | Use diagnostics, sample mapping and provider IDs where possible. |

## Decision

- Accept for prototype as partial market context provider.
- Do not accept as complete market value provider unless future evidence confirms `market_value_eur` availability and permitted usage.

## Rationale

Sportmonks appears to be the strongest candidate for structured player metadata, IDs, squads, transfers and possible contract fields. It may help fill age and contract context, but there is no clear evidence yet that it provides market value in euros. It should be evaluated through sample responses and license review before any integration.

## Next Actions

- Review relevant endpoints and terms manually.
- Validate sample responses for player date of birth, stable IDs, squads and contract fields.
- Map confirmed fields to the canonical market context schema.
- Keep any prototype opt-in and local.
- Do not integrate code until license, caching and field availability are confirmed.

## Links / References

- [Provider Evaluation Matrix](provider_evaluation_matrix.md)
- [v0.4.0 Provider Evaluation / Licensed Data Integration Plan](../v0_4_0_provider_evaluation_plan.md)
- [Market Context Layer Plan](../market_context_plan.md)
