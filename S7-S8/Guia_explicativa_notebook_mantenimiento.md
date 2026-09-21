# Guía explicativa del notebook de clasificación y segmentación industrial

## Visión general

El notebook construye dos herramientas complementarias:

1. Un modelo de **clasificación** que estima si un equipo fallará en el próximo turno.
2. Un modelo de **clustering** que agrupa observaciones con condiciones operativas parecidas.

La lógica completa es:

```text
Datos históricos
   ├─ Clasificación → probabilidad de falla → alerta de inspección
   └─ Clustering → régimen operativo → nivel de prioridad
```

---

## 0. Identificación del grupo

```python
NUMERO_GRUPO = "G6"
INTEGRANTES = [...]
```

### ¿Qué intenta hacer?

Identificar quién entrega el trabajo. Esta información no participa en el modelo.

### ¿Qué hace el código?

Guarda el grupo y los nombres en variables y luego los imprime. Los `assert` que debían verificar la información están comentados con `#`, por lo que actualmente no se ejecutan.

---

# Parte A: clasificación supervisada

“Supervisada” significa que el algoritmo recibe ejemplos históricos donde ya se sabe si hubo o no una falla.

## 1. Librerías y ubicación del dataset

El código importa herramientas para leer datos, completar valores faltantes, entrenar modelos, calcular métricas y generar tablas y gráficos.

Después busca el archivo CSV en varias ubicaciones. El resultado fue:

```text
Dataset: /content/GIAD-M3-S07_Laboratorio_2_Dataset_Silver.csv
```

Esto indica que el notebook fue ejecutado en Google Colab y encontró allí el archivo.

---

## 2. Carga y auditoría del dataset

```python
df = pd.read_csv(RUTA)
```

`df` es una tabla de pandas llamada DataFrame.

### Dimensiones

```text
Dimensiones: (900, 15)
```

Significa que existen 900 observaciones y 15 variables. Cada fila representa una observación de un equipo.

### Tipos de datos

El notebook encuentra variables de texto, números decimales y números enteros. Esto importa porque las variables numéricas y categóricas necesitan tratamientos diferentes.

### Valores faltantes

Hay faltantes en:

- `turno`: 9;
- `temperatura_c`: 22;
- `presion_bar`: 18;
- `corriente_a`: 14.

No se eliminan esas filas. Más adelante, el `Pipeline` completará los valores mediante imputación.

### Variable objetivo

```python
TARGET = "falla_proximo_turno"
```

Esta es la respuesta que se busca predecir:

- `0`: no fallará;
- `1`: fallará.

Los datos contienen 798 casos sin falla y 102 con falla. Como la columna solo contiene ceros y unos, su promedio es la proporción de unos:

```text
102 / 900 = 11.33 %
```

### Conexión con la interpretación grupal 1

La respuesta del grupo es correcta. Si un supuesto modelo respondiera siempre “no habrá falla”, acertaría los 798 casos sin falla:

```text
798 / 900 = 88.67 %
```

Aunque la accuracy parece alta, ese modelo detectaría cero de las 102 fallas. Por eso la accuracy puede engañar cuando una clase es mucho más frecuente que la otra.

---

## 3. Contrato predictivo

Esta sección no ejecuta código. Define cómo se utilizará el modelo.

- **Clase positiva:** `falla_proximo_turno = 1`.
- **Horizonte:** se predice el siguiente turno.
- **Acción:** una alerta debe provocar una inspección preventiva, no una parada automática.
- **Falso negativo:** el modelo dice “sin falla”, pero el equipo sí falla.
- **Falso positivo:** el modelo alerta, pero el equipo no falla.

### Métrica primaria: recall

El recall responde:

> De todas las fallas que realmente ocurrieron, ¿qué proporción detectamos?

```text
recall = fallas detectadas / fallas reales
```

### Contramétrica: precisión o cantidad de alertas

No basta con detectar muchas fallas. También se debe evitar producir tantas falsas alarmas que mantenimiento no pueda revisarlas.

La interpretación grupal 2 establece correctamente este equilibrio.

---

## 4. Selección de variables: X e y

```python
X = df[variables_predictoras].copy()
y = df[TARGET].copy()
```

En aprendizaje automático:

- `X` contiene la información utilizada para predecir;
- `y` contiene la respuesta correcta.

El resultado fue:

```text
X shape: (900, 10)
y shape: (900,)
```

Se utilizan variables como temperatura, vibración, presión, corriente, carga, horas desde mantenimiento y alarmas.

### Variables excluidas

Se excluyen `registro_id`, `timestamp_utc` y `equipo_id` porque son identificadores o metadatos. También se excluye `orden_correctiva_post_evento` porque se genera después de la falla.

Usar esta última sería parecido a intentar predecir el ganador de un partido utilizando una noticia escrita después del partido.

