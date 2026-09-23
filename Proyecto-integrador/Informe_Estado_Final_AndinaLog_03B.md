# Informe consolidado para la defensa

## Grupo 06 — AndinaLog — Subcaso 03B

**Proyecto:** Operaciones y planificación de datos  
**Mandato:** proteger la cadena de frío, mejorar la rotación del inventario y anticipar desviaciones térmicas durante el transporte.  
**Zona horaria adoptada:** hora de Bolivia (`America/La_Paz`, UTC−4), salvo que una fuente declare explícitamente otra zona horaria.  
**Estado del documento:** consolidación técnica de lo realizado entre diagnóstico, tratamiento, integración, análisis exploratorio y modelado S6–S10.

---

## 1. Propósito del proyecto

El trabajo del Grupo 06 busca convertir las fuentes Bronze de AndinaLog en información confiable para tres necesidades del negocio:

1. Identificar excursiones térmicas por producto, viaje, camión y categoría logística.
2. Analizar riesgo de vencimiento y merma considerando permanencia en almacén y fecha de vencimiento.
3. Construir variables y modelos capaces de anticipar una desviación térmica durante los próximos 60 minutos.

La pregunta predictiva final es:

> Dada una lectura IoT válida y sin desviación térmica actual, ¿se producirá una desviación térmica durante los próximos 60 minutos del mismo viaje?

La predicción está planteada como apoyo a una decisión operativa: generar una alerta preventiva para que una persona revise el viaje, el equipo de refrigeración y el estado de la carga. No representa una orden automática ni demuestra la causa de la desviación.

---

## 2. Fuentes del subcaso 03B

La documentación oficial asigna nueve fuentes principales al rol 03B:

| Fuente | Entidad | Estado actual | Uso principal |
|---|---|---:|---|
| `andinalog_iot_telemetry.csv` | Lecturas de sensores por viaje | Diagnosticada y tratada | Evidencias térmicas y predicción a 60 min |
| `andinalog_productos.csv` | Maestro de productos | Diagnosticada y tratada | Categoría logística, temperatura requerida y tolerancia |
| `andinalog_inventory_tracking.csv` | Inventario por lote | Diagnosticada y tratada | Permanencia, vencimiento y merma |
| `andinalog_flota.csv` | Maestro de camiones | Diagnosticada y tratada | Tipo, capacidad y centro del camión |
| `andinalog_wms_orders.csv` | Órdenes y viajes | Diagnosticada y tratada | Relación viaje–orden–producto–camión |
| `andinalog_warehouse_costs.csv` | Costos y rotación por centro | Diagnosticada y tratada | Contexto de inventario y centros |
| `andinalog_flota_eventos.json` | Configuración y eventos de flota | Diagnosticada y tratada | Eventos anteriores a cada lectura |
| `andinalog_hr_drivers.csv` | Información de conductores | Pendiente de decisión formal | Fuente sensible; no necesaria para el modelo actual |
| `andinalog_bitacora_choferes.txt` | Observaciones de conductores | Pendiente de decisión formal | Información cualitativa no usada en el modelo actual |

Las dos fuentes pendientes no impiden responder las tres evidencias principales. Para cerrar formalmente el inventario deben diagnosticarse o registrarse como excluidas, explicando que no proporcionan variables necesarias y disponibles en el instante de predicción. En HR Drivers también debe aplicarse minimización o seudonimización de datos personales.

---

## 3. Criterios generales de calidad

La calidad se evaluó desde dos perspectivas complementarias:

- **Calidad técnica:** tipo de dato, formato, valores nulos, duplicados, claves, fechas, unidades y rangos.
- **Calidad del dominio:** plausibilidad para transporte y logística, conservación de productos, operación de camiones y secuencia temporal de los viajes.

Un valor puede ser matemáticamente válido y, al mismo tiempo, no ser operacionalmente aceptable. Por ejemplo, Kelvin es una escala física válida, pero no forma parte de las unidades operativas adoptadas por AndinaLog para la temperatura de cabina.

### 3.1 Separación entre diagnóstico y tratamiento

El diagnóstico:

- conserva los valores originales;
- detecta y clasifica los problemas;
- añade banderas por campo;
- registra el motivo del problema;
- determina si la fila debe pasar a cuarentena.

