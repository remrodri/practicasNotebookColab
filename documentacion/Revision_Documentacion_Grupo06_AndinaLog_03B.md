# Revisión de documentación y plan metodológico

## Grupo 06 — AndinaLog — Subcaso 03B

**Fecha de actualización:** 2026-09-23  
**Rol:** Operaciones y Planificación de Datos

## 1. Mandato del subcaso

El proyecto debe apoyar decisiones para proteger la cadena de frío, mejorar la rotación del inventario y anticipar desviaciones térmicas durante el transporte.

El mandato se divide en tres evidencias conectadas:

1. Analizar excursiones térmicas por viaje, producto, camión y categoría logística.
2. Priorizar lotes con riesgo de vencimiento o merma y contextualizar la rotación y los costos por centro.
3. Alertar si puede producirse una desviación térmica durante los próximos 60 minutos.

Los análisis permiten identificar asociaciones, prioridades y señales de alerta. No demuestran causalidad por sí solos.

## 2. Fuentes asignadas y alcance actual

La documentación general asigna nueve fuentes al subcaso 03B.

| Fuente | Granularidad | Estado actual | Uso en el proyecto |
|---|---|---|---|
| `andinalog_iot_telemetry.csv` | Una lectura temporal de un viaje | Diagnóstico y tratamiento completados | Fuente principal de las evidencias térmicas y de los modelos |
| `andinalog_productos.csv` | Un producto | Diagnóstico y tratamiento completados | Categoría, temperatura requerida y tolerancia |
| `andinalog_inventory_tracking.csv` | Un movimiento de lote | Diagnóstico y tratamiento completados | Vencimiento, permanencia, saldo y merma |
| `andinalog_flota.csv` | Un camión | Diagnóstico y tratamiento completados | Tipo, capacidad y centro base |
| `andinalog_wms_orders.csv` | Una orden despachada | Diagnóstico y tratamiento completados | Pedido, producto, camión, centro y atributos disponibles antes del transporte |
| `andinalog_warehouse_costs.csv` | Un centro y periodo | Diagnóstico y tratamiento completados | Rotación, pérdidas por merma y costos del centro |
| `andinalog_flota_eventos.json` | Un evento de flota | Fuera del alcance actual | Podría aportar eventos anteriores, pero no se procesará en esta etapa |
| `andinalog_bitacora_choferes.txt` | Una observación de turno | Fuera del alcance actual | Contexto semiestructurado no utilizado en esta etapa |
| `andinalog_hr_drivers.csv` | Un registro de chofer y centro | Fuera del alcance actual | No es indispensable para los modelos térmicos; presenta distinta granularidad y datos personales |

El alcance analítico actual utiliza los seis CSV con Capa Silver. La exclusión de JSON, TXT y HR Drivers debe declararse como una limitación del proyecto. No se afirmará que se analizaron nueve fuentes.

`client_satisfaction`, `commercial_margins` y `clientes` corresponden al rol 03A y no forman parte del alcance 03B.

## 3. Criterios metodológicos aprendidos en S3–S10

| Sesión | Aplicación al proyecto |
|---|---|
| S3 — EDA | Inspección, estadísticas robustas, gráficos interpretables, reglas de dominio y candidatos a revisión sin eliminación automática |
| S4 — Transformación | Arquitectura Bronze → Trabajo → Silver/Cuarentena, banderas, configuración explícita y pruebas de conservación |
| S5 — Calidad | Interpretación de problemas, imputación justificada, trazabilidad, atípicos plausibles y minimización de datos personales |
| S6 — Regresión | Contrato predictivo continuo, partición temporal, `DummyRegressor`, modelos comparables, MAE/RMSE/R² y residuos |
| S7–S8 — Clasificación | Fuga de información, pipeline, clase minoritaria, baseline, recall, costo de errores y sensibilidad al umbral |
| S9 — MLP inicial | Corte train/validation/test antes del preprocesamiento, MLP pequeña, curvas y test sellado |
| S10 — Interpretación | Regularización L2, Dropout, EarlyStopping, selección con validation y apertura única de test |

