# Informe del Notebook 2: tratamiento didáctico de Inventory Tracking — AndinaLog 03B

## Propósito

El notebook `S4_02_AndinaLog_Inventory_Tracking_Tratamiento_Didactico.ipynb` transforma la salida completa del diagnóstico didáctico de inventario en un **Silver analítico** y una **cuarentena final**. Conserva los 12 valores Bronze y todos los estados y motivos del diagnóstico; agrega valores tratados, acciones y decisiones por fila. Las reglas están dentro del notebook, sin catálogo ni motor externo.

El tratamiento lee el **diagnosticado completo**. La cuarentena del Notebook 1 ya forma parte de ese archivo y no se agrega de nuevo.

## Entradas y salidas

| Elemento | Ruta relativa a `practicasNotebookColab` | Función |
|---|---|---|
| Bronze | `datasets/AndinaLog_03B_Bronce/andinalog_inventory_tracking.csv` | Fuente para verificar integridad y hash. |
| Diagnóstico de entrada | `proyecto-integrador/01_diagnostico/andinalog_inventory_tracking/salidas/andinalog_inventory_tracking_didactico_v1_diagnosticado.csv` | 6.040 filas con estados y motivos. |
| Notebook 2 | `proyecto-integrador/02_tratamiento/andinalog_inventory_tracking/S4_02_AndinaLog_Inventory_Tracking_Tratamiento_Didactico.ipynb` | Reglas de tratamiento. |
| Silver analítico | `proyecto-integrador/02_tratamiento/andinalog_inventory_tracking/salidas/andinalog_inventory_tracking_didactico_v1_silver.csv` | Una fila utilizable por movimiento y lote, incluidas las fechas estimadas identificadas. |
| Cuarentena final | `proyecto-integrador/02_tratamiento/andinalog_inventory_tracking/salidas/andinalog_inventory_tracking_didactico_v1_cuarentena_final.csv` | Duplicados excluidos y valores sin resolución defendible. |

Cada CSV de salida tiene **65 columnas**: las 44 del diagnosticado más los campos de preparación, imputación, balance, riesgo, acciones y destino final.

## Criterios de entrada y trazabilidad

Antes de tratar, el notebook exige las columnas Bronze, los pares `*_estado`/`*_motivo`, `fila_bronze`, la versión esperada de diagnóstico y el hash SHA-256 correspondiente al Bronze actual. También verifica que las 6.040 filas se mantengan en orden y que las 12 columnas originales coincidan exactamente con la fuente. Si una entrada cambia, la ejecución se detiene.

Los campos `en_cuarentena` y `motivos_fila` conservan la decisión diagnóstica. `en_cuarentena_final`, `decision_tratamiento` y `motivo_cuarentena_final` registran la decisión posterior. Una fila antes crítica puede pasar a Silver si se resuelve su problema mediante una regla explícita.

## Reglas deterministas de tratamiento

| Situación | Decisión | Trazabilidad |
|---|---|---|
| Fecha válida `DD/MM/AAAA` | Interpretar día/mes/año y escribir `AAAA-MM-DD` en `*_tratada`. | Fecha Bronze intacta; acción `NORMALIZAR_FECHA_...`. |
| `producto_id` con minúsculas o espacios exteriores | Preparar el ID en mayúsculas. | Original intacto; `producto_id_tratado` y `NORMALIZAR_PRODUCTO_ID`. |
| Copia exacta de las 12 columnas Bronze | Conservar la primera aparición y excluir la copia posterior. | `EXCLUIR_COPIA` y motivo de cuarentena. |
| Dos filas que se vuelven idénticas al normalizar fecha e ID | Conservar la primera y excluir la posterior. | Se comparan las 12 columnas preparadas antes de decidir. |
| Mismo `movimiento_id` o `lote_id` con atributos distintos tras preparar | Cuarentena de las variantes en conflicto. | No se elige una fila arbitrariamente. |
| `cantidad_ingreso = "cien"` | Cuarentena; no convertir a 100 ni derivar ingreso como salida más merma. | Valor Bronze y motivo final. |
| `cantidad_merma` negativa | Cuarentena; no cambiar el signo sin fuente operativa. | Valor Bronze y motivo final. |
| Fecha imposible | Cuarentena; no inventar una fecha. | Texto original y motivo final. |
| Salida posterior al vencimiento | Mantener en Silver si lo demás es válido y marcar riesgo. | `riesgo_salida_post_vencimiento=True`; no se borra el hecho de negocio. |

`cantidad_ingreso`, `cantidad_salida` y `cantidad_merma` se interpretan en **unidades de inventario del producto dentro del lote**. La presentación física no está especificada. El notebook calcula `saldo_unidades_inventario = ingreso − salida − merma`; un saldo positivo es aceptable, un saldo negativo con cantidades válidas causa cuarentena. No impone la igualdad entre ingreso y salida más merma.

