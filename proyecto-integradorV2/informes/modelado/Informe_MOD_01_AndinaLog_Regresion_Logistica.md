# Informe MOD 01 - AndinaLog IoT Regresion Logistica

## Problema predictivo

Estimar la probabilidad de que una lectura de telemetria de cabina registre una
**desviacion termica durante los proximos 60 minutos**, a partir de la informacion
disponible en el instante de prediccion. El modelo es una **regresion logistica**,
que es el modelo obligatorio de 03B, y su salida es una probabilidad que permite
ordenar ventanas de lectura por riesgo.

La etiqueta describe una asociacion temporal: que en la hora siguiente a la lectura
exista al menos una desviacion observada dentro del mismo viaje. No afirma causalidad
y no se usa para sancionar conductores.

## Unidad de observacion

Una lectura de telemetria con ventana futura evaluable. Cada fila es un instante
`timestamp` dentro de un viaje. La clave de lectura es `viaje_id` + `timestamp` y la
clave de agrupacion del modelado es `viaje_id`.

## Fuente Gold

- Entrada unica: `datos/gold/andinalog_iot_modelado_gold.csv`, leido en modo solo lectura.
- SHA-256 al inicio y al cierre de la ejecucion:
  `f0194aae8dfe9073fd0e5bbf14cb72353a02863915e483ceec66027e81406479`, identico en ambos
  momentos. El modelo **no modifica Gold**.
- Forma: 28448 filas y 20 columnas; 1200 viajes, 1200 ordenes, un orden por viaje.
- Rango temporal UTC: 2026-08-01 04:10 a 2026-08-31 15:11.
- El Gold fue producido por `notebooks/silver_gold/01_iot_gold/S2G_01_AndinaLog_IoT_Gold.ipynb`.
  No se reconstruyo el objetivo ni ninguna columna derivada.
- No se unieron otras fuentes: el alcance minimo de 03B no las requiere.

## Variable objetivo

`desviacion_proximos_60min_flag`. Se modela unicamente donde
`ventana_objetivo_evaluable == True`, es decir donde Gold observo la ventana futura
`(t, t+60]` dentro del mismo viaje. Dentro de esa poblacion el objetivo contiene solo
0 y 1. La desviacion del instante t no se cuenta como evento futuro.

## Predictores y mapeo con los nombres reales de Gold

Los conceptos del prompt se adaptaron a las columnas reales mediante el diccionario
`config['predictores_minimos']` del notebook:

| Concepto del prompt | Columna real en Gold | Tipo | Unidad | Disponible en t |
|---|---|---|---|---|
| Temperatura actual | `temperatura_cabina_c` | float64 | Celsius | si, instante t |
| Humedad actual | `humedad_cabina_pct` | float64 | % HR | si, instante t |
| Desviacion termica actual | `desviacion_termica_flag` | int64 | indicador 0/1 | si, instante t |
| Temperatura de la lectura anterior | `temperatura_anterior` | float64 | Celsius | si, `ts_temperatura_anterior <= t` |
| Variacion de temperatura 30 min | `variacion_temperatura_30min` | float64 | Celsius por 30 min | si, `ts_base_variacion` en `[t-45, t-30]` |

Ademas entran dos indicadores de ausencia de historia, creados en memoria por la
decision aprobada A: `sin_historial_temp_anterior` y `sin_historial_var30`. El modelo
usa 7 columnas: 5 predictores minimos y 2 indicadores.

No se uso ningun otro campo. `producto_id`, `camion_id`, `order_id` y `_fila_bronze`
son identificadores y quedan fuera aunque `producto_id` se asocie a la prevalencia
por regimen termico; `timestamp` no entra como variable, solo como referencia de
verificacion; `ts_temperatura_anterior`, `ts_base_variacion`,
`ventana_objetivo_evaluable`, `motivo_temperatura_anterior`, `motivo_variacion_30min`,
`objetivo_coincide_con_silver`, `calidad_estado` y `calidad_motivo` son controles o
auditoria y quedan fuera.

## Poblacion utilizada y exclusiones

| Paso | Filas que entran | Filas excluidas | Motivo |
|---|---|---|---|
| Filas totales de Gold | 28448 | - | - |
| `ventana_objetivo_evaluable == True` | 25777 | 2671 | la ventana futura de 60 min no fue observada dentro del viaje; `calidad_motivo = sin_cobertura_futura_hasta_60min_en_la_entidad` |
| Objetivo no nulo | 25777 | 0 | sin exclusions adicionales |
| Objetivo en {0, 1} | 25777 | 0 | sin exclusions adicionales |
| Clave de viaje no nula | 25777 | 0 | sin exclusions adicionales |
| **Poblacion de modelado** | **25777** | **2671** | conciliacion 25777 + 2671 = 28448 |

La seleccion es explicita y en cascada; no se uso `dropna()`. Las 2671 exclusiones
corresponden a las ultimas lecturas de cada viaje, cuyo objetivo es nulo por
construccion y nunca se rellena con cero. No son comparables con las evaluables.

Sobre la poblacion de modelado: 1200 viajes, 24477 ventanas negativas y 1300 positivas,
prevalencia **0.050433** y razon mayoria/minoria **18.83 a 1**. Hay 338 viajes con al
menos una ventana positiva y 862 sin ninguna. Cada viaje aporta entre 16 y 22 ventanas
evaluables, con mediana 22.

