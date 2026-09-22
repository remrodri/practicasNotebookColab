# Informe EDA integrado — Grupo 06, AndinaLog, subcaso 03B

## Objetivo y alcance

El EDA responde al mandato del subcaso 03B: **proteger la cadena de frío, mejorar la rotación del inventario y explorar señales para anticipar desviaciones térmicas en los próximos 60 minutos**. El notebook `S4_03_AndinaLog_03B_EDA_Didactico.ipynb` combina las cuatro salidas didácticas de tratamiento. No modifica los CSV ni entrena un modelo predictivo.

Las tres evidencias se organizan por su unidad de análisis: viaje para excursiones térmicas, lote para vencimiento/merma y lectura ordenada en el tiempo para la alerta temprana. Esta separación evita contar varias lecturas como varios viajes o mezclar el final de un viaje con el inicio de otro al calcular rezagos.

## Fuentes utilizadas

| Fuente tratada | Ruta relativa a `practicasNotebookColab` | Filas | Granularidad |
|---|---|---:|---|
| IoT | `proyecto-integrador/02_tratamiento/andinalog_iot_telemetry/salidas/andinalog_iot_telemetry_didactico_v1_tratado.csv` | 28.677 | Lectura de telemetría. |
| Productos | `proyecto-integrador/02_tratamiento/andinalog_productos/salidas/andinalog_productos_didactico_v1_silver.csv` | 60 | Producto único. |
| Flota | `proyecto-integrador/02_tratamiento/andinalog_flota/salidas/andinalog_flota_didactico_v1_silver.csv` | 30 | Camión único. |
| Inventario | `proyecto-integrador/02_tratamiento/andinalog_inventory_tracking/salidas/andinalog_inventory_tracking_didactico_v1_silver.csv` | 5.980 | Lote/movimiento único. |

El notebook está ubicado en `proyecto-integrador/03_EDA/S4_03_AndinaLog_03B_EDA_Didactico.ipynb`. Las salidas antiguas de cada Notebook 2 no se usan en este EDA.

## Auditoría de joins y compatibilidad

Los cruces usan **claves tratadas**: IoT `producto_id` → Productos `producto_id_tratado`; IoT `camion_id_tratado` → Flota `camion_id_tratado`; Inventario `producto_id_tratado` → Productos `producto_id_tratado`. Las dos dimensiones son únicas y las uniones se validan como muchos-a-uno. No hubo multiplicación de filas.

| Cruce | Filas de origen | Con correspondencia | Cobertura |
|---|---:|---:|---:|
| IoT → Productos | 28.677 | 28.677 | 100 % |
| IoT → Flota | 28.677 | 28.677 | 100 % |
| Inventario → Productos | 5.980 | 5.980 | 100 % |

**Aptitud térmica:** el tratamiento IoT actualizado y el EDA, ambos con Productos Silver didáctico actual, identifican **26.183** lecturas aptas para un KPI térmico observado. El notebook verifica la concordancia **fila por fila** entre `apta_kpi_termico` y el recálculo del EDA. Las banderas `desviacion_termica_flag` coinciden con la excursión recalculada en todas las filas IoT tratadas. La cifra histórica de 23.563 correspondía a un maestro antiguo de cobertura parcial y ya no debe usarse.

Hay **2.389 lecturas** de productos cuyo umbral contiene una categoría o temperatura inferida. Se conservan para análisis exploratorio, pero no entran en el indicador principal de excursión con umbral completamente observado.

## Vista general de las fuentes

- Productos Silver: **55** productos con umbral térmico completamente observado y **5** con categoría o temperatura inferida.
- Flota Silver: **14** camiones `Refrigerado` y **16** `Seco`.
- Inventario Silver: **5.962** vencimientos observados y **18** imputados.
- IoT tratado: **1.200 viajes**, con entre **22 y 24 lecturas tratadas** por viaje. La variación frente a 24 se debe tener en cuenta al comparar viajes.

## Evidencia 1 — excursiones térmicas por viaje

Se toman lecturas con temperatura observada, umbral de producto observado y coherencia de bandera. Después se agrupan por `(viaje_id, order_id, camion_id_tratado, producto_id)` para calcular temperatura media, número de lecturas con desviación y si el viaje tuvo al menos una. El resumen por categoría y tipo se obtiene **después** de esa agregación.

La población principal tiene **26.183 lecturas**, pertenecientes a **1.100 viajes**. De esos viajes, **311** tuvieron al menos una lectura con desviación térmica (**28,3 %** de los viajes de esta población).

| Categoría | Tipo de camión | Viajes | Lecturas con desviación | Viajes con desviación |
|---|---|---:|---:|---:|
| Congelado | Refrigerado | 203 | 220 | 37,4 % |
| Congelado | Seco | 9 | 30 | 88,9 % |
| Fresco | Refrigerado | 313 | 375 | 38,3 % |
| Fresco | Seco | 8 | 36 | 87,5 % |
| Seco | Refrigerado | 291 | 100 | 18,9 % |
| Seco | Seco | 276 | 79 | 16,3 % |

El tratamiento marca como `REVISAR` **407 lecturas de 17 viajes**: 216 lecturas de 9 viajes `Congelado`/`Seco` y 191 lecturas de 8 viajes `Fresco`/`Seco`. Hay otras **1.484 lecturas** cuya compatibilidad queda `NO_EVALUABLE` por faltar categoría observada o tipo conocido. Los 17 viajes marcados **permanecen en el denominador del KPI térmico** cuando sus lecturas cumplen los criterios de observación; el notebook los resume aparte. Esta marca no es cuarentena ni certifica un fallo del vehículo.

