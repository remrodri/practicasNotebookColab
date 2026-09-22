# Contrato de ingesta — AndinaLog 03B — Inventory Tracking v2

Responsable: Grupo 06, rol 03B. Versión: 2. Fecha: 2026-09-22.

| Elemento | Acuerdo |
|---|---|
| Fuente | `datasets/AndinaLog_03B_Bronce/andinalog_inventory_tracking.csv` |
| Formato | CSV UTF-8; primera fila con encabezados; se leen los campos como texto para no alterar Bronze |
| Frecuencia | No especificada por la fuente; no se supone una cadencia de actualización |
| Granularidad | Una fila Bronze; `fila_bronze` conserva su posición |
| Campos | movimiento_id, lote_id, producto_id, centro_distribucion, fecha_ingreso, fecha_salida, fecha_vencimiento, cantidad_ingreso, cantidad_salida, cantidad_merma, dias_en_almacen, costo_unitario_bob |
| Calidad | Claves únicas y formato válido; referencia parcial a Productos Silver; fechas de calendario válidas y secuencia coherente; cantidades no negativas y saldo no negativo; costo positivo. La salida posterior al vencimiento es riesgo operativo y no causa cuarentena por sí sola. |
| Diagnóstico | `diagnosticado` completo, subconjunto `cuarentena`, `reporte_calidad`; para cada campo, `_en_cuarentena` y `_motivo`. La bandera de fila es OR de las banderas de campo. El motivo puede describir revisión aunque la bandera sea falsa. El original no se modifica. |
| Tratamiento | Normalizar formatos de fecha y producto; inferir vencimiento faltante solo si el producto tiene al menos 20 lotes válidos y una única vida útil observada. Registrar vencimiento_imputado y excluirlo del KPI de vencimiento observado. Excluir duplicados, conflictos y valores imposibles. |
| Salida | Silver y cuarentena final particionan diagnosticado; `reporte_calidad` resume la etapa. Silver conserva Bronze, marcas diagnósticas, valores tratados y acciones. `en_cuarentena_diagnostico` identifica la decisión previa. |

Las cantidades son unidades del producto, sin equivalencia supuesta a kg o cajas. Las fechas son fechas de calendario sin conversión horaria. Un vencimiento estimado no confirma el vencimiento físico del lote.

La cuarentena de diagnóstico es un subconjunto del diagnosticado y no debe concatenarse con él. No hay catálogo externo obligatorio: las reglas están visibles en los notebooks y documentadas aquí.