## Tratamiento de faltantes

### Faltantes estructurales de historia (decision aprobada A)

Los nulos de `temperatura_anterior` y `variacion_temperatura_30min` no son errores de
sensor: Gold declara su causa y el notebook la verifica antes de actuar.

| Predictor | Nulos en la poblacion | Causas declaradas |
|---|---|---|
| `temperatura_anterior` | 1191 | `primera_lectura_del_viaje` 1191 |
| `variacion_temperatura_30min` | 1471 | `primera_lectura_del_viaje` 1191, `sin_lectura_en_[t-45,t-30]_minutos` 280 |

Todos los nulos tienen motivo estructural declarado y ninguno queda sin motivo, por lo
que la codificacion neutra se aplica exclusivamente a esas filas:

| Predictor | Valor original | Valor codificado | Indicador | Filas |
|---|---|---|---|---|
| `temperatura_anterior` | nula | `temperatura_cabina_c` del instante t | `sin_historial_temp_anterior` = 1 | 1191 |
| `variacion_temperatura_30min` | nula | `0.0` | `sin_historial_var30` = 1 | 1471 |

Las 1471 filas afectadas contienen 1444 clase 0 y 27 clase 1, y afectan a 1191 y 1200
viajes respectivamente. Estas codificaciones **no son mediciones observadas**: son un
valor neutro explicito mas un indicador que permite distinguirlas de un valor real. La
regla no se aplica a temperatura actual, humedad, desviacion actual, identificadores ni
a ningun otro sensor; si algun nulo tuviera otro motivo o careciera de motivo, el
notebook detiene la ejecucion con un error.

No hay informacion futura en la codificacion: usa solo la temperatura del propio instante
t, que ya es predictor del modelo, y una constante 0.0. No estima ningun parametro, no
usa estadisticos y no toca otros viajes.

### Faltantes residuales

Despues de la regla estructural solo queda un faltante: `humedad_cabina_pct` con 87
filas en 83 viajes (0.3375 %), de las cuales 82 son clase 0 y 5 clase 1. Los otros
cuatro predictores quedan completos.

Ese residuo se trata dentro del `Pipeline` con `SimpleImputer(strategy='median')`
**ajustado solo con entrenamiento**, conforme al tratamiento aprobado en el Plan. La
mediana se justifica con los datos reales **de entrenamiento**: la temperatura es bimodal
por regimen de producto, de modo que la media queda entre regimenes y la mediana es
robusta; en la variacion de 30 minutos la mediana casi nula es exactamente el valor
neutro "sin cambio". Las estadisticas descriptivas que sustentan esa justificacion se
calculan despues del split y unicamente sobre las 20621 filas de entrenamiento: no se
resume en ningun punto la poblacion completa, que incluiria el conjunto de prueba. No se
usa `ffill`, `bfill` ni informacion posterior a t, y no se imputan identificadores. El
numero de filas y variables afectadas queda registrado en la salida del notebook.

## Estrategia de split por grupo

- Metodo: `GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=20260925)`.
- Prohibido el split aleatorio por filas: cada viaje queda completo en una sola particion.

| Particion | Filas | Viajes | Clase 0 | Clase 1 | Prevalencia | Razon |
|---|---|---|---|---|---|---|
| Entrenamiento | 20621 | 960 | 19570 | 1051 | 0.050967 | 18.62 |
| Prueba | 5156 | 240 | 4907 | 249 | 0.048293 | 19.71 |
| Total | 25777 | 1200 | 24477 | 1300 | 0.050433 | 18.83 |

- Proporcion real de filas en prueba: 0.200023, frente a la configurada 0.20.
- Proporcion real de grupos en prueba: 0.20 exacto (240 de 1200 viajes).
- Interseccion de grupos entre particiones: **0**. Cada viaje esta en una sola particion
  y ninguna lectura de prueba aparece en entrenamiento (verificado con la clave
  `viaje_id` + `timestamp`).
- Ambas clases presentes en ambas particiones. La prueba contiene 240 viajes, de los
  cuales 66 tienen al menos una ventana positiva.
- El reparto se hizo una sola vez con la semilla declarada y no se buscaron semillas
  convenientes: en el Plan se verifico que otras semillas tambien conservan ambas
  clases, de modo que el resultado no depende de una semilla afortunada.

## Controles de fuga temporal

1. `ts_temperatura_anterior <= timestamp` y `ts_base_variacion <= timestamp` en toda la
   poblacion; todo antecedente presente tiene marca de tiempo y viceversa.
2. `X` contiene exactamente las 7 columnas de `config`; el objetivo, la bandera
   evaluable, los identificadores, el timestamp bruto y las columnas de control y
   auditoria estan ausentes, con interseccion vacia entre predictores y columnas no
   admisibles.
3. `Pipeline.fit(X_tr, y_tr)` se ejecuta una unica vez. La imputacion y el escalado se
   aprendieron con las 20621 filas de entrenamiento: las medianas aprendidas
   (temperatura 9.95, humedad 61.30, temperatura anterior 9.92, variacion 0.00) difieren
   de las medianas de prueba (17.63, 56.70, 17.64, 0.00), lo que demuestra que la prueba
   no participo. Esas medianas de prueba solo se imprimen como contraste.
