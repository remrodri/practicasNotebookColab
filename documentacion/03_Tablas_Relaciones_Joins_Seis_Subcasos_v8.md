**GIAD — Diplomado en Gestión Industrial y Analítica de Datos**

Módulo 3 — Proyecto Integrador · pandas

**Tablas, Relaciones, Campos y Joins Complejos**

**por Evidencia — Los Seis Subcasos (03B)**

_03 AndinaLog — Datos sintéticos v8 (Silver)_

Guía técnica de apoyo — Septiembre 2026

# Propósito y metodología

Este documento extiende a los seis subcasos del Módulo 3 el mismo análisis realizado para el Subcaso 01A (AITSA): para cada evidencia que el equipo debe producir, identifica qué archivos Silver usar, con qué granularidad (unidad de observación) llegan, qué claves permiten relacionarlos y qué unión (join) hay que preparar — incluyendo el orden de agregación y el riesgo específico de esa unión.

Cambios de la versión 8 que afectan a las uniones de este documento: rednexo_opex_costs pasa de 1 fila por zona-tecnología a un panel de 18 meses (378 filas), lo que exige agregar antes de unir en 02A-Evidencia 2; rednexo_nodos pasa de 15 a 30 nodos y cubre las 21 combinaciones zona-tecnología, lo que elimina el riesgo de NaN documentado en la versión anterior de 02B-Evidencia 1; y andinalog_client_satisfaction sube su cobertura de ~20% a ~49% de las órdenes, con un muestreo sesgado hacia pedidos que incumplieron OTIF (03A-Evidencia 1). Las fechas nuevas agregadas en v8 a los archivos de AITSA no alteran los joins descritos aquí.

## La regla que se repite en los seis subcasos: agregar antes de unir

Las tablas Silver de este proyecto conviven en al menos tres granularidades: dimensiones de una fila por entidad (clientes, técnicos, productos, cuadrillas...), hechos de una fila por evento/transacción (facturas, tickets, órdenes, movimientos de inventario...) y series de tiempo de muchas lecturas por entidad (telemetría IoT, eventos SCADA/NMS, desempeño de red). La ejecución de un join entre dos tablas de hechos o de series de tiempo exige un proceso de pre-agregación que homogenice su granularidad a un nivel de dimensión común; omitir ese paso produce un join muchos-a-muchos, y el resultado multiplica filas y las sumas posteriores quedan infladas sin que ningún mensaje de error lo advierta.

Por eso, en las 18 evidencias analizadas en este documento (3 por subcaso), el patrón dominante es: (1) declarar la granularidad de cada tabla de entrada, (2) pre-agregar cada tabla de hechos al nivel de dimensión con el que se va a unir, (3) unir con how="left" para no perder registros de la dimensión, y (4) completar valores faltantes de forma explícita (fillna(0) cuando la ausencia significa "no hubo evento", nunca cuando significa "dato no disponible").

## Subcasos cubiertos

| **Subcaso** | **Caso**            | **Rol**                                  |
| ----------- | ------------------- | ---------------------------------------- |
| 01A         | Caso 01 — AITSA     | Gerencia General y Dirección Estratégica |
| 01B         | Caso 01 — AITSA     | Dirección de Operaciones y PMO           |
| 02A         | Caso 02 — RedNexo   | Estrategia y Finanzas                    |
| 02B         | Caso 02 — RedNexo   | Tecnología y Operaciones                 |
| 03A         | Caso 03 — AndinaLog | Dirección Comercial y Clientes           |
| 03B         | Caso 03 — AndinaLog | Operaciones y Planificación de Datos     |

# Subcaso 03B — Operaciones y Planificación de Datos

**Caso 03 — AndinaLog · Mandato:** Proteger la cadena de frío, mejorar la rotación del inventario y anticipar desviaciones térmicas durante el transporte.

**Cruce principal (según la guía)**

Productos → inventario/telemetría; camiones → viajes/eventos; órdenes → viajes; centros → stock/costos/flota.

## Archivos Silver relevantes

