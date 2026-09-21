# Guía de trabajo — Proyecto Integrador AndinaLog 03B

**Grupo 06 · Operaciones y Planificación de Datos**  
**Versión de seguimiento: hasta la Sesión 6 · 18 de septiembre de 2026**

## 1. Propósito y alcance

El mandato del proyecto es **proteger la cadena de frío, mejorar la rotación del inventario y anticipar desviaciones térmicas durante el transporte**. Los resultados deben responder a tres evidencias:

| Evidencia | Pregunta principal | Tipo de trabajo |
|---|---|---|
| 1. Cadena de frío | ¿Cómo se presentan las excursiones térmicas por viaje, producto, categoría y camión? | Integración, EDA e interpretación descriptiva. |
| 2. Inventario | ¿Cómo se relacionan permanencia, vencimiento y merma? | Integración, EDA e interpretación descriptiva. |
| 3. Anticipación térmica | ¿Qué puede saberse, en una lectura del viaje, acerca de una desviación durante los siguientes 60 minutos? | Serie temporal, variables predictoras y dos contratos supervisados. |

**Los dos contratos predictivos pertenecen a la Evidencia 3.** No se requiere construir un modelo para cada una de las tres evidencias. El notebook formativo de S6 enseña el flujo de regresión; su contenido no sustituye las definiciones ni las validaciones de AndinaLog.

Esta guía registra lo **hecho y comprobado en los notebooks existentes**, lo que todavía es un experimento y el siguiente trabajo. Las instrucciones de otras guías y documentos se usan como referencias del proyecto; los recuentos y métricas de esta versión proceden de las salidas ejecutadas en el repositorio.

## 2. Fuentes y reglas comunes

El equipo conserva los archivos Bronze originales, diagnostica sus problemas, documenta reglas y cuarentenas, genera sus propios Silver y valida cada Silver antes de integrarlo. El Silver de referencia del curso no reemplaza este proceso.

| Fuente Silver usada | Papel actual |
|---|---|
| `andinalog_iot_telemetry_silver.csv` | Lecturas por viaje; Evidencias 1 y 3. |
| `andinalog_productos_silver.csv` | Categoría y parámetros térmicos; Evidencias 1, 2 y 3. |
| `andinalog_flota_silver.csv` | Características del camión; Evidencias 1 y 3. |
| `andinalog_inventory_tracking_silver.csv` | Movimientos o lotes; Evidencia 2. |

Las fuentes no se unen en una tabla única para todo el proyecto. Cada evidencia declara primero su **unidad de observación**, las claves y la cardinalidad de sus joins. Antes y después de integrar se comprueban la unicidad de las dimensiones, los registros sin correspondencia y que no se multipliquen filas por accidente. Una validación descriptiva individual de cada Silver es útil, pero el EDA principal se hace sobre el dataset analítico de la evidencia.

### Rutas de los trabajos existentes

Las rutas son relativas a la raíz `practicasNotebookColab/`:

| Trabajo | Notebook |
|---|---|
| EDA Evidencia 1 | `proyecto-integrador/EDA/Evidencia-1-Excursiones-térmicas/S4_03_AndinaLog_Evidencia1_Excursiones_Termicas.ipynb` |
| EDA Evidencia 2 | `proyecto-integrador/EDA/Evidencia_2_Riesgo_de_vencimiento_y_merma/S4_03_AndinaLog_Evidencia2_Vencimiento_Merma.ipynb` |
| EDA Evidencia 3 | `proyecto-integrador/EDA/Evidencia_3_Alerta_60min/S4_03_AndinaLog_Evidencia3_Alerta_60min.ipynb` |
| S6 · Contrato 1, regresión | `proyecto-integrador/regresion/S6_AndinaLog_03B_Contrato1_Regresion_60min.ipynb` |

## 3. Estado comprobado hasta S6

| Etapa | Estado | Evidencia de avance |
|---|---|---|
| Diagnóstico, tratamiento, cuarentena y Silver | Realizados para IoT, Productos, Flota e Inventory Tracking. | Notebooks de diagnóstico y tratamiento, archivos Silver y reportes de salida. |
| Integración y EDA de Evidencia 1 | Ejecutados. | IoT agregado a viaje; joins con Producto y Flota; notebook sin errores. |
| Integración y EDA de Evidencia 2 | Ejecutados. | Inventory + Productos; notebook sin errores. |
| Integración y EDA de Evidencia 3 | Ejecutados. | Serie IoT conservada a nivel lectura; variables temporales y corte candidato; notebook sin errores. |
| Dos contratos predictivos de Evidencia 3 | Definidos conceptualmente según la guía v8. | Uno de regresión y otro de clasificación; sus objetivos son diferentes. |
| Experimento S6 del Contrato 1 | Ejecutado y evaluado. | Baseline, regresión lineal y Random Forest; selección en VALIDACIÓN y evaluación posterior en TEST. |
| Contrato 2 de clasificación | Pendiente de modelado y evaluación. | `desviacion_proximos_60min_flag` está disponible y fue explorado, pero aún no hay experimento de clasificación concluido. |
| Alerta operativa o modelo final | Pendiente. | Faltan revisión de cobertura, definición operativa de umbrales y evaluación específica del riesgo de omitir excursiones. |

