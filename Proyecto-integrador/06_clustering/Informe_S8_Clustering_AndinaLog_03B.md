# Informe S8 — Clustering de viajes AndinaLog 03B

## Objetivo

Identificar perfiles operativos entre los viajes de entrenamiento sin utilizar los objetivos futuros para construir los grupos.

La unidad de clustering es **un viaje**. Esta decisión evita que un viaje con más lecturas tenga mayor peso únicamente por su frecuencia de registro.

## Datos utilizados

- Partición utilizada: `AJUSTE` definida en S6.
- Viajes: 796.
- Lecturas resumidas: 19.017.
- Variables de clustering: 19.
- Objetivos incluidos en K-Means: ninguno.

Las variables resumen temperatura, humedad, estabilidad térmica, duración, capacidad, cantidad transportada y eventos históricos. Las variables fueron imputadas con mediana y estandarizadas antes de calcular distancias.

## Selección del número de clusters

| k | Inercia | Silhouette | Tamaño mínimo | Tamaño máximo |
|---:|---:|---:|---:|---:|
| 2 | 10.808,94 | 0,3032 | 386 | 410 |
| 3 | 9.360,12 | **0,3310** | 78 | 409 |
| 4 | 8.448,56 | 0,3209 | 76 | 322 |
| 5 | 7.820,29 | 0,3198 | 34 | 321 |
| 6 | 7.280,19 | 0,2766 | 34 | 322 |

Se seleccionó **k=3** porque presenta el silhouette más alto y produce grupos interpretables sin crear segmentos excesivamente pequeños.

## Perfiles encontrados

### Cluster 0 — Prioridad térmica alta

- 78 viajes.
- 100 % presenta al menos una desviación futura.
- 26,51 % de sus lecturas tiene desviación futura.
- Máximo desvío futuro medio: 5,493 °C.
- 65,4 % corresponde a productos frescos y 33,3 % a congelados.
- 88,5 % utiliza camión refrigerado.
- Mayor frecuencia media de eventos previos que los otros grupos.

Este cluster debe priorizarse para investigar condiciones térmicas, rutas, equipos y reglas de operación. El clustering no demuestra que los eventos o el tipo de producto causen las desviaciones.

### Cluster 1 — Cadena de frío relativamente estable

- 309 viajes.
- 23,63 % presenta alguna desviación futura.
- 2,11 % de sus lecturas tiene desviación futura.
- Máximo desvío futuro medio: -0,214 °C.
- Combina principalmente productos frescos y congelados.
- 99,4 % utiliza camión refrigerado.
- Presenta la menor pendiente térmica máxima media.

### Cluster 2 — Operación seca

- 409 viajes.
- 18,09 % presenta alguna desviación futura.
- 2,33 % de sus lecturas tiene desviación futura.
- Máximo desvío futuro medio: -0,741 °C.
- 100 % corresponde a categoría logística seca.
- Temperatura media cercana a 20,06 °C.
- Se distribuye entre camiones secos y refrigerados.

## Interpretación

K-Means separó principalmente tres regímenes coherentes:

1. viajes con comportamiento térmico crítico;
2. cadena de frío estable;
3. operación de productos secos.

El cluster 0 concentra el mayor riesgo observado y puede servir para orientar una revisión del negocio. Sin embargo, los clusters no son etiquetas oficiales y sus números son arbitrarios: `cluster 0` no significa por definición “crítico” fuera de esta corrida.

## Uso posterior

- S9 puede utilizar estos perfiles únicamente como evidencia exploratoria o variable derivada del entrenamiento, cuidando que la asignación de validación y test se haga con el transformador ajustado en `AJUSTE`.
- No se recomienda usar el objetivo futuro como predictor ni ajustar nuevamente los clusters con test.
- Antes de una decisión operativa deben revisarse ejemplos concretos del cluster prioritario con responsables de cadena de frío.

## Limitaciones

- Datos sintéticos y un solo periodo.
- Silhouette moderado; existe solapamiento entre perfiles.
- Los agregados ocultan parte de la evolución temporal dentro del viaje.
- La asociación con desviaciones futuras se calculó después de formar los clusters y no demuestra causalidad.

