# Informe y diccionario del tratamiento IoT — AndinaLog 03B

**Corte:** 21 de septiembre de 2026  
**Implementación activa:** `proyecto-integrador/tratamiento/` (`treatment_engine.py`, `iot_treatment.py`, catálogo JSON y Notebook 2).  
**Versiones ejecutadas:** tratamiento `GIAD-M3-S4-IOT-tratamiento-v5`; entrada diagnóstica `GIAD-M3-S4-IOT-diagnostico-v6`.  
**Origen:** 28.920 lecturas Bronze; la huella SHA-256 coincide con el diagnóstico: `edb7afe2f7fb836e59fe605d30c88b3b5b13a6d8ab2ec0b37f206a14e58de6bf`.

## 1. Finalidad y arquitectura

El tratamiento toma las incidencias del diagnóstico y decide qué valor preparado puede usarse y qué filas deben permanecer fuera de Silver. El archivo **tratado** conserva las diez columnas Bronze originales; las conversiones y decisiones se guardan en columnas adicionales. Una fila nunca se borra para ocultar un problema.

Se separaron tres responsabilidades:

- `treatment_engine.py`: contrato reutilizable para cargar el catálogo, validar entradas, iniciar y cerrar acciones, calcular estado final y exportar sin sobrescribir versiones anteriores.
- `iot_treatment.py`: decisiones propias de IoT: temperatura, zona horaria, camiones, pares duplicados, cobertura y aptitud térmica.
- Notebook 2: localiza el proyecto y ejecuta el tratamiento. Lee el diagnóstico en `proyecto-integrador/diagnostico/` y escribe en `proyecto-integrador/tratamiento/salidas/`.

## 2. Cómo se creó el catálogo de tratamiento

El catálogo activo es **`catalogo_reglas_tratamiento.json`**. Se eligió JSON para mantener el mismo formato que el catálogo de diagnóstico y admitir metadatos y parámetros estructurados en futuras reglas. El CSV anterior ya no es el catálogo activo de `proyecto-integrador/tratamiento/`.

El catálogo contiene **30 decisiones**, una por cada `rule_id` del diagnóstico IoT 1.1.0. Sus identificadores estables permiten relacionar una incidencia de `problemas` con su política de tratamiento. Se creó clasificando cada regla según el efecto que tendría en la utilidad de una lectura:

1. **Resolución determinista:** por ejemplo, `F` se convierte a °C cuando el número es válido; un camión se normaliza solo si su ID canónico figura en Flota Silver; una copia se excluye si puede seleccionarse una lectura canónica con evidencia.
2. **Bloqueo pendiente:** datos esenciales faltantes o físicamente inválidos, `-999`, `K`, fechas imposibles y conflictos no resueltos impiden ingresar esa fila a Silver.
3. **Advertencia de cobertura:** un Producto o Camión ausente de una dimensión Silver parcial se registra, pero no invalida automáticamente la lectura Bronze. La aptitud para análisis que necesitan esa dimensión se indica por separado.

El catálogo no inventa datos ni convierte una advertencia en corrección. El adaptador IoT registra el resultado real de cada intento. Una incidencia solo pasa a `RESUELTO` cuando se aplicó y verificó un tratamiento; una copia pasa a `EXCLUIDO`, y una advertencia que no bloquea puede permanecer como `ADVERTENCIA`.

### Diccionario de campos del catálogo de tratamiento

| Campo | Significado |
|---|---|
| `version_catalogo` | Versión de las políticas de tratamiento. |
| `dataset` | Fuente a la que aplica: `andinalog_iot_telemetry`. |
| `version_diagnostico_requerida` | Contrato de entrada; impide mezclar reglas con un diagnóstico incompatible. |
| `regla_id` | Identificador que corresponde al `rule_id` del catálogo diagnóstico. |
| `codigo_error` | Motivo recibido desde diagnóstico. |
| `estado_inicial` | `PENDIENTE` o `ADVERTENCIA` antes de intentar una acción. |
| `bloquea_silver` | Indica si la incidencia impide inicialmente que la fila entre en Silver. No reemplaza la evaluación final tras las acciones. |
| `tratamiento_propuesto` | Acción candidata expresada en lenguaje legible. |
| `justificacion` | Razón de la política, especialmente cuando una advertencia no bloquea. |

## 3. Diccionario de decisiones por familia de reglas

| Reglas de diagnóstico | Decisión y motivo de negocio |
|---|---|
| R001–R010 | Tiempo e identificadores faltantes o mal formados quedan pendientes. R008 puede resolverse si el `camion_id` canónico, tras quitar espacios y pasar a mayúsculas, existe inequívocamente en Flota Silver. |
| R011–R012 | Se analizan pares con `(viaje_id, timestamp)`. En pares idénticos o complementarios sin contradicción se conserva una lectura canónica y la copia queda fuera de Silver. Conflictos ambiguos permanecen bloqueados. |
| R013–R014 | Unidad ausente o desconocida: sin interpretación fiable, no se prepara temperatura. |
| R015 | `F` se convierte a °C con `(F − 32) × 5/9` en `temperatura_c_preparada`; se conserva el número Bronze. |
| R016–R018 | Temperatura vacía, no numérica o `-999`: no se imputa ni se utiliza como medición térmica. |
| R019–R021 | Humedad vacía, no numérica o fuera de 0–100 %: no se inventa ni corrige automáticamente. |
| R022–R025 | Flags ausentes o ajenos a 0/1: la lectura queda pendiente de una fuente válida. Un flag 1 bien formado no es, por sí mismo, un error. |
| R026–R027 | Sin Producto o Camión en Silver: advertencia de cobertura, sin cuarentena automática; se marcan campos de cobertura. |
| R028 | Regla de viajes declarada en diagnóstico, pero no ejecutada por falta de maestro; no se simula una validación. |
| R029 | `K` no es unidad operacional esperada. No se convierte a °C automáticamente y la fila sigue en cuarentena. |
| R030 | Una discrepancia entre el flag y el rango del producto se trataría como advertencia para revisión. La ejecución v6 no produjo incidencias de esta regla. |

