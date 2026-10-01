---
name: andinalog-nb04-eda
description: Crea, revisa o corrige el Notebook 04 de EDA sobre la tabla Gold IoT de AndinaLog 03B. Úsala para los controles estructurales, los cinco gráficos Seaborn exigidos, la segmentación comprensible por producto y las interpretaciones destinadas a público no técnico.
---

# Notebook 04: EDA de Gold IoT

## Objetivo

Explicar cómo se comportan las variables y el riesgo futuro mediante controles y gráficos que respondan directamente las preguntas de la tarea.

## Contenido obligatorio

1. Cargar Gold y mostrar filas, columnas y unidad de observación.
2. Revisar duplicados, faltantes, tipos, estadísticas descriptivas y que los cruces no multiplicaron registros.
3. Mantener las cinco predictoras mínimas: temperatura actual, humedad actual, `desviacion_termica_flag`, `temperatura_anterior` y `variacion_temperatura_30min`.
4. Crear los cinco gráficos Seaborn requeridos:
   - `countplot` del objetivo futuro;
   - `histplot` de temperatura actual con color por objetivo;
   - `boxplot` de humedad actual por clase;
   - `barplot` de desviación actual frente al promedio del objetivo;
   - `scatterplot` de temperatura frente a variación a 30 minutos con color por objetivo.
5. Antes de cada gráfico, mostrar literalmente la pregunta que responde.
6. Después de cada gráfico, calcular cifras de apoyo y escribir una interpretación explícita, sencilla y coherente con el resultado real.
7. Analizar temperatura y riesgo por producto cuando la columna exista, sin inventar rangos oficiales por producto.
8. Añadir el gráfico temporal opcional solo si existen las columnas necesarias y limitarlo a dos o tres viajes.
9. Generar el informe Markdown con las mismas conclusiones esenciales del notebook.

## Restricciones

- No añadir correlaciones, pruebas avanzadas ni controles redundantes si la tarea no los pide.
- No anticipar conclusiones; toda afirmación debe salir de valores calculados.
- No confundir asociación visual con causalidad.
- No entrenar modelos en este notebook.

## Memoria

Actualizar las memorias del Notebook 04, Gold y la sesión activa.
