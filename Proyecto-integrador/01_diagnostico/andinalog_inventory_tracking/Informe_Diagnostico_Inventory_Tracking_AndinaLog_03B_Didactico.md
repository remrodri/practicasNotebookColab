# Informe del Notebook 1: diagnóstico didáctico de Inventory Tracking — AndinaLog 03B

## Propósito y alcance

El notebook `S4_01_AndinaLog_Inventory_Tracking_Diagnostico_Didactico.ipynb` analiza el CSV Bronze de movimientos de inventario del grupo 06, subcaso 03B. Su objetivo es identificar problemas técnicos y riesgos de negocio que afectan la rotación de lotes, la merma y el vencimiento de productos.

El diagnóstico **no modifica** los 12 campos originales, no imputa valores y no elimina filas. Añade un estado y un motivo por campo, además de un resumen por fila. Las reglas están escritas dentro del notebook, sin catálogo ni motor externo. El tratamiento posterior decidirá normalizaciones, correcciones y exclusiones.

## Entradas y salidas

| Elemento | Ruta relativa a `practicasNotebookColab` | Función |
|---|---|---|
| Bronze | `datasets/AndinaLog_03B_Bronce/andinalog_inventory_tracking.csv` | Entrada original: 6.040 filas y 12 columnas. |
| Productos Silver | `proyecto-integrador/andinalog_productos/notebook2/salidas/andinalog_productos_silver.csv` | Referencia opcional y de cobertura parcial para producto y costo. |
| Notebook | `proyecto-integrador/01_diagnostico/andinalog_inventory_tracking/S4_01_AndinaLog_Inventory_Tracking_Diagnostico_Didactico.ipynb` | Reglas y validaciones. |
| Diagnosticado | `proyecto-integrador/01_diagnostico/andinalog_inventory_tracking/salidas/andinalog_inventory_tracking_didactico_v1_diagnosticado.csv` | Todas las filas, con resultados por campo. |
| Cuarentena | `proyecto-integrador/01_diagnostico/andinalog_inventory_tracking/salidas/andinalog_inventory_tracking_didactico_v1_cuarentena.csv` | Subconjunto con al menos un estado `CRITICO`. |

La cuarentena diagnóstica **ya está incluida** en el diagnosticado; los archivos no deben concatenarse.

## Diccionario de negocio y reglas por columna

Cada fila representa un movimiento/lote. Las cantidades de ingreso, salida y merma se interpretan como **unidades de inventario del producto dentro de la fila**. El CSV no especifica si una unidad física es pieza, caja, kilogramo u otra presentación. `costo_unitario_bob` es el costo declarado por unidad de inventario. No se etiquetan las cantidades como kg ni se convierten unidades sin documentación.

| Campo Bronze | Significado | Regla de diagnóstico |
|---|---|---|
| `movimiento_id` | Identificador del movimiento. | Obligatorio; patrón `MOV-` más seis dígitos. Se distinguen copias exactas posteriores y claves repetidas con datos contradictorios. |
| `lote_id` | Identificador del lote. | Obligatorio; patrón `LOT-`, año de cuatro dígitos, guion y cinco dígitos. Se comprueba la unicidad y se distingue copia de conflicto. |
| `producto_id` | Producto del lote. | Obligatorio; patrón `PROD-` más tres dígitos. Ausencia en Productos Silver implica revisión, pues su cobertura es parcial. |
| `centro_distribucion` | Centro donde se registra el lote. | Obligatorio; solo Cochabamba, La Paz, Santa Cruz, Oruro o Tarija. |
| `fecha_ingreso` | Día de ingreso del lote. | Obligatoria y válida. `AAAA-MM-DD` es el formato canónico; `DD/MM/AAAA` válido requiere normalización posterior. |
| `fecha_salida` | Día de salida del lote. | Puede estar vacía si el lote sigue en almacén. Si está informada, debe ser una fecha válida no anterior al ingreso. Una salida después del vencimiento se marca como riesgo operativo. |
| `fecha_vencimiento` | Día límite del lote. | Obligatoria para evaluar el riesgo de vencimiento; debe ser una fecha válida no anterior al ingreso. |
| `cantidad_ingreso` | Unidades de inventario que ingresan al lote. | Entero mayor que cero. |
| `cantidad_salida` | Unidades de inventario que salen del lote. | Entero no negativo; puede ser cero. |
| `cantidad_merma` | Unidades de inventario perdidas o descartadas. | Entero no negativo; puede ser cero. |
| `dias_en_almacen` | Días declarados de permanencia. | Entero no negativo; si hay fecha de salida válida, se compara con la diferencia entre salida e ingreso. Sin salida, esa comparación no es evaluable. |
| `costo_unitario_bob` | Costo declarado por unidad de inventario, en bolivianos. | Numérico y mayor que cero. Donde hay Producto Silver, una diferencia superior a 0,01 BOB se señala para revisión, sin suponer que el costo maestro actual deba sustituir al costo histórico del lote. |

