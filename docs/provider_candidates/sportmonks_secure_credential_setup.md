# Sportmonks Secure Credential Setup

## Status

- Candidate: Sportmonks
- Credential setup status: verified/local-only
- Local credential setup verification: [passed](sportmonks_local_credential_setup_verification.md)
- Related ID discovery plan: [Sportmonks ID Discovery Plan](sportmonks_id_discovery_plan.md)
- Related trial scope plan: [Sportmonks Ignored Local Trial Scope Plan](sportmonks_ignored_local_trial_scope_plan.md)
- Related decision record: [Sportmonks Payload Decision Record](../provider_decisions/sportmonks_payload_decision_record.md)
- Provider approval: no
- Credentials created locally: yes, outside Git
- Credentials stored in Git: no
- API calls performed: no
- Payload inspection performed: no
- Provider cache created: no
- Local trial performed: no
- SQLite writes performed: no
- Streamlit activation performed: no
- Parser/transform code created: no

## Purpose

This document defines how a Sportmonks API token may be stored locally before future minimal ID discovery. It does not create or record a real token and does not call the API.

It keeps credentials outside Git and records the safety checks used to verify the manually created local `.env`.

## Credential Storage Decision

| Item | Decision | Status |
|---|---|---|
| Credential name | `SPORTMONKS_API_TOKEN` | configured locally |
| Storage file | Local `.env` or equivalent ignored local configuration | verified/local-only |
| Committed example value | none | fixed |
| Real token in Git | forbidden | fixed |
| Token in docs | forbidden | fixed |
| Token in shell history | avoid where possible | caution |
| Token in screenshots | forbidden | fixed |
| Token in logs | forbidden | fixed |

## Required Git Ignore Coverage

The local `.env` file must be ignored. Local environment or configuration variants must also be ignored before use, while safe example files may remain tracked. Provider cache paths and `.local.csv` outputs must remain ignored.

- [x] `.env` ignored.
- [ ] `.env.*` or equivalent local environment variants ignored if introduced, while allowing safe example files already in use.
- [x] `data/provider_cache/` ignored.
- [x] `data/enrichment/*.local.csv` ignored.
- [x] No credential appears in tracked files.
- [x] No credential appears in `git diff`.
- [x] `git status --short` does not show local credential files.

The current `.gitignore` already covers `.env`, provider cache and local enrichment CSV outputs, so no ignore change is required in this block. Any future alternative credential filename must be checked before use.

## Local Setup Instructions

The user created the ignored local `.env` file manually. The placeholder below remains only as a safe reference and does not contain the real token.

```text
# Create or update local ignored .env file only.
# Do not commit this file.
SPORTMONKS_API_TOKEN=<paste-token-locally-only>
```

Do not paste the real token into ChatGPT, Git, docs, commits, screenshots or terminal output shared publicly.

Do not run API commands or create provider cache in this block.

## Pre-Credential Safety Checks

```powershell
git status --short
git check-ignore .env
git check-ignore data/provider_cache/
git ls-files | Select-String -Pattern "\.env$|secret|credential|token|api_key|apikey"
```

`git check-ignore .env` should confirm that `.env` is ignored. The `git ls-files` check should not reveal tracked secret files. If any secret-like tracked file appears, stop and review it before proceeding.

## Post-Credential Safety Checks

```powershell
git status --short
git diff -- .env
git check-ignore .env
```

The local `.env` file must not appear in `git status --short`, and `git diff -- .env` must not show token contents. If `.env` appears as tracked or modified, stop immediately.

## Required Before ID Discovery API Calls

- `.env` or local configuration created outside Git.
- `SPORTMONKS_API_TOKEN` stored only locally.
- `git check-ignore .env` confirms ignore coverage.
- `git status --short` does not show `.env`.
- Raw payload path confirmed ignored.
- Cache path confirmed ignored.
- User explicitly confirms readiness for a separate minimal ID discovery block.
- No API calls made during credential setup.

## Stop Conditions

- The token appears in Git.
- The token appears in docs.
- The token appears in terminal output that will be shared.
- `.env` appears in `git status --short`.
- `git diff` displays token contents.
- Provider cache appears in Git.
- Any raw API response appears in Git.
- The user is unsure whether the token is exposed.

## Still Forbidden In This Block

- Do not paste the real token into this repository.
- Do not paste the real token into ChatGPT.
- Do not call Sportmonks APIs.
- Do not inspect payloads.
- Do not create provider cache.
- Do not create `.local.csv` files.
- Do not write to SQLite.
- Do not activate Streamlit.
- Do not create parser or transform code.
- Do not approve Sportmonks.

## Next Required Action

Local credential setup has been verified outside Git. The next separate explicit block may run minimal ID discovery and must only discover `season_id`, `team_id` and endpoint access using minimal requests.