El tratamiento:

- parte de la salida diagnosticada;
- normaliza valores conocidos;
- convierte unidades cuando existe una regla justificable;
- aplica imputaciones trazables;
- conserva el valor original junto al valor tratado cuando corresponde;
- produce Silver y cuarentena final.

Esta separación permite explicar qué llegó desde Bronze, qué problema fue encontrado y qué decisión se aplicó después.

### 3.2 Estructura simplificada del diagnóstico

Para cada campo al que se aplica una regla se utilizan columnas como:

- `<campo>_en_cuarentena`
- `<campo>_motivo`

La cuarentena general de la fila se obtiene a partir de las banderas de los campos. No se necesita una columna textual redundante con todos los nombres de columnas problemáticas.

### 3.3 Valores centinela

Valores como `-999` representan ausencia o error de lectura, no una medición real. En diagnóstico se conservan y se marcan. Durante el tratamiento pueden convertirse a valor faltante analítico, manteniendo una bandera que preserve su origen.

### 3.4 Fechas y zona horaria

Por decisión del proyecto, una fecha sin zona horaria explícita se interpreta como hora de Bolivia. Solo se aplica otra zona cuando la fuente la declara expresamente. Por ello, una columna denominada `timestamp_utc` no debe crearse si el dato nunca fue recibido o convertido realmente a UTC.

Las fechas se validan por:

- posibilidad de parseo;
- formato consistente;
- secuencia temporal dentro de la entidad;
- compatibilidad entre inicio, lectura, evento, entrega y vencimiento;
- ausencia de uso de información futura en las variables predictoras.

---

## 4. Decisiones por fuente

### 4.1 IoT Telemetry

La unidad canónica es Celsius.

| Unidad recibida | Diagnóstico | Tratamiento esperado |
|---|---|---|
| `C` | Válida | Se conserva |
| `F` | No canónica y requiere tratamiento | Conversión documentada a Celsius |
| `K` | No esperada en el dominio operacional | Cuarentena |
| Otra o vacía | Inválida o no evaluable | Cuarentena o revisión según evidencia |

También se validaron:

- identificadores de viaje y camión;
- temperatura y humedad;
- rangos plausibles;
- centinelas como `-999`;
- duplicados;
- marcas de tiempo;
- coherencia con producto, orden, viaje y tipo de camión.

Resultado principal del tratamiento IoT:

- 28.920 filas Bronze.
- 28.677 filas Silver.
- 243 filas en cuarentena final.

### 4.2 Productos

Se validaron identificadores, categorías logísticas, temperatura requerida y tolerancia. Las categorías se normalizaron únicamente cuando la correspondencia era inequívoca. Las imputaciones se marcaron con una bandera y un motivo.

Resultado:

- 63 filas Bronze.
- 60 filas Silver.
- 3 filas en cuarentena final.
- 3 categorías y 2 temperaturas imputadas usando evidencia observada y reglas documentadas.

La categoría `Congelado` existe dentro del dominio. Un error ortográfico como `conjelado` puede normalizarse a `Congelado` cuando no existe ambigüedad.

### 4.3 Inventory Tracking

Se revisaron claves de lote y producto, centro, cantidades, fechas de entrada y salida, vencimiento y permanencia. Una fecha de vencimiento estimada no equivale a una fecha confirmada. Cuando se genera una estimación debe conservarse una bandera de imputación y no presentarse como dato observado.

Resultado:

- 6.040 filas Bronze.
- 5.980 filas Silver.
- 60 filas en cuarentena final.
- 18 fechas de vencimiento imputadas y marcadas.

### 4.4 Flota

Se adoptaron cinco centros válidos:

- Cochabamba
- La Paz
- Santa Cruz
- Oruro
- Tarija

Los tipos de camión válidos observados son `Seco` y `Refrigerado`. Se validaron identificador, centro, tipo y capacidad con criterios técnicos y operacionales.

Resultado:

- 32 filas Bronze.
- 30 filas Silver.
- 2 duplicados en cuarentena final.

La relación producto–camión debe interpretarse mediante la orden o el viaje. La presencia de un producto fresco o congelado asociada con un camión seco requiere revisión del contexto operativo; por sí sola no prueba la causa de una excursión térmica.

