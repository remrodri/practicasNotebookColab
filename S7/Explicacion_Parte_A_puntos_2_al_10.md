# Explicación de la Parte A, puntos 2 al 10

La **Parte A** intenta responder una pregunta: *con las mediciones disponibles ahora, ¿podemos anticipar si un equipo fallará en el siguiente turno?* Cada bloque de código prepara o evalúa esa predicción. La **interpretación grupal** traduce los números a una decisión de mantenimiento.

Para leer el notebook: **0 significa «sin falla» y 1 significa «con falla»**. Los 900 registros son observaciones; no conviene asumir que son 900 equipos distintos.

## 2. Carga y auditoría del objetivo

**Qué hace el código.** Abre los datos y revisa cuántas filas y columnas hay, qué tipo de información contiene cada columna, dónde faltan valores y cuántos casos tienen `falla_proximo_turno = 1`.

**Qué muestra la salida.** Hay **900 registros y 15 columnas**. De ellos, **798 no presentan falla** y **102 sí presentan falla**. Por tanto, la *prevalencia* de fallas es **102 ÷ 900 = 11,33 %**. También faltan algunos datos, por ejemplo 22 temperaturas y 18 presiones; en la columna que indica la falla no falta ninguno.

El código calcula además que, si alguien predijera **«sin falla» para todos**, acertaría **88,67 %** de las veces. Parece un buen resultado, pero se debe a que la mayoría de los registros no tiene falla.

**Relación con la interpretación grupal 1.** El grupo señala la trampa: ese 88,67 % de *accuracy* (porcentaje total de aciertos) **no detectaría ninguna de las 102 fallas**. Su *recall* de fallas sería 0 %. Para mantenimiento, acertar muchos casos normales no compensa pasar por alto todas las averías.

## Interpretación grupal 2: contrato predictivo (a continuación del punto 2)

Aquí no aparece un nuevo resultado numérico ni un bloque de entrenamiento. El grupo deja por escrito **qué se quiere predecir y cómo se usará la alerta**.

En el notebook, esta interpretación aparece inmediatamente después de la interpretación grupal 1, dentro del trabajo del punto 2. **No hay un encabezado numerado «3» separado** antes del punto 4.

La decisión escrita es: predecir una **falla en el turno siguiente**; si hay alerta, priorizar una inspección preventiva. El grupo considera más grave un **falso negativo** (ocurre una falla y el modelo no avisa) que un **falso positivo** (avisa, se inspecciona y no había falla).

Por eso propone vigilar principalmente el **recall**, es decir, *qué proporción de las fallas reales se detecta*. A la vez, debe controlar la cantidad de alertas: incluso un modelo que detecta muchas fallas puede ser poco práctico si exige demasiadas inspecciones. Este «contrato» da sentido a las métricas de los puntos siguientes.

**Cómo entender cada pregunta y respuesta de esta interpretación:**

1. **Clase positiva.** Preguntan cuál es el evento que interesa detectar. El grupo responde `falla_proximo_turno = 1`: «positivo» aquí significa *falla*, no «bueno».
2. **Horizonte de predicción.** Preguntan *para cuándo* se hace el pronóstico. La respuesta es **el turno inmediatamente siguiente** a la medición, no cualquier falla futura.
3. **Acción ante una alerta.** Preguntan qué hará mantenimiento si el modelo avisa. El grupo propone **priorizar una inspección preventiva antes del siguiente turno**. Una alerta sirve para decidir una acción; por sí sola no repara el equipo.
4. **Costo de un falso negativo.** Es una **falla real que el modelo no detecta**. El grupo lo considera muy grave por el riesgo de parada, daño o seguridad. Es una valoración del posible impacto, no un costo monetario calculado en el notebook.
5. **Costo de un falso positivo.** Es una **alerta en un caso que no falla**. Consume tiempo de inspección. El grupo lo juzga menos grave que omitir una falla, aunque muchas falsas alertas también pueden saturar al personal.
6. **Métrica primaria.** El grupo elige **recall** porque mide la proporción de fallas reales que el modelo logra detectar. Por ejemplo, en el punto 8 detecta 19 de 20: `19 ÷ 20 = 95 %`.
7. **Contramétrica o límite operativo.** Preguntan qué hay que vigilar además del recall. La respuesta es la **precisión o el volumen de alertas**, para que las inspecciones sean realizables. Más adelante, el punto 9 compara 41, 33 y 22 alertas según el umbral.