4. Interseccion de grupos vacia entre entrenamiento y prueba, y tambien entre folds de
   la validacion cruzada, verificado con `assert` en cada fold.
5. El conjunto de prueba no participa en imputacion, escalado, seleccion de ponderacion,
   eleccion de umbral ni seleccion de modelo. Se evaluo una sola vez, con el modelo
   principal.
6. La codificacion neutral de historia no usa lecturas posteriores a t.

Sobre el orden cronologico: el split por grupo ya impide que lecturas consecutivas del
mismo viaje aparezcan en ambas particiones, y las ventanas del objetivo se resolvieron
dentro del viaje. Un split adicional por orden cronologico se evaluo en el Plan (240
viajes de prueba desde 2026-08-25, con prevalencia 0.0630) y se descarta como prueba
principal porque rompe la paridad de prevalencia entre particiones. La deriva temporal
queda como limitacion declarada: el mes unico de datos no permite medir estabilidad
estacional.

## Pipeline

```
ColumnTransformer
  continuo  : SimpleImputer(median) -> StandardScaler   # temperatura_cabina_c, humedad_cabina_pct,
                                                          # temperatura_anterior, variacion_temperatura_30min
  indicador : passthrough                                # desviacion_termica_flag,
                                                          # sin_historial_temp_anterior, sin_historial_var30
  remainder : drop
-> LogisticRegression(class_weight='balanced', penalty='l2', C=1.0, solver='lbfgs',
                      max_iter=2000, random_state=20260925)
```

- Las banderas binarias y los indicadores no se escalan, para conservar la lectura
  directa de su coeficiente.
- El preprocesamiento completo queda encapsulado en el `Pipeline` y se ajusta
  exclusivamente con entrenamiento.
- 7 features resultantes. El modelo convergio en 22 iteraciones de las 2000 disponibles.
- Nota de entorno: el solver `lbfgs` de scikit-learn 1.6.1 con SciPy 1.18.1 emite el
  aviso `OptimizeWarning: Unknown solver options: iprint`. Es un aviso de compatibilidad
  entre versiones, no un fallo de convergencia: `n_iter_` es 22 y las metricas son
  estables.

## Configuracion del modelo

Todo reside en el diccionario `config` de la primera celda del notebook: rutas, mapeo de
nombres, predictores, indicadores, proporciones, semilla, imputacion, escalado,
parametros de `LogisticRegression`, `class_weight`, `max_iter`, solver, regularizacion,
umbrales y metricas. No hay rutas ni constantes repartidas por el resto del notebook.

Parametros: `penalty='l2'`, `C=1.0`, `solver='lbfgs'`, `max_iter=2000`,
`random_state=20260925`, `class_weight='balanced'`. La regularizacion `l2` con `C=1.0`
es el punto de partida estandar y tambien frena la colinealidad entre temperatura actual
y temperatura anterior, sin necesidad de una busqueda extensa de hiperparametros.

## Criterio de seleccion del modelo

Los criterios se declararon **antes de mirar el conjunto de prueba** y se revisaron por
decision del usuario tras la auditoria del 2026-09-25, sin cambiar el modelo. Viven en
`config['sensibilidad']` del notebook y se imprimen en la celda de sensibilidad B y en la
celda de reproducibilidad.

| # | Criterio | Declaracion | Evidencia que lo sustenta |
|---|---|---|---|
| 1 | Criterio principal | Recall de la clase positiva | Recall medio en CV por grupos: `balanced` 0.455079 frente a 0.378285 sin ponderar |
| 2 | Restriccion operativa | Vigilancia de la precision y del volumen de falsas alertas | Precision media 0.287506 frente a 0.642513; alertas por fold 340.6 frente a 123.8; falsos positivos por fold 244.6 frente a 44.0 |
| 3 | Metrica global complementaria | PR AUC, no unico criterio de seleccion | PR AUC medio 0.347510 frente a 0.388929: favorece a la variante sin ponderar y se reporta como medida global de calidad del orden |
| 4 | Modelo principal | `class_weight='balanced'` | El falso negativo tiene mayor costo operativo en cadena de frio que una revision adicional: no alertar una desviacion futura cuesta mas que revisar de mas |
| 5 | Alternativa operativa | `class_weight=None` | Es la opcion si el negocio prioriza reducir falsas alertas, aceptando menos cobertura |
| 6 | Pendiente de definicion | El equilibrio definitivo precision-recall | Requiere un costo de negocio documentado o la confirmacion del docente |

Ambito de la comparacion: validacion cruzada por grupos **dentro de entrenamiento**, con
los mismos predictores, grupos y preprocesamiento. El conjunto de prueba no se uso para
comparar ni para elegir, y ninguna cifra de la entrega anterior se modifico con
resultados de prueba.

## Desbalance y ponderacion de clases

La prevalencia es 0.050433, con razon 18.83 a 1: 862 de 1200 viajes no aportan ninguna
ventana positiva y 12 de los 338 viajes positivos aportan una sola. `class_weight='balanced'`
multiplica el peso de la clase minoritaria por 18.62 en el conjunto de entrenamiento, lo
que desplaza la frontera de decision y eleva el recall a costa de precision y de un mayor
volumen de alertas.

Comparacion de sensibilidad realizada **solo con validacion cruzada por grupos dentro de
entrenamiento** (5 folds, 4124 filas por fold en promedio), con los mismos predictores,
grupos y preprocesamiento:

