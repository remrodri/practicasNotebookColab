# Guía explicativa del Laboratorio 3

## 1. Objetivo general

El notebook construye y evalúa una red neuronal que intenta detectar condiciones de riesgo de falla en un activo industrial. Cada fila representa una lectura del activo y contiene datos como temperatura, presión, vibración, carga, corriente y horas desde el último mantenimiento.

El trabajo no busca solamente obtener una predicción. También enseña a:

- separar correctamente los datos;
- evitar fugas de información;
- comparar el modelo con una referencia sencilla;
- reconocer el sobreajuste;
- elegir un umbral de decisión según el costo de los errores;
- evaluar el resultado final con datos que el modelo no había visto.

## 2. Conceptos básicos

La variable `riesgo_falla` tiene dos valores:

- **0:** no existe riesgo de falla;
- **1:** existe riesgo de falla.

La red no entrega directamente un 0 o un 1. Primero genera una probabilidad. Por ejemplo, un resultado de `0.20` significa que el modelo estima un 20 % de probabilidad de riesgo. Esa probabilidad se compara con un **umbral**. Con un umbral de 0,08, toda probabilidad igual o superior a 0,08 se clasifica como riesgo.

### Matriz de confusión

- **TP, verdadero positivo:** había riesgo y el modelo lo detectó.
- **TN, verdadero negativo:** no había riesgo y el modelo indicó que no lo había.
- **FP, falso positivo:** el modelo generó una alarma, pero no había riesgo.
- **FN, falso negativo:** sí había riesgo, pero el modelo no lo detectó.

En este laboratorio, un FN cuesta 10 unidades y un FP cuesta 1 unidad. Por eso es más importante evitar riesgos no detectados, aunque esto genere algunas falsas alarmas adicionales.

### Métricas utilizadas

- **Accuracy:** proporción total de predicciones correctas.
- **Precision:** de todas las alarmas emitidas, cuántas eran realmente riesgos.
- **Recall:** de todos los riesgos reales, cuántos detectó el modelo.
- **F1:** equilibrio entre *precision* y *recall*.
- **PR-AUC:** capacidad del modelo para separar la clase de interés cuando esta es poco frecuente. Cuanto mayor sea, mejor.
- **Loss o pérdida:** medida del error que la red intenta reducir durante el entrenamiento.

## 3. Explicación de cada celda de código

### Celda de código 1: preparación del entorno

Esta celda importa las herramientas que se usarán durante el laboratorio:

- NumPy y Pandas para trabajar con números y tablas;
- Matplotlib y Seaborn para crear gráficas;
- Scikit-learn para separar, escalar y evaluar los datos;
- TensorFlow/Keras para construir las redes neuronales.

También aplica un estilo visual a las gráficas y muestra la versión de TensorFlow. La comprobación de TensorFlow ayuda a confirmar que el entorno puede ejecutar el laboratorio.

### Celda de código 2: reproducibilidad y costos

Se fija la semilla `SEED = 42` en las distintas bibliotecas. Una semilla controla la generación de números aleatorios. Usar siempre la misma permite obtener resultados iguales o muy parecidos al repetir el experimento.

También se intenta activar el comportamiento determinista de TensorFlow. Finalmente se definen los costos didácticos:

- falso negativo: 10 unidades;
- falso positivo: 1 unidad.

Estos valores no representan dinero real. Sirven para expresar que omitir una falla es diez veces más grave que generar una falsa alarma.

### Celda de código 3: creación del dataset

Se generan 4.000 lecturas industriales sintéticas. “Sintético” significa que los datos fueron creados por código y no provienen de una empresa real.

Las variables se generan con distribuciones distintas para imitar comportamientos posibles de temperatura, presión, vibración, carga, corriente y tiempo desde el mantenimiento. Después se calcula un puntaje de riesgo que combina varias de esas variables, una relación no lineal y algo de ruido. Ese puntaje se convierte en una probabilidad y finalmente en la etiqueta `riesgo_falla`.

La celda muestra:

- las dimensiones del dataset: 4.000 filas y 7 columnas;
- las primeras filas;
- la cantidad y proporción de cada clase;
- una gráfica de la distribución de la variable objetivo.

El resultado más importante es que solo 293 filas, equivalentes al 7,325 %, pertenecen a la clase 1.

### Celda de código 4: auditoría de datos

Esta celda verifica que:

- no existan valores faltantes;
- no existan valores infinitos;
- la variable objetivo solo contenga 0 y 1.

Luego presenta estadísticas descriptivas de las variables: cantidad, media, desviación, mínimo, cuartiles y máximo. Las instrucciones `assert` detendrían la ejecución si alguna condición de calidad no se cumpliera. Como la auditoría fue superada, los datos están listos para continuar.

### Celda de código 5: separación en train, validation y test

El dataset se divide de esta manera:

- **train:** 2.400 filas, 60 %;
- **validation:** 800 filas, 20 %;
- **test:** 800 filas, 20 %.

La opción `stratify` mantiene una proporción semejante de casos de riesgo en los tres conjuntos. Por eso las tasas son 7,33 %, 7,25 % y 7,38 %, respectivamente.

Los índices también se revisan para confirmar que ninguna fila aparezca en más de un conjunto. *Train* sirve para aprender, *validation* para tomar decisiones y *test* para realizar la evaluación final.

### Celda de código 6: escalamiento

Las variables tienen unidades muy diferentes. Por ejemplo, la presión puede estar cerca de 6, mientras las horas desde el mantenimiento pueden llegar a 1.400. Esta diferencia puede dificultar el entrenamiento.

`StandardScaler` transforma cada variable para que en *train* tenga aproximadamente:

- media igual a 0;
- desviación estándar igual a 1.

El escalador aprende sus parámetros únicamente con *train*. Después utiliza esos mismos parámetros para transformar *validation* y *test*. Este orden evita que información de los conjuntos futuros influya en el entrenamiento.

### Celda de código 7: funciones de evaluación

Esta celda define cuatro funciones reutilizables:

1. `metricas_binarias` convierte las probabilidades en clases usando un umbral y calcula las métricas, la matriz de confusión y el costo total.
2. `buscar_umbral_costo` prueba 157 umbrales entre 0,02 y 0,80. Elige el que produce el menor costo y, si hay empate, favorece el mayor *recall*.
3. `graficar_historial` dibuja las pérdidas de entrenamiento y validación a lo largo de las épocas.
4. `graficar_matriz` presenta visualmente los TN, FP, FN y TP.

Definir estas funciones evita repetir código y garantiza que todos los modelos sean evaluados de la misma manera.

### Celda de código 8: baseline

El `DummyClassifier` es un modelo de referencia muy sencillo. No aprende relaciones entre las variables. Solo utiliza la proporción previa de las clases.

Como la clase 1 representa alrededor del 7 %, su probabilidad queda por debajo del umbral 0,5 y el baseline predice siempre la clase 0. Obtiene una *accuracy* de 0,928, pero un *recall* de 0,000, porque no detecta ninguno de los 58 riesgos de *validation*. Su costo es de 580 unidades.

Este resultado demuestra por qué una exactitud alta no significa necesariamente que el modelo sea útil.

### Celda de código 9: MLP inicial

Se construye una red neuronal multicapa o MLP con tres capas ocultas de 128, 64 y 32 neuronas. Las capas utilizan la activación ReLU y la salida usa una función sigmoide para producir una probabilidad entre 0 y 1.

La red se entrena durante 60 épocas. Una época es una pasada completa por los datos de entrenamiento. Durante el proceso se registran la pérdida, PR-AUC y *recall* tanto en *train* como en *validation*.

El menor `val_loss`, 0,2151, aparece en la época 8. Después, la pérdida de entrenamiento continúa bajando, pero la de validación deja de mejorar. Esto indica sobreajuste: la red memoriza cada vez más el conjunto de entrenamiento sin mejorar en datos nuevos.

### Celda de código 10: MLP regularizada

La segunda red es más pequeña: utiliza capas de 32 y 16 neuronas. Además incorpora:

- **L2:** penaliza pesos excesivamente grandes;
- **Dropout de 20 %:** desactiva aleatoriamente algunas conexiones durante el entrenamiento;
- **EarlyStopping:** detiene el proceso cuando `val_loss` deja de mejorar.

El entrenamiento terminó en la época 52, antes del máximo de 100. El mejor `val_loss` fue 0,2165 en la época 47 y se restauraron los pesos correspondientes al mejor momento. Aunque su pérdida mínima es parecida a la de la primera red, las curvas muestran un comportamiento más controlado y una menor tendencia al sobreajuste.

### Celda de código 11: selección del modelo y del umbral

Ambas redes producen probabilidades para *validation*. La función de búsqueda prueba diferentes umbrales y calcula el costo de cada alternativa.

Los resultados fueron:

| Modelo | Umbral | Recall | Precision | PR-AUC | FP | FN | Costo |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline | 0,500 | 0,000 | 0,000 | 0,072 | 0 | 58 | 580 |
| MLP inicial | 0,025 | 0,552 | 0,140 | 0,207 | 197 | 26 | 457 |
| MLP regularizada | 0,080 | 0,707 | 0,232 | 0,309 | 136 | 17 | 306 |

La MLP regularizada obtiene el menor costo, por lo que queda seleccionada con un umbral de 0,08. “Congelar” esta decisión significa que ya no puede cambiarse después de observar *test*.

### Celda de código 12: evaluación final en test

Esta celda abre el conjunto de *test* una sola vez. Incluye una protección que genera un error si se intenta repetir la evaluación en la misma sesión. El objetivo es impedir que *test* se utilice repetidamente para ajustar decisiones.

