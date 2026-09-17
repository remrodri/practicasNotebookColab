# DEFINICIÓN DEL PROYECTO INTEGRADOR

## Grupo 06 — AndinaLog
### Subcaso 03B — Operaciones y Planificación de Datos

---

# 1. Contexto del proyecto

El Proyecto Integrador trabaja con el caso **AndinaLog**, utilizando datos sintéticos que representan diferentes componentes de su operación logística.

Los datos entregados se encuentran inicialmente en una capa **Bronze**, es decir, datos crudos que contienen deliberadamente problemas de calidad como:

- registros duplicados;
- identificadores inconsistentes;
- fechas en diferentes formatos;
- valores nulos;
- valores fuera de rango;
- categorías no estandarizadas;
- unidades mezcladas;
- texto semiestructurado.

Por tanto, el proyecto no consiste únicamente en analizar datos, sino en construir un proceso que permita pasar desde datos crudos hasta información preparada y útil para apoyar decisiones operativas.

---

# 2. Mandato del Subcaso 03B

El mandato establecido para **Operaciones y Planificación de Datos** es:

> **Proteger la cadena de frío, mejorar la rotación del inventario y anticipar desviaciones térmicas durante el transporte.**

Este mandato define tres áreas principales de trabajo:

```text id="6hveqh"
                   MANDATO 03B
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
      PROTEGER      MEJORAR      ANTICIPAR
      CADENA DE     ROTACIÓN     DESVIACIONES
        FRÍO       INVENTARIO     TÉRMICAS
          │            │            │
          ▼            ▼            ▼
     Transporte     Almacenes      Predicción
```

---

# 3. Propósito del análisis

El propósito del proyecto es transformar los datos operativos disponibles en **evidencia analítica que permita comprender y anticipar problemas relacionados con la cadena de frío y el inventario**.

El proceso general puede entenderse como:

```text id="61vrbz"
DATOS OPERATIVOS
      ↓
CALIDAD DE DATOS
      ↓
INTEGRACIÓN
      ↓
ANÁLISIS
      ↓
IDENTIFICACIÓN DE PATRONES
      ↓
PREDICCIÓN
      ↓
EVIDENCIA PARA LA TOMA
DE DECISIONES OPERATIVAS
```

---

# 4. Pregunta general del proyecto

A partir del mandato puede plantearse como pregunta orientadora:

> **¿Cómo pueden utilizarse los datos operativos de AndinaLog para identificar problemas en la cadena de frío y el inventario, y anticipar desviaciones térmicas durante el transporte?**

Esta pregunta sirve como orientación del trabajo, mientras que las tres evidencias establecidas por la documentación determinan los análisis concretos que deben realizarse.

---

# 5. Objetivo general de trabajo

## Objetivo general

**Preparar, integrar y analizar los datos operativos de AndinaLog para generar evidencia sobre las excursiones térmicas y el riesgo de vencimiento y merma, y construir variables que permitan anticipar desviaciones térmicas durante el transporte.**

El objetivo puede visualizarse así:

```text id="2z33z3"
PREPARAR
   +
INTEGRAR
   +
ANALIZAR
   ↓
DATOS DE ANDINALOG
   ↓
┌──────────────┬───────────────┬────────────────┐
│              │               │
▼              ▼               ▼
Excursiones   Vencimiento    Desviaciones
térmicas      y merma        próximos 60 min
```

---

# 6. Objetivos específicos

## Objetivo específico 1 — Calidad de datos

**Diagnosticar y tratar los problemas de calidad presentes en los archivos Bronze necesarios para el análisis, documentando las reglas aplicadas y conservando la trazabilidad con los datos originales.**

Se busca pasar de:

```text id="znx7b6"
BRONZE
datos crudos
     ↓
diagnóstico
     ↓
tratamiento
     ↓
SILVER
datos preparados
```

---

## Objetivo específico 2 — Integración

**Integrar las fuentes de datos preparadas respetando su granularidad, claves y relaciones, con el fin de construir los datasets analíticos requeridos para cada evidencia.**

Esto implica controlar:

```text id="umr3zi"
granularidad
+
claves
+
cardinalidad
+
agregaciones
+
joins
```

y evitar relaciones muchos-a-muchos no controladas que puedan duplicar información.

---

## Objetivo específico 3 — Cadena de frío

**Analizar las excursiones térmicas por producto, viaje, camión y categoría logística para caracterizar el comportamiento de la cadena de frío durante el transporte.**

Corresponde a:

```text id="rv3y6c"
EVIDENCIA 1

IoT
 +
Productos
 +
Flota
 ↓
Excursiones térmicas
 ↓
producto
viaje
camión
categoría logística
```

---

## Objetivo específico 4 — Inventario

**Analizar el riesgo de vencimiento y merma considerando los días de permanencia en almacén y las fechas de vencimiento de los productos.**

Corresponde a:

```text id="0c36nh"
EVIDENCIA 2

Inventario
    +
Productos
    ↓
Permanencia
    +
Vencimiento
    +
Merma
    ↓
RIESGO DE INVENTARIO
```

---

## Objetivo específico 5 — Anticipación térmica

**Construir variables y reglas de alerta que permitan anticipar una desviación térmica durante los próximos 60 minutos utilizando la información temporal de los viajes y las características relevantes de productos y camiones.**

Corresponde a:

```text id="jtk6zv"
EVIDENCIA 3

IoT + Productos + Flota
          ↓
   Serie temporal
          ↓
 Feature Engineering
          ↓
Variables predictoras
          ↓
desviacion_proximos_60min_flag
          ↓
     ANTICIPACIÓN
```

---

# 7. Evidencias que debe producir el proyecto

La documentación establece tres evidencias principales.

## Evidencia 1

### Excursiones térmicas por producto, viaje, camión y categoría logística

Se busca determinar cómo se presentan las desviaciones térmicas dentro de las operaciones de transporte.

Las principales entidades involucradas son:

```text id="5z75v4"
IoT ──────── Producto
 │
 └────────── Camión
```

El análisis debe permitir pasar de simples lecturas de temperatura a información contextualizada por viaje, producto y vehículo.

---

# 8. Evidencia 2

### Riesgo de vencimiento y merma según días en almacén y fecha de vencimiento

Esta evidencia se concentra en el comportamiento del inventario.

Se deben relacionar:

```text id="j71tza"
LOTE
 │
 ├── producto
 ├── fecha ingreso
 ├── fecha salida
 ├── fecha vencimiento
 ├── días en almacén
 └── cantidad merma
```

El objetivo es producir evidencia sobre la permanencia del inventario y su relación con vencimiento y merma.

---

# 9. Evidencia 3

### Variables y reglas de alerta para anticipar una desviación térmica en los próximos 60 minutos

Esta evidencia introduce el componente predictivo del proyecto.

La pregunta fundamental es:

> **Con la información disponible en un determinado momento del viaje, ¿es posible anticipar que se producirá una desviación térmica durante los próximos 60 minutos?**

La variable objetivo disponible es:

```text id="uv4dxp"
desviacion_proximos_60min_flag
```

con interpretación:

```text id="q7oqi9"
0 → no ocurrirá desviación
    en los próximos 60 minutos

1 → ocurrirá desviación
    en los próximos 60 minutos
```

---

# 10. Información potencial para la anticipación

La documentación propone construir variables a partir de la serie temporal.

Entre ellas:

```text id="jy82g8"
Temperatura actual
       │
       ├── Temperatura anterior
       │
       ├── Tendencia / pendiente
       │
       └── Distancia al umbral
       
Humedad

Características del producto
       │
       ├── temperatura requerida
       ├── tolerancia
       └── categoría logística

Características del camión
       │
       └── tipo de camión
```

Estas variables constituirán candidatos para explicar o anticipar el comportamiento de la variable objetivo.

---

# 11. Fuentes principales

Para las tres evidencias principales se utilizarán especialmente:

| Fuente | Información principal |
|---|---|
| `andinalog_iot_telemetry` | Temperatura, humedad, viaje, producto, camión y desviaciones |
| `andinalog_productos` | Producto, categoría logística y requisitos térmicos |
| `andinalog_flota` | Características y tipo de camión |
| `andinalog_inventory_tracking` | Lotes, permanencia, vencimiento y merma |

Otras fuentes del subcaso pueden utilizarse cuando sean necesarias para análisis complementarios, pero no deben incorporarse únicamente por estar disponibles.

---

# 12. Relaciones principales

Las relaciones fundamentales son:

```text id="i21pc8"
PRODUCTOS
producto_id
    │
    ├────────→ IoT
    │
    └────────→ Inventario


FLOTA
camion_id
    │
    └────────→ IoT


IoT
viaje_id
order_id
camion_id
producto_id
```

Estas relaciones permiten enriquecer los eventos operativos con información contextual.

---

# 13. Qué NO busca el proyecto

El proyecto no consiste simplemente en:

```text id="p8j2m7"
✗ limpiar CSV por limpiar

✗ hacer gráficos porque sí

✗ unir todos los archivos disponibles

✗ producir un CSV gigante

✗ ejecutar modelos únicamente
  porque fueron enseñados en clase

✗ copiar los notebooks formativos
  y cambiar el nombre del dataset
```

Cada operación debe contribuir a alguna de las evidencias requeridas.

---

# 14. Qué SÍ busca el proyecto

El proyecto debe construir una cadena lógica:

```text id="g22ztg"
PROBLEMA INDUSTRIAL
        ↓
DATOS NECESARIOS
        ↓
CALIDAD
        ↓
DATOS CONFIABLES
        ↓
INTEGRACIÓN
        ↓
DATASET ANALÍTICO
        ↓
ANÁLISIS
        ↓
HALLAZGOS
        ↓
VARIABLES RELEVANTES
        ↓
PREDICCIÓN / ALERTA
        ↓
EVIDENCIA
        ↓
RECOMENDACIÓN
```

---

# 15. Resultado esperado del Módulo 3

Al finalizar el Módulo 3 se espera contar con:

```text id="7gxdze"
DATOS PREPARADOS
       +
DICCIONARIO ACTUALIZADO
       +
REGLAS DE LIMPIEZA
       +
VARIABLES RELEVANTES
       +
MÉTRICAS DEL MODELO
       +
RECOMENDACIONES
       +
LIMITACIONES
```

Estos resultados serán posteriormente utilizados como entrada para el Módulo 4.

---

# 16. Visión completa del proyecto

```text id="9qbj76"
                ANDINALOG
                    │
                    ▼
          PROBLEMA INDUSTRIAL
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
   Cadena de     Inventario   Anticipación
      frío                       térmica
       │            │            │
       ▼            ▼            ▼
 Evidencia 1    Evidencia 2   Evidencia 3
       │            │            │
       └────────────┼────────────┘
                    ▼
              DATOS BRONZE
                    │
                    ▼
           CALIDAD Y CURACIÓN
                    │
                    ▼
                 SILVER
                    │
                    ▼
           INTEGRACIÓN / JOINS
                    │
                    ▼
          DATASETS ANALÍTICOS
                    │
             ┌──────┴──────┐
             ▼             ▼
            EDA      FEATURE ENGINEERING
                           │
                           ▼
                     MODELADO / ALERTA
             │             │
             └──────┬──────┘
                    ▼
                EVIDENCIAS
                    │
                    ▼
                HALLAZGOS
                    │
                    ▼
             RECOMENDACIONES
```

---

# 17. Idea central que debe guiar el trabajo

Antes de realizar cualquier operación debemos poder responder:

> **¿Cómo contribuye esto a demostrar una de las tres evidencias del mandato de AndinaLog 03B?**

Si una limpieza, join, gráfico, variable o modelo no contribuye a responder una pregunta del proyecto, debe evaluarse si realmente es necesario.

El propósito final no es producir código.

El propósito es transformar los datos de AndinaLog en **evidencia analítica útil para comprender la cadena de frío, gestionar el riesgo de inventario y anticipar desviaciones térmicas durante el transporte**.