## Regla de imputación de `fecha_vencimiento`

Las 18 fechas de vencimiento faltantes se estiman usando la vida útil observada por producto, con condiciones estrictas:

1. Usar solo lotes con `producto_id` preparado válido, ingreso y vencimiento observados y coherentes, y sin copia ni conflicto.
2. Calcular los días entre vencimiento e ingreso por producto.
3. Exigir **al menos 20 lotes válidos** y **una sola duración observada** para ese producto.
4. Para un vencimiento vacío, calcular `fecha_ingreso + duración del producto`. No estimar una fecha imposible ni sobreescribir una fecha observada.

Las 18 filas afectadas pertenecen a 15 productos. Cada uno tiene al menos **89 lotes de respaldo** después de excluir copias y conflictos, y muestran una única duración. Se imputaron 9 fechas con 365 días, 7 con 180 días y 2 con 18 días. El resultado queda en `fecha_vencimiento_tratada`; el campo Bronze `fecha_vencimiento` permanece vacío. `vencimiento_imputado=True`, `vida_util_producto_dias_usada`, `acciones_tratamiento` y `motivos_tratamiento` explican la estimación.

Estas filas **entran en Silver analítico**. La estimación no confirma la fecha de la etiqueta o del registro oficial del lote. Por ello `apto_kpi_vencimiento_observado=False` para las 18 filas. Para una decisión operativa de retiro, venta o alerta sobre un lote concreto, se debe verificar el vencimiento en la fuente del lote. La regla estima una regularidad del dataset, no sustituye esa verificación.

## Riesgo de vencimiento y aptitud de análisis

`riesgo_salida_post_vencimiento` señala que la salida ocurrió después de la fecha de vencimiento tratada. `riesgo_basado_en_vencimiento_imputado` permite distinguir si esa comparación dependió de una estimación. `apto_kpi_vencimiento_observado` identifica las filas Silver cuya fecha de vencimiento estaba realmente registrada.

En la ejecución revisada hay **468 filas Silver** con salida posterior al vencimiento y **ninguna** de esas 468 depende de un vencimiento imputado. El diagnóstico había señalado 476; la diferencia corresponde a filas que no ingresaron en Silver, incluidas copias excluidas. No se debe presentar el número de diagnósticos como si fuera automáticamente el conteo de lotes Silver.

## Resultados de la ejecución revisada

| Medida | Resultado |
|---|---:|
| Filas diagnosticadas de entrada | 6.040 |
| Filas en cuarentena diagnóstica | 109 |
| Filas Silver | 5.980 |
| Filas en cuarentena final | 60 |
| Fechas válidas normalizadas | 25 |
| IDs de producto normalizados | 30 |
| Vencimientos imputados | 18 |
| Copias excluidas | 40 |
| Filas Silver aptas para KPI con vencimiento observado | 5.962 |
| Filas Silver con salida posterior al vencimiento | 468 |

Las **40 copias** incluyen 39 filas idénticas en Bronze y una pareja con la misma clave que se vuelve idéntica tras normalizar su fecha de ingreso. El primer registro se conserva; se excluye la copia posterior.

La cuarentena final se desglosa sin solapamientos: **40 copias**, **10 ingresos no numéricos**, **5 mermas negativas** y **5 fechas de salida imposibles**. La conciliación es **6.040 = 5.980 + 60**.

## Comprobaciones y límites

El notebook verifica que el Bronze y el diagnóstico permanecen intactos, que Silver y cuarentena final forman una partición de la entrada, que `movimiento_id` y `lote_id` son únicos en Silver, que cada fila en cuarentena tiene motivo, que las fechas de vencimiento Silver están preparadas y que ninguna fecha imputada se marca apta para un KPI de vencimiento observado. Revisa de nuevo el hash del Bronze antes de exportar.

El Silver es **analítico**: sirve para explorar rotación, saldos, merma y riesgo con marcas de procedencia. No es una certificación física del inventario ni de las fechas de vencimiento imputadas. Los productos sin correspondencia en Productos Silver de cobertura parcial no se descartan por ese solo motivo; su ausencia sigue visible en las marcas del diagnóstico. Para modelos predictivos, la vida útil debe recalcularse con datos disponibles en el conjunto de entrenamiento correspondiente, evitando usar información futura.

## Reproducción

Ejecutar las celdas en orden desde la raíz de `practicasNotebookColab` o en Colab tras configurar `RUTA_PROYECTO_DRIVE`. El notebook genera exactamente los dos CSV indicados. El tratamiento anterior en `proyecto-integrador/andinalog_inventory_tracking/notebook2/` corresponde al diagnóstico y catálogo antiguos; esta versión usa la salida didáctica de `01_diagnostico`.
