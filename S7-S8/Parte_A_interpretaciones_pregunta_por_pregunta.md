# Parte A: interpretaciones grupales, pregunta por pregunta

Esta guía sigue las **ocho interpretaciones grupales de la Parte A** del notebook, en el mismo orden. En cada pregunta se distingue **lo que respondió el grupo** de **lo que significa en palabras sencillas**. Los números proceden de las salidas guardadas en el notebook.

**Vocabulario mínimo:** `0` = sin falla; `1` = con falla. Un **falso negativo (FN)** es una falla real que el modelo no detectó. Un **falso positivo (FP)** es una alerta cuando no hubo falla. **Recall** = fallas detectadas ÷ todas las fallas reales. **Precisión** = alertas correctas ÷ todas las alertas emitidas. **Accuracy** = predicciones correctas ÷ todas las predicciones.

## Interpretación grupal 1 — Prevalencia y accuracy engañoso

### 1. ¿Cuál es la prevalencia de la clase positiva y cuántos registros representa sobre 900?

**Respuesta del grupo:** 11,33 %, equivalente a 102 registros con falla.

**Explicación:** «Clase positiva» significa aquí **falla (`1`)**; no significa algo bueno. El código contó **102 unos** entre **900 registros**. `102 ÷ 900 = 0,1133`, es decir, **11,33 %**. Dicho de otro modo, aproximadamente 11 de cada 100 registros presentan una falla en el turno siguiente. Hay **798 registros sin falla**.

### 2. ¿Qué accuracy obtendría un modelo que siempre predice «sin falla»? ¿Por qué parece bueno?

**Respuesta del grupo:** 88,67 %; parece alto porque acierta casi 9 de cada 10 casos, debido al desbalance entre clases.

**Explicación:** Si responde `0` en los 900 registros, acierta los **798 sin falla**: `798 ÷ 900 = 88,67 %`. No aprendió a anticipar nada; simplemente aprovechó que las fallas son poco frecuentes.

### 3. ¿Por qué ese accuracy es insuficiente para mantenimiento?

**Respuesta del grupo:** Porque tendría un recall de 0 % y pasaría por alto todas las fallas.

**Explicación:** Ese supuesto modelo acierta muchos casos normales, pero las **102 fallas reales** reciben la respuesta «sin falla». Su recall sería `0 ÷ 102 = 0 %`. Para prevenir averías, necesitamos saber cuántas fallas detecta, no solo cuántas predicciones totales acierta.

## Interpretación grupal 2 — Contrato predictivo

Esta interpretación aparece después del punto 2 del notebook. Es un acuerdo sobre **qué se va a predecir, qué se hará con una alerta y cómo se juzgará el modelo**. Todavía no muestra un resultado nuevo del modelo.

### 1. Clase positiva

**Respuesta del grupo:** La ocurrencia de una falla, `falla_proximo_turno = 1`.

**Explicación:** Es el evento que se quiere encontrar. Cuando más adelante veas «recall de la clase positiva», léelo como **porcentaje de fallas reales detectadas**.

### 2. Horizonte de predicción

**Respuesta del grupo:** El turno operativo inmediatamente posterior a la medición.

**Explicación:** «Horizonte» responde **¿para cuándo?**. El modelo mira mediciones actuales para anticipar una falla **en el próximo turno**, no en cualquier fecha futura. Esto también determina qué datos pueden usarse: deben existir antes de ese turno.

### 3. Acción ante una alerta

**Respuesta del grupo:** Priorizar y programar una inspección técnica preventiva antes del siguiente turno, sin detener innecesariamente la producción.

**Explicación:** Una alerta no equivale a una falla confirmada. Es una señal para **revisar primero ese equipo**. La utilidad del modelo depende de que mantenimiento pueda convertir las alertas en inspecciones a tiempo.

### 4. Costo de un falso negativo

**Respuesta del grupo:** Muy elevado por posibles paradas imprevistas, daños y riesgos de seguridad.

**Explicación:** Un falso negativo es **un equipo que sí falla, aunque el modelo dijo que no**. Se pierde la oportunidad de inspeccionarlo antes. El grupo describe consecuencias posibles; el notebook **no calcula un costo monetario ni demuestra que cada fallo omitido causó una parada**.

### 5. Costo de un falso positivo

**Respuesta del grupo:** Bajo o moderado; consume tiempo y recursos al inspeccionar un equipo que no iba a fallar.