### Conexión con la interpretación grupal 3

La explicación del grupo es correcta. Incluir información posterior al evento podría mejorar artificialmente las métricas, pero el modelo no dispondría de ella al realizar una predicción real. Eso sería una fuga de información.

---

## 5. División en entrenamiento y prueba

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
```

Los datos se dividen en:

- entrenamiento: 720 registros para aprender;
- prueba: 180 registros para evaluar al final.

La analogía sería: entrenamiento es el material para estudiar y test es el examen final.

### Parámetros importantes

- `test_size=0.20`: reserva 20% para test.
- `random_state=42`: permite repetir la misma división.
- `stratify=y`: conserva aproximadamente la proporción de fallas.

Resultados:

```text
Train: 11.39 % de fallas
Test:  11.11 % de fallas
```

La interpretación grupal dice que ambas proporciones son exactamente iguales. Más precisamente, son muy parecidas, pero no idénticas.

---

## 6. Modelo baseline

```python
baseline = DummyClassifier(strategy="most_frequent")
```

Este modelo siempre responde “sin falla”. Se utiliza como punto de comparación mínimo.

### Matriz de confusión

```text
[[160   0]
 [ 20   0]]
```

| | Predijo sin falla | Predijo falla |
|---|---:|---:|
| Realmente sin falla | 160 | 0 |
| Realmente falla | 20 | 0 |

Por tanto, obtiene 160 verdaderos negativos, 20 falsos negativos y ningún verdadero positivo.

### Métricas

```text
Accuracy:          88.89 %
Balanced accuracy: 50 %
Recall de falla:    0 %
```

La balanced accuracy promedia el desempeño sobre ambas clases. El modelo obtiene 100% para “sin falla” y 0% para “falla”, cuyo promedio es 50%.

### Conexión con la interpretación grupal 4

El baseline no protege a la planta: deja pasar las 20 fallas del test. Solo debe matizarse que la estratificación conserva aproximadamente la proporción y que el resultado demuestra 20 fallas sin alerta, no necesariamente “paradas constantes” en toda la operación futura.

---

## 7. Pipeline de preprocesamiento y modelo

El notebook identifica siete variables numéricas y tres categóricas.

### Variables numéricas

```python
SimpleImputer(strategy="median")
StandardScaler()
```

La imputación completa valores faltantes con la mediana del entrenamiento. La estandarización coloca las variables en escalas comparables.

### Variables categóricas

```python
SimpleImputer(strategy="most_frequent")
OneHotEncoder(handle_unknown="ignore")
```

Los faltantes se completan con la categoría más frecuente. Después, el one-hot encoding convierte las categorías en columnas binarias.

### Regresión logística

```python
LogisticRegression(max_iter=2000)
```

Aunque se llama “regresión”, aquí funciona como clasificador. Estima una probabilidad entre 0 y 1 de que ocurra una falla.

### Conexión con la interpretación grupal 5

El preprocesamiento vive dentro del `Pipeline` para que medianas, escalas y categorías se aprendan solo con el conjunto de entrenamiento. Calcularlas usando también test sería como conocer parte del examen antes de rendirlo.

La respuesta grupal es correcta: esta contaminación no suele producir errores de código; normalmente genera métricas demasiado optimistas.

---

## 8. Búsqueda de hiperparámetros

El notebook prueba ocho configuraciones:

```python
C = [0.05, 0.2, 1.0, 5.0]
class_weight = [None, "balanced"]
```

### Qué es C

`C` controla cuánto puede adaptarse la regresión logística a los datos. Un valor pequeño restringe más el modelo; un valor grande le da mayor libertad. Un valor mayor no es automáticamente mejor.

### Qué hace class_weight="balanced"

Da mayor importancia a los errores cometidos sobre la clase minoritaria, es decir, las fallas.

### Validación cruzada

```python
StratifiedKFold(n_splits=5)
```

El entrenamiento se divide en cinco partes. El modelo aprende con cuatro y se valida con la restante. El proceso se repite cinco veces.

### Resultado

```text
C = 0.05
class_weight = "balanced"
Balanced accuracy promedio = 0.8414
Desviación estándar = 0.0392
```

### Conexión con la interpretación grupal 6

La respuesta es correcta: ganan `C=0.05` y los pesos balanceados. Además, las configuraciones balanceadas presentan menor variación entre folds. “Alta estabilidad” debe entenderse como estabilidad relativa frente a las otras configuraciones probadas, no como garantía absoluta en producción.

---

## 9. Evaluación final en test

El mejor modelo se aplica al conjunto que permaneció aislado:

```python
y_pred = best_model.predict(X_test)
```

### Matriz de confusión

```text
[[146  14]
 [  1  19]]