### 4.5 WMS Orders

Se validaron órdenes, viajes, productos, camiones, cantidades, fechas y componentes de cumplimiento. Expresiones inequívocas como `cincuenta` pueden convertirse a `50`, dejando evidencia de la transformación.

Durante la integración se encontró una cobertura IoT→WMS de 99,67 %. Las 95 lecturas no enlazadas corresponden a cuatro viajes cuyas órdenes quedaron en la cuarentena final de WMS. Las lecturas IoT siguen siendo observaciones válidas, pero no deben recibir datos inventados de una orden no confirmada.

### 4.6 Warehouse Costs

Se validaron centro, periodo, rotación y montos en bolivianos. Un registro de Tarija sin rotación pudo completarse usando la repetición coherente del mismo centro y periodo cuando la evidencia disponible permitía una correspondencia inequívoca. La imputación quedó marcada.

### 4.7 Flota Eventos JSON

El JSON fue aplanado desde la estructura camión→eventos. Se revisaron identificadores, configuración, fecha, tipo de evento, severidad, lectura y reconocimiento.

Resultado:

- 192 eventos diagnosticados.
- 184 eventos únicos en Silver.
- 8 copias duplicadas en cuarentena.
- 10 valores `N/D` marcados.
- 20 valores ausentes reconocidos y documentados en Silver.

Los eventos se integraron temporalmente sin utilizar información posterior a la lectura que se desea predecir.

---

## 5. Integración de datos y control de joins

La integración siguió las relaciones principales del subcaso:

- productos → inventario y telemetría;
- camiones → viajes y eventos;
- órdenes → viajes;
- centros → inventario, costos y flota.

Antes de cada unión se revisó la granularidad de las tablas. Las fuentes con múltiples registros por clave se agregaron o alinearon temporalmente antes del join para evitar productos cartesianos y multiplicación artificial de filas.

La tabla analítica principal conserva una fila por lectura IoT. Los eventos de flota se vinculan utilizando solamente el evento anterior disponible dentro de la ventana definida.

Resultado de la integración temporal:

- 28.677 lecturas preservadas.
- 184 eventos Silver integrados.
- 100 % de cobertura de configuración de camiones.
- 5.243 lecturas con algún evento previo dentro de 24 horas.
- 1.290 lecturas con una alerta térmica previa.

Los eventos fueron evaluados como variables predictoras, pero no mejoraron los modelos en validación. Esta conclusión también es un resultado válido: disponer de una fuente no obliga a conservarla si no añade capacidad predictiva medible.

---

## 6. Evidencias del subcaso

### 6.1 Evidencia 1: excursiones térmicas

La evidencia permite analizar:

- temperatura promedio de cabina por viaje;
- cantidad de lecturas con desviación térmica;
- porcentaje de viajes con desviación;
- distribución por producto;
- distribución por categoría logística;
- distribución por camión y tipo de camión.

Las agregaciones se realizan antes de unir tablas cuando dos fuentes tienen granularidades diferentes. Esto evita duplicar conteos y totales.

### 6.2 Evidencia 2: vencimiento y merma

La evidencia permite calcular:

- días de permanencia en almacén;
- días restantes hasta vencimiento;
- lotes que continúan en almacén;
- merma por categoría logística;
- relación descriptiva entre permanencia, vencimiento y merma.

Las fechas imputadas se distinguen de las confirmadas. Las conclusiones se presentan como asociaciones descriptivas y no como efectos causales.

### 6.3 Evidencia 3: alerta térmica a 60 minutos

La tabla de modelado incorpora:

- temperatura actual;
- temperatura rezagada;
- pendiente entre lecturas;
- temperatura requerida del producto;
- tolerancia;
- desvío respecto al umbral;
- atributos del producto, viaje y camión;
- eventos de flota disponibles antes de la lectura;
- objetivo futuro a 60 minutos.

El objetivo se construye dentro de cada viaje, ordenando por marca de tiempo. Las variables futuras usadas para formar el objetivo no se incluyen como predictores.

---

## 7. Modelado S6–S10

### 7.1 S6 — Regresión

Objetivo: estimar la magnitud máxima de la desviación térmica durante los próximos 60 minutos.