## Relaciones entre campos y severidad

- **Balance de unidades:** si los tres valores son numéricos y no negativos, `cantidad_salida + cantidad_merma > cantidad_ingreso` es `CRITICO`. Un remanente positivo está permitido; no se exige igualdad entre ingreso, salida y merma.
- **Orden temporal:** salida anterior al ingreso o vencimiento anterior al ingreso es `CRITICO`.
- **Salida posterior al vencimiento:** es `REVISAR`. Puede describir un hecho relevante para el mandato de negocio; no debe desaparecer por cuarentena solo por esa relación temporal.
- **Fecha de salida vacía:** `NO_EVALUABLE` en la fecha de salida y en la comparación de `dias_en_almacen`; no se interpreta como fecha inválida. El archivo actual no contiene casos de salida vacía.
- **Vencimiento faltante:** `CRITICO`, pues impide calcular días para vencer y evaluar el riesgo del lote.
- **Duplicados:** una copia íntegra posterior se marca crítica en las claves; un mismo `movimiento_id` o `lote_id` con información diferente marca críticas todas las variantes. El diagnóstico no decide qué fila conservar cuando hay conflicto.
- **Productos Silver:** una clave bien formada sin correspondencia se marca `REVISAR`; no se declara inválida solo por la cobertura parcial de esa tabla.

Los estados son `OK`, `NO_EVALUABLE`, `REVISAR` y `CRITICO`, en ese orden de severidad. `en_cuarentena=True` cuando al menos una columna tiene `CRITICO`; los riesgos y advertencias `REVISAR` permanecen en el diagnosticado para análisis y tratamiento.

## Columnas añadidas y trazabilidad

El diagnosticado tiene **44 columnas**: las 12 Bronze, `fila_bronze`, 12 pares `*_estado`/`*_motivo` y siete campos de resumen y trazabilidad: `cantidad_columnas_con_problemas`, `en_cuarentena`, `severidad_maxima`, `columnas_con_problemas`, `motivos_fila`, `version_diagnostico`, `sha256_bronze`.

`fila_bronze` identifica la posición original. `sha256_bronze` permite comprobar que el resultado corresponde a una versión exacta del CSV fuente. Un campo puede reunir varios motivos; el estado conserva la severidad mayor.

## Resultados de la ejecución revisada

| Indicador | Resultado |
|---|---:|
| Filas Bronze y diagnosticadas | 6.040 |
| Filas sin problemas detectados | 4.536 |
| Filas con uno o más problemas o advertencias | 1.504 |
| Filas con severidad máxima `REVISAR` | 1.395 |
| Filas con severidad máxima `CRITICO` y en cuarentena | 109 |
| Salidas posteriores al vencimiento | 476 |
| Ingresos con formato válido `DD/MM/AAAA` | 25 |
| Fechas de vencimiento faltantes | 18 |
| Fechas de salida imposibles | 5 |
| IDs de producto con formato inválido | 30 |
| Copias exactas posteriores | 39 |
| Filas con clave de movimiento/lote en conflicto | 2 |
| Ingresos no numéricos | 10 |
| Mermas negativas | 5 |
| Filas con `producto_id` bien formado sin correspondencia en Productos Silver | 1.019 |

Los conteos por regla **se pueden solapar**. Por ejemplo, una fila duplicada se marca tanto en `movimiento_id` como en `lote_id`; no deben sumarse esos hallazgos como si fueran filas distintas.

El diagnóstico anterior enviaba 133 filas a cuarentena. Esta versión envía 109 porque distingue las 25 fechas válidas con formato alternativo como `REVISAR` y aplica la separación explícita entre defecto de calidad y riesgo de negocio. Los resultados no deben compararse solo por el conteo: cambiaron las reglas y la estructura de salida.

## Validaciones y límites

El notebook comprueba el esquema, que las 12 columnas originales no se modificaron, que se conservaron las 6.040 filas, que `fila_bronze` es única, que toda fila en cuarentena tiene motivo y que el hash Bronze no cambió antes de exportar. Genera exactamente los dos CSV indicados.

La tabla Productos Silver es parcial; la falta de correspondencia no equivale a un producto inexistente. La presentación física de las unidades de inventario no figura en las fuentes revisadas. Las fechas son días de calendario y no incluyen hora: la decisión sobre hora de Bolivia y UTC usada en telemetría no añade información a estas columnas. Los riesgos de vencimiento identificados requieren interpretación operativa posterior; el diagnóstico no corrige el evento ni determina responsabilidad.

## Siguiente etapa

El Notebook 2 didáctico deberá leer el **diagnosticado completo**, mantener los valores Bronze y documentar cualquier conversión o exclusión. Puede normalizar fechas `DD/MM/AAAA` y grafías inequívocas de `producto_id`; debe comprobar colisiones antes de decidir duplicados. La fecha imposible, la merma negativa, una cantidad textual y un vencimiento faltante no deben sustituirse automáticamente sin evidencia suficiente.
