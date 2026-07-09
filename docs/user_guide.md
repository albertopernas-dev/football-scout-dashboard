# User Guide

Esta guia explica como usar Football Scout Dashboard desde la perspectiva de scouting y analisis, sin entrar en detalles de implementacion.

## What This Dashboard Does

Football Scout Dashboard ayuda a revisar jugadores con datos deportivos, priorizar candidatos y preparar shortlists.

La app permite:

- Revisar rankings de jugadores con scores deportivos.
- Comparar perfiles entre jugadores.
- Buscar oportunidades con Opportunity Finder.
- Encontrar jugadores similares.
- Generar informes HTML de scouting.
- Descargar CSV con los resultados visibles de la tabla principal y Opportunity Finder.

El objetivo no es reemplazar el criterio humano, sino reducir una tabla amplia de jugadores a grupos mas manejables para revision.

## Dataset Summary

La parte superior de la app muestra un resumen ejecutivo del dataset activo.

Los campos principales son:

- Fuente activa: indica si los datos vienen de SQLite, CSV fallback, proveedor externo o upload manual.
- Jugadores: numero de filas cargadas tras preparar los datos.
- Equipos: numero de equipos distintos.
- Minutos: suma total de minutos disponibles.
- Muestra fiable: jugadores con una muestra de minutos suficientemente amplia.
- Porteros: numero de jugadores marcados como porteros.
- Contexto mercado: `Disponible` o `Limitado`.

Con el dataset local actual de LaLiga 2024, el contexto de mercado aparece como limitado porque no hay edad real, valor de mercado ni contrato.

Si se configura `FOOTBALL_SCOUT_MARKET_CONTEXT_CSV`, la app muestra en `Fuente de datos` la cobertura del enrichment: filas emparejadas, edad, valor de mercado, contrato, errores de validacion y claves duplicadas. Si no se configura, el dashboard mantiene el contexto de mercado limitado actual.

## Player Table

La tabla principal muestra el ranking recomendado de jugadores.

Columnas clave:

- Score bruto: score deportivo directo, sin ajuste por fiabilidad de minutos.
- Score recomendado: score bruto ajustado por fiabilidad de minutos. Es el ranking recomendado por defecto.
- Muestra: etiqueta de fiabilidad de minutos.
- Fiabilidad minutos: puntuacion 0-100 basada en minutos jugados.
- Ambito scoring: indica si el jugador usa scoring general o tratamiento de portero.
- Comparable ranking general: indica si el jugador es comparable con el ranking general de jugadores de campo.

Si `FOOTBALL_SCOUT_MARKET_CONTEXT_CSV` esta activo, la tabla puede mostrar columnas de contexto de mercado: match, edad, valor, contrato, fuente, confianza y claves duplicadas. Estos campos son informativos en esta fase y no cambian todavia el ranking recomendado.

Filtros especificos de la tabla:

- Ambito ranking:
  - Todos.
  - Solo comparables ranking general.
  - Solo porteros.
- Fiabilidad muestra:
  - Todas.
  - Media o fiable.
  - Solo fiable.

Estos filtros solo cambian la tabla visible. No eliminan datos del resto de la app.

La tabla incluye el boton `Descargar tabla visible CSV`. El CSV descargado contiene exactamente lo visible: filtros aplicados, orden actual y nombres de columnas visuales.

## Opportunity Finder

Opportunity Finder ayuda a crear una shortlist de candidatos a revisar.

En el dataset actual, la oportunidad debe interpretarse principalmente como rendimiento deportivo mas fiabilidad de muestra. No debe entenderse como oportunidad de mercado completa porque faltan edad real, valor de mercado y contrato.

Controles principales:

- Posiciones.
- Edad maxima.
- Minutos minimos.
- Valor de mercado maximo.
- Filtro por contrato proximo.
- Numero de resultados.

Controles de ranking:

- Ambito ranking:
  - Todos.
  - Solo comparables ranking general.
  - Solo porteros.
- Fiabilidad muestra:
  - Todas.
  - Media o fiable.
  - Solo fiable.

Estos filtros se aplican antes de calcular los resultados visibles, por lo que el `top_n` sale del universo filtrado.

Si `FOOTBALL_SCOUT_MARKET_CONTEXT_CSV` esta activo, Opportunity Finder usa los campos efectivos de edad, valor y contrato para sus filtros de mercado. La tabla de oportunidades puede mostrar match, edad, valor, contrato, fuente, confianza y claves duplicadas. El scoring general de rendimiento no cambia.

Opportunity Finder mantiene avisos cuando:

- falta contexto de mercado;
- aparecen jugadores con muestra baja;
- aparecen porteros no comparables con el ranking general.

Incluye el boton `Descargar oportunidades CSV`. El archivo contiene las oportunidades visibles, ya filtradas y con nombres de columnas legibles.

## Similar Players And Reports

La pestaña de similitud permite elegir un jugador y ver perfiles similares segun las columnas disponibles para el modelo.

Desde esa misma vista se puede generar y descargar un informe HTML de scouting.

Uso recomendado:

- Selecciona un jugador con muestra suficiente.
- Revisa los similares.
- Usa el informe como punto de partida, no como decision final.

## Goalkeepers

Los porteros no son plenamente comparables con jugadores de campo.

La app lo refleja con:

- Ambito scoring.
- Comparable ranking general.
- Score portero.

El `goalkeeper_score` se calcula solo con metricas de portero que tengan senal real entre porteros. En el dataset actual, la senal especifica de portero es limitada y depende principalmente de `rating_avg`.

Recomendacion:

- Usa el filtro `Solo porteros` para revisar porteros por separado.
- No mezcles conclusiones de porteros y jugadores de campo sin validacion adicional.

## Recommended Workflow

1. Revisa el resumen del dataset.
2. Comprueba si el contexto de mercado es disponible o limitado.
3. En la tabla principal, filtra por `Solo comparables ranking general`.
4. Usa `Media o fiable` o `Solo fiable` para priorizar muestras robustas.
5. Ordena y revisa el `Score recomendado`.
6. Mira el `Score bruto` para detectar senales exploratorias en jugadores con menos minutos.
7. Usa Opportunity Finder para crear una shortlist.
8. Descarga CSV de la shortlist visible.
9. Compara candidatos y busca similares.
10. Valida con video, contexto tactico y scouting humano.

## Current Limitations

Limitaciones del dataset actual:

- No hay edad real.
- No hay valor de mercado.
- No hay fin de contrato.
- Algunas metricas avanzadas no tienen senal real, como xG, xA, progresiones y recuperaciones.
- Las metricas de portero son limitadas.

Limitaciones del producto:

- El scoring ayuda a priorizar revision, pero no sustituye scouting humano.
- La app no valida contexto tactico, rol, lesiones, contrato real ni disponibilidad.
- Las conclusiones dependen de la calidad y cobertura de la fuente de datos activa.