| Configuracion | Recall medio | Precision medio | PR AUC medio | ROC AUC medio | F1 medio | Accuracy medio | Alertas por fold | Falsos positivos por fold | Falsos negativos por fold |
|---|---|---|---|---|---|---|---|---|---|
| `class_weight='balanced'` (principal) | **0.455079** | 0.287506 | 0.347510 | 0.763956 | 0.350421 | 0.912988 | 340.6 | 244.6 | **114.2** |
| `class_weight=None` (alternativa) | 0.378285 | **0.642513** | **0.388929** | 0.764124 | 0.475831 | 0.957707 | 123.8 | 44.0 | 130.4 |

Lectura contra cada criterio declarado, sin adornos:

- **Criterio principal (recall)**: a favor de `balanced`, 0.455079 frente a 0.378285, con
  menos falsos negativos por fold (114.2 frente a 130.4). Esta es la metrica que decide.
- **Restriccion operativa (precision y volumen de alertas)**: en contra de `balanced`, que
  produce 340.6 alertas por fold frente a 123.8 y 244.6 falsos positivos frente a 44.0.
  Ese es el costo operativo aceptado de la decision.
- **Metrica global complementaria (PR AUC)**: a favor de la variante sin ponderar, 0.388929
  frente a 0.347510. Ponderar clases reordena las probabilidades y por eso degrada un area
  que es independiente del umbral, mientras mejora el recall. Por eso el PR AUC se conserva
  como medida global y no como criterio de seleccion.

**`balanced` no es superior en todas las metricas**: gana en recall y pierde en precision,
en PR AUC y en volumen de alertas. Se conserva como modelo principal por el costo
operativo del falso negativo ya declarado, y la variante sin ponderar queda como
alternativa operativa si el negocio prioriza reducir falsas alertas. El equilibrio
definitivo no lo resuelven los datos: requiere un costo de negocio o la confirmacion del
docente. El conjunto de prueba no se uso para esta eleccion.

## Sensibilidad A: variante de historia completa

Comparacion por validacion cruzada por grupos, solo dentro de entrenamiento, sin usar la
prueba. La variante restringida usa unicamente lecturas con historia completa.

| Variante | Filas | Positivos | Prevalencia | Viajes | PR AUC medio | ROC AUC medio | F1 medio | Recall medio | Precision medio |
|---|---|---|---|---|---|---|---|---|---|
| Principal (codificacion neutra + indicadores) | 20621 | 1051 | 0.050967 | 960 | 0.347510 | 0.763956 | 0.350421 | 0.455079 | 0.287506 |
| Restringida (historia completa) | 19446 | 1034 | 0.053173 | 960 | 0.347265 | 0.756182 | 0.395683 | 0.449399 | 0.359249 |

Filas, positivos y viajes afectados por la restriccion: se excluyen 1175 filas de
entrenamiento, de ellas 17 positivas (1158 negativas), y ningun viaje pierde todas sus
filas: los 960 viajes siguen representados, aunque 960 pierden al menos una lectura. La
diferencia de PR AUC es de 0.0002, es decir despreciable, mientras la precision mejora
en la variante restringida. En conclusion, **no descartar lecturas por falta de historia
no aporta capacidad predictiva y si hace perder observaciones**: la codificacion neutra
con indicadores es la opcion adecuada. Esta comparacion es de sensibilidad; la decision
ya estaba aprobada y la prueba no participó.

## Umbral de decision

- **Umbral de referencia: 0.5**, que es el valor de `config` y el resultado principal.
- Umbral secundario, calculado **sin usar la prueba**, sobre las probabilidades
  out-of-fold de la validacion cruzada dentro de entrenamiento (20621 filas, 1051
  positivos):

| Criterio | Umbral | Precision | Recall | F1 | F2 | Alertas |
|---|---|---|---|---|---|---|
| Referencia de config | 0.50 | 0.2819 | 0.4567 | 0.3486 | 0.4063 | 1703 |
| Maximo F2 out-of-fold (FN mas caro) | 0.57 | 0.5976 | 0.4196 | 0.4930 | 0.4462 | 738 |
| Maximo F1 out-of-fold (equilibrio) | 0.93 | 0.6197 | 0.4139 | 0.4963 | 0.4433 | 702 |

Costo de falsos negativos: no anticipar una desviacion que si ocurre en la hora
siguiente, con el riesgo de que la cabina llegue a destino sin revision. Costo de falsos
positivos: alerta o revision innecesaria sobre una ventana que no va a desviarse. El
umbral 0.57 reduce las alertas de 1703 a 738 y casi duplica la precision a cambio de
algo de recall. **No se afirma que ningun umbral sea optimo**: no existe una funcion de
costo documentada por el docente, y el valor que se adopte en produccion debe fijarlo
quien defina ese costo. La prueba se reservo para la evaluacion final y no se uso para
elegir ningun umbral.

## Linea base

`DummyClassifier(strategy='most_frequent')`, ajustado con el mismo entrenamiento y
evaluado sobre la misma prueba. Predice siempre 0.

## Metricas de prueba (evaluacion final unica)

Conjunto de prueba: 5156 filas, 240 viajes, 249 ventanas positivas, prevalencia 0.048293.

