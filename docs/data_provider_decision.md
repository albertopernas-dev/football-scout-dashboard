# Data Provider Decision

## Objetivo

Este documento define qué proveedor conviene usar para el primer conector real de `football-scout-dashboard` y qué limitaciones tendrá. La decisión se centra en alimentar el esquema canónico actual sin conectar todavía ninguna API real.

El producto busca scouting/análisis futbolístico para filtrar jugadores, comparar perfiles, encontrar similares, detectar oportunidades de mercado y generar informes HTML. Por tanto, la fuente elegida debe aportar datos de jugador suficientemente estables para una demo útil, aunque las métricas avanzadas lleguen por fases.

Nota v0.4.0: la decision de proveedor se reabre especificamente para contexto de mercado, edad real y contrato. El plan de evaluacion esta documentado en [`docs/v0_4_0_provider_evaluation_plan.md`](v0_4_0_provider_evaluation_plan.md), y los decision records viven en [`docs/provider_decisions/`](provider_decisions/). API-Football sigue siendo util para rendimiento deportivo desde `fixtures/players`, pero no debe asumirse como fuente suficiente para market context. La revision actual esta documentada en [`docs/provider_decisions/api_football_market_context_review.md`](provider_decisions/api_football_market_context_review.md).

Fuentes de referencia:

- [API-Football documentation](https://www.api-football.com/documentation-v3)
- [StatsBomb Open Data](https://github.com/statsbomb/open-data)
- [football-data.org API documentation](https://www.football-data.org/documentation/quickstart)

## Criterios de Evaluación

- Cobertura de jugadores.
- Cobertura de ligas.
- Disponibilidad de estadísticas por jugador.
- Disponibilidad de métricas avanzadas.
- Facilidad técnica de integración.
- Coste/plan gratuito.
- Estabilidad para demo.
- Encaje con el esquema canónico.
- Utilidad para scouting real.

## Matriz Comparativa

| Provider | Strengths | Weaknesses | Best use in this project | Fit score, 1-5 |
|---|---|---|---|---|
| API-Football / API-Sports | Buena opción para primer proveedor vivo por cobertura amplia, endpoints orientados a jugadores/equipos/competiciones y respuesta JSON compatible con ingesta. | Puede requerir plan de pago o límites de cuota; no se debe asumir que incluya todas las métricas avanzadas del esquema. | Primer conector real para jugadores y estadísticas básicas normalizadas a SQLite. | 4 |
| StatsBomb Open Data | Excelente para event data, investigación y construcción de métricas propias; incluye JSON estructurado de competiciones, partidos, eventos y lineups. | Cobertura limitada a competiciones abiertas; no es una fuente viva general para cualquier liga/jugador. | Fuente complementaria para análisis avanzado y métricas propias en una fase posterior. | 3 |
| football-data.org | API estable para competiciones, equipos, partidos, resultados y algunos recursos de personas/jugadores. | Limitada para scouting profundo de jugadores y métricas avanzadas; no encaja como fuente principal de perfiles estadísticos. | Fuente auxiliar para calendario, competiciones, equipos o contexto básico. | 2 |
| CSV/manual fallback | Control total, barato, reproducible y excelente para tests/demo local. | No es una fuente real de producto; mantenimiento manual y datos estáticos. | Fallback, demo, desarrollo y fixtures de testing. | 2 |

## Metric Availability Map

| Canonical field | Required for MVP? | API-Football expected support | StatsBomb Open Data expected support | football-data.org expected support | Notes |
|---|---:|---|---|---|---|
| player | Yes | Yes | Yes | Yes | Nombre de jugador disponible en todas, con posibles diferencias de naming. |
| age | Yes | Yes | Unknown / requires validation | Partial | Puede derivarse de fecha de nacimiento si existe. |
| position | Yes | Partial | Partial | Partial | Requiere normalización de posiciones entre proveedores. |
| team | Yes | Yes | Yes | Yes | El contexto equipo/temporada puede variar por endpoint. |
| league | Yes | Yes | Yes | Yes | En StatsBomb depende de competición abierta disponible. |
| season | Yes | Yes | Yes | Partial | Formatos distintos; normalizar a string/año. |
| minutes | Yes | Yes | Partial | Partial | StatsBomb puede requerir agregación de eventos/lineups. |
| goals | Yes | Yes | Partial | Partial | En event data puede agregarse; en APIs deportivas suele venir agregado. |
| assists | Yes | Yes | Partial | Partial | Requiere validar definición por proveedor. |
| shots | Yes | Yes | Yes | Unknown / requires validation | StatsBomb event data permite construirlo. |
| key_passes | Yes | Partial | Partial | Unknown / requires validation | Puede depender de definición del proveedor. |
| duels_won | Yes | Partial | Partial | Unknown / requires validation | Requiere validar disponibilidad y definición. |
| interceptions | Yes | Partial | Yes | Unknown / requires validation | StatsBomb event data suele permitir derivar eventos defensivos. |
| xg | Yes | Unknown / requires validation | Yes | No | No asumir disponibilidad en API-Football sin validar plan/endpoint. |
| xa | Yes | Unknown / requires validation | Partial | No | Puede requerir construcción propia o dato avanzado específico. |
| progressive_passes | Yes | Unknown / requires validation | Partial | No | Normalmente requiere event data y definición propia. |
| progressive_carries | Yes | Unknown / requires validation | Partial | No | Normalmente requiere event data y coordenadas. |
| completed_dribbles | Yes | Partial | Partial | Unknown / requires validation | Requiere validar definición y disponibilidad. |
| recoveries | Yes | Unknown / requires validation | Partial | Unknown / requires validation | Puede requerir event data. |
| market_value | No, but important for Opportunity Finder | Unknown / requires validation | No | No | Probablemente requiere proveedor especializado de mercado. |
| contract_end | No, but important for Opportunity Finder | Unknown / requires validation | No | Partial | football-data.org muestra contratos en algunos recursos de personas, pero no debe asumirse cobertura completa. |

## Decisión Recomendada

La fuente inicial para un proveedor vivo debería ser **API-Football / API-Sports**, empezando solo con métricas básicas disponibles y validadas. Es la mejor opción para llevar la app desde demo local hacia datos vivos sin rediseñar la arquitectura.

**StatsBomb Open Data** debe entrar como fuente complementaria posterior para análisis avanzado, event data y construcción de métricas propias. No conviene usarla como proveedor vivo general por su cobertura limitada.

El **CSV/manual fallback** debe mantenerse para demo, desarrollo, tests y recuperación cuando SQLite/proveedor externo no devuelvan datos.

**football-data.org** no debería ser la fuente principal de scouting. Puede ser útil para contexto de competiciones, equipos, fixtures o resultados, pero no cubre suficientemente el objetivo principal de ranking y comparación profunda de jugadores.

## Plan de Implementación por Fases

### Fase 1

- Crear cliente mínimo para API-Football.
- Cargar jugadores/estadísticas básicas.
- Normalizar al esquema interno.
- Guardar en SQLite.
- Mantener CSV fallback.

### Fase 2

- Mejorar mapping de posiciones.
- Añadir validaciones de columnas.
- Añadir logging de fuentes fallidas.

### Fase 3

- Explorar StatsBomb Open Data para métricas avanzadas/eventos.
- Construir métricas propias si encaja con el modelo de scoring.

### Fase 4

- Evaluar PostgreSQL/Supabase si la app deja de ser local.

## Riesgos

- Coste y límites de API.
- Datos incompletos o inconsistentes entre ligas.
- Cambios de contrato o estructura de API.
- Falta de métricas avanzadas en proveedores deportivos estándar.
- Diferencias en nombres de jugadores/equipos.
- `market_value` y `contract_end` probablemente no estarán completos en proveedores deportivos estándar.
- Necesidad futura de un proveedor especializado para mercado y contratos.
- Riesgo de sobreajustar scores a una fuente antes de validar definiciones de métricas.

## Conclusión

La ruta más pragmática es empezar con API-Football como proveedor vivo básico, mantener SQLite como almacenamiento local y conservar CSV como fallback. StatsBomb Open Data debe reservarse para enriquecer métricas avanzadas cuando la app ya tenga un flujo de ingesta vivo estable.
