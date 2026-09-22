# Informe del Notebook 2: tratamiento IoT de AndinaLog 03B

## Propósito y relación con el diagnóstico

El notebook `S4_02_AndinaLog_IoT_Tratamiento_Didactico.ipynb` recibe el **CSV diagnosticado completo** del Notebook 1. Usa sus estados y motivos como evidencia, pero toma una nueva decisión por fila después de aplicar correcciones y, cuando hay evidencia suficiente, imputaciones. No lee la cuarentena del Notebook 1 como entrada adicional porque esas filas ya están dentro del diagnosticado.

Esta versión didáctica mantiene todas las columnas originales y las columnas `*_estado`/`*_motivo` del diagnóstico. Agrega valores tratados, acciones, motivos y una cuarentena **final**. Las reglas y parámetros están dentro del notebook; no hay catálogo externo.

## Entradas y salidas

| Elemento | Ubicación dentro del repositorio | Función |
|---|---|---|
| Entrada | `proyecto-integrador/01_diagnostico/andinalog_iot_telemetry/salidas/andinalog_iot_telemetry_didactico_v1_diagnosticado.csv` | Las 28.920 filas diagnosticadas. |
| Productos Silver | `proyecto-integrador/02_tratamiento/andinalog_productos/salidas/andinalog_productos_didactico_v1_silver.csv` | Objetivo, tolerancia y origen observado/inferido del umbral. Entrada requerida para la aptitud térmica. |
| Flota Silver | `proyecto-integrador/02_tratamiento/andinalog_flota/salidas/andinalog_flota_didactico_v1_silver.csv` | Tipo de camión para alerta relacional de negocio. Entrada requerida para esta comprobación. |
| Tratado | `proyecto-integrador/02_tratamiento/andinalog_iot_telemetry/salidas/andinalog_iot_telemetry_didactico_v1_tratado.csv` | Filas utilizables después del tratamiento. |
| Cuarentena final | `proyecto-integrador/02_tratamiento/andinalog_iot_telemetry/salidas/andinalog_iot_telemetry_didactico_v1_cuarentena_final.csv` | Filas que aún tienen un impedimento crítico. |

Las rutas de los dos maestros y de las dos salidas corresponden a la estructura actual de `02_tratamiento`. Si falta un maestro, el notebook detiene la ejecución para evitar publicar una aptitud calculada con datos obsoletos.

## Reglas de tratamiento

| Dato o situación | Decisión | Evidencia que se conserva |
|---|---|---|
| `camion_id` con minúsculas o espacios, recuperable inequívocamente | Normalizar a mayúsculas en `camion_id_tratado`. | `camion_id` original, `NORMALIZAR_CAMION_ID` y motivo. |
| `temp_unit=F` | Convertir la cifra a Celsius con `(F − 32) × 5/9`. | Cifra y unidad originales, `temperatura_cabina_c_tratada`, `temp_unit_tratado=C`, `CONVERTIR_F_A_C`. |
| `temp_unit=C` | Conservar la cifra numérica como Celsius. | Original y valor tratado. |
| `temp_unit=K` u otra unidad no reconocida | Cuarentena final; no aplicar una conversión operativa no aprobada. | Unidad original y motivo de cuarentena. |
| Temperatura `-999` | Tratar como faltante, nunca como medición. | Original `-999`, `CENTINELA_A_FALTANTE` y eventual imputación. |
| Humedad fuera de 0–100 % | Tratar como faltante antes de evaluar imputación. | Valor original y valor tratado vacío si no es recuperable. |
| Timestamp válido sin zona | Interpretar como hora `America/La_Paz` y derivar `timestamp_utc`. | Timestamp local original y UTC nuevo. |
| Fecha imposible | Cuarentena final. | Fecha original y motivo. |
| Copia exacta de una lectura | Excluir la copia; conservar la primera lectura. | `EXCLUIR_COPIA` y motivo. |
| Misma clave (`viaje_id`, `timestamp`) con datos diferentes | Cuarentena de las lecturas en conflicto. | `CUARENTENA_CONFLICTO` y motivo. |
| Identificador o bandera irrecuperable | Cuarentena final; no inventar claves ni etiquetas. | Original y motivo. |

La ausencia de correspondencia en un maestro no provoca por sí sola cuarentena final: la evaluación relacional queda en `NO_EVALUABLE`. El notebook exige que ambos archivos maestros actuales existan y que sus claves tratadas sean únicas.

## Imputación: cuándo se aplica y cómo se identifica

Solo se considera una lectura faltante **interior** entre dos observaciones originales del mismo `viaje_id`, `camion_id_tratado` y `producto_id`. Se exige fecha válida y orden temporal estricto, vecinos separados como máximo 60 minutos, ausencia de duplicados/conflictos en los vecinos y las tres filas con banderas térmicas `0`. No se usan valores previamente imputados como vecinos.

| Variable | Método | Restricción adicional | Marca de salida |
|---|---|---|---|
| Temperatura faltante o `-999` | Interpolación lineal según la distancia temporal entre vecinos. | Diferencia entre vecinos ≤ 2 °C; unidad de la fila `C` y unidades vecinas `C` o `F`. | `temperatura_imputada=True`; acción `IMPUTAR_TEMPERATURA`. |
| Humedad faltante o inválida | Interpolación lineal según la distancia temporal entre vecinos. | Diferencia entre vecinos ≤ 20 puntos porcentuales. | `humedad_imputada=True`; acción `IMPUTAR_HUMEDAD`. |