| Modelo | Accuracy | Precision | Recall | F1 | ROC AUC | PR AUC | TN | FP | FN | TP |
|---|---|---|---|---|---|---|---|---|---|---|
| Linea base (clase mayoritaria) | 0.951707 | 0.000000 | 0.000000 | 0.000000 | 0.500000 | 0.048293 | 4907 | 0 | 249 | 0 |
| Regresion logistica, umbral 0.5 | 0.923002 | 0.303191 | 0.457831 | 0.364800 | 0.759304 | 0.324069 | 4645 | 262 | 135 | 114 |
| Regresion logistica, umbral 0.57 (sensibilidad) | 0.956943 | 0.574586 | 0.417671 | 0.483721 | 0.759304 | 0.324069 | 4830 | 77 | 145 | 104 |

Umbral de referencia: 0.5, que es el valor de `config` y el resultado principal. La
comparacion de ponderaciones de la seccion anterior se resolvio con el criterio declarado
(recall como criterio principal), no con este umbral ni con resultados de prueba.

Que representa cada metrica y por que importa con este desbalance:

- **Matriz de confusion**: recuento directo de TN, FP, FN y TP. Es la unica que
  traduce el resultado en ventanas concretas que se alerts o se pierdan.
- **Precision**: proporcion de alertas que son desviaciones reales. Con prevalencia
  0.048, un modelo que alerte mucho puede tener precision baja aunque detecte casos.
  Baja precision significa falsos positivos.
- **Recall**: proporcion de desviaciones futuras que el modelo detecta. Es la metrica
  critica si el costo de un falso negativo es mayor. La linea base tiene recall 0.
- **F1**: media armonica de precision y recall; penaliza el equilibrio. Es la metrica
  mas util para comparar las tres filas de la tabla.
- **ROC AUC**: capacidad de separar las clases en todos los umbrales. En este problema
  es poco informativa porque la clase negativa domina; ademas es insensible a la
  prevalencia y puede verse optimista.
- **PR AUC**: area bajo la curva precision-recall. Es la metrica principal aqui, porque
  una linea base que predice siempre 0 obtiene exactamente la prevalencia; superarla es
  la mejora minima demostrable. No es calculable si la particion carece de una clase.
- **Prevalencia**: 0.048293 en prueba. Es la referencia contra la cual se lee el PR AUC.
- **Accuracy**: 0.923002 del modelo frente a 0.951707 de la base. Se reporta como
  metrica complementaria **nunca como unico criterio**: en un problema con 4.8 % de
  positivos, la base la maximiza sin detectar nada.

Mejora demostrada frente a la linea base: PR AUC 0.324069 frente a 0.048293, es decir
6.7 veces la referencia de prevalencia, con recall 0.457831 frente a 0. El modelo detecta
114 de las 249 ventanas con desviacion futura. A cambio produce 262 falsos positivos
sobre 4907 ventanas negativas, y su accuracy es menor que la de la base: ese intercambio
es proprio del desbalance y se documenta en lugar de ocultarse.

Como se leen estas metricas segun los criterios declarados: el **recall** es la metrica
operativa principal y la que sostiene la decision de ponderar clases; la **precision** y
el **volumen de falsos positivos** son la restriccion operativa que hay que vigilar, y en
este umbral estan en 0.303191 y 262 alertas sobre 5156 ventanas; el **PR AUC** es la
metrica global complementaria y por si sola no decidio el modelo. La variante
`class_weight=None` **no se evaluo sobre el conjunto de prueba**: su evidencia es
exclusivamente la validacion cruzada dentro de entrenamiento, de modo que la comparacion
entre ambas configuraciones se apoya en 20621 filas de entrenamiento y no en las 5156 de
prueba.

Validacion cruzada por grupos dentro de entrenamiento (5 folds de
`StratifiedGroupKFold`, sin viajes compartidos): PR AUC medio 0.347510 con desviacion
0.041145, ROC AUC medio 0.763956 con desviacion 0.031364, recall medio 0.455079 con
desviacion 0.043986. Cada fold contiene ambas clases y entre 51 y 59 viajes con al menos
una ventana positiva, por lo que la validacion es estable y no hay folds degenerados. La
dispersion entre folds (PR AUC entre 0.298351 y 0.395844) es la medida honesta de
incertidumbre: el resultado de prueba debe leerse dentro de ese rango.

## Matriz de confusion

Umbral 0.5: TN 4645, FP 262, FN 135, TP 114. Se escapan 135 de las 249 ventanas con
desviacion futura y se alertan 262 ventanas que no la tendran. Con el umbral 0.57: TN
4830, FP 77, FN 145, TP 104; se pierden 10 detecciones y se eliminan 185 alertas
falsas. La linea base tiene FN 249 y ningun TP.

## Interpretacion de coeficientes

| Predictor | Coeficiente (log-odds) | Odds ratio | IC 95 % del coeficiente |
|---|---|---|---|
| `desviacion_termica_flag` | 3.6683 | 39.19 | 3.5482 a 3.7885 |
| `humedad_cabina_pct` | 0.2595 | 1.30 | 0.2170 a 0.3019 |
| `temperatura_cabina_c` | 0.0289 | 1.03 | -2.6356 a 2.6935 |
| `variacion_temperatura_30min` | 0.0161 | 1.02 | -0.3723 a 0.4044 |
| `sin_historial_var30` | -0.1905 | 0.83 | -0.5380 a 0.1569 |
| `temperatura_anterior` | -0.2039 | 0.82 | -2.8677 a 2.4599 |
| `sin_historial_temp_anterior` | -1.0596 | 0.35 | -1.5410 a -0.5782 |

