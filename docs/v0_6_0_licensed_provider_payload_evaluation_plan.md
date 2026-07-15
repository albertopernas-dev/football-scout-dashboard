# v0.6.0 - Licensed Provider Payload Evaluation Plan

## Objective

v0.6.0 evaluates permitted or licensed provider payloads, or advanced synthetic fixtures, before any real provider integration is implemented.

The milestone does not allow scraping, live provider calls from the app, credentials in the repository or versioned real provider dumps. No real provider is connected yet. Any real payload must be permitted by its license and terms, and must remain local and ignored unless redistribution is explicitly allowed.

## Why This Milestone Exists

v0.4.0 established the provider-to-Market Context evaluation and transformation workflow. v0.5.0 demonstrated that workflow with synthetic provider fixture records and reviewed identity mappings. v0.6.0 determines whether a permitted payload can fit that contract without compromising licensing, repository safety or data traceability.

## Scope

- Evaluate the shape and schema of permitted or licensed payloads.
- Document coverage for provider IDs, player, team, league and season.
- Review availability and semantics of `age`, `market_value_eur` or an equivalent value, and `contract_end_date`.
- Review provenance fields such as `value_date`, `fetched_at`, `source`, `source_url` and `confidence`.
- Evaluate license terms for local use, caching, derived outputs, redistribution and screenshots.
- Assess a local, ignored identity mapping strategy.
- Run a local and offline transform experiment when the data terms allow it.
- Keep real outputs in `.local.csv` files or ignored local paths.

## Out of Scope

- Scraping.
- Automatic provider fetching.
- Live calls from Streamlit or the app.
- Committing real provider dumps.
- Publishing data under restrictive terms.
- Changing scoring with insufficient coverage.
- Adding provenance UI before the flow and coverage are validated.

## Proposed Workflow

```text
provider candidate
  -> decision record update
  -> license and terms review
  -> payload sample review
  -> payload shape notes
  -> identity mapping assessment
  -> local ignored transform experiment
  -> canonical Market Context validation
  -> diagnostics
  -> decision: accept, defer or reject
```

## Acceptance Criteria

- The v0.6.0 plan is documented.
- A provider payload evaluation checklist exists.
- A payload-specific decision record template exists.
- A completed synthetic payload evaluation example exists.
- An advanced synthetic payload shape example exists.
- A synthetic-only flattening helper can flatten the advanced synthetic payload shape.
- This helper does not constitute real provider integration or a real provider parser.
- ROADMAP identifies v0.6.0 as the current milestone.
- Only synthetic-only helper code is added; no app activation, real provider integration code or network workflow is added.
- No real data is versioned.
- No real provider is integrated.
- No real payload has been evaluated; the synthetic example does not approve or evaluate any real provider payload.

## Risks

- Restrictive or unclear licensing.
- Payloads that do not cover useful Market Context fields.
- Provider values that are not equivalent to market value.
- Inconsistent provider IDs.
- Team and season changes that complicate identity mapping.
- Caching or redistribution restrictions.
- Public screenshot or demo restrictions.
- Unsustainable costs or rate limits.
- Insufficient provenance.

Use the [Provider Payload Evaluation Checklist](provider_payload_evaluation_checklist.md) before accepting any payload for a transform experiment.
