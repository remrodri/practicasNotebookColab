# GUÍA DE TRABAJO — PROYECTO INTEGRADOR

## Grupo 06 — AndinaLog
### Subcaso 03B — Operaciones y Planificación de Datos

---

# 1. Objetivo del proyecto

El trabajo del Subcaso 03B tiene como mandato:

> **Proteger la cadena de frío, mejorar la rotación del inventario y anticipar desviaciones térmicas durante el transporte.**

El proyecto debe trabajar a partir de los archivos **Bronze**, los cuales contienen problemas de calidad introducidos intencionalmente.

El flujo general de trabajo será:

```text
BRONZE
   ↓
DIAGNÓSTICO DE CALIDAD
   ↓
REGLAS DE TRATAMIENTO
   ↓
CURACIÓN
   ↓
SILVER
   ↓
VALIDACIÓN
   ↓
INTEGRACIÓN / JOINS
   ↓
DATASETS ANALÍTICOS
   ↓
EDA
   ↓
FEATURE ENGINEERING
   ↓
APRENDIZAJE SUPERVISADO
   ↓
EVALUACIÓN
   ↓
INTERPRETACIÓN
```

> **IMPORTANTE:** No se debe utilizar directamente el Silver de referencia entregado por el curso para evitar el proceso de preparación. El equipo debe construir su propio Silver a partir de Bronze.

---

# 2. Organización de los datos

Los archivos originales deben conservarse sin modificaciones.

Estructura conceptual recomendada:

```text
datos/
│
├── bronze/
│   ├── andinalog_iot_telemetry.csv
│   ├── andinalog_productos.csv
│   ├── andinalog_inventory_tracking.csv
│   ├── andinalog_flota.csv
│   ├── ...
│
├── diagnosticados/
│
├── cuarentena/
│
├── silver/
│
└── analiticos/
```

La regla fundamental es:

```text
BRONZE = original
```

Nunca sobrescribir los archivos Bronze.

---

# 3. Identificar las fuentes necesarias

No es necesario integrar todos los CSV de AndinaLog en una sola tabla.

Cada evidencia requiere determinadas fuentes.

## Evidencia 1 — Excursiones térmicas

Objetivo:

**Analizar excursiones térmicas por producto, viaje, camión y categoría logística.**

Fuentes principales:

```text
IoT
+
Productos
+
Flota
```

---

## Evidencia 2 — Riesgo de vencimiento y merma

Objetivo:

**Analizar riesgo de vencimiento y merma según días en almacén y fecha de vencimiento.**

Fuentes principales:

```text
Inventory Tracking
+
Productos
```

---

## Evidencia 3 — Anticipación de desviaciones térmicas

Objetivo:

**Construir variables y reglas/modelos que permitan anticipar una desviación térmica durante los próximos 60 minutos.**

Fuentes principales:

```text
IoT
+
Productos
+
Flota
```

Variable objetivo disponible:

```text
desviacion_proximos_60min_flag
```

---

# 4. ETAPA 1 — Diagnóstico de datos Bronze

## Objetivo

Determinar qué problemas de calidad presenta cada fuente antes de modificarla.

El diagnóstico se realiza sobre:

```text
CSV BRONZE
```

y **no debe corregir todavía los datos**.

---

## 4.1 Cargar el dataset

Ejemplo conceptual:

```python
df = pd.read_csv(...)
```

Registrar como mínimo:

- número de filas;
- número de columnas;
- nombres de columnas;
- tipos de datos;
- granularidad esperada.

---

## 4.2 Declarar la unidad de observación

Antes de realizar transformaciones o joins debe conocerse qué representa una fila.

Ejemplos:

```text
IoT
1 fila = 1 lectura temporal de un viaje

Productos
1 fila = 1 producto

Flota
1 fila = 1 camión

Inventory Tracking
1 fila = 1 movimiento/lote
```

Esto será fundamental posteriormente para evitar joins incorrectos.

---

## 4.3 Detectar problemas de calidad

Revisar, según corresponda:

```text
Duplicados
Nulos
Vacíos
Identificadores inconsistentes
Fechas inválidas
Fechas con formatos diferentes
Valores no numéricos
Valores fuera de rango
Valores centinela
Unidades mezcladas
Categorías inconsistentes
Errores ortográficos
Texto semiestructurado
```

---

## 4.4 Identificar cuarentena

Cada registro problemático debe quedar identificado junto con el motivo.

Ejemplo conceptual:

```text
fila | problema
-----|---------------------
123  | FECHA_INVALIDA
240  | DUPLICADO
315  | UNIDAD_NO_RECONOCIDA
421  | VALOR_FUERA_RANGO
```

No significa necesariamente que todos esos registros serán eliminados.

Significa:

> **Este registro necesita una decisión de tratamiento.**

---

## SALIDA DE ETAPA 1

```text
Bronze intacto
+
Dataset diagnosticado
+
Detalle de problemas
+
Registros candidatos a cuarentena
```

---

# 5. ETAPA 2 — Tratamiento y curación

## Objetivo

Aplicar reglas justificadas a los problemas encontrados durante el diagnóstico.

Entrada:

```text
Dataset diagnosticado
+
Detalle de problemas
```

---

## 5.1 Definir reglas antes de corregir

Cada problema debe tener una regla documentada.

Ejemplo:

```text
Problema:
Identificador con espacios/minúsculas

Regla:
strip() + upper()

Resultado:
" p001 " → "P001"
```

Otro ejemplo:

```text
Problema:
Temperatura expresada en Fahrenheit

Regla:
Convertir a Celsius

Resultado:
°F → °C
```

---

## 5.2 Clasificar los tratamientos

Un registro puede:

```text
PROBLEMA
   │
   ├──→ corregirse
   │
   ├──→ normalizarse
   │
   ├──→ convertirse
   │
   ├──→ imputarse, si existe justificación
   │
   └──→ excluirse / permanecer en cuarentena
```

Toda decisión debe poder explicarse.

---

## 5.3 Mantener trazabilidad

Registrar:

```text
problema detectado
regla aplicada
filas afectadas
resultado
```

Idealmente:

```text
ANTES → REGLA → DESPUÉS
```

---

# 6. ETAPA 3 — Generación de Silver

Una vez aplicadas las reglas:

```text
BRONZE
   ↓
DIAGNÓSTICO
   ↓
TRATAMIENTO
   ↓
SILVER
```

El Silver constituye el dataset preparado para las siguientes etapas.

Ejemplo:

```text
andinalog_iot_telemetry_silver.csv
```

---

# 7. ETAPA 4 — Validación del Silver

Antes de realizar joins hay que comprobar que la curación produjo un dataset coherente.

Realizar una revisión básica de cada Silver:

```text
shape
info()
describe()
nulos
duplicados
tipos
rangos
categorías
claves
```

Especialmente revisar las claves que posteriormente serán utilizadas en joins:

```text
producto_id
camion_id
order_id
viaje_id
centro_distribucion
...
```

---

## IMPORTANTE — EDA individual

No es necesario realizar un **EDA industrial completo para cada CSV individual**.

El Silver individual necesita principalmente una **validación descriptiva suficiente para comprobar que quedó correctamente preparado**.

El EDA principal del proyecto se realizará posteriormente sobre los datasets analíticos construidos para cada evidencia.

---

# 8. ETAPA 5 — Integración y joins

Una vez preparados y validados los Silver necesarios se pueden relacionar.

Un JOIN significa:

> Incorporar información distribuida entre distintas tablas mediante claves comunes para construir el dataset requerido por una pregunta analítica.

No significa:

> Unir todos los CSV de AndinaLog en un único CSV gigante.

---

# 9. Regla fundamental de los joins

Antes de hacer un join:

```text
1. ¿Qué representa una fila de A?

2. ¿Qué representa una fila de B?

3. ¿Cuál es la clave?

4. ¿Cuál es la cardinalidad?

5. ¿Necesito agregar primero?

6. ¿Qué registros no tienen correspondencia?
```

Especial atención a relaciones:

```text
1 : 1
1 : N
N : 1
N : M
```

Los joins muchos-a-muchos no controlados pueden multiplicar registros y producir totales incorrectos sin generar errores de programación.

---

