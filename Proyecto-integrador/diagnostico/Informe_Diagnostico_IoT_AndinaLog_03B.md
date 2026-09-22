# Informe y diccionario del diagnóstico IoT — AndinaLog 03B

**Corte:** 21 de septiembre de 2026  
**Implementación:** `proyecto-integrador/diagnostico/quality_engine.py`, `andinalog_iot_telemetry/catalogo_reglas_iot.json` y Notebook 1.  
**Versión ejecutada:** diagnóstico `GIAD-M3-S4-IOT-diagnostico-v6`, catálogo `1.1.0`.  
**Origen:** `datasets/AndinaLog_03B_Bronce/andinalog_iot_telemetry.csv`, 28.920 lecturas.  
**Huella SHA-256 de Bronze:** `edb7afe2f7fb836e59fe605d30c88b3b5b13a6d8ab2ec0b37f206a14e58de6bf`.

## 1. Finalidad y alcance

El mandato de AndinaLog 03B es proteger la cadena de frío, mejorar la rotación de inventario y anticipar desviaciones térmicas durante el transporte. El diagnóstico IoT aporta lecturas confiables para calcular excursiones por producto, viaje y camión, y para ordenar la serie temporal de cada viaje. **Diagnosticar significa detectar, clasificar y explicar; no convertir, imputar, corregir ni eliminar valores Bronze.**

El nombre `temperatura_cabina_c` se interpreta operativamente como temperatura del compartimento de carga porque hay lecturas cercanas a −18 °C y el proyecto las relaciona con la temperatura requerida del producto. La ubicación física exacta del sensor no está documentada. El sufijo `_c` del nombre no garantiza que todos los números sean Celsius: la unidad efectiva está en `temp_unit`.

## 2. Cómo se creó el catálogo

Se eligió **JSON** porque cada regla necesita parámetros de distinto tipo: patrones de ID, límites numéricos, claves compuestas, fuentes de referencia y dependencias de producto. El archivo separa esas reglas específicas del motor reusable. Una regla tiene un identificador estable y declara el campo afectado, tipo de comprobación, parámetros, código de error, dimensión, severidad, acción sugerida y detalle explicativo.

Se construyó a partir de cuatro capas:

1. **Contrato técnico:** esquema de diez columnas, obligatoriedad, tipos, fechas reales, patrones de ID y flags binarios.
2. **Validez física y del sensor:** humedad entre 0 y 100 %, temperatura numérica y centinela `-999` como lectura ausente.
3. **Dominio logístico:** `C` canónica; `F` interpretable pero pendiente de normalización; `K` no esperada en la operación; tolerancia térmica definida por producto, no por un rango global.
4. **Relaciones y tiempo:** clave candidata `(viaje_id, timestamp)`, distinción entre copias y conflictos, referencias a Productos y Flota Silver, y posible maestro de viajes.

El motor genera una incidencia por incumplimiento y conserva `fila_bronze` para enlazarla con la fila original. `CRITICAL` identifica una lectura o clave que no puede utilizarse con seguridad bajo la regla actual; `WARNING` pide revisión o normalización sin invalidarla automáticamente. La acción del catálogo es la propuesta del diagnóstico; el tratamiento posterior toma la decisión efectiva.

### Diccionario de campos del catálogo de diagnóstico

| Campo | Significado |
|---|---|
| `version_catalogo` | Versión de las reglas aplicadas; permite reproducir un lote. |
| `columnas_bronze` | Orden y nombres esperados de las diez columnas crudas. |
| `clave_candidata` | `viaje_id` + `timestamp`; su unicidad operacional aún es una hipótesis documentada. |
| `rule_id` | Identificador estable de la regla; enlaza diagnóstico con catálogo de tratamiento. |
| `columna` | Columna o clave compuesta que evalúa la regla. |
| `tipo_regla` | Operador implementado por el motor, por ejemplo `datetime`, `sentinel`, `foreign_key` o `temperature_product_range`. |
| `parametros` | Patrón, rango, valor centinela, columnas de clave o dataset de referencia. |
| `codigo_error` | Motivo compacto para reportes y decisiones posteriores. |
| `dimension_calidad` | Completitud, conformidad, validez, unicidad o integridad. |
| `severidad` / `accion` | Clasificación diagnóstica y acción sugerida (`CUARENTENA` o `REVISAR`). |
| `detalle` | Explicación legible de por qué se activó la regla. |

