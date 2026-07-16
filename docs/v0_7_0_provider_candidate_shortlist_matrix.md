# v0.7.0 Provider Candidate Shortlist Matrix

## Purpose

This matrix supports comparison of potential candidates before one is selected for formal review. It does not select, approve or reject a provider by itself. It does not replace the payload checklist, candidate review pack or decision record, and it does not authorize real payload inspection or local experiments.

Its only purpose is to determine whether a candidate merits Candidate Intake.

## How To Use

1. Add only candidates with an identifiable source.
2. Do not download or inspect real payloads during this phase.
3. Use public information or information already permitted for review.
4. Record uncertainty as `unknown`.
5. Do not invent pricing, terms, fields or permissions.
6. Select at most one candidate to enter the formal workflow.
7. If legal or licensing questions remain material, label the candidate `defer` or `reject`.

## Decision Labels

- **investigate:** merits formal review but is not approved.
- **defer:** critical information is missing before review can begin.
- **park:** not a current priority.
- **reject:** does not fit or has a clear blocker.
- **unknown:** available information is insufficient.

## Evaluation Criteria

| Criterion | What To Check | Preferred Signal | Risk Signal |
|---|---|---|---|
| License clarity | Whether terms and license source are identifiable | Clear, current and applicable terms | Missing, ambiguous or conflicting terms |
| Local development permission | Whether local evaluation is allowed | Explicit local or development use | Local use forbidden or unknown |
| Caching permission | Whether payloads may be cached locally | Explicit, bounded local caching | Caching forbidden or unclear |
| Derived output permission | Whether normalized or canonical outputs are allowed | Derived outputs explicitly permitted | Derivatives forbidden or undefined |
| Redistribution restrictions | Limits on sharing payloads and outputs | Restrictions are clear and compatible | Broad or unclear restrictions |
| Identity fields availability | Stable player, team and competition identifiers | Stable IDs with documented semantics | Names only or unstable identifiers |
| Team/season mapping fit | Ability to map records in team and season context | Team- and season-aware identity | Missing team or season context |
| Market value availability | Presence and meaning of market value | Dated, sourced value with clear semantics | No value or unclear methodology |
| Contract end date availability | Presence and precision of contract end | ISO-compatible, sourced date | Inferred, partial or absent date |
| Age/birthdate availability | Presence and reliability of age context | Sourced birthdate or valid age | Missing or inconsistent age |
| Source/provenance quality | Traceability of each field | Field-level source and review date | Missing provenance |
| Currency/date clarity | Currency and date formats | Explicit currency and ISO dates | Ambiguous currency or date semantics |
| Coverage expectation | Expected useful population coverage | Broad, measurable coverage | Unknown or highly selective coverage |
| Cost or access burden | Sustainable access requirements | Clear and sustainable access | Unclear or excessive burden |
| Operational complexity | Authentication, pagination and refresh effort | Documented, bounded workflow | Fragile or opaque workflow |
| Data freshness | Update cadence and value dates | Dated data with known cadence | Stale or undated data |
| Manual review burden | Expected human verification effort | Reviewable sample and clear exceptions | High unresolved manual workload |
| Fit with existing canonical Market Context | Ability to map required canonical fields | Direct, traceable field mapping | Major semantic mismatch |
| Risk of accidental data versioning | Ease of keeping data local and ignored | Clear local storage and cleanup | Outputs likely to enter git accidentally |

## Shortlist Matrix Template

| Candidate | Source Type | Intended Use | License Clarity | Local Use | Caching | Derived Outputs | Identity Fit | Market Context Fit | Coverage Expectation | Cost/Access Burden | Operational Risk | Open Questions | Proposed Label |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Candidate A | unknown |  | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown |  | unknown |
| Candidate B | unknown |  | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown |  | unknown |
| Candidate C | unknown |  | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown |  | unknown |

## Scoring Guidance

This matrix is qualitative. Do not total points when legal or licensing blockers exist. License clarity takes precedence over technical fit, and a technically strong candidate with doubtful permissions must be deferred or rejected. A candidate may enter formal review only with the `investigate` label.

## Minimum Bar For Candidate Intake

- Candidate or source is identified.
- Terms or license source is identified.
- Intended use is documented.
- No obvious prohibition has been found.
- No payload has been downloaded unless permission was already confirmed.
- Open questions are documented.

## Escalation To Formal Review

When a candidate receives `investigate`, the next block must:

- Copy the candidate review pack.
- Complete Candidate Intake.
- Begin the License And Terms Gate.
- Create or prepare a decision record only if appropriate.
- Keep all real payload material outside git.

## Safety Rules

- No real payloads in git.
- No raw provider dumps.
- No credentials.
- No scraping.
- No live provider calls.
- No app activation.
- No SQLite writes.
- No `.local.csv` committed.
- No `data/provider_cache/` contents committed.
- Final git status must be clean.

## Relationship To Other Docs

- [v0.7.0 Permitted Provider Candidate Review Plan](v0_7_0_permitted_provider_candidate_review_plan.md)
- [v0.7.0 Candidate Review Workflow](v0_7_0_candidate_review_workflow.md)
- [v0.7.0 Candidate Review Pack Template](v0_7_0_candidate_review_pack_template.md)
- [Provider Payload Evaluation Checklist](provider_payload_evaluation_checklist.md)
- [Provider Payload Evaluation Template](provider_decisions/provider_payload_evaluation_template.md)
