# Informe B2S 04 - AndinaLog IoT Telemetry

## Objetivo, entidad y granularidad

Conversion auditada de lecturas IoT desde Bronze hacia un Silver compacto, una cuarentena investigable y
un reporte de calidad con una fila por regla.

- Entidad: lectura_iot_cabina.
- Granularidad: una fila por viaje_id y timestamp normalizados.
- Clave de lectura: ['viaje_id', 'timestamp'], unica en Silver.
- Entradas: datos/bronze/andinalog_iot_telemetry.csv, datos/silver/andinalog_wms_orders_silver.csv,
  datos/silver/andinalog_productos_silver.csv, datos/silver/andinalog_flota_silver.csv.
- Las fuentes Silver de apoyo se consultan solo para correspondencia y coherencia, y no se modifican.
- No se realizo ninguna imputacion ni se uso informacion futura.

## Perfil Bronze obtenido del archivo real

- Filas: 28920; columnas: 10.
- Columnas recibidas: ['timestamp', 'viaje_id', 'order_id', 'camion_id', 'producto_id', 'temperatura_cabina_c', 'temp_unit', 'humedad_cabina_pct', 'desviacion_termica_flag', 'desviacion_proximos_60min_flag'].
- Tipos recibidos: {'timestamp': 'str', 'viaje_id': 'str', 'order_id': 'str', 'camion_id': 'str', 'producto_id': 'str', 'temperatura_cabina_c': 'str', 'temp_unit': 'str', 'humedad_cabina_pct': 'str', 'desviacion_termica_flag': 'str', 'desviacion_proximos_60min_flag': 'str'}.
- Vacios por columna: {'timestamp': 0, 'viaje_id': 0, 'order_id': 0, 'camion_id': 0, 'producto_id': 0, 'temperatura_cabina_c': 80, 'temp_unit': 0, 'humedad_cabina_pct': 100, 'desviacion_termica_flag': 0, 'desviacion_proximos_60min_flag': 0}.
- Unidades de temperatura observadas: {'C': 28865, 'F': 50, 'K': 5}.
- Centinelas -999: {'temperatura_cabina_c': 120, 'humedad_cabina_pct': 0}.
- Formato de timestamp reconocido en 28920 filas; timestamps imposibles:
  15 con valores ['2026-02-31 09:15:00'].
- Lecturas por viaje: {24: 1086, 25: 108, 26: 6}.
- Cadencia de la serie normalizada y ordenada: {0.0: 120, 30.0: 27572, 60.0: 13} minutos.
- Inversiones del orden fisico del CSV: 113.
  Inversiones cronologicas tras ordenar por viaje_id y timestamp: 0.
- Duplicados: 230 filas exactas y 240 filas
  en 120 claves de lectura; de esas, 10
  filas tienen diferencias entre si dentro de su clave.
- Rangos numericos recibidos: {'temperatura_cabina_c': [-999.0, 291.22], 'humedad_cabina_pct': [-92.6, 100.0], 'desviacion_termica_flag': [0.0, 1.0], 'desviacion_proximos_60min_flag': [0.0, 1.0]}.
- sha256 de Bronze al inicio de la ejecucion: edb7afe2f7fb836e59fe605d30c88b3b5b13a6d8ab2ec0b37f206a14e58de6bf.

## Criterio de seleccion de columnas de Silver

Silver no exporta el dataframe de trabajo. `config` declara `columnas_silver`, `columnas_cuarentena` y
`columnas_reporte_calidad`, y el notebook falla si alguna columna declarada no se produce, si el orden
difiere o si hay columnas repetidas.

Silver queda con 18 columnas, todas con funcion verificable:

| columna_silver                 | funcion                                                                      |
|:-------------------------------|:-----------------------------------------------------------------------------|
| timestamp                      | marca de tiempo canonica en UTC                                              |
| viaje_id                       | entidad de la lectura                                                        |
| order_id                       | contexto de la orden                                                         |
| camion_id                      | contexto del camion                                                          |
| producto_id                    | contexto del producto                                                        |
| temperatura_cabina_c           | medida de temperatura en Celsius                                             |
| temp_unit                      | unidad canonica de la temperatura                                            |
| humedad_cabina_pct             | humedad relativa; vacia si estaba ausente en el valor recibido               |
| desviacion_termica_flag        | hecho de desviacion termica observado en el instante t                       |
| desviacion_proximos_60min_flag | etiqueta de desviacion en los proximos 60 minutos entregada por Bronze       |
| _fila_bronze                   | trazabilidad a la linea fisica de Bronze                                     |
| timestamp_original             | timestamp recibido; demuestra la conversion de zona horaria                  |
| temp_unit_original             | unidad recibida; demuestra el origen Fahrenheit de la conversion             |
| temperatura_cabina_c_original  | temperatura recibida; demuestra la conversion y la eliminacion de centinelas |
| motivos_transformacion         | motivos de transformacion aplicados a la fila                                |
| conteo_transformaciones        | conteo resumido de transformaciones aplicadas                                |
| banderas_informativas          | banderas informativas que no bloquean la fila                                |
| calidad_estado                 | estado de calidad; en Silver solo puede ser valida                           |

Columnas retiradas y justificacion:

| grupo                                         | columnas retiradas                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | justificacion                                                                                                                                             |
|:----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------|
| alias _tratado                                | timestamp_tratado, viaje_id_tratado, order_id_tratado, camion_id_tratado, producto_id_tratado, temp_unit_tratado, temperatura_cabina_c_tratado, humedad_cabina_pct_tratado, flags _tratado                                                                                                                                                                                                                                                                                                                                                                        | alias del valor canonico ya presente en la columna final                                                                                                  |
| copias _original que nunca cambian            | viaje_id_original, order_id_original, producto_id_original, humedad_cabina_pct_original, desviacion_termica_flag_original, desviacion_proximos_60min_flag_original, camion_id_original                                                                                                                                                                                                                                                                                                                                                                            | no demuestran ninguna transformacion; la normalizacion reversible de identificadores queda auditada por IOT-IDN-001 y es recuperable con _fila_bronze     |
| banderas bloqueantes siempre falsas en Silver | temperatura_cabina_c_centinela_detectado, temperatura_cabina_c_conversion_invalida, temperatura_unidad_no_esperada, temperatura_unidad_desconocida, temperatura_cabina_c_ausente, humedad_cabina_pct_fuera_rango, timestamp_conversion_invalida, timestamp_formato_reconocido, lectura_clave_duplicada, order_id_corresponde_wms_silver, producto_id_corresponde_silver, camion_id_corresponde_silver, producto_id_coherente_con_wms, camion_id_coherente_con_wms, desviacion_termica_calculable, desviacion_termica_calculada, desviacion_termica_flag_coherente | toda regla bloqueante debe declarar filas_silver igual a cero en el reporte de calidad, por lo que exportarlas en Silver no aporta informacion de consumo |
| columnas constantes                           | errores_bloqueantes, fue_imputada, imputacion_metodo, imputacion_motivo, conteo_imputaciones, calidad_motivo, motivos_imputacion, temperatura_convertida_fahrenheit                                                                                                                                                                                                                                                                                                                                                                                               | sin variacion ni funcion de consumo; la ausencia de imputaciones se demuestra con la regla IOT-IMP-001                                                    |
| helpers internos de calculo                   | t_viaje_id, t_order_id, t_camion_id, t_producto_id, t_temp_unit, t_temperatura_c, t_humedad_pct, t_flag_actual, t_flag_futuro, _ocurrencias, _clave_bronze, _corresponde_* y las marcas de cada regla                                                                                                                                                                                                                                                                                                                                                             | marcas de regla y valores intermedios: no son parte de ningun entregable                                                                                  |

Originales conservados solo cuando demuestran una transformacion real: `timestamp_original` difiere del
valor final en las 28448 filas por la conversion de Bolivia a UTC, y
`temperatura_cabina_c_original` difiere exactamente en las lecturas convertidas desde Fahrenheit
(49 filas).
Los identificadores, la humedad y las banderas no llevan original en Silver porque no cambian. La
posicion exacta en Bronze se recupera siempre con `_fila_bronze`.

