# Provider Decision Record - Capology Salary / Contract Review

## Status

Deferred for v0.4.0 core `market_value_eur`

Accepted for future salary/cost context if budget and license allow.

## Date Evaluated

2026-07-10

## Evaluator

Football Scout Dashboard maintainer

## Provider Type

Licensed salary / contract economics provider candidate

## Use Case

Evaluate whether Capology can support:

- salary and cost context;
- contract economics;
- contract-related context;
- market_value_eur;
- value/cost comparison fields for future Opportunity Finder extensions.

## Data Covered

| Field | Available? | Notes | Confidence |
|---|---|---|---|
| age | Not primary use case | Not evaluated as the main target for Capology. | Low |
| market_value_eur | Not confirmed / not primary | Capology should not be treated as a market value source without evidence. | Low |
| contract_end_date | Possible / needs validation | Contract economics may include contract-related fields, but exact field coverage must be validated. | Low |
| salary/cost context | Likely available | API Basic / Plus appear oriented to salary data. | Medium |
| stable IDs | Needs validation | Provider identifiers and matching approach must be reviewed. | Low |
| provenance | Needs review | License, source and display constraints must be reviewed. | Low |

## Coverage Assessment

- Capology appears strongest for salary/cost context rather than `market_value_eur`.
- API Basic / Plus are paid and salary-data oriented.
- LaLiga appears included in API Basic according to the prior pricing review.
- It does not replace market value enrichment.
- Coverage, field names and redistribution/display rights must be validated before any code integration.

## License And Usage Review

- Paid API terms must be reviewed before any implementation.
- Redistribution, screenshots/demo use, caching and attribution must be clarified.
- No credentials or API keys should be committed.
- No raw provider dumps should be versioned.

## Technical Assessment

- Potential future source for salary/cost extensions.
- Not suitable as the core v0.4.0 `market_value_eur` source.
- Any future integration should feed a local canonical artifact, not direct app runtime calls.
- Matching strategy must be validated against local player/team/league/season data.

## Data Quality Assessment

- Age quality: not evaluated.
- Market value methodology: not applicable unless future evidence shows a field.
- Contract date quality: unknown until sample responses are reviewed.
- Salary/cost quality: promising but dependent on license, methodology and field definitions.
- Identity matching quality: unknown.
- Stale data risk: depends on update cadence and plan.

## Cost Assessment

- Cost risk is high for a personal/demo project.
- API Basic / Plus are paid.
- Sustainability should be evaluated before any prototype.

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Treating salary as market value | Misleading Opportunity Finder interpretation | Keep salary/cost context separate from `market_value_eur`. |
| High subscription cost | Not sustainable for project usage | Defer unless budget and value justify it. |
| License limits display or caching | Cannot safely use in demo workflow | Review terms before integration. |
| Contract fields incomplete | Contract filters may be unreliable | Validate sample responses before mapping. |
| Matching uncertainty | Wrong salary/cost data attached to players | Use diagnostics and provider IDs if available. |

## Decision

- Defer for v0.4.0 core market value needs.
- Accept for future salary/cost context if budget and license allow.

## Rationale

Capology appears useful for salary and cost context, but it should not be treated as a `market_value_eur` source. For Football Scout Dashboard v0.4.0, the main need remains age, market value and contract end date. Capology may become valuable in a later salary/cost extension if the license and budget fit.

## Next Actions

- Keep as possible v0.4.x salary-cost extension.
- Do not use as market value provider.
- Revisit only if salary/cost context becomes a planned feature.
- Review license, cost, fields and matching before any prototype.

## Links / References

- [Provider Evaluation Matrix](provider_evaluation_matrix.md)
- [v0.4.0 Provider Evaluation / Licensed Data Integration Plan](../v0_4_0_provider_evaluation_plan.md)
- [Market Context Layer Plan](../market_context_plan.md)
