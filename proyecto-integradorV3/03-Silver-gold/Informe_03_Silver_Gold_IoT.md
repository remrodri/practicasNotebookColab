# Informe 03 — Construcción Silver a Gold IoT

## Objetivo

Construir una tabla predictiva por lectura sin mezclar viajes ni utilizar datos futuros como predictores.

## Resultados

- Filas Silver: 28,465
- Filas Gold: 28,465
- Viajes: 1,200
- Temperaturas anteriores disponibles: 27,265
- Variaciones de 30 minutos disponibles: 26,961
- Ventanas de 60 minutos evaluables: 25,797
- Ventanas no evaluables: 2,668
- Objetivos positivos: 1,296
- Objetivos negativos: 24,501
- Diferencias frente a la etiqueta recibida: 4

## Definiciones

- `temperatura_anterior`: lectura inmediatamente anterior del mismo viaje.
- `variacion_temperatura_30min`: temperatura actual menos la lectura cercana a 30 minutos atrás, con tolerancia de 5 minutos.
- `desviacion_proximos_60min_flag`: vale 1 si existe una desviación en `(t, t+60 min]`; vale 0 si la ventana está completa y no aparece una desviación.
- `ventana_objetivo_evaluable`: confirma que existe una lectura cercana al final de los 60 minutos.

## Conciliación

Gold conserva exactamente una fila por cada fila Silver: 28,465 = 28,465.

## Limitación

La reconstrucción utiliza únicamente lecturas Silver. Si una lectura con una desviación quedó en cuarentena, el evento no puede observarse desde Gold y puede diferir de la etiqueta recibida en Bronze.

Ejecución UTC: 2026-09-28T17:38:19.033060+00:00
