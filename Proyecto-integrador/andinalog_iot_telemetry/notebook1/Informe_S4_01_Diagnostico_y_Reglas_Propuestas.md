# Informe previo a la curación de telemetría IoT — AndinaLog 03B

**Fecha:** 15 de septiembre de 2026
**Fuente:** `datasets/AndinaLog_03B_Bronce/andinalog_iot_telemetry.csv`
**Diagnóstico:** `S4/andinalog_iot_telemetry/notebook1/salidas/andinalog_iot_telemetry_diagnosticado.csv`
**Estado:** propuesta para revisión; no autoriza todavía conversiones ni liberación de cuarentena.

## Objetivo y alcance

Este informe justifica qué datos podrían estandarizarse o tratarse en un segundo notebook y qué evidencia falta para hacerlo. El primer notebook solo marcó anomalías: no modificó las diez columnas originales. El segundo deberá conservar el valor original, registrar el valor preparado, la regla aplicada y los motivos de cuarentena antes y después del tratamiento.

## Evidencia del lote

El CSV Bronze contiene **28.920 filas**. El diagnóstico conserva las 28.920; **330** están marcadas `en_cuarentena=True` y **28.590** no presentan los motivos definidos. Los conteos por motivo no suman 330 porque una fila puede tener varios problemas.

| Motivo detectado | Filas | Evidencia principal |
|---|---:|---|
| Clave `viaje_id + timestamp` repetida | 120 | 114 copias idénticas en las columnas originales; 6 pares con alguna diferencia |
| Temperatura faltante | 80 | Campo vacío, sin evidencia suficiente para sustituirlo automáticamente |
| Humedad faltante | 100 | Campo vacío; una de estas filas también usa unidad K |
| Timestamp inválido | 15 | Todas registran `2026-02-31 09:15:00` |
| Humedad fuera del rango 0–100% | 15 | Todas son negativas, entre −80,5% y −38,2% |
| Unidad de temperatura no reconocida por la regla inicial | 5 | Todas indican `K`, con valores 255,34–294,01 |

No aparecieron temperatura o humedad no numéricas, flags diferentes de 0/1 ni identificadores vacíos en este lote. Hay **50** temperaturas con unidad `F` y **28.865** con `C`; no quedaron en cuarentena solo por su unidad. Las cinco `K` sí quedaron pendientes.

## Reglas propuestas para el segundo notebook

| Caso | Regla propuesta y justificación | Condición para retirar de cuarentena |
|---|---|---|
| Temperatura en `C` | Conservar el número en una nueva columna Celsius. La unidad ya expresa la magnitud requerida; el valor original debe mantenerse. | Si no tiene otros motivos pendientes. |
| Temperatura en `F` | Convertir a Celsius con `(F − 32) × 5/9` y guardar `temperatura_convertida_f=True`. Es una conversión de unidad definida y reversible; no requiere imputación. | Esas 50 filas ya están fuera de cuarentena por unidad; otros motivos, si existieran, se evalúan aparte. |
| Temperatura en `K` | **Propuesta condicionada:** si el responsable confirma que `K` significa kelvin, convertir con `K − 273,15` y dejar la bandera correspondiente. Los valores observados son compatibles con esa interpretación, pero no la prueban. | Confirmación del significado y de la procedencia de la unidad; la fila con humedad faltante seguirá en cuarentena hasta resolver también ese motivo. |
| Diferencia solo de mayúsculas en `camion_id` | Normalizar el identificador en una columna preparada para comparar claves; por ejemplo, `cam-12` y `CAM-12`. Mantener el texto recibido. | Confirmar que ambos códigos designan el mismo camión. Por sí sola, esta normalización no resuelve la lectura repetida. |
| Lectura duplicada idéntica | Elegir una lectura canónica por clave y marcar la copia como duplicado resuelto en el historial. Las 114 copias idénticas no aportan otra medición. | Confirmar que la clave `viaje_id + timestamp` identifica una sola lectura; conservar ambas filas en el archivo de auditoría y excluir la copia de la vista utilizable, sin borrarla. |
| Lectura duplicada con diferencias | Comparar los seis pares con el registro de origen. Uno difiere solo en la escritura de `camion_id`; cuatro tienen la copia posterior con temperatura o humedad vacía; en un par la primera está vacía y la posterior contiene temperatura. Elegir la lectura canónica por integridad y procedencia, no únicamente por orden de aparición. | Solo después de aprobar una regla de precedencia o disponer de fuente autoritativa. La fila descartada sigue identificada como copia/sustituida, sin fingir que es una nueva lectura válida. |
| Temperatura o humedad faltante | Buscar una medición original verificable o considerar una estimación temporal **solo si** hay lecturas cercanas del mismo viaje, con continuidad temporal y una regla aprobada. Señalar `fue_imputada` y método; el valor estimado no equivale a una observación. | El dato queda resuelto únicamente si el método y sus límites fueron aprobados. Si una variable es crítica para seguridad o predicción, puede permanecer en cuarentena aunque se estime. |
| Humedad negativa | Mantener en cuarentena. Una humedad relativa negativa no es físicamente válida. No aplicar valor absoluto, recorte a cero ni sustitución por mediana sin evidencia. | Corregir solo con lectura original o fuente confiable que explique el error de captura. |
| Fecha `2026-02-31` | Mantener en cuarentena. El día 31 de febrero es imposible; cambiarlo por una fecha vecina sería una suposición. | Reemplazar únicamente con timestamp recuperado de logs, dispositivo u otra fuente autorizada; documentar la zona horaria. |

## Decisiones pendientes antes de programar la curación

1. Confirmar el significado de `K` y si el timestamp de origen representa hora local de Bolivia o UTC.
2. Aprobar la clave de unicidad y la precedencia entre lecturas duplicadas, especialmente cuando la primera tiene un valor vacío y la segunda uno completo.
3. Definir si temperatura y humedad faltantes pueden estimarse, con qué distancia temporal máxima y para qué usos; documentar si una estimación permite salir de cuarentena.
4. Definir si las 15 humedades negativas y las 15 fechas imposibles disponen de una fuente original recuperable. Sin ella, permanecerán en cuarentena.
5. Acordar criterios térmicos por producto antes de añadir controles de rango operativo. Un límite único para todos los productos no está justificado por este CSV.

## Contrato de salida recomendado

El segundo notebook debe leer el CSV diagnosticado, mantener `fila_bronze` y las columnas originales, y añadir columnas preparadas y de trazabilidad: `motivos_iniciales`, `tratamientos_aplicados`, `motivos_finales` y `en_cuarentena_final`. La condición para liberar una fila es que **todos** sus motivos finales hayan sido resueltos con reglas aprobadas. El archivo completo seguirá incluyendo filas válidas y en cuarentena; el extracto de cuarentena seguirá siendo informativo. Los conteos finales deberán reconciliarse con las 28.920 filas recibidas.
