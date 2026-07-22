# Roadmap

## Current Status

- SQLite local funciona como fuente principal.
- LaLiga 2024 esta cargada desde payloads locales de API-Football `fixtures/players`.
- La app incluye ranking recomendado, filtros de comparabilidad y muestra, Opportunity Finder, descargas CSV, informes HTML y documentacion de scoring.
- v0.2.0 incluye una capa opt-in de Market Context para CSV manual, validacion, diagnostico, cobertura efectiva y uso de `effective_*` en Opportunity Finder.
- v0.3.0 completa el workflow local de enrichment real revisado: seed export, checklist de fuentes, safeguards, validacion estricta y display efectivo en Opportunity Finder.
- v0.4.0 completa el workflow de evaluacion de proveedores: decision records, matriz, politica de cache, contrato de transformacion, preview CLI, builder canonico y ejemplos sinteticos.
- v0.5.0 completa Provider Fixture Prototype como demo sintetico offline: validacion y aplicacion de identity mapping, CLI de records mapeados, builder canonico y preview.
- v0.6.0 publicada con governance de evaluacion, payload avanzado sintetico, flattening local y demo end-to-end sintetica hacia Market Context canonico.
- v0.7.0 completada y publicada como milestone documental/de gobernanza; Sportmonks sigue en `defer` y sin aprobacion.
- v0.8.0 completada y publicada; Sportmonks sigue sin aprobacion.
- v0.9.0 es el milestone actual para revisar provider suitability mediante comparacion descriptiva.
- El contexto de mercado real depende de CSVs revisados localmente; no hay scraping ni proveedor automatico conectado.

## Recommended Next Steps

1. Complete a separate v0.9.0 release/tag block.
2. Select any future milestone or provider path through a separate decision.
3. Keep provider contact, login, dashboards, API calls, cache reading, trials, implementation, scoring, ranking and provider approval blocked.

## v0.2.0 Market Context Layer

- Implementado para workflow manual/CSV opt-in.
- Incluye schema, validacion, merge helpers, diagnostico CLI, template/sample CSV y cobertura visible.
- La app muestra columnas `market_context_*` y cobertura efectiva.
- Opportunity Finder usa `effective_age`, `effective_market_value_eur` y `effective_contract_end_date` cuando existen valores validos.
- El scoring general permanece sin cambios.
- Pendiente: incorporar datos reales de enrichment y revisar pesos de oportunidad cuando haya cobertura suficiente.
- Plan detallado: [`docs/market_context_plan.md`](docs/market_context_plan.md).

## v0.3.0 Real Enrichment Workflow

- Implementado para workflow local/manual.
- Permite crear un seed CSV desde Opportunity Finder.
- Incluye checklist de calidad de fuentes.
- Protege CSVs revisados frente a sobrescritura accidental.
- Endurece validacion de `age`, `market_value_eur`, `contract_end_date`, `source` y `confidence`.
- Corrige diagnostico para evitar doble merge por env var.
- Opportunity Finder muestra valores efectivos de mercado como principales cuando existen.
- CSVs reales revisados permanecen locales e ignorados por git.
- Mantener trazabilidad con `source`, `source_url`, `confidence` y `notes`.
- Ejecutar diagnostico obligatorio antes de activar el CSV en la app.
- Revisar validation errors, duplicate keys, matched_pct y effective coverage.
- Activar enrichment solo mediante `FOOTBALL_SCOUT_MARKET_CONTEXT_CSV`.
- Mantener scraping y proveedor automatico fuera de alcance.
- Mantener scoring general sin cambios.
- Release notes: [`docs/release_notes_v0_3_0.md`](docs/release_notes_v0_3_0.md).
- Plan detallado: [`docs/v0_3_0_plan.md`](docs/v0_3_0_plan.md).

## v0.4.0 Provider Evaluation / Licensed Data Integration

Implemented as provider evaluation workflow.