## 4. Manejo temporal acordado

- Una fecha sin zona horaria explícita se interpreta como **hora de Bolivia (`America/La_Paz`)**.
- Una fecha se tratará como UTC únicamente cuando la fuente declare UTC o incluya una zona explícita.
- `timestamp_bolivia_tratado` será la referencia temporal principal de la telemetría.
- Las fechas calendario y los periodos mensuales no requieren conversión de zona horaria.
- Toda serie temporal se ordenará por `viaje_id` y tiempo antes de usar `shift`, `rolling` o construir objetivos futuros.

El Notebook S9 de práctica debe adaptarse: no se interpretará automáticamente el campo local como UTC.

## 5. Flujo de trabajo acordado

### Etapa 1 — Auditoría de entrada de los Silver

Se cargarán los seis Silver y se comprobará:

- existencia y dimensiones;
- columnas requeridas;
- claves y unicidad;
- nulos críticos;
- filas de cuarentena final;
- imputaciones y correcciones;
- tipos numéricos y temporales;
- fechas en hora de Bolivia;
- conciliación entre diagnóstico, Silver y cuarentena.

Esta auditoría verifica aptitud para integrar. No repite el diagnóstico completo.

### Etapa 2 — EDA básico por fuente

El EDA por CSV será breve porque la calidad detallada ya fue analizada.

- **IoT:** temperatura, humedad, frecuencia, lecturas por viaje, desviaciones e imputaciones.
- **Productos:** categorías, temperatura requerida, tolerancia, precio y costo.
- **Flota:** tipo de camión, capacidad y centro base.
- **WMS Orders:** cantidades, tiempos, OTIF, centro y correcciones.
- **Inventory Tracking:** días almacenados, vencimiento, lotes sin salida y merma.
- **Warehouse Costs:** rotación, pérdidas por merma y costo mensual por centro.

### Etapa 3 — Contrato de integración

Antes de cada join se declarará:

- unidad de observación;
- clave;
- cardinalidad esperada;
- tipo de unión;
- columnas aportadas;
- cobertura;
- filas antes y después;
- tratamiento de registros sin contraparte;
- riesgo de multiplicación.

Se utilizará `left` cuando deba conservarse la población principal. Las tablas de hechos se agregarán antes de unirse con otras tablas de hechos.

## 6. Evidencia 1 — Excursiones térmicas

### Unidad

Una fila representa un viaje.

### Construcción

1. Partir de IoT Silver por lectura.
2. Agregar por `viaje_id`, `order_id`, `camion_id` y `producto_id`.
3. Unir Productos por `producto_id` con cardinalidad muchos a uno.
4. Unir Flota por `camion_id` con cardinalidad muchos a uno.

### Resultados mínimos

- temperatura promedio de cabina por viaje;
- número total de lecturas;
- número de lecturas con desviación;
- indicador de viaje con al menos una desviación;
- porcentaje de viajes con desviación por categoría logística y tipo de camión.

El porcentaje debe calcularse con viajes como denominador, no con lecturas.

### Salida

`andinalog_03b_evidencia_1_viajes.csv`

## 7. Evidencia 2 — Vencimiento, merma, rotación y costos

### Unidad

Una fila representa un lote o movimiento de lote. El resumen complementario representa un centro y periodo.

### Construcción

1. Partir de Inventory Tracking Silver.
2. Unir Productos por `producto_id`.
3. Calcular permanencia, días para vencer, estado en almacén, saldo y merma.
4. Agregar los indicadores necesarios por centro y periodo.
5. Unir Warehouse Costs por `centro_distribucion + periodo_mes`.

### Reglas

- `fecha_salida` vacía significa que el lote continúa en almacén.
- Una fecha de vencimiento imputada debe conservar su bandera y no presentarse como fecha confirmada.
- Las pérdidas contables de Warehouse Costs no se reemplazarán con estimaciones calculadas desde Inventory Tracking.