Lectura, con sus limites:

- La **desviacion termica ya presente** domina el modelo: su coeficiente no escalado de
  3.67 implica un odds ratio de 39.2 (IC 34.8 a 44.2) para la hora siguiente, con el
  resto de predictores constante. Es el mismo contraste que el EDA describio (0.0152
  frente a 0.4185 de proporcion del objetivo).
- **Humedad**: un aumento de una desviacion estandar (15.45 puntos porcentuales) se
  asocia a un odds ratio de 1.30, con el intervalo mas estrecho del modelo.
- **Nivel termico**: `temperatura_cabina_c` y `temperatura_anterior` son practicamente
  indistinguibles porque su correlacion es 0.9886. Sus coeficientes son pequenos y sus
  errores estandar son enormes (1.36), con intervalos que cruzan cero. No se puede
  repartir el merito entre ambas ni atribuir un efecto al nivel termico: la
  regularizacion `l2` reparte el peso de forma casi arbitraria entre variables colineales.
- **Variacion de 30 minutos**: coeficiente pequeno y con intervalo que cruza cero, a
  pesar de que la mediana de la clase 1 era 0.22 C frente a -0.03 C de la clase 0. Aporta
  poca informacion una vez controlada la desviacion actual.
- **Indicadores de ausencia**: la primera lectura del viaje tiene un odds ratio de 0.35
  respecto a tener historia, con intervalo que no cruza cero. Es un efecto de
  disponibilidad de informacion, no un efecto termico: al inicio del viaje el modelo ve
  menos señales y el riesgo estimado baja. El indicador de variacion sin historia no
  resulta significativo (intervalo que cruza cero).
- Con `class_weight='balanced'` los coeficientes están reescalados por los pesos de clase
  y no son los de un modelo de maxima verosimilitud sin ponderar: el intercepto de
  -0.554659 tampoco debe leerse como probabilidad base.

**Advertencia**: un coeficiente grande no es una importancia causal ni una palanca de
negocio. Estos valores describen asociacion ajustada dentro del modelo, sobre ventanas
de lectura de un unico mes, y no permiten afirmar que actuar sobre la temperatura o la
humedad evite una desviacion. El modelo no se usa para sancionar conductores.

**Calibracion**: `class_weight='balanced'` reescala la frontera de decision, de modo que
**las probabilidades de salida no estan calibradas**. Un valor de 0.6 no debe leerse como
un 60 % verificado de probabilidad de desviacion, sino como un puntaje de priorizacion.
Por eso el umbral se fija con validacion sobre datos de entrenamiento y no leyendo
probabilidades, y si el negocio quiere usar la salida como estimacion de riesgo debe
construirse antes una curva de fiabilidad.

## Graficos

Cinco graficos, todos con titulo, ejes con unidad, leyenda, anotaciones de metricas y
`tight_layout()`, embebidos en el notebook ejecutado:

1. Matrices de confusion de la linea base y del modelo principal, con TN, FP, FN, TP
   anotados, leyenda que explica cada region de la matriz y metricas en el titulo.
2. Curva ROC del modelo, de la linea base y del azar, con ROC AUC en la leyenda.
3. Curva Precision-Recall con la linea de prevalencia de prueba como referencia y el
   punto del umbral 0.5 marcado.
4. Comparacion tabular en barras entre linea base y regresion logistica para precision,
   recall, F1, ROC AUC, PR AUC y accuracy, con el nombre de la metrica en el eje
   horizontal y el valor impreso sobre cada barra.
5. Coeficientes en escala log-odds con intervalo de confianza al 95 %.

## Limitaciones

1. El dato es un unico mes (agosto 2026) y un unico conjunto de productos: no permite
   medir estabilidad estacional ni valida el modelo fuera de ese regimen.
2. `class_weight='balanced'` esta aprobado porque prima el costo del falso negativo, pero
   no es superior en todas las metricas: pierde en precision (0.287506 frente a 0.642513),
   en PR AUC (0.347510 frente a 0.388929) y en volumen de alertas por fold (340.6 frente a
   123.8). El equilibrio precision-recall no esta resuelto por los datos: depende de un
   costo de negocio o de la confirmacion del docente, y hasta entonces la eleccion es una
   decision operativa, no un resultado del modelo. Ademas, las probabilidades de salida
   no estan calibradas por el uso de ponderacion de clases.
3. `producto_id` explica parte de la prevalencia (3.57 %, 6.82 % y 6.16 % por regimen) y
   queda fuera por ser identificador, de modo que el modelo no captura ese matiz.
4. Temperatura actual y anterior son casi colineales: sus coeficientes no son
   interpretables individualmente y el intervalo de cualquiera de los dos es muy ancho.
5. La etiqueta exige cobertura de al menos 45 de los 60 minutos; 2671 lecturas quedan
   fuera y no son comparables.
6. La unidad es la lectura, no el viaje: un viaje con diez ventanas positivas pesa diez
   veces mas que uno con una sola, y la evaluacion operativa por viaje no se realizo.
7. La codificacion neutral de historia no es una medicion. Un despliegue en produccion
   deberia conservar el indicador y reportar por separado las primeras lecturas.
