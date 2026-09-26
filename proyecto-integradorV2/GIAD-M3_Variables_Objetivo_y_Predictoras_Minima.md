# Variables Objetivo y Predictoras Mínima

**Resumen**

| **Caso**      | **Modelo**          | **Variable objetivo**          | **Archivos utilizados** |
| ------------- | ------------------- | ------------------------------ | ----------------------- |
| 03B AndinaLog | Regresión logística | desviacion_proximos_60min_flag | 1 CSV                   |

## 03B AndinaLog — Desviación térmica futura

**Modelo:** regresión logística.

**Variable objetivo:**

desviacion_proximos_60min_flag

**Archivo mínimo:**

- andinalog_iot_telemetry.csv

No es indispensable realizar cruces para construir un primer modelo.

**Variables predictoras mínimas:**

- temperatura actual
- humedad actual
- desviacion_termica_flag
- temperatura de la lectura anterior
- variación de temperatura durante los últimos 30 minutos

**Unidad de observación:** una lectura de telemetría.

**Interpretación esperada:** identificar cuándo las condiciones actuales indican que podría producirse una desviación térmica durante la siguiente hora.

**No utilizar:** lecturas o eventos posteriores al instante de predicción.

La separación de entrenamiento y prueba debe hacerse por viaje u orden, para evitar que lecturas consecutivas del mismo viaje queden en ambos conjuntos.

# EDA común para los seis casos

Antes de graficar, el código debe mostrar automáticamente:

1. Número de filas y columnas.
2. Unidad de observación.
3. Duplicados y valores faltantes.
4. Tipos de datos.
5. Estadísticas descriptivas.
6. Verificación de que los cruces no multiplicaron registros.

Luego se realizan los gráficos específicos.

## 03B AndinaLog — Desviación térmica futura

**Modelo:** regresión logística.  
**Objetivo:** desviacion_proximos_60min_flag.  
**Unidad:** una lectura de telemetría.

| **Gráfico Seaborn** | **Variables**                                           | **Pregunta que responde**                                         |
| ------------------- | ------------------------------------------------------- | ----------------------------------------------------------------- |
| Countplot           | objetivo                                                | ¿Qué tan poco frecuentes son las desviaciones futuras?            |
| Histplot            | temperatura actual con hue del objetivo                 | ¿Las futuras desviaciones parten de temperaturas diferentes?      |
| Boxplot             | humedad actual por clase                                | ¿La humedad cambia antes de una desviación?                       |
| Barplot             | desviación actual vs. promedio del objetivo             | ¿Una desviación presente anticipa otra en la siguiente hora?      |
| Scatterplot         | temperatura actual vs. variación de 30 minutos, con hue | ¿La combinación de nivel y tendencia permite reconocer el riesgo? |

Gráfico opcional:

- lineplot de temperatura a través del tiempo para dos o tres viajes, marcando cuándo aparece la desviación futura.

Este gráfico permite observar que el modelo no solo considera una temperatura alta, sino también cómo está evolucionando.

**Interpretaciones esperadas:**

- fuerte desbalance de clases;
- temperatura y humedad previas a los eventos;
- importancia de la tendencia;
- diferencia entre desviación actual y desviación futura.