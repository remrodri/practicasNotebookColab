# Proyecto Integrador V2 AndinaLog 03B

## Alcance

Este proyecto corresponde al Grupo 06, empresa AndinaLog y subcaso 03B. V2 sigue los prompts S11 del docente para construir pipelines Bronze a Silver y productos Silver a Gold. No reutilizar automaticamente codigo, estructuras, salidas, conteos o conclusiones de V1. V3 realizara la comparacion y combinacion posterior.

## Skills del proyecto

- Usa `$andinalog-03b-bronze-silver` para procesar una fuente Bronze CSV, JSON o TXT.
- Usa `$andinalog-03b-silver-gold` para integrar fuentes Silver y producir detalle y agregado Gold.
- Usa `$andinalog-03b-v2-pipeline` para revisar orden, alcance y coherencia general.

## Entregables

Por cada fuente Bronze entrega un notebook ejecutado, un informe MD, un CSV Silver y un CSV de cuarentena. Por cada producto Gold entrega un notebook ejecutado, un informe MD, un detalle Gold y un agregado Gold.

## Bronze a Silver

- Centraliza reglas en `config`.
- Implementa funciones y encadenalas con `df.pipe()`.
- Conserva valores originales y audita transformaciones e imputaciones.
- No uses `dropna()` para descartar silenciosamente errores.
- Calcula `calidad_estado` despues del tratamiento y la imputacion.
- Envia errores residuales a cuarentena.
- Interpreta fechas sin zona en `America/La_Paz` y conviertelas a UTC para Silver.
- Concilia Bronze, Silver y cuarentena.

## Imputacion

Imputa solo con una regla reproducible, inequivoca, compatible con el dominio y declarada en `config`. Conserva valor original, valor tratado, bandera, metodo y motivo. No uses estadisticas globales o informacion futura sin justificacion y control contra fuga.

## Silver a Gold

- Usa fuentes Silver conciliadas.
- Declara granularidad, claves y cardinalidad.
- Valida joins y conserva no correspondencias.
- Configura agregaciones mediante `metricas_agg`.
- Genera detalle Gold y agregado Gold.

## Dominio

Celsius es la unidad canonica; Fahrenheit es convertible; Kelvin no es esperado operacionalmente. Los centinelas como `-999` no son mediciones. Una fecha sin zona explicita se interpreta como hora de Bolivia antes de convertirse a UTC.

## Calidad de entrega

Los informes deben usar los resultados del notebook entregado. Todos los notebooks deben conservar ejecuciones visibles, controles finales y una seccion de reproducibilidad.
