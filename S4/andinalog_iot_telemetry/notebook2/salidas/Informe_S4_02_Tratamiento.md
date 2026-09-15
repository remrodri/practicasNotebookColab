# Informe de tratamiento de telemetría IoT

**Fuente Bronze SHA-256:** `c5f78ed802f8455dfc8eac91295954c38a159029e77b8ed748875fe2d8cf7467`
**Versión:** `GIAD-M3-S4-IOT-tratamiento-v1`

## Resultado del lote

Se conservaron las 28,920 filas. La cuarentena pasó de 330 a 326 filas; 4 salieron después de resolver todos sus motivos. Se registraron 5 problemas resueltos, 330 pendientes y 0 copias excluidas de la vista utilizable.

## Tratamientos aplicados

- Se convirtieron 50 temperaturas de Fahrenheit a Celsius con `(F − 32) × 5/9`, conservando el valor original. Estas lecturas no estaban en cuarentena únicamente por la unidad.
- Se convirtieron 5 temperaturas de kelvin a Celsius con `K − 273,15`, según la confirmación del usuario. Cuatro filas salieron de cuarentena; la quinta conserva un motivo adicional de humedad faltante.
- No se imputaron temperaturas ni humedades. No se corrigieron fechas imposibles ni humedades negativas por suposición.
- La regla para copias duplicadas continúa pendiente de acuerdo; no se liberó ni descartó ninguna por ese motivo.

## Problemas que permanecen

| Columna | Código | Hallazgos pendientes |
|---|---|---:|
| humedad_cabina_pct | FALTANTE | 100 |
| humedad_cabina_pct | FUERA_RANGO | 15 |
| temperatura_cabina_c | FALTANTE | 80 |
| timestamp | FECHA_INVALIDA | 15 |
| viaje_id+timestamp | DUPLICADO | 120 |

La cantidad de hallazgos pendientes puede superar las filas en cuarentena porque una fila puede presentar más de un problema. Cada intento y su resultado figuran en el CSV de acciones; el CSV tratado mantiene los valores originales y el estado inicial y final.

## Reglas y límites de esta ejecución

- `TEMP_C_CONSERVAR`: **APROBADA**. C ya representa Celsius; conservar el valor original
- `TEMP_F_A_C`: **APROBADA**. Conversión de F a Celsius confirmada por el usuario el 2026-09-15
- `TEMP_K_A_C`: **APROBADA**. K confirmado como kelvin por el usuario el 2026-09-15
- `DUPLICADO_IDENTICO`: **PENDIENTE**. Sin acuerdo documentado.
- `FALTANTE_TEMPERATURA`: **PENDIENTE**. Sin acuerdo documentado.
- `FALTANTE_HUMEDAD`: **PENDIENTE**. Sin acuerdo documentado.
- `HUMEDAD_FUERA_RANGO`: **PENDIENTE**. Sin acuerdo documentado.
- `FECHA_INVALIDA`: **PENDIENTE**. Sin acuerdo documentado.
- `DUPLICADO_DIFERENTE`: **PENDIENTE**. Sin acuerdo documentado.

Una fila permaneció en cuarentena cuando no había una regla aprobada, faltaba evidencia o quedaba otro motivo sin resolver. No se forzó ninguna liberación.