| **Archivo**                             | **Granularidad**                              | **Acceso**         | **Rol en el análisis**                                 |
| --------------------------------------- | --------------------------------------------- | ------------------ | ------------------------------------------------------ |
| andinalog_iot_telemetry_silver.csv      | 1 lectura por viaje (28 800; 24 por viaje)    | Compartido         | Temperatura de cabina y bandera de desviación térmica. |
| andinalog_productos_silver.csv          | 1 producto                                    | Compartido         | Temperatura y tolerancia requeridas por producto.      |
| andinalog_flota_silver.csv              | 1 camión (30)                                 | Específico del rol | Tipo de camión y centro base.                          |
| andinalog_inventory_tracking_silver.csv | 1 movimiento de lote (6 000; 1 fila = 1 lote) | Compartido         | Días en almacén, merma y fecha de vencimiento.         |
| andinalog_warehouse_costs_silver.csv    | 1 centro (5)                                  | Específico del rol | Rotación de stock y pérdidas por merma por centro.     |

## Mapa de relaciones (claves)

| **Entidad origen**  | **Clave**        | **Entidad relacionada**                    | **Cardinalidad / sentido**                     |
| ------------------- | ---------------- | ------------------------------------------ | ---------------------------------------------- |
| andinalog_flota     | camion_id        | WMS / IoT / eventos                        | 1 camión → N viajes                            |
| andinalog_productos | producto_id      | inventario / IoT                           | 1 producto → N lotes / N lecturas              |
| centro_distribucion | clave conformada | WMS / inventario / costos / flota / RR.HH. | Dimensión conformada para capacidad y rotación |

## Evidencias que el equipo debe producir

### Evidencia 1. Excursiones térmicas por producto, viaje, camión y categoría logística

**Tablas de entrada y campos clave**

| **Tabla**                          | **Granularidad**         | **Campos usados**                                                                         |
| ---------------------------------- | ------------------------ | ----------------------------------------------------------------------------------------- |
| andinalog_iot_telemetry_silver.csv | 1 lectura (24 por viaje) | viaje_id, order_id, camion_id, producto_id, temperatura_cabina_c, desviacion_termica_flag |
| andinalog_productos_silver.csv     | 1 producto               | producto_id, categoria_logistica                                                          |
| andinalog_flota_silver.csv         | 1 camión                 | camion_id, tipo_camion                                                                    |

**Plan de unión**

1. Agregar telemetry a nivel viaje (groupby viaje_id, order_id, camion_id, producto_id): promedio de temperatura y conteo de lecturas con desviacion_termica_flag=1.
2. tuvo_desviacion = n_desviaciones > 0, a nivel viaje.
3. Unir el resultado por viaje con productos (producto_id) y flota (camion_id) — ambos N-a-1, seguros porque ya se agregó a nivel viaje.
4. Agrupar por (categoria_logistica, tipo_camion) para el resumen final.

**Join complejo — código verificado**

```
tel = pd.read_csv("andinalog_iot_telemetry_silver.csv")
productos = pd.read_csv("andinalog_productos_silver.csv")
flota = pd.read_csv("andinalog_flota_silver.csv")
```

```
viaje = tel.groupby(["viaje_id", "order_id", "camion_id", "producto_id"], as_index=False).agg(
    n_lecturas=("timestamp", "count"),
    temp_prom=("temperatura_cabina_c", "mean"),
    n_desviaciones=("desviacion_termica_flag", "sum"),
)
viaje["tuvo_desviacion"] = viaje["n_desviaciones"] > 0
```

```
viaje = viaje.merge(productos[["producto_id", "categoria_logistica"]], on="producto_id", how="left") \
    .merge(flota[["camion_id", "tipo_camion"]], on="camion_id", how="left")
```

```
resumen = viaje.groupby(["categoria_logistica", "tipo_camion"], as_index=False).agg(
    n_viajes=("viaje_id", "count"),
    pct_viajes_con_desviacion=("tuvo_desviacion", "mean"),
)
```

**Riesgo de unión.** Unir productos/flota directamente contra telemetry sin agregar antes no duplicaría filas (la relación sigue siendo N-a-1 lectura→producto), pero sí complica el cálculo de "viajes con desviación": contar lecturas con flag=1 sin agrupar por viaje sobre-representa los viajes con más lecturas afectadas frente a los que tuvieron una sola. Agregar a nivel viaje primero evita ese sesgo.

### Evidencia 2. Riesgo de vencimiento y merma según días en almacén y fecha de vencimiento

**Tablas de entrada y campos clave**

| **Tabla**                               | **Granularidad**                              | **Campos usados**                                                                                     |
| --------------------------------------- | --------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| andinalog_inventory_tracking_silver.csv | 1 movimiento (1 fila = 1 lote_id, confirmado) | lote_id, producto_id, fecha_ingreso, fecha_salida, fecha_vencimiento, cantidad_merma, dias_en_almacen |
| andinalog_productos_silver.csv          | 1 producto                                    | producto_id, categoria_logistica                                                                      |

