# Informe del Notebook 1: diagnóstico didáctico de Productos — AndinaLog 03B

## Propósito

El notebook `S4_01_AndinaLog_Productos_Diagnostico_Didactico.ipynb` revisa el maestro Bronze de Productos del grupo 06, subcaso 03B. Este maestro aporta la categoría logística a inventario y la temperatura objetivo y tolerancia a los análisis de telemetría IoT. Una categoría o un umbral erróneo puede alterar la interpretación de una excursión térmica, por lo que el diagnóstico combina reglas técnicas con coherencia de negocio.

El diagnóstico **detecta, clasifica y explica**. No normaliza IDs, no corrige categorías, no imputa temperaturas ni elimina copias. Conserva intactas las siete columnas Bronze. Las reglas están dentro del notebook, sin catálogo ni motor externo.

## Entrada y salidas

| Elemento | Ruta relativa a `practicasNotebookColab` | Contenido |
|---|---|---|
| Bronze | `datasets/AndinaLog_03B_Bronce/andinalog_productos.csv` | 63 filas y siete columnas originales. |
| Notebook | `proyecto-integrador/01_diagnostico/andinalog_productos/S4_01_AndinaLog_Productos_Diagnostico_Didactico.ipynb` | Reglas y comprobaciones. |
| Diagnosticado | `proyecto-integrador/01_diagnostico/andinalog_productos/salidas/andinalog_productos_didactico_v1_diagnosticado.csv` | Las 63 filas con estados, motivos y resumen. |
| Cuarentena diagnóstica | `proyecto-integrador/01_diagnostico/andinalog_productos/salidas/andinalog_productos_didactico_v1_cuarentena.csv` | Subconjunto de filas con algún estado `CRITICO`. |

La cuarentena está **incluida** en el diagnosticado; no se deben concatenar ambos archivos para el tratamiento.

## Diccionario de negocio y reglas por columna

| Campo Bronze | Significado | Regla aplicada |
|---|---|---|
| `producto_id` | Clave del producto para cruces con inventario, viajes e IoT. | Obligatorio; patrón exacto `PROD-###`. Se comprueban copias exactas posteriores, IDs repetidos con atributos distintos y coincidencias que surgirían al normalizar mayúsculas y espacios. |
| `nombre_producto` | Nombre descriptivo del producto. | Obligatorio. No se exige que el texto contenga el mismo número del ID: los nombres son genéricos y esa convención visual no demuestra una regla de negocio. |
| `categoria_logistica` | Clasificación usada para resumir riesgo y necesidades térmicas. | Obligatoria; solo `Fresco`, `Congelado` o `Seco` en este caso. Una categoría desconocida es crítica. |
| `temperatura_conservacion_requerida_c` | Temperatura objetivo del producto, en °C. | Obligatoria y numérica. Se compara con el patrón térmico observado para la categoría si esta es reconocida; una temperatura negativa puede ser válida para congelados. |
| `tolerancia_temperatura_c` | Desviación tolerada respecto del objetivo, en °C. | Obligatoria, numérica y mayor que cero. Se contrasta con la tolerancia observada para la categoría cuando es evaluable. |
| `precio_unitario_bob` | Precio declarado por unidad, en bolivianos. | Obligatorio, numérico y mayor que cero. Si es menor que el costo, se marca `REVISAR` para entender la decisión comercial. |
| `costo_unitario_bob` | Costo declarado por unidad, en bolivianos. | Obligatorio, numérico y mayor que cero. |

El archivo no define la presentación física de la unidad de producto. El diagnóstico no supone que el precio o costo sea por caja, pieza o kilogramo.

## Coherencia térmica del dominio

Los productos con categoría válida y datos completos muestran estas combinaciones en el dataset:

| Categoría | Objetivo observado | Tolerancia observada |
|---|---:|---:|
| `Fresco` | 4 °C | ±2 °C |
| `Congelado` | −18 °C | ±2 °C |
| `Seco` | 20 °C | ±5 °C |