## 4. Variables disponibles y fuga de información

**Qué hace el código.** Separa los datos en `X` y `y`:

- `X`: las **10 variables** que el modelo puede usar, como temperatura, vibración, presión, turno y alarmas recientes.
- `y`: la respuesta que debe aprender a predecir, `falla_proximo_turno`.

La salida `X shape: (900, 10)` significa **900 registros con 10 datos de entrada por registro**. `y shape: (900,)` significa **900 respuestas conocidas**.

**Relación con la interpretación grupal 3.** Se excluye `orden_correctiva_post_evento` porque se genera **después** del evento. Sería como intentar pronosticar una avería usando una orden emitida tras la avería: el modelo parecería excelente en el ejercicio, pero no podría usar ese dato cuando se necesite anticipar una falla real. Eso se llama **fuga de información**. El grupo también excluye los identificadores para evitar que el modelo se apoye en códigos de registros o equipos en lugar de patrones operativos. La afirmación del grupo de que incluir la variable posterior daría métricas «casi perfectas» es una **posibilidad**, no algo demostrado por esta salida.

## 5. Partición estratificada y modelo de referencia

**Qué hace el código.** Reserva **720 registros para entrenar** y **180 para probar** el modelo. `stratify=y` procura mantener una proporción de fallas parecida en ambos grupos: **11,39 % en entrenamiento** y **11,11 % en prueba**. Son proporciones *muy similares*, aunque no exactamente iguales.

Luego prueba un modelo de referencia (*baseline*) que siempre responde «sin falla».

**Qué muestra la salida.** En los 180 casos de prueba había **160 sin falla y 20 con falla**. La matriz del baseline es:

| Resultado real | Predice sin falla (0) | Predice falla (1) |
|---|---:|---:|
| Sin falla (0) | 160 | 0 |
| Con falla (1) | 20 | 0 |

Acertó los 160 casos normales, pero **no detectó ninguna de las 20 fallas**. Su accuracy es **88,89 %**, mientras que su recall para fallas es **0 %**. La *balanced accuracy* es **0,50**: esta métrica da el mismo peso al desempeño en ambas clases y deja más visible el problema.

**Relación con la interpretación grupal 4.** La respuesta del grupo es correcta en lo esencial: un porcentaje global de aciertos alto no convierte al baseline en una herramienta útil para prevenir fallas.

## 6. Pipeline reproducible

**Qué hace el código.** Prepara los datos antes de entregarlos a una **regresión logística**, que es el modelo de clasificación usado aquí. Identifica **7 variables numéricas** y **3 categóricas**. En las numéricas, rellena los valores ausentes con la mediana y ajusta las escalas; en las categóricas, rellena con el valor más frecuente y convierte las categorías a números que el modelo pueda procesar.

**Qué significa la salida.** La larga representación de `Pipeline(...)` muestra **cómo quedó armado el proceso**. Todavía no es una medición de su calidad: en este punto se ha definido la secuencia de preparación y modelado.

**Relación con la interpretación grupal 5.** El grupo explica por qué la preparación debe aprender sus valores usando solo los datos de entrenamiento. Si la mediana o la escala se calcularan incluyendo los datos de prueba, la evaluación dejaría de ser completamente independiente. El código puede funcionar sin mostrar un error, pero sus resultados podrían ser demasiado optimistas.

## 7. Ajuste de hiperparámetros