Población:

- 27.477 lecturas aptas para regresión.

División temporal por viajes:

- 796 viajes para ajuste.
- 180 para validación.
- 180 para prueba.
- 44 viajes excluidos como margen temporal.

Modelo seleccionado: Random Forest base.

Resultados en prueba:

- MAE: 0,739 °C.
- RMSE: 1,124 °C.
- R²: 0,607.
- Mejora de RMSE frente a Dummy: 37,61 %.

Limitación principal: dentro del subconjunto de excursiones reales, 56,9 % fueron estimadas con una magnitud menor o igual a cero. Por ello, la regresión sirve para explorar la magnitud, pero no debe utilizarse sola como mecanismo de alerta.

### 7.2 S7 — Clasificación tradicional

Objetivo: clasificar si se producirá una desviación térmica durante los próximos 60 minutos.

Población:

- 28.557 lecturas aptas.
- Prevalencia positiva: 4,63 %.

Modelo seleccionado: Random Forest base.

Resultados en prueba con el criterio usado en S7:

- Precision: 78,36 %.
- Recall: 45,26 %.
- F1: 0,574.
- PR-AUC: aproximadamente 0,526.
- ROC-AUC: 0,844.
- TN: 4.013.
- FP: 29.
- FN: 127.
- TP: 105.

En S7 se utilizó inicialmente un costo FN:FP de 5:1. Para la decisión final S10 se adoptó 10:1, de acuerdo con el ejercicio de red neuronal y con una mayor penalización por no detectar una futura desviación. Esta diferencia debe explicarse como evolución del supuesto operativo, no como dos criterios finales simultáneos.

### 7.3 S8 — Clustering

Objetivo: identificar perfiles de viaje sin usar el objetivo futuro para formar los grupos.

Se utilizó una fila por viaje y solamente los 796 viajes del conjunto de ajuste.

Resultado:

- `k=3` obtuvo el mejor silhouette: 0,3310.
- Clúster 0: 78 viajes; 100 % presentó desviación futura.
- Clúster 1: 309 viajes; perfil relativamente estable de cadena de frío.
- Clúster 2: 409 viajes; perfil asociado principalmente con operación seca.

El objetivo futuro se utilizó después del entrenamiento exclusivamente para describir los clústeres. Esto evita fuga de información.

### 7.4 S9 — MLP inicial

El MLP inicial se evaluó únicamente en validación. El conjunto de prueba permaneció cerrado.

Resultados de validación:

- Precision: 84,78 %.
- Recall: 25,83 %.
- F1: 0,396.
- PR-AUC: 0,360.
- ROC-AUC: 0,748.
- Mejor `val_loss`: época 7.

En la misma validación, Random Forest obtuvo PR-AUC 0,398 y recall 36,42 %. Por ello, el MLP inicial todavía no justificaba reemplazar al modelo clásico.

### 7.5 S10 — MLP regularizada y prueba final

Arquitectura adoptada:

- entrada numérica y categórica;
- capa Dense de 32 unidades con ReLU y L2;
- Dropout de 0,20;
- capa Dense de 16 unidades con ReLU y L2;
- salida sigmoide;
- L2 = 0,001;
- EarlyStopping sobre `val_loss`, `patience=8`, restaurando los mejores pesos.

El preprocesamiento se ajustó únicamente con el conjunto de entrenamiento. La selección del umbral se realizó con validación, aplicando un costo operativo FN:FP de 10:1. El umbral final fue 0,10.

Resultados del MLP en prueba:

- Precision: 71,33 %.
- Recall: 46,12 %.
- F1: 0,560.
- PR-AUC: 0,501.
- ROC-AUC: 0,850.
- TN: 3.999.
- FP: 43.
- FN: 125.
- TP: 107.
- Costo operativo: 1.293.

Con el mismo costo 10:1, Random Forest obtuvo un costo de 1.299. El MLP redujo el costo en solo 6 unidades. Random Forest conserva mejores valores de precision, F1 y PR-AUC, además de una explicación y operación más sencillas.

### 7.6 Decisión de modelo

El MLP demuestra que una red regularizada puede competir con el modelo clásico y obtener un costo ligeramente menor bajo el supuesto 10:1. La diferencia es pequeña y no demuestra una superioridad robusta.

