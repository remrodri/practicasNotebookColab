# Informe de tratamiento de Inventory Tracking

**Fuente Bronze SHA-256:** `4142c8736512c78c553bdd78dd49b6fe304039f7deec8cc096102d31289a1619`
**Versión:** `GIAD-M3-S4-INVENTORY-tratamiento-v1`

## Resultado del lote

Se conservaron las 6,040 filas Bronze. La cuarentena pasó de 133 a 133 filas; 0 salieron después de resolver todos sus motivos. Silver contiene 5,907 movimientos. Se registraron 0 problemas resueltos, 95 pendientes y 39 copias excluidas.

## Tratamientos aplicados

- Se prepararon 0 fechas válidas `DD/MM/YYYY` como `YYYY-MM-DD`, conservando el valor Bronze.
- Se prepararon 0 identificadores de producto en mayúsculas cuando coincidían con un identificador canónico presente en el lote.
- No se imputaron fechas de vencimiento ni cantidades; no se corrigieron fechas imposibles ni mermas negativas por suposición.
- Una salida más merma menor que el ingreso se admite como posible stock remanente; solo el exceso sería inconsistente.

## Duplicados y selección canónica

Se eligieron 39 movimientos canónicos de pares exactamente idénticos y 0 de pares equivalentes tras una normalización de fecha aprobada. Se conservaron 39 copias excluidas para auditoría.
Los conflictos sin evidencia suficiente siguen pendientes; cada decisión consta en `andinalog_inventory_tracking_decisiones_duplicados.csv`.

## Motivos que permanecen en cuarentena

| Columna | Código | Motivos finales |
|---|---|---:|
| cantidad_ingreso | NO_NUMERICA | 10 |
| cantidad_merma | NEGATIVA | 5 |
| fecha_ingreso | FORMATO_FECHA_DISTINTO | 25 |
| fecha_salida | FECHA_INVALIDA | 5 |
| fecha_vencimiento | FALTANTE | 18 |
| movimiento_id | CLAVE_EN_CONFLICTO | 2 |
| movimiento_id | DUPLICADO_IDENTICO | 39 |
| producto_id | FORMATO_INVALIDO | 30 |

Una fila puede tener varios motivos. El CSV de acciones detalla cada intento y el archivo tratado conserva el estado inicial y final.

## Reglas y límites de esta ejecución

- `DUPLICADO_IDENTICO`: **APROBADA**. Tratamiento: Elegir primera fila canónica y excluir copia exacta posterior. Validación: Las doce columnas Bronze deben ser idénticas; una sola canónica por movimiento_id. Acuerdo: Regla de copias idénticas aprobada en el catálogo IoT del proyecto; se aplica al mismo criterio sobre las doce columnas Bronze
- `DUPLICADO_EQUIVALENTE_FECHA`: **PENDIENTE**. Tratamiento: Elegir primera fila si la única diferencia desaparece tras normalizar fecha aprobada. Validación: Requiere FECHA_DDMM_A_ISO aprobada; dos filas equivalentes en las doce columnas preparadas. Acuerdo: pendiente.
- `DUPLICADO_CONFLICTIVO`: **PENDIENTE**. Tratamiento: Conservar ambas filas en cuarentena. Validación: Fuente autoritativa para decidir si hay dos movimientos o un error de captura. Acuerdo: pendiente.
- `FECHA_DDMM_A_ISO`: **PENDIENTE**. Tratamiento: Interpretar fecha válida DD/MM/YYYY y preparar YYYY-MM-DD. Validación: Fecha válida en formato DD/MM/YYYY; revisar día y mes antes de aprobar. Acuerdo: pendiente.
- `PRODUCTO_MAYUSCULAS`: **PENDIENTE**. Tratamiento: Preparar identificador en mayúsculas solo si existe el canónico en el lote. Validación: Confirmar equivalencia de producto con catálogo maestro; la coincidencia del lote es solo control técnico. Acuerdo: pendiente.
- `FECHA_VENCIMIENTO_FALTANTE`: **PENDIENTE**. Tratamiento: Conservar en cuarentena sin imputación automática. Validación: Vencimiento verificable en fuente del lote. Acuerdo: pendiente.
- `FECHA_IMPOSIBLE`: **PENDIENTE**. Tratamiento: Conservar en cuarentena sin inventar fecha. Validación: Fecha original recuperada de fuente autorizada. Acuerdo: pendiente.
- `CANTIDAD_INGRESO_NO_NUMERICA`: **PENDIENTE**. Tratamiento: Conservar en cuarentena; no traducir 'cien' automáticamente. Validación: Cantidad numérica confirmada en documento de ingreso. Acuerdo: pendiente.
- `MERMA_NEGATIVA`: **PENDIENTE**. Tratamiento: Conservar en cuarentena; no cambiar signo automáticamente. Validación: Merma real confirmada por registro operativo. Acuerdo: pendiente.
- `COHERENCIA_TEMPORAL`: **PENDIENTE**. Tratamiento: Conservar en cuarentena hasta aclarar secuencia y días. Validación: Fechas y duración reconciliadas con fuente autorizada. Acuerdo: pendiente.
- `EXCESO_CANTIDADES`: **PENDIENTE**. Tratamiento: Conservar en cuarentena; no equilibrar cifras automáticamente. Validación: Ingreso salida y merma conciliados; el remanente positivo es válido. Acuerdo: pendiente.
- `OTROS_PROBLEMAS`: **PENDIENTE**. Tratamiento: Conservar en cuarentena y revisar contra fuente operativa. Validación: Valor original verificado y regla específica aprobada antes de liberar. Acuerdo: pendiente.

Una fila permaneció en cuarentena cuando no había una regla aprobada, faltaba evidencia o quedaba otro motivo sin resolver. No se forzó ninguna liberación.
