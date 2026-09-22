# Informe del Notebook 2: tratamiento didáctico de Productos — AndinaLog 03B

## Propósito

El notebook `S4_02_AndinaLog_Productos_Tratamiento_Didactico.ipynb` recibe el **diagnosticado completo** del Notebook 1 didáctico de Productos y crea un maestro Silver **analítico** con una fila por producto. Conserva las siete columnas Bronze, los pares `*_estado`/`*_motivo` y los resúmenes del diagnóstico; añade valores tratados, imputaciones, acciones y una decisión final por fila. No necesita un catálogo ni un motor externos.

La cuarentena diagnóstica ya está contenida en el diagnosticado y no se concatena como otra entrada. `en_cuarentena` refleja la etapa diagnóstica; `en_cuarentena_final` refleja la decisión después de tratar.

## Entradas y salidas

| Elemento | Ruta relativa a `practicasNotebookColab` | Función |
|---|---|---|
| Bronze de Productos | `datasets/AndinaLog_03B_Bronce/andinalog_productos.csv` | Fuente original y verificación de hash. |
| Diagnosticado didáctico | `proyecto-integrador/01_diagnostico/andinalog_productos/salidas/andinalog_productos_didactico_v1_diagnosticado.csv` | Las 63 filas con estados y motivos. |
| Bronze de Inventory Tracking | `datasets/AndinaLog_03B_Bronce/andinalog_inventory_tracking.csv` | Referencia auxiliar de vida útil **observada** por producto. |
| Notebook 2 | `proyecto-integrador/02_tratamiento/andinalog_productos/S4_02_AndinaLog_Productos_Tratamiento_Didactico.ipynb` | Reglas visibles y comprobaciones. |
| Silver | `proyecto-integrador/02_tratamiento/andinalog_productos/salidas/andinalog_productos_didactico_v1_silver.csv` | 60 productos únicos con atributos tratados e indicadores de inferencia. |
| Cuarentena final | `proyecto-integrador/02_tratamiento/andinalog_productos/salidas/andinalog_productos_didactico_v1_cuarentena_final.csv` | Tres copias posteriores excluidas del maestro. |

El notebook verifica versión, orden y 63 filas del diagnóstico, igualdad de las siete columnas Bronze, y SHA-256 del archivo de Productos. También registra `sha256_inventario_referencia` para identificar la fuente auxiliar de las inferencias.

## Regla de referencia: vida útil por producto

La vida útil se obtiene del **Bronze de inventario**, no del Silver de inventario, para usar únicamente fechas de ingreso y vencimiento realmente observadas. Se descartan copias exactas, claves de movimiento/lote con atributos contradictorios, fechas inválidas y duraciones no positivas. Un producto tiene una vida útil de referencia solo si existen **al menos 20 lotes válidos** y todos muestran la misma duración entre ingreso y vencimiento.

El cálculo es contextual al dataset sintético de AndinaLog; una vida útil uniforme observada no sustituye la ficha técnica del producto. Se conserva el número de lotes de respaldo en `lotes_respaldo_vida_util` y la duración en `vida_util_observada_dias`.

Los patrones usados para contrastar categorías son:

| Categoría | Objetivo térmico observado | Tolerancia observada | Vida útil observada |
|---|---:|---:|---:|
| `Fresco` | 4 °C | ±2 °C | 18 días |
| `Congelado` | −18 °C | ±2 °C | 180 días |
| `Seco` | 20 °C | ±5 °C | 365 días |

Son patrones consistentes en estos datos, **no requisitos universales** para todos los productos reales.

## Reglas de tratamiento

| Situación | Acción | Control |
|---|---|---|
| `producto_id` en minúsculas o con espacios exteriores | Crear `producto_id_tratado` en mayúsculas y sin espacios exteriores. | Exigir patrón `PROD-###` y verificar duplicados y conflictos después de preparar. |
| Categoría no permitida | Inferirla **solo si** objetivo, tolerancia y vida útil observada coinciden con un único patrón. | Marcar `categoria_imputada=True`, conservar la categoría Bronze y anotar método y motivo. |
| Temperatura objetivo faltante | Inferirla **solo si** categoría válida, tolerancia y vida útil observada coinciden con un patrón. | Marcar `temperatura_imputada=True`, conservar el original vacío y anotar método y motivo. |
| Copia idéntica después de preparar | Conservar la primera fila según `fila_bronze`; excluir la posterior del Silver. | Comparar ID, nombre, categoría, objetivo, tolerancia, precio y costo preparados. |
| Mismo ID tratado con atributos diferentes | Cuarentena de todas las variantes. | No seleccionar arbitrariamente una fila. |
| Categoría o umbral sin resolución, precio/costo no positivo | Cuarentena final. | No inventar atributos sin respaldo. |
| Precio menor que costo | Mantener la fila con `REVISAR_MARGEN`. | Puede ser una decisión comercial; no se altera el valor. |

