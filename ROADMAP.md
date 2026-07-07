# Roadmap

## Current Status

- SQLite local funciona como fuente principal.
- LaLiga 2024 esta cargada desde payloads locales de API-Football `fixtures/players`.
- La app incluye ranking recomendado, filtros de comparabilidad y muestra, Opportunity Finder, descargas CSV, informes HTML y documentacion de scoring.
- El contexto de mercado sigue limitado: faltan edad real, valor de mercado y contrato.

## Recommended Next Steps

1. Incorporar una fuente fiable para edad, valor de mercado y contrato.
2. Mejorar metricas especificas de porteros, como paradas, goles encajados y porterias a cero si la fuente lo permite.
3. Ampliar a mas ligas y temporadas manteniendo el pipeline local reproducible.
4. Mejorar visualizaciones de comparacion y shortlists.
5. Explorar exportacion batch de reportes para shortlists.
6. Preparar screenshots o un video corto de demo.

## v0.2.0 Market Context Layer

- Enriquecer el dataset con edad real, valor de mercado y fecha de fin de contrato.
- Empezar con un CSV manual de enrichment, validado y testeado.
- Mantener fuente, confianza y cobertura visibles.
- Usar el contexto real en Opportunity Finder cuando exista.
- Conservar warnings claros cuando la cobertura sea parcial o nula.
- Plan detallado: [`docs/market_context_plan.md`](docs/market_context_plan.md).

## Potential GitHub Issues

- [DATA] Add player age, market value and contract source.
- [DATA] Add more leagues and seasons.
- [FEATURE] Improve goalkeeper-specific scoring.
- [FEATURE] Add shortlist-oriented visualizations.
- [FEATURE] Add batch scouting report export.
- [UX] Add screenshots and demo walkthrough.
- [DOCS] Keep user guide and scoring methodology updated as data sources evolve.
