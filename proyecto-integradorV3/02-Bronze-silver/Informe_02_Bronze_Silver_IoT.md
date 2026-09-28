# Informe 02 — Tratamiento Bronze a Silver de IoT

## Objetivo

Preparar las lecturas de telemetría de AndinaLog sin inventar mediciones y separar los errores no resolubles en cuarentena.

## Unidad de observación

Una fila representa una lectura de telemetría de un viaje en un momento determinado.

## Resultados

- Filas Bronze: 28,920
- Filas Silver: 28,465
- Filas en cuarentena: 455
- Códigos de camión normalizados: 50
- Temperaturas Fahrenheit convertidas: 50
- Filas imputadas: 0

## Motivos de cuarentena

- temperatura_centinela: 120 filas
- duplicado_redundante: 115 filas
- humedad_vacia: 100 filas
- temperatura_vacia: 80 filas
- humedad_fuera_rango: 15 filas
- fecha_invalida: 15 filas
- duplicado_conflictivo: 10 filas
- unidad_no_admitida: 5 filas

## Decisiones principales

- Celsius es la unidad final.
- Fahrenheit se convierte mediante una fórmula exacta.
- Kelvin permanece en cuarentena porque no es una unidad esperada.
- `-999` se reconoce como ausencia de medición.
- Las fechas imposibles no se adivinan.
- Los duplicados redundantes y conflictivos se conservan en cuarentena con su motivo.
- No se imputaron temperaturas ni humedades.

## Conciliación

28,920 filas Bronze = 28,465 filas Silver + 455 filas en cuarentena.

## Limitaciones

No se validó la existencia de viajes, camiones, órdenes o productos contra tablas maestras porque esas fuentes no forman parte de este tratamiento. Esta ausencia de enriquecimiento no invalida por sí sola una lectura correcta.

Ejecución UTC: 2026-09-28T17:31:38.526893+00:00
