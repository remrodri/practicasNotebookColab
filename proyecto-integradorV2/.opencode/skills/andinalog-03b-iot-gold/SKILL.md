---
name: andinalog-03b-iot-gold
description: Construye o revisa el notebook ejecutado y el informe que transforman IoT Silver de AndinaLog 03B en una tabla Gold por lectura con predictores temporales y la etiqueta de desviacion futura a 60 minutos. Usar antes del EDA y del modelado.
---

# AndinaLog 03B IoT Silver a Gold

Construye una tabla analitica reproducible a partir de IoT Silver aprobado. Lee [references/contrato.md](references/contrato.md) antes de definir ventanas temporales.

## Entradas y entregables

Entrada minima: IoT Silver y su evidencia de auditoria aprobada.

Entrega:

1. Notebook `.ipynb` ejecutado con salidas visibles.
2. Informe `.md` basado en esa ejecucion.
3. CSV Gold a nivel de lectura.

## Flujo

1. Inspecciona columnas, tipos, granularidad, frecuencia y claves reales.
2. Centraliza rutas, nombres, horizonte, ventana, tolerancias y reglas en `config`.
3. Ordena por viaje u orden y timestamp UTC; comprueba monotonicidad y duplicados.
4. Genera temperatura anterior sin cruzar entidades.
5. Calcula la variacion de 30 minutos con una operacion consciente del tiempo.
6. Construye `desviacion_proximos_60min_flag` dentro de la misma entidad y en `(t, t+60 min]`.
7. Marca por separado si la ventana objetivo es completamente evaluable.
8. Conserva una fila Gold por lectura Silver y valida que no haya multiplicacion ni perdida silenciosa.
9. Exporta Gold y redacta el informe con conteos, definiciones, cobertura y reproducibilidad.

## Reglas estrictas

- El futuro solo se utiliza para construir la variable objetivo, nunca un predictor.
- No asignes objetivo `0` a una lectura sin cobertura suficiente hasta completar los 60 minutos.
- No combines viajes, ordenes o camiones al calcular rezagos o ventanas.
- Conserva timestamps UTC y documenta la clave de agrupacion.
- No fuerces joins; IoT es suficiente si contiene las variables requeridas.
- Si una variable minima no existe ni puede derivarse sin ambiguedad, documenta la limitacion.
- Gold conserva filas no evaluables con objetivo nulo y bandera explicita.
