# Contrato 03B - Cumplimiento de Variables Objetivo y Predictoras Minima

Este documento mapea cada cláusula del documento oficial del docente
`documentacion/GIAD-M3_Variables_Objetivo_y_Predictoras_Minima.md` (SHA-256
`68a58984240ce88cf3eaef556c0b5899eff2b73dd16e4ae233e68b9169998af7`, copia verificada del
original) hacia la evidencia concreta de cada entregable de 03B. Sirve como contrato para
los notebooks nuevos y como trazabilidad para la defensa.

Grupo 06 · AndinaLog · Subcaso 03B · alerta térmica en los próximos 60 minutos.

## 1. Encabezado del documento oficial

| Cláusula oficial | Valor exigido | Evidencia | Estado |
|---|---|---|---|
| Caso | 03B AndinaLog | Todas las rutas de entrega de V2 son de 03B | Cumple |
| Modelo | Regresión logística | `MOD_01_AndinaLog_Regresion_Logistica.ipynb` celda 19: `LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=2000, random_state=20260925, class_weight='balanced')` dentro de un `Pipeline` | Cumple |
| Variable objetivo | `desviacion_proximos_60min_flag` | Misma celda 2 (`config['mapeo_columnas']['objetivo']`); no se reconstruye el objetivo en ninguna etapa | Cumple |
| Archivos utilizados | 1 CSV | `andinalog_iot_telemetry.csv` (Bronze) → Silver → Gold, sin uniones: `Informe_S2G_01_IoT_Gold.md` declara "Entrada unica" y "No se realizo ningun join" | Cumple |

## 2. Variables predictoras mínimas: mapeo de conceptos a nombres reales

El documento oficial nombra conceptos; Gold y los notebooks usan nombres reales. El mapeo vive
en `config['predictores_minimos']` de cada notebook y se imprime en su salida.

| Concepto oficial | Columna real | Tipo y unidad | Disponible en t | Evidencia |
|---|---|---|---|---|
| temperatura actual | `temperatura_cabina_c` | float64, Celsius | sí, instante t | `MOD_01` celda 2 (config) y celda 10 (tabla de roles: rol predictor) |
| humedad actual | `humedad_cabina_pct` | float64, % HR | sí, instante t | Ídem |
| desviacion_termica_flag | `desviacion_termica_flag` | int64, indicador 0/1 | sí, instante t | Ídem; se conserva sin escalar (`passthrough` en `MOD_01` celda 19) |
| temperatura de la lectura anterior | `temperatura_anterior` | float64, Celsius | sí, `ts_temperatura_anterior <= t` | `MOD_01` celda 40, control "Antecedentes temporales nunca posteriores al instante de prediccion" |
| variación de temperatura durante los últimos 30 minutos | `variacion_temperatura_30min` | float64, Celsius por 30 min | sí, `ts_base_variacion` en `[t-45, t-30]` | Ídem |

Las cinco se usan en el EDA (`EDA_01` celda 24, revisión individual de los cinco predictores
mínimos) y en el modelo (`MOD_01` celda 19, `ColumnTransformer` con las cuatro continuas y
`desviacion_termica_flag` en `passthrough`).

Indicadores adicionales del modelo, que no sustituyen a las cinco mínimas:
`sin_historial_temp_anterior` y `sin_historial_var30`, que codifican ausencia estructural de
historia declarada en Gold (`motivo_temperatura_anterior`, `motivo_variacion_30min`).

## 3. Unidad de observación

| Cláusula oficial | Evidencia | Estado |
|---|---|---|
| Una lectura de telemetría | `MOD_01` celda 6 y `EDA_01` celda 5: "Una fila = una lectura de telemetria en el instante `timestamp` de un viaje"; clave de lectura `viaje_id` + `timestamp`; `Informe_MOD_01` sección "Unidad de observacion" | Cumple |

## 4. Prohibición de usar lecturas o eventos posteriores al instante de predicción

| Cláusula oficial | Evidencia | Estado |
|---|---|---|
| No utilizar lecturas o eventos posteriores al instante de predicción | Las ventanas de `temperatura_anterior` y `variacion_temperatura_30min` se resuelven dentro de `viaje_id` con instantes no posteriores a `t`; el objetivo se define sobre el intervalo estricto `(t, t+60]`, por lo que la desviación del instante `t` no cuenta como evento futuro. Controles: `MOD_01` celda 40 (antecedentes no posteriores, objetivo ausente de X, sin variables posteriores a t) y `EDA_01` celda 16. Definición documentada en `Informe_S2G_01_IoT_Gold.md`, sección "Definición exacta del objetivo": "La desviación del instante t no se incluye como evento futuro: el intervalo evaluado es `(t, t+60]` de forma estricta" | Cumple |

## 5. Separación de entrenamiento y prueba por viaje u orden