**Estado no equivale a aprobación operativa.** Que un notebook se ejecute correctamente demuestra reproducibilidad técnica sobre estos datos; la utilidad para interceptar un camión requiere una evaluación adicional.

## 4. Evidencia 1 — Cadena de frío

### Construcción

IoT contiene varias lecturas por viaje. Se resume primero por `viaje_id`, `order_id`, `camion_id` y `producto_id`, y luego se unen Productos por `producto_id` y Flota por `camion_id`. La unidad analítica principal es el **viaje**. Entre las medidas figuran número de lecturas, desviaciones térmicas y si hubo al menos una desviación.

### Resultado ejecutado y límite

El EDA registró **28.425 lecturas utilizables y 1.200 viajes**. Hubo **346 viajes con al menos una lectura marcada como desviación (28,83 %)**. El notebook informa **210 combinaciones sin producto** y **101 sin camión en Flota**. Esas faltas de correspondencia delimitan las comparaciones por categoría y tipo de camión.

El resultado identifica asociaciones descriptivas. No permite atribuir una causa térmica a un producto o camión sin controles operativos adicionales. Esta evidencia **no necesita un modelo predictivo propio**.

## 5. Evidencia 2 — Vencimiento y merma

### Construcción

La unidad es el **lote o movimiento de inventario**. Se relaciona Inventory Tracking con Productos por `producto_id`. Se distinguen la fecha de ingreso, salida y vencimiento, días en almacén, cantidad de merma y categoría logística. Una fecha de salida vacía se interpreta según la regla de negocio antes de declararla error; `aun_en_almacen` y los días restantes al vencimiento deben tener una fecha de referencia explícita.

### Resultado ejecutado y límite

El EDA utilizó **5.907 lotes**; encontró **0 aún almacenados**, **465 vencidos** y **1.495 próximos a vencer** según su fecha de referencia. Registró **52.739 unidades de merma**, equivalentes al **1,73 %** de las unidades ingresadas. El corte empleado fue **19 de octubre de 2026**, inferido en el notebook como última fecha operativa observada, y el umbral de proximidad fue de **30 días**. También quedaron **1.000 lotes sin producto** en la dimensión.

Estos recuentos corresponden al **corte analítico definido en el notebook**, no a una afirmación sobre el inventario vigente hoy. La cobertura parcial de Productos limita el análisis por categoría. Esta evidencia **no necesita un modelo predictivo propio**.

## 6. Evidencia 3 — Serie temporal y dos contratos

La unidad es **una lectura IoT de un viaje**. A diferencia de la Evidencia 1, no se reduce IoT a una fila por viaje: se conserva la secuencia y se ordena por `viaje_id` y `timestamp`. Los rezagos y tendencias se calculan dentro de cada viaje. Nunca debe aplicarse `shift()` o `rolling()` sobre todos los viajes como si fueran una sola serie.

El EDA 3 trabajó con **28.425 lecturas de 1.200 viajes**. El flag binario estaba marcado en **1.318 lecturas (4,64 %)**. El conjunto candidato de ese EDA tenía **20.523 lecturas (72,20 %)** y 905 viajes. La cobertura incluía **4.984 lecturas sin Producto** y **2.389 sin Flota**. Estos números son del **EDA para clasificación** y no son intercambiables con la muestra del experimento de regresión, que aplica reglas adicionales para construir un objetivo futuro continuo.

### 6.1 Contrato 1 — Regresión, trabajado en S6

| Elemento | Definición |
|---|---|
| Decisión | Estimar la magnitud de un posible desvío térmico futuro para priorizar revisión o intercepción. |
| Unidad y momento | Una lectura IoT; la predicción se hace en su `timestamp`. |
| Horizonte | Observaciones **posteriores** a la lectura y hasta 60 minutos después, dentro del mismo viaje. |
| Objetivo `y` | Máximo futuro, en °C, de `abs(temperatura_cabina_c − temperatura_conservacion_requerida_c) − tolerancia_temperatura_c`. Puede ser negativo cuando el máximo permanece dentro del límite. |
| `X` usada en el notebook S6 | Temperatura y humedad actuales, temperatura anterior, cambio de temperatura por minuto, distancia actual al umbral, categoría logística y tipo de camión. |
| Exclusiones | El máximo futuro, el flag de los próximos 60 minutos y toda información conocida solo después de la lectura. |