**Qué hace el código.** Prueba **8 configuraciones** de la regresión logística: cuatro valores de `C` combinados con dos opciones de `class_weight`. Cada configuración se evalúa mediante **5 particiones de validación**, usando solo los datos de entrenamiento. `C` controla cuánto se restringe el modelo; `class_weight="balanced"` da más peso a la clase minoritaria, las fallas.

**Qué muestra la salida.** Ganó **`C = 0.05` y `class_weight = "balanced"`**, con una *balanced accuracy* promedio de **0,8414** en validación. Su desviación estándar fue **0,0392**, una medida de cuánto variaron los resultados entre las cinco particiones. En esta búsqueda, las configuraciones `balanced` tuvieron desviaciones menores que las configuraciones sin ponderación.

**Relación con la interpretación grupal 6.** La lectura del grupo coincide con la tabla: ponderar las fallas ayudó a este modelo a atender la clase poco frecuente. El **84,14 % corresponde a la validación dentro de entrenamiento**; todavía no es el resultado de la prueba final.

## 8. Evaluación en los datos de prueba

**Qué hace el código.** Usa el modelo elegido para predecir los **180 registros de prueba**, que no participaron en la búsqueda anterior.

**Cómo leer la matriz.** Las filas indican lo que **ocurrió realmente** y las columnas lo que **predijo el modelo**:

| Resultado real | Predice sin falla (0) | Predice falla (1) |
|---|---:|---:|
| Sin falla (0) | 146 | 14 |
| Con falla (1) | 1 | 19 |

Esto significa:

- **146** casos sin falla correctamente identificados.
- **14 falsos positivos:** se emitió una alerta, pero no hubo falla.
- **1 falso negativo:** hubo falla, pero no se emitió alerta.
- **19 fallas correctamente detectadas.**

El modelo emitió **33 alertas** en total: 19 útiles y 14 falsas. Detectó **19 de las 20 fallas**, de modo que su **recall es 95 %**. De las 33 alertas, 19 correspondían a fallas reales: su **precisión es 57,58 %**. La *balanced accuracy* fue **93,12 %**.

**Relación con la interpretación grupal 7.** El grupo identifica bien los tipos de error y la precisión moderada. Hay un matiz: afirma que **33 alertas son manejables**, pero el notebook no da aquí una capacidad real de inspección para justificarlo. De hecho, en el punto 9 se plantea un límite hipotético de **25 alertas** para estos 180 casos; bajo ese límite, 33 lo superarían. Tampoco podemos afirmar que el único falso negativo necesariamente produjo una parada concreta: el dato muestra una falla no anticipada, y el impacto operativo descrito por el grupo es el riesgo asociado.

## 9. Sensibilidad al umbral

El modelo produce una puntuación para la clase «falla». El **umbral** decide a partir de qué puntuación se emite una alerta: cuanto más bajo sea, más fácil es alertar.

| Umbral | Alertas | Falsas alertas | Fallas no detectadas | Fallas detectadas |
|---|---:|---:|---:|---:|
| 0,35 | 41 | 22 | 1 | 19 |
| 0,50 | 33 | 14 | 1 | 19 |
| 0,80 | 22 | 5 | 3 | 17 |

**Relación con la interpretación grupal 8.** Al bajar de **0,50 a 0,35**, se hacen **8 inspecciones adicionales**, todas falsas en este conjunto de prueba, y **no se detecta ninguna falla adicional**. Por tanto, aquí no disminuye el número de fallas omitidas: sigue siendo 1.

Al subir a **0,80**, las alertas bajan de 33 a 22 y las falsas alertas de 14 a 5, pero se dejan pasar **3 fallas en vez de 1**. Si el límite supuesto es **25 inspecciones por este conjunto de 180 registros**, **0,80 es el único de los tres umbrales que cabe en ese límite**. Esa es la razón práctica de la recomendación del grupo. Antes de aplicarla en la planta habría que relacionar ese límite con un período y una carga de trabajo reales.

## 10. Evidencia de avance