## 3. Diccionario de datos y criterio de negocio

| Campo Bronze | Significado usado | Regla clave y motivo |
|---|---|---|
| `timestamp` | Momento de la lectura. | Fecha real; ordenar por viaje para rezagos y ventanas de 60 minutos. El texto no informa zona horaria. |
| `viaje_id` | Trayecto que agrupa lecturas. | Obligatorio, patrón `VIA-#####`, referencia a viaje si existe maestro. |
| `order_id` | Pedido asociado. | Obligatorio, patrón `ORD-YYYY-#####`; el año del código no sustituye una validación contra pedidos. |
| `camion_id` | Vehículo de la lectura. | Obligatorio, patrón `CAM-##`, referencia a Flota; espacios/minúsculas no alteran Bronze. |
| `producto_id` | Carga transportada. | Obligatorio, patrón `PROD-###`; permite aplicar objetivo y tolerancia térmica. |
| `temperatura_cabina_c` | Lectura térmica del compartimento de carga, como interpretación de negocio. | Numérica; vacío y `-999` son incidencias distintas. El rango pertinente depende de producto y unidad. |
| `temp_unit` | Unidad de la lectura. | `C`: canónica. `F`: reconocida y pendiente de conversión. `K`: no esperada y crítica. Otras: desconocidas. |
| `humedad_cabina_pct` | Humedad relativa de la carga, en %. | Numérica, 0–100; faltante o fuera de rango afecta la utilidad de la lectura. |
| `desviacion_termica_flag` | Señal de desviación térmica actual. | Debe ser 0/1. Un 1 puede representar un evento real, no un error. Se contrasta con el umbral del producto donde sea evaluable. |
| `desviacion_proximos_60min_flag` | Etiqueta de desviación futura en el viaje. | Debe ser 0/1. No equivale a error ni a cuarentena; su definición temporal exacta requiere validación para modelado. |

**Convención de tiempo adoptada para el proyecto:** el tratamiento interpretará las fechas Bronze sin zona como `America/La_Paz` y creará UTC como representación canónica. Es una decisión metodológica del equipo, no un metadato probado del archivo. El diagnóstico conserva el texto original.

## 4. Diccionario de las 30 reglas y sus motivos

