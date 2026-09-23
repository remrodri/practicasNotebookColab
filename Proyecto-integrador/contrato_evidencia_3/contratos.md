# Contratos predictivos — AndinaLog 03B, Evidencia 3

## Contrato 1: Regresión

| Elemento | Definición |
|---|---|
|---|---|
| **Decisión** | Anticipar la magnitud de la desviación térmica para decidir si se debe intervenir el transporte. |
| **Unidad de observación** | Una lectura de telemetría de un viaje. |
| **Instante y horizonte** | Predicción en el momento de la lectura para los próximos **60 minutos**. Las fechas sin zona explícita se interpretan como hora de Bolivia. |
| **Objetivo `y`** | `max_desvio_termico_proximos_60min_c`, máximo futuro de `desvio_respecto_umbral_c` dentro del mismo viaje. Ya fue construido en el EDA integrado; 27.477 lecturas son aptas para regresión. |
| **Predictoras base** | Temperatura y humedad actuales, rezagos y tendencias históricas, tiempo desde inicio, temperatura requerida, tolerancia, producto, camión y pedido disponibles al instante de lectura. |
| **Predictoras de eventos** | Conteos de eventos y alertas anteriores en 60 min, 180 min y 24 h; fallas, severidad, reconocimiento, recencia, mantenimiento y configuración del camión. |
| **Split** | Temporal y por viaje: un mismo `viaje_id` no puede quedar repartido entre entrenamiento, validación y prueba. |
| **Baseline y métricas** | `DummyRegressor` como referencia; comparar MAE, RMSE y R². La utilidad de eventos se acepta solo si mejora la validación temporal. |
| **Exclusiones por fuga** | Objetivo futuro, lecturas posteriores, eventos con fecha igual o posterior al instante de predicción y datos reales de entrega conocidos después. |

## Contrato 2: Clasificación

| Elemento | Definición |
|---|---|
|---|---|
| **Decisión** | Alertar si el camión tendrá una desviación térmica en la próxima hora para decidir una intervención. |
| **Unidad de observación** | Una lectura de telemetría de un viaje. |
| **Instante y horizonte** | Predicción en el momento de la lectura para los próximos **60 minutos**. |
| **Objetivo `y`** | `clasificacion_objetivo_60min`: 1 si habrá desviación y 0 en caso contrario. Hay 28.557 lecturas aptas y una prevalencia aproximada de 4,63 %. |
| **Predictoras** | Las mismas familias del contrato de regresión, restringidas a información presente o histórica. |
| **Split** | Temporal y por viaje, preservando la proporción de la clase cuando sea posible sin romper el orden temporal. |
| **Baseline y métricas** | Baseline mayoritario y modelo clásico; priorizar recall de la clase positiva, PR-AUC, matriz de confusión y costo de falsos negativos. |
| **Exclusiones por fuga** | El propio objetivo, cualquier resumen que use la ventana futura y eventos iguales o posteriores al instante de predicción. |

## Contrato de la integración de eventos

La unión utiliza `camion_id` y exige `timestamp_evento < timestamp_lectura`. Las variables se agregan por ventanas históricas y nunca se incorpora una fila de evento directamente a cada lectura. Esto conserva las 28.677 filas IoT y evita producto cartesiano.

`valor_lectura_numerico` permanece fuera del primer modelo porque el JSON no declara una unidad homogénea por tipo de evento.