La recomendación defendible es:

- conservar Random Forest como referencia operativa principal por desempeño global, estabilidad y facilidad de explicación;
- conservar el MLP como alternativa experimental;
- validar ambos con datos futuros antes de desplegar una alerta real;
- revisar el costo FN:FP con responsables de operación, porque 10:1 es un supuesto didáctico y no un costo económico confirmado por AndinaLog.

---

## 8. Matriz de trazabilidad de la red

### Problema y horizonte

Clasificación binaria por lectura IoT para anticipar una desviación térmica durante los próximos 60 minutos. La salida es una probabilidad destinada a una alerta preventiva con revisión humana.

### Split

División temporal por viaje completo: 796 viajes de ajuste, 180 de validación, 180 de prueba y 44 de margen. Ningún viaje aparece en dos conjuntos. Semilla 42.

### Arquitectura mínima

Preprocesamiento ajustado con entrenamiento → Dense(32, ReLU, L2) → Dropout(0,20) → Dense(16, ReLU, L2) → Dense(1, sigmoid).

### Control

L2=0,001, Dropout=0,20 y EarlyStopping con `patience=8`. Selección de arquitectura y umbral solamente con entrenamiento y validación.

### Baseline y métrica

Comparación contra Dummy, regresión logística, Random Forest y MLP. La métrica principal es PR-AUC por el desbalance de clases. También se informan recall, precision, F1, ROC-AUC, matriz de confusión y costo FN:FP=10:1.

### Test final

El test se abre una sola vez después de congelar población, variables, preprocesamiento, arquitectura y umbral. El MLP alcanza costo 1.293 y Random Forest 1.299 bajo el supuesto 10:1.

---

## 9. Limitaciones

1. Los datos son sintéticos y no representan automáticamente el comportamiento futuro de una flota real.
2. El costo 10:1 es un supuesto didáctico y necesita validación económica y operativa.
3. Una asociación entre evento, tipo de camión o categoría y desviación no demuestra causalidad.
4. La baja prevalencia de la clase positiva hace que accuracy sea una métrica poco informativa.
5. El recall final sigue siendo limitado: ambos modelos omiten una parte importante de las desviaciones futuras.
6. Los eventos anteriores no mejoraron los modelos en validación con las variables construidas.
7. Cuatro viajes no pudieron enriquecerse con WMS porque sus órdenes quedaron en cuarentena; corresponden a 95 lecturas IoT.
8. Las fechas imputadas de vencimiento son estimaciones y deben mantenerse diferenciadas de las confirmadas.
9. HR Drivers y la bitácora de choferes todavía requieren una decisión formal de diagnóstico o exclusión.
10. Antes de operación real se necesita validación temporal adicional, monitoreo de deriva y definición del procedimiento humano posterior a una alerta.

---

## 10. Uso responsable y participación humana

La alerta propuesta apoya a operadores y responsables logísticos. No debe utilizarse para sancionar automáticamente a conductores ni atribuir responsabilidad individual.

Los datos personales de HR Drivers deben excluirse del modelo salvo que exista una necesidad analítica demostrable, autorización y medidas de protección. Para el problema actual no se ha demostrado que los nombres u otros identificadores personales sean necesarios.

El proyecto utilizó herramientas de inteligencia artificial como apoyo para estructurar reglas, revisar código y redactar documentación. Las decisiones sobre dominio, tratamiento, variables, métricas y recomendaciones deben ser revisadas y asumidas por el equipo. Los resultados verificables provienen de los notebooks, datasets y salidas conservadas en el proyecto.

---

## 11. Estado de los entregables

