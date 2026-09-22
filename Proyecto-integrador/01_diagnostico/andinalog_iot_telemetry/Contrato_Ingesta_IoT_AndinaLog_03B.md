# Contrato de ingesta IoT — AndinaLog 03B

**Responsable:** Grupo 06, Operaciones, Planificación y Datos. **Versión del contrato:** 2.0. **Fecha:** 2026-09-22.

## Fuente y límites conocidos

| Aspecto | Acuerdo para este proyecto |
|---|---|
| Fuente | `datasets/AndinaLog_03B_Bronce/andinalog_iot_telemetry.csv`, conjunto sintético del caso 03B. |
| Granularidad | Una lectura candidata por (`viaje_id`, `timestamp`). Las copias y claves contradictorias se señalan antes de analizar. |
| Frecuencia | Se observan muchas lecturas separadas por 30 minutos; **no** hay una frecuencia contractual del dispositivo confirmada. El EDA comprueba el intervalo real antes de calcular rezagos. |
| Formato | CSV con diez columnas Bronze. Los identificadores y banderas son texto; las magnitudes se parsean como números decimales. |
| Hora | Todo `timestamp` sin zona representa hora de Bolivia (`America/La_Paz`). Se conserva el original y se prepara `timestamp_bolivia_tratado` en la misma hora local. No se deriva UTC en esta versión. |
| Semántica térmica | `temperatura_cabina_c` se interpreta en este ejercicio como lectura del compartimento monitoreado; el significado físico exacto del sensor requiere confirmación. La unidad real de cada fila está en `temp_unit`. |
| Unidad operacional | `C` es la única unidad conforme a la ingesta. `F` pasa a cuarentena diagnóstica y se convierte a °C en tratamiento; una fila recuperable puede entrar en Silver. `K` no se convierte automáticamente. |
| Centinela | `-999` no es temperatura. Se marca en diagnóstico y solo se estima en tratamiento con vecinos válidos y motivo; jamás se toma como observación real. |

## Campos y reglas de ingreso

| Campo Bronze | Significado y formato esperado | En cuarentena diagnóstica cuando… | Tratamiento permitido |
|---|---|---|---|
| `timestamp` | Fecha y hora de Bolivia `AAAA-MM-DD HH:MM:SS`. | Falta, es imposible, tiene formato inválido o participa en clave de lectura duplicada/conflictiva. | Validar y conservar hora local; no inventar fecha. |
| `viaje_id` | Viaje, patrón `VIA-` + cinco dígitos. | Falta, patrón inválido o clave de lectura duplicada/conflictiva. | No imputar identificador. |
| `order_id` | Orden, patrón `ORD-AAAA-NNNNN`. | Falta o patrón inválido. | No imputar identificador. |
| `camion_id` | Camión, patrón `CAM-##`. | Falta o patrón inválido. | Normalizar espacios/minúsculas si resulta un ID inequívoco; Flota Silver aporta contexto. |
| `producto_id` | Producto, patrón `PROD-###`. | Falta o patrón inválido. | No inventar ID; Productos Silver aporta objetivo, tolerancia y categoría. |
| `temperatura_cabina_c` | Magnitud numérica cuya unidad se lee de `temp_unit`. | Falta, no es numérica o vale `-999`. | Convertir F si procede; interpolar faltantes interiores solo con evidencia temporal restringida; marcar `temperatura_imputada`. |
| `temp_unit` | Unidad recibida. Ingreso conforme: `C`. | Falta, es `F`, `K` u otra unidad. | `F`→°C con `(F−32)×5/9`; `K` y unidades desconocidas no se convierten automáticamente. |
| `humedad_cabina_pct` | Humedad relativa numérica, 0–100 %. | Falta, no es numérica o está fuera del rango. | Interpolación restringida si hay vecinos válidos; marcar `humedad_imputada`. |
| `desviacion_termica_flag` | Bandera actual `0`/`1`. | Falta o tiene otro valor. | No inventar bandera; comprobar coherencia con umbral observado cuando sea posible. |
| `desviacion_proximos_60min_flag` | Etiqueta futura `0`/`1` provista por la fuente. | Falta o tiene otro valor. | No imputar. Su origen temporal aún no se ha reconstruido; se usa solo como objetivo exploratorio. |

La ausencia de correspondencia en un maestro, o la imposibilidad de comprobar una regla contextual, puede dejar un **motivo informativo** con bandera de cuarentena `False`. Por eso `False` significa “esta columna no obliga a cuarentena”, no “todas las comprobaciones pasaron”. Las combinaciones de producto frío con camión registrado `Seco` se marcan para revisión en tratamiento, sin cuarentena automática.

## Contrato entre etapas

- **Diagnóstico:** conserva las diez columnas originales; añade `fila_bronze`, `*_en_cuarentena`, `*_motivo`, `en_cuarentena` y `zona_horaria_origen`. Produce diagnosticado completo, su subconjunto de cuarentena y reporte de calidad.
- **Tratamiento:** lee solo el diagnosticado completo. Silver conserva originales y evidencia diagnóstica junto con valores tratados, acciones, motivos y banderas de conversión/imputación. Produce Silver, cuarentena final y reporte de calidad.
- **Conservación:** filas diagnosticadas = filas Silver + filas en cuarentena final. La cuarentena diagnóstica ya está incluida en el diagnosticado y no se suma de nuevo.
- **KPI térmico observado:** excluye temperatura imputada y umbral de producto inferido; comprueba coherencia de la bandera actual. Una conversión física de F a °C no equivale a imputación.

La versión del contrato y la fecha se documentan aquí y en la matriz de transformaciones; no se repiten en cada fila del CSV.