- Incluye plan de evaluacion de proveedores.
- Incluye decision records, matriz de evaluacion y reviews iniciales.
- Define politica de cache local y contrato provider -> Market Context.
- Incluye helper canonico, preview CLI, builder CLI y ejemplos sinteticos.
- Mantiene scraping fuera de alcance.
- Mantiene el flujo app -> datos locales validados, sin llamadas directas app -> proveedor.
- No integra un proveedor real todavia.
- Release notes: [`docs/release_notes_v0_4_0.md`](docs/release_notes_v0_4_0.md).
- Plan detallado: [`docs/v0_4_0_provider_evaluation_plan.md`](docs/v0_4_0_provider_evaluation_plan.md).

## v0.5.0 Provider Fixture Prototype

Implemented as an offline synthetic demo.

- Incluye contrato, validacion y aplicacion exacta de identity mapping revisado.
- Incluye samples sinteticos de mapping y provider fixture records.
- Incluye CLI offline para records mapeados y demo end-to-end hacia Market Context canonico.
- Excluye mappings `unmatched`, `ambiguous` y `rejected` sin fuzzy matching.
- Mantiene separadas identity mapping confidence y Market Context confidence.
- No integra un proveedor real, no hace scraping y no realiza llamadas de red.
- Plan detallado: [`docs/v0_5_0_provider_fixture_prototype_plan.md`](docs/v0_5_0_provider_fixture_prototype_plan.md).
- Identity mapping: [`docs/provider_identity_mapping_plan.md`](docs/provider_identity_mapping_plan.md).
- Release notes: [`docs/release_notes_v0_5_0.md`](docs/release_notes_v0_5_0.md).

## v0.6.0 Licensed Provider Payload Evaluation

Completed and published.

- Incluye checklist de licencia, procedencia, campos, cache y diagnostico.
- Incluye template de decision record y ejemplo de evaluacion sintetica.
- Incluye payload avanzado y mapping revisado completamente sinteticos.
- Incluye helper y CLI de flattening local, mas demo end-to-end hacia Market Context canonico.
- Mantener scraping, fetch automatico y llamadas live desde la app fuera de alcance.
- No se ha evaluado ningun payload real ni integrado ningun proveedor real.
- Plan: [`docs/v0_6_0_licensed_provider_payload_evaluation_plan.md`](docs/v0_6_0_licensed_provider_payload_evaluation_plan.md).
- Release notes: [`docs/release_notes_v0_6_0.md`](docs/release_notes_v0_6_0.md).
- Checklist: [`docs/provider_payload_evaluation_checklist.md`](docs/provider_payload_evaluation_checklist.md).

## v0.7.0 Permitted Provider Candidate Review

Completed and published.
- No integra un proveedor real; Sportmonks fue seleccionado solo para Candidate Intake y permanece sin aprobar.
- Mantiene payloads y outputs reales fuera de git.
- No activa datos de proveedor en la app.
- Plan: [`docs/v0_7_0_permitted_provider_candidate_review_plan.md`](docs/v0_7_0_permitted_provider_candidate_review_plan.md).
- Release readiness: [`docs/v0_7_0_release_readiness.md`](docs/v0_7_0_release_readiness.md).
- Release notes: [`docs/release_notes_v0_7_0.md`](docs/release_notes_v0_7_0.md).
- Release: https://github.com/albertopernas-dev/football-scout-dashboard/releases/tag/v0.7.0
- Workflow: [`docs/v0_7_0_candidate_review_workflow.md`](docs/v0_7_0_candidate_review_workflow.md).
- Pack template: [`docs/v0_7_0_candidate_review_pack_template.md`](docs/v0_7_0_candidate_review_pack_template.md).
- Shortlist matrix: [`docs/v0_7_0_provider_candidate_shortlist_matrix.md`](docs/v0_7_0_provider_candidate_shortlist_matrix.md).
- Initial shortlist: [`docs/provider_candidates/v0_7_0_initial_shortlist.md`](docs/provider_candidates/v0_7_0_initial_shortlist.md).
- Current candidate: [Sportmonks](docs/provider_candidates/sportmonks_candidate_review_pack.md) remains unapproved; minimal field review passed and no broad payload inspection occurred.
- Sportmonks Stage 1 gate: [`continue`](docs/provider_candidates/sportmonks_license_terms_gate.md) for the next governance step only; no provider approval or broad payload inspection.
- Public review notes: [`docs/provider_candidates/sportmonks_public_terms_review_notes.md`](docs/provider_candidates/sportmonks_public_terms_review_notes.md).
- Permission request sent: [docs/provider_candidates/sportmonks_permission_request_sent_log.md](docs/provider_candidates/sportmonks_permission_request_sent_log.md).
- Ticket acknowledgement: [docs/provider_candidates/sportmonks_ticket_acknowledgement_log.md](docs/provider_candidates/sportmonks_ticket_acknowledgement_log.md); exact ticket reference remains outside Git.
- Substantive response summary: [docs/provider_candidates/sportmonks_permission_response_summary.md](docs/provider_candidates/sportmonks_permission_response_summary.md); Stage 1 moved to `continue` under recorded conditions.
- La decision final puede ser accept, defer o reject.

