# v0.9.0 Provider Public Research Protocol

## Status

- Milestone: v0.9.0
- Protocol status: `public-source-research-protocol-completed`
- Related provider comparison plan: [v0.9.0 Provider Comparison Plan](v0_9_0_provider_comparison_plan.md)
- Related comparison scope decision: [v0.9.0 Provider Comparison Scope Decision](provider_decisions/v0_9_0_provider_comparison_scope_decision.md)
- Related protocol decision: [v0.9.0 Provider Public Research Protocol Decision](provider_decisions/v0_9_0_provider_public_research_protocol_decision.md)
- Candidate set locked: yes
- Future public web research approved: no, the existing authorization has been fulfilled
- Research performed under this protocol: yes
- Research block completed: yes
- Evidence completeness review completed: yes
- Login or private dashboard access approved: no
- Account creation approved: no
- API calls approved: no
- Provider cache reading approved: no
- Automated scraping approved: no
- Implementation approved: no
- Provider approval: none

## Purpose

The protocol defines how current public facts will be collected, classified and compared for the four selected candidates.

Future research must determine what is publicly verifiable about:

- identity and labels;
- position and jersey coverage;
- Market Context fields;
- competition coverage;
- freshness;
- pricing and public plan limits;
- licensing and permitted use;
- local workflow fit;
- integration complexity.

This protocol does not contain current provider findings.

## Locked Candidate Set

| Candidate | Research Role | Boundary |
|---|---|---|
| Sportmonks | Main evaluated candidate from v0.8.0 | Public pages only; no account, dashboard, API or cache |
| API-Football / API-Sports | Existing technical baseline | Public documentation only; existing statistics integration does not imply Market Context approval |
| Capology | Salary and contract context candidate | Public pages only; no bulk extraction or automated access |
| Transfermarkt manual reference | Manual market and contract reference | Manual-reference assessment only; no scraping, API assumptions or automated integration |

- No new candidate may be added in the research block.
- Any new provider requires a separate scope decision.
- Inclusion does not imply approval.
- Sportmonks receives no scoring advantage from the existing scaffold.

## Allowed Public Sources

### Tier 1: authoritative official sources

- Official product documentation.
- Official API documentation available without login.
- Official coverage pages.
- Official pricing and public plan pages.
- Official help centre or FAQ pages.
- Official terms of service.
- Official licensing or data-use pages.
- Official attribution guidance.
- Official public changelogs.
- Official company pages describing field availability.

### Tier 2: official public marketing pages

These sources may support only:

- product positioning;
- advertised coverage;
- advertised capabilities;
- publicly stated plan descriptions.

Marketing claims must be classified as `advertised`, not as technically confirmed capability, unless additional official documentation supports them.

### Tier 3: secondary public sources

These sources may be used only as context:

- reputable journalism;
- reputable technical reviews;
- public community discussions;
- public comparison articles.

They:

- must never be the primary source for licensing, permitted use, contractual pricing or field guarantees;
- must be classified as `secondary-context`;
- cannot turn an unknown fact into a confirmed one.

## Forbidden Sources And Access

- Private dashboards.
- Authenticated provider pages.
- Account-specific plan screens.
- Trial accounts.
- Newly created accounts.
- API calls.
- SDK execution.
- Downloaded payloads.
- Browser developer tools used to inspect hidden responses.
- Automated scraping.
- Bulk page extraction.
- Provider cache.
- Raw JSON.
- Credentials.
- `.env`.
- Affiliate blogs as primary evidence.
- Copied legal text beyond short necessary summaries.

## Research Date And Freshness

Every evidence item must record:

- exact consultation date in `YYYY-MM-DD`;
- page title;
- provider or publisher;
- public URL;
- source tier;
- whether the fact is likely to change;
- the date shown by the source, if available;
- whether the finding is current, historical or unclear.

Pricing, plans, field coverage, competition coverage and licensing must always be treated as time-sensitive. They require current public verification during the future research block and must not rely only on repository memory.

## Evidence Classification

Use only these classifications:

- `confirmed`: explicitly supported by an authoritative public source.
- `advertised`: stated on an official marketing page but not technically verified.
- `partial`: some aspect is confirmed but material gaps remain.
- `unknown`: no reliable public evidence found.
- `not-available`: an authoritative source explicitly indicates absence.
- `not-applicable`: the criterion does not apply to the candidate.
- `restricted`: public evidence indicates access or use is restricted.
- `conflicting`: reliable public sources materially disagree.

Every finding must distinguish:

- `fact`;
- `inference`;
- `open-question`.

Inferences must cite the supporting facts and use explicit inference language.

## Evidence Requirements Per Claim

Every claim must include:

- candidate;
- criterion;
- concise claim;
- classification;
- fact / inference / open-question;
- source title;
- source publisher;
- public URL;
- consultation date;
- source tier;
- concise paraphrased evidence;
- freshness risk;
- limitations;
- conflict note if applicable.

Copy no more source text than necessary. Do not include payloads, player data or examples involving real people unless indispensable to confirm a public structure; even then, avoid individual values.

## Comparison Areas

1. Identity stability.
2. Human-readable player labels.
3. Team and competition labels.
4. Position IDs and labels.
5. Jersey coverage.
6. Player age.
7. Market value.
8. Contract end date.
9. Salary or compensation context.
10. Relevant league coverage.
11. Freshness and update cadence.
12. Provenance.
13. Licensing clarity.
14. Internal derived-use clarity.
15. Attribution requirements.
16. Redistribution restrictions.
17. Local/cache-first workflow fit.
18. Identity mapping complexity.
19. Integration complexity.
20. Current public pricing or plan limits.

## No-Scoring Policy

- The first public research pass uses no numeric scores.
- No weights are assigned.
- No overall ranking is produced.
- No winner is selected.
- The draft comparison matrix uses evidence classifications only.
- Numeric scoring requires a later separate decision after evidence completeness is reviewed.

Unknowns and marketing claims must not be converted into artificial numeric precision.

## Approved Research Outputs

The completed approved block created only:

- `docs/provider_comparison/evidence/sportmonks_public_evidence.md`
- `docs/provider_comparison/evidence/api_football_public_evidence.md`
- `docs/provider_comparison/evidence/capology_public_evidence.md`
- `docs/provider_comparison/evidence/transfermarkt_manual_public_evidence.md`
- `docs/provider_comparison/v0_9_0_provider_comparison_matrix.md`
- `docs/provider_comparison/v0_9_0_public_research_summary.md`

No recommendation decision, provider approval, scoring or code was created.

## Research Execution Order

1. Verify official source availability for every candidate.
2. Research governance and licensing first.
3. Research field and coverage claims second.
4. Research pricing and plan limits third.
5. Populate candidate evidence notes.
6. Populate the comparison matrix.
7. Record unknowns and conflicts.
8. Stop before making a recommendation.

## Stop Conditions

Stop the future research block if:

- a required source needs login;
- current official facts cannot be verified;
- legal or permitted-use meaning remains materially ambiguous;
- research would require an API call;
- research would require provider cache;
- research would require raw JSON;
- research would require automated scraping;
- a new provider becomes necessary;
- a candidate cannot be evaluated without account creation;
- scoring or ranking begins;
- any provider is described as approved;
- confidential or account-specific information appears.

A stop condition may affect only one criterion or candidate. In that case, record `unknown`, `restricted` or `conflicting` instead of improvising.

## Verification Requirements For Future Research

The future block must:

- provide full diffs;
- record every consulted public URL in the evidence files;
- report consultation dates;
- confirm no login or private dashboard access;
- confirm no API calls;
- confirm no cache reading;
- confirm no raw JSON;
- confirm no scraping;
- run `git diff --check`;
- show `git status --short`;
- show ignored provider cache status;
- make no commit before review.

## Next Required Action

A separate docs-only decision may define a qualitative recommendation protocol.

This protocol no longer authorizes further research automatically. Any new research requires another decision. Scoring, ranking, recommendation execution, implementation and provider approval remain blocked.