**Plan de unión**

1. Convertir fecha_ingreso, fecha_salida y fecha_vencimiento a fecha (pd.to_datetime).
2. aun_en_almacen = fecha_salida.isna() — marca lotes que todavía no salieron (no deben tratarse como "ya gestionados").
3. dias_para_vencer = (fecha_vencimiento − fecha_ingreso).días − dias_en_almacen, como aproximación del margen restante.
4. Unir con productos por producto_id (N-a-1, seguro) para incorporar categoria_logistica.
5. Agrupar por categoria_logistica para el resumen de riesgo (merma total, días promedio en almacén, lotes aún en almacén).

**Join complejo — código verificado**

```
inv = pd.read_csv("andinalog_inventory_tracking_silver.csv")
```

```
inv["fecha_ingreso"] = pd.to_datetime(inv["fecha_ingreso"])
inv["fecha_salida"] = pd.to_datetime(inv["fecha_salida"])
inv["fecha_vencimiento"] = pd.to_datetime(inv["fecha_vencimiento"])
```

```
inv["aun_en_almacen"] = inv["fecha_salida"].isna()
inv["dias_para_vencer"] = (
    (inv["fecha_vencimiento"] - inv["fecha_ingreso"]).dt.days - inv["dias_en_almacen"]
)
```

```
riesgo = inv.merge(productos[["producto_id", "categoria_logistica"]], on="producto_id", how="left")
resumen_riesgo = riesgo.groupby("categoria_logistica", as_index=False).agg(
    n_lotes=("lote_id", "count"),
    merma_total=("cantidad_merma", "sum"),
    dias_prom_almacen=("dias_en_almacen", "mean"),
    lotes_aun_en_almacen=("aun_en_almacen", "sum"),
)
```

**Riesgo de unión.** A diferencia de otras tablas de hechos de este dataset, inventory_tracking ya es 1 fila por lote_id (verificado: sin duplicados), así que este join no tiene riesgo de fan-out. El riesgo aquí es de fechas: fecha_salida vacía no es un error, es un lote que sigue en almacén — tratarlo como 0 días o descartar la fila subestimaría el riesgo real de vencimiento.

### Evidencia 3. Variables y reglas de alerta para anticipar una desviación térmica en los próximos 60 minutos

**Tablas de entrada y campos clave**

| **Tabla**                          | **Granularidad**                                | **Campos usados**                                                                             |
| ---------------------------------- | ----------------------------------------------- | --------------------------------------------------------------------------------------------- |
| andinalog_iot_telemetry_silver.csv | 1 lectura (granularidad temporal, 24 por viaje) | viaje_id, timestamp, temperatura_cabina_c, humedad_cabina_pct, desviacion_proximos_60min_flag |
| andinalog_productos_silver.csv     | 1 producto                                      | producto_id, temperatura_conservacion_requerida_c, tolerancia_temperatura_c                   |
| andinalog_flota_silver.csv         | 1 camión                                        | camion_id, tipo_camion                                                                        |

**Plan de unión**

1. Unir telemetry con productos (producto_id) y flota (camion_id) — ambos N-a-1, seguros; esta parte es un join ordinario.
2. La complejidad no está en las claves sino en el ORDEN: desviacion_proximos_60min_flag es la variable objetivo de una serie temporal por viaje_id, así que hay que ordenar por (viaje_id, timestamp) antes de construir cualquier variable de rezago o tendencia.
3. Construir variables predictoras respetando ese orden: temperatura_cabina_c rezagada (shift), pendiente entre lecturas consecutivas, y distancia al umbral de tolerancia del producto.
4. Verificar que las 24 lecturas por viaje están completas (groupby(viaje_id).size()) antes de calcular rezagos, para no mezclar el final de un viaje con el inicio de otro.

**Join complejo — código verificado**

```
df = tel.merge(
    productos[["producto_id", "temperatura_conservacion_requerida_c", "tolerancia_temperatura_c"]],
    on="producto_id", how="left",
).merge(flota[["camion_id", "tipo_camion"]], on="camion_id", how="left")
```

```
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values(["viaje_id", "timestamp"])  # imprescindible antes de un shift()
```