## v0.8.0 Provider Permission Response Handling

- Completed with a docs-only closeout and limitations.
- Focus: handle provider permission responses safely.
- A non-sensitive Sportmonks substantive response summary exists.
- The Stage 1 gate is `continue` for the next governance step only.
- Sportmonks is not approved as a provider.
- No broad payload inspection or local trial has been performed; minimal ID discovery passed and credential setup remains outside Git.
- Sportmonks provider payload checklist created as draft/pre-trial.
- Sportmonks payload-specific decision record created as draft/pre-trial.
- Sportmonks ignored local trial scope plan remains draft/pre-trial.
- Football Free Plan confirmed by user screenshot; 4 leagues and 3000 API calls shown.
- Free Plan league list confirmed.
- Denmark Superliga league_id 271 selected for the first trial.
- Denmark Superliga 2026/2027 `season_id 27897` and FC København `team_id 85` confirmed.
- Manual UI lookup did not expose the IDs; 3 minimal API calls confirmed them and squad endpoint access returned HTTP 200.
- Sportmonks minimal ID discovery completed; non-sensitive summary recorded.
- Confirmed ID scope review passed.
- Minimal payload field review decision created under strict scope.
- Minimal payload field review executed from existing ignored cache with 0 API calls; review status `passed` and shape `partially suitable`.
- Transform design suitability decision created: docs-only planning approved; implementation remained blocked at that stage.
- Sportmonks transform design plan created docs-only; no code or implementation approval.
- Sportmonks implementation-plan readiness decision created; only docs-only plan creation was approved.
- Sportmonks implementation plan created docs-only.
- First local-only code implementation approval decision created under strict file scope.
- First local-only Sportmonks transform scaffold created with synthetic tests only; no network or real provider payloads.
- One approved local preview completed against exactly one ignored cache input.
- Preview result: `row_count 6`, `has_position_ids 0`, `has_jersey_numbers 0`.
- Preview result accepted with limitations; the local scaffold validation portion is complete.
- Governance chain completed for v0.8.0.
- Sportmonks secure credential setup verified as local-only.
- Local `.env` credential setup verified outside Git; the token remains untracked and undocumented.
- Trial scope remains one team, one season and a minimal payload, with Team Squad by Team and Season ID as the primary candidate endpoint.
- Published as tag and GitHub Release v0.8.0.

- Only 3 minimal ID discovery calls performed; still no broad payload inspection or local trial.
- Still no API calls during the preview, manual raw JSON review, additional cache reading, broad payload inspection, `.local.csv`, local trial, SQLite writes, Streamlit app integration or provider approval.
- Unresolved: labels, position coverage, jersey coverage and Market Context.
- Raw correspondence, ticket identifiers, payloads, credentials and provider cache remain outside Git.
- Plan: [`docs/v0_8_0_provider_permission_response_handling_plan.md`](docs/v0_8_0_provider_permission_response_handling_plan.md).
- Release notes: [docs/release_notes_v0_8_0.md](docs/release_notes_v0_8_0.md).

