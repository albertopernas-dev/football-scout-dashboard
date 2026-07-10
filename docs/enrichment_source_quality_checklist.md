# Enrichment Source Quality Checklist

## Objective

Use this checklist to decide whether a market context enrichment row is reliable enough to use in Football Scout Dashboard.

The goal is not to maximize coverage at any cost. The goal is to add traceable, reviewable context without creating false precision.

## Source Confidence Categories

### High Confidence

Use `high` when the value comes from a source with strong traceability and low ambiguity.

Examples:

- official club or league source;
- official contractual documentation when applicable;
- licensed or reviewed dataset with clear methodology;
- reliable public source with clear publication date and explicit value;
- manually reviewed value confirmed consistently across trusted sources.

### Medium Confidence

Use `medium` when the value is likely usable but has some dependency on interpretation or a secondary source.

Examples:

- reputable aggregator with reasonable consistency;
- reliable media source citing concrete data;
- manual cross-check across multiple sources that broadly agree;
- source with clear date but limited methodology.

### Low Confidence

Use `low` when the value is useful for exploration but should not drive decisions on its own.

Examples:

- partial data;
- secondary source;
- estimate rather than confirmed value;
- source without a clear date;
- discrepancy between sources;
- manually reviewed but uncertain match.

### Rejected

Do not use these values in enrichment CSVs.

Examples:

- rumours;
- social media posts without a traceable source;
- unauthorized scraping;
- data without provenance;
- invented values;
- values copied without knowing source date or meaning.

## Age Rules

- Age must have a traceable source.
- Age must be an integer in the 15-45 range.
- Do not use `0` for unknown age.
- If the player identity is ambiguous, leave age empty.
- If sources disagree and the correct value cannot be resolved, leave age empty or use `low` confidence with clear notes.

## Market Value Rules

- Do not use `0` for unknown market value.
- Unknown market value must be empty.
- Market value must be a positive number in euros.
- Notes should clarify whether the value is a published value, estimate or reviewed approximation.
- Prefer consistent market value sources within the same CSV.
- Do not mix incompatible valuation methodologies without documenting the difference.

## Contract End Date Rules

- Use strict ISO format: `YYYY-MM-DD`.
- Do not use formats such as `DD/MM/YYYY`.
- Do not infer contract end dates without a source.
- If only year or month is known, document that in `notes` or leave the field empty.
- If extension clauses or options create ambiguity, document them in `notes`.
- If sources disagree, leave empty or use low confidence with clear explanation.

## Confidence Rules

- `high`: official, licensed, reviewed or strongly traceable value.
- `medium`: reputable but not fully official, or cross-checked from secondary sources.
- `low`: partial, estimated, ambiguous or exploratory value.
- `source` and `confidence` are required when `age`, `market_value_eur` or `contract_end_date` is filled.
- Empty confidence is allowed only when no enrichment values are filled.

## Notes Rules

Use `notes` to make review decisions auditable.

Good notes include:

- source date;
- reason for confidence level;
- source description when `source_url` is empty;
- differences between sources;
- identity or team-name ambiguity;
- assumptions made during manual review.

Avoid notes that only repeat the value without context.

## Checklist Before Activating A CSV

- [ ] Validation errors = 0.
- [ ] Duplicate keys = 0.
- [ ] `matched_pct` reviewed.
- [ ] Effective age coverage reviewed.
- [ ] Effective market value coverage reviewed.
- [ ] Effective contract coverage reviewed.
- [ ] Sources reviewed.
- [ ] Unknown values are empty, not `0`.
- [ ] No rejected sources are present.
- [ ] Low-confidence values are documented in `notes`.
- [ ] The CSV is activated explicitly with `FOOTBALL_SCOUT_MARKET_CONTEXT_CSV`.

## Final Rule

If a value cannot be traced, leave it empty.
