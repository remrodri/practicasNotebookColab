---
name: andinalog-nb03-silver-gold
description: Crea, revisa o corrige el Notebook 03 que transforma IoT Silver en la tabla Gold predictiva de AndinaLog 03B. Úsala para ordenar lecturas por viaje, crear predictores temporales y la etiqueta de desviación en los próximos 60 minutos sin multiplicar filas.
---

# Notebook 03: Silver a Gold

## Objetivo

Construir una tabla Gold con una fila por lectura, variables temporales reproducibles y el objetivo futuro del caso 03B.

## Procedimiento

1. Cargar Silver y comprobar su granularidad y claves.
2. Ordenar por `viaje_id` y fecha-hora antes de cualquier cálculo temporal.
3. Conservar las variables base requeridas y crear `temperatura_anterior` dentro de cada viaje.
4. Calcular `variacion_temperatura_30min` con la lógica temporal documentada en el notebook.
5. Crear `desviacion_proximos_60min_flag` usando únicamente lecturas posteriores del mismo viaje.
6. Mantener como nulo el objetivo cuando no exista horizonte futuro suficiente; no convertir automáticamente esos casos en cero.
7. Si hay cruces con otras tablas, declarar clave, cardinalidad esperada y conteos antes y después.
8. Verificar que no se multipliquen lecturas y que las variables no mezclen viajes.
9. Guardar Gold y generar un informe Markdown con cifras calculadas.
10. Explicar cada transformación importante en celdas de texto accesibles.

## Restricciones

- No usar información posterior como predictor.
- No calcular desplazamientos globales fuera de `viaje_id`.
- No imputar variables temporales si hacerlo inventa una observación inexistente.
- No entrenar el modelo en este notebook.

## Criterio de cierre

La granularidad se conserva, el objetivo está alineado con el horizonte de 60 minutos y el notebook se ejecuta completo sin errores.

## Memoria

Actualizar las memorias del Notebook 03, Silver, Gold y la sesión activa.