| Entregable | Estado | Acción pendiente |
|---|---:|---|
| Diagnóstico y tratamiento de siete fuentes | Completo en contenido | Ejecutar y guardar los notebooks definitivos que aún no muestran salidas |
| Evidencias 1, 2 y 3 | Completo | Seleccionar gráficos y cifras finales para informe/presentación |
| S6–S9 | Completo y ejecutado | Añadir o uniformar la sección de reproducibilidad |
| S10 | Resultados completos | Ejecutar el notebook y guardar sus salidas visibles |
| Datos y diccionario | Desactualizado | Actualizar WMS, Warehouse Costs, eventos y dataset final |
| Matriz de trazabilidad general | Parcial | Añadir ubicaciones exactas y verificación de otro integrante |
| Matriz de trazabilidad S10 | Desactualizada | Sustituir población, prevalencia, split y resultados provisionales |
| Plan de correcciones | Desactualizado | Cerrar hallazgos ya resueltos; usarlo solo si aplica después de S12 |
| HR Drivers y bitácora TXT | Pendiente formal | Diagnosticar o justificar exclusión |
| Informe técnico PDF, máximo 6 páginas | Pendiente | Sintetizar este informe con gráficos y resultados centrales |
| Presentación, máximo 8 diapositivas/10 minutos | Pendiente | Preparar narrativa de defensa |

---

## 12. Reproducibilidad pendiente

Los notebooks definitivos deben terminar con una sección que muestre:

- versiones de Python y librerías;
- semilla utilizada;
- zona horaria adoptada;
- rutas relativas de entrada y salida;
- conteos de filas de entrada, Silver y cuarentena;
- parámetros del modelo;
- afirmación de que el notebook se reinició y ejecutó de principio a fin.

Actualmente varios notebooks de diagnóstico y tratamiento no guardan ejecuciones visibles. El notebook S10 tampoco conserva salidas en el archivo, aunque sus resultados estén registrados en el informe. Esto debe corregirse antes de entregar.

---

## 13. Guion de defensa técnica

### 1. Problema

“AndinaLog necesita proteger la cadena de frío y anticipar desviaciones térmicas durante los viajes. Nuestro objetivo predictivo fue detectar si una lectura sin desviación actual tendrá una desviación en los próximos 60 minutos.”

### 2. Calidad de datos

“Separamos diagnóstico de tratamiento. El diagnóstico conserva y marca el problema; el tratamiento normaliza, convierte o imputa solo cuando existe una regla justificable. Celsius es la unidad canónica, Fahrenheit se convierte y Kelvin se considera no esperado en este dominio.”

### 3. Integración

“La unidad principal es una lectura IoT. Controlamos cardinalidades y alineamos eventos usando solamente información anterior a cada lectura. Conservamos las 28.677 lecturas Silver y evitamos multiplicar filas.”

### 4. Objetivo y fuga de información

“El objetivo futuro se construyó dentro de cada viaje y las variables futuras no se usaron como predictores. Los viajes completos se separaron temporalmente para evitar que el mismo viaje apareciera en entrenamiento y prueba.”

### 5. Modelos

“Comparamos baselines, Random Forest y una red neuronal. Como la clase positiva representa 4,63 %, usamos PR-AUC, recall, precision, F1 y un costo que penaliza diez veces más un falso negativo.”

### 6. Resultado

“En test, el MLP obtuvo PR-AUC 0,501, recall 46,12 % y costo 1.293. Random Forest obtuvo costo 1.299 y mejores métricas globales. La diferencia de costo fue solo seis unidades.”

### 7. Decisión

“Recomendamos Random Forest como referencia operativa por su equilibrio, estabilidad y facilidad de explicación. El MLP queda como alternativa experimental. Ninguno debe desplegarse sin validación futura y sin confirmar el costo real de las alertas.”

### 8. Limitación

“El sistema todavía omite parte de las desviaciones futuras, los datos son sintéticos y no afirmamos causalidad. La alerta requiere revisión humana.”

---

## 14. Conclusión

El Grupo 06 ya dispone de la evidencia técnica necesaria para explicar el flujo completo del subcaso 03B: calidad de datos, tratamiento, integración, EDA, construcción del objetivo, prevención de fuga, comparación de modelos y evaluación final.

El resultado principal no consiste únicamente en entrenar una red neuronal. El proyecto demuestra una cadena trazable desde Bronze hasta la decisión operativa, conserva las anomalías y transformaciones, controla los joins, compara modelos con un baseline y reconoce las limitaciones.

Para considerar el proyecto listo para entrega todavía deben cerrarse tareas documentales y de reproducibilidad: ejecutar S10 y los notebooks definitivos pendientes, actualizar los tres Excel, formalizar la decisión sobre HR/TXT y preparar el informe PDF y la presentación.
