# Informe del Notebook 1: diagnóstico IoT de AndinaLog 03B

## Propósito y alcance

El notebook `S4_01_AndinaLog_IoT_Diagnostico_Didactico.ipynb` examina el CSV Bronze `andinalog_iot_telemetry.csv` de AndinaLog, grupo 06, subcaso 03B. El objetivo de negocio es proteger la cadena de frío y preparar lecturas confiables para analizar excursiones térmicas por producto, viaje y camión, y futuras alertas de desviación en 60 minutos.

El diagnóstico **no corrige ni sustituye valores**. Mantiene las diez columnas originales, añade una pareja `*_estado` y `*_motivo` por cada columna, y resume el estado de cada fila. Las reglas están escritas dentro del notebook; esta versión didáctica no depende de un catálogo ni de un motor de reglas externos.

## Entradas y salidas

| Elemento | Ubicación dentro del repositorio | Función |
|---|---|---|
| Entrada Bronze | `datasets/AndinaLog_03B_Bronce/andinalog_iot_telemetry.csv` | Datos originales; 28.920 lecturas y 10 columnas. |
| Productos Silver | `proyecto-integrador/andinalog_productos/notebook2/salidas/andinalog_productos_silver.csv` | Consulta opcional de objetivo y tolerancia térmica por producto. Su cobertura es parcial. |
| Flota Silver | `proyecto-integrador/andinalog_flota/notebook2/salidas/andinalog_flota_silver.csv` | Consulta opcional de camiones. Su cobertura es parcial. |
| Diagnosticado | `proyecto-integrador/01_diagnostico/andinalog_iot_telemetry/salidas/andinalog_iot_telemetry_didactico_v1_diagnosticado.csv` | Todas las lecturas con estados, motivos y resumen. |
| Cuarentena de diagnóstico | `proyecto-integrador/01_diagnostico/andinalog_iot_telemetry/salidas/andinalog_iot_telemetry_didactico_v1_cuarentena.csv` | Subconjunto de filas que tienen al menos un problema crítico. |

La cuarentena del diagnóstico **ya está incluida en el diagnosticado**. No se deben concatenar ambos CSV.

## Diccionario de negocio y reglas

| Columna Bronze | Significado | Reglas de diagnóstico |
|---|---|---|
| `timestamp` | Momento de la lectura, expresado sin zona en el archivo. | Obligatorio; formato `AAAA-MM-DD HH:MM:SS`; fecha de calendario válida. Según la aclaración del docente, una fecha sin zona se interpreta como hora de Bolivia (`America/La_Paz`). El diagnóstico no la convierte. |
| `viaje_id` | Viaje al que pertenece la lectura. | Obligatorio; patrón `VIA-` y cinco dígitos. Junto con `timestamp` forma la clave candidata de una lectura. |
| `order_id` | Orden logística asociada. | Obligatorio; patrón `ORD-`, cuatro dígitos, guion y cinco dígitos. |
| `camion_id` | Camión que transporta el producto. | Obligatorio; patrón `CAM-` y dos dígitos. La ausencia en Flota Silver se marca para revisión porque esa tabla puede tener cobertura parcial. |
| `producto_id` | Producto transportado. | Obligatorio; patrón `PROD-` y tres dígitos. La ausencia en Productos Silver se marca para revisión, no como prueba de invalidez. |
| `temperatura_cabina_c` | Lectura térmica del compartimento/cabina monitoreada para la cadena de frío. | Obligatoria y numérica. `-999` es un centinela, no una temperatura. La interpretación física depende de `temp_unit`. |
| `temp_unit` | Unidad de la lectura térmica. | `C` es canónica; `F` es reconocida y requiere conversión posterior; `K` no es unidad operacional esperada y se clasifica como crítica. Otras unidades son inválidas. |
| `humedad_cabina_pct` | Humedad relativa medida. | Obligatoria, numérica y entre 0 % y 100 %. |
| `desviacion_termica_flag` | Indicador registrado de desviación térmica actual. | Debe ser `0` o `1`. Si hay producto con objetivo y tolerancia, se compara con el resultado calculado. Una excursión real no es un error; la incoherencia de la bandera sí requiere revisión. |
| `desviacion_proximos_60min_flag` | Indicador de desviación en la ventana futura de 60 minutos. | Debe ser `0` o `1`. El diagnóstico no reconstruye su origen ni la cambia. |

