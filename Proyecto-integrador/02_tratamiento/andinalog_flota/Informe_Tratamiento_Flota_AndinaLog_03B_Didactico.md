# Informe del Notebook 2: tratamiento didáctico de Flota — AndinaLog 03B

## Propósito

El notebook `S4_02_AndinaLog_Flota_Tratamiento_Didactico.ipynb` prepara el maestro de camiones de AndinaLog, grupo 06, subcaso 03B, a partir del **CSV diagnosticado completo** del Notebook 1 didáctico. Su finalidad es obtener un Silver con una sola fila utilizable por camión y conservar una cuarentena final explicada para los registros excluidos o irrecuperables.

El diagnóstico y el tratamiento tienen funciones distintas: el primero marca problemas sin alterar datos; el segundo aplica correcciones justificables y decide el destino final. `en_cuarentena` conserva la decisión del diagnóstico y `en_cuarentena_final` registra la del tratamiento. No se concatena la cuarentena inicial con el diagnosticado, pues ya está incluida en él.

Esta versión contiene las reglas dentro del notebook. No requiere catálogo externo ni motor de tratamiento.

## Fuentes y archivos generados

| Elemento | Ruta relativa a `practicasNotebookColab` | Función |
|---|---|---|
| Bronze original | `datasets/AndinaLog_03B_Bronce/andinalog_flota.csv` | Referencia para verificar integridad y hash. |
| Diagnóstico de entrada | `proyecto-integrador/01_diagnostico/andinalog_flota/salidas/andinalog_flota_didactico_v1_diagnosticado.csv` | Las 32 filas con estados y motivos. |
| Notebook 2 | `proyecto-integrador/02_tratamiento/andinalog_flota/S4_02_AndinaLog_Flota_Tratamiento_Didactico.ipynb` | Código y explicación del tratamiento. |
| Silver | `proyecto-integrador/02_tratamiento/andinalog_flota/salidas/andinalog_flota_didactico_v1_silver.csv` | Camiones únicos y utilizables. |
| Cuarentena final | `proyecto-integrador/02_tratamiento/andinalog_flota/salidas/andinalog_flota_didactico_v1_cuarentena_final.csv` | Filas excluidas o que siguen siendo inválidas, con motivo. |

Los dos CSV de salida conservan las columnas Bronze originales y las marcas del diagnóstico. Las columnas tratadas están separadas de las originales para poder comparar ambas etapas.

## Contrato de entrada

Antes de tratar, el notebook comprueba:

1. La presencia de las cuatro columnas Bronze (`camion_id`, `centro_distribucion_base`, `capacidad_kg`, `tipo_camion`), sus pares `*_estado`/`*_motivo` y las columnas de trazabilidad del diagnóstico.
2. Que `fila_bronze` sea única y siga el orden de las filas Bronze.
3. Que las cuatro columnas originales del diagnóstico coincidan exactamente con el archivo Bronze actual.
4. Que `sha256_bronze` coincida con el hash del archivo de origen y que `version_diagnostico` sea la versión didáctica esperada.
5. Que `en_cuarentena` contenga únicamente `True` o `False` como texto al leerse del CSV.

Si alguno de estos puntos falla, el tratamiento se detiene para evitar mezclar versiones o procesar una entrada distinta de la diagnosticada.

## Reglas de tratamiento

| Situación | Decisión aplicada | Razón |
|---|---|---|
| ID con espacios exteriores o minúsculas | Crear `camion_id_tratado` quitando espacios y pasando a mayúsculas, solo si el resultado cumple `CAM-##` y no presenta conflicto de atributos. | Es una corrección determinista de escritura, no un nuevo identificador inventado. |
| Copia exacta posterior | Conservar la primera aparición según `fila_bronze` y enviar la copia a cuarentena final. | Un maestro debe contar cada camión una sola vez; la copia conserva su evidencia. |
| Mismo ID normalizado con centro, capacidad o tipo contradictorio | Enviar las variantes a cuarentena final. | No hay fuente autorizada para elegir automáticamente cuál atributo es verdadero. |
| Centro fuera de los cinco permitidos | Cuarentena final. | Los centros confirmados para este caso son Cochabamba, La Paz, Santa Cruz, Oruro y Tarija. |
| Tipo fuera de `Seco` y `Refrigerado` | Cuarentena final. | Son las categorías operativas aceptadas en este ejercicio. |
| Capacidad faltante, no numérica o no positiva | Cuarentena final. | No representa una capacidad de carga utilizable. |
| Capacidad positiva menor que 750 kg | Permanece en Silver si lo demás es válido, pero se marca `capacidad_revisar_ficha=True`. | El umbral es orientativo y requiere contrastar la ficha técnica; no es un mínimo legal o universal. |