Los límites de 60 minutos, 2 °C y 20 puntos son **parámetros conservadores del ejercicio**, no umbrales oficiales de AndinaLog ni especificaciones verificadas del sensor. Deben contrastarse con la frecuencia y el comportamiento real del dispositivo antes de producción. No se imputan timestamps, claves, unidades desconocidas ni banderas.

`acciones_tratamiento` y `motivos_tratamiento` documentan las decisiones **por fila**; si se imputan temperatura y humedad en una misma fila, sus acciones aparecen juntas. Los indicadores `temperatura_imputada` y `humedad_imputada` permiten distinguir cada variable. Los valores originales permanecen en las columnas Bronze y los resultados se guardan en `temperatura_cabina_c_tratada` y `humedad_cabina_pct_tratada`.

Una temperatura imputada no equivale a una excursión observada. Por eso `apta_kpi_termico=False` y `apta_objetivo_60min=False` cuando se imputa temperatura. La bandera de desviación original no se recalcula ni se reemplaza.

## Decisión final y aptitud analítica

Una fila queda en `decision_tratamiento=TRATADO` si dispone de fecha, identificadores, banderas, unidad operativa, temperatura y humedad válidas después de las reglas, y no es copia o conflicto. En caso contrario queda en `CUARENTENA`, con explicación en `motivo_cuarentena_final`. Por ello una fila que estaba en la cuarentena del diagnóstico puede salir como tratada si el problema se resolvió de forma justificable.

`apta_kpi_termico` requiere una lectura tratada, no imputada, un **umbral completamente observado** en Productos Silver y coherencia entre el cálculo de excursión y la bandera actual. El CSV IoT anterior guardaba 23.563 aptas porque consultaba una ruta antigua con cobertura parcial; con el Productos Silver didáctico actual son **26.183**. El EDA verifica fila por fila que la marca guardada coincida con su recálculo. `apta_objetivo_60min` conserva su sentido de elegibilidad básica sin temperatura imputada; la validación temporal de la etiqueta futura sigue siendo una tarea analítica aparte.

### Alerta de compatibilidad producto–camión

Se cruzan `producto_id` con Productos Silver por `producto_id_tratado` y `camion_id_tratado` con Flota Silver por la misma clave tratada. Se añade `categoria_producto_maestro`, `tipo_camion_maestro`, `compatibilidad_tipo_camion_estado`, `posible_incompatibilidad_termica` y `compatibilidad_tipo_camion_motivo` sin alterar los campos originales.

| Estado | Condición | Decisión |
|---|---|---|
| `REVISAR` | Categoría **observada** `Fresco` o `Congelado` y camión registrado `Seco`. | Marcar posible incompatibilidad para verificación operativa. Se mantiene en tratado y en KPI térmico si satisface las reglas de observación. |
| `SIN_ALERTA` | Categoría observada y tipo de camión conocido, sin la combinación anterior. | Conservar; no significa certificación de cadena de frío. |
| `NO_EVALUABLE` | Falta categoría observada o tipo de camión conocido. | Conservar sin afirmar compatibilidad. |

La tabla Flota solo registra `Seco` o `Refrigerado`; no documenta equipo térmico adicional. Por ello `REVISAR` no confirma un error, no cambia el tipo de camión y **no genera cuarentena automática**. Las desviaciones térmicas de esos viajes permanecen visibles en el análisis.

## Resultados de la ejecución revisada

| Medida | Resultado |
|---|---:|
| Filas diagnosticadas de entrada | 28.920 |
| Filas tratadas | 28.677 |
| Filas en cuarentena final | 243 |
| Columnas en cada CSV de tratamiento | 60 |
| Fahrenheit convertidos a Celsius | 50 |
| Identificadores de camión normalizados | 50 |
| Temperaturas imputadas entre las filas tratadas | 120 |
| Humedades imputadas entre las filas tratadas | 92 |
| Filas tratadas aptas para KPI térmico | 26.183 |
| Lecturas tratadas con posible incompatibilidad | 407 |
| Viajes con posible incompatibilidad | 17 (9 Congelado, 8 Fresco) |
| Lecturas tratadas con compatibilidad no evaluable | 1.484 |
| Filas tratadas con `apta_objetivo_60min=True` | 28.557 |

La conservación de filas se comprobó: **28.920 = 28.677 + 243**. La cuarentena del diagnóstico tenía 505 filas; la final tiene 243. Esta diferencia refleja recuperación mediante tratamiento y exclusión definitiva de los casos no recuperables, no una modificación del CSV Bronze.

Entre los motivos exclusivos de cuarentena final observados están 115 copias exactas, 77 temperaturas no recuperables, 21 humedades no recuperables, 15 fechas imposibles y 5 claves en conflicto. Hay además filas con más de un motivo, incluidos los 5 registros Kelvin.

## Validaciones y límites

El notebook comprueba que las columnas de entrada se conservaron, `fila_bronze` sigue siendo única, tratado y cuarentena particionan todas las filas, cada fila en cuarentena tiene motivo, ninguna temperatura imputada se marca apta para KPI térmico o etiqueta futura, y las filas tratadas tienen hora UTC y magnitudes utilizables. También comprueba que una lectura apta tiene umbral observado y que `REVISAR` coincide con la marca de posible incompatibilidad. El EDA confirma la concordancia de `apta_kpi_termico` fila por fila con los maestros actuales.

El tratamiento conserva la trazabilidad, pero no verifica con una fuente externa si el sensor midió correctamente. Los umbrales de imputación y la interpretación de `temperatura_cabina_c` como medición del compartimento monitoreado son decisiones de este ejercicio. Antes de usar las salidas para una alerta operativa o un modelo predictivo se debe verificar la documentación del sensor, la definición exacta de las banderas y la cobertura de los maestros de productos, flota y viajes.
