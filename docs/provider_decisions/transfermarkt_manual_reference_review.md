# Provider Decision Record - Transfermarkt Manual Reference Review

## Status

Accepted for local/manual reviewed references

Rejected for automated integration or scraping

## Date Evaluated

2026-07-10

## Evaluator

Football Scout Dashboard maintainer

## Provider Type

Manually reviewed public reference

## Use Case

Evaluate whether Transfermarkt can support manual review for:

- age;
- market_value_eur;
- contract_end_date;
- source URLs;
- confidence and notes in local reviewed CSVs.

## Data Covered

| Field | Available? | Notes | Confidence |
|---|---|---|---|
| age | Available as manual reference | Should be manually reviewed and validated against range rules. | Medium |
| market_value_eur | Available as manual reference | Treat as estimated/demand-based market value, not transfer fee. | Medium |
| contract_end_date | Available as manual reference | Contract and expiring-contract pages can support manual review. | Medium |
| stable IDs | Not used in current workflow | Current Market Context Layer matches by player/team/league/season. | Low |
| value_date/provenance | Manual | Must be captured through `source`, `source_url`, `confidence` and `notes`. | Medium |

## Coverage Assessment

- Transfermarkt appears to be the best public reference for market value and contract expiry.
- It should be used only through manual review.
- Coverage depends on manual selection and review effort.
- No automated scraper or third-party scraper API should be used.
- Real copied values should remain local and should not be versioned.

## License And Usage Review

- Do not scrape Transfermarkt.
- Do not use third-party scraper APIs as a workaround.
- Do not commit copied real values to the repository.
- Keep `source`, `source_url`, `confidence` and `notes` in local reviewed CSVs.
- Use diagnostics and validation before activating local CSVs.

## Technical Assessment

- Fits the existing v0.3.0 local reviewed CSV workflow.
- Does not require provider-specific code.
- Does not require app runtime dependency.
- Works through manual entry, validation and diagnostics.
- Should remain separate from automated provider evaluation.

## Data Quality Assessment

- Age quality: useful when manually reviewed.
- Market value methodology: estimated/demand-based; should not be treated as actual transfer fee.
- Contract date quality: useful when manually reviewed and documented.
- Identity matching quality: depends on reviewer accuracy and diagnostics.
- Provenance quality: good if source URL and notes are filled.
- Stale data risk: values can change and should include review notes/date where useful.

## Cost Assessment

- Low direct cost.
- High manual review effort.
- Sustainable for small shortlists, not broad automated coverage.

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Scraping or automated extraction | Legal/terms and reputational risk | Reject automated integration and scraping. |
| Treating market value as transfer fee | Misleading market analysis | Document methodology as estimated/demand-based in notes. |
| Versioning copied values | Redistribution risk | Keep real reviewed CSVs local and ignored by git. |
| Manual entry mistakes | Wrong enrichment values | Use validation, diagnostics and source URLs. |
| Stale values | Outdated Opportunity Finder context | Review dates and notes before use. |

## Decision

- Accept for local/manual reviewed references.
- Reject automated integration and scraping.

## Rationale

Transfermarkt is useful as a public reference for manually reviewed market value and contract-expiry context. It should not become an automated provider integration. The existing local CSV workflow already supports this source type safely when values remain local, documented and validated.

## Next Actions

- Continue using as a manual reference when appropriate.
- Keep `source`, `source_url`, `confidence` and `notes` in reviewed CSV rows.
- Do not use scrapers or third-party scraper APIs.
- Do not version copied real values.
- Run diagnostics before activating local reviewed CSVs.

## Links / References

- [Provider Evaluation Matrix](provider_evaluation_matrix.md)
- [v0.4.0 Provider Evaluation / Licensed Data Integration Plan](../v0_4_0_provider_evaluation_plan.md)
- [Market Context Layer Plan](../market_context_plan.md)