# 10. DATASET ANALÍTICO — Evidencia 1

## Excursiones térmicas

Fuentes:

```text
IoT Silver
+
Productos Silver
+
Flota Silver
```

Pero IoT contiene múltiples lecturas por viaje.

Por ello:

```text
IoT Silver
     ↓
GROUP BY
viaje_id
order_id
camion_id
producto_id
     ↓
1 registro resumido por viaje
```

Calcular, por ejemplo:

```text
n_lecturas
temperatura promedio
n_desviaciones
tuvo_desviacion
```

donde:

```text
tuvo_desviacion =
n_desviaciones > 0
```

Después:

```text
        Viajes agregados
              │
       ┌──────┴──────┐
       ↓             ↓
 producto_id      camion_id
       ↓             ↓
 Productos         Flota
       ↓             ↓
 categoría       tipo_camion
       └──────┬──────┘
              ↓
    DATASET EVIDENCIA 1
```

---

# 11. EDA — Evidencia 1

Ahora sí realizar el EDA orientado al problema industrial.

Preguntas posibles:

```text
¿Cuántos viajes tuvieron desviaciones?

¿Qué proporción de viajes presentó desviaciones?

¿Cómo varían según categoría logística?

¿Cómo varían según tipo de camión?

¿Qué productos aparecen asociados?

¿Cómo se comporta la temperatura?
```

Aquí el EDA tiene mayor valor que analizar IoT de manera aislada porque ya incorpora el contexto del producto y del vehículo.

---

# 12. DATASET ANALÍTICO — Evidencia 2

Fuentes:

```text
Inventory Silver
+
Productos Silver
```

Join mediante:

```text
producto_id
```

Construir variables relacionadas con:

```text
fecha_ingreso
fecha_salida
fecha_vencimiento
dias_en_almacen
cantidad_merma
categoria_logistica
```

---

## 12.1 Lotes aún almacenados

Una `fecha_salida` vacía puede representar:

```text
LOTE TODAVÍA EN ALMACÉN
```

No debe considerarse automáticamente un error.

Crear conceptualmente:

```text
aun_en_almacen
```

---

## 12.2 Días restantes para vencer

Construir:

```text
dias_para_vencer
```

utilizando:

```text
fecha_vencimiento
fecha_ingreso
dias_en_almacen
```

---

# 13. EDA — Evidencia 2

Analizar, entre otros:

```text
cantidad de lotes
merma total
días promedio en almacén
lotes aún almacenados
riesgo de vencimiento
categoría logística
```

Objetivo:

> Convertir información de inventario en evidencia relacionada con rotación, vencimiento y merma.

---

# 14. DATASET ANALÍTICO — Evidencia 3

## Anticipar desviación térmica próximos 60 minutos

Fuentes:

```text
IoT Silver
+
Productos Silver
+
Flota Silver
```

Aquí existe una diferencia fundamental respecto a la Evidencia 1:

**NO debemos reducir inmediatamente IoT a una fila por viaje.**

Necesitamos conservar la serie temporal.

---

# 15. Orden temporal

Cada viaje contiene múltiples lecturas.

Conceptualmente:

```text
VIAJE 001

t0 → t1 → t2 → t3 → ... → t23
```

Antes de crear variables temporales:

```text
ordenar por:

viaje_id
timestamp
```

Nunca aplicar directamente `shift()` o `rolling()` sobre todo el DataFrame sin separar los viajes.

---

# 16. Feature Engineering

A partir de las variables originales se pueden construir variables predictoras.

Ejemplos indicados para el proyecto:

```text
temperatura actual

humedad actual

temperatura anterior
(temp_lag1)

cambio de temperatura
(temp_pendiente)

distancia respecto al umbral permitido

categoría logística

tipo de camión
```

Ejemplo conceptual:

```text
temperatura actual = 5.5
temperatura anterior = 4.8

temp_pendiente =
5.5 - 4.8
= +0.7
```

La pendiente permite representar si la temperatura está aumentando o disminuyendo.

---

# 17. Variable objetivo

Para la Evidencia 3 existe:

```text
desviacion_proximos_60min_flag
```

Interpretación:

```text
0 → no ocurrirá desviación
    en los próximos 60 minutos

1 → ocurrirá desviación
    en los próximos 60 minutos
```

Por tanto:

```text
X = variables predictoras

y = desviacion_proximos_60min_flag
```

---

# 18. EDA orientado al modelado

Antes de entrenar un modelo analizar:

```text
distribución de y
proporción 0 / 1
temperatura vs target
humedad vs target
pendiente vs target
distancia al umbral vs target
categorías relevantes
datos faltantes
variables potencialmente problemáticas
```

El objetivo de este EDA ya no es solamente describir los datos.

Debe ayudar a responder:

> **¿Qué información podría permitir anticipar una desviación?**

---

# 19. ETAPA DE APRENDIZAJE SUPERVISADO

Hasta la Sesión 6 se ha introducido el flujo general de aprendizaje supervisado mediante regresión.

El patrón aprendido es:

```text
CONTRATO PREDICTIVO
       ↓
Definir X / y
       ↓
TRAIN / TEST
       ↓
BASELINE
       ↓
MODELO
       ↓
PREDICCIÓN
       ↓
MÉTRICAS
       ↓
INTERPRETACIÓN
       ↓
LIMITACIONES
```

---

# 20. Contrato predictivo

Antes de entrenar cualquier modelo se debe responder:

### Decisión

¿Qué decisión industrial pretende apoyar el modelo?

### Unidad de observación

¿Qué representa una fila?

### Momento de predicción

¿En qué momento estaría disponible la predicción?

### Target

¿Qué queremos predecir?

### Features

¿Qué información estará disponible cuando se realice la predicción?

### Validación

¿Cómo se separarán entrenamiento y prueba?

---

# 21. Separación Train / Test

Al tratarse de datos temporales, debe respetarse el orden temporal.

Conceptualmente:

```text
PASADO                              FUTURO

──────── TRAIN ──────────────│──── TEST ────→
```

No se debe permitir que información futura se utilice para predecir el pasado.

---

# 22. Baseline

Antes de evaluar un modelo más complejo debe establecerse una referencia simple.

Conceptualmente:

```text
BASELINE
    ↓
¿Mi modelo realmente mejora
respecto a una estrategia sencilla?
```

El baseline evita considerar útil un modelo únicamente porque produce predicciones.

---

# 23. Regresión — contenido visto hasta Sesión 6

En la Sesión 6 se trabajó con un problema cuyo objetivo era una variable numérica continua.

Se utilizaron conceptos como:

```text
DummyRegressor
LinearRegression
RandomForestRegressor
```

y métricas como:

```text
MAE
MSE
RMSE
R²
```

---

# 24. IMPORTANTE — El problema predictivo 03B

La Evidencia 3 de AndinaLog utiliza:

```text
desviacion_proximos_60min_flag
```

que tiene valores:

```text
0 / 1
```

Por tanto, el problema planteado por esta variable objetivo corresponde conceptualmente a una **predicción binaria**, no a la regresión numérica continua practicada en la Sesión 6.

Por ahora:

**NO seleccionar todavía el modelo final.**

Esperar a los contenidos posteriores del curso relacionados con este tipo de problema antes de definir definitivamente:

```text
algoritmos
métricas
umbral
evaluación
```

---

# 25. Estado actual del proyecto

Con los contenidos vistos hasta ahora, ya podemos definir:

```text
✓ Datos Bronze

✓ Diagnóstico de calidad

✓ Cuarentena

✓ Reglas de tratamiento

✓ Curación

✓ Silver

✓ Validación del Silver

✓ Granularidad

✓ Relaciones entre tablas

✓ Joins

✓ Dataset analítico

✓ EDA

✓ Feature Engineering básico

✓ X / y

✓ Train / Test

✓ Baseline

✓ Concepto de aprendizaje supervisado

✓ Regresión como técnica aprendida
```

Todavía no debemos cerrar:

```text
○ Modelo definitivo para Evidencia 3

○ Algoritmos definitivos

○ Métricas definitivas de clasificación

○ Ajuste de hiperparámetros

○ Modelo final

○ Recomendaciones finales

○ Entregables finales del proyecto
```

