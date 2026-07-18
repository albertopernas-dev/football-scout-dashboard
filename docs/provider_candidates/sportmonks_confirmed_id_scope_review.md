# Sportmonks Confirmed ID Scope Review

## Status

- Candidate: Sportmonks
- Review status: passed
- Related minimal ID discovery summary: [Sportmonks Minimal ID Discovery Summary](sportmonks_minimal_id_discovery_summary.md)
- Related ID discovery plan: [Sportmonks ID Discovery Plan](sportmonks_id_discovery_plan.md)
- Related credential verification: [Sportmonks Local Credential Setup Verification](sportmonks_local_credential_setup_verification.md)
- Minimal payload field review decision: [approved for a future minimal review](../provider_decisions/sportmonks_minimal_payload_field_review_decision.md)
- Provider approval: no
- IDs confirmed: yes
- Broad payload inspection performed: no
- Additional API calls performed in this block: no
- Raw responses reviewed in this block: no
- Provider cache committed: no
- SQLite writes performed: no
- Streamlit activation performed: no
- Parser/transform code created: no

## Confirmed IDs

| Item | Value | Status |
|---|---|---|
| League | Denmark Superliga | confirmed |
| League ID | `271` | confirmed |
| Season | 2026/2027 | confirmed |
| Season ID | `27897` | confirmed |
| Team | FC København | confirmed |
| Team ID | `85` | confirmed |
| Candidate endpoint | Team Squad by Team and Season ID | access confirmed |
| Endpoint result | HTTP 200; data present; 6 entries | confirmed |

## Review Notes

- The confirmed IDs are sufficient for a later minimal payload field review decision.
- This review does not inspect payload fields.
- This review does not approve Sportmonks as a provider.
- This review does not authorize broad payload pulls.
- This review does not authorize SQLite writes, Streamlit integration or parser/transform code.
- Any future field review must be a separate explicit block with its own scope and stop conditions.

## Boundaries For Later Minimal Payload Field Review

- Maximum scope should remain one endpoint, one team and one season.
- Raw responses must remain under ignored local provider cache only.
- The review may inspect field names or categories, but must not build integration code.
- It must not transform provider data into canonical app tables.
- It must not create `.local.csv` outputs unless explicitly approved later.
- It must not write SQLite.
- It must not activate Sportmonks in Streamlit.
- It must not approve Sportmonks.

## Still Forbidden

- Do not commit `.env`.
- Do not commit the API token.
- Do not commit raw JSON.
- Do not commit provider cache.
- Do not perform broad payload inspection.
- Do not perform the local trial.
- Do not write to SQLite.
- Do not activate Streamlit.
- Do not create parser or transform code.
- Do not approve Sportmonks.

## Next Required Action

A later explicit block may execute the minimal payload field review under the [approved decision](../provider_decisions/sportmonks_minimal_payload_field_review_decision.md).

No API calls are performed or granted by the current docs-only block.
