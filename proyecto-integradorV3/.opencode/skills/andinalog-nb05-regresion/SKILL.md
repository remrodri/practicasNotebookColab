---
name: andinalog-nb05-regresion
description: Crea, revisa o corrige el Notebook 05 de regresión logística de AndinaLog 03B. Úsala para predecir desviación térmica en los próximos 60 minutos con las cinco variables mínimas, partición por viaje, métricas claras y análisis por desviación actual y producto.
---

# Notebook 05: regresión logística

## Objetivo

Entrenar y evaluar un modelo interpretable que estime si habrá desviación térmica durante los próximos 60 minutos.

## Procedimiento

1. Cargar Gold y seleccionar solo filas con objetivo evaluable y predictores disponibles según la decisión documentada.
2. Usar las cinco predictoras mínimas: temperatura actual, humedad actual, `desviacion_termica_flag`, `temperatura_anterior` y `variacion_temperatura_30min`.
3. Separar entrenamiento y prueba por `viaje_id` para impedir que un mismo viaje aparezca en ambos grupos.
4. Ajustar imputación, escalado y codificación únicamente con entrenamiento mediante un pipeline.
5. Comparar con una línea base sencilla y entrenar regresión logística.
6. Reportar matriz de confusión y métricas comprensibles, incluyendo desempeño de la clase de riesgo.
7. Explicar falsos positivos y falsos negativos en términos operativos.
8. Evaluar el desempeño por `desviacion_termica_flag` actual para comprobar si el modelo funciona peor cuando todavía no existe una desviación.
9. Evaluar por producto cuando haya suficientes casos y advertir cuando una muestra sea pequeña.
10. Explicar coeficientes o probabilidades con prudencia, sin afirmar causalidad.
11. Generar un informe Markdown que conserve las interpretaciones esenciales incluidas en el notebook.

## Restricciones

- No usar variables futuras como predictores.
- No ajustar decisiones mirando el conjunto de prueba.
- No dividir aleatoriamente filas ignorando los viajes.
- No presentar exactitud global como única medida.
- No ocultar subgrupos con bajo desempeño o sin observaciones suficientes.

## Criterio de cierre

El notebook debe ser reproducible, ejecutarse sin errores y explicar claramente cuándo el modelo funciona, cuándo falla y por qué eso importa.

## Memoria

Actualizar las memorias del Notebook 05, Gold, decisiones y la sesión activa.