### Resultados mínimos

- días en almacén y días para vencer por lote;
- lotes aún almacenados;
- merma por categoría logística;
- riesgo de vencimiento por categoría y centro;
- rotación, pérdidas monetarias y costos por centro.

### Salidas

- `andinalog_03b_evidencia_2_lotes.csv`
- `andinalog_03b_evidencia_2_centros.csv`

## 8. Evidencia 3 — Alerta térmica a 60 minutos

### Unidad

Una fila representa una lectura IoT de un viaje en un instante.

### Construcción

1. Partir de IoT Silver.
2. Unir Productos por `producto_id`.
3. Unir Flota por `camion_id`.
4. Unir WMS Orders por `order_id`.
5. Ordenar por `viaje_id` y `timestamp_bolivia_tratado`.
6. Calcular variables históricas dentro del mismo viaje.
7. Construir los objetivos futuros dentro de los siguientes 60 minutos.

### Variables mínimas

- temperatura y humedad actuales;
- temperatura requerida y tolerancia;
- desvío actual respecto al límite;
- temperatura rezagada;
- cambio y pendiente entre lecturas;
- estadísticas históricas disponibles hasta el instante actual;
- minutos desde el inicio del viaje;
- categoría logística y tipo de camión;
- atributos del pedido disponibles antes del instante de predicción;
- banderas de imputación relevantes.

### Exclusiones

- variables objetivo dentro de `X`;
- datos posteriores a la lectura;
- cantidad entregada, tiempo real y OTIF como predictores de una alerta durante el viaje;
- identificadores usados como valores numéricos continuos;
- agregados calculados con lecturas futuras.

### Salida

`andinalog_03b_evidencia_3_lecturas.csv`

## 9. EDA integrado

Después de construir las evidencias se realizará el análisis principal del proyecto:

- excursiones por viaje, categoría y tipo de camión;
- vencimiento, merma, rotación y costo;
- cobertura y registros sin contraparte en los joins;
- frecuencia y separación temporal de lecturas;
- distribución y desbalance de los objetivos;
- relación entre temperatura actual, rezagos, pendiente y respuesta futura;
- atípicos operativos plausibles;
- limitaciones de cobertura, temporalidad y causalidad.

Los gráficos deben tener una pregunta, título, unidades e interpretación. Un patrón visual no se presentará como relación causal.

## 10. Dataset predictivo

La Evidencia 3 será la base del modelado. Se generarán:

- `andinalog_03b_dataset_analitico.csv`: variables, objetivos, identificadores y trazabilidad;
- `andinalog_03b_modelo_regresion.csv`: predictores aprobados y objetivo continuo;
- `andinalog_03b_modelo_clasificacion.csv`: predictores aprobados y objetivo binario;
- `andinalog_03b_reporte_integracion.csv`: conteos, cobertura y controles de joins.

## 11. Contrato predictivo de regresión

- **Decisión:** anticipar la magnitud de la desviación para priorizar una intercepción o revisión.
- **Unidad:** una lectura IoT.
- **Horizonte:** próximos 60 minutos.
- **Objetivo:** `max_desvio_termico_proximos_60min_c`.
- **Definición:** máximo futuro dentro del viaje de:

```text
abs(temperatura_cabina_c - temperatura_requerida_c) - tolerancia_c
```

- **Baseline:** `DummyRegressor`.
- **Modelos candidatos:** regresión lineal y al menos un regresor no lineal.
- **Métricas:** MAE, MSE, RMSE y R².
- **Diagnóstico:** residuos, errores extremos, estabilidad y tolerancia operativa.

## 12. Contrato predictivo de clasificación

- **Decisión:** alertar si el camión superará el umbral durante la próxima hora.
- **Unidad:** una lectura IoT.
- **Horizonte:** próximos 60 minutos.
- **Objetivo:** `desviacion_proximos_60min_flag`.
- **Baseline mínimo:** `DummyClassifier`.
- **Baseline clásico:** regresión logística balanceada.
- **Modelo candidato:** MLP regularizada.
- **Métricas:** recall, precision, F1, PR-AUC, FP, FN y costo.
- **Umbral:** elegido exclusivamente con validation según costo y capacidad operativa.