Silver y cuarentena no exportan las banderas booleanas `fue_transformada` ni `fue_imputada` porque serian
constantes y no aportarian informacion. La equivalencia verificable es la siguiente:
`fue_transformada` equivale a `conteo_transformaciones > 0` y a `motivos_transformacion` no vacio, y
`fue_imputada` equivale a `motivos_imputacion` no vacio. En esta ejecucion hay
28448 de 28448 filas de Silver con
transformacion y 458 de
472 filas de cuarentena con transformacion. No se imputo ninguna fila:
`motivos_imputacion` esta vacio en las 472 de
472 filas de cuarentena, coherente con la regla IOT-IMP-001, y Silver no exporta esa
columna porque no contiene ninguna imputacion.

Motivos de transformacion en Silver: {'fecha_local_bolivia_convertida_utc': 28448, 'normalizacion_identificador:camion_id': 50, 'temperatura_fahrenheit_convertida_celsius': 49}.
Banderas informativas en Silver: {'IOT-REF-001': 4866, 'IOT-REF-002': 3109, 'IOT-REF-003': 1615, 'IOT-NUL-002': 98, 'IOT-SEQ-002': 13}.
Los tokens de `errores_bloqueantes` y de `banderas_informativas` son `regla_id` estables; su
significado esta en `descripcion_regla` del reporte de calidad.

## Valores canonicos de Silver

- `timestamp` es UTC con sufijo `+00:00`, entre 2026-08-01 04:10:00+00:00 y 2026-08-31 15:11:00+00:00.
- `temperatura_cabina_c` es Celsius, entre -21.63 y 29.69, sin centinelas.
- `temp_unit` es `C` en las 28448 filas.
- `calidad_estado` es `valida` en todas las filas porque Silver no admite errores bloqueantes.

## Cuarentena investigable

Cuarentena queda con 29 columnas:

| columna_cuarentena                      | funcion                                                                         |
|:----------------------------------------|:--------------------------------------------------------------------------------|
| _fila_bronze                            | posicion fisica de la fila en Bronze                                            |
| errores_bloqueantes                     | regla_id de cada error bloqueante, separados por pipe                           |
| calidad_motivo                          | descripcion legible del error bloqueante principal                              |
| calidad_estado                          | estado de calidad; en cuarentena siempre es cuarentena                          |
| clave_lectura_bronze                    | clave de lectura tal como se recibio en Bronze                                  |
| clave_lectura_normalizada               | clave de lectura con identificador normalizado y timestamp en UTC               |
| timestamp_original                      | timestamp recibido                                                              |
| viaje_id_original                       | viaje_id recibido                                                               |
| order_id_original                       | order_id recibido                                                               |
| camion_id_original                      | camion_id recibido                                                              |
| producto_id_original                    | producto_id recibido                                                            |
| temperatura_cabina_c_original           | temperatura recibida, centinelas incluidos                                      |
| temp_unit_original                      | unidad recibida                                                                 |
| humedad_cabina_pct_original             | humedad recibida                                                                |
| desviacion_termica_flag_original        | desviacion_termica_flag recibida                                                |
| desviacion_proximos_60min_flag_original | desviacion_proximos_60min_flag recibida                                         |
| timestamp_utc_normalizado               | instante al que se llega con la normalizacion; vacio si la fecha es imposible   |
| temperatura_c_normalizada               | temperatura ya normalizada a Celsius y sin centinela; vacia si no es corregible |
| lectura_clave_duplicada                 | control de duplicidad; habilita la accion posterior de recuperacion             |
| ocurrencias_clave_lectura               | numero de ocurrencias de la clave de lectura en Bronze                          |
| corresponde_wms_silver                  | control referencial: existe correspondencia en WMS Silver                       |
| corresponde_producto_silver             | control referencial: existe correspondencia en Productos Silver                 |
| corresponde_flota_silver                | control referencial: existe correspondencia en Flota Silver                     |
| motivos_transformacion                  | motivos de transformacion aplicados antes del enrutamiento                      |
| motivos_imputacion                      | motivos de imputacion; vacio porque la imputacion esta deshabilitada en config  |
| banderas_informativas                   | banderas informativas que no bloquean la fila, identificadas por regla_id       |
| conteo_transformaciones                 | conteo de transformaciones aplicadas                                            |
| conteo_errores_bloqueantes              | conteo de errores bloqueantes de la fila                                        |
| conteo_banderas_informativas            | conteo de banderas informativas de la fila                                      |

