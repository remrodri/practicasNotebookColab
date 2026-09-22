# Contrato de ingesta — AndinaLog 03B — Productos v2

Responsable: Grupo 06, rol 03B. Versión: 2. Fecha: 2026-09-22.

| Elemento | Acuerdo |
|---|---|
| Fuente | `datasets/AndinaLog_03B_Bronce/andinalog_productos.csv` |
| Formato | CSV UTF-8; primera fila con encabezados; se leen los campos como texto para no alterar Bronze |
| Frecuencia | No especificada por la fuente; no se supone una cadencia de actualización |
| Granularidad | Una fila Bronze; `fila_bronze` conserva su posición |
| Campos | producto_id, nombre_producto, categoria_logistica, temperatura_conservacion_requerida_c, tolerancia_temperatura_c, precio_unitario_bob, costo_unitario_bob |
| Calidad | ID PROD-### único; categoría Fresco, Congelado o Seco; objetivo y tolerancia térmica coherentes con la categoría; precios y costos BOB positivos. Precio menor que costo es observación comercial. |
| Diagnóstico | `diagnosticado` completo, subconjunto `cuarentena`, `reporte_calidad`; para cada campo, `_en_cuarentena` y `_motivo`. La bandera de fila es OR de las banderas de campo. El motivo puede describir revisión aunque la bandera sea falsa. El original no se modifica. |
| Tratamiento | Normalizar ID sin conflicto. Inferir categoría únicamente con objetivo, tolerancia y vida útil observada concordantes; inferir objetivo faltante solo con categoría, tolerancia y vida útil concordantes. Marcar categoria_imputada y temperatura_imputada. Excluir duplicados posteriores y conflictos. |
| Salida | Silver y cuarentena final particionan diagnosticado; `reporte_calidad` resume la etapa. Silver conserva Bronze, marcas diagnósticas, valores tratados y acciones. `en_cuarentena_diagnostico` identifica la decisión previa. |

Los patrones térmicos y de vida útil provienen de este dataset; no son límites universales. Los umbrales inferidos no son aptos para el KPI térmico observado.

La cuarentena de diagnóstico es un subconjunto del diagnosticado y no debe concatenarse con él. No hay catálogo externo obligatorio: las reglas están visibles en los notebooks y documentadas aquí.
