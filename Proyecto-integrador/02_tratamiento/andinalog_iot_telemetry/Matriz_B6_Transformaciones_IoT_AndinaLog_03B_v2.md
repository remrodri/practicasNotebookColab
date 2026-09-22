# Matriz B6 de transformaciones IoT — AndinaLog 03B

**Responsable:** Grupo 06. **Versión:** IoT v2. **Fecha:** 2026-09-22. Esta matriz corresponde a las nueve filas IoT completadas en la plantilla Excel del docente. Los tres ejemplos industriales de la plantilla no son reglas de AndinaLog.

| Variable | Entrada | Regla / acción | Salida + bandera | Prueba |
|---|---|---|---|---|
| `timestamp` | Texto sin zona | Parsear como hora de Bolivia; fecha imposible a cuarentena. | `timestamp_bolivia_tratado`, `timestamp_en_cuarentena`. | Hora tratada válida en Silver; 15 fechas inválidas en diagnóstico. |
| `camion_id` | `CAM-##` o grafía recuperable | Normalizar espacios/minúsculas; no inventar identificador. | `camion_id_tratado`, acción `NORMALIZAR_CAMION_ID`. | 50 IDs normalizados; patrón válido en Silver. |
| `temperatura_cabina_c` | `-999`, vacío o cifra | Centinela a faltante; interpolar solo entre vecinos observados válidos. | `temperatura_cabina_c_tratada`, `temperatura_imputada`. | 120 temperaturas imputadas en Silver; ninguna apta para KPI observado. |
| `temp_unit` | `C`, `F`, `K` u otra | Solo C cumple ingesta; F se pone en cuarentena diagnóstica y se convierte; K no se convierte automáticamente. | `temp_unit_tratado=C`, `temperatura_convertida_f_a_c`. | 50 F diagnosticadas; 49 convertidas en Silver y una en cuarentena final por fecha inválida. |
| `humedad_cabina_pct` | Vacío, inválido o 0–100 % | Validar rango; interpolar solo con vecinos válidos. | `humedad_cabina_pct_tratada`, `humedad_imputada`. | 92 imputadas; ninguna humedad Silver queda faltante. |
| (`viaje_id`, `timestamp`) | Clave repetida | Excluir copia posterior; cuarentena de variantes en conflicto. | `en_cuarentena_final`, `motivo_cuarentena_final`. | 115 copias; 10 filas en claves conflictivas. |
| Banderas térmicas | `0`, `1` u otro | Validar dominio binario; no imputar etiquetas. | Banderas originales, `*_en_cuarentena`, `*_motivo`. | Solo 0/1 en Silver; Bronze conservado. |
| Umbral de producto | Producto + temperatura | Cruzar Productos Silver actual; excluir umbral inferido de KPI observado. | `umbral_producto_evaluable`, `apta_kpi_termico`. | 26.183 lecturas aptas; EDA coincide fila por fila. |
| Producto / camión | Fresco o Congelado + Seco | Marcar posible incompatibilidad, sin cuarentena automática. | `posible_incompatibilidad_termica`, motivo. | 407 lecturas de 17 viajes; cruce validado con maestros. |

El diagnóstico no modifica Bronze. Silver conserva los valores recibidos junto con los tratados, acciones y motivos. Los conteos provienen de la ejecución IoT v2 y deben recalcularse si cambia alguna fuente. La fecha y la versión se documentan en esta matriz y en la plantilla Excel, no por fila de telemetría.
