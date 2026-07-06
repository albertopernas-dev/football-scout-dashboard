# Scoring Methodology

Este documento explica como interpretar los scores y rankings de Football Scout Dashboard con el dataset local actual.

## Fuente de datos actual

El flujo local actual usa payloads de API-Football `fixtures/players`, agregados y normalizados a una base SQLite local.

Estado de referencia:

- Proveedor original: API-Football / API-Sports.
- Endpoint base utilizado para rendimiento: `fixtures/players`.
- Almacenamiento principal: SQLite local en `data/football_scout.db`.
- Competicion/dataset actual: LaLiga 2024.
- Jugadores cargados: 588.
- Campos sin cobertura real en el dataset actual: edad, valor de mercado y fin de contrato.

Esto significa que la app ya puede ordenar jugadores por rendimiento deportivo observado, pero no debe interpretarse como una fuente completa de oportunidad de mercado.

## Scores principales

La app muestra scores internos con nombres visuales para que el ranking sea mas claro.

| Nombre visual | Columna interna | Interpretacion |
| --- | --- | --- |
| Score bruto | `overall_score` | Score deportivo calculado desde perfiles de rendimiento y percentiles por posicion. |
| Score recomendado | `sample_adjusted_overall_score` | Score bruto ajustado por fiabilidad de minutos. Es el criterio recomendado para ordenar jugadores. |
| Oportunidad bruta | `market_opportunity_score` | Score de oportunidad calculado con rendimiento y contexto de mercado cuando esta disponible. |
| Oportunidad recomendada | `sample_adjusted_market_opportunity_score` | Oportunidad bruta ajustada por fiabilidad de minutos. Es el criterio recomendado en Opportunity Finder. |

Los scores brutos se mantienen visibles porque ayudan a detectar senales exploratorias. Los scores recomendados son mas prudentes cuando un jugador tiene pocos minutos.

## Fiabilidad por minutos

La app no oculta automaticamente jugadores con pocos minutos, pero marca la fiabilidad de la muestra y ajusta los scores recomendados.

Etiquetas de muestra:

- Menos de 300 minutos: `Muestra baja`.
- De 300 a 899 minutos: `Muestra media`.
- 900 minutos o mas: `Muestra fiable`.

La fiabilidad numerica de minutos escala de 0 a 100:

- 0 minutos equivale a 0.
- 900 minutos o mas equivale a 100.
- Entre 0 y 900 se aplica una escala lineal.

Formula de ajuste:

```text
adjusted = 50 + (score - 50) * (minutes_reliability_score / 100)
```

Consecuencia practica:

- Si la fiabilidad es 100, el score recomendado coincide con el score bruto.
- Si la fiabilidad es 0, el score recomendado vuelve a un punto neutral de 50.
- Si la fiabilidad es intermedia, el score se acerca parcialmente a 50.

Este ajuste evita que muestras muy pequenas dominen rankings recomendados sin eliminar esos jugadores de la exploracion.

## Metricas con senal real

El scoring no usa una metrica solo porque exista como columna. Antes de entrar en el calculo, cada metrica debe tener senal real:

- La columna debe existir.
- Debe contener valores numericos validos.
- No puede estar completamente a cero.
- Debe tener variacion real, con al menos dos valores distintos despues de limpiar nulos.

Si una metrica como `xg_per90` o `progressive_passes_per90` aparece a cero en todo el dataset actual, se ignora para no diluir ni penalizar perfiles artificialmente.

Si en el futuro se carga un dataset donde esa metrica tenga valores reales y variacion, volvera a entrar automaticamente en el scoring.

Metricas con senal real en el dataset actual:

- `assists_per90`
- `duels_won_per90`
- `goals_per90`
- `interceptions_per90`
- `key_passes_per90`
- `shots_per90`

Metricas presentes pero sin senal real en el dataset actual:

- `completed_dribbles_per90`
- `progressive_carries_per90`
- `progressive_passes_per90`
- `recoveries_per90`
- `xa_per90`
- `xg_per90`

## Contexto de mercado limitado

En el dataset actual, la cobertura de estos campos es 0%:

- `age`
- `market_value`
- `contract_end`

Por ese motivo, Opportunity Finder debe interpretarse actualmente como un ranking de rendimiento deportivo + fiabilidad de muestra, no como una oportunidad de mercado completa.

La app muestra un aviso cuando falta contexto de mercado para recordar que:

- Edad desconocida no significa jugador joven.
- Valor de mercado desconocido no significa jugador barato.
- Contrato desconocido no significa contrato proximo.

Cuando se incorpore una fuente fiable para edad, valor y contrato, `market_opportunity_score` y `sample_adjusted_market_opportunity_score` tendran mas valor como ranking de oportunidad real.

## Porteros

Los porteros no son plenamente comparables con el ranking general de jugadores de campo.

La app marca este contexto con:

- `scoring_scope`
- `is_general_ranking_comparable`
- `goalkeeper_score`

Reglas actuales:

- Los porteros se identifican por posiciones como `Goalkeeper`, `GK` o `G`.
- Los porteros quedan marcados como no comparables con el ranking general.
- Si no hay metricas especificas de portero con senal suficiente, `scoring_scope` pasa a `Goalkeeper limited` y `goalkeeper_score` queda en 50.
- Si hay metricas GK informativas, `goalkeeper_score` se calcula solo entre porteros, no contra jugadores de campo.

En el dataset actual, la unica senal GK disponible es principalmente `rating_avg`. Por tanto, `goalkeeper_score` es util como orientacion limitada, pero todavia no sustituye un modelo especifico de porteros con paradas, goles encajados, centros, salidas, acciones bajo presion u otras metricas propias de la posicion.

## Como interpretar los rankings

Uso recomendado:

1. Mira primero el `Score recomendado`.
2. Revisa la etiqueta de muestra (`Muestra baja`, `Muestra media`, `Muestra fiable`).
3. Usa el score bruto para detectar senales exploratorias.
4. En Opportunity Finder, interpreta la oportunidad como limitada si faltan edad, valor y contrato.
5. Trata porteros aparte cuando `scoring_scope` indique contexto de portero.

Un jugador con score bruto alto y muestra baja puede ser interesante, pero no deberia ocupar el mismo nivel de confianza que un jugador con score similar y mas de 900 minutos.

## Limitaciones actuales

- No hay edad real, valor de mercado ni fin de contrato en el dataset actual.
- Algunas metricas avanzadas como xG, xA, progresiones, conducciones y recuperaciones no tienen senal real en la fuente actual.
- El modelo de porteros es conservador y limitado por falta de metricas GK fuertes.
- La definicion de cada metrica depende de la fuente original y debe validarse antes de comparar con otros proveedores.
- El scoring ayuda a priorizar revision, pero no sustituye scouting humano, video, contexto tactico, rol del jugador ni validacion medica/contractual.