**Explicación:** Un falso positivo es **una alerta que no correspondía a una falla**. Aunque sea menos grave que omitir una avería, muchas falsas alertas pueden ocupar a todos los técnicos y restar credibilidad al sistema.

### 6. Métrica primaria

**Respuesta del grupo:** Recall o sensibilidad de la clase positiva.

**Explicación:** Se elige recall porque el objetivo es **detectar la mayor cantidad posible de fallas reales**. Más adelante, el modelo detecta 19 de 20 fallas en prueba: `19 ÷ 20 = 95 %` de recall. Esa cifra no dice cuántas alertas falsas emitió; para eso se mira otra medida.

### 7. Contramétrica o límite operativo

**Respuesta del grupo:** Precisión o volumen total de alertas, para no saturar al personal.

**Explicación:** «Contra» significa **una segunda condición que limita la decisión**: detectar fallas no sirve de mucho si se generan más alertas de las que se pueden revisar. La precisión indica qué fracción de las alertas era correcta; el volumen indica cuántas inspecciones habría que hacer. No son la misma medida, pero ambas ayudan a juzgar la carga operativa.

## Interpretación grupal 3 — Variables disponibles y fuga de información

El código deja **10 variables de entrada** (`X`) y la respuesta conocida (`y = falla_proximo_turno`). Excluye identificadores y `orden_correctiva_post_evento`.

### 1. ¿Por qué se excluye `orden_correctiva_post_evento` de `X`?

**Respuesta del grupo:** Porque se genera después de ocurrida la falla y no existe al anticipar el turno siguiente.

**Explicación:** Sería como intentar pronosticar un accidente consultando el informe escrito **después** del accidente. El dato podría delatar la respuesta durante el ejercicio, pero no estaría disponible al tomar una decisión real. Esa es una **fuga de información temporal**.

### 2. ¿Por qué tampoco entran `registro_id`, `timestamp_utc` y `equipo_id`?

**Respuesta del grupo:** Son identificadores o metadatos; podrían inducir al modelo a memorizar registros o equipos en vez de aprender patrones operativos.

**Explicación:** Un identificador distingue una fila o un equipo, pero por sí solo no explica el estado físico medido. En este diseño se prefiere que el modelo aprenda de temperatura, vibración, presión, alarmas, etc. La hora o la identidad de un equipo podrían ser útiles en otros diseños, pero aquí se excluyen para evitar atajos difíciles de generalizar.

### 3. ¿Qué pasaría si se incluyera por error la orden posterior?

**Respuesta del grupo:** Las métricas podrían subir artificialmente a valores casi perfectos; sería una señal de alarma.

**Explicación:** El modelo estaría usando una pista que solo aparece **después** de lo que pretende predecir. Así, un resultado excelente en el notebook podría desplomarse al usarlo antes de la falla. El grupo menciona «~100 %» como advertencia ilustrativa: **el notebook no hizo esa prueba**, por lo que no sabemos la cifra exacta.

## Interpretación grupal 4 — Partición estratificada y baseline

El código separó **720 registros para entrenamiento** y **180 para prueba**. En prueba hay **160 sin falla** y **20 con falla**. El *baseline* siempre predice «sin falla».

### 1. ¿Por qué se usó `stratify=y`?

**Respuesta del grupo:** Para conservar una proporción de fallas parecida en entrenamiento y prueba: 11,39 % y 11,11 %.

**Explicación:** La separación estratificada procura que ambos conjuntos representen el problema original. Si se separaran al azar sin esta precaución, una clase poco frecuente podría quedar demasiado escasa en prueba. **Las proporciones son similares, no exactamente iguales**, como dice la respuesta original.

### 2. ¿Cuántas fallas detecta el baseline y cuál es su recall?

**Respuesta del grupo:** Detecta **0 de las 20 fallas**; su recall es **0 %**.

**Explicación:** Su matriz es `[[160, 0], [20, 0]]`. La segunda fila describe las **20 fallas reales**: las 20 quedaron en la columna «predice sin falla». No hubo ninguna alerta correcta.

### 3. ¿Por qué su accuracy alto no lo hace útil?

**Respuesta del grupo:** El 88,89 % se debe a que la mayoría de los casos no falla; no anticipa ningún problema.

**Explicación:** Acertó `160 ÷ 180 = 88,89 %` al responder siempre «sin falla». Sin embargo, la tarea de mantenimiento es **encontrar fallas**. La *balanced accuracy* de **0,50** refleja mejor que el desempeño en la clase de fallas es nulo.

