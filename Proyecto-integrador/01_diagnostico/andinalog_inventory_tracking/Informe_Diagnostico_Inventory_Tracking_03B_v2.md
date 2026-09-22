# Informe de diagnóstico — Inventory Tracking v2

Grupo 06, AndinaLog 03B. Fecha: 2026-09-22.

## Qué se evaluó

Claves únicas y formato válido; referencia parcial a Productos Silver; fechas de calendario válidas y secuencia coherente; cantidades no negativas y saldo no negativo; costo positivo. La salida posterior al vencimiento es riesgo operativo y no causa cuarentena por sí sola. Se conservaron todos los valores Bronze. El diagnóstico detecta y explica; no normaliza ni imputa.

## Resultado verificado

| Medida | Filas |
|---|---:|
| Bronze y diagnosticado | 6040 |
| Cuarentena diagnóstica | 109 |
| Sin cuarentena inicial | 5931 |

La salida incluye, para cada una de las 12 columnas Bronze, una bandera `*_en_cuarentena` y su `*_motivo`. `en_cuarentena` resume las banderas. El reporte de calidad contiene conteos globales y por campo. `cuarentena` contiene exactamente las filas marcadas del diagnosticado.

## Destino

El tratamiento lee el diagnosticado completo, incluidas las 109 filas marcadas, porque algunas anomalías tienen resolución trazable. Las cantidades son unidades del producto, sin equivalencia supuesta a kg o cajas. Las fechas son fechas de calendario sin conversión horaria. Un vencimiento estimado no confirma el vencimiento físico del lote.