```

| Resultado | Cantidad | Significado |
|---|---:|---|
| Verdadero negativo | 146 | No falló y no se alertó |
| Falso positivo | 14 | Se alertó, pero no falló |
| Falso negativo | 1 | Falló y no se alertó |
| Verdadero positivo | 19 | Falló y se alertó |

### Métricas

- **Accuracy: 91.67%**. Acertó 165 de 180 casos.
- **Recall: 95%**. Detectó 19 de las 20 fallas.
- **Precisión: 57.58%**. De las 33 alertas, 19 correspondieron a fallas.
- **F1: 71.70%**. Combina precisión y recall.
- **Balanced accuracy: 93.12%**. Promedia el reconocimiento de ambas clases.

### Conexión con la interpretación grupal 7

Los cálculos del grupo son correctos: hubo un falso negativo, 14 falsos positivos y 33 alertas totales.

Sin embargo, todavía no puede afirmarse que 33 alertas sean manejables sin conocer la capacidad de inspección. La siguiente sección establece un máximo de 25; bajo ese límite, 33 ya no serían viables.

---

## 10. Sensibilidad al umbral

La regresión logística produce una probabilidad. El umbral decide desde qué valor se genera una alerta.

```text
Probabilidad = 0.65

Umbral 0.50 → alerta
Umbral 0.80 → no alerta
```

### Resultados

| Umbral | FP | FN | TP | Precisión | Recall | Alertas |
|---:|---:|---:|---:|---:|---:|---:|
| 0.35 | 22 | 1 | 19 | 46.34% | 95% | 41 |
| 0.50 | 14 | 1 | 19 | 57.58% | 95% | 33 |
| 0.80 | 5 | 3 | 17 | 77.27% | 85% | 22 |

Al bajar el umbral se generan más alertas. Al subirlo, disminuyen las alertas y aumenta la precisión, pero se pueden perder más fallas.

### Conexión con la interpretación grupal 8

Si la planta puede atender como máximo 25 alertas, el único umbral admisible entre los tres es 0.80, con 22 alertas. El costo de esta decisión es pasar de detectar 19 de 20 fallas a detectar 17 de 20.

El mejor F1 no basta para decidir: también deben considerarse seguridad, costos y capacidad real de inspección.

---

# Parte B: clustering no supervisado

Aquí no se intenta predecir directamente una respuesta. Se buscan grupos naturales de condiciones operativas.

## 11. Preparación para clustering

Se emplean siete variables numéricas: temperatura, vibración, presión, corriente, carga, horas desde mantenimiento y alarmas.

Después se completan faltantes y se estandarizan las variables:

```python
Xc_imputado = imputer_c.fit_transform(Xc)
Xc_escalado = scaler_c.fit_transform(Xc_imputado)
```

La matriz resultante tiene 900 filas y siete variables.

### Por qué se estandarizan

K-Means utiliza distancias. Sin estandarización, una variable con números grandes podría dominar la agrupación únicamente por sus unidades.

Aquí se preparan las 900 observaciones juntas porque se realiza un análisis descriptivo del conjunto completo. Para usar el clustering en producción, se deberían guardar el imputador, el escalador y K-Means ya entrenados.

---

## 12. Por qué la falla no entra en K-Means

```python
EXCLUIR_CLUSTER = IDENTIFICADORES + FUGAS + [TARGET]
```

`falla_proximo_turno` no se utiliza para construir los clusters. El objetivo es encontrar regímenes físicos y operativos, no crear directamente un grupo de fallas y otro de no fallas.

Después de formar los grupos, sí se observa la tasa de falla de cada uno para describirlos.

### Conexión con la interpretación grupal 9

La respuesta es correcta. Si la falla entrara al clustering, la conclusión sería circular: el grupo tendría muchas fallas porque la propia variable de falla se utilizó para construirlo.

---

## 13. Selección de k

`k` es el número de clusters. El notebook prueba valores entre 2 y 6.

### Inercia

Mide qué tan cerca quedan las observaciones del centro de su cluster. Siempre tiende a disminuir al aumentar `k`, por lo que no se debe elegir el número de grupos mirando solo el menor valor.

### Silhouette

Mide simultáneamente qué tan cerca está cada observación de su propio cluster y qué tan separada está de los demás.

| k | Silhouette |
|---:|---:|
| 2 | 0.3082 |
| 3 | 0.2857 |
| 4 | 0.2592 |
| 5 | 0.2410 |
| 6 | 0.2429 |

`k=2` tiene el mejor silhouette. Sin embargo, 0.3082 representa una separación moderada, no extraordinariamente clara.

---

## 14. Perfil con k=2

### Cluster 0

- 492 observaciones;
- tasa de falla: 1.2%;
- menor temperatura, carga, vibración y tiempo desde mantenimiento;
- 0.25 alarmas en promedio.

### Cluster 1

- 408 observaciones;
- tasa de falla: 23.5%;
- mayor temperatura, vibración y carga;
- 321 horas desde mantenimiento;
- 1.18 alarmas en promedio.

Esta segmentación distingue básicamente un régimen relativamente normal y otro más exigido o deteriorado.

---

## 15. Perfil con k=3

### Cluster 0: bajo riesgo

- 438 observaciones;
- tasa de falla: 0.9%;
- menor temperatura, corriente y carga;
- pocas alarmas.

### Cluster 1: riesgo intermedio

- 325 observaciones;
- tasa de falla: 6.2%;
- carga y corriente elevadas;
- 189 horas desde mantenimiento;
- alarmas moderadas.

### Cluster 2: régimen crítico

- 137 observaciones;
- tasa de falla: 56.9%;
- vibración: 6.921 mm/s;
- 556 horas desde mantenimiento;
- aproximadamente dos alarmas recientes;
- temperatura elevada.

Aunque `k=3` tiene un silhouette ligeramente inferior, separa el grupo riesgoso del régimen intermedio.

### Conexión con la interpretación grupal 10

La respuesta está bien fundamentada: estadísticamente, `k=2` tiene mejor separación; operativamente, `k=3` ofrece tres niveles más útiles para mantenimiento.

Los números de cluster son etiquetas arbitrarias. En producción sería mejor llamarlos “bajo”, “intermedio” y “crítico” según sus características.

---

## 16. Validaciones automáticas

Los `assert` verifican que:

- existan 900 observaciones;
- el objetivo no entre en `X`;
- la variable de fuga quede excluida;
- entrenamiento y test tengan el tamaño esperado;
- gane `class_weight="balanced"`;
- el recall supere 90% con el umbral predeterminado;
- la falla no entre en K-Means;
- se prueben cinco valores de `k`.

El resultado fue:

```text
✓ Todas las validaciones fueron superadas.
```

Esto demuestra que el notebook siguió las reglas técnicas definidas. No demuestra por sí solo que el modelo esté listo para producción.

---

## 17. Interpretación grupal 11: recomendación final

La propuesta combina ambas herramientas:

```text
Alerta del clasificador
        +