### 4. ¿Qué ocurriría si mantenimiento lo utilizara como modelo real?

**Respuesta del grupo:** Las fallas llegarían sin aviso, con posibles paradas y daños.

**Explicación:** En estos 180 casos, **las 20 fallas reales habrían quedado sin alerta**. Por ello el baseline solo sirve como **punto mínimo de comparación**, no como sistema de prevención. Las consecuencias operativas mencionadas son riesgos posibles, no efectos medidos en el notebook.

## Interpretación grupal 5 — Pipeline sin contaminación

El *pipeline* prepara los datos: rellena faltantes, escala las **7 variables numéricas**, codifica las **3 categóricas** y luego usa regresión logística. En el punto 6 se muestra la estructura del proceso; aún no se reporta una métrica de rendimiento.

### 1. ¿Qué pasaría si la mediana y el escalado se calcularan con train + test?

**Respuesta del grupo:** Habría contaminación o fuga de información desde los datos de prueba.

**Explicación:** Los datos de prueba deben simular casos **no vistos**. Si sus valores ayudan a calcular la mediana o la escala antes de evaluar, ya influyeron en la preparación del modelo. El *pipeline* hace esos cálculos usando solo el conjunto de entrenamiento en cada ajuste.

### 2. ¿Por qué sería difícil detectar esa contaminación mirando solo las métricas?

**Respuesta del grupo:** El código funcionaría y las métricas podrían verse normales o demasiado buenas.

**Explicación:** Una cifra final no revela **cómo se prepararon** los datos. Para descubrir la fuga hay que revisar el orden del proceso: primero separar entrenamiento y prueba; después aprender las transformaciones con entrenamiento. El problema no tiene por qué producir un mensaje de error.

## Interpretación grupal 6 — Ajuste de hiperparámetros

Se probaron **8 configuraciones** mediante validación cruzada de **5 partes**, usando solo entrenamiento. `C` es un ajuste de la regresión logística; `class_weight="balanced"` aumenta la importancia relativa de la clase minoritaria.

### 1. ¿Qué combinación ganó y qué resultado obtuvo?

**Respuesta del grupo:** `C = 0.05` y `class_weight="balanced"`, con *balanced accuracy* promedio de **0,8414** (84,14 %).

**Explicación:** Entre las ocho opciones, esa obtuvo el mejor promedio en las cinco evaluaciones internas. **No es el resultado final en los 180 casos de prueba**; esa evaluación aparece en el punto 8.

### 2. ¿Qué grupo de configuraciones fue más estable entre las cinco partes?

**Respuesta del grupo:** Las configuraciones `balanced`, con desviaciones entre **0,027 y 0,039**, frente a **0,059 a 0,091** sin ponderación.

**Explicación:** La desviación estándar indica cuánto cambió el resultado de una partición a otra. En esta búsqueda, **menor desviación** significa resultados más parecidos entre las cinco partes. Eso respalda la comparación del grupo, aunque cinco particiones no garantizan el mismo comportamiento en cualquier dato futuro.

### 3. ¿Por qué suele ganar `class_weight="balanced"` aquí?

**Respuesta del grupo:** Porque las fallas son solo el 11,3 % y la ponderación obliga al modelo a prestar más atención a esa clase.

**Explicación:** Sin ponderación, equivocarse en pocos casos de falla puede quedar «tapado» por muchos aciertos sin falla. La ponderación hace más costoso para el entrenamiento equivocarse en la clase minoritaria. En **estos resultados**, todas las configuraciones `balanced` superaron a las no ponderadas en *balanced accuracy*; no es una regla universal para cualquier conjunto de datos.

## Interpretación grupal 7 — Costo del error en prueba

La matriz final es `[[146, 14], [1, 19]]`. Las **filas son los resultados reales** y las **columnas las predicciones**. Por tanto: 146 sin falla acertados, 14 falsas alertas, 1 falla omitida y 19 fallas detectadas.

### 1. ¿Cuántos falsos negativos hay y qué implican?

**Respuesta del grupo:** **1**; representa una falla real no anticipada, con riesgo de parada, daño o sobrecosto.

**Explicación:** El `1` está en la fila «realmente hubo falla» y la columna «predijo sin falla». El modelo detectó 19 de 20 fallas y **omitió una**. La salida no dice que efectivamente se produjo una parada; describe el riesgo de no haber alertado.

### 2. ¿Cuántos falsos positivos hay y qué implican?

**Respuesta del grupo:** **14**; son inspecciones preventivas que no encontraron una falla del siguiente turno.