**No hay imputación** de capacidad, centro, tipo o ID. Son atributos de un maestro: una mediana o el dato de otro camión no demostrarían las características del vehículo real. Si falta un atributo, debe recuperarse de una fuente autorizada.

## Trazabilidad por fila

El tratamiento añade:

| Columna | Significado |
|---|---|
| `camion_id_tratado` | Identificador después de la normalización permitida. |
| `camion_id_normalizado` | `True` cuando el ID tratado difiere del original. |
| `centro_distribucion_base_tratado`, `tipo_camion_tratado` | Valores del maestro separados del original; no se alteran en esta versión. |
| `capacidad_kg_tratada` | Capacidad convertida a número cuando es posible. |
| `acciones_tratamiento` | Acciones como `NORMALIZAR_CAMION_ID` y `EXCLUIR_COPIA`. |
| `motivos_tratamiento` | Explicación de las acciones aplicadas. |
| `capacidad_revisar_ficha` | Alerta para una capacidad positiva inferior a 750 kg. |
| `motivo_cuarentena_final` | Motivo concreto por el que una fila no entra en Silver. |
| `en_cuarentena_final`, `decision_tratamiento` | Decisión final (`CUARENTENA` o `SILVER`). |
| `version_tratamiento` | Versión de estas reglas didácticas. |

Las columnas del diagnóstico, incluidos `*_estado`, `*_motivo`, `motivos_fila` y `en_cuarentena`, permanecen disponibles. Así puede verse que las filas `cam-20` y `cam-30` estaban en cuarentena diagnóstica y pasaron a Silver después de una corrección verificable.

## Resultados de la ejecución revisada

| Medida | Resultado |
|---|---:|
| Filas del diagnosticado | 32 |
| Filas en cuarentena diagnóstica | 4 |
| IDs normalizados sin conflicto | 2 |
| Copias exactas posteriores excluidas | 2 |
| Filas Silver | 30 |
| Filas en cuarentena final | 2 |
| Filas con imputación | 0 |

Detalle de los cuatro casos tratados:

| `fila_bronze` | Original | Decisión | Explicación |
|---:|---|---|---|
| 20 | `cam-20` | Silver como `CAM-20` | Normalización a mayúsculas sin conflicto de atributos. |
| 30 | `cam-30` | Silver como `CAM-30` | Normalización a mayúsculas sin conflicto de atributos. |
| 31 | `CAM-01` | Cuarentena final | Copia exacta posterior; se conserva la primera aparición en Silver. |
| 32 | `CAM-27` | Cuarentena final | Copia exacta posterior; se conserva la primera aparición en Silver. |

La conciliación es **32 filas de entrada = 30 Silver + 2 cuarentena final**. Los 30 `camion_id_tratado` de Silver son únicos.

## Comprobaciones de salida y límites

El notebook valida que las columnas de entrada quedaron intactas, que Silver y cuarentena final particionan todas las filas, que cada fila en cuarentena tiene motivo y que los camiones Silver tienen ID válido, centro y tipo permitidos y capacidad positiva. Antes de exportar comprueba otra vez que el Bronze no cambió.

El Silver es apto para cruces por `camion_id_tratado`, pero los demás conjuntos pueden conservar grafías antiguas. En los cruces debe aplicarse una política de clave coherente y visible; no se deben emparejar silenciosamente registros distintos. La cifra de capacidad expresa el valor declarado por la fuente, no una verificación de homologación o ficha técnica. La validez de `Seco`/`Refrigerado` y de los cinco centros pertenece al alcance del caso 03B y debe revisarse si cambia el catálogo operativo.

## Reproducción

Ejecutar las celdas en orden desde la raíz de `practicasNotebookColab`, o en Colab tras configurar `RUTA_PROYECTO_DRIVE`. El notebook lee la salida didáctica del diagnóstico y escribe exactamente los dos CSV indicados. El tratamiento anterior situado en `proyecto-integrador/andinalog_flota/notebook2/` usa otro diagnóstico y un catálogo de reglas pendiente; no es la entrada de esta versión.