Los errores se identifican con `regla_id` dentro de `errores_bloqueantes` en lugar de una columna booleana
por regla, y lo mismo ocurre con `banderas_informativas`. Se conserva `lectura_clave_duplicada` porque
habilita la accion posterior de recuperacion y evita ambiguedad con `ocurrencias_clave_lectura`. El conteo
de banderas informativas siempre acompaña a los tokens y coincide con ellos fila a fila, verificado por un
control de cierre que recalcula los conjuntos de filas por regla informativa desde Bronze y desde las
fuentes Silver maestras.

- Motivos de cuarentena: {'IOT-CLA-001': 240, 'IOT-SEN-001': 120, 'IOT-NUL-001': 80, 'IOT-FEC-002': 15, 'IOT-RNG-001': 15, 'IOT-UNI-002': 5}.
- Banderas informativas en cuarentena: {'IOT-REF-001': 76, 'IOT-REF-002': 50, 'IOT-REF-003': 22, 'IOT-NUL-002': 2}; el conteo por fila coincide con el numero
  de tokens en las 472 filas.
- Filas con una sola regla: 469.
- Filas con dos reglas: 3; son lecturas con la temperatura ausente cuya
  clave tambien esta duplicada.
- Filas sin motivo: 0.
- Las activaciones se solapan: la suma de los motivos no es el numero de filas.

## Reglas, duplicados y secuencia temporal

- Fahrenheit convertido a Celsius con la formula exacta (F - 32) * 5 / 9:
  50 lecturas, de las cuales
  49
  llegan a Silver. El rango Fahrenheit recibido es [-2.31, 74.41] y el Celsius resultante es
  canonico.
- Kelvin no esperado operacionalmente: 5 lecturas a cuarentena, con rango
  recibido [254.28, 291.22].
- Centinelas -999: 120 en temperatura y
  0 en humedad. Ninguno es una medicion.
- Temperatura ausente: 80 lecturas a cuarentena.
- Humedad ausente: 100 lecturas, conservadas nulas y reportadas como
  informativa, sin imputar.
- Humedad fuera de 0-100: 15 lecturas a cuarentena, con valores
  ['-37.4', '-38.8', '-39.8', '-45.2', '-50.5', '-50.9', '-52.1', '-52.3', '-55.9', '-72.7', '-76.6', '-81.2', '-83.3', '-87.9', '-92.6'].
- Timestamp invalido: 15 lecturas a cuarentena.
- Duplicados: politica conservadora declarada en `config`. Las 120 claves duplicadas y sus
  240 ocurrencias van completas a cuarentena con el motivo
  `clave_lectura_duplicada_sin_criterio_de_desempate`. No se elige ganador porque no existe regla de negocio
  inequivoca. De esas 240 filas, 230 son duplicado exacto de su
  clave y 5 claves tienen ocurrencias con valores distintos entre si, en
  10 filas. Los duplicados exactos no se cuentan como un problema
  adicional independiente.
- Secuencia: `IOT-SEQ-001` se evalua despues de normalizar el timestamp y ordenar por `viaje_id` y
  `timestamp`, y arroja 0 incidencias. Las
  113 inversiones del orden fisico del CSV se documentan como
  caracteristica del archivo de entrada y no se marcan como error de las lecturas. `_fila_bronze`
  conserva la posicion fisica original.