Pertenencia al régimen crítico
        ↓
Prioridad de inspección
```

### Modelo recomendado

Regresión logística con `C=0.05` y `class_weight="balanced"`. La elección está respaldada por validación cruzada.

### Umbral recomendado

El grupo recomienda 0.80 porque produce 22 alertas y respeta el máximo de 25.

Existe un matiz importante: el recall de 95% corresponde al umbral 0.50. Con el umbral final de 0.80, el recall es 85%.

La recomendación correcta sería:

```text
El modelo detecta 95% con el umbral estándar de 0.50.
Al adaptarlo a la capacidad máxima de 25 inspecciones,
se utiliza 0.80 y se acepta un recall de 85%.
```

### Clustering recomendado

Se elige `k=3` por su utilidad operativa, aunque `k=2` tenga mejor silhouette.

### Precaución con la regla combinada

La frase “inspeccionar equipos del cluster 2 que además superen 0.80” exige cumplir ambas condiciones. Esto podría dejar sin inspección una alerta fuerte de otro cluster o un equipo crítico cuya probabilidad quede justo debajo de 0.80.

Sería más prudente trabajar con niveles de prioridad:

1. Probabilidad superior a 0.80: inspección prioritaria.
2. Pertenencia al cluster crítico: vigilancia o inspección reforzada.
3. Coincidencia de ambas señales: máxima prioridad.

Antes de usar la intersección como única regla, debería calcularse su propia matriz de confusión.

---

## 18. Exportación de resultados

El notebook crea dos archivos CSV auxiliares:

- predicciones del conjunto test;
- perfiles de los tres clusters.

El primero contiene el resultado real, la predicción y la probabilidad. El segundo resume las características de cada cluster. Sirven para documentar la ejecución, pero no son entregables separados.

---

## 19. Conclusión general

El notebook demuestra que, en estos datos:

- la accuracy por sí sola es engañosa;
- excluir información posterior al evento es indispensable;
- el modelo balanceado detecta muchas más fallas que el baseline;
- con umbral 0.50 detecta 19 de 20 fallas, pero genera 33 alertas;
- con umbral 0.80 genera 22 alertas, pero detecta 17 de 20 fallas;
- `k=3` identifica un régimen crítico con una tasa de falla de 56.9%.

No demuestra todavía que el sistema funcionará igual en una planta real. Para eso se necesitan datos nuevos, validación temporal, información de más equipos y una prueba piloto.

> Un modelo de mantenimiento no debe juzgarse solamente por cuántas predicciones acierta. Debe evaluarse por las fallas que detecta, las que deja escapar, las inspecciones que provoca y la capacidad real de la planta para actuar sobre sus alertas.