**Explicación:** El `14` está en la fila «realmente no hubo falla» y la columna «predijo falla». Esas alertas consumirían tiempo de revisión. No deben confundirse con las **19 alertas correctas**.

### 3. ¿La solución respeta la capacidad real de inspección de la planta?

**Respuesta del grupo:** Dice que sí, porque genera **33 alertas** en 180 registros y las considera manejables.

**Explicación:** El cálculo `19 alertas correctas + 14 falsas = 33 alertas` es correcto. Sin embargo, **la capacidad real de la planta no aparece en este punto**. Por eso no se puede concluir solo con esa matriz que 33 inspecciones sean manejables. En el punto 9 se introduce un límite hipotético de **25 alertas por este conjunto de prueba**; bajo ese supuesto, 33 superarían la capacidad.

### 4. ¿Qué limitación permanece?

**Respuesta del grupo:** La precisión es **57,58 %**; una parte importante de las alertas es falsa y puede provocar fatiga de alertas.

**Explicación:** De las **33 alertas**, solo **19** correspondían a fallas: `19 ÷ 33 = 57,58 %`. Las otras **14 de 33**, aproximadamente **42,42 %**, eran falsas. El modelo detecta casi todas las fallas (**95 % de recall**), pero exige revisar varios equipos que no fallarán.

## Interpretación grupal 8 — Sensibilidad al umbral

El umbral indica desde qué puntuación se emite una alerta. La tabla real del notebook es:

| Umbral | Falsas alertas (FP) | Fallas omitidas (FN) | Fallas detectadas (TP) | Alertas totales | Precisión | Recall |
|---|---:|---:|---:|---:|---:|---:|
| 0,35 | 22 | 1 | 19 | 41 | 46,34 % | 95 % |
| 0,50 | 14 | 1 | 19 | 33 | 57,58 % | 95 % |
| 0,80 | 5 | 3 | 17 | 22 | 77,27 % | 85 % |

### 1. ¿Qué cambia al bajar de 0,50 a 0,35?

**Respuesta del grupo:** Suben las falsas alertas de **14 a 22** y las alertas totales de **33 a 41**; las fallas omitidas siguen en **1**.

**Explicación:** El umbral más bajo facilita emitir alertas. En **estos datos**, agregó **8 alertas**, pero ninguna detectó una falla adicional. El costo de inspección sube; **el riesgo medido por los falsos negativos no disminuye** entre esos dos umbrales.

### 2. ¿Qué cambia al subir de 0,50 a 0,80?

**Respuesta del grupo:** Bajan las falsas alertas de **14 a 5** y las alertas totales de **33 a 22**, pero las fallas omitidas suben de **1 a 3**.

**Explicación:** Un umbral alto exige mayor evidencia antes de alertar. Hace falta inspeccionar menos equipos, pero se pierden **dos fallas adicionales** respecto al umbral 0,50. El recall baja de **95 % a 85 %**.

### 3. Si mantenimiento solo puede atender 25 alertas, ¿qué umbral recomienda el grupo?

**Respuesta del grupo:** **0,80**, porque produce **22 alertas**, el único valor por debajo del límite de 25; detecta **17 de 20 fallas**.

**Explicación:** Los otros umbrales generan **41** y **33** alertas, así que exceden ese límite supuesto. Con 0,80 cabrían 22 inspecciones, pero **3 fallas reales no recibirían alerta**. Es una decisión condicionada a que el límite de 25 corresponda de verdad a ese volumen y período de trabajo.

### 4. ¿Por qué no elegir un umbral solo por su F1?

**Respuesta del grupo:** Porque F1 no incorpora por sí mismo la capacidad del personal ni el costo operativo de las alertas.

**Explicación:** F1 combina precisión y recall en un número. En esta tabla, **0,80 también tiene el F1 más alto (0,8095)**, pero la razón operativa para elegirlo bajo el límite supuesto es que produce **22 alertas**, no simplemente que gane en F1. Si las consecuencias de omitir 3 fallas fueran inaceptables, habría que revisar el límite de inspección o la decisión; una cifra de F1 no resuelve por sí sola ese conflicto.

## Punto 10 — Evidencia de avance

El punto 10 **no añade otra interpretación grupal ni nuevas métricas**. Pide conservar en el notebook las **interpretaciones 1 a 8** y las salidas visibles. Sirve para comprobar que cada respuesta puede relacionarse con una salida del código. La Parte B comienza después, en el punto 11.