`desviacion_termica_flag` representa el estado actual. Para mantener coherencia con el Notebook S9 se excluirá del conjunto principal de predictores. Podrá analizarse en un escenario secundario si se demuestra que está disponible en tiempo real y que no incorpora información futura.

No se eliminarán automáticamente todas las lecturas con desviación actual. El subconjunto sin desviación actual podrá presentarse como análisis adicional de anticipación estricta.

## 13. Partición y prevención de fuga

La separación será temporal y por viajes completos:

- 60 % train;
- 20 % validation;
- 20 % test.

Los viajes se ordenarán por su fecha de inicio. Ningún `viaje_id` aparecerá en más de un conjunto.

Reglas:

- imputadores, codificadores y escaladores se ajustan solo con train;
- validation selecciona modelo, hiperparámetros y umbral;
- test permanece sellado hasta congelar todas las decisiones;
- test se abre una sola vez y no se usa para reajustar;
- la semilla se registra para operaciones reproducibles, sin confundirla con validez externa.

## 14. Arquitectura y control de la MLP

Arquitectura inicial propuesta:

```text
entrada
→ Dense(32, ReLU, L2)
→ Dropout(0,20)
→ Dense(16, ReLU, L2)
→ Dense(1, sigmoid)
```

Control inicial:

- L2 = 0,001;
- Dropout = 0,20;
- Adam;
- binary crossentropy;
- EarlyStopping sobre `val_loss`;
- `patience = 8`;
- `restore_best_weights = True`;
- semilla 42.

La arquitectura es una hipótesis inicial y debe justificar su complejidad frente a los modelos clásicos.

## 15. Estado actualizado del proyecto

Conteos Silver verificados:

| Fuente | Filas Silver |
|---|---:|
| IoT Telemetry | 28.677 |
| Productos | 60 |
| Inventory Tracking | 5.980 |
| Flota | 30 |
| WMS Orders | 7.468 |
| Warehouse Costs | 5 |

El diagnóstico y tratamiento de las seis fuentes están completados. El siguiente bloque de trabajo es la auditoría de entrada y el EDA básico, seguido por la construcción y análisis de las tres evidencias.

## 16. Entregables actualizados

1. Notebooks de diagnóstico y tratamiento de las seis fuentes.
2. Notebook único de auditoría, integración y EDA.
3. Tres tablas de evidencia y reporte de integración.
4. Dataset predictivo con contratos de regresión y clasificación.
5. Notebook de regresión con baseline, comparación y residuos.
6. Notebook de clasificación clásica y MLP con validation y test sellado.
7. Matrices de trazabilidad para regresión y clasificación.
8. Excel actualizado con inventario, diccionario y muestra del dataset integrado.
9. Informe técnico final, máximo seis páginas, con declaración de uso de IA.
10. Presentación de máximo ocho diapositivas para diez minutos.
11. Plan de correcciones, si corresponde.

## 17. Secuencia inmediata

1. Auditar los seis Silver.
2. Ejecutar EDA básico por fuente.
3. Definir y validar el contrato de cada join.
4. Construir las tres evidencias.
5. Ejecutar el EDA integrado.
6. Construir los datasets predictivos.
7. Desarrollar regresión y clasificación clásica.
8. Entrenar y comparar la MLP.
9. Seleccionar modelo y umbral con validation.
10. Abrir test una sola vez.
11. Actualizar trazabilidad, informe y presentación.

## 18. Decisión práctica

El trabajo de diagnóstico y tratamiento constituye una base válida. El siguiente paso no es entrenar directamente un modelo: primero debe construirse un notebook reproducible de **Auditoría, Integración y EDA**, con controles de granularidad, cobertura y multiplicación de filas. Sus salidas serán la evidencia para definir definitivamente las variables de los dos contratos predictivos.
