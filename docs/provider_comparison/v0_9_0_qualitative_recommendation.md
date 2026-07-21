# v0.9.0 Qualitative Provider Recommendation

## Status

- Milestone: v0.9.0
- Recommendation status: `qualitative-role-outcomes-completed`
- Related protocol: [v0.9.0 Qualitative Provider Recommendation Protocol](v0_9_0_qualitative_recommendation_protocol.md)
- Related protocol decision: [v0.9.0 Qualitative Provider Recommendation Protocol Decision](../provider_decisions/v0_9_0_qualitative_recommendation_protocol_decision.md)
- Related evidence completeness review: [v0.9.0 Provider Evidence Completeness Review](v0_9_0_evidence_completeness_review.md)
- Recommendation execution completed: yes, docs-only
- New research performed: no
- Numeric scoring performed: no
- Weights assigned: no
- Ranking performed: no
- Universal winner selected: no
- Multi-provider architecture recommended: no
- Implementation recommended: no
- Provider approval: none

## Evidence Boundary

- This execution uses only the locked inputs defined by the approved protocol.
- No facts, sources or research were added.
- Outcomes are qualitative and specific to each candidate's supported role.
- `confirmed` does not mean provider approval.
- `unknown`, `restricted` and `conflicting` findings remain unresolved.
- Technical availability and permission to use data remain separate dimensions.

## Candidate Outcomes

| Candidate | Supported Role | Qualitative Outcome | Evidence Basis | Blocking Unknowns | Explicitly Not Approved |
|---|---|---|---|---|---|
| Sportmonks | Automated-provider candidate under clarification. | `continue-targeted-clarification` | Documented player identity and readable labels.<br>Documented position IDs and labels.<br>Documented contract-end field.<br>Public pricing and API workflow information.<br>Existing local scaffold provides limited technical context but does not establish suitability. | Market value.<br>Salary context.<br>Actual field population.<br>Relevant league and plan-level availability.<br>Internal derived-use boundaries.<br>Cache, redistribution and licensing clarification.<br>Production suitability. | Provider approval.<br>API access.<br>Additional cache reading.<br>Trial.<br>Implementation.<br>SQLite or Streamlit integration. |
| API-Football / API-Sports | Existing football-statistics and technical baseline. | `technical-baseline-only` | Documented stable identity.<br>Player, team and competition labels.<br>Age and football-statistics schemas.<br>Existing offline statistics workflow. | Market value.<br>Contract end.<br>Salary context.<br>Cache and retention rights.<br>Redistribution.<br>Internal derived-use rights.<br>Market Context suitability. | Market Context provider role.<br>New provider integration.<br>Additional API access.<br>Provider approval.<br>Implementation changes. |
| Capology | Salary and contract context candidate. | `separate-role-candidate` | Documented salary fields.<br>Documented contract-expiration field.<br>Player identity, age and club/league context.<br>Public methodology and pricing information.<br>Explicit publication and agreement boundaries. | Market value.<br>Jersey coverage.<br>Agreement-specific caching.<br>Internal derived-use rights.<br>Publication and redistribution terms.<br>Exact source certainty and field population. | Complete provider role.<br>Provider approval.<br>API access.<br>Contract or purchase.<br>Implementation.<br>SQLite or Streamlit integration. |
| Transfermarkt manual reference | Reviewed manual market-value and contract reference. | `manual-reference-only` | Publicly visible labels.<br>Positions and jersey references.<br>Age.<br>Market values.<br>Contract references.<br>Public methodology for market values. | Salary context.<br>Formal identifier persistence.<br>Attribution and reuse boundaries.<br>Manual derived-use limits.<br>Structured-data pricing or licensing. | Automated provider role.<br>API assumptions.<br>Scraping.<br>Bulk extraction.<br>Automated caching.<br>Integration.<br>Provider approval. |

## Cross-Candidate Interpretation

- The candidates do not serve the same role.
- Sportmonks retains potential as an automated-provider candidate but requires targeted clarification.
- API-Football remains the technical and statistics baseline, not a demonstrated Market Context solution.
- Capology covers a specialized salary and contract role, subject to agreement and source-certainty limitations.
- Transfermarkt remains useful only within the reviewed manual workflow.
- No candidate resolves every criterion by itself.
- This execution does not select a universal winner.
- A multi-provider architecture is not recommended.
- Apparent complementarity does not become authorization to integrate providers.

## Clarification Candidates

### Sportmonks

A future decision may define a bounded clarification request concerning:

- Field population.
- Market value and salary availability.
- Relevant plan and league coverage.
- Caching and retention.
- Internal derived use.
- Redistribution.
- Permitted implementation boundary.

### Capology

A future decision may define a bounded clarification request concerning:

- Agreement-specific internal use.
- Caching and retention.
- Derived outputs.
- Publication and redistribution.
- League and field coverage.
- Source certainty and estimate semantics.

This block does not authorize provider contact. Each possible request requires a separate decision, and the two requests must not be grouped automatically.

## Deferred Or Stopped Paths

- No candidate receives `stop-exploration`.
- No candidate receives `defer`.
- Further API-Football work for Market Context is paused under `technical-baseline-only`.
- Transfermarkt automation remains excluded under `manual-reference-only`.
- Sportmonks and Capology do not advance beyond their recorded outcomes without new decisions.

## Manual-Reference Boundary

- Transfermarkt remains limited to reviewed manual reference.
- No scraping.
- No bulk extraction.
- No automation.
- No integration.
- Market values are not objective transfer fees.
- Any future manual data must follow the existing reviewed local workflow and require its own decision where applicable.

## Safety And Governance Boundary

- No new research.
- No login.
- No accounts.
- No private dashboards.
- No API calls.
- No provider cache.
- No raw JSON.
- No payloads.
- No scraping.
- No `.local.csv`.
- No SQLite.
- No Streamlit.
- No implementation.
- No scoring.
- No weights.
- No ranking.
- No universal winner.
- No provider approval.

## Final Qualitative Conclusion

- Sportmonks: `continue-targeted-clarification`.
- API-Football / API-Sports: `technical-baseline-only`.
- Capology: `separate-role-candidate`.
- Transfermarkt: `manual-reference-only`.

These outcomes are specific to each candidate's role. They do not constitute a ranking, automatic selection, provider approval, implementation authorization or authorization for a multi-provider solution.

## Next Decision Boundary

The next docs-only decision must choose exactly one of these paths:

1. Define a clarification request for Sportmonks.
2. Define a clarification request for Capology.
3. Close v0.9.0 with every provider remaining unapproved.
4. Stop further action and retain only the documented outcomes.

This document does not choose a path. It does not automatically authorize new research, provider contact, API calls, cache reading, a trial, implementation or provider approval.