8. La ventana de 30 minutos se resuelve con una sola lectura base, porque la cadencia es
   de 30 minutos; con intervalos reales de 60 o 90 minutos la variacion queda nula.
9. La validacion cruzada muestra una dispersion de PR AUC de 0.041 entre folds; el
   resultado de prueba es un punto dentro de ese rango, no una cifra exacta.
10. El area bajo la curva ROC no es la metrica adecuada para este desbalance: se reporta
    por completitud, no como criterio.

## Recomendacion operativa prudente

El modelo es util como **priorizador de ventanas**, no como alarma. Acerca de 4.8 de cada
100 ventanas tienen desviacion futura; el modelo, en su umbral de referencia, prioriza
correctamente 114 de 249 casos reales y descarta 135. Eso permite concentrate en las
ventanas de mayor probabilidad en lugar de revisar todo el viaje, siempre que se
entienda que la lista no es exhaustiva.

Pautas prudentes:

1. Usar el recall como criterio operativo principal, la precision y el volumen de alertas
   como restriccion a vigilar, y el PR AUC como medida global complementaria. Nunca la
   accuracy, que premia a la linea base sin detectar nada.
2. Recordar que la lista priorizada **no es exhaustiva**: en el umbral de referencia quedan
   135 de 249 ventanas positivas sin alertar, de modo que un viaje puede tener una
   desviacion que el modelo no senale.
3. No fijar un umbral definitivo ni el equilibrio precision-recall sin un costo de negocio
   acordado o la confirmacion del docente. Con los datos actuales, si se prioriza no dejar
   pasar desviaciones el umbral 0.57 es preferible al 0.5 (reduce las alertas falsas de 262
   a 77 y sube la precision de 0.30 a 0.57, a cambio de 10 detecciones menos); si el
   negocio prioriza reducir falsas alertas, la alternativa operativa es
   `class_weight=None`, que en validacion cruzada reduce las alertas por fold de 340.6 a
   123.8 y sube la precision de 0.29 a 0.64, aceptando menos cobertura.
4. Tratar la salida como puntaje de priorizacion, no como probabilidad calibrada de riesgo.
5. No interpretar los coeficientes como causas ni usarlos para evaluar conductores.
6. Monitorear la prevalencia por regimen de producto antes de usar el modelo fuera del
   alcance de este mes, y recalibrar si cambia la mezcla de productos.
7. Reportar siempre por separado las lecturas de primera lectura de viaje, donde el
   modelo tiene menos informacion y subestima el riesgo.

## Reproducibilidad

- Ejecucion UTC: 2026-09-25T21:04:09.730518+00:00 (celda de reproducibilidad del
  notebook entregado).
- Interprete: `C:\Users\remrodri\Github\practicasNotebookColab\.venv\Scripts\python.exe`.
- Python 3.13.15, pandas 3.0.5, numpy 2.5.3, scikit-learn 1.6.1, seaborn 0.13.2,
  matplotlib 3.10.0.
- Semilla unica en `config`: 20260925, usada en `GroupShuffleSplit` y en
  `StratifiedGroupKFold`.
- Split: `GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=20260925)`.
  Validacion: `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=20260925)`.
- Deteccion de raiz: variable de entorno `ANDINALOG_ROOT` o ancestros del directorio
  actual; ejecutar las celdas en orden desde la raiz del proyecto.
- El notebook se ejecuto de principio a fin: 42 celdas, 25 de codigo, 0 errores de
  ejecucion, 0 tracebacks, 5 graficos embebidos y 34 controles finales en OK. No escribe
  ni modifica el Gold; su unico archivo exportado es el CSV de metricas
  `datos/modelado/metricas_mod_01_regresion_logistica.csv` (144 filas, 7 columnas,
  SHA-256 `33873639ac52dbae04276bbf0feef3562b72c9d8765e5903d4a89b5aa7e3b928`), declarado en
  `config['rutas']['metricas_csv']`.
- El CSV de metricas esta en formato largo con las columnas `bloque`, `variante`,
  `ambito`, `umbral`, `metrica`, `valor` y `detalle`, y recoge ocho bloques:
  `prueba_evaluacion_final` (33 filas), `cv_grupos_principal` y su resumen (30 y 3),
  `cv_grupos_sin_ponderar` y su resumen (30 y 3), `sensibilidad_A_historia` (12),
  `sensibilidad_B_ponderacion` (18) y `umbrales_out_of_fold` (15). Es la unica
  materializacion en disco de las cifras de este informe.
- Cifras de referencia: 28448 filas Gold, 25777 filas de modelado, 1200 viajes, 1300
  positivos, prevalencia 0.050433, 960 viajes de entrenamiento con 20621 filas y 1051
  positivos, 240 viajes de prueba con 5156 filas y 249 positivos, interseccion de grupos
  0, hash del Gold
  `f0194aae8dfe9073fd0e5bbf14cb72353a02863915e483ceec66027e81406479`.

## Controles finales