Este punto **no ejecuta un modelo ni genera nuevas cifras**. Es una lista de comprobación para cerrar la Sesión 7: deben quedar escritas las interpretaciones grupales 1 a 8 y guardarse el notebook **con las salidas visibles**. Así se puede seguir el razonamiento desde la proporción inicial de fallas hasta la elección de un umbral. Según el propio notebook, este avance forma parte del laboratorio; la calificación final llega tras cerrar la Parte B.

## Idea para recordar toda la Parte A

El modelo del punto 8 detecta **19 de 20 fallas** al umbral habitual de 0,50, pero genera **33 alertas**. El punto 9 muestra por qué la decisión final también depende de **cuántas inspecciones puede atender mantenimiento y cuántas fallas está dispuesto a arriesgarse a no detectar**.

---

# Preguntas y respuestas completas del grupo

Esta sección reproduce las ocho interpretaciones de la Parte A tal como aparecen en el notebook. Las secciones anteriores explican cómo relacionarlas con los resultados del código.

### Interpretación grupal 1 — Prevalencia y accuracy engañoso

Con los resultados anteriores a la vista, respondan como grupo:

1. ¿Cuál es la prevalencia de la clase positiva y cuántos registros representa sobre 900?
2. ¿Qué accuracy obtendría un modelo que siempre predice "sin falla"? ¿Por qué esa cifra parece buena a simple vista?
3. ¿Por qué ese accuracy sería insuficiente como única métrica para decidir si el modelo sirve para mantenimiento?

**Respuesta del grupo:**

1. La prevalencia es del 11.33%, lo que equivale a 102 registros con falla de los 900 totales.
2. Obtendría un 88.67% de accuracy. Parece alta a simple vista porque casi 9 de cada 10 casos son acertados, pero es solo un reflejo del fuerte desbalance de clases.
3. Es insuficiente porque ese modelo tendría un recall de 0%, pasando por alto el 100% de las fallas reales que mantenimiento necesita prevenir.

### Interpretación grupal 2 — Contrato predictivo

Antes de entrenar cualquier modelo, el grupo debe fijar por escrito el contrato predictivo. Completen cada punto con una decisión concreta y justificada, no solo una palabra:

- **Clase positiva:** ...
- **Horizonte de predicción:** ...
- **Acción ante una alerta:** ...
- **Costo de un falso negativo (no detectar una falla real):** ...
- **Costo de un falso positivo (alertar sin que exista falla):** ...
- **Métrica primaria:** ...
- **Contramétrica o límite operativo (qué no debe empeorar):** ...

**Respuesta del grupo:**

- **Clase positiva:** Ocurrencia de falla en el equipo (falla_proximo_turno = 1), que es el evento crítico que se busca mitigar.
- **Horizonte de predicción:** El turno operativo inmediatamente posterior al momento de la medición.
- **Acción ante una alerta:** Priorizar y programar una inspección técnica preventiva en el equipo antes de iniciar el siguiente turno, sin detener la producción de forma innecesaria.
- **Costo de un falso negativo:** Crítico y muy elevado, pues provoca paradas imprevistas de planta, daños mecánicos graves y riesgos de seguridad al no advertir una falla real.
- **Costo de un falso positivo:** Bajo o moderado, limitándose al tiempo y recursos invertidos por el técnico en revisar un equipo que no iba a fallar.
- **Métrica primaria:** Recall (o Sensibilidad) de la clase positiva, ya que el objetivo principal del negocio es capturar la mayor cantidad de fallas reales posibles.
- **Contramétrica o límite operativo:** Precisión (o volumen total de alertas), asegurando que la cantidad de inspecciones no sature la capacidad operativa del personal de mantenimiento.

### Interpretación grupal 3 — Justificación de disponibilidad

