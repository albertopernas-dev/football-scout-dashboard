# Roadmap

## Current Status

- SQLite local funciona como fuente principal.
- LaLiga 2024 esta cargada desde payloads locales de API-Football `fixtures/players`.
- La app incluye ranking recomendado, filtros de comparabilidad y muestra, Opportunity Finder, descargas CSV, informes HTML y documentacion de scoring.
- v0.2.0 incluye una capa opt-in de Market Context para CSV manual, validacion, diagnostico, cobertura efectiva y uso de `effective_*` en Opportunity Finder.
- El contexto de mercado real sigue limitado hasta conectar o completar datos reales de edad, valor de mercado y contrato.

## Recommended Next Steps

1. Incorporar datos reales revisados o una fuente fiable para edad, valor de mercado y contrato.
2. Ajustar pesos de Opportunity Finder cuando exista cobertura real suficiente.
3. Mejorar metricas especificas de porteros, como paradas, goles encajados y porterias a cero si la fuente lo permite.
4. Ampliar a mas ligas y temporadas manteniendo el pipeline local reproducible.
5. Mejorar visualizaciones de comparacion y shortlists.
6. Explorar exportacion batch de reportes para shortlists.

## v0.2.0 Market Context Layer

- Implementado para workflow manual/CSV opt-in.
- Incluye schema, validacion, merge helpers, diagnostico CLI, template/sample CSV y cobertura visible.
- La app muestra columnas `market_context_*` y cobertura efectiva.
- Opportunity Finder usa `effective_age`, `effective_market_value_eur` y `effective_contract_end_date` cuando existen valores validos.
- El scoring general permanece sin cambios.
- Pendiente: incorporar datos reales de enrichment y revisar pesos de oportunidad cuando haya cobertura suficiente.
- Plan detallado: [`docs/market_context_plan.md`](docs/market_context_plan.md).

## Potential GitHub Issues

- [DATA] Add player age, market value and contract source.
- [DATA] Add more leagues and seasons.
- [FEATURE] Improve goalkeeper-specific scoring.
- [FEATURE] Add shortlist-oriented visualizations.
- [FEATURE] Add batch scouting report export.
- [UX] Add screenshots and demo walkthrough.
- [DOCS] Keep user guide and scoring methodology updated as data sources evolve.