La guía de contratos v8 también propone considerar **eventos previos de flota y atributos del pedido**. El primer experimento S6 aún no los incorpora. Su inclusión requiere verificar las claves, el momento en que se conocían y la cobertura; no basta con encontrar la columna en un archivo.

#### Construcción del objetivo

El notebook une IoT con Productos y Flota sin multiplicar lecturas. Calcula la distancia térmica al umbral en cada lectura y, por viaje, toma el máximo en la ventana `(t, t + 60 minutos]`. Excluye una fila cuando el viaje no tiene observación hasta el fin del horizonte, no hay una lectura futura utilizable o faltan datos necesarios. Esta regla es conservadora; documenta qué población queda representada.

Sobre **21.482 ventanas comparables**, `máximo futuro > 0` y el flag binario del Silver discrepan en **7 casos**. El notebook muestra esas filas. No se debe afirmar la causa sin contrastar la regla exacta con que se generó el flag; entre las posibilidades están la inclusión de la lectura actual y diferencias en la ventana o el umbral.

#### Muestra y partición

Quedaron **18.733 lecturas elegibles (65,90 % de las lecturas IoT Silver)**; **920 (4,91 %)** tienen un máximo futuro positivo. Los motivos de exclusión se superponen y sus recuentos **no deben sumarse**. Para evaluar se separan **viajes completos en orden temporal**, con margen de 60 minutos entre bloques:

| Bloque | Viajes | Lecturas | Máximo futuro positivo |
|---|---:|---:|---:|
| Ajuste | 514 | 10.636 | 562 (5,28 %) |
| Validación | 178 | 3.684 | 129 (3,50 %) |
| Histórico anterior a TEST, usado para reajuste final | 710 | 14.693 | Incluye ajuste, validación y viajes anteriores elegibles. |
| TEST | 181 | 3.751 | 212 (5,65 %) |

El corte de VALIDACIÓN fue **18 de agosto de 2026, 12:12** y el de TEST **24 de agosto de 2026, 18:54**. Las filas de viajes que cruzan un corte o su margen quedan fuera de esa comparación. El histórico para el reajuste final incluye datos anteriores a TEST; no es la suma exacta de Ajuste y Validación porque también conserva viajes elegibles alrededor del corte de validación.

#### Experimento y resultados

La media de entrenamiento (`DummyRegressor`) sirve de baseline. Regresión lineal y Random Forest se compararon en VALIDACIÓN. Random Forest obtuvo allí **RMSE de 1,020 °C**, frente a **1,059 °C** de regresión lineal y **1,503 °C** del baseline. La elección del regresor se hizo **antes de consultar TEST**.

Después de reajustar el modelo elegido y el baseline con el historial anterior a TEST, se obtuvo:

| Modelo | MAE TEST | RMSE TEST | R² TEST |
|---|---:|---:|---:|
| Baseline de media | 1,236 °C | 1,763 °C | −0,013 |
| Random Forest | 0,727 °C | 1,112 °C | 0,597 |

La mejora del RMSE general frente al baseline fue de **36,94 %**. Sin embargo, entre las **212 lecturas de TEST con excursión futura**, Random Forest tuvo **MAE de 2,326 °C**, **RMSE de 3,040 °C** y una **subestimación media de 2,292 °C**. En **59,43 %** de esas lecturas, la predicción fue `≤ 0` pese a que el máximo futuro real superó el umbral.

**Interpretación:** el experimento demuestra capacidad de reducir el error promedio respecto a una referencia sencilla, pero **no demuestra que el modelo sea una alerta segura o útil para decidir una intercepción**. El error en excursiones, su frecuencia, el costo de una omisión y el umbral de acción requieren análisis específico. No se debe transformar `predicción > 0` en una regla operativa aprobada solo con estas métricas.

### 6.2 Contrato 2 — Clasificación, pendiente

| Elemento | Definición |
|---|---|
| Decisión | Alertar si se espera una superación del umbral térmico en la próxima hora para valorar un desvío o intercepción. |
| Unidad y momento | Una lectura IoT en el instante `timestamp`. |
| Horizonte | Próximos 60 minutos del mismo viaje. |
| Objetivo `y` | `desviacion_proximos_60min_flag`, con valores 0 y 1; es un campo precomputado en el Silver. |
| `X` candidatas | Lecturas actuales y pasadas, parámetros térmicos del producto y atributos conocidos del camión; eventualmente eventos previos de flota y atributos disponibles del pedido. |
| Exclusiones | El propio flag, datos futuros y cualquier otra bandera que no esté disponible al emitir la predicción. |

