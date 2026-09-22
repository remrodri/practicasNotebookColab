# Informe de diagnóstico — Productos v2

Grupo 06, AndinaLog 03B. Fecha: 2026-09-22.

## Qué se evaluó

ID PROD-### único; categoría Fresco, Congelado o Seco; objetivo y tolerancia térmica coherentes con la categoría; precios y costos BOB positivos. Precio menor que costo es observación comercial. Se conservaron todos los valores Bronze. El diagnóstico detecta y explica; no normaliza ni imputa.

## Resultado verificado

| Medida | Filas |
|---|---:|
| Bronze y diagnosticado | 63 |
| Cuarentena diagnóstica | 13 |
| Sin cuarentena inicial | 50 |

La salida incluye, para cada una de las 7 columnas Bronze, una bandera `*_en_cuarentena` y su `*_motivo`. `en_cuarentena` resume las banderas. El reporte de calidad contiene conteos globales y por campo. `cuarentena` contiene exactamente las filas marcadas del diagnosticado.

## Destino

El tratamiento lee el diagnosticado completo, incluidas las 13 filas marcadas, porque algunas anomalías tienen resolución trazable. Los patrones térmicos y de vida útil provienen de este dataset; no son límites universales. Los umbrales inferidos no son aptos para el KPI térmico observado.