- Cadencia: `IOT-SEQ-002` registra los intervalos mayores que
  30 minutos como huecos informativos
  (13 intervalos de 60 minutos). Ninguna fila va a cuarentena por el
  orden fisico del CSV ni por un intervalo de 60 minutos.
- No se aplican limites termicos inventados: una desviacion operacional valida no es error de calidad.
  Desviaciones termicas observadas: 951.

## Imputacion

No se imputo ninguna variable. `config` deja las imputaciones deshabilitadas y prohibe
['media', 'mediana', 'moda', 'ffill', 'bfill', 'informacion_futura']. Motivo declarado: no existe regla reproducible, inequivoca y compatible con el dominio para imputar temperatura ni humedad ausentes; la ausencia se conserva y se reporta.
La regla `IOT-IMP-001` del reporte se declara no aplicable porque no hay ninguna regla de imputacion en
`config` que aplicar: por eso no tiene denominador de evaluacion, sus conteos son cero y su accion
declarada es `no_imputada_por_config`, distinto de una regla evaluada sin incidencias. La ausencia se
conserva y se reporta, nunca se rellena.

## Integridad referencial

- Lecturas sin correspondencia en WMS Silver: 4942 en 205 order_id normalizados distintos.
- Lecturas sin correspondencia en Productos Silver: 3159 en 6 producto_id normalizados distintos.
- Lecturas sin correspondencia en Flota Silver: 1637 en 2 camion_id normalizados distintos. Los identificadores se comparan ya normalizados, de modo que
  distintas grafias del mismo camion no se cuentan como claves diferentes.
- Contradicciones con una orden WMS existente: 0 sobre
  23978 lecturas con orden coincidente.
- Coherencia de la desviacion termica: 0 incoherencias sobre
  25576 lecturas comparables.
- Criterio: una lectura valida no pasa a cuarentena porque una fuente auxiliar no tenga clave utilizable; solo es bloqueante la contradiccion con una referencia existente.

## Reporte de calidad

Archivo: `datos/quality/andinalog_iot_telemetry_reporte_calidad.csv`, una fila por regla y las columnas declaradas en
`columnas_reporte_calidad`.

- Reglas evaluadas: 22.
- Reglas con incidencias: ['IOT-CLA-001', 'IOT-FEC-002', 'IOT-IDN-001', 'IOT-NUL-001', 'IOT-NUL-002', 'IOT-REF-001', 'IOT-REF-002', 'IOT-REF-003', 'IOT-RNG-001', 'IOT-SEN-001', 'IOT-SEQ-002', 'IOT-UNI-001', 'IOT-UNI-002'].
- Estados presentes: ['aplicada_transformacion', 'envio_a_cuarentena', 'evaluada_sin_incidencias', 'informativa_sin_cuarentena', 'no_aplicable'].
- Reglas evaluadas sin incidencias: ['IOT-CNV-001', 'IOT-UNI-003', 'IOT-SEN-002', 'IOT-FMT-001', 'IOT-FEC-001', 'IOT-SEQ-001', 'IOT-REF-004', 'IOT-OPE-001'].
- Reglas no aplicables por configuracion: ['IOT-IMP-001'].