El contrato está definido y el EDA de su target está realizado. **No hay todavía un modelo de clasificación evaluado** en los notebooks revisados. Antes de entrenarlo se debe comprobar la regla y disponibilidad temporal del flag, revisar los 7 desacuerdos observados frente al objetivo continuo, fijar una partición temporal por viajes y establecer un baseline de clasificación. La baja frecuencia de positivos exige interpretar métricas relacionadas con omisiones y falsas alarmas, además de la métrica global que se elija cuando el curso aborde clasificación.

## 7. Qué hacer después de S6

### Cierre responsable del Contrato 1

1. Registrar en el texto del notebook la lectura industrial de las métricas generales y de las **212 excursiones** de TEST. Destacar las subestimaciones y las predicciones `≤ 0` ante excursiones.
2. Investigar la definición exacta del flag precomputado y resolver o documentar los **7 desacuerdos**. Mantener separados los dos objetivos aunque resulten casi coincidentes.
3. Revisar la cobertura de Producto y Flota y describir a qué viajes y lecturas se aplican los resultados. No presentar el 65,90 % elegible como si fuera toda la operación.
4. Definir, con criterio operativo, qué error en °C y qué tasa de omisiones serían tolerables antes de proponer una intervención. Si se prueban nuevos predictores o ajustes, hacer la comparación en validación y reservar un TEST nuevo para la evaluación final cuando sea posible.

### Preparación del Contrato 2

1. Confirmar la semántica del horizonte y del flag; describir qué se conoce exactamente en el momento de la lectura.
2. Establecer `X/y`, reglas de elegibilidad, tratamiento de nulos y exclusiones por fuga. Conservar viajes completos al separar los bloques temporales.
3. Establecer una referencia sencilla de clasificación y evaluar después los algoritmos y métricas enseñados para ese tipo de problema. Distinguir explícitamente falsos negativos, falsas alarmas y la tasa base de 1.
4. Elegir un umbral de alerta únicamente después de relacionar esas tasas con la capacidad de intervención y los costos operativos. Evitar decidirlo con el conjunto final de prueba.

### Síntesis del proyecto

Redactar conclusiones por evidencia, sus límites de cobertura y recomendaciones proporcionadas a la evidencia disponible. Los EDA 1 y 2 aportan hallazgos descriptivos; la Evidencia 3 aporta un primer experimento cuantitativo y aún tiene pendiente la clasificación. El proyecto no requiere añadir notebooks por inercia: cada trabajo nuevo debe responder a una pregunta o resolver una limitación identificada.

## 8. Lista de control para la siguiente entrega

- [x] Bronze conservados y Silver propios preparados para las fuentes usadas.
- [x] Granularidad, claves, cardinalidad y cobertura examinadas en las tres evidencias.
- [x] EDA 1, EDA 2 y EDA 3 ejecutados e interpretados con sus límites.
- [x] Dos contratos predictivos de la Evidencia 3 diferenciados.
- [x] Contrato 1: objetivo continuo, `X/y`, partición temporal, baseline, regresores, validación y TEST ejecutados.
- [x] Contrato 1: diagnóstico del error en excursiones futuras calculado.
- [ ] Contrato 1: acordar tolerancia y criterio de utilidad operativa; investigar los 7 desacuerdos del flag.
- [ ] Contrato 2: baseline y modelo de clasificación evaluados según el contenido correspondiente del curso.
- [ ] Integrar hallazgos, limitaciones y recomendaciones finales de las tres evidencias.

## 9. Referencias internas del proyecto

- `documentacion/01_Definición del proyecto — AndinaLog 03B.md`: mandato y tres evidencias.
- `documentacion/02_Guía de trabajo — Proyecto Integrador AndinaLog 03B.md`: guía anterior de fases y tratamiento de datos.
- `documentacion/GIAD-M3_Guia_Estudiantes_Contratos_Predictivos_v8.md`: dos contratos del subcaso 03B y método de decisión, unidad, horizonte, `y` y `X`.
- `documentacion/03_Tablas_Relaciones_Joins_Seis_Subcasos_v8.md`: granularidades, claves y orden temporal de las integraciones.
- Los cuatro notebooks del apartado **Rutas de los trabajos existentes**: ejecución y resultados observados.

> **Principio de trabajo:** problema industrial → calidad y Silver → integración → EDA por evidencia → contratos predictivos de la Evidencia 3 → evaluación temporal → interpretación → recomendaciones justificadas.
