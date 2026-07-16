# v0.7.0 Initial Provider Candidate Shortlist

## Purpose

This is a preliminary shortlist for deciding which candidate might enter Candidate Intake. It uses only existing project documentation and general source categories already recorded in the repository. It downloads and inspects no payload, performs no current legal review, approves no provider and selects no final candidate.

Treat every license and permission field as `unknown` or `requires review` until the formal workflow confirms it.

Sportmonks has been selected for Candidate Intake only. Its label remains `investigate`; this is not approval, does not complete legal review and does not authorize payload inspection.

## Safety Position

- No payload inspected.
- No terms accepted.
- No license approved.
- No provider selected.
- No integration planned.
- No app activation.
- No scraping.
- No live provider calls.
- No credentials.
- No real data in git.

## Candidate Source Notes

Some names appear because they already exist in historical v0.4.0 decision records. That context is not current approval, current permission or permission to inspect a payload. Every candidate still requires a fresh license and terms gate.

## Initial Shortlist Matrix

| Candidate / Source | Source Type | Intended Use | Expected Useful Fields | Existing Project Context | License Clarity | Local Use | Caching | Derived Outputs | Identity Fit | Market Context Fit | Coverage Expectation | Operational Risk | Open Questions | Initial Label |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| API-Football / API-Sports | Sports performance API | Performance identity context; reassess only if new Market Context evidence exists | Player/team IDs, league, season, performance fields | Existing cached performance pipeline; historical review rejects it as current primary Market Context source | requires current review | requires review | requires review | requires review | Potentially useful IDs; requires formal review | Insufficient in current workflow | Unknown for any new payload | Medium | Current terms/license; cache and derived-output permission; payload format; identity fields; Market Context coverage; refresh process | defer |
| Sportmonks | Structured football data provider candidate | Possible player metadata, identity and contract context | Candidate IDs, player metadata, squads and possible contract fields; all require validation | Historical project review identifies a partial prototype hypothesis, not current approval | requires current review | requires review | requires review | requires review | Potentially promising; unverified | Partial and unverified; market value not confirmed | unknown | Medium | Current terms/license; cache and derived-output permission; payload format; exact identity and Market Context fields; coverage; refresh process | investigate |
| Capology | Salary and contract economics reference/provider candidate | Possible future salary or cost context | Salary/cost and possible contract-related fields; exact semantics unverified | Historical review defers it for core `market_value_eur` | requires current review | requires review | requires review | requires review | unknown | Salary/cost must remain distinct from market value | unknown | High | Current terms/license; cache and derived-output permission; payload format; identity fields; coverage; refresh process; cost semantics | defer |
| Transfermarkt manual reference | Manually reviewed public reference | Manual market value and contract reference | Potential manual age, value and contract references | Historical review permits only a local/manual workflow and rejects scraping or automated integration | requires current review | source-specific review | not assumed | requires review | Manual reviewed matching only | Potential manual reference; no automated payload fit | Manual and selective | High | Current terms/license; manual-use boundaries; derived-output permission; provenance; coverage; refresh process | defer |
| Official club / league public pages | Fragmented official public sources | Manual verification of announcements and squad facts | Possible dates, squad facts or contract announcements depending on source | Historical matrix records fragmented manual verification only | source-specific review | requires review | not assumed | requires review | source-specific | source-specific and incomplete | unknown / fragmented | High | Terms/license for each source; cache and derived-output permission; payload or page format; identity fields; coverage; refresh process | defer |
| User-reviewed manual CSV enrichment | User-controlled local workflow | Manually reviewed Market Context with explicit provenance | Canonical age, market value, contract date, source, confidence and notes when manually supplied | Existing v0.3.0 local enrichment workflow | source-by-source evidence required | local user-controlled file | local only | depends on each cited source | Reviewed player/team/league/season matching | Fits canonical schema when evidence is valid | Manual and selective | Medium | Evidence terms/license; source permissions; identity quality; coverage; refresh and re-review process | investigate |

## Candidate Notes

### API-Football / API-Sports

- **Existing project context:** used in the local cached fixture/player performance pipeline; v0.7.0 assumes no permission or suitability for new Market Context payloads.
- **Potential fit:** IDs, teams, league/season and player performance context.
- **Main unknowns:** current terms, caching, derived outputs and real Market Context coverage.
- **Initial label:** defer pending new evidence and formal review.

### Sportmonks

- **Potential fit:** structured football metadata and identity context.
- **Main unknowns:** current license, permitted storage, derived outputs, available fields, coverage and access burden.
- **Initial label:** investigate, meaning formal review only and not approval.

### Capology

- **Potential fit:** salary, cost and possibly contract-related context.
- **Main unknowns:** license restrictions, redistribution, identity mapping and whether salary/cost semantics must remain separate from canonical market value.
- **Initial label:** defer.

### Transfermarkt Manual Reference

- **Potential fit:** manually reviewed market value and contract reference.
- **Main unknowns:** current manual-use restrictions, redistribution, provenance and whether derived outputs may be stored. Scraping remains prohibited by project policy.
- **Initial label:** defer.

### Official Club / League Public Pages

- **Potential fit:** manual verification of contract announcements, squad facts and dates when source-specific use is permitted.
- **Main unknowns:** heterogeneous formats, source-specific terms, scraping restrictions, review burden and provenance.
- **Initial label:** defer.

### User-Reviewed Manual CSV Enrichment

- **Existing project context:** the v0.3.0 local enrichment workflow already validates reviewed CSVs.
- **Potential fit:** a controlled manual layer when the user supplies traceable and permitted evidence.
- **Main unknowns:** evidence quality, source-specific permission, coverage and refresh process.
- **Initial label:** investigate, without replacing formal source review.

## Recommended First Candidate For Formal Intake

No candidate is selected by this document. The next block must choose exactly one candidate explicitly.

Selection should prioritize:

1. The clearest license path.
2. The strongest identity fields.
3. Useful Market Context fields.
4. The lowest risk of restricted data entering git.
5. A manageable local and offline trial.

## Escalation Rule

Only after a candidate is explicitly chosen:

- Copy the candidate review pack.
- Complete Stage 0 Candidate Intake.
- Begin the License And Terms Gate.
- Do not inspect a payload until the gate permits it.
- Create a decision record if appropriate.

## Relationship To v0.7.0 Matrix

- [Provider Candidate Shortlist Matrix](../v0_7_0_provider_candidate_shortlist_matrix.md)
- [Candidate Review Workflow](../v0_7_0_candidate_review_workflow.md)
- [Candidate Review Pack Template](../v0_7_0_candidate_review_pack_template.md)
- [Provider Decisions](../provider_decisions/README.md)
