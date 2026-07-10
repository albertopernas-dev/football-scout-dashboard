# Roadmap

## Current Status

- SQLite local funciona como fuente principal.
- LaLiga 2024 esta cargada desde payloads locales de API-Football `fixtures/players`.
- La app incluye ranking recomendado, filtros de comparabilidad y muestra, Opportunity Finder, descargas CSV, informes HTML y documentacion de scoring.
- v0.2.0 incluye una capa opt-in de Market Context para CSV manual, validacion, diagnostico, cobertura efectiva y uso de `effective_*` en Opportunity Finder.
- v0.3.0 completa el workflow local de enrichment real revisado: seed export, checklist de fuentes, safeguards, validacion estricta y display efectivo en Opportunity Finder.
- El contexto de mercado real depende de CSVs revisados localmente; no hay scraping ni proveedor automatico conectado.

## Recommended Next Steps

1. Evaluar proveedores oficiales/licenciados para contexto de mercado.
2. Ampliar datos reales revisados para edad, valor de mercado y contrato.
3. Ajustar pesos de Opportunity Finder solo cuando exista cobertura real suficiente.
4. Mejorar metricas especificas de porteros, como paradas, goles encajados y porterias a cero si la fuente lo permite.
5. Ampliar a mas ligas y temporadas manteniendo el pipeline local reproducible.
6. Mejorar visualizaciones de comparacion y shortlists.
7. Explorar exportacion batch de reportes para shortlists.

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

## Potential v0.4.x Milestones

- v0.4.0: Provider Evaluation / Licensed Data Integration.
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
- [FEATURE] Add saved shortlists.
- [DATA] Add more leagues and seasons.
- [FEATURE] Improve goalkeeper-specific scoring.
- [FEATURE] Add shortlist-oriented visualizations.
- [FEATURE] Add batch scouting report export.
- [UX] Add screenshots and demo walkthrough.
- [DOCS] Keep user guide and scoring methodology updated as data sources evolve.
