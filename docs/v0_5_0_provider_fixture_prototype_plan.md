# v0.5.0 - Provider Fixture Prototype Plan

## Objective

v0.5.0 aims to prototype an offline provider integration flow with synthetic fixtures or licensed/permitted payload samples. The milestone keeps the no-scraping rule, avoids live provider calls from the app and continues routing provider-derived data through local validation, preview and diagnostics.

## Scope

- synthetic or licensed provider fixture payloads;
- mapping provider IDs to local dataset entities;
- traceability through `provider_player_id`, `provider_team_id` and `provider_name`;
- transformation to canonical Market Context;
- validation, preview and diagnostics;
- opt-in activation through environment variable.

## Out of Scope

- scraping;
- live calls from the app;
- real provider work without reviewed license terms;
- versioning real provider dumps;
- changing scoring with low coverage;
- automating data purchase or download.

## Proposed Workflow

```text
provider decision record
  -> fixture payload review
  -> identity mapping
  -> normalized records
  -> canonical builder
  -> preview
  -> diagnostics
  -> app activation
```

## Acceptance Criteria

- Mapping contract documented.
- Synthetic mapping sample versioned.
- Provider identity mapping validator added.
- No real data.
- No real provider integrated.
- No functional app changes.
- Mapping is not applied to provider fixtures yet.

## Risks

- Provider IDs may be incomplete.
- Team changes can vary by season.
- Names may be ambiguous.
- Duplicate players can appear across teams or competitions.
- Name-based matching is risky.
- Licenses may restrict caching, redistribution or screenshots.