El tratamiento anterior proponía corregir todo `conjelado` a `Congelado`. Esa regla no se aplica: habría creado contradicciones con los valores térmicos y la vida útil de los tres productos afectados.

## Imputaciones aplicadas

| Producto | Original | Evidencia observada | Valor tratado |
|---|---|---|---|
| `PROD-026` | Categoría `conjelado` | 4 ± 2 °C y 18 días en 104 lotes de respaldo. | `Fresco`; `categoria_imputada=True`. |
| `PROD-028` | Categoría `conjelado` | 20 ± 5 °C y 365 días en 97 lotes de respaldo. | `Seco`; `categoria_imputada=True`. |
| `PROD-036` | Categoría `conjelado` | 4 ± 2 °C y 18 días en 89 lotes de respaldo. | `Fresco`; `categoria_imputada=True`. |
| `PROD-018` | Objetivo térmico vacío | `Seco`, tolerancia ±5 °C y 365 días en 107 lotes de respaldo. | 20 °C; `temperatura_imputada=True`. |
| `PROD-049` | Objetivo térmico vacío | `Fresco`, tolerancia ±2 °C y 18 días en 92 lotes de respaldo. | 4 °C; `temperatura_imputada=True`. |

Los cinco productos se incluyen en Silver **con trazabilidad de estimación**. `apto_umbral_termico_observado=False` para ellos; el indicador no niega que la inferencia sea útil para análisis, sino que evita presentar sus atributos como parámetros verificados de una ficha de producto.

## Duplicados y unicidad

Se normalizaron seis IDs en minúsculas. Después de preparar los siete atributos, se detectaron **tres copias posteriores**:

| Fila Bronze excluida | ID preparado | Razón |
|---:|---|---|
| 61 | `PROD-010` | Copia exacta del primer registro. |
| 62 | `PROD-024` | `prod-024` se vuelve idéntico a `PROD-024` tras normalizar el ID. |
| 63 | `PROD-014` | Copia exacta del primer registro. |

Los primeros registros de esos productos permanecen en Silver. Los 60 `producto_id_tratado` de Silver son únicos.

## Resultados de la ejecución revisada

| Medida | Resultado |
|---|---:|
| Filas del diagnosticado | 63 |
| Filas en cuarentena diagnóstica | 13 |
| Filas Silver | 60 |
| Filas en cuarentena final | 3 |
| IDs normalizados | 6 |
| Categorías imputadas | 3 |
| Temperaturas objetivo imputadas | 2 |
| Copias excluidas | 3 |
| Productos Silver con umbral térmico totalmente observado | 55 |
| Productos Silver con algún atributo térmico inferido | 5 |

La conciliación es **63 = 60 Silver + 3 cuarentena final**. Ambos CSV conservan las columnas Bronze, el diagnóstico y la explicación del tratamiento.

## Uso correcto del Silver en IoT e inventario

Los campos **canónicos para cruces y cálculos nuevos** son `producto_id_tratado`, `categoria_logistica_tratada`, `temperatura_conservacion_requerida_c_tratada` y `tolerancia_temperatura_c_tratada`. Los nombres sin sufijo conservan el **Bronze original**: por ejemplo, `prod-008` sigue en `producto_id` y `conjelado` sigue en `categoria_logistica`. Un notebook que simplemente apunte a este Silver y siga usando los campos originales **no obtendrá los valores curados**.

Antes de reutilizar Productos Silver en los notebooks de IoT, inventario o EDA, los cruces deben emplear explícitamente los campos tratados y respetar `categoria_imputada`, `temperatura_imputada` y `apto_umbral_termico_observado`. Esto es especialmente importante para los umbrales que determinan una desviación térmica. El notebook no modifica automáticamente los análisis ya ejecutados con el Silver antiguo.

## Comprobaciones y límites

El notebook comprueba que Bronze y diagnóstico permanezcan intactos; que Silver y cuarentena final formen una partición de 63 filas; que el ID tratado sea único en Silver; que sus categorías, temperaturas y tolerancias estén utilizables; que toda cuarentena tenga motivo; y que ningún atributo imputado figure como umbral completamente observado. Verifica de nuevo los hashes de Productos e Inventario antes de exportar.

La inferencia usa patrones del dataset sintético. Para uso operativo de cadena de frío, los cinco productos inferidos deben contrastarse con fichas técnicas o datos maestros autorizados. La existencia de 60 productos en este Silver tampoco demuestra cobertura completa de todos los `producto_id` usados en inventario o IoT; las ausencias referenciales deben seguir tratándose como cobertura parcial.

## Reproducción

Ejecutar las celdas en orden desde la raíz de `practicasNotebookColab` o configurar `RUTA_PROYECTO_DRIVE` en Colab. El notebook genera exactamente Silver y cuarentena final. El tratamiento anterior situado en `proyecto-integrador/andinalog_productos/notebook2/` usa el catálogo y diagnóstico antiguos; esta versión usa la salida didáctica de `01_diagnostico`.
