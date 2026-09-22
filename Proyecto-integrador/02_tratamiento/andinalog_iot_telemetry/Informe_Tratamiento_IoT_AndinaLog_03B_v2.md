# Informe del tratamiento IoT v2 — AndinaLog 03B

## Alcance

El Notebook 2 `S4_02_AndinaLog_IoT_Tratamiento_Didactico_v2.ipynb` lee **solo** `andinalog_iot_telemetry_didactico_v2_diagnosticado.csv`. Conserva los diez valores Bronze y sus banderas/motivos diagnósticos; añade los campos tratados, acciones, motivos y marcas de imputación. En las salidas, `en_cuarentena_diagnostico` nombra la decisión histórica y `en_cuarentena_final` la decisión después de tratar.

La hora local validada queda en `timestamp_bolivia_tratado`, sin columna UTC. `F` se convierte a Celsius y se marca en `temperatura_convertida_f_a_c`; una conversión no es imputación. El centinela `-999` se vuelve faltante analítico y solo se interpola entre dos observaciones cercanas, válidas y coherentes del mismo viaje/camión/producto. No se imputan identificadores, fechas ni banderas. Las reglas siguen visibles en el notebook.

## Tres salidas

| Salida en `02_tratamiento/andinalog_iot_telemetry/salidas/` | Filas | Uso |
|---|---:|---|
| `andinalog_iot_telemetry_didactico_v2_silver.csv` | 28.677 | Lecturas utilizables con original + tratado + evidencia de transformación. |
| `andinalog_iot_telemetry_didactico_v2_cuarentena_final.csv` | 243 | Lecturas no recuperables con motivo final. |
| `andinalog_iot_telemetry_didactico_v2_reporte_calidad_tratamiento.csv` | 10 métricas | Conciliación, recuperación y conteos de correcciones. |

**Conciliación:** 28.920 diagnosticadas = 28.677 Silver + 243 en cuarentena final. De las 554 filas inicialmente marcadas para cuarentena, **311 fueron recuperadas**. Ninguna fila inicialmente libre de cuarentena pasó a cuarentena final en esta ejecución.

## Transformaciones y procedencia

| Transformación | Resultado | Evidencia de salida |
|---|---:|---|
| Lecturas `F` diagnosticadas | 50 | 49 entran a Silver con °C tratado y `temperatura_convertida_f_a_c=True`; una queda en cuarentena final por fecha inválida, aunque se pudo calcular su conversión. |
| Identificadores de camión normalizados | 50 | `camion_id` original y `camion_id_tratado`; acción `NORMALIZAR_CAMION_ID`. |
| Temperaturas imputadas en Silver | 120 | `temperatura_imputada=True` y motivo de interpolación. No cuentan como excursión observada. |
| Humedades imputadas en Silver | 92 | `humedad_imputada=True` y motivo. |
| Lecturas Silver aptas para KPI térmico observado | 26.183 | Temperatura observada, umbral de producto observado y bandera actual coherente. |
| Posible incompatibilidad producto frío–camión `Seco` | 407 lecturas de 17 viajes | `posible_incompatibilidad_termica=True`, estado `REVISAR`; se conserva en Silver y en KPI cuando cumple la aptitud térmica. |

`K`, fechas imposibles, claves irrecuperables y magnitudes sin evidencia suficiente permanecen en cuarentena final. Los motivos concretos se guardan en `motivo_cuarentena_final`. La bandera original `desviacion_proximos_60min_flag` no se inventa ni se recalcula; por ahora sirve como objetivo exploratorio, no como etiqueta validada independientemente.

## Pruebas

El notebook comprueba la integridad de los campos de entrada, la partición Silver/cuarentena, la presencia de motivo en cuarentena, la unidad `C` y hora local válida en Silver, y que ninguna temperatura imputada se marque apta para KPI observado. El EDA integrado v2 comprueba la aptitud térmica fila por fila contra Productos Silver, los cruces con Flota y la marca de posible incompatibilidad. El contrato y la matriz de transformaciones describen las reglas para su revisión por el grupo.