| regla_id    | columna_evaluada                                                                               | dimension_calidad      | severidad   |   filas_evaluadas |   filas_afectadas |   porcentaje_afectado | accion_aplicada                              |   filas_silver |   filas_cuarentena | estado_regla               |
|:------------|:-----------------------------------------------------------------------------------------------|:-----------------------|:------------|------------------:|------------------:|----------------------:|:---------------------------------------------|---------------:|-------------------:|:---------------------------|
| IOT-CNV-001 | temperatura_cabina_c;humedad_cabina_pct;desviacion_termica_flag;desviacion_proximos_60min_flag | exactitud              | alta        |             28920 |                 0 |              0        | sin_incidencias                              |              0 |                  0 | evaluada_sin_incidencias   |
| IOT-UNI-001 | temp_unit                                                                                      | exactitud              | informativa |             28920 |                50 |              0.001729 | conversion_exacta_fahrenheit_a_celsius       |             49 |                  1 | aplicada_transformacion    |
| IOT-UNI-002 | temp_unit                                                                                      | validez                | critica     |             28920 |                 5 |              0.000173 | envio_a_cuarentena                           |              0 |                  5 | envio_a_cuarentena         |
| IOT-UNI-003 | temp_unit                                                                                      | validez                | alta        |             28920 |                 0 |              0        | sin_incidencias                              |              0 |                  0 | evaluada_sin_incidencias   |
| IOT-SEN-001 | temperatura_cabina_c                                                                           | exactitud              | alta        |             28920 |               120 |              0.004149 | envio_a_cuarentena                           |              0 |                120 | envio_a_cuarentena         |
| IOT-SEN-002 | humedad_cabina_pct                                                                             | exactitud              | alta        |             28920 |                 0 |              0        | sin_incidencias                              |              0 |                  0 | evaluada_sin_incidencias   |
| IOT-NUL-001 | temperatura_cabina_c                                                                           | completitud            | alta        |             28920 |                80 |              0.002766 | envio_a_cuarentena                           |              0 |                 80 | envio_a_cuarentena         |
| IOT-NUL-002 | humedad_cabina_pct                                                                             | completitud            | informativa |             28920 |               100 |              0.003458 | sin_imputar_por_ausencia_de_regla_inequivoca |             98 |                  2 | informativa_sin_cuarentena |
| IOT-RNG-001 | humedad_cabina_pct                                                                             | validez                | alta        |             28920 |                15 |              0.000519 | envio_a_cuarentena                           |              0 |                 15 | envio_a_cuarentena         |
| IOT-FMT-001 | viaje_id;order_id;camion_id;producto_id                                                        | validez                | alta        |             28920 |                 0 |              0        | sin_incidencias                              |              0 |                  0 | evaluada_sin_incidencias   |
| IOT-IDN-001 | viaje_id;order_id;camion_id;producto_id                                                        | consistencia           | informativa |             28920 |                50 |              0.001729 | normalizacion_determinista_strip_upper       |             50 |                  0 | aplicada_transformacion    |
| IOT-FEC-001 | timestamp                                                                                      | validez                | alta        |             28920 |                 0 |              0        | sin_incidencias                              |              0 |                  0 | evaluada_sin_incidencias   |
| IOT-FEC-002 | timestamp                                                                                      | validez                | alta        |             28920 |                15 |              0.000519 | envio_a_cuarentena                           |              0 |                 15 | envio_a_cuarentena         |
| IOT-CLA-001 | viaje_id;timestamp                                                                             | unicidad               | alta        |             28920 |               240 |              0.008299 | envio_a_cuarentena_de_todas_las_ocurrencias  |              0 |                240 | envio_a_cuarentena         |
| IOT-SEQ-001 | timestamp                                                                                      | consistencia           | media       |             28905 |                 0 |              0        | sin_incidencias                              |              0 |                  0 | evaluada_sin_incidencias   |
| IOT-SEQ-002 | timestamp                                                                                      | consistencia           | informativa |             28905 |                13 |              0.00045  | informativa_hueco_de_cadencia                |             13 |                  0 | informativa_sin_cuarentena |
| IOT-REF-001 | order_id                                                                                       | integridad_referencial | informativa |             28920 |              4942 |              0.170885 | informativa_sin_enriquecimiento              |           4866 |                 76 | informativa_sin_cuarentena |
| IOT-REF-002 | producto_id                                                                                    | integridad_referencial | informativa |             28920 |              3159 |              0.109232 | informativa_sin_enriquecimiento              |           3109 |                 50 | informativa_sin_cuarentena |
| IOT-REF-003 | camion_id                                                                                      | integridad_referencial | informativa |             28920 |              1637 |              0.056604 | informativa_sin_enriquecimiento              |           1615 |                 22 | informativa_sin_cuarentena |
| IOT-REF-004 | producto_id;camion_id                                                                          | integridad_referencial | alta        |             23978 |                 0 |              0        | sin_incidencias                              |              0 |                  0 | evaluada_sin_incidencias   |
| IOT-OPE-001 | desviacion_termica_flag                                                                        | consistencia           | media       |             25576 |                 0 |              0        | sin_incidencias                              |              0 |                  0 | evaluada_sin_incidencias   |
| IOT-IMP-001 | todas                                                                                          | completitud            | informativa |                 0 |                 0 |              0        | no_imputada_por_config                       |              0 |                  0 | no_aplicable               |