La MLP regularizada obtiene en *test*:

- *accuracy*: 0,782;
- *precision*: 0,205;
- *recall*: 0,678;
- F1: 0,315;
- PR-AUC: 0,316;
- 155 falsos positivos;
- 19 falsos negativos;
- costo total: 345 unidades.

El baseline tendría un costo de 590 unidades. La red, por tanto, reduce considerablemente el costo, aunque todavía deja riesgos sin detectar y produce bastantes falsas alarmas.

## 4. Explicación de las interpretaciones

### Interpretación 1: población y objetivo

Esta respuesta identifica qué representa la información y explica el desbalance. La idea principal es que solo una pequeña parte de las filas corresponde a riesgo. Por ello, predecir siempre “sin riesgo” daría una *accuracy* alta, pero sería inútil para detectar fallas.

### Interpretación 2: función de los conjuntos

La respuesta explica que cada conjunto tiene una función diferente. Separarlos evita que el modelo sea evaluado con los mismos datos que utilizó para aprender o para tomar decisiones. Consultar *test* antes del final sería parecido a conocer las preguntas de un examen antes de rendirlo.

### Interpretación 3: escalamiento y fuga

El escalamiento permite que variables con unidades diferentes sean comparables para la red. Las medias de *validation* y *test* no son exactamente cero porque el escalador no se ajustó con ellas. Eso es correcto: utilizar esos conjuntos durante el ajuste permitiría que información futura se filtrara al proceso de entrenamiento.

### Interpretación 4: baseline y desbalance

El baseline sirve como mínimo de comparación. Su *accuracy* parece buena, pero no detecta ningún riesgo. La interpretación demuestra que deben priorizarse métricas relacionadas con la clase minoritaria y el costo real de los errores.

### Interpretación 5: diagnóstico de la MLP inicial

Cuando `train_loss` baja y `val_loss` empeora, existe sobreajuste. La red funciona mejor con los datos que ya conoce, pero pierde capacidad para generalizar. El punto mínimo de validación se produce temprano, en la época 8, aunque el entrenamiento continúa hasta la 60.

### Interpretación 6: comparación de las curvas

La regularización intenta controlar el sobreajuste. `EarlyStopping` evita seguir entrenando cuando ya no hay una mejora útil. La segunda red no necesariamente logra una pérdida mucho menor, pero presenta un proceso más estable y finalmente obtiene mejores métricas y menor costo en *validation*.

### Interpretación 7: selección con validation

El umbral de 0,08 es mucho menor que 0,5. Esto hace que la red sea más sensible: detecta más riesgos, pero también genera más falsas alarmas. La elección es coherente con el costo definido, porque dejar pasar una falla es diez veces más grave que emitir una alarma incorrecta.

La decisión se toma únicamente con *validation*. Después se congela para evitar seleccionar el modelo que, por casualidad, resulte mejor en *test*.

### Interpretación 8: resultado final

En *test*, la red detectó 40 de 59 riesgos y dejó 19 sin detectar. También generó 155 falsas alarmas. Los resultados son un poco inferiores a los de *validation*, pero no muestran una caída extrema. La PR-AUC incluso es muy similar. Esto sugiere que el desempeño se mantiene razonablemente estable en datos nuevos.

## 5. Cómo entender la conclusión técnica

La conclusión no afirma que el modelo esté listo para controlar una operación industrial real. Recomienda un **piloto controlado** por estas razones:

- supera claramente al baseline;
- reduce el costo de 590 a 345 unidades en *test*;
- detecta aproximadamente el 67,8 % de los riesgos;
- su comportamiento entre *validation* y *test* es relativamente consistente.

Sin embargo, todavía existen limitaciones importantes:

- los datos son sintéticos;
- solo hay 293 casos positivos en todo el dataset;
- los costos son didácticos y no fueron definidos por una empresa;
- se utilizó una única partición de los datos;
- la baja *precision* implica muchas falsas alarmas;
- no se evaluaron cambios de comportamiento a través del tiempo;
- no se estudió todavía la explicación individual de las predicciones.

Un piloto controlado significa probar el sistema en un entorno limitado, mantener supervisión humana y no automatizar decisiones críticas. Durante ese piloto deberían registrarse las falsas alarmas, las fallas no detectadas y la utilidad real de cada alerta. Solo después de validar el modelo con datos industriales reales podría considerarse un despliegue más amplio.

## 6. Idea central del laboratorio

El mejor modelo no es necesariamente el que tiene la mayor *accuracy*. En un problema con pocos casos de riesgo, lo importante es analizar qué errores comete, cuánto cuestan esos errores y si el desempeño se mantiene en datos no utilizados durante el desarrollo. En este experimento, la MLP regularizada con umbral 0,08 ofrece el mejor equilibrio bajo los costos establecidos, pero todavía requiere validación y supervisión antes de cualquier uso real.