| Cláusula oficial | Evidencia | Estado |
|---|---|---|
| La separación debe hacerse por viaje u orden, para evitar que lecturas consecutivas del mismo viaje queden en ambos conjuntos | `MOD_01` celda 17: `GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=20260925)` con `viaje_id` como grupo; 960 viajes de entrenamiento y 240 de prueba, intersección de grupos igual a 0, ambas clases en ambas particiones. No existe `train_test_split` en el notebook | Cumple |

## 6. EDA común para los seis casos: chequeos automáticos antes de graficar

| # | Chequeo oficial | Evidencia en `EDA_01_AndinaLog_IoT_Gold.ipynb` | Estado |
|---|---|---|---|
| 1 | Número de filas y columnas | Celda 7: forma Gold y rol declarado por columna | Cumple |
| 2 | Unidad de observación | Celda 5: clave de lectura, unicidad y viajes | Cumple |
| 3 | Duplicados y valores faltantes | Celdas 9 y 10: faltantes por columna con porcentaje, y duplicados exactos, en clave de lectura y en identificador | Cumple |
| 4 | Tipos de datos | Celda 8: tipos declarados columna por columna | Cumple |
| 5 | Estadísticas descriptivas | Celda 12: descriptivas de variables numéricas sin identificadores | Cumple |
| 6 | Verificación de que los cruces no multiplicaron registros | Celdas 15 y sección "Control de granularidad": contraste de filas leídas contra Silver y Gold declarados, con 0 diferencias | Cumple |

## 7. Gráficos obligatorios del EDA

| Gráfico oficial | Variables oficiales | Evidencia en `EDA_01` | Pregunta que responde |
|---|---|---|---|
| Countplot | objetivo | Celda 31, gráfico 1 | ¿Qué tan poco frecuentes son las desviaciones futuras? |
| Histplot | temperatura actual con hue del objetivo | Celda 32, gráfico 2 | ¿Las futuras desviaciones parten de temperaturas diferentes? |
| Boxplot | humedad actual por clase | Celda 33, gráfico 3 | ¿La humedad cambia antes de una desviación? |
| Barplot | desviación actual vs promedio del objetivo | Celda 34, gráfico 4 | ¿Una desviación presente anticipa otra en la siguiente hora? |
| Scatterplot | temperatura actual vs variación de 30 minutos, con hue | Celda 35, gráfico 5 | ¿La combinación de nivel y tendencia permite reconocer el riesgo? |
| Lineplot (opcional) | temperatura en el tiempo para dos o tres viajes, marcando la desviación futura | Celda 37, gráfico temporal opcional | Muestra que el modelo no solo mira el nivel sino también la evolución |

Los seis gráficos están embebidos, con título, ejes con unidad, leyenda y anotaciones.

## 8. Interpretaciones esperadas

| Interpretación oficial | Evidencia | Estado |
|---|---|---|
| Fuerte desbalance de clases | `EDA_01` celda 22 y sección "Desbalance de clases": prevalencia 0.050433 y razón mayoria/minoria 18.8285; 338 de 1200 viajes con alguna ventana positiva | Cumple |
| Temperatura y humedad previas a los eventos | `EDA_01` celda 25, estadísticas por clase, y gráficos 2 y 3 | Cumple |
| Importancia de la tendencia | `EDA_01` celda 27 y gráfico 5: la clase 1 se concentra en variaciones positivas | Cumple |
| Diferencia entre desviación actual y futura | `EDA_01` gráfico 4 y `Informe_MOD_01` sección "Interpretación de coeficientes": el objetivo usa `(t, t+60]` y la desviación actual es un predictor con odds ratio de 39.19 | Cumple |

## 9. Decisiones que exceden el mínimo oficial y quedan declaradas

1. La etiqueta exige cobertura observada de al menos 45 de los 60 minutos; las 2671 lecturas sin
   cobertura quedan fuera del análisis del objetivo y nunca se rellenan con cero.
2. Los nulos de historia se codifican con un valor neutro más un indicador, y los 87 faltantes
   residuales de humedad se imputan con mediana ajustada solo con entrenamiento dentro del
   `Pipeline`.
3. La comparación entre `class_weight='balanced'` y la variante sin ponderar se resuelve con
   validación cruzada por grupos dentro de entrenamiento, nunca con el conjunto de prueba.
4. Las probabilidades del modelo balanceado no están calibradas y se interpretan como puntaje
   de priorización.

## 10. Regla para los notebooks nuevos

1. Declarar en la primera celda de configuración el objetivo, la unidad de observación, la clave
   de grupo y el mapeo de las cinco predictoras mínimas a los nombres reales.
2. Filtrar por la bandera de cobertura y por el objetivo explícitamente, sin `dropna()`.
3. Separar por grupo con semilla fija y demostrar que la intersección de grupos es vacía.
4. Ajustar imputación y escalado solo con entrenamiento dentro de un `Pipeline`.
5. Evaluar el conjunto de prueba una sola vez, con matriz de confusión, precision, recall, F1,
   ROC AUC, PR AUC, prevalencia y línea base.
6. No afirmar causalidad ni presentar probabilidades no calibradas como riesgo absoluto.