Una fila puede activar varias reglas. La suma de `filas_afectadas`, `filas_silver` o `filas_cuarentena`
entre reglas no representa registros unicos. El reporte de calidad no participa en
`Bronze = Silver + cuarentena`; se valida regla por regla contra un recalculo independiente hecho desde
Bronze y los CSV exportados, y las 22 reglas coinciden.

## Enrutamiento y resultado

- Estados: {'valida': 28448, 'cuarentena': 472}.
- `calidad_estado` se calcula despues del tratamiento y de la imputacion: `imputar` no modifica ninguna
  fila y `asignar_calidad` decide el estado a partir de las reglas bloqueantes.
- Antes de exportar se comprueba que ninguna regla bloqueante este activa en las filas destinadas a
  Silver, y la comprobacion pasa.

## Resultado y conciliacion

- Conciliacion: Bronze 28920 = Silver 28448 + cuarentena 472.
- Las claves `_fila_bronze` de Silver y cuarentena son disjuntas y su union es exactamente el conjunto de
  lineas de Bronze.
- Silver tiene clave de lectura unica, timestamp en UTC, temperatura en Celsius, `temp_unit` igual a `C`
  y cero errores bloqueantes.
- Los valores recibidos de la cuarentena coinciden fila a fila con Bronze.
- Bronze no fue modificado: mismo sha256 al inicio y al final de la ejecucion.

## Archivos generados

- `notebooks/bronze_silver/04_iot_telemetry/B2S_04_AndinaLog_IoT_Telemetry.ipynb`
- `datos/silver/andinalog_iot_telemetry_silver.csv`
- `datos/quarantine/andinalog_iot_telemetry_quarantine.csv`
- `datos/quality/andinalog_iot_telemetry_reporte_calidad.csv`
- `informes/bronze_silver/Informe_B2S_04_IoT_Telemetry.md`

No leido, no modificado y no entregable: `datos/silver/andinalog_iot_telemetry_silver - Copy.csv`. Es una
copia obsoleta de una version anterior de Silver, queda fuera de entradas, busquedas automaticas,
conciliaciones y controles de existencia. Se decidira por separado si se elimina o se mueve fuera de
`datos/silver` despues de la auditoria.

## Limitaciones

- No hay contrato que sostente limites termicos, por lo que no se aplican y no se puede afirmar que una
  temperatura alta o baja sea un error.
- La desviacion termica solo se puede verificar cuando el producto tiene temperatura de conservacion y
  tolerancia en Productos Silver; en las demas lecturas no es evaluable y no se cuenta como incoherencia.
- La humedad ausente y la humedad fuera de rango reciben tratamientos distintos: la primera se conserva
  porque el sensor no entrego lectura, la segunda se rechaza porque el valor recibido es imposible.
- El orden fisico del CSV de Bronze no es una secuencia cronologica y no se usa como tal.
- La etiqueta `desviacion_proximos_60min_flag` se entrega tal como llega de Bronze; esta etapa no la
  recalcula ni la valida contra ventanas temporales.
- El modelo predictivo posterior debe derivar sus ventanas temporales por viaje y no puede usar ninguna
  lectura posterior al instante de prediccion.

## Correcciones aplicadas por la auditoria

La auditoria independiente de esta entrega confirmo un hallazgo importante y cinco hallazgos menores. Este
Build los corrige sin cambiar ninguna decision metodologica aprobada.

