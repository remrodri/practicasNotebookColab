# Matriz de trazabilidad — contrato de la red

**Grupo:** 06  
**Caso:** AndinaLog  
**Subcaso:** 03B — Operaciones y Planificación de Datos  
**Objetivo:** anticipar una desviación térmica durante los próximos 60 minutos.

| Campo | Decisión del equipo | Evidencia |
|---|---|---|
| **Problema y horizonte** | Se plantea una **clasificación binaria** para estimar si una lectura que todavía no presenta desviación térmica tendrá una desviación durante los próximos **60 minutos**. La probabilidad generada se utilizará como alerta preventiva con revisión humana. | `desviacion_proximos_60min_flag` será la variable objetivo. La población inicial contiene **27.617 lecturas**, **1.200 viajes** y **769 casos positivos futuros**, equivalentes al **2,78 %**. Se utilizan filas con `apta_objetivo_60min = True`, `en_cuarentena_final = False` y `desviacion_termica_flag = 0`. |
| **Split** | La separación será **temporal y por viajes completos**: 60 % para entrenamiento, 20 % para validación y 20 % para prueba. Los viajes se ordenarán por su fecha de inicio y ningún `viaje_id` podrá aparecer en más de un conjunto. Se utilizará la semilla 42 en las operaciones que requieran aleatoriedad. | El Notebook 10 mostrará una tabla con cantidad de filas, viajes, intervalo de fechas y tasa positiva por conjunto. También comprobará que las intersecciones de `viaje_id` entre train, validation y test estén vacías y registrará la semilla utilizada. |
| **Arquitectura mínima** | El procesamiento incluirá variables numéricas y categóricas. La red propuesta será: **entrada → Dense(32, ReLU, L2) → Dropout(0,20) → Dense(16, ReLU, L2) → Dense(1, sigmoid)**. | El Notebook 10 mostrará `model.summary()`, el número de variables resultantes después del preprocesamiento y la secuencia de capas, parámetros y salida del modelo. |
| **Control** | Se utilizará regularización **L2 = 0,001**, `Dropout = 0,20` y `EarlyStopping` sobre `val_loss`, con `patience = 8` y `restore_best_weights = True`. Los transformadores del preprocesamiento se ajustarán exclusivamente con train. | Se conservarán la configuración del modelo y del callback, las curvas de pérdida de train y validation, la mejor época y la comprobación de que el escalador y el codificador fueron ajustados únicamente con entrenamiento. |
| **Baseline y métrica** | La MLP se comparará con `DummyClassifier` y una regresión logística con ponderación de clases. El modelo y el umbral se elegirán usando solamente validation. Se empleará un costo provisional **FN:FP = 10:1**, junto con recall y PR-AUC. La accuracy será secundaria debido al desbalance. | El Notebook 10 generará una tabla comparativa con modelo, umbral, precision, recall, F1, PR-AUC, FP, FN y costo. También mostrará la curva de costo según el umbral. El costo 10:1 se documentará como supuesto didáctico pendiente de validación operativa. |
| **Test final** | El conjunto de test se abrirá **una sola vez**, después de congelar la población, las variables, el preprocesamiento, la arquitectura, el modelo y el umbral. No se reajustará el modelo después de observar sus resultados. | Se registrarán la fecha de ejecución, la matriz de confusión, precision, recall, F1, PR-AUC, FP, FN y costo final. También se compararán los resultados de validation y test. Responsable: **Equipo 06**. |

## Fuentes de la decisión

- `andinalog_iot_telemetry_didactico_v2_silver.csv`.
- Silver de productos, flota y WMS Orders para los cruces y variables de contexto.
- Notebook de práctica `GIAD_M3_S10_Laboratorio_3_Interpretacion_completado.ipynb`.
- Documentación del subcaso 03B de AndinaLog.

## Regla de cierre

La evidencia con métricas reales se completará al ejecutar el Notebook 10 definitivo. El modelo y el umbral se seleccionarán con validation y deberán permanecer congelados antes de abrir test.