El notebook usa esa relación como **comprobación contextual del dataset**, no como especificación universal. Una diferencia en un registro con categoría válida se marcaría `REVISAR` para verificar la ficha del producto; no se reemplaza el umbral automáticamente. Si la categoría es desconocida, la comparación del objetivo y tolerancia es `NO_EVALUABLE` y se conserva el motivo.

Tres registros tienen categoría `conjelado`. No se interpreta automáticamente como `Congelado`: `PROD-026` y `PROD-036` tienen **4 ± 2 °C**, patrón observado de `Fresco`; `PROD-028` tiene **20 ± 5 °C**, patrón observado de `Seco`. Los tres quedan en cuarentena diagnóstica por categoría no permitida. El tratamiento deberá documentar cómo determina la categoría real antes de liberar estos productos para cruces con IoT.

## Unicidad e integridad de clave

`producto_id` es clave del maestro. El diagnóstico distingue:

1. **Copia exacta posterior:** misma fila en los siete campos Bronze; se marca crítica la copia, conservando el primer registro.
2. **ID exacto con atributos contradictorios:** se marcan críticas todas sus variantes; no se elige una por orden de aparición.
3. **Colisión al normalizar:** un ID con otra grafía puede coincidir con un ID existente al quitar espacios y pasar a mayúsculas. Si los atributos coinciden, se señala la equivalencia para revisión; si difieren, se marca conflicto crítico. El diagnóstico no fusiona registros.

En el archivo actual hay dos copias exactas posteriores (`PROD-010` y `PROD-014`) y un ID `prod-024` que coincide con `PROD-024` al normalizar. La fila original `PROD-024` queda con advertencia por esa futura coincidencia; `prod-024` también tiene un error crítico de formato. Estas filas no se corrigen en Notebook 1.

## Estados, severidad y trazabilidad

Cada columna Bronze tiene `*_estado` y `*_motivo`. Los estados son `OK`, `NO_EVALUABLE`, `REVISAR` y `CRITICO`. `en_cuarentena=True` si algún campo es `CRITICO`. Una advertencia `REVISAR` no envía por sí sola la fila a cuarentena.

El diagnosticado contiene **29 columnas**: siete originales, `fila_bronze`, 14 columnas de estado/motivo y siete columnas de resumen y trazabilidad: `cantidad_columnas_con_problemas`, `en_cuarentena`, `severidad_maxima`, `columnas_con_problemas`, `motivos_fila`, `version_diagnostico` y `sha256_bronze`. El hash identifica la versión exacta del Bronze. Un campo puede acumular varios motivos; su estado conserva la mayor severidad.

## Resultados de la ejecución revisada

| Indicador | Resultado |
|---|---:|
| Filas Bronze y diagnosticadas | 63 |
| Filas sin problemas detectados | 49 |
| Filas con al menos un hallazgo | 14 |
| Filas con severidad máxima `REVISAR` | 1 |
| Filas con severidad máxima `CRITICO` y en cuarentena | 13 |
| IDs con formato inválido, por minúsculas | 6 |
| Copias exactas posteriores | 2 |
| Categorías `conjelado` no permitidas | 3 |
| Temperaturas objetivo faltantes | 2 |
| Filas con colisión potencial de ID al normalizar | 2 |

Los conteos **se solapan**: `prod-024` forma parte de los seis IDs con formato inválido y de la pareja que coincide al normalizar. El diagnóstico no detectó precios o costos no positivos ni precios inferiores al costo en este Bronze.

## Validaciones y límites

El notebook comprueba el esquema de siete columnas, que no cambió ninguno de sus valores, que se conservaron las 63 filas, que `fila_bronze` es única, que toda fila en cuarentena tiene motivo y que el hash del Bronze sigue siendo el de la entrada. Exporta exactamente los dos CSV indicados.

La relación de categoría, objetivo y tolerancia se obtuvo de los registros consistentes de este dataset. La tolerancia válida para un producto real puede requerir una ficha técnica distinta de ese patrón. Los productos en cuarentena no deben usarse como dimensión térmica confirmada de IoT hasta resolver sus categorías o temperaturas. El tratamiento podrá normalizar claves y excluir copias cuando no haya conflicto, pero deberá conservar las decisiones y motivos por fila.
