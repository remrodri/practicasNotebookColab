# Informe del diagnóstico IoT v2 — AndinaLog 03B

## Alcance

El Notebook 1 `S4_01_AndinaLog_IoT_Diagnostico_Didactico_v2.ipynb` revisa las 28.920 lecturas Bronze sin modificar ninguna de sus diez columnas. Aplica el [contrato de ingesta](Contrato_Ingesta_IoT_AndinaLog_03B.md): hora sin zona = Bolivia, unidad conforme de ingreso = `C`, `-999` = centinela y `K` = unidad no operacional.

Por cada variable Bronze se escriben `*_en_cuarentena` y `*_motivo`. La bandera de fila `en_cuarentena` es verdadera si alguna bandera de columna lo es. Un motivo puede explicar una advertencia contextual con bandera `False`; esta no implica que todas las reglas pudieron evaluarse. El CSV no contiene `columnas_con_problemas`, estados de severidad, motivos repetidos por fila, versión ni hash por registro. El notebook comprueba la integridad Bronze mediante SHA-256 internamente.

## Tres salidas

| Salida en `01_diagnostico/andinalog_iot_telemetry/salidas/` | Filas | Uso |
|---|---:|---|
| `andinalog_iot_telemetry_didactico_v2_diagnosticado.csv` | 28.920 | Entrada única al tratamiento; contiene todas las filas. |
| `andinalog_iot_telemetry_didactico_v2_cuarentena_diagnostico.csv` | 554 | Subconjunto del diagnosticado para revisar o tratar; **no** es una segunda entrada. |
| `andinalog_iot_telemetry_didactico_v2_reporte_calidad_diagnostico.csv` | 9 métricas | Conteos del lote y de incidencias seleccionadas. |

La salida diagnosticada tiene 33 columnas: `fila_bronze`, diez Bronze, dos campos por cada Bronze, `en_cuarentena` y `zona_horaria_origen`.

## Hallazgos y decisiones

| Hallazgo | Conteo | Decisión diagnóstica |
|---|---:|---|
| Unidad Fahrenheit | 50 | `temp_unit_en_cuarentena=True`; la conversión se decide en Notebook 2. |
| Unidad Kelvin | 5 | Cuarentena diagnóstica; no hay conversión operacional automática. |
| Temperatura `-999` | 120 | `temperatura_cabina_c_en_cuarentena=True`; no es medición. |
| Fecha inválida | 15 | Cuarentena diagnóstica; no se inventa una hora. |
| Copia exacta posterior | 115 | Cuarentena diagnóstica; no se cuenta dos veces. |
| Filas en clave conflictiva | 10 | Revisión de las variantes; no se elige una lectura arbitraria. |

Los conteos de hallazgos pueden solaparse. Por ello **no se suman** para obtener las 554 filas de cuarentena.

El diagnóstico utiliza los Productos y Flota Silver didácticos actuales como contexto. Una ausencia en un maestro o una comprobación imposible puede dejar un motivo con bandera `False`: por sí sola no prueba que el ID sea erróneo. La comprobación producto frío–camión `Seco` se realiza posteriormente en tratamiento.

## Pruebas y límites

El notebook verifica que las diez columnas Bronze permanecen idénticas, que `fila_bronze` es única, que cada fila de cuarentena tiene un motivo en alguna columna marcada y que el tamaño de la cuarentena coincide con el OR de las banderas por campo. La marca futura de desviación se valida como `0`/`1`, pero no se reconstruye su origen temporal.

Las 554 filas de cuarentena diagnóstica no son necesariamente pérdidas: el tratamiento puede recuperar unidades F o centinelas con evidencia suficiente. La hora original se conserva como hora de Bolivia; no se deriva UTC.