## v0.9.0 Provider Suitability Scope

- Status: completed docs-only; tag/release pending.
- Selected evaluation path `Compare providers`: completed.
- Final outcomes:
  - Sportmonks: `continue-targeted-clarification`.
  - API-Football / API-Sports: `technical-baseline-only`.
  - Capology: `separate-role-candidate`.
  - Transfermarkt manual reference: `manual-reference-only`.
- All providers remain unapproved.
- No implementation path, universal winner or multi-provider architecture is selected.
- Numeric scoring and ranking remain blocked.
- Recommended next:
  1. Complete a separate v0.9.0 release/tag block.
  2. Select any future milestone separately.
  3. Keep all restricted actions blocked.
- Still forbidden: login, private dashboards, account creation, API calls, provider cache reading, raw JSON review, automated scraping, implementation, `.local.csv`, SQLite writes, Streamlit integration, scoring, ranking and provider approval.
- Plan: [`docs/v0_9_0_provider_suitability_scope_plan.md`](docs/v0_9_0_provider_suitability_scope_plan.md).
- Scope decision: [`docs/provider_decisions/sportmonks_v0_9_0_scope_decision.md`](docs/provider_decisions/sportmonks_v0_9_0_scope_decision.md).
- Comparison plan: [docs/v0_9_0_provider_comparison_plan.md](docs/v0_9_0_provider_comparison_plan.md).
- Evidence completeness review: [docs/provider_comparison/v0_9_0_evidence_completeness_review.md](docs/provider_comparison/v0_9_0_evidence_completeness_review.md).
- Qualitative recommendation protocol: [docs/provider_comparison/v0_9_0_qualitative_recommendation_protocol.md](docs/provider_comparison/v0_9_0_qualitative_recommendation_protocol.md).
- Qualitative recommendation: [docs/provider_comparison/v0_9_0_qualitative_recommendation.md](docs/provider_comparison/v0_9_0_qualitative_recommendation.md).
- Closeout decision: [docs/provider_decisions/v0_9_0_provider_suitability_closeout_decision.md](docs/provider_decisions/v0_9_0_provider_suitability_closeout_decision.md).
- Release notes: [docs/release_notes_v0_9_0.md](docs/release_notes_v0_9_0.md).
- Comparison scope decision: [`docs/provider_decisions/v0_9_0_provider_comparison_scope_decision.md`](docs/provider_decisions/v0_9_0_provider_comparison_scope_decision.md).
- Public research protocol: [`docs/v0_9_0_provider_public_research_protocol.md`](docs/v0_9_0_provider_public_research_protocol.md).
- Protocol decision: [`docs/provider_decisions/v0_9_0_provider_public_research_protocol_decision.md`](docs/provider_decisions/v0_9_0_provider_public_research_protocol_decision.md).

## Potential v0.4.x Follow-ups

- v0.4.x: Better goalkeeper model.
- v0.4.x: UI polish and saved shortlists.
- v0.4.x: Richer reports and shortlist exports.

## Potential GitHub Issues

- [DATA] Add player age, market value and contract source.
- [DATA] Build first real enrichment CSV for LaLiga 2024 top opportunities.
- [DATA] Add enrichment source quality checklist.
- [FEATURE] Add app filter for effective market context source.
- [FEATURE] Add coverage threshold warning for Opportunity Finder.
- [RESEARCH] Evaluate market data providers.
- [DATA] Define provider decision record.
- [DATA] Maintain provider evaluation matrix.
- [DATA] Define provider cache policy.
- [DATA] Define provider-to-market-context transform contract.
- [DATA] Prototype provider-to-market-context canonical transform.
- [FEATURE] Add saved shortlists.
- [DATA] Add more leagues and seasons.
- [FEATURE] Improve goalkeeper-specific scoring.
- [FEATURE] Add shortlist-oriented visualizations.
- [FEATURE] Add batch scouting report export.
- [UX] Add screenshots and demo walkthrough.
- [DOCS] Keep user guide and scoring methodology updated as data sources evolve.