- H-1 IMPORTANTE, cerrado: la cuarentena no exportaba `banderas_informativas` aunque si exportaba su
  conteo, de modo que 78 filas
  tenian un motivo informativo no legible. Se adiciono la columna a `columnas_cuarentena` y a
  `proyectar_cuarentena`; la cuarentena queda con 29 columnas y sus
  banderas informativas son {'IOT-REF-001': 76, 'IOT-REF-002': 50, 'IOT-REF-003': 22, 'IOT-NUL-002': 2}. El control de cierre verifica que la columna
  existe, que todos sus tokens son `regla_id` declarados, que el numero de tokens coincide con
  `conteo_banderas_informativas` en las 472 filas y que los conjuntos de filas por
  regla informativa recalculados desde Bronze y desde las fuentes maestras coinciden con los del archivo.
- H-2 MENOR, cerrado: se documenta en la seccion de seleccion de columnas la equivalencia entre
  `fue_transformada` y `conteo_transformaciones` mas `motivos_transformacion`, y entre `fue_imputada` y
  `motivos_imputacion`, con los conteos de esta ejecucion.
- H-3 MENOR, sin cambio por decision aprobada: `calidad_motivo` no se exporta en Silver porque seria
  constante; la evidencia de cero errores bloqueantes queda en el reporte y en la conciliacion.
- H-4 MENOR, cerrado: la evidencia de `IOT-CLA-001` declara ahora las 120 claves, las
  240 filas, los 230 duplicados exactos y las
  5 claves con diferencias, en 10 filas.
- H-5 MENOR, cerrado: `IOT-IMP-001` queda con estado `no_aplicable`, denominador cero y accion
  `no_imputada_por_config`.
- H-6 MENOR, cerrado: se corrigieron los anglicismos en los textos de evidencia del reporte de calidad.

## Contradicciones respecto del plan

- hay 80 temperaturas vacias y 120 centinelas -999.0; el plan habia indicado ausencia de ambos.
- hay 100 humedades vacias, no 951.
- hay 15 fechas imposibles aunque todas cumplen el patron textual.
- hay 230 filas duplicadas exactas y 240 filas en 120 claves de lectura duplicadas.
- la frecuencia regular observada es 30 minutos, no 20-21.
- no se aplican limites termicos -50/50 o -10/40 porque no existe contrato que los sustente.
- las faltas referenciales se mantienen informativas, no bloqueantes, por no ser errores intrinsecos de sensor.
- las inversiones de tiempo del orden fisico del CSV no son un error de la serie de lecturas.

## Reproducibilidad

- Fecha de ejecucion UTC: 2026-09-26T07:00:05.461037+00:00.
- Python: 3.14.6.
- pandas: 3.0.5.
- numpy: 2.5.3.
- Semilla: None (el pipeline es deterministico y no usa aleatoriedad; la semilla no aplica).
- Rutas de entrada: datos/bronze/andinalog_iot_telemetry.csv, datos/silver/andinalog_wms_orders_silver.csv,
  datos/silver/andinalog_productos_silver.csv, datos/silver/andinalog_flota_silver.csv.
- Rutas de salida: datos/silver/andinalog_iot_telemetry_silver.csv, datos/quarantine/andinalog_iot_telemetry_quarantine.csv,
  datos/quality/andinalog_iot_telemetry_reporte_calidad.csv, informes/bronze_silver/Informe_B2S_04_IoT_Telemetry.md.
- Zona inicial de los timestamps sin zona: America/La_Paz; zona canonica de
  Silver: UTC.
- Conversion de Fahrenheit: (F - 32) * 5 / 9.
- Cadencia esperada: 30 minutos.
- Conteos de esta ejecucion: Bronze 28920, Silver 28448,
  cuarentena 472, reglas de calidad 22.
- sha256 de Bronze: edb7afe2f7fb836e59fe605d30c88b3b5b13a6d8ab2ec0b37f206a14e58de6bf.
- Los controles finales se aplican sobre los tres CSV persistidos, no solo sobre los dataframes en
  memoria, y el informe se escribe al final de esa misma ejecucion.