Las combinaciones `Congelado`/`Seco` y `Fresco`/`Seco` tienen solo **9 y 8 viajes**, respectivamente. Sus porcentajes son descriptivos y **no demuestran** que el tipo de camión cause la desviación; faltaría controlar asignación de productos, ruta, clima, tiempos y otros factores. El análisis tampoco interpreta `Seco` como vehículo apto para cadena de frío solo porque aparece en un cruce.

## Evidencia 2 — vencimiento, permanencia y merma

La vista principal exige fecha de vencimiento **observada** y categoría de producto **observada**. Hay **5.673 lotes** con ambas condiciones, de 5.980 lotes Silver. Se excluyen de ese resumen los **18 vencimientos imputados** y los **289 lotes** asociados a categorías inferidas. La fecha de salida vacía representa un lote aún en almacén; el CSV Silver actual no contiene casos de salida vacía.

`días para vencer al salir = fecha_vencimiento − fecha_salida`. Un valor negativo señala una salida posterior al vencimiento. La merma porcentual se calcula por lote como `100 × cantidad_merma / cantidad_ingreso`, permitiendo una comparación proporcional sin afirmar que las unidades físicas de productos distintos sean iguales.

| Categoría | Lotes | Días promedio en almacén | Mediana de merma por lote | Mediana de días para vencer al salir | Salidas posteriores al vencimiento |
|---|---:|---:|---:|---:|---:|
| Congelado | 1.039 | 13,6 | 1,4 % | 169 | 0 |
| Fresco | 1.784 | 13,3 | 2,9 % | 7 | 425 |
| Seco | 2.850 | 21,1 | 0,7 % | 346 | 0 |

En la población observada, los **425 lotes con salida posterior al vencimiento** son de categoría `Fresco`. Esto es una prioridad para revisar procesos de rotación y merma, no evidencia suficiente para atribuir una causa. En todo el Silver hay **468** salidas posteriores al vencimiento; el total principal es menor porque excluye categorías inferidas y fechas imputadas.

La suma de `cantidad_merma` se puede mostrar como **unidades registradas**, pero no se debe etiquetar como kg, cajas o piezas: la presentación física por producto no está documentada. Para comparar categorías se prioriza el porcentaje por lote.

## Evidencia 3 — señales para alerta en 60 minutos

Las lecturas se ordenan por `(viaje_id, timestamp_utc)` y el rezago se calcula dentro del mismo viaje. La población exploratoria exige temperatura actual y anterior observadas, umbral de producto observado y un intervalo real de **30 minutos** entre lecturas. La pendiente se calcula a partir de la diferencia entre temperaturas consecutivas; la distancia actual al umbral es `|temperatura_actual − objetivo| − tolerancia`.

Hay **24.892 lecturas elegibles** con rezago y **1.153** etiquetas positivas de desviación en los próximos 60 minutos (**4,6 %**). De ellas, **24.070** aún estaban dentro de la tolerancia en el momento actual; **664** de esas lecturas tienen etiqueta positiva (**2,8 %**). Ese subconjunto es especialmente relevante para una alerta *antes* de la excursión.

| Distancia actual respecto del umbral | Lecturas | Etiqueta positiva en próximos 60 min |
|---|---:|---:|
| ≤ −2 °C | 11.526 | 1,52 % |
| −2 a 0 °C | 12.544 | 3,90 % |
| 0 a 2 °C | 273 | 17,58 % |
| > 2 °C | 549 | 80,33 % |

La proporción futura aumenta conforme la lectura actual se acerca o supera el umbral. Es una **asociación descriptiva**, no rendimiento de un modelo ni causalidad. Las dos bandas positivas ya representan una excursión actual; para evaluar aviso verdaderamente temprano conviene centrarse en las bandas con distancia ≤ 0. La bandera de los próximos 60 minutos se reserva como objetivo y no se usa para construir predictores.

## Decisiones metodológicas y límites

1. **Hora:** se ordena IoT con `timestamp_utc`; la hora de Bolivia se deriva solo para interpretar patrones horarios. Inventario utiliza fechas de calendario sin hora.
2. **Imputaciones:** no se mezclan con los KPI principales observados. Permanecen disponibles con sus marcas para análisis de sensibilidad. La alerta de posible incompatibilidad no excluye por sí sola del KPI ni de la salida tratada.
3. **Granularidad:** los viajes se cuentan después de agregar lecturas; los lotes se cuentan una vez; los rezagos se calculan por viaje.
4. **Cobertura y selección:** los denominadores de los indicadores son subconjuntos distintos de los Silver completos. Las restricciones mejoran la trazabilidad, pero impiden generalizar automáticamente los porcentajes a todas las filas.
5. **Predicción:** este EDA no evalúa un clasificador. Un modelo futuro debe dividir datos en el tiempo, evitar usar información posterior al instante de predicción y reconstruir inferencias usando solo datos disponibles en entrenamiento.
6. **Gráficos:** el notebook genera gráficos con Matplotlib cuando está disponible, como en Colab. Si el entorno no lo tiene instalado, ejecuta las tablas y comprobaciones sin gráficos.

## Próximo uso

Las tablas y visualizaciones del EDA pueden alimentar la exposición del grupo 06 y el informe del caso 03B. Los hallazgos que merecen validación operativa son la concentración de salidas posteriores al vencimiento en productos frescos y los 17 viajes con posible incompatibilidad producto–camión. Para desarrollar la alerta de 60 minutos, conviene comenzar con las lecturas aún dentro de tolerancia y evaluar temporalmente las variables de rezago, pendiente y distancia al umbral.
