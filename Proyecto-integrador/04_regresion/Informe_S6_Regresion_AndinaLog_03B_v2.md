# Informe S6 — Regresión térmica AndinaLog 03B

## Pregunta predictiva

Con la información disponible en una lectura, ¿cuál será el máximo desvío térmico respecto al umbral durante los próximos 60 minutos?

- **Unidad:** una lectura IoT.
- **Objetivo:** `max_desvio_termico_proximos_60min_c`.
- **Horizonte:** 60 minutos posteriores a la lectura.
- **Uso esperado:** priorizar la revisión o intercepción de un transporte.

## Datos utilizados

La tabla integrada contiene 28.677 lecturas. Se utilizaron las 27.477 marcadas como aptas para regresión y con objetivo continuo calculable.

Se compararon dos familias:

1. **Base:** medición actual, rezagos, tendencia térmica, condiciones requeridas, producto, camión, centro y pedido disponibles en el instante de predicción.
2. **Con eventos:** las variables base más conteos históricos, alertas, fallas, severidad, reconocimiento, recencia, mantenimiento y configuración de eventos de flota.

No se incluyeron el objetivo binario, el número de lecturas futuras, banderas de aptitud ni información posterior.

## Partición temporal

| Partición | Viajes | Lecturas utilizadas |
|---|---:|---:|
| Ajuste | 796 | 18.221 |
| Validación | 180 | 4.129 |
| Test | 180 | 4.119 |
| Excluidos por corte o margen | 44 | No participan |

Cada viaje pertenece a una sola partición. Entre los bloques existe un margen de 60 minutos para proteger el horizonte futuro. El archivo `asignacion_split_viajes.csv` será reutilizado en S7–S10.

## Selección en validación

| Modelo | Variables | MAE (°C) | RMSE (°C) | R² |
|---|---|---:|---:|---:|
| Random Forest | Base | **0,703** | **0,999** | **0,567** |
| Ridge | Base | 0,769 | 1,075 | 0,499 |
| Lineal | Base | 0,769 | 1,075 | 0,499 |
| Ridge | Con eventos | 0,766 | 1,076 | 0,498 |
| Lineal | Con eventos | 0,766 | 1,076 | 0,498 |
| Random Forest | Con eventos | 0,816 | 1,098 | 0,477 |
| Dummy media | Base | 1,160 | 1,519 | -0,001 |

Se seleccionó **Random Forest con variables base** antes de abrir test. Los eventos no mejoraron la validación de esta tarea de regresión. Esto no implica que sean inútiles: todavía deben evaluarse para la clasificación de alertas de S7.

## Resultado final en test

| Modelo | MAE (°C) | RMSE (°C) | R² | Mejora de RMSE frente a Dummy |
|---|---:|---:|---:|---:|
| Random Forest base | **0,739** | **1,124** | **0,607** | **37,61 %** |
| Dummy media | 1,256 | 1,802 | -0,010 | 0 % |

El sesgo medio fue -0,003 °C y el percentil 95 del error absoluto fue 1,994 °C. El modelo mejora claramente el baseline global.

## Riesgo en excursiones

Test contiene 232 lecturas con excursión futura real. En ese subconjunto:

- MAE: 2,431 °C.
- El 56,90 % de las predicciones quedó en cero o por debajo pese a existir una excursión futura.

La regresión describe bien el conjunto global, pero todavía subestima demasiados casos críticos. Por ello no debe usarse sola como alarma. S7 debe evaluar directamente la clasificación de desviaciones, con prioridad en recall y falsos negativos.

## Errores por grupo

- Camiones refrigerados: RMSE 1,096 °C.
- Camiones secos: RMSE 1,223 °C.
- Lecturas con evento previo en 24 h: RMSE 1,006 °C.
- Lecturas sin evento previo: RMSE 1,145 °C.
- Las 23 lecturas sin centro correspondiente presentan RMSE 1,996 °C; corresponden a la cobertura parcial ya documentada de WMS Orders.

Estas comparaciones son diagnósticas y no se usaron para volver a seleccionar el modelo después de abrir test.

## Conclusión

Random Forest base supera al promedio y explica aproximadamente el 60,7 % de la variación observada en el corte final. Las variables de eventos no aportaron mejora en validación para la magnitud continua. El desempeño sobre excursiones reales justifica continuar con S7, donde el problema se formulará como alerta binaria y el costo principal será no detectar una desviación.

