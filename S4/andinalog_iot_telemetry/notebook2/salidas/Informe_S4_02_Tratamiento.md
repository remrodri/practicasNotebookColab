# Informe de tratamiento de telemetría IoT

**Fuente Bronze SHA-256:** `c5f78ed802f8455dfc8eac91295954c38a159029e77b8ed748875fe2d8cf7467`
**Referencia de flota SHA-256:** `5c02eb8ef591c7f98846b8f547f41383467b41e7768bddb4031bb43d1b812bec`
**Versión:** `GIAD-M3-S4-IOT-tratamiento-v2`

## Resultado del lote

Se conservaron las 28,920 filas. La cuarentena pasó de 450 a 445 filas; 5 salieron después de resolver todos sus motivos. Se registraron 6 problemas resueltos, 330 pendientes y 120 copias excluidas de la vista utilizable.

## Tratamientos aplicados

- Se convirtieron 50 temperaturas de Fahrenheit a Celsius con `(F − 32) × 5/9`, conservando el valor original. Estas lecturas no estaban en cuarentena únicamente por la unidad.
- Se convirtieron 5 temperaturas de kelvin a Celsius con `K − 273,15`, según la confirmación del usuario. 4 filas salieron de cuarentena; las demás conservaron un motivo adicional.
- No se imputaron temperaturas ni humedades. No se corrigieron fechas imposibles ni humedades negativas por suposición.

## Duplicados y selección canónica

Se revisaron 120 pares de lecturas con la misma clave `viaje_id + timestamp`: 114 pares idénticos, 1 con una diferencia de mayúsculas en `camion_id` confirmada por la referencia de flota y 5 con una lectura más completa sin valores no vacíos contradictorios.
Se eligió una lectura canónica por par y se conservaron 120 copias como `EXCLUIDO_COMO_COPIA` en el archivo completo y en cuarentena. Una lectura canónica antes marcada como duplicada salió de cuarentena. Una lectura incompleta anterior recibió una acción adicional de copia sustituida. Ninguna copia se borró ni se contó como una nueva medición utilizable.
Cualquier par con valores no vacíos contradictorios, sin una lectura claramente más completa o sin un código de camión verificable permanece pendiente. La elección de cada par y su justificación constan en `andinalog_iot_telemetry_decisiones_duplicados.csv`.

## Motivos que permanecen en cuarentena

| Columna | Código | Motivos finales |
|---|---|---:|
| humedad_cabina_pct | FALTANTE | 100 |
| humedad_cabina_pct | FUERA_RANGO | 15 |
| temperatura_cabina_c | FALTANTE | 80 |
| temperatura_cabina_c | VALOR_CENTINELA | 120 |
| timestamp | FECHA_INVALIDA | 15 |
| viaje_id+timestamp | DUPLICADO | 120 |

La cantidad de motivos finales puede superar las filas en cuarentena porque una fila puede presentar más de un problema. Los duplicados excluidos figuran como motivos finales para impedir su uso como nuevas lecturas. Cada intento y su resultado constan en el CSV de acciones; el CSV tratado mantiene los valores originales y el estado inicial y final.

## Reglas y límites de esta ejecución

- `TEMP_C_CONSERVAR`: **APROBADA**. Tratamiento: Conservar el valor en Celsius en columna preparada. Validación: Valor numérico y unidad C. Acuerdo: C ya representa Celsius; conservar el valor original
- `TEMP_F_A_C`: **APROBADA**. Tratamiento: Convertir F a C con (F-32)*5/9. Validación: Valor numérico y unidad F. Acuerdo: Conversión de F a Celsius confirmada por el usuario el 2026-09-15
- `TEMP_K_A_C`: **APROBADA**. Tratamiento: Convertir K a C con K-273.15. Validación: K confirmado como kelvin; valor numérico no negativo. Acuerdo: K confirmado como kelvin por el usuario el 2026-09-15
- `DUPLICADO_IDENTICO`: **APROBADA**. Tratamiento: Elegir primera lectura canónica y excluir copia exacta. Validación: Misma clave y diez columnas originales idénticas. Acuerdo: Regla de duplicados aprobada por el usuario el 2026-09-15
- `DUPLICADO_MAYUSCULAS`: **APROBADA**. Tratamiento: Elegir primera lectura y excluir copia con camion_id equivalente. Validación: Solo cambia mayúscula/minúscula de camion_id; código normalizado en flota. Acuerdo: Regla aprobada por el usuario; CAM-12 existe en la referencia de flota
- `DUPLICADO_COMPLEMENTARIO`: **APROBADA**. Tratamiento: Elegir lectura más completa y excluir la incompleta. Validación: Todos los valores no vacíos coinciden y una lectura tiene más campos completos. Acuerdo: Regla de duplicados aprobada por el usuario el 2026-09-15
- `FALTANTE_TEMPERATURA`: **PENDIENTE**. Tratamiento: Sin imputación automática. Validación: Fuente recuperable o método aprobado. Acuerdo: pendiente.
- `FALTANTE_HUMEDAD`: **PENDIENTE**. Tratamiento: Sin imputación automática. Validación: Fuente recuperable o método aprobado. Acuerdo: pendiente.
- `HUMEDAD_FUERA_RANGO`: **PENDIENTE**. Tratamiento: Conservar en cuarentena. Validación: Lectura original verificable. Acuerdo: pendiente.
- `FECHA_INVALIDA`: **PENDIENTE**. Tratamiento: Conservar en cuarentena. Validación: Timestamp real recuperado de fuente autorizada. Acuerdo: pendiente.
- `DUPLICADO_CONFLICTIVO`: **PENDIENTE**. Tratamiento: Conservar ambas lecturas en cuarentena. Validación: Valores no vacíos contradictorios o selección ambigua; requiere fuente autoritativa. Acuerdo: pendiente.

Una fila permaneció en cuarentena cuando no había una regla aprobada, faltaba evidencia o quedaba otro motivo sin resolver. No se forzó ninguna liberación.
