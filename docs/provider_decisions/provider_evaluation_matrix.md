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
| Sportmonks | Public API with explicit terms / licensed sports data provider candidate | Reviewed / candidate prototype | Likely via player metadata; validate sample responses | Not confirmed | Possible contract start/end fields; validate semantics | Likely yes | Needs validation | Review terms before prototype | Do not assume | Review terms before prototype | Unknown | Medium | Unknown | [Sportmonks market context review](sportmonks_market_context_review.md) | Candidate partial provider for age, IDs, squads, transfers and possible contract fields; not accepted for market value yet. |
| Capology | Salary / contract economics provider candidate | Reviewed / deferred for salary-cost | Not primary use case | Not confirmed / not primary | Possible contract economics; validate fields | Needs validation | Needs validation | Paid terms require review | Do not assume | Review terms before prototype | High for personal/demo use | Unknown | Unknown | [Capology salary / contract review](capology_salary_contract_review.md) | Defer for core market value; possible future salary/cost extension. |
| Transfermarkt manual references | Manually reviewed public reference | Active fallback / manual only | Manual | Manual | Manual | Not used | Manual | Source-specific | Do not version copied values | Local reviewed CSV only | Low direct cost; high manual effort | Medium | Depends on review date | [Transfermarkt manual reference review](transfermarkt_manual_reference_review.md) | Good manual reference for market value and contract expiry; reject scraping and automated integration. |
| Official league/club sources | Official league/club source | Active manual verification / fragmented | Possible | Usually no | Possible via announcements | Unknown | Source-specific | Source-specific | Source-specific | Local notes only if permitted | Low direct cost; high manual effort | Medium | Varies by source | Pending | Useful for high-confidence verification; fragmented coverage likely. |
| Licensed sports data provider | Licensed sports data provider | To evaluate | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Pending | Candidate for structured market context if license and cost allow. |
| Public API with explicit terms | Public API with explicit terms | To evaluate | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Pending | Candidate only if terms, fields and caching are clear. |
| Wyscout/Hudl | Licensed sports data provider | Deferred for market context | Unknown | No clear public evidence | No clear public evidence | Likely provider IDs if licensed | Likely performance/video context | Requires license review | Do not assume | Do not assume | Likely high | Unknown | Unknown | Pending | Defer for market context until public evidence and license terms confirm relevant fields. |
| Sportradar | Licensed sports data provider | Deferred for market context / to evaluate | Unknown | No clear public evidence | No clear public evidence | Likely provider IDs if licensed | Likely sports data context | Requires license review | Do not assume | Do not assume | Likely high | Unknown | Unknown | Pending | Defer for market context until field coverage and license terms are clear. |

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