porque esos elementos dependen de contenidos que todavía no se han revisado.

---

# 26. Flujo de trabajo que debemos seguir

## FASE A — Preparación

```text
[ ] Identificar los Bronze necesarios
[ ] Conservar originales intactos
[ ] Declarar granularidad
[ ] Ejecutar diagnóstico
[ ] Registrar problemas
[ ] Definir cuarentena
[ ] Documentar reglas
[ ] Ejecutar tratamiento
[ ] Generar Silver
[ ] Validar Silver
```

## FASE B — Integración

```text
[ ] Seleccionar Silver según evidencia
[ ] Verificar claves
[ ] Verificar cardinalidad
[ ] Preagregar cuando corresponda
[ ] Ejecutar joins
[ ] Verificar filas sin correspondencia
[ ] Verificar que el join no multiplicó registros
[ ] Generar dataset analítico
```

## FASE C — Análisis

```text
[ ] EDA Evidencia 1
[ ] Interpretar excursiones térmicas

[ ] EDA Evidencia 2
[ ] Interpretar vencimiento y merma

[ ] EDA Evidencia 3
[ ] Analizar variables relacionadas con el target
```

## FASE D — Preparación predictiva

```text
[ ] Ordenar series temporalmente
[ ] Construir features
[ ] Definir X
[ ] Definir y
[ ] Revisar disponibilidad temporal de las variables
[ ] Separar Train / Test
[ ] Definir baseline
```

## FASE E — Modelado

```text
[ ] Esperar/completar contenido correspondiente del curso
[ ] Seleccionar algoritmos
[ ] Entrenar
[ ] Evaluar
[ ] Comparar con baseline
[ ] Interpretar
[ ] Documentar limitaciones
```

---

# 27. Regla de trabajo del proyecto

Antes de escribir código, preguntar siempre:

```text
1. ¿Qué evidencia estoy construyendo?

2. ¿Qué pregunta quiero responder?

3. ¿Qué fuentes necesito?

4. ¿Qué representa una fila?

5. ¿Los datos ya están curados?

6. ¿Necesito un join?

7. ¿Necesito agregar antes del join?

8. ¿Qué resultado espero obtener?

9. ¿Cómo voy a validar que es correcto?

10. ¿Qué conclusión industrial puedo obtener?
```

Esto evita crear notebooks con muchas operaciones que técnicamente funcionan pero no contribuyen a las evidencias requeridas.

---

# 28. Mapa maestro

```text
                     ANDINALOG 03B
                          │
                          ▼
                       BRONZE
                          │
                          ▼
                     DIAGNÓSTICO
                          │
                    ┌─────┴─────┐
                    ↓           ↓
                 válidos    cuarentena
                    │           │
                    └─────┬─────┘
                          ▼
                     TRATAMIENTO
                          │
                          ▼
                       SILVER
                          │
                    VALIDACIÓN
                          │
              ┌───────────┼───────────┐
              │           │           │
              ▼           ▼           ▼
           IoT       Productos      Flota
              \           |           /
               \          |          /
                └──────── JOIN ─────┘
                          │
                          ▼
                  DATASET ANALÍTICO
                          │
                   ┌──────┴──────┐
                   │             │
                   ▼             ▼
                  EDA       FEATURE ENGINEERING
                                 │
                                 ▼
                              X / y
                                 │
                                 ▼
                         TRAIN / TEST
                                 │
                                 ▼
                            BASELINE
                                 │
                                 ▼
                              MODELO
                                 │
                                 ▼
                           EVALUACIÓN
                                 │
                                 ▼
                         INTERPRETACIÓN
                                 │
                                 ▼
                    DECISIÓN / RECOMENDACIÓN
```

---

# 29. Principio final

Los notebooks utilizados durante las sesiones deben entenderse como herramientas para aprender cada etapa.

El **Proyecto Integrador no consiste en copiar y concatenar notebooks**.

El objetivo es construir un proceso coherente:

> **Problema industrial → datos → calidad → integración → análisis → variables → modelo → evidencia → interpretación → recomendación.**

Cada notebook, script, gráfico o modelo que se produzca debe poder ubicarse claramente dentro de ese flujo.