34 controles, todos en OK: Gold no modificado; forma 28448 x 20; clave de lectura unica;
conciliacion 25777 + 2671 = 28448; ausencia de `dropna`; objetivo nulo solo en ventanas no
evaluables; objetivo solo 0 y 1; exclusiones contadas por causa; filas de modelado
25777; 1200 grupos; proporcion de prueba 0.2000 frente a 0.20 configurado; ambas clases
en ambas particiones; interseccion de grupos vacia; ninguna lectura de prueba en
entrenamiento; predictores = 5 minimos + 2 indicadores; predictores disjuntos de
objetivo, bandera, identificadores, timestamp y auditoria; objetivo ausente de X; sin
variables posteriores a t; antecedentes nunca posteriores al instante de prediccion;
antecedente presente equivale a marca de tiempo presente; codificacion neutra solo en
nulos estructurales declarados; indicadores creados para cada regla; residuales tratados
dentro del Pipeline; imputacion y escalado aprendidos solo con entrenamiento; Pipeline
ajustado una sola vez con `X_tr`, verificado con el registro de ajustes y no afirmado;
convergencia sin agotar iteraciones; validacion cruzada sin solapes de viajes; metricas
de linea base y de modelo disponibles; accuracy no es la unica metrica; semilla fija en
split y validacion; prueba evaluada una sola vez por modelo, verificado con contador
(`{'modelo_principal': 1, 'linea_base': 1}`); estadisticas descriptivas resumidas solo con
filas de entrenamiento; comparacion de ponderacion sin uso del conjunto de prueba y con
recall como criterio principal y el PR AUC marcado como no unico criterio; unico CSV
exportado de metricas y Gold no escrito.

## Correcciones aplicadas tras la auditoria

La auditoria del 2026-09-25 dejo 0 hallazgos criticos, 0 importantes y 5 menores. Los cinco
se corrigieron y el notebook se reejecuto por completo. **Ninguna cifra aprobada cambio**:
la poblacion (25777), el split (20621/5156 con 960/240 viajes e interseccion 0), el
modelo, los umbrales (0.5 y 0.57) y todas las metricas de prueba son identicas a las de la
entrega auditada, y el SHA-256 del Gold permanece en
`f0194aae8dfe9073fd0e5bbf14cb72353a02863915e483ceec66027e81406479`.

| Hallazgo | Correccion | Evidencia de cierre |
|---|---|---|
| MENOR-1: dos controles finales afirmaban en vez de verificar (una sola evaluacion de prueba y un solo ajuste del pipeline) | Se sustituyeron por controles que calculan su propia evidencia: un contador de pasadas de prediccion por modelo y un registro de ajustes con la forma de X usada | Salida de la celda de controles: `{'modelo_principal': 1, 'linea_base': 1}` y `[{'objeto': ..., 'filas': 20621, ...}]` |
| MENOR-2: estadisticas descriptivas calculadas sobre toda la poblacion, que includia prueba | La tabla `mean/median/std/min/max` se calcula despues del split y solo sobre `X_tr`, con el numero de filas usado en la propia salida | Celda del Pipeline: "SOLO de entrenamiento (filas usadas: 20621)"; control "Las estadisticas descriptivas se resumen solo con filas de entrenamiento" en OK |
| MENOR-3: la funcion de codificacion neutra no revalidaba los motivos | La funcion valida ella misma los motivos declarados y lanza `ValueError` si un nulo no es ausencia estructural, sin depender de la celda previa | Codigo de `preparar_faltantes_estructurales`; en esta ejecucion no hubo nulos inesperados y los 1191 + 1471 nulos siguen con motivo declarado |
| MENOR-4: dos graficos sin leyenda o sin eje x | Leyenda explicativa en el mapa de calor de matrices de confusion y `set_xlabel('Metrica evaluada...')` en el grafico de barras | Los 5 graficos llevan titulo, eje x, eje y y leyenda |
| MENOR-5: no se declaraba que las probabilidades no estan calibradas | Se anadio la advertencia de calibracion en la celda de coeficientes y en este informe, junto a la recomendacion de umbral y de tratar la salida como puntaje de priorizacion | Seccion "Interpretacion de coeficientes" y pauta 4 de la recomendacion operativa |

Adicionalmente, y a peticion explicita del usuario tras la auditoria, se documento el
bloque de criterios de seleccion del modelo (criterio principal recall, restriccion
operativa sobre precision y volumen de alertas, PR AUC como metrica global
complementaria, `balanced` como principal por el costo del falso negativo, `class_weight=None`
como alternativa operativa y equilibrio pendiente de costo de negocio o del docente), se
anadieron a la comparacion de sensibilidad las medias por fold de alertas, falsos positivos
y falsos negativos, y se exporto el CSV de metricas de la entrega. Ninguna de esas
adiciones uso el conjunto de prueba, y `class_weight='balanced'` se mantiene como modelo
principal sin cambios.

## Rutas de los entregables

- Notebook: `notebooks/modelado/MOD_01_AndinaLog_Regresion_Logistica.ipynb`
- Informe: `informes/modelado/Informe_MOD_01_AndinaLog_Regresion_Logistica.md`
- Metricas exportadas: `datos/modelado/metricas_mod_01_regresion_logistica.csv`
- Entrada leida: `datos/gold/andinalog_iot_modelado_gold.csv`
- Gold producido por: `notebooks/silver_gold/01_iot_gold/S2G_01_AndinaLog_IoT_Gold.ipynb`
- Evidencia previa: `informes/silver_gold/Informe_S2G_01_IoT_Gold.md` y
  `informes/eda/Informe_EDA_01_AndinaLog_IoT_Gold.md`