1. ¿Por qué `orden_correctiva_post_evento` se excluye de `X`? Usen el diccionario de datos para justificar la respuesta en términos de "disponible antes vs. después del horizonte".
2. ¿Por qué `registro_id`, `timestamp_utc` y `equipo_id` tampoco entran como variables predictoras, aunque estén disponibles antes del horizonte?
3. Si por error se hubiera incluido `orden_correctiva_post_evento` en `X`, ¿qué le pasaría a las métricas del modelo y por qué esa mejora sería una señal de alarma y no un logro?

**Respuesta del grupo:**

1. Se excluye porque es una variable generada después de que la falla ya ocurrió. Incluirla violaría el principio de disponibilidad temporal al no existir dicha información al momento de anticipar el siguiente turno
2. No se incluyen porque son metadatos e identificadores de alta cardinalidad. Su presencia provocaría que el modelo memorice registros o equipos específicos en lugar de aprender patrones físicos y operativos generalizables.
3. Las métricas subirían artificialmente a niveles casi perfectos (~100%). Esto sería una alarma crítica y no un logro porque revelaría una fuga de datos que inutilizaría el modelo en un entorno real de producción al no contar con esa variable a tiempo.

### Interpretación grupal 4 — Partición estratificada y por qué el baseline no protege la decisión

1. ¿Por qué la partición se hizo con `stratify=y` en vez de un `train_test_split` simple? Comparen la prevalencia impresa en train y en test: ¿qué le hubiera podido pasar a esa proporción de fallas en test si la partición no se hubiera estratificado?
2. ¿Cuántas fallas reales detecta el baseline en test (revisen la matriz de confusión) y qué recall tiene sobre la clase positiva?
3. El baseline logra una accuracy alta. ¿Por qué esa cifra no significa que el baseline sea útil para mantenimiento?
4. ¿Qué le pasaría a la planta si Mantenimiento usara el baseline como si fuera un modelo predictivo real?

**Respuesta del grupo:**

1. Se usó stratify=y para asegurar que tanto train (11.39%) como test (11.11%) tengan exactamente la misma proporción de fallas. Si no se estratificaba, el azar podía dejar a test con muy pocas o ninguna falla, impidiendo evaluar el modelo con datos realistas.
2. El baseline detecta 0 fallas en test (acierta 160 casos sin falla y falla en las 20 averías reales). Por lo tanto, su recall en la clase positiva es de 0.00 (0%).
3. Su accuracy es alto (88.89%) únicamente porque la gran mayoría de las máquinas no falla. No sirve para mantenimiento porque acierta por descarte sin haber anticipado un solo problema.
4. La planta sufriría paradas no programadas constantes y posibles daños graves en los equipos. Al asumir que "nunca pasa nada", las 20 fallas reales ocurrirían en plena operación sin previo aviso.

### Interpretación grupal 5 — Por qué ajustar dentro del Pipeline

1. ¿Qué pasaría si la mediana de imputación y el `StandardScaler` se calcularan sobre todo el dataset (train + test) antes de dividir, en vez de ajustarse solo con `train` dentro del `Pipeline`?
2. ¿Por qué esa contaminación es difícil de detectar simplemente mirando las métricas finales?

**Respuesta del grupo:**

1. Se produciría contaminación o fuga de información (data leakage), ya que el modelo aprendería con datos calculados a partir de información del conjunto de prueba (test) que en la realidad aún no debería conocer.
2. Porque no genera errores de código y las métricas finales se ven normales o falsamente optimistas; el verdadero problema solo se hace evidente cuando el modelo falla al operar con datos nuevos en producción.

### Interpretación grupal 6 — Estabilidad y elección de hiperparámetros

1. ¿Qué combinación de `C` y `class_weight` ganó la búsqueda y qué `balanced_accuracy` promedio obtuvo en validación cruzada?
2. Comparen la desviación estándar (`std_test_score`) entre las combinaciones con `class_weight="balanced"` y las combinaciones con `class_weight=None`. ¿Qué grupo es más estable entre folds?
3. ¿Por qué `class_weight="balanced"` tiende a ganar en un dataset con solo 11,3% de fallas, en vez del modelo sin ponderar?

