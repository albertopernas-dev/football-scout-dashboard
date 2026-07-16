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
- v0.7.0 es el milestone actual para revisar un candidato permitido sin prometer integracion.
- El contexto de mercado real depende de CSVs revisados localmente; no hay scraping ni proveedor automatico conectado.

## Recommended Next Steps

1. Elegir un proveedor o fuente candidata especifica.
2. Revisar licencia y terminos antes de inspeccionar payloads.
3. Completar checklist y decision record.
4. Si esta permitido, ejecutar un trial local e ignorado del payload.

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

- Current milestone.
- No promete una integracion real ni selecciona candidato en este bloque inicial.
- Mantiene payloads y outputs reales fuera de git.
- No activa datos de proveedor en la app.
- Plan: [`docs/v0_7_0_permitted_provider_candidate_review_plan.md`](docs/v0_7_0_permitted_provider_candidate_review_plan.md).
- Workflow: [`docs/v0_7_0_candidate_review_workflow.md`](docs/v0_7_0_candidate_review_workflow.md).
- Pack template: [`docs/v0_7_0_candidate_review_pack_template.md`](docs/v0_7_0_candidate_review_pack_template.md).
- Shortlist matrix: [`docs/v0_7_0_provider_candidate_shortlist_matrix.md`](docs/v0_7_0_provider_candidate_shortlist_matrix.md).
- Initial shortlist: [`docs/provider_candidates/v0_7_0_initial_shortlist.md`](docs/provider_candidates/v0_7_0_initial_shortlist.md).
- La decision final puede ser accept, defer o reject.

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