| ID | Comprobación | Motivo de negocio o calidad | Severidad |
|---|---|---|---|
| R001–R002 | `timestamp` obligatorio y fecha real | Sin tiempo fiable no se ordena el viaje. | Crítica |
| R003–R004 | `viaje_id` obligatorio y patrón | Sin viaje fiable no se agrupa la serie. | Crítica |
| R005–R006 | `order_id` obligatorio y patrón | Relación trazable con el pedido. | Crítica |
| R007–R008 | `camion_id` obligatorio y patrón | Vehículo identificable; el formato puede tratarse si se confirma en Flota. | Crítica |
| R009–R010 | `producto_id` obligatorio y patrón | Permite consultar el contrato térmico del producto. | Crítica |
| R011 | Copia idéntica de clave de lectura | Evita contar dos veces una misma medición. | Crítica |
| R012 | Misma clave con contenidos distintos | No se elige una lectura sin evidencia. | Crítica |
| R013 | `temp_unit` obligatoria | Sin unidad no se interpreta la magnitud. | Crítica |
| R014 | Unidad ajena a `C`, `F`, `K` | Unidad desconocida. | Crítica |
| R015 | Unidad `F` | Válida, pero requiere valor preparado en °C. | Advertencia |
| R016–R017 | Temperatura obligatoria y numérica | Lectura necesaria para cadena de frío. | Crítica |
| R018 | Temperatura `-999` | Código centinela, no temperatura real. | Crítica |
| R019–R020 | Humedad obligatoria y numérica | Dato requerido por el contrato actual de calidad. | Crítica |
| R021 | Humedad fuera de 0–100 % | Valor físicamente inválido. | Crítica |
| R022–R023 | Flag térmico actual presente y binario | La señal debe poder interpretarse. | Crítica |
| R024–R025 | Flag de próximos 60 minutos presente y binario | La etiqueta debe poder interpretarse. | Crítica |
| R026 | Producto ausente en Productos Silver | Dimensión de cobertura parcial; no prueba por sí sola un ID inválido. | Advertencia |
| R027 | Camión ausente en Flota Silver | Dimensión de cobertura parcial; no prueba por sí sola un ID inválido. | Advertencia |
| R028 | Viaje ausente en maestro de viajes | Regla declarada, pero sin fuente disponible en esta ejecución. | Crítica si se ejecuta |
| R029 | Unidad `K` | Kelvin no pertenece al contrato operacional adoptado para AndinaLog. | Crítica |
| R030 | Flag térmico frente a objetivo ± tolerancia de producto | Detecta desacuerdo entre señal y umbral; no marca como error una excursión correctamente señalada. | Advertencia |

En R030, la conversión de `F` a °C se calcula **solo en memoria para comprobar la regla**. Se omiten valores faltantes, `-999`, `K` y filas sin referencia térmica válida. La comparación usa `temperatura_conservacion_requerida_c` y `tolerancia_temperatura_c` de Productos Silver.

## 5. Resultado ejecutado

| Métrica | Resultado |
|---|---:|
| Lecturas Bronze | 28.920 |
| Filas con al menos una incidencia | 7.539 |
| Incidencias totales | 8.108 |
| Incidencias críticas / advertencias | 510 / 7.598 |
| Filas en cuarentena inicial | 505 |
| Reglas no ejecutadas | 1 (`R028`, sin maestro de viajes) |

Principales incidencias: 5.067 faltas de correspondencia en Productos Silver; 2.481 en Flota Silver; 120 temperaturas `-999`; 115 copias idénticas; 100 humedades faltantes; 80 temperaturas faltantes; 50 lecturas `F`; 50 formatos de camión no canónicos; 15 fechas imposibles; 15 humedades fuera de rango; 10 incidencias en cinco pares de lecturas conflictivas; y cinco unidades `K`. R030 se ejecutó sin encontrar discrepancias evaluables. Estos recuentos **se superponen**: no deben sumarse como filas distintas.

## 6. Limitaciones y corrección pendiente

- La ubicación física del sensor no está confirmada; «compartimento de carga» es una interpretación coherente con el proyecto y los valores.
- La zona horaria Bronze no se documenta en el archivo. La conversión futura a UTC descansa en la convención del equipo.
- Productos y Flota Silver tienen cobertura parcial. Sus faltas de correspondencia son advertencias, no pruebas de invalidez.
- **Defecto de trazabilidad de v6:** `columna_afectada` y `columnas_con_problemas` quedaron vacías por la forma en que el motor trasladó `columna` al resultado. El código de regla y `fila_bronze` sí identifican las incidencias, pero debe corregirse y regenerarse una versión posterior antes de usar reportes por columna.

## 7. Archivos de salida

El Notebook 1 generó, en `proyecto-integrador/diagnostico/andinalog_iot_telemetry/salidas/`, CSV con prefijo `andinalog_iot_telemetry_v6_`: `diagnosticado`, `problemas`, `cuarentena`, `reporte_calidad`, `reporte_por_regla`, `reporte_por_columna`, `reporte_por_dimension` y `estado_reglas`.