**Respuesta del grupo:**

1. Ganó la combinación de C = 0.05 con class_weight = "balanced", alcanzando un balanced accuracy promedio de 0.8414 (84.14%) en validación cruzada.
2. Los modelos con class_weight="balanced" tienen desviaciones estándar más bajas (0.027 a 0.039) que los modelos con None (0.059 a 0.091). Por lo tanto, el grupo con balanced es mucho más estable y consistente entre los folds.
3. Porque al haber tan pocas fallas (11.3%), el modelo normal tiende a ignorarlas para no equivocarse; en cambio, balanced castiga con mayor fuerza no predecir una falla real, obligando al modelo a prestar atención a la clase minoritaria.

### Interpretación grupal 7 — Costo del error

1. **Falsos negativos:** ¿cuántos hay en la matriz de confusión? ¿Qué implica cada uno para la planta (una falla real que no se detectó)?
2. **Falsos positivos:** ¿cuántos hay? ¿Qué implica cada uno en términos de inspecciones innecesarias?
3. Con 180 observaciones en test y este resultado, ¿la solución respeta la capacidad real de inspección de una planta (revisen cuántas alertas totales genera)?
4. ¿Qué limitación importante permanece incluso con este modelo ajustado?

**Respuesta del grupo:**

1. Hay 1 falso negativo. Para la planta implica una falla real no anticipada, lo que se traduce en una parada no programada, sobrecostos de reparación urgente o posibles riesgos operativos.
2. Hay 14 falsos positivos. Cada uno representa una orden de inspección preventiva despachada a un equipo que estaba funcionando bien, consumiendo tiempo y horas-hombre innecesarias de los técnicos.
3. Sí, la solución es viable operativamente porque genera 33 alertas en total (19 fallas reales detectadas + 14 falsas alarmas) sobre 180 equipos evaluados, un volumen manejable para la cuadrilla de mantenimiento.
4. La limitación principal es la precisión moderada (57.58%): casi 4 de cada 10 alertas emitidas siguen siendo falsas alarmas, lo que a largo plazo puede causar desconfianza o "fatiga de alertas" en el personal de planta.

### Interpretación grupal 8 — Sensibilidad al umbral

1. Al bajar el umbral de 0.50 a 0.35, ¿qué costo aumenta y cuál disminuye? Usen las columnas FP, FN y alertas_totales de la tabla.
2. Al subir el umbral de 0.50 a 0.80, ¿qué costo aumenta y cuál disminuye?
3. Si Mantenimiento solo puede atender 25 alertas por corte de test sin saturarse, ¿qué umbral de los tres recomendaría el grupo y por qué?
4. ¿Por qué no sería correcto elegir un umbral únicamente porque produce la cifra de F1 más alta, sin considerar la capacidad de inspección?

**Respuesta del grupo:**

1. Aumenta el costo operativo por inspecciones innecesarias (los FP suben de 14 a 22 y las alertas totales pasan de 33 a 41). En cambio, el costo por riesgo no varía (los FN se mantienen en 1, conservando un recall de 0.95).
2. Aumenta el costo por riesgo de falla no detectada (los FN suben de 1 a 3, bajando el recall de 0.95 a 0.85). Disminuye el costo de inspecciones inútiles (los FP caen drásticamente de 14 a 5 y las alertas totales se reducen a 22).
3. Se recomendaría el umbral 0.80, ya que genera 22 alertas totales, siendo el único que no sobrepasa el límite de 25 inspecciones de la planta. Permite detectar el 85% de las fallas reales con una alta precisión del 77.27% sin saturar a los técnicos.
4. Porque el puntaje F1 es un promedio armónico puramente matemático que no toma en cuenta los recursos humanos ni el tiempo disponible del equipo de mantenimiento. Si un umbral da el mejor F1 pero genera más alertas de las que los técnicos pueden revisar, el modelo colapsará la operación en la práctica.