### Relaciones entre columnas

- La pareja (`viaje_id`, `timestamp`) identifica una lectura candidata. Una copia idéntica posterior se marca crítica para no contarla dos veces. Si dos filas comparten la clave y tienen datos distintos, ambas requieren revisión en cuarentena.
- Una temperatura en Fahrenheit puede evaluarse temporalmente en Celsius para revisar coherencia, pero el valor Bronze permanece intacto.
- La bandera térmica actual se compara con `|temperatura_C − objetivo_producto_C| > tolerancia_producto_C` cuando están disponibles ambas magnitudes. Sin cobertura de producto no se inventa el umbral.
- Los faltantes en tablas Silver de cobertura parcial son advertencias de integridad referencial, no motivo automático de cuarentena.

### Alcance de la comprobación producto–camión

Este diagnóstico evalúa cada CSV IoT y las referencias disponibles en su momento. La posible combinación `Fresco`/`Congelado` con camión `Seco` se evalúa **después**, en el tratamiento de IoT que cruza los maestros didácticos actuales de Productos y Flota. Esa marca relacional es una alerta para revisión operativa: no corrige el Bronze ni envía por sí sola una fila a cuarentena. El informe de tratamiento documenta la regla y el EDA muestra sus viajes por separado.

## Estados, motivos y severidad

Cada columna original tiene `nombre_estado` y `nombre_motivo`:

| Estado | Significado | Consecuencia en diagnóstico |
|---|---|---|
| `OK` | No se detectó incidencia con las reglas aplicadas. | La columna no suma problemas. |
| `NO_EVALUABLE` | Falta contexto para una evaluación concreta. | Se conserva y explica. |
| `REVISAR` | Hay una anomalía o advertencia que requiere atención. | La fila permanece en el diagnosticado. |
| `CRITICO` | Hay un problema que impide usar la lectura sin tratamiento o revisión. | `en_cuarentena=True`. |

Un mismo campo puede acumular varios textos en `*_motivo`. Además se agregan `fila_bronze`, `cantidad_problemas`, `en_cuarentena`, `severidad_maxima`, `columnas_con_problemas`, `motivos_fila`, `zona_horaria_origen`, `version_diagnostico` y `sha256_bronze`. El hash identifica exactamente el archivo de entrada usado en la corrida.

## Resultados de la ejecución revisada

| Medida | Resultado |
|---|---:|
| Filas Bronze y diagnosticadas | 28.920 |
| Columnas del diagnosticado | 39 |
| Filas sin problemas detectados | 21.381 |
| Filas con uno o más problemas | 7.539 |
| Filas con severidad `REVISAR` | 7.034 |
| Filas con severidad `CRITICO` y en cuarentena de diagnóstico | 505 |
| Lecturas con `temp_unit=F` | 50 |
| Lecturas con `temp_unit=K` | 5 |

Estas cifras describen la **salida de diagnóstico**, antes de las correcciones e imputaciones del Notebook 2. Las 505 filas de cuarentena no se consideran pérdidas definitivas: algunas pueden recuperarse mediante tratamiento justificable.

## Decisiones metodológicas y límites

1. El diagnóstico describe la calidad del dato recibido y no altera la evidencia Bronze.
2. Bolivia es la zona de origen de los timestamps sin zona; UTC se deriva en tratamiento para ordenar y unir datos entre sistemas.
3. Se distingue validez matemática de validez de negocio: Kelvin es una unidad física, pero no una unidad operativa esperada en este caso.
4. Las dimensiones Silver disponibles tienen cobertura parcial; un identificador ausente no se declara inválido solo por ese cruce.
5. El indicador de los próximos 60 minutos se valida como categoría, pero el notebook no demuestra cómo fue construido. Su uso predictivo exige controles temporales posteriores para evitar fuga de información.

## Reproducción

Ejecutar las celdas del notebook en orden desde la raíz del repositorio o en Colab con la ruta Drive configurada. El notebook verifica el esquema de diez columnas, el número de filas, que Bronze permanezca sin cambios, la correspondencia de la cuarentena y el hash de entrada. Produce exactamente los dos CSV indicados arriba.