```
df["desvio_respecto_umbral_c"] = (
    (df["temperatura_cabina_c"] - df["temperatura_conservacion_requerida_c"]).abs()
    - df["tolerancia_temperatura_c"]
)
df["temp_lag1"] = df.groupby("viaje_id")["temperatura_cabina_c"].shift(1)
df["temp_pendiente"] = df["temperatura_cabina_c"] - df["temp_lag1"]
```

```
# df["desviacion_proximos_60min_flag"] queda como variable objetivo (y) del modelo
```

**Riesgo de unión.** Un shift() o rolling() aplicado sin ordenar antes por (viaje_id, timestamp) — o aplicado sobre todo el DataFrame sin agrupar por viaje_id — mezclaría la última lectura de un viaje con la primera del siguiente, generando una variable de rezago sin sentido físico. En series de tiempo por entidad, el orden y el agrupamiento son parte del "join" tanto como la clave.

# Recomendaciones transversales para los seis equipos

Los 18 cruces analizados en este documento — tres por cada uno de los seis subcasos — repiten un número reducido de patrones de riesgo. Reconocerlos acelera la revisión de cualquier unión nueva que el equipo necesite construir más allá de las evidencias mínimas.

## 1\. Agregar antes de unir (muchos-a-muchos)

Aparece en 01A (cashflow/tickets → proyecto), 01B (hr_costs/tickets → técnico), 02A (crm_billing → zona×tecnología; y, desde v8, opex_costs → zona×tecnología, que pasó de 1 fila a un panel de 18 meses) y 02B (hr_schedules/support_log → cuadrilla). La prueba rápida: si dos tablas de hechos comparten una clave y ninguna de las dos es la dimensión, agréguelas por separado antes de unirlas.

## 2\. Cobertura parcial de claves (no toda fila tiene contraparte)

aitsa/rednexo/andinalog comparten este patrón: desde v8, ≈49% de las 7.500 órdenes de AndinaLog tienen evaluación de satisfacción (antes 20%), y esa cobertura está además sesgada hacia pedidos con problemas de entrega; solo 1.800 de 10.000 abonados de RedNexo tienen un ticket. La cobertura de nodos de RedNexo, en cambio, se resolvió en v8: 30 nodos cubren ahora las 21 combinaciones zona-tecnología de CRM (antes 15, cobertura parcial). En los casos que persisten, how="left" (u "outer") y un fillna explícito documentado es la respuesta correcta — how="inner" descarta silenciosamente la mayoría de los registros; y cuando la cobertura además está sesgada (no solo incompleta), como en la satisfacción de AndinaLog, ni siquiera el fillna resuelve el problema: hay que declarar la dirección del sesgo.

## 3\. Unión de difusión (broadcast) entre distintos grados de granularidad

El costo de migración de RedNexo está a nivel zona, pero el ingreso y el OPEX están a nivel zona×tecnología (02A); los parámetros financieros de RedNexo son una tabla de una sola fila que se usa como constante, no como llave de unión. Confundir un broadcast con una suma duplica el costo total tantas veces como categorías de la dimensión más fina.

## 4\. Comparación de categorías ordinales (texto)

La brecha de certificación en 01B y el nivel de experiencia en 02B comparan campos de texto ("Junior", "Intermedio", "Senior") que deben mapearse a un rango numérico antes de poder restarse o promediarse.

## 5\. Atribución indirecta (puente de varios saltos)

El costo de devolución de AndinaLog vive en client_satisfaction (granularidad: 1 fila por orden) pero se necesita a nivel cliente: hace falta pasar por wms_orders como tabla puente (order_id → cliente_id) antes de agregar (03A, Evidencia 2). La merma de inventario, a nivel producto/lote, exige un supuesto explícito de reparto si se quiere atribuir a un cliente.

## 6\. Orden temporal dentro de una entidad (series de tiempo)

Construir variables de rezago o tendencia (telemetría de AITSA, RedNexo o AndinaLog) exige ordenar por (entidad_id, timestamp) y agrupar por esa misma entidad antes de aplicar shift() o rolling(); de lo contrario se mezclan lecturas de instalaciones, nodos o viajes distintos.

_Estos seis patrones son, en conjunto, la aplicación concreta de los "Criterios mínimos de integración" de la guía de datos sintéticos del Proyecto Integrador: declarar la granularidad antes de relacionar, construir dimensiones conformadas y medidas explícitas, comprobar integridad de claves, evitar uniones muchos-a-muchos no controladas y diferenciar hechos observados de inferencias analíticas._