## 4. Diccionario de datos preparados y salidas

| Campo o archivo | Definición |
|---|---|
| `timestamp` | Texto Bronze original, conservado. |
| `timestamp_utc` | Fecha válida interpretada como hora de Bolivia y representada en UTC. Una fecha imposible queda vacía. |
| `zona_horaria_origen_asumida` | `America/La_Paz`; explicita una convención del equipo, no una prueba del origen. |
| `temperatura_c_preparada` | Valor Celsius listo para análisis cuando la unidad es `C` o `F` y la lectura no es `-999`. |
| `tratamiento_temperatura` | `C_ORIGINAL`, `F_A_C` o `SIN_TRATAMIENTO`; ninguna fila `K` se marca como convertida. |
| `camion_id_preparado` | ID canónico cuando pudo confirmarse en Flota Silver; el Bronze original sigue intacto. |
| `en_cuarentena_final` / `motivos_finales` | Resultado de incidencias bloqueantes aún pendientes o de copias excluidas. |
| `cobertura_producto` / `cobertura_flota` | Indican disponibilidad de cada dimensión Silver; una ausencia no equivale automáticamente a dato inválido. |
| `apto_serie` | Lectura fuera de cuarentena con `timestamp_utc` válido. |
| `apto_termica` | Lectura apta para serie, con producto en la dimensión y temperatura preparada. |
| `*_tratado.csv` | Todas las filas Bronze con columnas nuevas de preparación y decisión. |
| `*_silver.csv` | Lecturas sin bloqueo final; temperatura en °C, unidad `C`, UTC y campos de cobertura. |
| `*_acciones.csv` | Una decisión trazable por incidencia diagnóstica. |
| `*_decisiones_duplicados.csv` | Clasificación y selección canónica de cada par repetido. |
| `*_cuarentena_final.csv` | Filas que siguen excluidas de Silver. |
| `*_reporte_tratamiento.csv` | Métricas ejecutadas y versiones de entrada y salida. |

La hora de origen se interpreta como `America/La_Paz` por decisión metodológica del equipo. Para la primera lectura, `2026-08-11 14:11:00` produce `2026-08-11T18:11:00Z`. La zona real del sistema emisor **no está indicada en Bronze**; si se obtiene evidencia distinta, se deberá regenerar UTC y los análisis temporales posteriores.

## 5. Resultado ejecutado

| Métrica | Resultado |
|---|---:|
| Filas Bronze conservadas en tratado | 28.920 |
| Filas en Silver | 28.464 |
| Cuarentena inicial / final | 505 / 456 |
| Filas liberadas respecto a la cuarentena inicial | 49 |
| Filas aptas para análisis térmico con producto | 23.478 |
| Temperaturas `F` convertidas / `K` convertidas | 50 / 0 |
| Camiones normalizados con respaldo de Flota Silver | 44 |
| Pares de lectura revisados | 120: 115 idénticos y 5 complementarios |
| Copias excluidas de Silver | 120 |

Las **8.108 acciones** quedaron como 99 `RESUELTO`, 120 `EXCLUIDO`, 341 `PENDIENTE` y 7.548 `ADVERTENCIA`. Son acciones por incidencia y no equivalen a filas distintas. Las 44 normalizaciones de camión y cinco selecciones canónicas explican las 49 filas que dejaron la cuarentena inicial; las 50 conversiones `F` resolvieron advertencias que no bloqueaban por sí solas.

Se comprobó que el tratado conserva sin cambios las diez columnas Bronze, Silver no contiene `-999`, no tiene claves `(viaje_id, timestamp)` duplicadas y las cinco filas `K` permanecen en cuarentena.

## 6. Límites y próximos controles

- Productos y Flota Silver tienen cobertura parcial. `apto_termica` restringe explícitamente los análisis que requieren umbral por producto. El reporte cuenta 5.067 filas sin Producto Silver y 2.437 sin Flota Silver en el tratado; los valores se refieren a cobertura, no a errores de identidad confirmados.
- El maestro de viajes sigue ausente, por lo que la asignación de cada viaje no quedó validada contra una fuente autoritativa.
- `columna_afectada` llegó vacía desde el diagnóstico v6. `acciones` conserva `rule_id`, código y fila, pero la trazabilidad por columna requiere corregir y regenerar el diagnóstico.
- La interpretación horaria debe mantenerse visible en cualquier evidencia de 60 minutos. No debe presentarse como zona verificada del emisor.

## 7. Archivos de salida

En `proyecto-integrador/tratamiento/salidas/` se generaron seis CSV con prefijo `andinalog_iot_telemetry_v5_`: `tratado`, `silver`, `acciones`, `decisiones_duplicados`, `cuarentena_final` y `reporte_tratamiento`. La versión v5 no sobrescribe salidas previas.
