---
name: andinalog-03b-silver-gold
description: Genera o revisa un notebook ejecutado y un informe MD que integran fuentes Silver de AndinaLog 03B mediante joins validados y producen un detalle Gold y un agregado Gold parametrizable. Usar cuando el usuario indique la evidencia o producto Gold y sus fuentes Silver.
---

# AndinaLog 03B Silver a Gold

Construye un producto Gold por invocacion. Usa solamente fuentes Silver conciliadas y sigue el segundo prompt S11 del docente.

## Entradas

Necesitas el objetivo Gold y las fuentes Silver. Determina y documenta tabla maestra, tabla transaccional, claves y granularidades a partir de los archivos reales y del dominio.

Antes de usarlas, comprueba que las fuentes necesarias tengan notebook ejecutado, Silver, cuarentena, informe, conciliacion valida y auditoria aprobada. Clasifica cada fuente como utilizada, contextual o excluida y explica el motivo.

## Entregables obligatorios

1. Notebook `.ipynb` listo para Colab y ejecutado.
2. Informe `.md` basado en la ejecucion actual.
3. `<nombre>_detalle_gold.csv`.
4. `<nombre>_agregado_gold.csv`.

## Flujo

1. Declara objetivo, unidad analitica y contrato del join.
2. Lee y valida las fuentes Silver.
3. Comprueba unicidad de la clave maestra.
4. Declara `metricas_agg` al inicio.
5. Ejecuta `left` join con `validate="1:m"` cuando esa sea la cardinalidad real.
6. Si la relacion no es 1:m, agrega primero a la granularidad correcta; no fuerces la validacion.
7. Conserva entidades maestras y registra correspondencias y ausencias.
8. Agrega antes de unir cuando una clave no sea unica y exista riesgo muchos a muchos.
9. Calcula `groupby().agg(metricas_agg)` y aplana el MultiIndex.
10. Trata matematicamente los nulos de agregacion y explica cada decision.
11. Valida conteos, cobertura, unicidad y coherencia entre detalle y agregado.
12. Exporta ambos CSV, conserva resultados visibles y redacta el informe.

## Reglas estrictas

- Usa pandas para joins y agregaciones.
- Excluye de promedios claves, fechas, textos y banderas sin significado numerico.
- No ocultes claves sin correspondencia.
- Evita muchos a muchos no controlados.
- No uses informacion futura en un Gold destinado a prediccion.
- Declara el instante de corte de cada variable predictiva y excluye eventos o bitacoras posteriores.
- Excluye identificadores personales y variables laborales sin necesidad analitica demostrada.
- No copies conteos o resultados de V1.
- Distingue hechos, inferencias y recomendaciones; no afirmes causalidad.

## Productos previstos

- Evidencia 1: excursiones termicas por producto, viaje, camion y categoria.
- Evidencia 2: riesgo de vencimiento y merma.
- Evidencia 3: tabla analitica para alerta termica a 60 minutos.

Adapta fuentes y metricas a cada evidencia despues de inspeccionar sus Silver.
