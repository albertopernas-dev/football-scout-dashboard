# Provider Evaluation Matrix

## Objective

This matrix compares candidate sources for market context before any provider-specific code is integrated.

Do not include:

- credentials;
- private pricing details;
- provider dumps;
- proprietary data;
- unauthorized scraping sources.

| Candidate | Provider type | Status | Age | Market value | Contract end | Stable IDs | Historical data | License clarity | Redistribution allowed? | Cache allowed? | Cost risk | Matching risk | Data freshness | Decision record | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| API-Football | Existing sports performance API | Reviewed | Insufficient in current workflow | No | No | Yes | Performance data yes | Review terms before expansion | Do not assume | Local cache currently used for dev/demo; review terms before expansion | Existing usage known; expansion requires review | Medium | Fixture-based for performance | [API-Football market context review](api_football_market_context_review.md) | Keep for performance, not market context. |
| Official league/club sources | Official league/club source | To evaluate | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Pending | Useful for high-confidence verification; fragmented coverage likely. |
| Licensed sports data provider | Licensed sports data provider | To evaluate | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Pending | Candidate for structured market context if license and cost allow. |
| Public API with explicit terms | Public API with explicit terms | To evaluate | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Pending | Candidate only if terms, fields and caching are clear. |
| Manually reviewed public references | Manually reviewed public reference | Active fallback | Manual | Manual | Manual | No | Manual | Source-specific | Source-specific | Local notes only | Low direct cost; high manual effort | Medium | Depends on review date | v0.3.0 local reviewed CSV workflow | Current v0.3.0 workflow supports this through local reviewed CSVs. |

## Scoring Guidance

Use these labels consistently when updating the matrix:

- Green: usable / clear / low risk.
- Yellow: partial / needs review.
- Red: not suitable / blocked.
- Unknown: not evaluated.

This is guidance only. Do not implement automatic scoring from this matrix.

## How To Use This Matrix

1. Create a decision record for every evaluated source.
2. Update the matrix only after reviewing license, fields and coverage.
3. Do not move a source to `Accepted` without a decision record.
4. Do not integrate provider-specific code until a decision record exists.
5. Keep the matrix high-level; put detailed evidence in the provider decision record.
