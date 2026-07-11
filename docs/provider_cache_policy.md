# Provider Cache Policy

## Objective

Define how Football Scout Dashboard should handle local provider caches before any licensed data integration is implemented.

The cache policy protects credentials, licensed data and reproducibility while preserving the existing architecture:

```text
provider raw fetch -> local cache -> canonical transform -> validation -> diagnostics -> opt-in activation
```

The Streamlit app should never depend on live provider calls at runtime.

## Principles

- Keep provider integrations local, explicit and auditable.
- Do not commit credentials, API keys or private tokens.
- Do not commit raw provider payloads.
- Do not commit real provider-derived canonical outputs unless terms explicitly allow redistribution.
- Prefer local cache replay over repeated provider calls.
- Validate and diagnose canonical outputs before app activation.
- Keep the app usable without market context.
- Respect provider terms before fetching, caching, transforming or displaying data.

## What Can Be Cached

Only if provider terms allow it:

- raw API responses for local development;
- provider export files used for transformation;
- request/response metadata needed for debugging;
- canonical market context CSVs for local review;
- diagnostic logs without credentials or restricted payloads.

## What Must Not Be Cached

- API keys;
- bearer tokens;
- account credentials;
- private pricing contracts;
- restricted payloads when caching is not permitted;
- provider dumps intended for redistribution;
- copied data that licensing does not allow storing locally;
- screenshots or exports that violate provider terms.

## Local-Only Data

Local-only data should stay outside git. This includes:

- raw provider payloads;
- paid provider exports;
- reviewed market context CSVs containing real values;
- generated canonical provider outputs unless redistribution is explicitly allowed;
- logs that include provider response details.

## Git Policy

Do not version provider cache folders.

If provider cache implementation is added later, `data/provider_cache/` should be ignored by git.

Versionable files should be limited to:

- synthetic fixtures;
- empty templates;
- documentation;
- code;
- tests using synthetic data only.

## Credentials Policy

- Never commit credentials.
- Never paste API keys into docs.
- Never store credentials in cached request logs.
- Prefer environment variables or a local secrets mechanism.
- Keep `.env.example` as a template only.
- Rotate any credential that is accidentally exposed.

## Raw Payload Policy

Raw provider payloads may be useful for debugging and transform development, but they are high-risk from a licensing perspective.

Rules:

- cache raw payloads only if terms permit it;
- keep raw payloads local and ignored;
- do not attach raw payloads to issues or release artifacts;
- do not use raw payloads as test fixtures unless they are synthetic or explicitly redistributable;
- record enough metadata to know provider, endpoint, date and parameters without leaking secrets.

## Canonical Output Policy

Canonical outputs should feed the Market Context Layer, not bypass it.

Minimum canonical schema:

```text
player,team,league,season,age,market_value_eur,contract_end_date,source,source_url,confidence,notes
```

Canonical outputs with real provider data should remain local unless redistribution is explicitly permitted.

Before activation:

- run schema validation;
- run value validation;
- run diagnostics;
- review coverage;
- review duplicate keys;
- confirm source/confidence/notes are present where needed.

## Retention And Refresh

Retention should be conservative:

- keep only payloads needed for reproducibility or debugging;
- delete stale raw payloads when no longer needed;
- refresh provider data explicitly, not implicitly at app runtime;
- record fetch dates and value dates when available;
- rerun diagnostics after refreshes.

## Provider Terms Review

Before caching any provider data, review:

- local/private use rights;
- redistribution rights;
- caching permission;
- attribution requirements;
- screenshot/demo restrictions;
- rate limits;
- paid plan restrictions;
- data retention limits.

If terms are unclear, do not cache or integrate the provider.

## Recommended Folder Structure

If provider cache implementation is added later:

```text
data/
  provider_cache/
    <provider_name>/
      raw/
      canonical/
      logs/
```

`data/provider_cache/` should be ignored by git if this structure is implemented.

## Verification Checklist

- [ ] Provider terms reviewed.
- [ ] Caching explicitly allowed or kept out of scope.
- [ ] No credentials in files.
- [ ] Raw payloads ignored by git.
- [ ] Real canonical outputs ignored by git unless redistribution is allowed.
- [ ] Synthetic fixtures used for tests.
- [ ] Canonical output validates against Market Context Layer rules.
- [ ] Diagnostics reviewed before activation.
- [ ] App works without provider cache.
