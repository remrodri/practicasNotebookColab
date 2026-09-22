# Matriz de transformaciones B6 — Inventory Tracking v2

| Variable | Entrada | Regla / acción | Salida + bandera | Prueba | Responsable | Versión | Fecha |
|---|---|---|---|---|---|---|---|
| `movimiento_id` | Bronze | Claves únicas y formato válido | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `lote_id` | Bronze | Claves únicas y formato válido | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `producto_id` | Bronze | Claves únicas y formato válido | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `centro_distribucion` | Bronze | Claves únicas y formato válido | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `fecha_ingreso` | Bronze | Claves únicas y formato válido | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `fecha_salida` | Bronze | Claves únicas y formato válido | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `fecha_vencimiento` | Bronze | Claves únicas y formato válido | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `cantidad_ingreso` | Bronze | Claves únicas y formato válido | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `cantidad_salida` | Bronze | Claves únicas y formato válido | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `cantidad_merma` | Bronze | Claves únicas y formato válido | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `dias_en_almacen` | Bronze | Claves únicas y formato válido | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| `costo_unitario_bob` | Bronze | Claves únicas y formato válido | Conservar original + `_en_cuarentena` + `_motivo` | Conteo por campo en reporte | Grupo 06 | v2 | 2026-09-22 |
| Fila | Diagnóstico completo | Tratamiento: Normalizar formatos de fecha y producto; inferir vencimiento faltante solo si el producto tiene al menos 20 lotes válidos y una única vida útil observada. Registrar vencimiento_imputado y excluirlo del KPI de vencimiento observado. Excluir duplicados, conflictos y valores imposibles. | Silver o cuarentena final; `decision_tratamiento`, `motivo_cuarentena_final` | Silver + cuarentena final = 6040 | Grupo 06 | v2 | 2026-09-22 |

Esta matriz resume las decisiones. Los motivos concretos por fila se encuentran en los CSV y la lógica ejecutable en los notebooks. Las cantidades son unidades del producto, sin equivalencia supuesta a kg o cajas. Las fechas son fechas de calendario sin conversión horaria. Un vencimiento estimado no confirma el vencimiento físico del lote.
